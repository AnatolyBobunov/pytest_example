# connect to shusha DB, fixture is executed before every test case in the current directory
import pytest
import logging
import pymysql.cursors
import configparser
import os
import json
import time
import allure
from logging.handlers import RotatingFileHandler
from datetime import datetime
from py.xml import html

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


HOST = conf.get('database', 'HOST')
USER = conf.get('database', 'USER')
PASSWORD = conf.get('database', 'PASSWORD')
DATABASE = conf.get('database', 'DATABASE')
PORT = int(conf.get('database', 'PORT'))
LOG_LEVEL = conf.get('logging', 'LOG_LEVEL')
LOG_TYPE = conf.get('logging', 'LOG_TYPE')
LOG_SIZE = int(conf.get('logging', 'LOG_SIZE'))
LOG_OUTPUT = conf.get('logging', 'LOG_OUTPUT')
CLEAR_RESULTS = conf.get('other', 'CLEAR_RESULTS')


@pytest.fixture(scope="session")
def shshaDB(request):
    """
    Fixture is used for DB connection setup
    return object
    """
    with allure.step("Connect to DB"):
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWORD,
                               database=DATABASE, port=PORT,
                               cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()
        return cursor

    def printOut():
        conn.close()
    request.addfinalizer(printOut)


@pytest.fixture(scope="session")
def shshaDB_func(query):
    """
    for DB connection
    return dictionary list
    """
    conn = pymysql.connect(host=HOST, user=USER,
                           password=PASSWORD,
                           database=DATABASE, port=PORT,
                           cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    finally:
        conn.close()


class Superlogging():
    '''
    По умолчанию log_type='ONLY_CONSOLE', level_log=logging.DEBUG
    log_type - принимает строку,
    возможные значение 'ALL','ONLY_CONSOLE','ONLY_FILE','NONE'
    level_log - принимает значения lg.debug, lg.info, lg.warning, lg.error, lg.critical

    Examples:
    lg.debug('Debug level - {}'.format('Enable'))
    lg.info('Info level - Enable')
    lg.warning('Warning level - Enable')
    lg.error('Error level - Enable')
    lg.critical('Critical level - Enable')

    example: lg = Superlogging(log_type='ONLY_CONSOLE', level_log=logging.DEBUG).logging_start()

    Хотя нафига тут класс - не знаю, можно было и простой
    функцией обойтись, но раз уж написал...
    '''

    now = datetime.now()
    LOG_NAME = LOG_OUTPUT + '/log' + now.strftime("%Y%m%d"+"_"+"%H"+":"+"%M")

    def __init__(self, log_type='ONLY_CONSOLE', level_log=logging.DEBUG):
        self.log_type = log_type
        print("self.log_type > ", self.log_type)
        self.level_log = logging.getLevelName(level_log)
        self.lg = logging.getLogger(__name__)

    def logging_start(self):
        LOG_NAME = self.LOG_NAME

        console_log_formatter = logging.Formatter(u'%(asctime)s %(name)8s [LINE:%(lineno)d] %(levelname)s - %(message)s')
        file_log_formatter = logging.Formatter(u'%(asctime)s %(filename)35s %(levelname)8s - %(message)s > %(funcName)s:%(lineno)s')
        lg = self.lg

        if self.log_type == 'ALL':
            # create console and file handler
            consoleHandler = logging.StreamHandler()
            fileHandler = RotatingFileHandler(LOG_NAME, mode='a', maxBytes=LOG_SIZE*1024*1024,
                                              backupCount=1, encoding=None, delay=0)
            consoleHandler.setFormatter(console_log_formatter)
            fileHandler.setFormatter(file_log_formatter)
            lg.setLevel(self.level_log)
            if lg.handlers == []:
                lg.addHandler(consoleHandler)
                lg.addHandler(fileHandler)
            lg.debug('Log in file and in console - activated')
        elif self.log_type == 'ONLY_CONSOLE':
            # create console handler
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(console_log_formatter)
            lg.setLevel(self.level_log)
            if lg.handlers == []:
                lg.addHandler(consoleHandler)
            lg.debug('Console log - activated')
        elif self.log_type == 'ONLY_FILE':
            # create file handler
            fileHandler = RotatingFileHandler(LOG_NAME, mode='a', maxBytes=LOG_SIZE*1024*1024,
                                              backupCount=1, encoding=None, delay=0)
            fileHandler.setFormatter(file_log_formatter)
            lg.setLevel(self.level_log)
            if lg.handlers == []:
                lg.addHandler(fileHandler)
            lg.debug('Log in file - activated')
        elif self.log_type == 'NONE':
            # Disable logging
            logging.disable(logging.CRITICAL)
            print('Logging not activated')

        lg.info('All logging level - Enable')
        return lg


lg = Superlogging(log_type=LOG_TYPE, level_log=LOG_LEVEL).logging_start()


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
            except Exception: lg.error('Folder not found or invalid folder name')


@pytest.fixture(scope="function", autouse=True)
def start_test(request):
    '''
    Start test. Start measure time
    '''
    start01 = time.time()
    testname = request.node.name
    lg.info('Test started {}'.format(testname))
    yield
    lg.debug("time for all step {} seconds\n".format(time.time() - start01))


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.insert(1, html.th('Time', class_='sortable time', col='time'))
    cells.pop()


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.insert(1, html.td(datetime.utcnow(), class_='col-time'))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
