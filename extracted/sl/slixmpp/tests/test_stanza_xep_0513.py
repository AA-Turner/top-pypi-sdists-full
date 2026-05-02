import unittest

from slixmpp import Message
from slixmpp.plugins.xep_0513 import stanza
from slixmpp.test import SlixTest


class TestMentions(SlixTest):
    def setUp(self) -> None:
        stanza.register_plugin()

    def test_modifier(self) -> None:
        for modifier in "active", "noping":
            msg = Message()
            msg["mention"].enable(modifier)
            self.check(
                msg,
                f"""
                <message xmlns="jabber:client">
                <mention xmlns="urn:xmpp:mentions:0">
                    <{modifier} />
                </mention>
                </message>
                """
            )

    def test_multi(self) -> None:
        msg = Message()
        m1 = stanza.Mention()
        m1["uri"] = "some-uri"
        m2 = stanza.Mention()
        m2["jid"] = "user@server"
        msg.append(m1)
        msg.append(m2)
        self.check(
            msg,
            """
            <message xmlns="jabber:client">
            <mention xmlns="urn:xmpp:mentions:0" uri="some-uri" />
            <mention xmlns="urn:xmpp:mentions:0" jid="user@server" />
            </message>
            """
        )

        self.assertEqual(msg["mentions"][0]["uri"], "some-uri")
        self.assertEqual(msg["mentions"][1]["jid"].server, "server")


suite = unittest.TestLoader().loadTestsFromTestCase(TestMentions)
