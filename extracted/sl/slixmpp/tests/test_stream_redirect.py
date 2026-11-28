import unittest.mock
from slixmpp.test import SlixTest


class TestStreamSeeOtherHost(SlixTest):
    """
    Test that we properly handle see-other-host
    """

    def test_other_host_secure_redirect(self):
        """Test if a secure redirect is properly handled."""
        self.stream_start(mode='client', jid='tester@localhost')

        # Mock an established TLS connection: redirects are allowed
        self.xmpp.transport.make_secure()
        with unittest.mock.MagicMock() as on_error:
            self.xmpp.add_event_handler('stream_error', on_error)
            self.recv("""
                <stream:error>
                    <see-other-host xmlns='urn:ietf:params:xml:ns:xmpp-streams'>[2001:41D0:1:A49b::1]:9222</see-other-host>
                </stream:error>
            """)
            on_error.assert_called_once()
        # Ensure the domain has not changed
        self.assertEqual(self.xmpp.default_domain, 'localhost')
        # But the custom address has
        self.assertEqual(self.xmpp.custom_address, ('2001:41D0:1:A49b::1', 9222))

    def test_other_host_insecure_redirect(self):
        """Test that an insecure redirect is rejected as expected."""
        self.stream_start(mode='client', jid='tester@localhost')

        with unittest.mock.MagicMock() as on_error:
            self.xmpp.add_event_handler('stream_error', on_error)
            self.recv("""
                <stream:error>
                    <see-other-host xmlns='urn:ietf:params:xml:ns:xmpp-streams'>[2001:41D0:1:A49b::1]:9222</see-other-host>
                </stream:error>
            """)
            on_error.assert_called_once()
        # Ensure no connection parameters have been modified
        self.assertEqual(self.xmpp.default_domain, 'localhost')
        self.assertEqual(self.xmpp.custom_address, None)

    def test_max_redirects(self):
        """Test that we do not go over the max redirect limit"""
        self.stream_start(mode='client', jid='tester@localhost')

        # Mock an established TLS connection: redirects are allowed
        self.xmpp.transport.make_secure()
        # Limit redirects to 2
        self.xmpp.max_redirects = 2
        with unittest.mock.MagicMock() as on_error:
            self.xmpp.add_event_handler('stream_error', on_error)
            self.recv("""
                <stream:error>
                    <see-other-host xmlns='urn:ietf:params:xml:ns:xmpp-streams'>[2001:41D0:1:A49b::1]:9222</see-other-host>
                </stream:error>
            """)
            on_error.assert_called()
            self.recv("""
                <stream:error>
                    <see-other-host xmlns='urn:ietf:params:xml:ns:xmpp-streams'>example.org:8222</see-other-host>
                </stream:error>
            """)
            on_error.assert_called()
            self.recv("""
                <stream:error>
                    <see-other-host xmlns='urn:ietf:params:xml:ns:xmpp-streams'>jeproteste.info:7222</see-other-host>
                </stream:error>
            """)
            on_error.assert_called()
        # Ensure the domain has not changed
        self.assertEqual(self.xmpp.default_domain, 'localhost')
        # Ensure that we did not take the third redirect, as our max is 2
        self.assertEqual(self.xmpp.custom_address, ('example.org', 8222))


suite = unittest.TestLoader().loadTestsFromTestCase(TestStreamSeeOtherHost)
