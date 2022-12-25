import logging

from time import process_time


def logged(f):

    def wrapper(*args, **kwargs):
        logger: logging.Logger = args[0].logger
        logger.info(f'{f.__name__} started...')
        start = process_time()
        result = f(*args, **kwargs)
        end = process_time()
        logger.info(f'{f.__name__} finished. {end - start:.3f}s')
        return result

    return wrapper
