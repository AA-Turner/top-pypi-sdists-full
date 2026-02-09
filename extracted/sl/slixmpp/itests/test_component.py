import os
import unittest

from slixmpp.componentxmpp import ComponentXMPP
from slixmpp import JID

IN_CI = os.getenv('CI') == 'woodpecker'


class SlixComponentIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.component = ComponentXMPP(CI_JID, CI_SECRET, CI_SERVER, CI_PORT)
        self.component.register_plugin("xep_0199")
        await self.component.connect()
        await self.component.wait_until("session_start")

    async def asyncTearDown(self):
        self.component.abort()

    @unittest.skipIf(not IN_CI, "Not in woodpecker CI")
    async def test_ping(self):
        """Check that a component can connect and send a ping to the server"""
        jid = JID(f"whatever@{CI_JID}")
        iq_pong = await self.component.plugin["xep_0199"].send_ping(JID(CI_SERVER), ifrom=jid)
        self.assertEqual(iq_pong["type"], "result")
        self.assertEqual(iq_pong.get_to(), jid)


CI_JID = "slixmpp.prosody"
CI_SECRET = "secret"
CI_SERVER = "prosody"
CI_PORT = 5347

suite = unittest.TestLoader().loadTestsFromTestCase(SlixComponentIntegration)
