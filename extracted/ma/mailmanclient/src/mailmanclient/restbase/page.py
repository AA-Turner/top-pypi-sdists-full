# Copyright (C) 2010-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailmanclient.
#
# mailmanclient is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailmanclient is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailmanclient.  If not, see <http://www.gnu.org/licenses/>.
from urllib.parse import urlencode, urlsplit, parse_qs, urlunsplit

from mailmanclient.constants import DEFAULT_PAGE_ITEM_COUNT

__metaclass__ = type
__all__ = [
    'Page'
]


class Page:

    def __init__(self, connection, path, model, count=DEFAULT_PAGE_ITEM_COUNT,
                 page=1):
        self._connection = connection
        self._path = path
        self._count = count
        self._page = page
        self._model = model
        self._entries = []
        self.total_size = 0
        self._create_page()

    def __getitem__(self, key):
        return self._entries[key]

    def __iter__(self):
        for entry in self._entries:
            yield entry

    def __repr__(self):
        return '<Page {0} ({1})'.format(self._page, self._model)

    def __len__(self):
        return len(self._entries)

    def _build_url(self):
        url = list(urlsplit(self._path))
        qs = parse_qs(url[3])
        qs["count"] = self._count
        qs["page"] = self._page
        url[3] = urlencode(qs, doseq=True)
        return urlunsplit(url)

    def _create_page(self):
        self._entries = []
        response, content = self._connection.call(self._build_url())
        self.total_size = content["total_size"]
        for entry in content.get('entries', []):
            instance = self._model(
                self._connection, entry['self_link'], entry)
            self._entries.append(instance)

    @property
    def nr(self):
        return self._page

    @property
    def next(self):
        return self.__class__(
            self._connection, self._path, self._model, self._count,
            self._page + 1)

    @property
    def previous(self):
        if self.has_previous:
            return self.__class__(
                self._connection, self._path, self._model, self._count,
                self._page - 1)

    @property
    def has_previous(self):
        return self._page > 1

    @property
    def has_next(self):
        return self._count * self._page < self.total_size
