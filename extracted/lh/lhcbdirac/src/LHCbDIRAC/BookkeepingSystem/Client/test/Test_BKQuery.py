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
from copy import deepcopy

from DIRAC import S_OK

from LHCbDIRAC.BookkeepingSystem.Client.BKQuery import BKQuery, makeBKPath

AVAILABLE_FILE_TYPES = {
    "ParameterNames": ["FileType", "Description"],
    "Records": [
        ["DST", "A DST file"],
        ["MDST", "A smaller file"],
        ["ALLSTREAMS.ANAPROD_BSTOJPSIPHI.DST", None],
        ["HLT2.DST", "HLT2 DST file"],
    ],
}
AVAILABLE_FILE_TYPES["TotalRecords"] = len(AVAILABLE_FILE_TYPES["Records"])


@pytest.fixture
def fake_available_file_types(monkeypatch):
    monkeypatch.setattr(
        "LHCbDIRAC.BookkeepingSystem.Client.BookkeepingClient.BookkeepingClient.getAvailableFileTypes",
        lambda self: S_OK(deepcopy(AVAILABLE_FILE_TYPES)),
    )


def test_reversible(fake_available_file_types):
    query_dict = {
        "ConfigName": "MC",
        "ConfigVersion": "Dev",
        "ConditionDescription": "Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8",
        "ProcessingPass": "/Sim10c/AnaProd-v0r0p6844333-MC_BuToD0K_D0ToHHHH_sig_Up_hlt1/2",
        "EventType": "12165042",
        "FileType": "HLT2.DST",
        "SimulationConditions": "Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8",
    }
    query_path = makeBKPath(query_dict)
    assert (
        query_path == "/MC/Dev/Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8/Sim10c/"
        "AnaProd-v0r0p6844333-MC_BuToD0K_D0ToHHHH_sig_Up_hlt1/2/12165042/HLT2.DST"
    )
    assert BKQuery().buildBKQuery(query_path) == query_dict | {"Visible": "Yes"}


def test_complex(fake_available_file_types):
    query_dict = BKQuery().buildBKQuery(
        "/MC/Dev/Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8/Sim10c/"
        "AnaProd-v0r0p6844333-MC_BuToD0K_D0ToHHHH_sig_Up_hlt1/2/12165042/HLT2.DST",
        prods=[212760],
        fileTypes=["HLT2.DST"],
        visible=True,
    )
    assert query_dict == {
        "ConfigName": "MC",
        "ConfigVersion": "Dev",
        "ConditionDescription": "Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8",
        "ProcessingPass": "/Sim10c/AnaProd-v0r0p6844333-MC_BuToD0K_D0ToHHHH_sig_Up_hlt1/2",
        "EventType": "12165042",
        "Production": 212760,
        "FileType": "HLT2.DST",
        "Visible": "Yes",
        "SimulationConditions": "Beam6800GeV-expected-2024-MagUp-Nu7.6-25ns-Pythia8",
    }
