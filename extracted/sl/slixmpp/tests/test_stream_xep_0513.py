import unittest.mock

from slixmpp.test import SlixTest


class TestExplicitMentions(SlixTest):
    def setUp(self) -> None:
        self.stream_start(plugins={"xep_0513"})

    def test_event(self) -> None:
        with unittest.mock.MagicMock() as on_mention:
            self.xmpp.add_event_handler("mention", on_mention)  # type:ignore
            self.recv(
                """
                <message to='news@chat.commons.example' type='groupchat'>
                <body>Hello, Alice!</body>
                <mention xmlns='urn:xmpp:mentions:0'
                    begin='7'
                    end='12'
                    occupantid='alice@occupant-id'/>
                </message>
                """
            )
        on_mention.assert_called_once()
        msg = on_mention.call_args[0][0]
        assert msg["mention"]["begin"] == 7


suite = unittest.TestLoader().loadTestsFromTestCase(TestExplicitMentions)
