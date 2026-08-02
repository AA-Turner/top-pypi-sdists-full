import sys
from tests import common
from hglib.error import CommandError
import hglib
from hglib import context
from hglib.util import b

class test_context(common.basetest):
    def test_non_existent(self):
        self.assertRaises(ValueError, context.changectx, self.client, b('foo'))

    def test_basic(self):
        self.append('a', 'a')
        self.append('b', 'b')
        rev0, node0 = self.client.commit(b('first'), addremove=True)

        self.append('c', 'c')
        rev1, node1 = self.client.commit(b('second'), addremove=True)

        self.assertRaises(KeyError, self.client.__getitem__, 'doesnotexist')

        ctx = self.client[node0]

        self.assertEquals(ctx.description(), b('first'))
        self.assertEquals(str(ctx), node0[:12].decode('latin-1'))
        self.assertEquals(ctx.node(), node0)
        self.assertEquals(int(ctx), rev0)
        self.assertEquals(ctx.rev(), rev0)
        self.assertEquals(ctx.branch(), b('default'))

        self.assertTrue(ctx)

        self.assertTrue(b('a') in ctx and b('b') in ctx)
        self.assertFalse(b('c') in ctx)
        self.assertEquals(list(ctx), [b('a'), b('b')])
        self.assertEquals(ctx.files(), [b('a'), b('b')])

        self.assertEquals(ctx.modified(), [])
        self.assertEquals(ctx.added(), [b('a'), b('b')])
        self.assertEquals(ctx.removed(), [])
        self.assertEquals(ctx.ignored(), [])
        self.assertEquals(ctx.clean(), [])

        man = {b('a') : b('047b75c6d7a3ef6a2243bd0e99f94f6ea6683597'),
               b('b') : b('62452855512f5b81522aa3895892760bb8da9f3f')}
        self.assertEquals(ctx.manifest(), man)

        self.assertEquals([int(c) for c in ctx.parents()], [-1])
        self.assertEquals(int(ctx.p1()), -1)
        self.assertEquals(int(ctx.p2()), -1)

        self.assertEquals([int(c) for c in ctx.children()], [1])
        self.assertEquals([int(c) for c in ctx.descendants()], [0, 1])
        self.assertEquals([int(c) for c in ctx.ancestors()], [0])

        self.client.bookmark(b('bookmark'), inactive=True, rev=node0)
        self.assertEquals(ctx.bookmarks(), [b('bookmark')])

        self.client.tag(b('tag'), rev=node0)
        # tags are read on construction
        self.assertEquals(self.client[node0].tags(), [b('tag')])

    def test_construction(self):
        self.append('a', 'a')
        rev0, node0 = self.client.commit(b('first'), addremove=True)
        tip = self.client.tip()

        # from client.revision
        ctx = context.changectx(self.client, tip)
        self.assertEquals(ctx.node(), tip.node)

        # from revset
        ctx = context.changectx(self.client, b('all()'))
        self.assertEquals(ctx.node(), tip.node)

    def test_in_keyword(self):
        """
        test the 'in' keyword using both revision numbers or changeset ids.
        """
        if sys.version_info < (2, 7):
            return

        self.append('a', 'a')
        rev0, node0 = self.client.commit(b('first'), addremove=True)
        self.append('a', 'a')
        rev1, node1 = self.client.commit(b('second'))

        self.assertIn(1, self.client)
        hash_1 = self.client.log(0)[0][1]
        self.assertIn(hash_1, self.client)
        self.assertNotIn(2, self.client)
        hash_2 = self.client.log(1)[0][1]
        self.assertIn(hash_2, self.client)
        hash_2 = b('deadbeef')
        self.assertNotIn(hash_2, self.client)
