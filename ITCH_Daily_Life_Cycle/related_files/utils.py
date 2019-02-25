#!/usr/bin/python3
from conftest import lg


def counting_value(result, key, value):
    """
    Story: counting of pair key:value by strictly setpoints
    result = fetchall, list of turple
    key = key
    value = value
    """
    a = 0

    for row in result:
        if row.get(key) == value:
            a = a + 1
        else:
            continue
    return a


class GeneratedTest:
    """Object for a tests generated by a model"""
    def __init__(self, case_name, query):
        self.query = query
        self.case_name = case_name


class MyTest:
    """ Class for SQL test"""
    def __init__(self, DB, query):
        """Init connection and variables"""
        self.DB = DB
        self.query = query
        self.result = None
        self.rowcount = None

    def run(self):
        """Do a query"""
        self.DB.execute(self.query)
        self.rowcount = self.DB.rowcount

    def output(self, disabled=False):
        """Fetch results and output them"""
        self.disabled = disabled
        lg.info('Query: {}'.format(self.query))
        self.result = self.DB.fetchall()
        if self.result:
            if not self.disabled:
                lg.info('Result: {}'.format(self.result))

    def generateHtml(self):
        """Generate table from fetched results"""
        if self.result:
            htmlRow = ""
            header = ""
            body = "<table border='1' bordercolor=''#ddd' cellspacing='0' cellpadding='4' style='table-layout:fixed;vertical-align:bottom;font-size:13px;font-family:verdana,sans,sans-serif;border-collapse:collapse;border:1px solid rgb(130,130,130)'>"
            for field in self.result[0].keys():
                header += "\n\t\t<th>{}</th>".format(field)
            body += "\n\t<tr>{}\n\t</tr>".format(header)

            for row in self.result:
                htmlRow = ""
                for key in row:
                    htmlRow += "\n\t\t<td>{}</td>".format(str(row[key]))
                body += "\n\t<tr>{}\n\t</tr>".format(htmlRow)
            body += "\n</table>"
            return body
