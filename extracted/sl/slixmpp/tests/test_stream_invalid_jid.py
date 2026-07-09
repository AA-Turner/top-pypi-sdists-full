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
        self.send(None, timeout=0.05)

    def test_component_presence_to(self) -> None:
        self.stream_start(mode="component", plugins=[])
        self.recv(
            f"""
            <presence from="whatever@whatever" to="{self.xmpp.boundjid.bare}/🎉">
            </presence>
            """
        )
        self.send(None, timeout=0.05)

    def test_client_presence_from(self) -> None:
        self.stream_start(mode="client", plugins=[])
        self.recv(
            f"""
            <presence from="whatever@whatever/🎉" to="{self.xmpp.boundjid.bare}">
            </presence>
            """
        )
        self.send(None, timeout=0.05)

    def test_iq_get_no_handler(self) -> None:
        # xep_0086 "stays loaded" somwhoe when running the full test suite, so
        # we have to load it here to consistently get that code="501"
        self.stream_start(
            mode="component", jid="matridge.h.redacted.eu", plugins=["xep_0086"]
        )
        self.recv(
            """
            <iq from="redacted@h.redacted.eu/Monal-iOS"
                id="some-id"
                type="get"
                to="xxx@matridge.h.redacted.eu/xmpp:redacted@redacted.eu 🏳🌈♾">
              <ping xmlns="urn:xmpp:ping" />
            </iq>
            """
        )
        self.send(
            """
            <iq xmlns="jabber:component:accept"
                from="xxx@matridge.h.redacted.eu/xmpp:redacted@redacted.eu 🏳🌈♾"
                id="some-id"
                to="redacted@h.redacted.eu/Monal-iOS"
                type="error">
              <error xmlns="jabber:client" code="501" type="cancel">
                <feature-not-implemented xmlns="urn:ietf:params:xml:ns:xmpp-stanzas" />
                <text xmlns="urn:ietf:params:xml:ns:xmpp-stanzas">No handlers registered for this request.</text>
              </error>
            </iq>
            """,
        )

    def test_iq_get(self) -> None:
        self.stream_start(
            mode="component", jid="matridge.h.redacted.eu", plugins=["xep_0410"]
        )
        self.recv(
            """
            <iq from="redacted@h.redacted.eu/Monal-iOS"
                id="some-id"
                type="get"
                to="xxx@matridge.h.redacted.eu/xmpp:redacted@redacted.eu 🏳🌈♾">
              <ping xmlns="urn:xmpp:ping" />
            </iq>
            """
        )
        self.send(
            """
            <iq xmlns="jabber:component:accept"
                from="xxx@matridge.h.redacted.eu/xmpp:redacted@redacted.eu 🏳🌈♾"
                id="some-id"
                to="redacted@h.redacted.eu/Monal-iOS"
                type="result">
            </iq>
            """,
        )


suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamInvalidJID)
