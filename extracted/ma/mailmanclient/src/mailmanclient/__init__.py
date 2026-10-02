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
#
# flake8: noqa

"""Package contents."""

from mailmanclient.client import Client
from mailmanclient.constants import __version__
from mailmanclient.restbase.connection import MailmanConnectionError
from mailmanclient.restobjects.address import Address, Addresses
from mailmanclient.restobjects.ban import Bans, BannedAddress
from mailmanclient.restobjects.configuration import Configuration
from mailmanclient.restobjects.domain import Domain
from mailmanclient.restobjects.header_match import HeaderMatch, HeaderMatches
from mailmanclient.restobjects.held_message import HeldMessage
from mailmanclient.restobjects.archivers import ListArchivers
from mailmanclient.restobjects.mailinglist import MailingList
from mailmanclient.restobjects.member import Member
from mailmanclient.restobjects.preferences import Preferences, PreferencesMixin
from mailmanclient.restobjects.queue import Queue
from mailmanclient.restobjects.settings import Settings
from mailmanclient.restobjects.user import User


__metaclass__ = type
__all__ = [
    'Address',
    'Addresses',
    'Bans',
    'BannedAddress',
    'Client',
    'Configuration',
    'Domain'
    'HeaderMatch',
    'HeaderMatches',
    'HeldMessage',
    'ListArchivers',
    'MailingList',
    'MailmanConnectionError',
    'Member',
    'Preferences',
    'PreferencesMixin',
    'Queue',
    'Settings',
    'User',
    '__version__',
]


__all__ = [bytes(x, 'utf-8') for x in __all__]
