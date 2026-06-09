import unittest

from slixmpp.test import SlixTest


class TestStreamInvalidJID(SlixTest):
    """
    Test handling stanzas from invalid JIDs
    """

    def test_component_presence_from(self) -> None:
        self.stream_start(mode="component", plugins=[])
        self.recv(
            f"""
            <presence from="whatever@whatever/🎉" to="{self.xmpp.boundjid.bare}">
            </presence>
            """
        )
        self.send(None)

    def test_component_presence_to(self) -> None:
        self.stream_start(mode="component", plugins=[])
        self.recv(
            f"""
            <presence from="whatever@whatever" to="{self.xmpp.boundjid.bare}/🎉">
            </presence>
            """
        )
        self.send(None)

    def test_client_presence_from(self) -> None:
        self.stream_start(mode="client", plugins=[])
        self.recv(
            f"""
            <presence from="whatever@whatever/🎉" to="{self.xmpp.boundjid.bare}">
            </presence>
            """
        )
        self.send(None)


suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamInvalidJID)
