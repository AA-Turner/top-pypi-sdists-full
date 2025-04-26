###############################################################################
# (c) Copyright 2019 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
"""Unit test of ConsistencyChecks."""
# pylint: disable=invalid-name,missing-docstring,protected-access
from unittest.mock import Mock

import pytest

from LHCbDIRAC.BookkeepingSystem.Client.test.mock_BookkeepingClient import bkc_mock
from LHCbDIRAC.DataManagementSystem.Client import ConsistencyChecks as ConsistencyChecksModule

FILETYPES = [
    ["SEMILEPTONIC.DST", "LOG", "RAW"],
    ["SEMILEPTONIC.DST", "LOG", "RAW"],
    ["SEMILEPTONIC.DST"],
    ["SEMILEPTONIC.DST"],
]


@pytest.fixture
def cc_mock(monkeypatch):
    dmMock = Mock()
    dmMock.getReplicas.return_value = {
        "OK": True,
        "Value": {"Successful": {"bb.raw": "metadataPippo"}, "Failed": {}},
    }

    cc = ConsistencyChecksModule.ConsistencyChecks(transClient=Mock(), dm=dmMock, bkClient=bkc_mock)

    cc.fileTypesExcluded = ["LOG"]
    cc.prod = 0
    monkeypatch.setattr(ConsistencyChecksModule, "BookkeepingClient", lambda: bkc_mock)
    yield cc


def test_selectByFileType(cc_mock):
    lfnDicts = [
        {
            "aa.raw": {
                "bb.raw": {"FileType": "RAW", "RunNumber": 97019},
                "bb.log": {"FileType": "LOG"},
                "/bb/pippo/aa.dst": {"FileType": "DST"},
                "/lhcb/1_2_1.Semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
            },
            "cc.raw": {
                "dd.raw": {"FileType": "RAW", "RunNumber": 97019},
                "bb.log": {"FileType": "LOG"},
                "/bb/pippo/aa.dst": {"FileType": "LOG"},
                "/lhcb/1_1.semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
            },
        },
        {"aa.raw": {"/bb/pippo/aa.dst": {"FileType": "LOG"}, "bb.log": {"FileType": "LOG"}}},
        {
            "aa.raw": {
                "bb.raw": {"FileType": "RAW", "RunNumber": 97019},
                "bb.log": {"FileType": "LOG"},
                "/bb/pippo/aa.dst": {"FileType": "DST"},
                "/lhcb/1_2_1.Semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
            },
            "cc.raw": {
                "dd.raw": {"FileType": "RAW", "RunNumber": 97019},
                "bb.log": {"FileType": "LOG"},
                "/bb/pippo/aa.dst": {"FileType": "LOG"},
                "/lhcb/1_1.semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
            },
        },
        {"aa.raw": {"/bb/pippo/aa.dst": {"FileType": "LOG"}, "bb.log": {"FileType": "LOG"}}},
    ]

    lfnDictsExpected = [
        {
            "aa.raw": {
                "/lhcb/1_2_1.Semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
                "bb.log": {"FileType": "LOG"},
                "bb.raw": {"RunNumber": 97019, "FileType": "RAW"},
            },
            "cc.raw": {
                "dd.raw": {"RunNumber": 97019, "FileType": "RAW"},
                "bb.log": {"FileType": "LOG"},
                "/bb/pippo/aa.dst": {"FileType": "LOG"},
                "/lhcb/1_1.semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"},
            },
        },
        {"aa.raw": {"/bb/pippo/aa.dst": {"FileType": "LOG"}, "bb.log": {"FileType": "LOG"}}},
        {
            "aa.raw": {"/lhcb/1_2_1.Semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"}},
            "cc.raw": {"/lhcb/1_1.semileptonic.dst": {"FileType": "SEMILEPTONIC.DST"}},
        },
        {},
    ]

    # testing various cases
    for fileType, lfnDict, lfnDictExpected in zip(FILETYPES, lfnDicts, lfnDictsExpected):
        cc_mock.fileType = fileType

        res = cc_mock._selectByFileType(lfnDict)

        assert res == lfnDictExpected

        res = cc_mock._selectByFileType(lfnDict)
        assert res == lfnDictExpected


def test_getFileTypesCount(cc_mock):
    lfnDict = {"aa.raw": {"bb.log": {"FileType": "LOG"}, "/bb/pippo/aa.dst": {"FileType": "DST"}}}
    res = cc_mock._getFileTypesCount(lfnDict)
    resExpected = {"aa.raw": {"DST": 1, "LOG": 1}}
    assert res == resExpected

    lfnDict = {
        "aa.raw": {
            "bb.log": {"FileType": "LOG"},
            "/bb/pippo/aa.dst": {"FileType": "DST"},
            "/bb/pippo/cc.dst": {"FileType": "DST"},
        }
    }
    res = cc_mock._getFileTypesCount(lfnDict)
    resExpected = {"aa.raw": {"DST": 2, "LOG": 1}}
    assert res == resExpected


def test_getDescendants(cc_mock):
    cc_mock.fileType = ["SEMILEPTONIC.DST", "LOG", "RAW"]
    res = cc_mock.getDescendants(["aa.raw"])
    (
        filesWithDescendants,
        filesWithoutDescendants,
        filesWitMultipleDescendants,
        descendants,
        inFCNotInBK,
        inBKNotInFC,
        removedFiles,
        inFailover,
    ) = res
    assert {k: set(v) for k, v in filesWithDescendants.items()} == {"aa.raw": {"bb.log", "bb.raw"}}
    assert filesWithoutDescendants == {}
    assert filesWitMultipleDescendants == {}
    assert descendants == ["bb.raw"]
    assert inFCNotInBK == []
    assert inBKNotInFC == []
    assert removedFiles == []
    assert inFailover == []
