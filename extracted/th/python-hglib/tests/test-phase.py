from tests import common
import hglib
from hglib.util import b

class test_phase(common.basetest):
    """test the different ways to use the phase command"""
    def test_phase(self):
        """test getting data from a single changeset"""
        self.append('a', 'a')
        rev, node0 = self.client.commit(b('first'), addremove=True)
        self.assertEqual([(0, b('draft'))], self.client.phase(node0))
        ctx = self.client[rev]
        self.assertEqual(b('draft'), ctx.phase())

    def test_phase_public(self):
        """test phase change from draft to public"""
        self.append('a', 'a')
        rev, node0 = self.client.commit(b('first'), addremove=True)
        self.client.phase(node0, public=True)
        self.assertEqual([(0, b('public'))], self.client.phase(node0))
        ctx = self.client[rev]
        self.assertEqual(b('public'), ctx.phase())

    def test_phase_secret(self):
        """test phase change from draft to secret"""
        self.append('a', 'a')
        rev, node0 = self.client.commit(b('first'), addremove=True)
        self.assertRaises(hglib.error.CommandError,
                          self.client.phase, node0, secret=True)
        self.client.phase(node0, secret=True, force=True)
        self.assertEqual([(0, b('secret'))], self.client.phase(node0))
        ctx = self.client[rev]
        self.assertEqual(b('secret'), ctx.phase())


    def test_phase_multiple(self):
        """test phase changes and show the phases of the different changesets"""
        self.append('a', 'a')
        rev, node0 = self.client.commit(b('a'), addremove=True)
        self.client.phase(node0, public=True)
        self.append('b', 'b')
        rev, node1 = self.client.commit(b('b'), addremove=True)
        self.append('c', 'c')
        rev, node2 = self.client.commit(b('c'), addremove=True)
        self.client.phase(node2, secret=True, force=True)
        self.assertEqual([(0, b('public')), (2, b('secret')), (1, b('draft'))],
                         self.client.phase([node0, node2, node1]))
