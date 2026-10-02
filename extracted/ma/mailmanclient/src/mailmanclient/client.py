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

"""Client code."""

import warnings
from operator import itemgetter
from urllib.parse import quote

from mailmanclient.constants import (MISSING)
from mailmanclient.restobjects.address import Address
from mailmanclient.restobjects.ban import Bans, BannedAddress
from mailmanclient.restobjects.configuration import Configuration
from mailmanclient.restobjects.domain import Domain
from mailmanclient.restobjects.mailinglist import MailingList
from mailmanclient.restobjects.member import Member
from mailmanclient.restobjects.preferences import Preferences
from mailmanclient.restobjects.queue import Queue
from mailmanclient.restobjects.styles import Styles
from mailmanclient.restobjects.user import User
from mailmanclient.restobjects.templates import Template, TemplateList
from mailmanclient.restbase.connection import Connection
from mailmanclient.restbase.page import Page

__metaclass__ = type
__all__ = [
    'Client'
]


#
# --- The following classes are part of the API
#

class Client:
    """Access the Mailman REST API root.

    :param baseurl: The base url to access the Mailman 3 REST API.
    :type baseurl: str
    :param name: The Basic Auth user name.  If given, the `password` must
        also be given.
    :type name: str
    :param password: The Basic Auth password.  If given the `name` must
        also be given.
    :type password: str
    :param request_hooks: Callable hooks to process request parameters before
        being sent to Core's API.
    :type request_hooks: List[callables]
    """

    def __init__(self, baseurl, name=None, password=None, request_hooks=None):
        """Initialize client access to the REST API."""
        self._connection = Connection(baseurl, name, password, request_hooks)

    def __repr__(self):
        return '<Client ({0.name}:{0.password}) {0.baseurl}>'.format(
            self._connection)

    def add_hooks(self, request_hooks):
        """Add a hook to process connections to Mailman's API.

        Hooks are callables that are passed in the parameters of HTTP call made
        to Mailman Core' RESt API and are expected to return the same number of
        parameters back. This can be useful to manipulate parameters and update
        them, or simply log each call to API.
        ::

            from mailmanclient.client import Client
            client = Client('http://localhost:8001/3.1', <user>, <password>)

            def sample_hook(params):
                print(f'Request params are {params}')
                return params

            client.add_hook([sample_hook])


        :param request_hooks: A list of callables that take in a dictionary of
           parameters. ``params`` is the list of request parameters before the
           request is made.
        """
        self._connection.add_hooks(request_hooks=request_hooks)

    @property
    def system(self):
        """Get the basic system information.

        :returns: System information about Mailman Core
        :rtype: Dict[str, str]
        """
        return self._connection.call('system/versions')[1]

    @property
    def preferences(self):
        """Get all default system Preferences.

        :returns: System preferences.
        :rtype: :class:`Preferences`
        """
        return Preferences(self._connection, 'system/preferences')

    @property
    def configuration(self):
        """Get the system configuration.

        :returns: All the system configuration.
        :rtype: Dict[str, :class:`Configuration`]
        """
        response, content = self._connection.call('system/configuration')
        return {section: Configuration(
            self._connection, section) for section in content['sections']}

    @property
    def pipelines(self):
        """Get a list of all Pipelines.

        :returns: A list of all the pipelines in Core.
        :rtype: List
        """
        response, content = self._connection.call('system/pipelines')
        return content

    @property
    def chains(self):
        """Get a list of all the Chains.

        :returns: A list of all the chains in Core.
        :rtype: List
        """
        response, content = self._connection.call('system/chains')
        return content

    @property
    def queues(self):
        """Get a list of all Queues.

        :returns: A list of all the queues in Core.
        :rtype: List
        """
        response, content = self._connection.call('queues')
        queues = {}
        for entry in content['entries']:
            queues[entry['name']] = Queue(
                self._connection, entry['self_link'], entry)
        return queues

    @property
    def styles(self):
        """All the default styles in Mailman Core.

        :returns: All the styles in Core.
        :rtype: :class:`Styles`
        """
        return Styles(self._connection, 'lists/styles')

    @property
    def lists(self):
        """Get a list of all MailingLists.

        :returns: All the mailing lists.
        :rtype: list(:class:`MailingList`)
        """
        return self.get_lists()

    def get_lists(self, advertised=False):
        """Get a list of all the MailingLists.

        :param advertised: If marked True, returns all MailingLists including
                           the ones that aren't advertised.
        :type advertised: bool
        :returns: A list of mailing lists.
        :rtype: List(:class:`MailingList`)
        """
        url = 'lists'
        if advertised:
            url += '?advertised=true'
        response, content = self._connection.call(url)
        if 'entries' not in content:
            return []
        return [MailingList(self._connection, entry['self_link'], entry)
                for entry in content['entries']]

    def get_list_page(self, count=50, page=1, advertised=None, mail_host=None):
        """Get a list of all MailingList with pagination.

        :param count: Number of entries per-page (defaults to 50).
        :param page: The page number to return (defaults to 1).
        :param advertised: If marked True, returns all MailingLists including
                           the ones that aren't advertised.
        :param mail_host: Domain to filter results by.
        """
        if mail_host:
            url = 'domains/{0}/lists'.format(mail_host)
        else:
            url = 'lists'
        if advertised:
            url += '?advertised=true'
        return Page(self._connection, url, MailingList, count, page)

    @property
    def domains(self):
        """Get a list of all Domains.

        :returns: All the domains on the system.
        :rtype: List[:class:`Domain`]
        """
        response, content = self._connection.call('domains')
        if 'entries' not in content:
            return []
        return [Domain(self._connection, entry['self_link'])
                for entry in sorted(content['entries'],
                                    key=itemgetter('mail_host'))]

    @property
    def members(self):
        """Get a list of all the Members.

        :returns: All the list memebrs.
        :rtype: List[:class:`Member`]
        """
        response, content = self._connection.call('members')
        if 'entries' not in content:
            return []
        return [Member(self._connection, entry['self_link'], entry)
                for entry in content['entries']]

    def get_member(self, fqdn_listname, subscriber_address):
        """Get the Member object for a given MailingList and Subsciber's Email
        Address.

        :param str fqdn_listname: Fully qualified address for the MailingList.
        :param str subscriber_address: Email Address for the subscriber.
        :returns: A member of a list.
        :rtype: :class:`Member`
        """
        return self.get_list(fqdn_listname).get_member(subscriber_address)

    def get_nonmember(self, fqdn_listname, nonmember_address):
        """Get the Member object for a given MailingList and Non-member's
        Email.

        :param str fqdn_listname: Fully qualified address for the MailingList.
        :param str subscriber_address: Email Address for the non-member.
        :returns: A member of a list.
        :rtype: :class:`Member`
        """
        return self.get_list(fqdn_listname).get_nonmember(nonmember_address)

    def get_member_page(self, count=50, page=1):
        """Return a paginated list of Members.

        :param int count: Number of items to return.
        :param int page: The page number.
        :returns: Paginated lists of members.
        :rtype: :class:`Page` of :class:`Member`.
        """
        return Page(self._connection, 'members', Member, count, page)

    @property
    def users(self):
        """Get all the users.

        :returns: All the users in Mailman Core.
        :rtype: List[:class:`User`]
        """
        response, content = self._connection.call('users')
        if 'entries' not in content:
            return []
        return [User(self._connection, entry['self_link'], entry)
                for entry in sorted(content['entries'],
                                    key=itemgetter('self_link'))]

    def get_user_page(self, count=50, page=1):
        """Get all the users with pagination.

        :param int count: Number of entries per-page (defaults to 50).
        :param int page: The page number to return (defaults to 1).
        :returns: Paginated list of users on Mailman.
        :rtype: :class:`Page` of :class:`User`
        """
        return Page(self._connection, 'users', User, count, page)

    def create_domain(self, mail_host, base_url=MISSING,
                      description=None, owner=None, alias_domain=None):
        """Create a new Domain.

        :param str mail_host: The Mail host for the new domain. If you want
            foo@bar.com" as the address for your MailingList, use "bar.com"
            here.
        :param str description: A brief description for this Domain.
        :param str owner: Email address for the owner of this list.
        :param str alias_domain: Alias domain.
        :returns: The created Domain.
        :rtype: :class:`Domain`
        """
        if base_url is not MISSING:
            warnings.warn(
                'The `base_url` parameter in the `create_domain()` method is '
                'deprecated. It is not used any more and will be removed in '
                'the future.', DeprecationWarning, stacklevel=2)
        data = dict(mail_host=mail_host)
        if description is not None:
            data['description'] = description
        if owner is not None:
            data['owner'] = owner
        if alias_domain is not None:
            data['alias_domain'] = alias_domain
        response, content = self._connection.call('domains', data)
        return Domain(self._connection, response.headers.get('location'))

    def delete_domain(self, mail_host):
        """Delete a Domain.

        :param str mail_host: The Mail host for the domain you want to delete.
        """
        response, content = self._connection.call(
            'domains/{0}'.format(mail_host), None, 'DELETE')

    def get_domain(self, mail_host, web_host=MISSING):
        """Get Domain by its mail_host."""
        if web_host is not MISSING:
            warnings.warn(
                'The `web_host` parameter in the `get_domain()` method is '
                'deprecated. It is not used any more and will be removed in '
                'the future.', DeprecationWarning, stacklevel=2)
        response, content = self._connection.call(
            'domains/{0}'.format(mail_host))
        return Domain(self._connection, content['self_link'])

    def create_user(self, email, password, display_name=''):
        """Create a new User.

        :param str email: Email address for the new user.
        :param str password: Password for the new user.
        :param str display_name: An optional name for the new user.
        :returns: The created user instance.
        :rtype: :class:`User`
        """
        response, content = self._connection.call(
            'users', dict(email=email,
                          password=password,
                          display_name=display_name))
        return User(self._connection, response.headers.get('location'))

    def get_user(self, address):
        """Given an Email Address, return the User it belongs to.

        :param str address: Email Address of the User.
        :returns: The user instance that owns the address.
        :rtype: :class:`User`
        """
        response, content = self._connection.call(
            'users/{0}'.format(address))
        return User(self._connection, content['self_link'], content)

    def get_address(self, address):
        """Given an Email Address, return the Address object.

        :param str address: Email address.
        :returns: The Address object for given email address.
        :rtype: :class:`Address`
        """
        response, content = self._connection.call(
            'addresses/{0}'.format(address))
        return Address(self._connection, content['self_link'], content)

    def get_list(self, fqdn_listname):
        """Get a MailingList object.

        :param str fqdn_listname: Fully qualified name of the MailingList.
        :returns: The mailing list object of the given fqdn_listname.
        :rtype: :class:`MailingList`
        """
        response, content = self._connection.call(
            'lists/{0}'.format(fqdn_listname))
        return MailingList(self._connection, content['self_link'], content)

    def delete_list(self, fqdn_listname):
        """Delete a MailingList.

        :param str fqdn_listname: Fully qualified name of the MailingList.
        """
        response, content = self._connection.call(
            'lists/{0}'.format(fqdn_listname), None, 'DELETE')

    @property
    def bans(self):
        """Get a list of all the bans.

        :returns: A list of all the bans.
        :rtype: :class:`Bans`
        """
        return Bans(self._connection, 'bans', mlist=None)

    def get_bans_page(self, count=50, page=1):
        """Get a list of all the bans with pagination.

        :param int count: Number of entries per-page (defaults to 50).
        :param int page: The page number to return (defaults to 1).
        :returns: Paginated list of banned addresses.
        :rtype: :class:`Page` of :class:`BannedAddress`
        """
        return Page(self._connection, 'bans', BannedAddress, count, page)

    @property
    def templates(self):
        """Get all site-context templates.

        :returns: List of templates for the site context.
        :rtype: :class:`TemplateList`
        """
        return TemplateList(self._connection, 'uris')

    def get_templates_page(self, count=25, page=1):
        """Get paginated site-context templates.

        :returns: Paginated list of templates of site context.
        :rtype: :class:`Page` of :class:`Template`
        """
        return Page(self._connection, 'uris', Template, count, page)

    def set_template(self, template_name, url, username=None, password=None):
        """Set template in site-context.

        :param str template_name: The template to set.
        :param str url: The URL to fetch the template from.
        :param str username: Username for access to the template.
        :param str password: Password for the ``username`` to access templates.
        """
        data = {template_name: url}
        if username is not None and password is not None:
            data['username'] = username
            data['password'] = password
        return self._connection.call('uris', data, 'PATCH')[1]

    def find_lists(self, subscriber, role=None, count=50, page=1,
                   mail_host=None):
        """Given a subscriber and a role, return all the list they are
        subscribed to with given role.

        If no role is specified all the related mailing lists are returned
        without duplicates, even though there can potentially be multiple
        memberships of a user in a single mailing list.

        :param str subscriber: The address of the subscriber.
        :param str role: owner, moderator or subscriber.
        :param int count: Number of entries per-page (defaults to 50).
        :param int page: The page number to return (defaults to 1).
        :param str mail_host: Domain to filter results by.
        :returns: A filtered list of mailing lists with given filters.
        :rtype: List[:class:`MailingList`]
        """
        url = 'lists/find'
        data = dict(subscriber=subscriber, count=count, page=page)
        if role is not None:
            data['role'] = role
        response, content = self._connection.call(url, data)
        if 'entries' not in content:
            return []
        return [MailingList(self._connection, entry['self_link'], entry)
                for entry in content['entries']
                if not mail_host or entry['mail_host'] == mail_host]

    def find_users(self, query):
        """Find users with query string matching display name and emails.

        :param str query: The string to search for. The search string is case
            insensitive as core doens't care about the case.
        :param int count: Number of entries per-page (defaults to 50).
        :param int page: The page number to return (defaults to 1).
        """
        url = 'users/find?q={}'.format(quote(query))
        response, content = self._connection.call(url)
        if 'entries' not in content:
            return []
        return [User(self._connection, entry['self_link'], entry)
                for entry in content['entries']]

    def find_users_page(self, query, count, page):
        """Same as :py:meth:`find_users` but allows for pagination.

        :param str query: The string to search for. The search string is case
            insensitive as core doens't care about the case.
        :param int count: Number of entries per-page (defaults to 50).
        :param int page: The page number to return (defaults to 1).
        """
        url = 'users/find?q={}'.format(quote(query))
        return Page(self._connection, url, User, count, page)
