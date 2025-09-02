# Slixmpp: The Slick XMPP Library
# Copyright (C) 2025 Mathieu Pasquet
# This file is part of Slixmpp.
# See the file LICENSE for copying permission.

import unittest
from datetime import datetime
from slixmpp.test import SlixTest
from slixmpp.plugins.xep_0494 import XEP_0494
import slixmpp.plugins.xep_0494.stanza as stanza


class TestCAM(SlixTest):

    def setUp(self):
        stanza.register_plugins()

    def test_stanzabuild(self):
        """Testing creating a stanza."""

        xmlstring = """
<iq>
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
        """

        iq = self.Iq()
        client = iq['clients']['client']
        client['connected'] = True
        client['first_seen'] = '2023-04-06T14:26:08Z'
        client['last_seen'] = '2023-04-06T14:37:25Z'
        client['id'] = 'zeiP41HLglIu'
        client['type'] = 'session'
        client['auth']['password'] = True
        client['permission'] = 'unrestricted'
        client['user_agent']['software'] = 'Gajim'
        client['user_agent']['uri'] = 'https://gajim.org/'
        client['user_agent']['device'] = 'Juliet\'s laptop'
        client2 = stanza.Client()
        iq['clients'].append(client2)
        client2['connected'] = False
        client2['first_seen'] = datetime.fromisoformat('2023-03-27T15:16:09Z')
        client2['last_seen'] = '2023-03-27T15:37:24Z'
        client2['id'] = 'HjEEr45_LQr'
        client2['type'] = 'access'
        client2['auth'].enable('grant')
        client2['permission'] = 'normal'
        client2['user_agent']['software'] = 'REST client'

        self.check(iq, xmlstring, use_values=False)


suite = unittest.TestLoader().loadTestsFromTestCase(TestCAM)
