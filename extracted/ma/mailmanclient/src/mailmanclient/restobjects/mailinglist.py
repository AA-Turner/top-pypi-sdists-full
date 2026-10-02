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
import warnings
from operator import itemgetter
from urllib.error import HTTPError
from urllib.parse import urlencode, quote_plus

from mailmanclient.restobjects.header_match import HeaderMatches
from mailmanclient.restobjects.archivers import ListArchivers
from mailmanclient.restobjects.member import Member
from mailmanclient.restobjects.settings import Settings
from mailmanclient.restobjects.held_message import HeldMessage
from mailmanclient.restobjects.templates import TemplateList
from mailmanclient.restbase.base import RESTObject
from mailmanclient.restbase.page import Page

__metaclass__ = type
__all__ = [
    'MailingList'
]


class MailingList(RESTObject):

    _properties = ('advertised', 'display_name', 'fqdn_listname', 'list_id',
                   'list_name', 'mail_host', 'member_count', 'volume',
                   'self_link', 'description')

    def __init__(self, connection, url, data=None):
        super(MailingList, self).__init__(connection, url, data)
        self._settings = None

    def __repr__(self):
        return '<List {0!r}>'.format(self.fqdn_listname)

    @property
    def owners(self):
        """All MailingList owners."""
        return self.get_roster('owner')

    def get_roster(self, roster, fields=None):
        """Get roster of the MailingList.

        If the fields is specified without `self_link` and `address`, they are
        added since it is required for returning the response.

        :param str roster: One of the Membership rosters from
           'owner', 'moderator', 'member' and 'nonmember'.
        :param List[str] fields: List of Member's fields to fetch from the
           API. Skipping certain fields can speed up the API response
           when they aren't required since they need to be fetched from
           database individually.
        """
        url = self._url + '/roster/{}'.format(roster)
        if fields is not None:
            # We cannot instantiate Member object without address and
            # self_link objects, so just add them too. They don't add
            # a lot of overhead.
            if 'address' not in fields:
                fields.append('address')
            if 'self_link' not in fields:
                fields.append('self_link')
            url += '?' + '&'.join('fields={}'.format(each) for each in fields)
        response, content = self._connection.call(url)
        if 'entries' not in content:
            return []
        else:
            return [Member(self._connection, entry['self_link'], entry)
                    for entry in sorted(content['entries'],
                                        key=itemgetter('address'))]

    @property
    def moderators(self):
        """All MailingList moderators."""
        return self.get_roster('moderator')

    @property
    def members(self):
        """All MailingList members."""
        return self.get_roster('member')

    @property
    def nonmembers(self):
        """All MailingList non-members."""
        return self.get_roster('nonmember')

    def get_member_page(self, count=50, page=1, fields=None):
        """Return a paginated list of MailingList's members.

        :param int count: Count of members in one page.
        :param int page: The page number.
        """
        url = 'lists/{0}/roster/member'.format(self.fqdn_listname)
        return Page(self._connection, url, Member, count, page)

    def find_members(
            self, address=None, role=None, page=None, count=50):
        """Find a Mailinglist's members.

        This provides a filtering API for list's Members including,
        non-members, owners and moderators by speciying the role.

        :param str address: Member's address.
        :param str role: Member's role.
        :param int page: Page number for paginated results.
        :param int count: Number of results per-page for paginated results.

        """
        data = {'list_id': self.list_id}
        if address:
            data['subscriber'] = address
        if role:
            data['role'] = role

        url = 'members/find?{}'.format(urlencode(data, doseq=True))
        if page is None:
            response, content = self._connection.call(url, data)
            if 'entries' not in content:
                return []
            return [Member(self._connection, entry['self_link'], entry)
                    for entry in content['entries']]
        else:
            return Page(self._connection, url, Member, count, page)

    @property
    def settings(self):
        """All MailingList settings."""
        if self._settings is None:
            self._settings = Settings(
                self._connection,
                'lists/{0}/config'.format(self.fqdn_listname))
        return self._settings

    @property
    def held(self):
        """Held messages of a MailingList.."""
        response, content = self._connection.call(
            'lists/{0}/held'.format(self.fqdn_listname), None, 'GET')
        if 'entries' not in content:
            return []
        return [HeldMessage(self._connection, entry['self_link'], entry)
                for entry in content['entries']]

    def get_held_page(self, count=50, page=1):
        """Paginated list of held messages for the MailingList.

        :param int page: Page number for paginated results.
        :param int count: Number of results per-page for paginated results.
        """
        url = 'lists/{0}/held'.format(self.fqdn_listname)
        return Page(self._connection, url, HeldMessage, count, page)

    def get_held_count(self):
        """Get a count of held messages for the MailingList."""
        response, json = self._connection.call(
            'lists/{}/held/count'.format(self.fqdn_listname), None, 'GET')
        return json['count']

    def get_held_message(self, held_id):
        """Get a single held message for MailingList.

        :param int held_id: Held message id to get.
        """
        url = 'lists/{0}/held/{1}'.format(self.fqdn_listname, held_id)
        return HeldMessage(self._connection, url)

    @property
    def requests(self):
        """See :meth:`get_requests`."""
        return self.get_requests()

    @property
    def unsubscription_requests(self):
        """Get a list of subscription requests pending moderator Approval."""
        return self.get_requests(request_type='unsubscription')

    def get_requests(self, token_owner=None, request_type='subscription'):
        """Return a list of dicts with subscription requests.

        This is the new API for requests which allows filtering via
        `token_owner` since it isn't possible to do so via the property
        requests.

        :param token_owner: Who owns the pending requests?  Should be one in
            'no_one', 'moderator' and 'subscriber'.
        :param request_type: The type of pending request. Value should be in
            'subscription' or 'unsubscription'. Defaults to 'subscription'.
        """
        url = 'lists/{0}/requests'.format(self.fqdn_listname)
        fragments = []
        if token_owner:
            fragments.append('token_owner={}'.format(token_owner))
        if request_type:
            fragments.append('request_type={}'.format(request_type))
        if fragments:
            url += '?{}'.format('&'.join(fragments))
        response, content = self._connection.call(url, None, 'GET')
        if 'entries' not in content:
            return []
        else:
            entries = []
            for entry in content['entries']:
                request = dict(email=entry['email'],
                               token=entry['token'],
                               display_name=entry['display_name'],
                               token_owner=entry['token_owner'],
                               list_id=entry['list_id'],
                               request_date=entry['when'])
                entries.append(request)
        return entries

    def get_requests_count(self, token_owner=None):
        """Return a total count of pending subscription requests.

        This should be a faster query when *all* the requests aren't needed and
        only a count is needed to display on the badge in List's settings page.

        :param token_owner: Who owns the pending requests?  Should be one in
            'no_one', 'moderator' and 'subscriber'.
        :returns: The count of pending requests.
        """
        url = 'lists/{}/requests/count'.format(self.fqdn_listname)
        if token_owner:
            url += '?token_owner={}'.format(token_owner)
        response, json = self._connection.call(url)
        return json['count']

    def get_request(self, token):
        """Get an individual pending request for the given token.

        :param token: The token for the request.
        :returns: The request dictionary.
        """
        url = 'lists/{}/requests/{}'.format(self.fqdn_listname, token)
        response, json = self._connection.call(url)
        return json

    @property
    def archivers(self):
        """Get a list of MailingList archivers."""
        url = 'lists/{0}/archivers'.format(self.list_id)
        return ListArchivers(self._connection, url, self)

    @archivers.setter
    def archivers(self, new_value):
        url = 'lists/{0}/archivers'.format(self.list_id)
        archivers = ListArchivers(self._connection, url, self)
        archivers.update(new_value)
        archivers.save()

    def add_owner(self, address, display_name=None):
        """Add a list owner.

        :param str address: Email address of the owner.
        :param str display_name: Display name of the Owner.
        """
        self.add_role('owner', address, display_name)

    def add_moderator(self, address, display_name=None):
        """Add a list moderator.

        :param str address: Email address of the moderator.
        :param str display_name: Display name of the moderator.
        """
        self.add_role('moderator', address, display_name)

    def add_role(self, role, address, display_name=None):
        """Add a new Member with a specific role.

        :param str role: The role for the new member.
        :param str address: A valid email address for the new Member.
        :param str display_name: An optional display name for the Member.
        """
        data = dict(list_id=self.list_id,
                    subscriber=address,
                    display_name=display_name,
                    role=role)
        self._connection.call('members', data)

    def remove_owner(self, address):
        """Remove a list owner.

        :param str address: Email address of the owner to remove.
        """
        self.remove_role('owner', address)

    def remove_moderator(self, address):
        """Remove a list moderator.

        :param str address: Email address of the moderator to remove.
        """
        self.remove_role('moderator', address)

    def remove_role(self, role, address):
        """Remove a list Member with a specific Role.

        :param str role: The role for the new member.
        :param str address: A valid email address for the new Member.
        """
        url = 'lists/%s/%s/%s' % (
            self.fqdn_listname, role, quote_plus(address))
        self._connection.call(url, method='DELETE')

    def moderate_message(self, request_id, action, comment=None):
        """Moderate a held message.

        :param request_id: Id of the held message.
        :type request_id: Int.
        :param action: Action to perform on held message.
        :type action: String.
        :param comment: The reason for action, only supported for rejection.
        :type comment: str
        """
        data = dict(action=action)
        if comment is not None:
            data['comment'] = comment

        path = 'lists/{0}/held/{1}'.format(
            self.fqdn_listname, str(request_id))
        response, content = self._connection.call(
            path, data, 'POST')
        return response

    def discard_message(self, request_id):
        """Shortcut for moderate_message.

        :param str request_id: The request_id of the held message.
        """
        return self.moderate_message(request_id, 'discard')

    def reject_message(self, request_id, reason=None):
        """Shortcut for moderate_message.

        :param str request_id: The request_id of the held message.
        :param str reason: An optional reason for rejection of the message.
        """
        return self.moderate_message(request_id, 'reject', reason)

    def defer_message(self, request_id):
        """Shortcut for moderate_message.

        :param str request_id: The request_id of the held message.
        """
        return self.moderate_message(request_id, 'defer')

    def accept_message(self, request_id):
        """Shortcut for moderate_message.

        :param str request_id: The request_id of the held message.
        """
        return self.moderate_message(request_id, 'accept')

    def moderate_request(self, request_id, action, reason=None):
        """
        Moderate a subscription request.

        :param action: accept|reject|discard|defer
        :type action: str.
        :param reason: The reason associated with rejections.
        :type reason: str
        """
        path = 'lists/{0}/requests/{1}'.format(self.list_id, request_id)
        data = {'action': action}
        if reason:
            data['reason'] = reason
        response, content = self._connection.call(path, data)
        return response

    def manage_request(self, token, action):
        """Alias for moderate_request, kept for compatibility"""
        warnings.warn(
            'The `manage_request()` method has been replaced by '
            '`moderate_request()` and will be removed in the future.',
            DeprecationWarning, stacklevel=2)
        return self.moderate_request(token, action)

    def accept_request(self, request_id):
        """Shortcut to accept a subscription request."""
        return self.moderate_request(request_id, 'accept')

    def reject_request(self, request_id):
        """Shortcut to reject a subscription request."""
        return self.moderate_request(request_id, 'reject')

    def discard_request(self, request_id):
        """Shortcut to discard a subscription request."""
        return self.moderate_request(request_id, 'discard')

    def defer_request(self, request_id):
        """Shortcut to defer a subscription request."""
        return self.moderate_request(request_id, 'defer')

    def _get_membership(self, email, role):
        """Get a single membership resource.

        :param address: The email address of the member for this list.
        :param role: The membership role.
        :return: A member proxy object.
        """
        # In order to get the member object we query the REST API for
        # the member. Incase there is no matching subscription, an
        # HTTPError is returned instead.
        try:
            path = 'lists/{0}/{1}/{2}'.format(
                self.list_id, role, quote_plus(email))
            response, content = self._connection.call(path)
            return Member(self._connection, content['self_link'], content)
        except HTTPError:
            raise ValueError('%s is not a %s address of %s' %
                             (email, role, self.fqdn_listname))

    def get_member(self, email):
        """Get a Member of the list.

        :param address: The email address of the member for this list.
        :return: A member proxy object.
        """
        return self._get_membership(email, 'member')

    def get_nonmember(self, email):
        """Get a non-member of the list.

        :param address: The email address of the non-member for this list.
        :return: A member proxy object.
        """
        return self._get_membership(email, 'nonmember')

    def subscribe(self, address, display_name=None, pre_verified=False,
                  pre_confirmed=False, pre_approved=False, invitation=False,
                  send_welcome_message=None, delivery_mode=None,
                  delivery_status=None):
        """Subscribe an email address to a mailing list.

        :param address: Email address to subscribe to the list.
        :type address: str
        :param display_name: The real name of the new member.
        :type display_name: str
        :param pre_verified: True if the address has been verified.
        :type pre_verified: bool
        :param pre_confirmed: True if membership has been approved by the user.
        :type pre_confirmed: bool
        :param pre_approved: True if membership is moderator-approved.
        :type pre_approved: bool
        :param invitation: True if this is an invitation to join the list.
        :type invitation: bool
        :param send_welcome_message: True if welcome message should be sent.
        :type send_welcome_message: bool
        :param delivery_mode: Delivery mode of the Member.
        :type delivery_mode: str. One between 'regular', 'plaintext_digests',
            'mime_digests', 'summary_digests'.
        :param delivery_status: Delivery status of the Member.
        :type delivery_status: str. One between 'enabled', 'by_owner',
            'by_moderator', 'by_user'.
        :return: A member proxy object.
        """
        data = dict(
            list_id=self.list_id,
            subscriber=address,
        )
        if display_name:
            data['display_name'] = display_name
        if pre_verified:
            data['pre_verified'] = True
        if pre_confirmed:
            data['pre_confirmed'] = True
        if pre_approved:
            data['pre_approved'] = True
        if invitation:
            data['invitation'] = True
        if delivery_mode:
            data['delivery_mode'] = delivery_mode
        if delivery_status:
            data['delivery_status'] = delivery_status
        # Even if it is False, we should send this value because it means we
        # should suppress welcome message, so check for None value to skip the
        # parameter.
        if send_welcome_message is not None:
            data['send_welcome_message'] = send_welcome_message
        response, content = self._connection.call('members', data)
        # If a member is not immediately subscribed (i.e. verificatoin,
        # confirmation or approval need), the response content is returned.
        if response.status_code == 202:
            return content
        # If the subscription is executed immediately, a member object
        # is returned.
        return Member(self._connection, response.headers.get('location'))

    def unsubscribe(self, email, pre_confirmed=None,
                    pre_approved=None):
        """Unsubscribe an email address from a mailing list.

        :param address: Email address to unsubscribe.
        :type address: str
        :param pre_confirmed: True if unsubscribe is approved by the user.
        :type pre_confirmed: bool
        :param pre_approved: True if unsubscribe is moderator-approved.
        :type pre_approved: bool
        """
        data = dict()
        if pre_confirmed is not None:
            data['pre_confirmed'] = pre_confirmed
        if pre_approved is not None:
            data['pre_approved'] = pre_approved
        try:
            path = 'lists/{0}/member/{1}'.format(self.list_id, email)
            response, json = self._connection.call(path, data, method='DELETE')
            if response.status_code == 202:
                return json
        except HTTPError:
            # The member link does not exist, i.e. they are not a member
            raise ValueError('%s is not a member address of %s' %
                             (email, self.fqdn_listname))

    def mass_unsubscribe(self, email_list):
        """Unsubscribe a list of emails from a mailing list.

        This function return a json of emails mapped to booleans based
        on whether they were unsubscribed or not, for whatever reasons

        :param email_list: list of emails to unsubscribe
        """
        try:
            path = 'lists/{}/roster/member'.format(self.list_id)
            response, content = self._connection.call(
                path, {'emails': email_list}, 'DELETE')
            return content
        except HTTPError as e:
            raise ValueError(str(e))

    @property
    def bans(self):
        """A list of banned addresses for this MailingList."""
        from mailmanclient.restobjects.ban import Bans
        url = 'lists/{0}/bans'.format(self.list_id)
        return Bans(self._connection, url, mlist=self)

    def get_bans_page(self, count=50, page=1):
        """Get a paginated list of bans for this MailingList.

        :param int page: Page number for paginated results.
        :param int count: Number of results per-page for paginated results.
        """
        from mailmanclient.restobjects.ban import BannedAddress
        url = 'lists/{0}/bans'.format(self.list_id)
        return Page(self._connection, url, BannedAddress, count, page)

    @property
    def header_matches(self):
        """A list of header-match rules for the MailingList."""
        url = 'lists/{0}/header-matches'.format(self.list_id)
        return HeaderMatches(self._connection, url, self)

    @property
    def templates(self):
        """Get a list of MailingList templates."""
        url = self._url + '/uris'
        return TemplateList(self._connection, url)

    def set_template(self, template_name, uri, username=None, password=None):
        """Set a MailingList template URI.

        :param str template_name: The name of the template.
        :param str uri: The URI to fetch the template.
        :param str username: Username for fetching template from uri.
        :param str password: Password for fetching template from uri.
        """
        url = self._url + '/uris'
        data = {template_name: uri}
        if username is not None and password is not None:
            data['username'] = username
            data['password'] = password
        return self._connection.call(url, data, 'PATCH')[1]

    def _check_membership(self, address, allowed_roles):
        """
        Given an address and role, check if there is a membership record that
        matches the given address with a given role for this Mailing List.
        """
        url = 'members/find'
        data = {'subscriber': address,
                'list_id': self.list_id}
        response, content = self._connection.call(url, data=data)
        if 'entries' not in content:
            return False
        for membership in content['entries']:
            # We check for all the returned roles for this User and MailingList
            if membership['role'] in allowed_roles:
                return True
        return False

    def is_owner(self, address):
        """
        Given an address, checks if the given address is an owner of this
        mailing list.
        """
        return self._check_membership(address=address,
                                      allowed_roles=('owner',))

    def is_moderator(self, address):
        """
        Given an address, checks if the given address is a moderator of this
        mailing list.
        """
        return self._check_membership(address=address,
                                      allowed_roles=('moderator',))

    def is_member(self, address):
        """
        Given an address, checks if the given address is subscribed to this
        mailing list.
        """
        return self._check_membership(address=address,
                                      allowed_roles=('member',))

    def is_owner_or_mod(self, address):
        """
        Given an address, checks if the given address is either a owner or
        a moderator of this list.

        It is possible for them to be both owner and moderator.
        """
        return self._check_membership(address=address,
                                      allowed_roles=('owner', 'moderator'))
