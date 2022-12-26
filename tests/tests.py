import json
import pandas as pd
import pytest
import unittest

from werkzeug.exceptions import NotFound

from app import AvailableModels
from domain.enums import DataSheetIndexes


class TestGetModelsRest(unittest.TestCase):

    def test_get(self):
        gmr = AvailableModels()

        self.assertDictEqual(json.loads(gmr.get()[0]),
                             {'LASSO_REGRESSION': 1, 'LINEAR_REGRESSION': 2, 'RIDGE_REGRESSION': 3})


@pytest.fixture()
def get_fixture_data(scope="module"):
    df = pd.read_excel('/Users/meirroketlisvili/PycharmProjects/FTAD_MLOps/data/dataset/data.xlsx', sheet_name='data')
    return df


def test_rows(get_fixture_data):
    def copy():
        return get_fixture_data.copy()

    def duplicated_rows_df(df):
        return df.duplicated().any()

    assert duplicated_rows_df(copy()), 'WHAT ARE YOU AN IDIOT?'


def test_columns(get_fixture_data):
    def copy():
        return get_fixture_data.copy()

    def get_data_columns(df):
        return set(df.columns)

    print(get_data_columns(copy()))

    reference_columns = set(DataSheetIndexes.name_values_dict().keys())

    print(reference_columns)

    assert get_data_columns(copy()) == reference_columns, \
        'THIS PROBABLY SHOULD HELP: https://www.youtube.com/watch?v=dQw4w9WgXcQ'
