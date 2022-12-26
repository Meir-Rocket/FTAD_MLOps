import pandas as pd
import os
import ssl
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup


def get_regions(ctx):
    url = 'http://indicators.miccedu.ru/monitoring/2019/index.php?m=vpo'

    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all('a')

    regions = {}
    for region in result:
        if region.get('href').startswith('_vpo/material.php?type=2'):
            regions[str(region.text)] = region.get('href')

    return regions


def get_universities_data(url_univ, ctx):
    html = urllib.request.urlopen(url_univ, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    universities = {}
    result = soup.find_all('a')

    for university in result:
        if university.get('href').startswith('inst'):
            universities[str(university.text)] = university.get('href')

    basic_url = 'http://indicators.miccedu.ru/monitoring/2019/_vpo/'

    universities_data = {}

    for i in list(universities.keys()):
        print('Now searching for data about university: ' + str(i))
        url_current = str(basic_url + universities[i])
        html_current = urllib.request.urlopen(url_current, context=ctx).read()
        soup_current = BeautifulSoup(html_current, 'html.parser')

        result_current = soup_current.find_all('td')
        result_current1 = list(soup_current.find_all('td', attrs={'class': 'n'})[ijk]
                               for ijk in range(0, len(soup_current.find_all('td', attrs={'class': 'n'}))))

        l1 = []
        for ijk in range(0, len(result_current)):
            l1.append(result_current[ijk].text)

        l2 = []
        for ijk in result_current1[0:6]:
            l2.append(l1[int(l1.index(ijk.text)) + 1])

        for ijk in result_current1[6:]:
            l2.append(l1[int(l1.index(ijk.text)) + 2])

        universities_data[i] = l2
        print('It\'s done with ' + str(i))
        print('\n')

    return universities_data


def get_columns(ctx):
    url_for_columns = 'http://indicators.miccedu.ru/monitoring/2019/_vpo/inst.php?id=1944'

    html_for_columns = urllib.request.urlopen(url_for_columns, context=ctx).read()
    soup_for_columns = BeautifulSoup(html_for_columns, 'html.parser')

    columns = list(soup_for_columns.find_all('td', attrs={'class': 'n'})[ijk].text.strip()
                   for ijk in range(0, len(soup_for_columns.find_all('td', attrs={'class': 'n'}))))
    return columns


def run_parser():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    regs = get_regions(ctx)

    cols = get_columns(ctx)

    dataframe = pd.DataFrame(columns=cols)

    for i in regs:
        url_uni = 'http://indicators.miccedu.ru/monitoring/2019/' + regs[i]
        uni_data = get_universities_data(url_uni, ctx)
        df = pd.DataFrame.from_dict(uni_data, orient='index', columns=cols)
        dataframe = dataframe.append(df)

        print('*************\nNOW DONE WITH ' + str(i) + '\n*************\n')

    dataframe.to_excel(os.getcwd() + '/data/dataset/data.xlsx')
