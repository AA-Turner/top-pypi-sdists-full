###############################################################################
# (c) Copyright 2024 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import pytest
import json
import os

from DIRAC.Core.Utilities.ReturnValues import returnValueOrRaise

# WARNING! This code modify specified Oracle instance
# NEVER RUN IT with Production/Certification instance
# WARNING!


def loadJSON(filename: str):
    """Load content from JSON file
    :param str filename: JSON file name
    :returns: python object with content
    """
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        content = json.load(f)
    return content


def clearDBContent(bkdb, content):
    """Cleanup tables specified in the content"""
    for tablename in reversed([table["Table"] for table in content["Tables"]]):
        returnValueOrRaise(bkdb.dbW_.query(f"DELETE FROM {tablename}"))


def fillDBContent(bkdb, content):
    """Load data specified in the content"""
    for table in content["Tables"]:
        tablename = table["Table"]
        for record in table["Records"]:
            columns = list(record)
            sql_fields = ", ".join(columns)
            sql_values = ", ".join([f":{i+1}" for i in range(len(columns))])
            record_values = [record[field] for field in columns]
            sql = f"INSERT INTO {tablename} ({sql_fields}) VALUES ({sql_values})"
            returnValueOrRaise(bkdb.dbW_.query(sql, params=[record_values]))


##############################################


@pytest.fixture
def fileTree(bkdb):
    content = loadJSON("descendents.json")
    clearDBContent(bkdb, content)
    fillDBContent(bkdb, content)
    yield content
    clearDBContent(bkdb, content)


def _orderGetFileDescendents(results):
    success = results["Successful"]
    for lfn in success:
        success[lfn].sort()


def test_file_descendents(bkdb, fileTree):
    result = returnValueOrRaise(
        bkdb.getFileDescendents(["/test/100/1.RAW", "/unknown/file"], depth=5, production=0, checkreplica=False)
    )
    # print(json.dumps(result, sort_keys=True, indent=2)) # to find what it should be, and copy into json...
    expected = fileTree["Results"]["two_5_0_False"]
    assert _orderGetFileDescendents(result) == _orderGetFileDescendents(expected)

    result = returnValueOrRaise(
        bkdb.getFileDescendents(
            ["/test/100/1.RAW", "/test/100/2.RAW", "/test/100/3.RAW"], depth=5, production=0, checkreplica=True
        )
    )
    # print(json.dumps(result, sort_keys=True, indent=2)) # to find what it should be, and copy into json...
    expected = fileTree["Results"]["three_5_0_True"]
    assert _orderGetFileDescendents(result) == _orderGetFileDescendents(expected)

    result = returnValueOrRaise(
        bkdb.getFileDescendents(
            ["/test/100/1.RAW", "/test/100/2.RAW", "/test/100/3.RAW"], depth=5, production=102, checkreplica=True
        )
    )
    # print(json.dumps(result, sort_keys=True, indent=2)) # to find what it should be, and copy into json...
    expected = fileTree["Results"]["three_5_102_True"]
    assert _orderGetFileDescendents(result) == _orderGetFileDescendents(expected)

    result = returnValueOrRaise(
        bkdb.getFileDescendentsTree(
            ["/test/100/1.RAW", "/test/100/2.RAW", "/test/100/3.RAW"], depth=5, production=102, checkreplica=True
        )
    )
    # print(json.dumps(result, sort_keys=True, indent=2)) # to find what it should be, and copy into json...
    expected = fileTree["Results"]["tree_three_5_102_True"]
    assert result == expected
