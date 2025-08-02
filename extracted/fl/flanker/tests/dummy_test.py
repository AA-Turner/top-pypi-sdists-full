# coding=utf-8
import json
from os.path import join, abspath, dirname

from nose.tools import ok_, eq_

from flanker.addresslib.address import parse
from flanker.mime.create import from_string


def test_some():
    absolute_path = join(abspath(dirname(__file__)), 'yunuf7.txt')
    with open(absolute_path, 'r') as f:
        raw_mime = f.read()

    msg = from_string(raw_mime)
    vars = json.loads(msg.parts[0].body)
    email = vars[u'yunuf7@şljhy.com']['email']
    eq_(u'yunuf7@şljhy.com', parse(email).address)
