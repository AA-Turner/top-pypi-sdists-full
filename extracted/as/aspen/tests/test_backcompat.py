from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pytest import raises


GARBAGE = b"a\xef\xf9"


# I had thought to wrap codec error handler registration in a context manager
# so we could clean up the global registry state post-test, but:

# > There is no API to unregister a codec search function, since deregistration
# > would break the codec cache used by the registry to speedup codec
# > lookup.
#
# > Why would you want to unregister a codec search function ?
#
# https://mail.python.org/pipermail/python-dev/2011-September/113590.html

# O.o


def test_garbage_is_garbage():
    raises(UnicodeDecodeError, lambda s: s.decode('utf8'), GARBAGE)

def test_backslashreplace_error_strategy_works_when_decoding():
    actual = GARBAGE.decode('utf8', 'backslashreplace')
    assert actual == r"a\xef\xf9"

def test_backslashreplace_error_strategy_works_when_encoding():
    actual = 'comet: \u2604'.encode('ascii', 'backslashreplace')
    assert actual == br"comet: \u2604"
