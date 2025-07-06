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
"""Async client for Mailman Core 3.1 API.


AsyncClient provides a thin Python API over Mailman Core's HTTP API. It is
currently is very early stages and supports on read operations. Some of the
read operations might be missinng as well.

To start using the client, you need an async http library. httpx_ is officially
supported one, but making some other client work with it is pretty easy.
::

    >>> import httpx
    >>> conn = httpx.AsyncClient()
    >>> from mailmanclient.asynclient import AsyncClient
    >>> client = AsyncClient(conn, 'http://localhost:8001/3.1',
    ...                      'restadmin', 'restpass')


You will need an event loop to actually run the client. You can reuse your
existing one by calling ``await`` on the client methods, or you can create a
new one using the standard library ``asyncio`` module.
::

    >>> import asyncio
    >>> domains = asyncio.run(client.domains())

.. _httpx: https://www.python-httpx.org/

"""

__all__ = [
    'AsyncClient',
]

from typing import List, Mapping, Any
from mailmanclient.restobjects.utils import list_of_objects
from mailmanclient.restobjects.types import HTTPClientProto
from mailmanclient.restbase.async_connection import Connection
from mailmanclient.asyncobjects.domain import Domain
from mailmanclient.asyncobjects.mailinglist import MailingList
from mailmanclient.asyncobjects.user import User
from mailmanclient.asyncobjects.address import Address
from mailmanclient.asyncobjects.member import Member


JSON_CONTENT_TYPE = 'application/json'


class AsyncClient:
    """Provide an Idiomatic API for Mailman Core.


    It requires an HTTP client instance as the first argument. You can use any
    client which has a ``.request()`` method and accepts named parameters
    ``url``, ``path``, ``auth``, ``method`` and ``data``. ``data`` is supposed
    to be a dictionary of parameters to be passed to the HTTP request and the
    rest are string parameters with their usual meaning.

    The parameters are based off on httpx python library.

    :param client: Http client object with an async request method.
    :param base_url: Base URL to Core's API.
    :param user: Core admin username.
    :param password: Core admin password.

    """

    def __init__(
        self,
        client: HTTPClientProto,
        base_url: str,
        user: str,
        password: str,
    ) -> None:
        self.client = client
        self.connection = Connection(self.client, base_url, user, password)

    async def domains(self) -> List[Domain]:
        """Get all domains.

        ``/<api>/domains``
        """
        response, content = await self.connection.call('domains')
        return list_of_objects(Domain, content, self.connection)

    async def system(self) -> Mapping[str, Any]:
        """Get the Mailman system information.

        ``/<api>/system``
        """
        response, content = await self.connection.call('system')
        return content

    async def lists(self) -> List[MailingList]:
        """Get a list of MailingLists

        ``/<api>/lists``
        """
        response, content = await self.connection.call('lists')
        return list_of_objects(MailingList, content, self.connection)

    async def members(self) -> List[Member]:
        """All the Members

        ``/<api>/members``
        """
        response, content = await self.connection.call('members')
        return list_of_objects(Member, content, self.connection)

    async def users(self) -> List[User]:
        """All the users in Mailman Core

        ``/<api>/users``
        """
        response, content = await self.connection.call('users')
        return list_of_objects(User, content, self.connection)

    async def addresses(self) -> List[Address]:
        """All the addresses in Mailman

        ``/<api>/address``
        """
        response, content = await self.connection.call('addresses')
        return list_of_objects(Address, content, self.connection)

    async def find_members(
            self, list_id: str = None, subscriber: str = None,
            role: str = None, moderation_action: str = None,
            delivery_status: str = None, delivery_mode: str = None,
    ) -> List[Member]:
        """Find members.

        ``/<api>/members/find``

        :param list_id: Mailinglist id.
        :param subscriber: Email or user_id or partial search string.
        :param role: Membership role. One of 'owner', 'member', 'nonmember' or
             'moderator'.
        :param moderation_action: One of the moderation action from 'defer',
             'accept', 'discard', 'reject', 'hold'.
        :param delivery_status: Delivery status of the Member. It can be one
             among 'enabled', 'by_user', 'by_moderator' or 'by_bounces'.
        :param delivery_mode: Delivery mode of the member. It can be one
             between 'plaintext_digests', 'mime_digests', 'regular'.
        """
        data = dict(list_id=list_id,
                    subscriber=subscriber,
                    role=role,
                    moderation_action=moderation_action,
                    delivery_status=delivery_status,
                    delivery_mode=delivery_mode)
        # Skip parameters that have None value.
        # TODO: Handle parameters that can have None value.
        data = {key: value for key, value in data.items() if value is not None}
        response, content = await self.connection.call(
            'members/find', data=data, method='GET')
        return list_of_objects(Member, content, self.connection)
