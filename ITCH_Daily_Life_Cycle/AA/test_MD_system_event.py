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
def test_MD_SystemEvent_O(shshaDB):
    """
    Story: SystemEvent message for all Gateway with EventCode = O
    """
    query = """
    SELECT timestamp, sourceport, sourceip, destinationip, destinationport,
    msgseqnum, headermarketdatagroup, length, messagetype, eventcode
    FROM mitch_systemevent
    where length='7' AND eventcode='O' AND messagetype='S' AND msgseqnum='2'
    ORDER BY headermarketdatagroup
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
        assert_that(test.rowcount, equal_to(6))
    with allure.step('Validate results, headermarketdatagroup'):
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'A'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'B'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'C'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'D'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'E'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'F'), equal_to(1))
    with allure.step('Validate results, length'):
        assert_that(counting_value(test.result, 'length', 7), equal_to(6))
    with allure.step('Validate results, eventcode'):
        assert_that(counting_value(test.result, 'eventcode', 'O'), equal_to(6))


@allure.feature('Market Data')
@allure.story('2.1.3_ITCH_Daily_Life_Cycle')
def test_MD_SystemEvent_C(shshaDB):
    """
    Story: SystemEvent message for all Gateway with EventCode = C
    """
    query = """
    SELECT timestamp, sourceport, sourceip, destinationip, destinationport,
    msgseqnum, headermarketdatagroup, length, messagetype, eventcode
    FROM mitch_systemevent
    where length='7' AND eventcode='C' AND messagetype='S'
    ORDER BY headermarketdatagroup
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
        assert_that(test.rowcount, equal_to(6))
    with allure.step('Validate results, headermarketdatagroup'):
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'A'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'B'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'C'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'D'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'E'), equal_to(1))
        assert_that(counting_value(test.result, 'headermarketdatagroup', 'F'), equal_to(1))
    with allure.step('Validate results, length'):
        assert_that(counting_value(test.result, 'length', 7), equal_to(6))
    with allure.step('Validate results, eventcode'):
        assert_that(counting_value(test.result, 'eventcode', 'C'), equal_to(6))
