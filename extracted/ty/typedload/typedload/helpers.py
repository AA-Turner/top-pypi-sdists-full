"""
typedload

Internal helper functions
"""

# Copyright (C) 2021-2024 Salvo "LtWorf" Tomaselli
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
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

__all__ = [
    'tname',
    'mangle_name',
]


def tname(type_) -> str:
    '''
    Return a nice string for a type
    '''
    return getattr(type_, '__qualname__', str(type_))

def mangle_name(loader_or_dumper, field) -> str | None:
    '''
    Return the mangled name of a field according to the loader/dumper
    configuration, or None if the name is to be used as-is
    '''
    return (
        field.metadata.get(loader_or_dumper.mangle_key)
        or (
            loader_or_dumper.mangler(field.name)
            if loader_or_dumper.mangler
            else None
        )
    )
