# coding: utf-8

from django.utils.timezone import now as tznow
from django.test import TestCase

from nano.tools.models import *
from nano.tools import *
from nano.tools.tests.models import TreeItem


class TreeMixinTest(TestCase):

    def setUp(self):
        self.root1 = TreeItem()
        self.root1.save() 
        self.child1 = TreeItem(part_of=self.root1)
        self.child1.save()
        self.child2 = TreeItem(part_of=self.root1)
        self.child2.save()
        self.grandchild1 = TreeItem(part_of=self.child2)
        self.grandchild1.save()

    def test_roots(self):
        items = set(self.child1.roots())
        self.assertEqual(items, set((self.root1,)))

    def test_get_path(self):
        items = self.child1.get_path()
        self.assertEqual(items, [self.root1,self.child1])

    def test_descendants(self):
        items = set(self.root1.descendants())
        self.assertEqual(items, set([self.child1, self.child2, self.grandchild1]))
        items = list(self.child1.descendants())
        self.assertEqual(items, [])

    def test_children(self):
        items = set(self.root1.children())
        self.assertEqual(items, set([self.child1, self.child2]))
        items = list(self.child1.children())
        self.assertEqual(items, [])

    def test_parent(self):
        items = self.root1.parent()
        self.assertEqual(items, None)
        items = self.child1.parent()
        self.assertEqual(items, self.root1)

    def test_siblings(self):
        items = list(self.root1.siblings())
        self.assertEqual(items, [])
        items = set(self.child1.siblings())
        self.assertEqual(items, set([self.child1, self.child2]))

    def test_is_sibling_of(self):
        items = self.root1.is_sibling_of(self.child1)
        self.assertFalse(items)
        items = self.child1.is_sibling_of(self.child2)
        self.assertTrue(items)

    def test_is_child_of(self):
        items = self.root1.is_child_of(self.child1)
        self.assertFalse(items)
        items = self.child1.is_child_of(self.root1)
        self.assertTrue(items)

    def test_is_root(self):
        items = self.root1.is_root()
        self.assertTrue(items)
        items = self.child1.is_root()
        self.assertFalse(items)

    def test_is_leaf(self):
        items = self.root1.is_leaf()
        self.assertFalse(items)
        items = self.child1.is_leaf()
        self.assertTrue(items)

class TextTest(TestCase):
    pass

class FunctionTest(TestCase):

    def test_nullfunction(self):
        result = nullfunction(1, 2, three=3)
        self.assertEqual(result, 1)
        result = nullfunction(1, 2)
        self.assertEqual(result, 1)
        result = nullfunction(1, three=3)
        self.assertEqual(result, 1)
        result = nullfunction(1)
        self.assertEqual(result, 1)

    def test_pop_error(self):

        class Foo(object):

            session = {'error': 'baa'}

        request = Foo()
        result = pop_error(request)
        self.assertEqual(result, 'baa')
        self.assertFalse('error' in request.session)

        request.session = {}
        result = pop_error(request)
        self.assertEqual(result, None)

    def test_asciify(self):
        self.assertEqual('', asciify(''))
        self.assertEqual('abcABC123', asciify('abcABC123'))
        self.assertEqual('blabrsyltety', asciify('blåbærsyltetøy'))

    def test_grouper_nothing_to_group(self):
        self.assertEqual([], list(grouper(0, '')))
        self.assertEqual([], list(grouper(0, 'abc')))
        self.assertEqual([], list(grouper(1, '')))
        self.assertEqual([], list(grouper(2, '')))

    def test_grouper(self):
        self.assertEqual(
            [('a',), ('b',), ('c',)],
            list(grouper(1, 'abc'))
        )
        self.assertEqual(
            [('a', u'b'), ('c', None)],
            list(grouper(2, 'abc'))
        )
        self.assertEqual(
            [(u'a', u'b', u'c')],
            list(grouper(3, 'abc'))
        )
        self.assertEqual(
            [(u'a', u'b', u'c', None)],
            list(grouper(4, 'abc'))
        )

    def test_grouper_fillvalue(self):
        self.assertEqual(
            [('a',), ('b',), ('c',)],
            list(grouper(1, 'abc', fillvalue='X'))
        )
        self.assertEqual(
            [('a', 'b'), ('c', 'X')],
            list(grouper(2, 'abc', fillvalue='X'))
        )
        self.assertEqual(
            [('a', 'b', 'c')],
            list(grouper(3, 'abc', fillvalue='X'))
        )
        self.assertEqual(
            [('a', 'b', 'c', 'X')],
            list(grouper(4, 'abc', fillvalue='X'))
        )
