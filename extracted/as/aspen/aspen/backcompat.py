from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import codecs


# Before Python 3.5 the 'backslashreplace' error handler only worked when
# encoding, not when decoding. We want the 3.5+ behavior, and we want it in the
# global codecs registry as soon as possible.

def backslashreplace_errors(unicode_error):
    offender = unicode_error.object[unicode_error.start:unicode_error.end]
    if isinstance(offender, bytes):
        r = ''.join(r'\x{0:x}'.format(b if isinstance(b, int) else ord(b))
                    for b in offender)
    else:
        r = offender.encode('ascii', 'old-backslashreplace').decode('ascii')
    return (r, unicode_error.end)

def upgrade_backslashreplace():
    if codecs.lookup_error('backslashreplace') is not codecs.backslashreplace_errors:
        return  # don't upgrade if someone else already has
    codecs.register_error('old-backslashreplace', codecs.backslashreplace_errors)
    codecs.register_error('backslashreplace', backslashreplace_errors)
