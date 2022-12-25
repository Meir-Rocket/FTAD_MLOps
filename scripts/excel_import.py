import logging
import os
import sys

from dbs.database import DatabaseInitializer


def init_logger() -> logging.Logger:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(levelname)s: %(message)s',
    )
    return logging.getLogger('DatabaseInitializerLogger')


def import_data(cfg: dict):
    if cfg['UPDATE_DATA']:
        database = cfg['SQLALCHEMY_DATABASE']
        if cfg['DATA_PATH']:
            file = cfg['DATA_PATH']
        else:
            file = os.getcwd() + '/data/dataset/data.xlsx'
        DatabaseInitializer(database, file, init_logger()).init_db()
