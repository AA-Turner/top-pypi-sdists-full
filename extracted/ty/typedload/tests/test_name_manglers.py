# typedload
# Copyright (C) 2026 Auri
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Auri <me@aurieh.me>

import unittest

from typedload import name_manglers


class TestManglers(unittest.TestCase):

    def test_snake_case_to_camel_case(self):
        inflect = name_manglers.snake_case_to_camel_case
        assert inflect('') == ''
        assert inflect('foo') == 'foo'
        assert inflect('foo_bar') == 'fooBar'
        assert inflect('foo_bar_baz') == 'fooBarBaz'

    def test_snake_case_to_pascal_case(self):
        inflect = name_manglers.snake_case_to_pascal_case
        assert inflect('') == ''
        assert inflect('foo') == 'Foo'
        assert inflect('foo_bar') == 'FooBar'
        assert inflect('foo_bar_baz') == 'FooBarBaz'

    def test_snake_case_to_kebab_case(self):
        inflect = name_manglers.snake_case_to_kebab_case
        assert inflect('') == ''
        assert inflect('foo') == 'foo'
        assert inflect('foo_bar') == 'foo-bar'
        assert inflect('foo_bar_baz') == 'foo-bar-baz'
