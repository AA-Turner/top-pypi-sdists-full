###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import pytest
from DIRAC import S_OK

import LHCbDIRAC
from LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB import BookkeepingResultMismatch, ProxyMethod
from LHCbDIRAC.BookkeepingSystem.DB.LegacyOracleBookkeepingDB import LegacyOracleBookkeepingDB
from LHCbDIRAC.BookkeepingSystem.DB.NewOracleBookkeepingDB import NewOracleBookkeepingDB


class DemoException(Exception):
    pass


def _raising_function(self):
    raise DemoException("This should never be reached")


@pytest.fixture
def fake_bkdb(monkeypatch, bkdb):
    """Return an instance of OracleBookkeepingDB with fake methods monkeypatched."""
    monkeypatch.setattr(
        LegacyOracleBookkeepingDB, "fakeDuplicated", lambda _: S_OK("resultLegacyDuplicated"), raising=False
    )
    monkeypatch.setattr(NewOracleBookkeepingDB, "fakeDuplicated", lambda _: S_OK("resultNewDuplicated"), raising=False)

    monkeypatch.setattr(LegacyOracleBookkeepingDB, "fakeMatching", lambda _: S_OK("resultIdentical"), raising=False)
    monkeypatch.setattr(NewOracleBookkeepingDB, "fakeMatching", lambda _: S_OK("resultIdentical"), raising=False)

    monkeypatch.setattr(
        LegacyOracleBookkeepingDB, "fakeLegacyOnly", lambda _: S_OK("resultLegacyLegacyOnly"), raising=False
    )

    monkeypatch.setattr(NewOracleBookkeepingDB, "fakeNewOnly", lambda _: S_OK("resultNewNewOnly"), raising=False)

    monkeypatch.setattr(
        LegacyOracleBookkeepingDB, "fakeNewRaises", lambda _: S_OK("resultLegacyNewRaises"), raising=False
    )
    monkeypatch.setattr(NewOracleBookkeepingDB, "fakeNewRaises", _raising_function, raising=False)

    monkeypatch.setattr(LegacyOracleBookkeepingDB, "fakeLegacyRaises", _raising_function, raising=False)
    monkeypatch.setattr(
        NewOracleBookkeepingDB, "fakeLegacyRaises", lambda _: S_OK("resultNewLegacyRaises"), raising=False
    )

    monkeypatch.setattr(
        LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB,
        "DUPLICATION_SAFE_METHODS",
        ["fakeDuplicated", "fakeLegacyOnly", "fakeNewOnly", "fakeMatching"],
    )

    yield bkdb


def test_preferred_implementation(monkeypatch, fake_bkdb):
    assert not isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultLegacyDuplicated")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)

    assert isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultLegacyDuplicated")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeDuplicated"])

    assert isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultNewDuplicated")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", False)

    assert not isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultNewDuplicated")


def test_exception_not_raised(monkeypatch, fake_bkdb):
    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "FAIL_ON_DIFFERENCE", True)

    assert not isinstance(fake_bkdb.fakeMatching, ProxyMethod)
    assert fake_bkdb.fakeMatching() == S_OK("resultIdentical")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)

    assert isinstance(fake_bkdb.fakeMatching, ProxyMethod)
    assert fake_bkdb.fakeMatching() == S_OK("resultIdentical")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeMatching"])

    assert isinstance(fake_bkdb.fakeMatching, ProxyMethod)
    assert fake_bkdb.fakeMatching() == S_OK("resultIdentical")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", False)

    assert not isinstance(fake_bkdb.fakeMatching, ProxyMethod)
    assert fake_bkdb.fakeMatching() == S_OK("resultIdentical")


def test_exception_raised(monkeypatch, fake_bkdb):
    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "FAIL_ON_DIFFERENCE", True)

    assert not isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultLegacyDuplicated")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)

    assert isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    with pytest.raises(BookkeepingResultMismatch):
        fake_bkdb.fakeDuplicated()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeDuplicated"])

    assert isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    with pytest.raises(BookkeepingResultMismatch):
        fake_bkdb.fakeDuplicated()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", False)

    assert not isinstance(fake_bkdb.fakeDuplicated, ProxyMethod)
    assert fake_bkdb.fakeDuplicated() == S_OK("resultNewDuplicated")


@pytest.mark.parametrize(
    "name,expected_result",
    [
        ["fakeLegacyOnly", "resultLegacyLegacyOnly"],
        ["fakeNewOnly", "resultNewNewOnly"],
    ],
)
def test_one_only(monkeypatch, fake_bkdb, name, expected_result):
    assert not isinstance(getattr(fake_bkdb, name), ProxyMethod)
    assert getattr(fake_bkdb, name)() == S_OK(expected_result)

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)

    assert not isinstance(getattr(fake_bkdb, name), ProxyMethod)
    assert getattr(fake_bkdb, name)() == S_OK(expected_result)

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeLegacyOnly"])

    assert not isinstance(getattr(fake_bkdb, name), ProxyMethod)
    assert getattr(fake_bkdb, name)() == S_OK(expected_result)


def test_new_raising(monkeypatch, fake_bkdb):
    assert not isinstance(fake_bkdb.fakeNewRaises, ProxyMethod)
    assert fake_bkdb.fakeNewRaises() == S_OK("resultLegacyNewRaises")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)
    assert fake_bkdb.fakeNewRaises() == S_OK("resultLegacyNewRaises")

    monkeypatch.setattr(
        LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DUPLICATION_SAFE_METHODS", ["fakeNewRaises"]
    )
    with pytest.raises(DemoException):
        fake_bkdb.fakeNewRaises()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", False)
    assert fake_bkdb.fakeNewRaises() == S_OK("resultLegacyNewRaises")

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeNewRaises"])
    with pytest.raises(DemoException):
        fake_bkdb.fakeNewRaises()


def test_legacy_raising(monkeypatch, fake_bkdb):
    assert not isinstance(fake_bkdb.fakeNewRaises, ProxyMethod)
    with pytest.raises(DemoException):
        fake_bkdb.fakeLegacyRaises()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", True)
    with pytest.raises(DemoException):
        fake_bkdb.fakeLegacyRaises()

    monkeypatch.setattr(
        LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DUPLICATION_SAFE_METHODS", ["fakeLegacyRaises"]
    )
    with pytest.raises(DemoException):
        fake_bkdb.fakeLegacyRaises()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "DO_COMPARE", False)
    with pytest.raises(DemoException):
        fake_bkdb.fakeLegacyRaises()

    monkeypatch.setattr(LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB, "METHODS_PREFER_NEW", ["fakeLegacyRaises"])
    assert fake_bkdb.fakeLegacyRaises() == S_OK("resultNewLegacyRaises")
