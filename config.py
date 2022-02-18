import logging

def init_log(verbose=False):
    general_level = logging.INFO
    azure_level = logging.CRITICAL
    datefmt = "%d-%m-%Y|%H:%M:%S"
    format='%(asctime)s|%(levelname).1s|%(module)s:%(funcName)s:%(lineno)d|%(message)s'
    if verbose:
        general_level = logging.DEBUG
        logging.debug('Verbosity Activated....')
        azure_level = logging.DEBUG
    logging.getLogger('azure').setLevel(azure_level)
    logging.basicConfig(format=format, datefmt=datefmt, level=general_level)
