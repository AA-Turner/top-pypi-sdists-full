import unittest
from slixmpp.test.integration import SlixIntegration


class TestSos(SlixIntegration):
    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.add_client(
            self.envjid('CI_ACCOUNT1'),
            self.envstr('CI_ACCOUNT1_PASSWORD'),
        )
        self.register_plugins(['xep_0455'])
        await self.connect_clients()

    async def test_sos(self):
        """Check we can get the status addr and fetch empty data"""
        addresses = await self.clients[0]['xep_0455'].get_external_status_addresses()
        self.assertGreaterEqual(len(addresses), 1)
        fetched_status = await self.clients[0]['xep_0455'].fetch_status(addresses[0])
        self.assertEqual(fetched_status, None)


suite = unittest.TestLoader().loadTestsFromTestCase(TestSos)
