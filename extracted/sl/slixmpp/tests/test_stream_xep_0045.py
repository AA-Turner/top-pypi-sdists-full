import unittest
import unittest.mock

from slixmpp.test import SlixTest


class TestMUC(SlixTest):
    def setUp(self):
        self.stream_start(plugins=['xep_0045', 'xep_0030'])

    def test_new_affiliation(self):
        handler = unittest.mock.AsyncMock()
        self.xmpp.add_event_handler("muc::room@rooms.test::affiliation_change", handler)
        self.recv(  # language=XML
            """
            <message from="room@rooms.test">
              <x xmlns="http://jabber.org/protocol/muc#user">
                <item jid="caca@prout"
                      affiliation="member" />
              </x>
            </message>
            """
        )
        handler.assert_awaited_once()
        msg = handler.call_args.args[0]
        assert msg["muc"]["item"]["jid"] == "caca@prout"
        assert msg["muc"]["item"]["affiliation"] == "member"

    def test_remove_affiliation(self):
        handler = unittest.mock.AsyncMock()
        self.xmpp.add_event_handler("muc::room@rooms.test::affiliation_change", handler)
        self.recv(  # language=XML
            """
            <message from="room@rooms.test">
              <x xmlns="http://jabber.org/protocol/muc#user">
                <status code="321" />
                <item jid="caca@prout"
                      affiliation="none" />
              </x>
            </message>
            """
        )
        handler.assert_awaited_once()
        msg = handler.call_args.args[0]
        assert msg["muc"]["item"]["jid"] == "caca@prout"
        assert msg["muc"]["item"]["affiliation"] == "none"


suite = unittest.TestLoader().loadTestsFromTestCase(TestMUC)
