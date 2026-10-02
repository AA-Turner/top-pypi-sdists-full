# Copyright (C) 2021-2023 by the Free Software Foundation, Inc.
#
# This file is part of mailman.client.
#
# mailman.client is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, version 3 of the License.
#
# mailman.client is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with mailman.client.  If not, see <http://www.gnu.org/licenses/>.

"""Some async method utilities."""

__all__ = [
    'list_of_objects',
]

from typing import List, TypeVar, Type
from mailmanclient.restobjects.types import ContentType, ConnectionProto
from mailmanclient.restbase.async_base import RESTObject


T = TypeVar('T', bound=RESTObject)


def list_of_objects(
        obj_type: Type[T],
        response: ContentType,
        connection: ConnectionProto) -> List[T]:
    """Convert a list of 'entries' in response to list of objects."""
    if 'entries' in response:
        entries = response.get('entries')
        if entries is not None:
            return [obj_type(connection, data) for data in entries]
    return []
