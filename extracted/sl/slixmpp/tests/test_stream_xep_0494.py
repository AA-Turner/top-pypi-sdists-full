import unittest
from slixmpp.exceptions import IqError
from slixmpp.test import SlixTest


class TestLiveCam(SlixTest):

    def setUp(self):
        self.stream_start(plugins=['xep_0494'])

    def test_request_clients(self):
        """Request a client list"""

        clients = []

        async def run():
            clients.extend(await self.xmpp['xep_0494'].get_clients())

        self.xmpp.wrap(run())
        self.wait_()

        self.send("""
          <iq type="get" id="1">
            <list xmlns="urn:xmpp:cam:0"/>
          </iq>
        """)

        self.recv("""
<iq type="result" id="1">
  <clients xmlns="urn:xmpp:cam:0">
    <client connected="true" id="zeiP41HLglIu" type="session">
      <first-seen>2023-04-06T14:26:08Z</first-seen>
      <last-seen>2023-04-06T14:37:25Z</last-seen>
      <auth>
        <password/>
      </auth>
      <permission status="unrestricted"/>
      <user-agent>
        <software>Gajim</software>
        <uri>https://gajim.org/</uri>
        <device>Juliet's laptop</device>
      </user-agent>
    </client>
    <client connected="false" id="HjEEr45_LQr" type="access">
      <first-seen>2023-03-27T15:16:09Z</first-seen>
      <last-seen>2023-03-27T15:37:24Z</last-seen>
      <auth>
          <grant/>
      </auth>
      <permission status="normal"/>
      <user-agent>
        <software>REST client</software>
      </user-agent>
    </client>
  </clients>
</iq>
        """)
        self.wait_()
        self.assertEqual(len(clients), 2)
        self.assertTrue(clients[0]['connected'])
        self.assertEqual(clients[0]['type'].value, 'session')
        self.assertTrue(clients[0]['auth']['password'])
        self.assertFalse(clients[0]['auth']['fast'])
        self.assertEqual(clients[0]['permission'].value, 'unrestricted')
        self.assertEqual(clients[0]['user_agent']['software'], 'Gajim')
        self.assertFalse(clients[1]['connected'])

    def test_revoke_client(self):
        """Try to revoke a client"""

        result = []

        async def run():
            await self.xmpp['xep_0494'].revoke('toto')
            result.append(True)

        self.xmpp.wrap(run())
        self.wait_()

        self.send("""
          <iq type="get" id="1">
            <revoke xmlns="urn:xmpp:cam:0" id="toto"/>
          </iq>
        """)
        self.recv("""
          <iq type="result" id="1"/>
        """)
        self.wait_()

        self.assertTrue(result)

    def test_revoke_client_fail(self):
        """Try to revoke a client and fail"""

        result = []

        async def run():
            try:
                await self.xmpp['xep_0494'].revoke('toto')
            except IqError:
                result.append(True)

        self.xmpp.wrap(run())
        self.wait_()

        self.send("""
          <iq type="get" id="1">
            <revoke xmlns="urn:xmpp:cam:0" id="toto"/>
          </iq>
        """)
        self.recv("""
          <iq type="error" id="1"/>
        """)
        self.wait_()

        self.assertTrue(result)


suite = unittest.TestLoader().loadTestsFromTestCase(TestLiveCam)
