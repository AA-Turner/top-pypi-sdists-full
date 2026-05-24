"""
typedload

Name manglers for inflecting identifier names
"""

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

__all__ = [
    'snake_case_to_camel_case',
    'snake_case_to_pascal_case',
    'snake_case_to_kebab_case',
]

def snake_case_to_camel_case(name: str) -> str:
    """
    Given a snake_case name, return inflected camelCase name.
    """
    head, *rest = name.split('_')
    return head + ''.join(part.capitalize() for part in rest)

def snake_case_to_pascal_case(name: str) -> str:
    """
    Given a snake_case name, return inflected PascalCase name.
    """
    return ''.join(part.capitalize() for part in name.split('_'))

def snake_case_to_kebab_case(name: str) -> str:
    """
    Given a snake_case name, return inflected kebab-case name.
    """
    return name.replace('_', '-')
