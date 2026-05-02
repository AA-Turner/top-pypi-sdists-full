# Copyright (C) 2016  Pachol, Vojtěch <pacholick@gmail.com>
#
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import functools
import re

from brackettree import clscomp


def cachedproperty(f):
    r"""
    >>> class DeepThought:
    ...     @cachedproperty
    ...     def answer_to_life_the_universe_and_everything(self):
    ...         print("7.5M years calculating")
    ...         return 42
    >>> dt = DeepThought()
    >>> dt.answer_to_life_the_universe_and_everything
    7.5M years calculating
    42
    >>> dt.answer_to_life_the_universe_and_everything
    42
    """
    @functools.wraps(f)
    def wrapped(self):
        if not hasattr(f, '__value'):
            f.__value = f(self)
        return f.__value
    return property(wrapped)


class Node(metaclass=clscomp.PatternType):
    r"""
    >>> n = Node(''' aaa : (bbb: "cc\\"c", ddd: ["ee)e", "fff"])ggg''')
    >>> n.printtree()
    Node
    ├── ' aaa : '
    ├── RoundNode
    │   ├── 'bbb: '
    │   ├── DoubleQNode
    │   │   └── 'cc\\"c'
    │   ├── ', ddd: '
    │   └── SquareNode
    │       ├── DoubleQNode
    │       │   └── 'ee)e'
    │       ├── ', '
    │       └── DoubleQNode
    │           └── 'fff'
    └── 'ggg'
    """

    @classmethod
    def _subcollect(cls, arg):
        dct = {}
        for subcls in cls.__subclasses__():
            try:
                dct[getattr(subcls, arg)] = subcls
            except AttributeError:
                pass
            dct.update(subcls._subcollect(arg))
        return dct

    @cachedproperty
    def lefts(self):
        return self._subcollect("left")

    @cachedproperty
    def rights(self):
        return self._subcollect("right")

    @cachedproperty
    def pattern(self):
        return re.compile(r'(?<!\\)([{}{}])'.format(
            re.escape(''.join(self.lefts)),
            re.escape(''.join(self.rights))))

    def __init__(self, text=None, parent=None, prev=None):
        self.items = []
        self.parent = parent
        self.prev = prev

        if text is not None:
            def it(s):
                *headsep, tail = re.split(self.pattern, s, maxsplit=1)
                if headsep:
                    yield headsep
                    yield from it(tail)
                else:
                    yield tail, None
            self.__class__.it = it(text)

        self.trueinit()

    def trueinit(self):
        prev = None
        for head, sep in self.it:
            newtext = newnode = None
            if head:
                # self.items.append(TextNode(head))
                newtext = TextNode(head, parent=self, prev=prev)
                self.items.append(newtext)
                prev = newtext
            if sep in self.lefts:
                # self.items.append(self.lefts[sep]())
                newnode = self.lefts[sep](parent=self, prev=prev)
                self.items.append(newnode)
                prev = newnode
            elif hasattr(self, 'right') and sep == self.right:
                return  # return doesn't ultimately end the loop as break would

            if newtext:
                newtext.next = newnode

    def __str__(self):
        return self.__class__.__name__
    __repr__ = __str__

    def __len__(self):
        return len(self.items)

    def printtree(self, last=True, before=[]):
        print((''.join(before) + (last and "└── " or "├── "))[4:] + repr(self))
        if not self.items:
            return
        before.append(last and "    " or "│   ")

        *lead, last = self.items
        for i in lead:
            i.printtree(last=False)
        last.printtree(last=True)
        before.pop()

    def match(self, pattern):
        pattern = clscomp.Pattern(pattern)

        if pattern.regex and isinstance(self, str) and \
           re.match(pattern.regex, str(self), re.DOTALL):
            return True
        if pattern.type_ and isinstance(self, pattern.type_):
            return True

        return False

    def findall(self, pattern):
        r"""
        >>> n = Node(''' aaa : (bbb: "cc\\"c", ddd: ["ee)e", "fff"])ggg''')
        >>> list( n.findall(QuoteNode > ".*") )
        ['cc\\"c', 'ee)e', 'fff']
        >>> list( n.findall(SquareNode > QuoteNode > ".*") )
        ['ee)e', 'fff']
        """
        pattern = clscomp.Pattern(pattern)
        # print(pattern.preceded_by.regex)
        # precedings = parents = ancestors = ()

        for i in self.items:
            yield from i.findall(pattern)

        if pattern.preceded_by:
            if not self.prev or not self.prev.match(pattern.preceded_by):
                return
        if pattern.child_of:
            if not self.parent or not self.parent.match(pattern.child_of):
                return
        if pattern.descendand_of:
            # TODO
            if not self.parent:
                return
            parent = self.parent
            while parent:
                parent = parent.parent

        if self.match(pattern):
            yield self

    def find(self, pattern):
        try:
            return next(self.findall(pattern))
        except StopIteration:
            return None


class BracketNode(Node):
    pass


class QuoteNode(Node):
    def trueinit(self):
        for head, sep in self.it:
            self.items.append(head)
            if sep == self.right:
                break
            self.items.append(sep)

        # with open("/tmp/brackets.log", 'a') as f:
        #     f.write(str(self.items))
        #     f.write('\n')
        self.items = [TextNode(''.join(self.items), parent=self)]


class TextNode(str, Node):
    def __new__(cls, value, parent=None, prev=None):
        obj = super(TextNode, cls).__new__(cls, value)
        obj.parent = parent
        obj.prev = prev
        obj.items = ()
        return obj

    def __init__(self, text, parent=None, prev=None):
        self.items = ()
        self.parent = parent
        self.prev = prev


class RoundNode(BracketNode):
    left = '('
    right = ')'


class CurlyNode(BracketNode):
    left = '{'
    right = '}'


class SquareNode(BracketNode):
    left = '['
    right = ']'


# class AngleNode(BracketNode):
#     left = '<'
#     right = '>'


class SingleQNode(QuoteNode):
    left = "'"
    right = "'"


class DoubleQNode(QuoteNode):
    left = '"'
    right = '"'


if __name__ == "__main__":
    import doctest
    doctest.testmod()
