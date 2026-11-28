import unittest.mock

from slixmpp.test import SlixTest


class TestIntentionalMentions(SlixTest):
    def setUp(self) -> None:
        self.stream_start(plugins={"xep_0513"})

    def test_event(self) -> None:
        with unittest.mock.MagicMock() as on_mention:
            self.xmpp.add_event_handler("mention", on_mention)  # type:ignore
            self.recv(
                """
                <message to='news@chat.commons.example' type='groupchat'>
                  <body>Hello, Alice!</body>
                  <markup xmlns='urn:xmpp:markup:0'>
                    <span start='7' end='12'>
                      <mention xmlns='urn:xmpp:mentions:0'
                        type='urn:xmpp:mentions:0#occupant'
                        target='alice@occupant-id' />
                    </span>
                  </markup>
                </message>
                """
            )
        on_mention.assert_called_once()
        msg = on_mention.call_args[0][0]
        span = msg["markup"]["span"]
        assert span["start"] == 7
        assert span["end"] == 12
        assert span["mentions"][0]["target"] == "alice@occupant-id"

    def test_no_event_without_mention(self) -> None:
        with unittest.mock.MagicMock() as on_mention:
            self.xmpp.add_event_handler("mention", on_mention)  # type:ignore
            self.recv(
                """
                <message to='news@chat.commons.example' type='groupchat'>
                  <body>Hello, everyone!</body>
                </message>
                """
            )
        on_mention.assert_not_called()

    def test_event_fires_once_per_message_with_several_mentions(self) -> None:
        with unittest.mock.MagicMock() as on_mention:
            self.xmpp.add_event_handler("mention", on_mention)  # type:ignore
            self.recv(
                """
                <message to='news@chat.commons.example' type='groupchat'>
                  <body>Hi Alice and Bob</body>
                  <markup xmlns='urn:xmpp:markup:0'>
                    <span start='3' end='8'>
                      <mention xmlns='urn:xmpp:mentions:0'
                        type='urn:xmpp:mentions:0#occupant' target='alice' />
                      <mention xmlns='urn:xmpp:mentions:0'
                        type='urn:xmpp:mentions:0#occupant' target='bob' />
                    </span>
                  </markup>
                </message>
                """
            )
        on_mention.assert_called_once()
        msg = on_mention.call_args[0][0]
        self.assertEqual(
            [m["target"] for m in msg["markup"]["span"]["mentions"]],
            ["alice", "bob"],
        )

    def test_feature_advertised(self) -> None:
        info = self.xmpp.plugin["xep_0030"].static.get_info(None, None, None, {})
        self.assertIn("urn:xmpp:mentions:0", info["features"])


suite = unittest.TestLoader().loadTestsFromTestCase(TestIntentionalMentions)
