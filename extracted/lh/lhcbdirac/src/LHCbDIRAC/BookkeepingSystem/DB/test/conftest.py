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
from urllib.parse import urlparse

import pytest


@pytest.fixture
def bkdb(request, monkeypatch):
    # These imports need to be protected else the tests can only be ran for
    # editable installs
    import LHCbDIRAC
    from LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB import OracleBookkeepingDB

    oracle_url = request.config.getoption("--oracle-url")
    if oracle_url is None:
        pytest.skip("Requires an Oracle DB connection string to be passed with --oracle-url")
    parsed = urlparse(oracle_url)
    assert parsed.scheme == "oracle", "Only Oracle connections are supported"

    monkeypatch.setattr(
        LHCbDIRAC.BookkeepingSystem.DB.OracleBookkeepingDB,
        "getDatabaseSection",
        lambda a, b: f"/Systems/{a}/Production/Databases/{b}",
    )

    # By default, oracle uses out-of-band (OOB) communication which uses a
    # random port for sending additional data. When running the DB in a docker
    # container this makes it impossible to connect to the DB from the host as
    # we can't predict what the port will be to forward it (and it changes for
    # every connection attempt). An alternative would be to use `--net=host`
    # but `disable_oob=True` is cleaner.
    yield OracleBookkeepingDB(
        username=parsed.username,
        password=parsed.password,
        host=f"{parsed.hostname}:{parsed.port or 1521}{parsed.path}",
        disable_oob=True,
    )
