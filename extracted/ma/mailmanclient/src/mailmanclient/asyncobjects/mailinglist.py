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

"""Async Mailinglist object.."""

__all__ = [
    'MailingList',
]

from enum import Enum
from typing import List
from mailmanclient.restbase.async_base import RESTObject
from mailmanclient.asyncobjects.member import Member
from mailmanclient.restobjects.utils import list_of_objects
from mailmanclient.restobjects.types import ConnectionProto, ContentType


class MemberRole(Enum):
    """Member role values."""
    member = 'member'
    owner = 'owner'
    moderator = 'moderator'
    nonmember = 'nonmember'


class MailingList(RESTObject):

    _properties = ('advertised', 'display_name', 'fqdn_listname', 'list_id',
                   'list_name', 'mail_host', 'member_count', 'volume',
                   'self_link', 'description')

    def __repr__(self) -> str:
        return '<MailingList {}>'.format(self.fqdn_listname)

    async def config(self) -> 'Config':
        """Get MailingList settings.

        /<api>/lists/<listid>/config
        """
        path = 'lists/{}/config'.format(self.list_id)
        _, content = await self._connection.call(path)
        return Config(self, self._connection, content)

    async def get_roster(self, role) -> List[Member]:
        """Get MailingList roster.

        /<api>/lists/<listid>/roster/<role>
        """
        path = 'lists/{}/roster/{}'.format(self.fqdn_listname, role)
        _, content = await self._connection.call(path)
        return list_of_objects(Member, content, self._connection)

    async def members(self) -> List[Member]:
        """Get Mailinglist members (subscribers.)

        /<api>/lists/<listid>/roster/member
        """
        return await self.get_roster(MemberRole.member)

    async def owners(self) -> List[Member]:
        """Get Mailinglist owners.

        /<api>/lists/<listid>/roster/owner
        """
        return await self.get_roster(MemberRole.owner)

    async def moderators(self) -> List[Member]:
        """Get Mailinglist moderators.

        /<api>/lists/<listid>/roster/moderator
        """
        return await self.get_roster(MemberRole.moderator)

    async def nonmember(self) -> List[Member]:
        """Get Mailinglist nonmembers.

        /<api>/lists/<listid>/roster/nonmember
        """
        return await self.get_roster(MemberRole.nonmember)


class Config(RESTObject):

    _read_only_properties = (
        'bounces_address',
        'created_at',
        'digest_last_sent_at',
        'fqdn_listname',
        'join_address',
        'last_post_at',
        'leave_address',
        'list_id',
        'list_name',
        'mail_host',
        'next_digest_number',
        'no_reply_address',
        'owner_address',
        'post_id',
        'posting_address',
        'request_address',
        'scheme',
        'self_link',
        'volume',
        'web_host',
        )

    def __init__(self,
                 mailing_list: MailingList,
                 connection: ConnectionProto,
                 data: ContentType) -> None:
        super().__init__(connection, data)
        self.mailing_list = mailing_list

    def __repr__(self) -> str:
        return '<Settings for {}>'.format(self.mailing_list.fqdn_listname)
