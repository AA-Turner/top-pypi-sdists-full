"""Test the bounce detection modules."""

import unittest

from contextlib import closing
from email import message_from_binary_file as parse, message_from_string
from flufl.bounce._detectors.caiwireless import Caiwireless
from flufl.bounce._detectors.microsoft import Microsoft
from flufl.bounce._detectors.smtp32 import SMTP32
from flufl.bounce._scan import all_failures, scan_message
from pkg_resources import resource_stream


COMMASPACE = b', '


class TestOtherBounces(unittest.TestCase):
    def test_SMTP32_failure(self):
        # This file has no X-Mailer: header
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'postfix_01.txt')) as fp:
            msg = parse(fp)
        self.failIf(msg['x-mailer'] is not None)
        temporary, permanent = SMTP32().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)

    def test_caiwireless(self):
        # BAW: this is a mostly bogus test; I lost the samples. :(
        msg = message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        temporary, permanent = Caiwireless().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)

    def test_microsoft(self):
        # BAW: similarly as above, I lost the samples. :(
        msg = message_from_string("""\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

""")
        temporary, permanent = Microsoft().process(msg)
        self.failIf(temporary)
        self.failIf(permanent)

    def test_caiwireless_lp_917720(self):
        # https://bugs.launchpad.net/flufl.bounce/+bug/917720
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'simple_01.txt')) as fp:
            msg = parse(fp)
        self.assertEqual(scan_message(msg), set([b'bbbsss@example.com']))


class TestScanAllDetectors(unittest.TestCase):
    # Ensure that _scan runs detectors.
    def test_llnl(self):
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'llnl_01.txt')) as fp:
            msg = parse(fp)
        self.assertEqual(scan_message(msg), set([b'user1@example.gov']))
        temporary, permanent = all_failures(msg)
        self.assertEqual(temporary, set())
        self.assertEqual(permanent, set([b'user1@example.gov']))

    def test_unrecognized(self):
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'dumbass_01.txt')) as fp:
            msg = parse(fp)
        self.assertEqual(scan_message(msg), set())
        temporary, permanent = all_failures(msg)
        self.assertEqual(temporary, set())
        self.assertEqual(permanent, set())

    def test_warning(self):
        with closing(resource_stream('flufl.bounce.tests.data',
                                     'simple_03.txt')) as fp:
            msg = parse(fp)
        self.assertEqual(scan_message(msg), set())
        temporary, permanent = all_failures(msg)
        self.assertEqual(temporary, set([b'userx@example.za']))
        self.assertEqual(permanent, set())


class TestDetectors(unittest.TestCase):
    # This is a pure placeholder for the nose2 plugin in
    # flufl.bounce.testing.helpers.Detectors.
    pass
