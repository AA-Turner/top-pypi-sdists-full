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

from mailmanclient.restbase.base import RESTObject

__metaclass__ = type
__all__ = [
    'HeldMessage'
]


class HeldMessage(RESTObject):

    _properties = ('hold_date', 'message_id', 'msg', 'reason', 'request_id',
                   'self_link', 'sender', 'subject', 'type')

    def __repr__(self):
        return '<HeldMessage {0!r} by {1}>'.format(
            self.request_id, self.sender)

    def moderate(self, action, comment=None):
        """Moderate a held message.

        :param action: Action to perform on held message.
        :type action: String.
        """
        data = dict(action=action)
        if comment is not None:
            data['comment'] = comment

        response, content = self._connection.call(
            self._url, data, 'POST')
        return response

    def discard(self):
        """Shortcut for moderate."""
        return self.moderate('discard')

    def reject(self, reason=None):
        """Shortcut for moderate.

        :param reason: An optional reason for rejecting the held message.
        """
        return self.moderate('reject', comment=reason)

    def defer(self):
        """Shortcut for moderate."""
        return self.moderate('defer')

    def accept(self):
        """Shortcut for moderate."""
        return self.moderate('accept')
