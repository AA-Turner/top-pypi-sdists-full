# Copyright (C) 2007-2023 by the Free Software Foundation, Inc.
#
# This file is part of GNU Mailman.
#
# GNU Mailman is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# GNU Mailman is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# GNU Mailman.  If not, see <http://www.gnu.org/licenses/>.

"""Harness for testing Mailman's documentation."""

from contextlib import contextmanager

__all__ = [
    'dump',
    ]


def dump(results):
    if results is None:
        print(None)
        return
    for key in sorted(results):
        if key == 'entries':
            for i, entry in enumerate(results[key]):
                # entry is a dictionary.
                print('entry %d:' % i)
                for entry_key in sorted(entry):
                    print('    {0}: {1}'.format(entry_key, entry[entry_key]))
        else:
            print('{0}: {1}'.format(key, results[key]))


@contextmanager
def print_exception(*args, **kw):
    try:
        yield
    except Exception as ex:
        print(f'{type(ex).__name__}: {ex}')
