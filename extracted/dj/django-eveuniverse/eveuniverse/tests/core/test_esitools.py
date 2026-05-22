import pook

from eveuniverse.core import esitools
from eveuniverse.tests.helpers import TestCaseWithClearCache
from eveuniverse.tests.testdata.factories_2 import make_esi_url


class TestIsEsiOnline(TestCaseWithClearCache):
    @pook.on
    def test_is_online(self):
        # given
        pook.get(
            make_esi_url("status"),
            reply=200,
            response_json={
                "players": 42,
                "server_version": "version",
                "start_time": "2019-08-24T14:15:22Z",
            },
        )

        # when/then
        self.assertTrue(esitools.is_esi_online())

    @pook.on
    def test_is_offline(self):
        # given
        pook.get(
            make_esi_url("status"),
            reply=500,
            response_json={"error": "error"},
        )

        # then
        self.assertFalse(esitools.is_esi_online())

    @pook.on
    def test_should_report_vip_as_offline(self):
        # given
        pook.get(
            make_esi_url("status"),
            reply=200,
            response_json={
                "players": 42,
                "server_version": "version",
                "start_time": "2019-08-24T14:15:22Z",
                "vip": True,
            },
        )

        # when/then
        self.assertFalse(esitools.is_esi_online())
