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
from mailmanclient.restbase.base import RESTDict

__metaclass__ = type
__all__ = [
    'Settings'
]


class Settings(RESTDict):

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
