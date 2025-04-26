###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from LHCbDIRAC.ProductionManagementSystem.DB.AnalysisProductionsDB import AnalysisProductionsDB
from LHCbDIRAC.ProductionManagementSystem.DB.AnalysisProductionsObjects import AnalysisSample as AP


@pytest.fixture
def apdb():
    db = AnalysisProductionsDB(url="sqlite+pysqlite:///:memory:")
    yield db


REQUEST_1 = {
    "request_id": 1234,
    "filetype": "TUPLE.ROOT",
    "name": "MySample",
    "version": "v1r2p3",
    "wg": "MyWG",
    "analysis": "MyAnalysis",
    "extra_info": {
        "transformations": [],
        "merge_request": "https://gitlab.cern.ch/lhcb-datapkg/AnalysisProductions/-/merge_requests/0",
        "jira_task": "https://its.cern.ch/jira/browse/WGP-0",
    },
    "validity_start": datetime.now() - timedelta(days=1),
    "housekeeping_interaction_due": None,
    "owners": [],
    "auto_tags": [
        {"name": "config", "value": "MC"},
        {"name": "polarity", "value": "MagDown"},
        {"name": "eventtype", "value": "23133002"},
        {"name": "datatype", "value": "2012"},
    ],
    "publications": [],
}

REQUEST_2 = {
    "request_id": 987,
    "filetype": "TUPLE.ROOT",
    "name": "AnotherSample",
    "version": "v1r2p4",
    "wg": "AnotherWG",
    "analysis": "AnotherAnalysis",
    "extra_info": {
        "transformations": [],
        "merge_request": "https://gitlab.cern.ch/lhcb-datapkg/AnalysisProductions/-/merge_requests/0",
        "jira_task": "https://its.cern.ch/jira/browse/WGP-0",
    },
    "validity_start": datetime.now() - timedelta(days=1),
    "housekeeping_interaction_due": None,
    "owners": [],
    "auto_tags": [
        {"name": "config", "value": "LHCb"},
        {"name": "polarity", "value": "MagUp"},
        {"name": "datatype", "value": "2018"},
    ],
    "publications": [],
}

REQUEST_3 = {
    "request_id": 988,
    "filetype": "TUPLE.ROOT",
    "name": "AnotherSample",
    "version": "v1r2p3",
    "wg": "MyWG",
    "analysis": "MyAnalysis",
    "extra_info": {
        "transformations": [],
        "merge_request": "https://gitlab.cern.ch/lhcb-datapkg/AnalysisProductions/-/merge_requests/0",
        "jira_task": "https://its.cern.ch/jira/browse/WGP-0",
    },
    "validity_start": datetime.now() - timedelta(days=1),
    "housekeeping_interaction_due": None,
    "owners": [],
    "auto_tags": [
        {"name": "config", "value": "LHCb"},
        {"name": "polarity", "value": "MagUp"},
        {"name": "datatype", "value": "2018"},
    ],
    "publications": [],
}

TRANSFORMS_1a = {
    "id": 45,
    "status": "Archived",
    "steps": [
        {
            "stepID": 50,
            "application": "DaVinci/v45r6",
            "extras": ["AnalysisProductions.v0r0p2510752", "ProdConf"],
            "options": ["$SOMETHING/a.py"],
        }
    ],
    "used": False,
}

TRANSFORMS_1b = {
    "id": 47,
    "status": "Archived",
    "steps": [
        {
            "stepID": 51,
            "application": "Noether/v1r4",
            "extras": ["AppConfig.v3r398", "ProdConf"],
            "options": ["$SOMETHING/b.py"],
        }
    ],
    "used": True,
}


def _compareRequest(orig, new):
    assert new["sample_id"] is not None
    assert orig["request_id"] == new["request_id"]
    assert new["state"] is not None

    assert orig["wg"].lower() == new["wg"]
    assert orig["analysis"].lower() == new["analysis"]
    assert orig["version"].lower() == new["version"]
    assert orig["name"].lower() == new["name"]
    assert orig["extra_info"]["jira_task"] == new["jira_task"]
    assert orig["extra_info"]["merge_request"] == new["merge_request"]

    assert orig["owners"] == []
    assert new["owners"] == []
    assert orig["extra_info"]["transformations"] == new["transformations"]

    assert orig["validity_start"] == new["validity_start"]
    assert new["validity_end"] is None
    assert new["last_state_update"] is not None


def test_empty(apdb):
    assert apdb.listAnalyses() == {}
    assert apdb.listAnalyses(at_time=None) == {}
    assert apdb.listAnalyses(at_time=datetime.now()) == {}

    assert apdb.getKnownAutoTags() == set()

    assert apdb.getProductions() == []
    assert apdb.getProductions(wg="MyWG", analysis="MyAnalysis") == []
    assert apdb.getProductions(at_time=None) == []
    assert apdb.getProductions(at_time=datetime.now()) == []

    assert apdb.getArchivedRequests() == []
    assert apdb.getArchivedRequests(state="waiting") == []
    assert apdb.getArchivedRequests(state="ready") == []


def test_ownership(apdb):
    assert apdb.getOwners(wg="mywg", analysis="myanalysis") == []
    apdb.setOwners(wg="mywg", analysis="myanalysis", owners=["auser"])
    assert apdb.getOwners(wg="mywg", analysis="myanalysis") == ["auser"]

    assert apdb.getOwners(wg="mywg2", analysis="myanalysis") == []
    apdb.setOwners(wg="mywg2", analysis="myanalysis", owners=["user2"])
    assert apdb.getOwners(wg="mywg2", analysis="myanalysis") == ["user2"]

    assert apdb.getOwners(wg="mywg", analysis="myanalysis2") == []
    apdb.setOwners(wg="mywg", analysis="myanalysis2", owners=["user3"])
    assert apdb.getOwners(wg="mywg", analysis="myanalysis2") == ["user3"]

    apdb.setOwners(wg="mywg", analysis="myanalysis2", owners=[])
    assert apdb.getOwners(wg="mywg", analysis="myanalysis2") == []

    apdb.setOwners(wg="mywg", analysis="myanalysis", owners=["user4", "user5"])
    assert apdb.getOwners(wg="mywg", analysis="myanalysis") == ["user4", "user5"]

    apdb.setOwners(wg="mywg", analysis="myanalysis", owners=[])
    assert apdb.getOwners(wg="mywg", analysis="myanalysis") == []


def test_registerNew(apdb):
    newRequests = apdb.registerRequests([REQUEST_1])
    assert len(newRequests) == 1

    newRequest = newRequests[0]
    assert newRequest["sample_id"] == 1
    assert newRequest["state"] == "waiting"
    _compareRequest(REQUEST_1, newRequest)

    assert apdb.listAnalyses() == {"mywg": ["myanalysis"]}

    assert apdb.listAnalyses2() == [
        {
            "analysis": "myanalysis",
            "n_active": 0,
            "n_ready": 0,
            "n_replicating": 0,
            "n_total": 1,
            "n_waiting": 1,
            "owners": [],
            "wg": "mywg",
            "earliest_housekeeping_due": (
                datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=90)
            ),
            "transform_ids": [],
        }
    ]

    assert apdb.getProductions() == [newRequest]
    assert apdb.getProductions(wg="mywg", analysis="myanalysis") == [newRequest]
    assert apdb.getProductions(wg="MYWG", analysis="MYANALYSIS") == [newRequest]
    assert apdb.getProductions(name="mysample") == [newRequest]
    assert apdb.getProductions(name="MySample") == [newRequest]
    assert apdb.getProductions(name="anothersample") == []
    assert apdb.getProductions(state="waiting") == [newRequest]
    assert apdb.getProductions(state="active") == []
    assert apdb.getProductions(version="v1r2p3") == [newRequest]
    assert apdb.getProductions(version="v1r2p4") == []

    assert apdb.getKnownAutoTags() == {"config", "polarity", "eventtype", "datatype"}
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {
            "config": "mc",
            "polarity": "magdown",
            "eventtype": "23133002",
            "datatype": "2012",
        }
    }


def test_duplicate(apdb):
    apdb.registerRequests([REQUEST_1])
    with pytest.raises(ValueError, match=f"Already registered.*{REQUEST_1['request_id']}.*"):
        apdb.registerRequests([REQUEST_1])


def test_listRequests(apdb):
    assert apdb.listRequests() == []
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    requests = apdb.listRequests()
    assert len(requests) == 3
    for request in requests:
        assert request["tags"] == []
        assert isinstance(request["autotags"], dict)
        if "eventtype" in request["autotags"]:
            assert {"config", "datatype", "polarity", "eventtype"} == set(request["autotags"])
        else:
            assert {"config", "datatype", "polarity"} == set(request["autotags"])

    apdb.archiveSamples([apdb.getProductions()[0]["sample_id"]])

    requests = apdb.listRequests()
    assert len(requests) == 2


def test_multiple_samples_per_request(apdb: AnalysisProductionsDB):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    assert {"myanalysis", "anotheranalysis"} == {x["analysis"] for x in apdb.listAnalyses2()}
    orig1 = apdb.getProductions(wg=REQUEST_1["wg"], analysis=REQUEST_1["analysis"], name=REQUEST_1["name"])
    assert len(orig1) == 1

    apdb.addRequestsToAnalysis("newwg", "newanalysis", [(REQUEST_1["request_id"], "TUPLE.ROOT")])
    assert {"newanalysis", "myanalysis", "anotheranalysis"} == {x["analysis"] for x in apdb.listAnalyses2()}

    with pytest.raises(ValueError, match="Some requests are already registered"):
        apdb.addRequestsToAnalysis(
            "newwg", "newanalysis", [(REQUEST_1["request_id"], "TUPLE.ROOT"), (REQUEST_2["request_id"], "TUPLE.ROOT")]
        )
    assert len(apdb.getProductions(wg="newwg", analysis="newanalysis")) == 1

    apdb.addRequestsToAnalysis(
        "newwg", "newanalysis", [(REQUEST_2["request_id"], "TUPLE.ROOT"), (REQUEST_3["request_id"], "TUPLE.ROOT")]
    )
    assert len(apdb.getProductions(wg="newwg", analysis="newanalysis")) == 3

    ref1 = apdb.getProductions(wg="newwg", analysis="newanalysis", name=REQUEST_1["name"])
    assert len(ref1) == 1
    for key in set(orig1[0]) | set(ref1[0]):
        if key not in {"validity_start", "wg", "analysis", "sample_id"}:
            assert orig1[0][key] == ref1[0][key], key


def test_archival(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])

    assert apdb.getArchivedRequests() == []
    assert apdb.getArchivedRequests(state="waiting") == []
    assert apdb.getArchivedRequests(state="ready") == []

    apdb.archiveSamples([1])

    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234
    archivedRequests = apdb.getArchivedRequests(state="waiting")
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234
    assert apdb.getArchivedRequests(state="ready") == []

    with pytest.raises(ValueError, match=r".*have already been archived.*"):
        apdb.archiveSamples([2, 1, 3])
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234

    with pytest.raises(ValueError, match=r"Unknown sample IDs passed.*"):
        apdb.archiveSamples([2, 12, 3])
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234

    apdb.archiveSamples([2, 3])
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 3


def test_archiveAtTime(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])

    assert apdb.getArchivedRequests() == []
    assert apdb.getArchivedRequests(state="waiting") == []
    assert apdb.getArchivedRequests(state="ready") == []

    # archive in the past
    archive_time_past = datetime.now() - timedelta(days=1)
    apdb.archiveSamplesAtSpecificTime([1], archive_time_past)

    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234
    archivedRequests = apdb.getArchivedRequests(state="waiting")
    assert archivedRequests[0]["request_id"] == 1234
    assert apdb.getArchivedRequests(state="ready") == []

    with pytest.raises(ValueError, match=r".*have already been archived.*"):
        apdb.archiveSamplesAtSpecificTime([2, 1, 3], archive_time_past)
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234

    with pytest.raises(ValueError, match=r"Unknown sample IDs passed.*"):
        apdb.archiveSamplesAtSpecificTime([2, 12, 3], archive_time_past)
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1
    assert archivedRequests[0]["request_id"] == 1234

    # archive in the future
    archive_time_future = datetime.now() + timedelta(days=1)
    apdb.archiveSamplesAtSpecificTime([2, 3], archive_time_future)
    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1


def test_addPublication(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    requests = apdb.listRequests()
    assert len(requests) == 3

    def result_has_pub(r, n, sample_id=None):
        if n not in r:
            return False
        if sample_id:
            if not any(i["sample_id"] == sample_id for i in r[n]):
                return False

        return True

    sample_ids = [1, 2, 3]

    prods_with_pubs = apdb.getProductions(require_has_publication=True)
    assert (
        len(prods_with_pubs) == 0
    ), "getProductions(require_has_publication=True) did not return empty, when it should have"

    with pytest.raises(ValueError, match=r"This publication number is too long.*"):
        apdb.addPublication(sample_ids, "LHCb-" + "h" * 75)

    apdb.addPublication(sample_ids, "LHCb-ANA-YYYY-NNN")

    sample_publications = apdb.getPublications(sample_ids)
    assert result_has_pub(sample_publications, "LHCb-ANA-YYYY-NNN"), 'Result doesn\'t have "LHCb-ANA-YYYY-NNN" at all'
    assert result_has_pub(
        sample_publications, "LHCb-ANA-YYYY-NNN", sample_id=sample_ids[0]
    ), f'Result doesn\'t have "LHCb-ANA-YYYY-NNN" for sample_id {sample_ids[0]}'
    assert result_has_pub(
        sample_publications, "LHCb-ANA-YYYY-NNN", sample_id=sample_ids[1]
    ), f'Result doesn\'t have "LHCb-ANA-YYYY-NNN" for sample_id {sample_ids[1]}'
    assert result_has_pub(
        sample_publications, "LHCb-ANA-YYYY-NNN", sample_id=sample_ids[2]
    ), f'Result doesn\'t have "LHCb-ANA-YYYY-NNN" for sample_id {sample_ids[2]}'

    with pytest.raises(IntegrityError):
        apdb.addPublication(sample_ids, "LHCb-ANA-YYYY-NNN")

    apdb.addPublication([sample_ids[0]], "LHCb-PAPER-YYYY-NNN")
    sample_publications = apdb.getPublications(sample_ids)

    assert result_has_pub(
        sample_publications, "LHCb-PAPER-YYYY-NNN"
    ), 'Result doesn\'t have "LHCb-PAPER-YYYY-NNN" at all'
    assert result_has_pub(
        sample_publications, "LHCb-ANA-YYYY-NNN", sample_id=sample_ids[0]
    ), f'Result doesn\'t have "LHCb-ANA-YYYY-NNN" for sample_id {sample_ids[0]}'
    assert result_has_pub(
        sample_publications, "LHCb-PAPER-YYYY-NNN", sample_id=sample_ids[0]
    ), f'Result doesn\'t have "LHCb-PAPER-YYYY-NNN" for sample_id {sample_ids[0]}'
    assert not result_has_pub(
        sample_publications, "LHCb-PAPER-YYYY-NNN", sample_id=sample_ids[1]
    ), f'Result shouldn\'t have "LHCb-PAPER-YYYY-NNN" for sample_id {sample_ids[1]}'
    assert not result_has_pub(
        sample_publications, "LHCb-PAPER-YYYY-NNN", sample_id=sample_ids[2]
    ), f'Result shouldn\'t have "LHCb-PAPER-YYYY-NNN" for sample_id {sample_ids[2]}'

    prods_with_pubs = apdb.getProductions()

    assert len(prods_with_pubs) == 3

    assert "LHCb-ANA-YYYY-NNN" in prods_with_pubs[0]["publications"]
    assert "LHCb-ANA-YYYY-NNN" in prods_with_pubs[1]["publications"]
    assert "LHCb-ANA-YYYY-NNN" in prods_with_pubs[2]["publications"]
    assert "LHCb-PAPER-YYYY-NNN" in prods_with_pubs[0]["publications"]
    assert "LHCb-PAPER-YYYY-NNN" not in prods_with_pubs[1]["publications"]
    assert "LHCb-PAPER-YYYY-NNN" not in prods_with_pubs[2]["publications"]

    prods_with_pubs = apdb.getProductions(require_has_publication=True)
    assert (
        len(prods_with_pubs) == 3
    ), "getProductions(require_has_publication=True) did not return the three requests with publications"


def test_get_and_delayHousekeepingInteractionDue(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    requests = apdb.listRequests()
    assert len(requests) == 3

    sample_ids = [1, 2, 3]

    assert apdb.getArchivedRequests() == []

    def getHousekeepingInteractionDue(sample_ids: list[int]):
        query = select(AP.sample_id, AP.housekeeping_interaction_due)
        query = query.filter(AP.sample_id.in_(sample_ids))
        query = query.filter(AP.validity_end.is_(None))

        # this returns due dates for existing and non-archived requests
        # non-existing requests are omitted
        # archived requests are omitted
        # existing requests with no due date are returned but with a null value
        with apdb.session as session:
            return {i: d for i, d in session.execute(query).all()}

    # check that house keeping dates are returned at all even if None
    # if they don't exist, they won't be returned
    hkdates = getHousekeepingInteractionDue(sample_ids)
    assert all(sample_id in hkdates.keys() for sample_id in sample_ids)
    assert len(hkdates) == 3

    due_datetime_200d = datetime.now() + timedelta(days=200)
    due_datetime_1y = datetime.now() + timedelta(days=365)
    # delay a non-existent request
    with pytest.raises(ValueError, match=r"Unknown sample IDs passed.*"):
        apdb.delayHousekeepingInteractionDue(sample_ids + [999999999, 990999], due_datetime_200d)
    hkdates = getHousekeepingInteractionDue(sample_ids)

    # check nothing changed
    assert all(hkdates[sample_id] != due_datetime_200d for sample_id in sample_ids)

    # set housekeeping 200 days in the future for one request
    apdb.delayHousekeepingInteractionDue([sample_ids[0]], due_datetime_200d)
    hkdates = getHousekeepingInteractionDue(sample_ids)
    assert hkdates[sample_ids[0]] == due_datetime_200d
    assert all(sample_id in hkdates.keys() for sample_id in sample_ids)

    # archive one of the requests
    apdb.archiveSamples([sample_ids[0]])

    archivedRequests = apdb.getArchivedRequests()
    assert len(archivedRequests) == 1

    # shouldn't be returned anymore
    hkdates = getHousekeepingInteractionDue(sample_ids)
    assert len(hkdates.values()) == 2

    with pytest.raises(ValueError, match=r"Some samples have already been archived*"):
        apdb.delayHousekeepingInteractionDue(sample_ids, due_datetime_200d)

    hkdates = getHousekeepingInteractionDue(sample_ids)
    # check nothing changed
    assert all(hkdates[sample_id] != due_datetime_200d for sample_id in sample_ids[1:])
    assert len(hkdates) == 2

    # set the dates for the rest of these
    apdb.delayHousekeepingInteractionDue(sample_ids[1:], due_datetime_1y)

    # check everything changed as we expect
    hkdates = getHousekeepingInteractionDue(sample_ids)
    assert all(
        hkdates[sample_id] != due_datetime_200d and hkdates[sample_id] == due_datetime_1y
        for sample_id in sample_ids[1:]
    )
    assert len(hkdates) == 2

    due_now = apdb.getHousekeepingInteractionDueNow()
    assert len(due_now) == 0

    # set housekeeping in the past and check it is marked as due
    due_datetime_past = datetime.now() - timedelta(days=5)
    apdb.delayHousekeepingInteractionDue([sample_ids[-1]], due_datetime_past)
    due_now = apdb.getHousekeepingInteractionDueNow()
    assert len(due_now) == 1

    # set analysis owner and check it turns up.
    wg_o = due_now[0]["wg"]
    ana_o = due_now[0]["analysis"]
    apdb.setOwners(wg=wg_o, analysis=ana_o, owners=["user_who_forgot", "and_another"])

    due_now = apdb.getHousekeepingInteractionDueNow()
    assert "user_who_forgot" in due_now[0]["owner_usernames"]


def test_registerTransformations(apdb):
    apdb.registerRequests([REQUEST_1])

    with pytest.raises(ValueError):
        apdb.registerTransformations({})

    apdb.registerTransformations({1234: {"TUPLE.ROOT": [TRANSFORMS_1a]}})
    assert apdb.getProductions()[0]["transformations"] == [TRANSFORMS_1a]

    with pytest.raises(ValueError, match=r".*already known.*"):
        apdb.registerTransformations({1234: {"TUPLE.ROOT": [TRANSFORMS_1a, TRANSFORMS_1b]}})
    assert apdb.getProductions()[0]["transformations"] == [TRANSFORMS_1a]

    apdb.registerTransformations({1234: {"TUPLE.ROOT": [TRANSFORMS_1b]}})
    assert apdb.getProductions()[0]["transformations"] == [TRANSFORMS_1a, TRANSFORMS_1b]

    apdb.deregisterTransformations({1234: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]}})
    assert apdb.getProductions()[0]["transformations"] == [TRANSFORMS_1b]


def test_registerTransformationsError(apdb):
    """Ensure that nothing is changed if an invalid request ID is passed."""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    with pytest.raises(ValueError, match=r"Did not find requests for IDs: \[\(99999, 'TUPLE.ROOT'\)\]"):
        apdb.registerTransformations(
            {
                987: {"TUPLE.ROOT": [TRANSFORMS_1a]},
                99999: {"TUPLE.ROOT": [TRANSFORMS_1a]},
                988: {"TUPLE.ROOT": [TRANSFORMS_1a]},
            }
        )
    for prod in apdb.getProductions():
        assert prod["transformations"] == [], prod


def test_deregisterTransformationsError(apdb):
    """Ensure that nothing is changed if an invalid request ID is passed."""
    apdb.registerRequests([REQUEST_2, REQUEST_3])
    apdb.registerTransformations({987: {"TUPLE.ROOT": [TRANSFORMS_1a]}, 988: {"TUPLE.ROOT": [TRANSFORMS_1a]}})
    with pytest.raises(ValueError, match=r"Did not find requests for IDs: \[\(99999, \'TUPLE.ROOT\'\)\]"):
        apdb.deregisterTransformations(
            {
                987: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
                99999: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
                988: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
            }
        )
    for prod in apdb.getProductions():
        assert prod["transformations"] == [TRANSFORMS_1a], prod


def test_deregisterTransformationsError2(apdb):
    """Ensure that nothing is changed if an invalid request ID is passed."""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    apdb.registerTransformations(
        {
            1234: {"TUPLE.ROOT": [TRANSFORMS_1a]},
            987: {"TUPLE.ROOT": [TRANSFORMS_1a]},
            988: {"TUPLE.ROOT": [TRANSFORMS_1a]},
        }
    )
    with pytest.raises(ValueError, match=r"Transformation 47 is not known"):
        apdb.deregisterTransformations(
            {
                1234: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
                987: {"TUPLE.ROOT": [TRANSFORMS_1a["id"], 47]},
                988: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
            }
        )
    for prod in apdb.getProductions():
        assert prod["transformations"] == [TRANSFORMS_1a], prod

    apdb.deregisterTransformations(
        {
            1234: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
            987: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
            988: {"TUPLE.ROOT": [TRANSFORMS_1a["id"]]},
        }
    )
    for prod in apdb.getProductions():
        assert prod["transformations"] == [], prod


def test_setState(apdb):
    apdb.registerRequests([REQUEST_1])
    prod1 = apdb.getProductions()[0]
    assert prod1["state"] == "waiting"
    assert "progress" not in prod1

    apdb.setState({(1234, "TUPLE.ROOT"): {"state": "active", "progress": 0.5}})

    prod2 = apdb.getProductions()[0]
    assert prod1["last_state_update"] <= prod2["last_state_update"]
    assert prod2["state"] == "active"
    assert prod2["progress"] == 0.5

    apdb.setState({(1234, "TUPLE.ROOT"): {"state": "ready", "progress": None}})

    prod3 = apdb.getProductions()[0]
    assert prod2["last_state_update"] <= prod3["last_state_update"]
    assert prod3["state"] == "ready"
    assert "progress" not in prod3


def test_setStateMultiple(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_3])
    apdb.setState(
        {
            (1234, "TUPLE.ROOT"): {"state": "active", "progress": 0.5},
            (988, "TUPLE.ROOT"): {"state": "active", "progress": 0.4},
        }
    )
    prod1, prod2 = apdb.getProductions()
    assert prod1["request_id"] == 1234
    assert prod1["state"] == "active"
    assert prod1["progress"] == 0.5
    assert prod2["request_id"] == 988
    assert prod2["state"] == "active"
    assert prod2["progress"] == 0.4
    with pytest.raises(ValueError, match=r"Failed to update Request.*"):
        apdb.setState(
            {
                (1234, "TUPLE.ROOT"): {"state": "active", "progress": 0.6},
                (99999, "TUPLE.ROOT"): {"state": "active", "progress": 0.3},
                (988, "TUPLE.ROOT"): {"state": "active", "progress": 0.7},
            }
        )
    prod1, prod2 = apdb.getProductions()
    assert prod1["request_id"] == 1234
    assert prod1["state"] == "active"
    assert prod1["progress"] == 0.5
    assert prod2["request_id"] == 988
    assert prod2["state"] == "active"
    assert prod2["progress"] == 0.4


def test_getKnownAutoTags(apdb):
    apdb.registerRequests([REQUEST_2])
    assert set(apdb.getKnownAutoTags()) == {"config", "polarity", "datatype"}
    apdb.registerRequests([REQUEST_1])
    assert set(apdb.getKnownAutoTags()) == {"config", "polarity", "eventtype", "datatype"}


def test_setTagsNoChanges(apdb):
    """Setting tags to the same value should be a no-op."""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    apdb.setTags(
        {
            1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
            2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
        },
        {
            1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
            2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
        },
    )
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
        3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
    }
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }


def test_setTagsCaseInsensitive(apdb):
    """Tags should always be lowercased"""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    apdb.setTags(
        {
            2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
        },
        {
            2: {"config": "lhcb", "Polarity": "MagUp", "datatype": "2018"},
        },
    )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }
    apdb.setTags(
        {
            2: {"config": "lhcb", "Polarity": "MagUp", "datatype": "2018"},
        },
        {
            2: {"config": "lhcb", "polarity": "MagUp", "datatype": "2018"},
        },
    )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }
    apdb.setTags(
        {
            2: {"config": "lhcb", "Polarity": "MagUp", "datatype": "2018"},
        },
        {
            2: {"config": "lhcb", "polarity": "MagUp", "dataType": "2018", "HELLO": "WORLD", "FoO": 123},
        },
    )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "hello": "world", "foo": "123"}
    }
    with pytest.raises(ValueError, match=r".*contains duplicate keys.*"):
        apdb.setTags(
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
            },
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "hello": "world", "HELLO": 123},
            },
        )
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
        3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
    }


def test_setTagsWithChanges(apdb):
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    apdb.setTags(
        {
            3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
        },
        {
            3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"},
        },
    )
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
        3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_ss"},
    }
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }


def test_setTagsMissingOldTags(apdb):
    """Tags cannot be changed if oldTags isn't up to date"""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    with pytest.raises(ValueError, match=r".*must contain the same keys.*"):
        apdb.setTags(
            {},
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"},
            },
        )
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
        3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
    }
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }


def test_setTagsWrongOldTags(apdb):
    """Tags cannot be changed if oldTags isn't up to date"""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    apdb.setTags(
        {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}},
        {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"}},
    )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_ss"}
    }
    with pytest.raises(ValueError, match=r"oldTags is out of date"):
        apdb.setTags(
            {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}},
            {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}},
        )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_ss"}
    }
    with pytest.raises(ValueError, match=r"oldTags is out of date"):
        apdb.setTags(
            {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_os"}},
            {2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_ws"}},
        )
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "dptokpipi_ss"}
    }


# def test_setTagsOutdated(apdb):


def test_setTagsAutoTags(apdb):
    """Ensure AutoTags cannot be added, removed or modified"""
    apdb.registerRequests([REQUEST_1, REQUEST_2, REQUEST_3])
    with pytest.raises(ValueError, match=r"Cannot modify AutoTags.*"):
        apdb.setTags(
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
                2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
            },
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"},
                2: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "eventtype": "90000000"},
            },
        )
    with pytest.raises(ValueError, match=r"Cannot modify AutoTags.*"):
        apdb.setTags(
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
                2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
            },
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"},
                2: {"config": "lhcb", "polarity": "magdown", "datatype": "2018"},
            },
        )
    with pytest.raises(ValueError, match=r"Cannot modify AutoTags.*"):
        apdb.setTags(
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
                2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
            },
            {
                3: {"config": "lhcb", "polarity": "magup", "datatype": "2018", "sample": "DpToKpipi_SS"},
                2: {"config": "lhcb", "polarity": "magup"},
            },
        )
    assert apdb.getTags("MyWG", "MyAnalysis") == {
        1: {"config": "mc", "polarity": "magdown", "eventtype": "23133002", "datatype": "2012"},
        3: {"config": "lhcb", "polarity": "magup", "datatype": "2018"},
    }
    assert apdb.getTags("AnotherWG", "AnotherAnalysis") == {
        2: {"config": "lhcb", "polarity": "magup", "datatype": "2018"}
    }
