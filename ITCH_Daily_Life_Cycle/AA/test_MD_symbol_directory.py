#!/usr/bin/python3

import pytest
import allure
from hamcrest import assert_that, equal_to
from related_files.utils import MyTest, counting_value
from conftest import lg


"""
Test writing example
"""


@allure.feature('Market Data')
@allure.story('2.1.3_ITCH_Daily_Life_Cycle')
def test_MD_SymbolDirectory_ETF(shshaDB):
    """
    Story: SymbolDirectory message for Market = ETF
    """
    query = """
    SELECT timestamp, headermarketdatagroup, length, messagetype, nanosecond, instrumentid,
    symbolstatus, isin, pricebandtolerances, dynamiccircuitbreakertolerances,
    staticcircuitbreakertolerances, segment, underlying, currency, flags
    FROM mitch_symboldirectory
    WHERE (length=92) AND (messagetype='R') AND (instrumentid LIKE '8141%') AND (symbolstatus=' ')
    AND (segment='ETC') AND (pricebandtolerances=30) AND (dynamiccircuitbreakertolerances=7.5)
    AND (staticcircuitbreakertolerances=15) AND (underlying=0) AND (currency='EUR') AND (flags=0)
    ORDER BY instrumentid, timestamp
    """

    test = MyTest(shshaDB, query)

    with allure.step('Run query'):
        test.run()
        allure.attach(query, 'Attached Query', allure.attachment_type.TEXT)
    test.output()
    with allure.step('Output query'):
        if test.result:
            allure.attach(test.generateHtml(), 'Rows returned', allure.attachment_type.HTML)

    with allure.step('Validate results, all row count'):
        assert_that(test.rowcount, equal_to(5))
    with allure.step('Validate results, headermarketdatagroup'):
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'A'), equal_to(1))
    with allure.step('Validate results, headermarketdatagroup'):
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'C'), equal_to(4))
    with allure.step('Validate results, length'):
        assert_that(counting_value(test.result, 'length', 92), equal_to(5))


@allure.feature('Market Data')
@allure.story('2.1.3_ITCH_Daily_Life_Cycle')
def test_MD_SymbolDirectory_MIFID(shshaDB):
    """
    Story: SymbolDirectory message for Market = MIFID
    """
    query = """
    SELECT timestamp, headermarketdatagroup, length, messagetype, nanosecond,
    instrumentid, symbolstatus, isin, pricebandtolerances,
    dynamiccircuitbreakertolerances, staticcircuitbreakertolerances, segment,
    underlying, currency, flags
    FROM mitch_symboldirectory
    WHERE (length=92) AND (messagetype='R') AND (instrumentid LIKE '8142%')
    AND ((symbolstatus=' ') OR (symbolstatus='H'))
    AND (segment='MFD') AND (pricebandtolerances=0) AND (dynamiccircuitbreakertolerances=0)
    AND (staticcircuitbreakertolerances=0) AND (underlying=0) AND (currency='EUR') AND (flags=0)
    ORDER BY instrumentid, timestamp
    """

    test = MyTest(shshaDB, query)

    with allure.step('Run query'):
        test.run()
        allure.attach(query, 'Attached Query', allure.attachment_type.TEXT)
    test.output()
    with allure.step('Output query'):
        if test.result:
            allure.attach(test.generateHtml(), 'Rows returned', allure.attachment_type.HTML)

    with allure.step('Validate results, all row count'):
        assert_that(test.rowcount, equal_to(5))
    with allure.step('Validate results, headermarketdatagroup'):
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'A'), equal_to(5))
    with allure.step('Validate results, symbolstatus'):
        assert_that(counting_value(test.result, 'symbolstatus', ' '), equal_to(5))
    with allure.step('Validate results, length'):
        assert_that(counting_value(test.result, 'length', 92), equal_to(5))
