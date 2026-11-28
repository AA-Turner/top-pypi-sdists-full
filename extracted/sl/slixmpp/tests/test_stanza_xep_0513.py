import unittest

from slixmpp import Message
from slixmpp.plugins.xep_0394 import stanza as xep_0394
from slixmpp.plugins.xep_0513 import stanza
from slixmpp.test import SlixTest
from slixmpp.xmlstream import ET


class TestMentions(SlixTest):
    def setUp(self) -> None:
        stanza.register_plugin()

    def test_individual_mention(self) -> None:
        msg = Message()
        span = msg["markup"]["span"]
        span["start"] = 7
        span["end"] = 12
        span["mention"]["type"] = "occupant"
        span["mention"]["target"] = "occ-1"

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='7' end='12'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='occ-1' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_multiple_mentions_in_one_span(self) -> None:
        """Several occupants in one span."""
        msg = Message()

        span = msg["markup"]["span"]
        span["start"] = 3
        span["end"] = 14
        for target in ("occ-1", "occ-2"):
            mention = stanza.Mention()
            mention["type"] = "occupant"
            mention["target"] = target
            span.append(mention)

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='3' end='14'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='occ-1' />
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='occ-2' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_multiple_spans(self) -> None:
        """Two separate mentions in one body, each with its own span."""
        msg = Message()

        first = msg["markup"]["span"]
        first["start"] = 0
        first["end"] = 5
        first["mention"]["type"] = "occupant"
        first["mention"]["target"] = "alice-id"

        second = xep_0394.Span()
        second["start"] = 10
        second["end"] = 13
        second["mention"]["type"] = "occupant"
        second["mention"]["target"] = "bob-id"
        msg["markup"].append(second)

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='0' end='5'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='alice-id' />
                </span>
                <span start='10' end='13'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='bob-id' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_channel_mention_active(self) -> None:
        """@here style mention."""
        msg = Message()

        span = msg["markup"]["span"]
        span["start"] = 0
        span["end"] = 5
        span["mention"]["type"] = "channel"
        span["mention"]["active"] = True

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='0' end='5'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#channel'
                    active='true' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_channel_mention_without_target(self) -> None:
        """channel mention MUST NOT carry a target."""
        msg = Message()
        span = msg["markup"]["span"]
        span["start"] = 5
        span["end"] = 10
        span["mention"]["type"] = "channel"

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='5' end='10'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#channel' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_role_mention_moderators(self) -> None:
        """Mention by role."""
        msg = Message()

        span = msg["markup"]["span"]
        span["start"] = 4
        span["end"] = 13
        span["mention"]["type"] = "moderators"

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='4' end='13'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#moderators' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_all_role_and_affiliation_types_expand(self) -> None:
        for typ in (
            "moderators",
            "participants",
            "visitors",
            "owners",
            "admins",
            "members",
            "none",
        ):
            with self.subTest(typ=typ):
                mention = stanza.Mention()
                mention["type"] = typ
                self.assertEqual(mention["type"], f"urn:xmpp:mentions:0#{typ}")

    def test_hats_mention(self) -> None:
        """Hats mention; target is the hat URI."""
        msg = Message()

        span = msg["markup"]["span"]
        span["start"] = 7
        span["end"] = 15
        span["mention"]["type"] = "urn:xmpp:mentions:0#hats"
        span["mention"]["target"] = "http://schemas.example.com/hats#students"

        self.check(
            msg,
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='7' end='15'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#hats'
                    target='http://schemas.example.com/hats#students' />
                </span>
              </markup>
            </message>
            """,
        )

    def test_active_false_is_omitted(self) -> None:
        mention = stanza.Mention()
        mention["type"] = "channel"
        mention["active"] = False
        self.assertFalse(mention["active"])
        self.assertNotIn("active", mention.xml.attrib)

    def test_parse_incoming_stanza(self) -> None:
        xml = ET.fromstring(
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='7' end='12'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#occupant'
                    target='alice-occupant' />
                </span>
              </markup>
            </message>
            """
        )
        msg = Message(xml=xml)
        span = msg["markup"]["span"]
        self.assertEqual(span["start"], 7)
        self.assertEqual(span["end"], 12)
        mention = span["mentions"][0]
        self.assertEqual(mention["type"], "urn:xmpp:mentions:0#occupant")
        self.assertEqual(mention["target"], "alice-occupant")
        self.assertFalse(mention["active"])

    def test_parse_incoming_channel_mention_active(self) -> None:
        xml = ET.fromstring(
            """
            <message>
              <markup xmlns='urn:xmpp:markup:0'>
                <span start='0' end='5'>
                  <mention xmlns='urn:xmpp:mentions:0'
                    type='urn:xmpp:mentions:0#channel' active='true' />
                </span>
              </markup>
            </message>
            """
        )
        mention = Message(xml=xml)["markup"]["span"]["mentions"][0]
        self.assertTrue(mention["active"])
        self.assertIsNone(mention["target"])


suite = unittest.TestLoader().loadTestsFromTestCase(TestMentions)
