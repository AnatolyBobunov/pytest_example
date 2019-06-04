# connect to shusha DB, fixture is executed before every test case in the current directory
import logging
import configparser
import os
import time
from logging.handlers import RotatingFileHandler
from datetime import datetime

config_file_name = 'test_config.ini'


def get_config(filename):
    find_path = os.path.split(os.path.abspath(os.path.dirname(filename)))[0]
    for dirpath, dirnames, filenames in os.walk(find_path):
        if filename in filenames:
            path = os.path.abspath(filename)
    config = configparser.RawConfigParser()
    try:
        config.read(path)
        return config
    except Exception:
        raise IOError('ERORR get_config function: Cannot read config.ini')


conf = get_config(config_file_name)


LOG_LEVEL = conf.get('logging', 'LOG_LEVEL')
LOG_TYPE = conf.get('logging', 'LOG_TYPE')
LOG_SIZE = int(conf.get('logging', 'LOG_SIZE'))
LOG_OUTPUT = conf.get('logging', 'LOG_OUTPUT')


def find_folder(folder_name):
    '''
    Rises one level higher and starts find folder
    according to "folder_name".
    Folder name must be unique
    '''
    find_path = os.path.split(os.path.abspath(os.path.dirname(folder_name)))[0]
    lg.debug('Start found foldername - {}, start position - {}'.format(folder_name, find_path))
    for root, dirs, files in os.walk(find_path):
        for item in dirs:
            try:
                if item.endswith(folder_name):
                    dir = os.path.join(root, folder_name) + '/'
                    lg.debug('Finally foldername - {}'.format(dir))
                    return dir
            except Exception:
                lg.error('Folder not found or invalid folder name')


# @pytest.fixture(scope="function", autouse=True)
def start_test(request):
    '''
    Start test. Start measure time
    '''
    start01 = time.time()
    testname = request.node.name
    lg.info('Test started {}'.format(testname))
    yield
    lg.debug("time for all step {} seconds\n".format(time.time() - start01))
