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


class Pattern:
    # def __new__(cls, pattern=None, **kwargs):
    #     """
    #     >>> a = Pattern()
    #     >>> b = Pattern(a)
    #     >>> a is b
    #     True
    #     """
    #     # print(f'__new__: pattern={pattern}')
    #     if pattern.__class__ is cls:
    #         return pattern
    #     return super(Pattern, cls).__new__(cls)

    regex = type_ = preceded_by = child_of = descendand_of = None

    def __init__(self, pattern):
        """
        >>> from nodes import *
        >>> pattern = RoundNode > ".*bbb.*" + DoubleQNode
        >>> pattern.type_
        <class 'nodes.DoubleQNode'>
        >>> pattern.preceded_by.regex
        '.*bbb.*'
        >>> pattern.child_of.type_
        <class 'nodes.RoundNode'>
        """
        # if pattern.__class__ is Pattern:
        #     pass
        if isinstance(pattern, str):
            self.regex = pattern
            self.type_ = None
        else:
            self.regex = None
            print('setting type_')
            self.type_ = pattern

        # if preceded_by:
        #     self.preceded_by = preceded_by
        # if child_of:
        #     self.child_of = child_of
        # if descendand_of:
        #     self.descendand_of = descendand_of

    # def __str__(self):
    #     return str(self.regex or self.type_ or self.__class__.__name__)

    # def __repr__(self):
    #     return repr(self.regex or self.type_ or self.__class__.__name__)

    def __add__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        other.preceded_by = self
        return other

    def __radd__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        self.preceded_by = other
        return self

    def __gt__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        other.child_of = self
        return other

    def __lt__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        self.child_of = other
        return self

    def __lshift__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        other.descendand_of = self
        return other

    def __rshift__(self, other):
        if not isinstance(other, Pattern):
            other = Pattern(other)
        self.descendand_of = other
        return self


class PatternType(type, Pattern):
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()
