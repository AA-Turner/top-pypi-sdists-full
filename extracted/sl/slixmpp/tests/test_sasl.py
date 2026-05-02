import unittest

# Importing mechanisms registers all SCRAM variants in the global MECHANISMS
# and MECH_SEC_SCORES dicts used by choose().
from slixmpp.util.sasl import mechanisms  # noqa: F401 (side-effect import)
from slixmpp.util.sasl.client import choose, SASLCancelled
from slixmpp.util.sasl.mechanisms import SCRAM


def _credentials(channel_binding=None):
    """Return a credentials callback that yields fixed test values."""
    def callback(required, optional):
        result = {}
        for val in required | optional:
            if val == 'username':
                result[val] = 'testuser'
            elif val == 'password':
                result[val] = 'testpass'
            elif val == 'channel_binding':
                result[val] = channel_binding
            else:
                result[val] = b''
        return result
    return callback


def _security(encrypted=True, binding_proposed=True, tls_version='TLSv1.3'):
    """Return a security-settings callback."""
    def callback(values):
        result = {}
        for val in values:
            if val == 'encrypted':
                result[val] = encrypted
            elif val == 'binding_proposed':
                result[val] = binding_proposed
            elif val == 'tls_version':
                result[val] = tls_version
            else:
                result[val] = False
        return result
    return callback


def _build_scram(name, channel_binding=None, tls_version='TLSv1.3'):
    """Instantiate a SCRAM mechanism directly, bypassing choose()."""
    creds = _credentials(channel_binding)(
        SCRAM.required_credentials, SCRAM.optional_credentials)
    sec = _security(tls_version=tls_version)(SCRAM.security)
    return SCRAM(name, creds, sec)


class TestSCRAMChannelBindingFallback(unittest.TestCase):
    """SCRAM-PLUS channel binding fallback behaviour.

    On TLS 1.3, Python ssl only supports tls-unique (forbidden on TLS 1.3 per
    RFC 9266) and does not implement tls-exporter at all
    (https://github.com/python/cpython/issues/95341).

    On TLS < 1.3, tls-unique is available and SCRAM-PLUS should succeed.  An
    unexpected None binding must NOT trigger a silent fallback that could
    mask a downgrade attack or other security issue."""

    def test_scram_plus_cancelled_on_tls13_when_binding_unavailable(self):
        """SCRAM-SHA-1-PLUS raises SASLCancelled on TLS 1.3 with no binding."""
        with self.assertRaises(SASLCancelled):
            _build_scram('SCRAM-SHA-1-PLUS', channel_binding=None,
                         tls_version='TLSv1.3')

    def test_choose_falls_back_to_non_plus_on_tls13(self):
        """choose() selects SCRAM-SHA-1 when binding is unavailable on TLS 1.3."""
        mech = choose(
            {'SCRAM-SHA-1-PLUS', 'SCRAM-SHA-1', 'PLAIN'},
            _credentials(channel_binding=None),
            _security(binding_proposed=True, tls_version='TLSv1.3'),
        )
        self.assertEqual(mech.name, 'SCRAM-SHA-1')

    def test_scram_plus_cancelled_when_no_tls(self):
        """SCRAM-SHA-1-PLUS raises SASLCancelled when there is no TLS at all."""
        with self.assertRaises(SASLCancelled):
            _build_scram('SCRAM-SHA-1-PLUS', channel_binding=None,
                         tls_version=None)

    def test_scram_plus_not_cancelled_on_tls12_with_missing_binding(self):
        """On TLS 1.2, missing binding does NOT trigger SASLCancelled.

        tls-unique is available on TLS 1.2; an absent channel_binding is
        unexpected and should not silently downgrade the mechanism.
        """
        # Should not raise — setup() returns normally
        mech = _build_scram('SCRAM-SHA-1-PLUS', channel_binding=None,
                             tls_version='TLSv1.2')
        self.assertTrue(mech.use_channel_binding)

    def test_choose_does_not_fall_back_on_tls12_with_missing_binding(self):
        """choose() keeps SCRAM-SHA-1-PLUS on TLS 1.2 even with None binding."""
        mech = choose(
            {'SCRAM-SHA-1-PLUS', 'SCRAM-SHA-1', 'PLAIN'},
            _credentials(channel_binding=None),
            _security(binding_proposed=True, tls_version='TLSv1.2'),
        )
        self.assertEqual(mech.name, 'SCRAM-SHA-1-PLUS')

    def test_scram_plus_accepted_when_binding_available(self):
        """SCRAM-SHA-1-PLUS initialises normally when binding data is present."""
        mech = _build_scram('SCRAM-SHA-1-PLUS', channel_binding=b'fake-binding')
        self.assertTrue(mech.use_channel_binding)

    def test_choose_selects_plus_when_binding_available(self):
        """choose() prefers SCRAM-SHA-1-PLUS when channel binding data is present."""
        mech = choose(
            {'SCRAM-SHA-1-PLUS', 'SCRAM-SHA-1', 'PLAIN'},
            _credentials(channel_binding=b'fake-binding'),
            _security(binding_proposed=True, tls_version='TLSv1.2'),
        )
        self.assertEqual(mech.name, 'SCRAM-SHA-1-PLUS')

    def test_non_plus_unaffected_by_fix(self):
        """SCRAM-SHA-1 (non-PLUS) is never cancelled regardless of binding data."""
        mech = _build_scram('SCRAM-SHA-1', channel_binding=None)
        self.assertFalse(mech.use_channel_binding)

    def test_setup_initialises_step_and_mutual_auth(self):
        """setup() must always initialise self.step and self._mutual_auth.

        Cover both the TLS < 1.3 early-return path and the normal
        completion paths to ensure those attributes are always present.
        """
        # Normal completion: PLUS with binding data present
        mech = _build_scram('SCRAM-SHA-1-PLUS', channel_binding=b'fake-binding')
        self.assertEqual(mech.step, 0)
        self.assertFalse(mech._mutual_auth)

        # Normal completion: non-PLUS (no binding used)
        mech = _build_scram('SCRAM-SHA-1', channel_binding=None)
        self.assertEqual(mech.step, 0)
        self.assertFalse(mech._mutual_auth)

        # Early-return path: TLS 1.2, binding expected but unavailable.
        # setup() currently returns before the assignments; step and
        # _mutual_auth must still be initialised for process() to work.
        mech = _build_scram('SCRAM-SHA-1-PLUS', channel_binding=None,
                             tls_version='TLSv1.2')
        self.assertEqual(mech.step, 0)
        self.assertFalse(mech._mutual_auth)


suite = unittest.TestLoader().loadTestsFromTestCase(
    TestSCRAMChannelBindingFallback)
