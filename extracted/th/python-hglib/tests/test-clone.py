import os
from tests import common
import hglib
from hglib.util import b

class test_clone(common.basetest):
    def test_basic(self):
        self.append('a', 'a')
        self.client.commit(b('first'), addremove=True)
        cloned = hglib.clone(b('.'), b('cloned'))
        self.assertRaises(ValueError, cloned.log)
        cloned.open()
        self.assertEquals(self.client.log(), cloned.log())

    def test_clone_uncompressed(self):
        hglib.clone(b('.'), b('cloned'), uncompressed=True)
