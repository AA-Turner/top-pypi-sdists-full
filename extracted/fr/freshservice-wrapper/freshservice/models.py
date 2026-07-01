# Copyright 2018 eGym GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Basic datastructures for the use of the Freshservice API.

Classes:
    FreshserviceModel - Base class for common operations
    Agent - Class for Helpdesk admins
    Asset - Class for CMDB items
    Task - Convenient representation of a Helpdesk task
    Ticket - Convenient representation of a Helpdesk ticket
    User - Class for users

"""
from .errors import BadInput, UnexpectedValue


class FreshserviceModel(object):

    """Base class for the FreshserviceAPI data model.

    All other model classes inherit this. It provides basic
    functionality to initialize class attributes and common methods.

    """

    def __init__(self, inner_dictionary_names, **kwargs):
        """Constructor of FreshserviceModel.

        This method sets the class attributes with the content of
        kwargs. Some attributes will be saved private, to make them
        accessible more conveniently via properties.

        Args:
            inner_dictionary_names (list): A list of names, which
                represent dictionaries in kwargs. Every dictionary in
                this list will be popped, so that kwargs doesn't contain
                to many inner dictionaries. As a result the models
                __dict__ will have less inner levels.
            kwargs (dict): It is expected, that a dictionary is used,
                which is obtained by parsing JSON, passed by the
                Freshservice API.

        """
        for k in inner_dictionary_names:
            if k in kwargs.keys() and len(kwargs[k]) > 0:
                kwargs.update(kwargs.pop(k))

        for k, v in kwargs.items():
            if hasattr(self.__class__, k):
                k = '_' + k
            setattr(self, k, v)

    def __str__(self):
        """This method only prints the content of its dictionary."""
        return str(self.__dict__)

    def __repr__(self):
        """Create object representation.

        With this you can create a duplicate of the object with eval.
        Note, that this is probably not the same code, that actually
        created this object.

        """
        representation = self.__class__.__name__ + '('
        not_first = False
        for k, v in self.__dict__.items():
            if not_first:
                representation += ', '
            not_first = True
            representation += k + ' = ' + repr(v)
        representation += ')'
        return representation


class Asset(FreshserviceModel):

    def __init__(self, custom_fields, **kwargs):
        super().__init__(
            inner_dictionary_names=[
                'item', 'config_item', 'levelfield_values'
            ],
            **kwargs)

        for key, value in custom_fields.items():
            long_name = '{}_{}'.format(key, value)
            setattr(self, key, getattr(self, long_name))
            delattr(self, long_name)


class Ticket(FreshserviceModel):

    """The ticket model.

    This class represents the ticket data model of Freshservice. It
    provides wrapper classes for better usability of the priority,
    status and source classes. Due to inconsistencies in the
    Freshservice API, it is currently only used for HTTP GET.
    """

    # Ticket source
    EMAIL = 1
    PORTAL = 2
    PHONE = 3
    CHAT = 4

    # Ticket status
    OPEN = 2
    PENDING = 3
    RESOLVED = 4
    CLOSED = 5

    # Ticket Priority
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4

    def __init__(self, custom_fields=None, api_postfix='', **kwargs):
        """Constructor of Ticket.

        This method calls the constructor of the FreshserviceModel. It
        also renames some attributes for ease of use.
        """
        if custom_fields is None:
            custom_fields = []

        super().__init__(['item', 'helpdesk_ticket', 'custom_field'], **kwargs)

        for field in custom_fields:
            setattr(self, field, getattr(self, field + api_postfix))
            delattr(self, field + api_postfix)

    @property
    def priority(self):
        """Return string representation of priority.

        This returns either 'low', 'medium', 'high', or 'urgent'. The
        API itself saves numeric values. Alternatively you may use the
        field 'priority_name'.
        """
        _p = {
            self.LOW: 'low',
            self.MEDIUM: 'medium',
            self.HIGH: 'high',
            self.URGENT: 'urgent'
        }
        try:
            return _p[self._priority]
        except KeyError:
            raise UnexpectedValue('Priority: {}'.format(self._priority))

    @priority.setter
    def priority(self, value):
        """Set priority with string representation.

        The setter expects one of the following values: 'low', 'medium',
        'high', 'urgent'
        """
        _p = {
            'low': self.LOW,
            'medium': self.MEDIUM,
            'high': self.HIGH,
            'urgent': self.URGENT
        }
        try:
            self._priority = _p[value]
        except KeyError:
            raise BadInput('Priority: {}.'.format(value))

    @property
    def status(self):
        """Return string representation of status.

        This returns either 'open', 'pending', 'resolved', or 'closed'.
        The API itself saves numeric values. Alternatively you may use
        the field 'status_name'.
        """
        _s = {
            self.OPEN: 'open',
            self.PENDING: 'pending',
            self.RESOLVED: 'resolved',
            self.CLOSED: 'closed'
        }
        try:
            return _s[self._status]
        except KeyError:
            raise UnexpectedValue('Status: {}'.format(self._status))

    @status.setter
    def status(self, value):
        """Set status with string representation.

        The setter expects one of the following values: 'open',
        'pending', 'resolved', or 'closed'
        """
        _s = {
            'open': self.OPEN,
            'pending': self.PENDING,
            'resolved': self.RESOLVED,
            'closed': self.CLOSED
        }
        try:
            self._status = _s[value]
        except KeyError:
            raise BadInput('Status: {}'.format(value))

    @property
    def source(self):
        """Return string representation of source.

        This returns either 'email', 'portal', 'phone', or 'chat'. The
        API itself saves numeric values. Alternatively you may use the
        field 'source_name'.
        """
        _s = {
            self.EMAIL: 'email',
            self.PORTAL: 'portal',
            self.PHONE: 'phone',
            self.CHAT: 'chat'
        }
        try:
            return _s[self._source]
        except KeyError:
            raise UnexpectedValue('Source: {}'.format(self._source))

    @source.setter
    def source(self, value):
        """Set source with string representation.

        The setter expects one of the following values: 'email',
        'portal', 'phone', 'chat'
        """
        _s = {
            'email': self.EMAIL,
            'portal': self.PORTAL,
            'phone': self.PHONE,
            'chat': self.CHAT
        }
        try:
            self._source = _s[value]
        except KeyError:
            raise BadInput('Source: {}'.format(value))


class Task(FreshserviceModel):

    """The task model.

    This is very similar to the ticket model, just a little simplified.
    Therefore most of the documentation also applies here.
    """

    # Task status
    OPEN = 1
    INPROGRESS = 2
    COMPLETED = 3

    def __init__(self, **kwargs):
        """Constructor for creating a Task object."""
        super().__init__(['item', 'it_task'], **kwargs)

    @property
    def status(self):
        """Get a string representation of the status."""
        _s = {
            self.OPEN: 'open',
            self.INPROGRESS: 'inprogress',
            self.COMPLETED: 'completed'
        }
        try:
            return _s[self._status]
        except KeyError:
            raise UnexpectedValue('Status: {}'.format(self._status))

    @status.setter
    def status(self, value):
        """Set the status with a string representation."""
        _s = {
            'open': self.OPEN,
            'inprogress': self.INPROGRESS,
            'completed': self.COMPLETED
        }
        try:
            self._status = _s[value]
        except KeyError:
            raise BadInput('Status: {}'.format(value))


class User(FreshserviceModel):

    def __init__(self, **kwargs):
        super().__init__(['user'], **kwargs)


class Agent(FreshserviceModel):

    def __init__(self, **kwargs):
        super().__init__(['agent'], **kwargs)
