"""Test the bounce detection modules."""

from email import message_from_string
from importlib import import_module

import pytest

from flufl.bounce._detectors.caiwireless import Caiwireless
from flufl.bounce._detectors.microsoft import Microsoft
from flufl.bounce._detectors.smtp32 import SMTP32
from flufl.bounce._scan import _DETECTORS, all_failures, scan_message
from flufl.bounce.interfaces import BounceDetector

from .utils import _parse


def test_smtp32_no_xmailer():
    # postfix_01.txt has no X-Mailer: header, so SMTP32 should bail out.
    msg = _parse('postfix_01.txt')
    assert msg['x-mailer'] is None
    temporary, permanent = SMTP32().process(msg)
    assert not temporary
    assert not permanent


_EMPTY_MULTIPART_REPORT = """\
Content-Type: multipart/report; boundary=BOUNDARY

--BOUNDARY

--BOUNDARY--

"""


def test_caiwireless_empty_report():
    # We lost the original samples for this one.
    msg = message_from_string(_EMPTY_MULTIPART_REPORT)
    temporary, permanent = Caiwireless().process(msg)
    assert not temporary
    assert not permanent


def test_microsoft_empty_report():
    # We lost the original samples for this one.
    msg = message_from_string(_EMPTY_MULTIPART_REPORT)
    temporary, permanent = Microsoft().process(msg)
    assert not temporary
    assert not permanent


def test_caiwireless_lp_917720():
    # https://bugs.launchpad.net/flufl.bounce/+bug/917720
    msg = _parse('simple_01.txt')
    assert scan_message(msg) == {b'bbbsss@example.com'}


def test_scan_llnl():
    msg = _parse('llnl_01.txt')
    assert scan_message(msg) == {b'user1@example.gov'}
    temporary, permanent = all_failures(msg)
    assert temporary == set()
    assert permanent == {b'user1@example.gov'}


def test_scan_unrecognized():
    msg = _parse('dumbass_01.txt')
    assert scan_message(msg) == set()
    temporary, permanent = all_failures(msg)
    assert temporary == set()
    assert permanent == set()


def test_scan_warning():
    msg = _parse('simple_03.txt')
    assert scan_message(msg) == set()
    temporary, permanent = all_failures(msg)
    assert temporary == {b'userx@example.za'}
    assert permanent == set()


# (detector_module, filename, expected_addresses, is_temporary)
DETECTORS = [
    # Postfix bounces
    ('postfix', 'postfix_01.txt', [b'xxxxx@local.ie'], False),
    ('postfix', 'postfix_02.txt', [b'yyyyy@digicool.com'], False),
    ('postfix', 'postfix_03.txt', [b'ttttt@ggggg.com'], False),
    ('postfix', 'postfix_04.txt', [b'userx@mail1.example.com'], False),
    ('postfix', 'postfix_05.txt', [b'userx@example.net'], False),
    # Exim bounces
    ('exim', 'exim_01.txt', [b'userx@its.example.nl'], False),
    # SimpleMatch bounces
    ('simplematch', 'sendmail_01.txt',
     [b'zzzzz@shaft.coal.nl', b'zzzzz@nfg.nl'], False),
    ('simplematch', 'simple_01.txt', [b'bbbsss@example.com'], False),
    ('simplematch', 'simple_02.txt', [b'userx@example.net'], False),
    ('simplematch', 'simple_04.txt', [b'userx@example.com'], False),
    ('simplematch', 'newmailru_01.txt', [b'zzzzz@newmail.ru'], False),
    ('simplematch', 'hotpop_01.txt', [b'userx@example.com'], False),
    ('simplematch', 'microsoft_03.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_05.txt', [b'userx@example.net'], False),
    ('simplematch', 'simple_06.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_07.txt', [b'userx@example.net'], False),
    ('simplematch', 'simple_08.txt', [b'userx@example.de'], False),
    ('simplematch', 'simple_09.txt', [b'userx@example.de'], False),
    ('simplematch', 'simple_10.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_11.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_12.txt', [b'userx@example.ac.jp'], False),
    ('simplematch', 'simple_13.txt', [b'userx@example.fr'], False),
    ('simplematch', 'simple_14.txt',
     [b'userx@example.com', b'usery@example.com'], False),
    ('simplematch', 'simple_15.txt', [b'userx@example.be'], False),
    ('simplematch', 'simple_16.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_17.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_18.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_19.txt', [b'userx@example.com.ar'], False),
    ('simplematch', 'simple_20.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_23.txt', [b'userx@example.it'], False),
    ('simplematch', 'simple_24.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_25.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_26.txt', [b'userx@example.it'], False),
    ('simplematch', 'simple_27.txt', [b'userx@example.net.py'], False),
    ('simplematch', 'simple_29.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_30.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_31.txt', [b'userx@example.fr'], False),
    ('simplematch', 'simple_32.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_33.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_34.txt', [b'roland@example.com'], False),
    ('simplematch', 'simple_36.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_37.txt', [b'user@example.edu'], False),
    ('simplematch', 'simple_38.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_39.txt', [b'userx@example.ru'], False),
    ('simplematch', 'simple_41.txt', [b'userx@example.com'], False),
    ('simplematch', 'simple_42.txt', [], False),
    ('simplematch', 'simple_43.txt', [], False),
    ('simplematch', 'simple_44.txt', [b'user@example.com'], False),
    ('simplematch', 'simple_45.txt', [b'subscriber@earthlink.net'], False),
    ('simplematch', 'bounce_02.txt', [b'userx@example.com'], False),
    ('simplematch', 'bounce_03.txt', [b'userx@example.uk'], False),
    ('simplematch', 'yahoo_12.txt', [b'user@yahoo.com'], False),
    # SimpleWarning
    ('simplewarning', 'simple_03.txt', [b'userx@example.za'], True),
    ('simplewarning', 'simple_21.txt', [b'userx@example.com'], True),
    ('simplewarning', 'simple_22.txt', [b'User@example.org'], True),
    ('simplewarning', 'simple_28.txt', [b'userx@example.com'], True),
    ('simplewarning', 'simple_35.txt', [b'calvin@example.com'], True),
    ('simplewarning', 'simple_40.txt', [b'user@example.com'], True),
    # GroupWise
    ('groupwise', 'groupwise_01.txt', [b'userx@example.EDU'], False),
    # Text/html groupwise -- just make sure it doesn't throw.
    ('groupwise', 'groupwise_02.txt', [], False),
    # Actually from Exchange, and Exchange recognizes it.
    ('exchange', 'groupwise_02.txt', [b'userx@example.com'], False),
    # Not a bounce but has confused groupwise.
    ('groupwise', 'groupwise_03.txt', [], False),
    # Yale's own
    ('yale', 'yale_01.txt', [b'userx@cs.yale.edu', b'userx@yale.edu'], False),
    # DSN, i.e. RFC 1894
    ('dsn', 'dsn_01.txt', [b'userx@example.com'], False),
    ('dsn', 'dsn_02.txt', [b'zzzzz@example.uk'], False),
    ('dsn', 'dsn_03.txt', [b'userx@example.be'], False),
    ('dsn', 'dsn_04.txt', [b'userx@example.ch'], False),
    ('dsn', 'dsn_05.txt', [b'userx@example.cz'], True),
    ('dsn', 'dsn_06.txt', [b'userx@example.com'], True),
    ('dsn', 'dsn_07.txt', [b'userx@example.nz'], True),
    ('dsn', 'dsn_08.txt', [b'userx@example.de'], True),
    ('dsn', 'dsn_09.txt', [b'userx@example.com'], False),
    ('dsn', 'dsn_10.txt', [b'anne.person@dom.ain'], False),
    ('dsn', 'dsn_11.txt', [b'joem@example.com'], False),
    ('dsn', 'dsn_12.txt', [b'userx@example.jp'], False),
    ('dsn', 'dsn_13.txt', [b'userx@example.com'], False),
    ('dsn', 'dsn_14.txt', [b'userx@example.com.dk'], False),
    ('dsn', 'dsn_15.txt', [b'userx@example.com'], False),
    ('dsn', 'dsn_16.txt', [b'userx@example.com'], False),
    ('dsn', 'dsn_17.txt', [b'userx@example.fi'], True),
    ('dsn', 'dsn_18.txt', [b'email@replaced.net'], False),
    # Microsoft Exchange
    ('exchange', 'microsoft_01.txt', [b'userx@example.COM'], False),
    ('exchange', 'microsoft_02.txt', [b'userx@example.COM'], False),
    # Microsoft's `SMTPSVC'?
    ('microsoft', 'microsoft_04.txt', [b'userx@example.COM'], False),
    # SMTP32
    ('smtp32', 'smtp32_01.txt', [b'userx@example.ph'], False),
    ('smtp32', 'smtp32_02.txt', [b'userx@example.com'], False),
    ('smtp32', 'smtp32_03.txt', [b'userx@example.com'], False),
    ('smtp32', 'smtp32_04.txt',
     [b'after_another@example.net', b'one_bad_address@example.net'], False),
    ('smtp32', 'smtp32_05.txt', [b'userx@example.com'], False),
    ('smtp32', 'smtp32_06.txt', [b'Absolute_garbage_addr@example.net'], False),
    ('smtp32', 'smtp32_07.txt', [b'userx@example.com'], False),
    # Qmail
    ('qmail', 'qmail_01.txt', [b'userx@example.de'], False),
    ('qmail', 'qmail_02.txt', [b'userx@example.com'], False),
    ('qmail', 'qmail_03.txt', [b'userx@example.jp'], False),
    ('qmail', 'qmail_04.txt', [b'userx@example.au'], False),
    ('qmail', 'qmail_05.txt', [b'userx@example.com'], False),
    ('qmail', 'qmail_06.txt', [b'ntl@xxx.com'], False),
    ('qmail', 'qmail_07.txt', [b'user@example.net'], False),
    ('qmail', 'qmail_08.txt', [], False),
    # LLNL's custom Sendmail
    ('llnl', 'llnl_01.txt', [b'user1@example.gov'], False),
    # Netscape's server
    ('netscape', 'netscape_01.txt',
     [b'aaaaa@corel.com', b'bbbbb@corel.com'], False),
    # Yahoo's proprietary format
    ('yahoo', 'yahoo_01.txt', [b'userx@example.com'], False),
    ('yahoo', 'yahoo_02.txt', [b'userx@example.es'], False),
    ('yahoo', 'yahoo_03.txt', [b'userx@example.com'], False),
    ('yahoo', 'yahoo_04.txt',
     [b'userx@example.es', b'usery@example.uk'], False),
    ('yahoo', 'yahoo_05.txt',
     [b'userx@example.com', b'usery@example.com'], False),
    ('yahoo', 'yahoo_06.txt',
     [b'userx@example.com', b'usery@example.com',
      b'userz@example.com', b'usera@example.com'], False),
    ('yahoo', 'yahoo_07.txt',
     [b'userw@example.com', b'userx@example.com',
      b'usery@example.com', b'userz@example.com'], False),
    ('yahoo', 'yahoo_08.txt',
     [b'usera@example.com', b'userb@example.com',
      b'userc@example.com', b'userd@example.com',
      b'usere@example.com', b'userf@example.com'], False),
    ('yahoo', 'yahoo_09.txt',
     [b'userx@example.com', b'usery@example.com'], False),
    ('yahoo', 'yahoo_10.txt',
     [b'userx@example.com', b'usery@example.com',
      b'userz@example.com'], False),
    ('yahoo', 'yahoo_11.txt', [b'bad_user@aol.com'], False),
    ('yahoo', 'yahoo_13.txt', [b'bogus-address@example.net'], False),
    # sina.com appears to use their own weird SINAEMAIL MTA
    ('sina', 'sina_01.txt',
     [b'userx@sina.com', b'usery@sina.com'], False),
    ('aol', 'aol_01.txt', [b'screenname@aol.com'], False),
    # Caiwireless's pseudo-MIME format
    ('caiwireless', 'caiwireless_01.txt', [b'userx@example.com'], False),
    # No addresses are detectable in dumbass_01.txt - we love Microsoft.
]


@pytest.mark.parametrize(
    ('detector_module', 'filename', 'expected', 'is_temporary'),
    DETECTORS,
    ids=[f'{m}-{f}-{"T" if t else "P"}' for m, f, _, t in DETECTORS],
)
def test_detector(detector_module, filename, expected, is_temporary):
    module = import_module(f'flufl.bounce._detectors.{detector_module}')
    [component_name] = module.__all__
    component = getattr(module, component_name)()
    msg = _parse(filename)
    temporary, permanent = component.process(msg)
    got = set(temporary) if is_temporary else set(permanent)
    assert got == set(expected)


@pytest.mark.parametrize(
    'detector_class',
    _DETECTORS,
    ids=[cls.__name__ for cls in _DETECTORS],
)
def test_detector_conforms_to_protocol(detector_class):
    # Every registered detector must structurally satisfy the BounceDetector
    # protocol.  This replaces the guarantee that zope.interface's
    # @implementer decorator used to provide.
    assert isinstance(detector_class(), BounceDetector)
