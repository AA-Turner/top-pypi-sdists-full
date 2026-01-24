import logging
import os
from uuid import uuid4 as new_uuid

import pytest

import btrdb
from btrdb.exceptions import BTrDBError
from btrdb.utils.credentials import credentials_by_profile


@pytest.mark.skipif(
    os.getenv("BTRDB_INTEGRATION_TEST_PROFILE") is None,
    reason="Need an integration test server to run integration tests.",
)
class TestConnection:
    def test_connection_info(self, conn):
        info = conn.info()
        logging.info(f"connection info: {info}")

    def test_incorrect_connect(
        self,
    ):
        env_name = os.getenv("BTRDB_INTEGRATION_TEST_PROFILE")
        creds = credentials_by_profile(env_name)
        conn_str = creds["endpoints"]
        err_msg = r"""Could not connect to the database, error message: <_InactiveRpcError of RPC that terminated with:\n\tstatus = StatusCode.UNAUTHENTICATED\n\tdetails = "invalid api key"\n"""
        with pytest.raises(BTrDBError, match=err_msg):
            conn = btrdb.connect(conn_str=conn_str, apikey="BOGUS_KEY")

    @pytest.mark.xfail(
        reason="Should return BTrDBError, but returns GRPCError instead, FIXME"
    )
    def test_from_uuid(self, conn):
        # todo, investigate this, the stat code returned is 0, which is why its not being returned as a btrdb error
        uu = new_uuid()
        stream = conn.stream_from_uuid(uu)
        with pytest.raises(btrdb.exceptions.BTrDBError):
            print(stream)

    def test_create_stream(self, conn, tmp_collection):
        uuid = new_uuid()
        stream = conn.create(uuid, tmp_collection, tags={"name": "s"})
        assert stream.uuid == uuid
        assert stream.name == "s"

    def test_query(self, conn, tmp_collection):
        conn.create(new_uuid(), tmp_collection, tags={"name": "s1"})
        conn.create(new_uuid(), tmp_collection, tags={"name": "s2"})
        uuids = conn.query(
            "select name from streams where collection = $1 order by name;",
            [tmp_collection],
        )
        assert len(uuids) == 2
        assert uuids[0]["name"] == "s1"
        assert uuids[1]["name"] == "s2"

    def test_list_collections(self, conn, tmp_collection):
        assert tmp_collection not in conn.list_collections()
        stream = conn.create(new_uuid(), tmp_collection, tags={"name": "s"})
        assert tmp_collection in conn.list_collections()
