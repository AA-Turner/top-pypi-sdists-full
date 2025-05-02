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

"""Wrapper for the Freshservice API.

Classes:
    API - Wrapper for basic FreshserviceAPI access via HTTP messages
    AgentAPI - Wrapper for Helpdesk administrators
    AssetAPI - Wrapper for CMDB items
    TaskAPI - Wrapper for Helpdesk tasks
    TicketAPI - Wrapper for Helpdesk tickets
    UserAPI - Wrapper for Helpdesk customers

"""
import logging

from requests import Request, Session

from .models import Asset, Ticket, Task, User, Agent
from .errors import (ResponseError,
                     AuthenticationFailed,
                     UserSearchFailed,
                     AgentSearchFailed)


class AssetAPI(object):

    """API for handling CMDB assets.

    An important note about the asset_type data structure: The
    custom_fields attribute wont be initialized right away. Doing so
    would require one API call for each asset type, which is a waste of
    ressources in general (because you can't assume that every asset
    type will actually be used). Instead the field will be initialized
    with None and will be loaded on request.
    """

    def __init__(self, api):
        self._api = api
        self._prefix = 'cmdb/'

        self._asset_types = self.get_asset_types()
        self.asset_types = {}

        for asset_type in self._asset_types:
            self.asset_types[asset_type['label']] = {
                'id': asset_type['id'],
                'custom_fields': None
            }

    def get_asset_types(self):
        """Returns a list of all asset types."""
        return self._api.get(self._prefix + 'ci_types.json')

    def get_custom_fields(self, type_id):
        """Return all domain specific fields for given asset type.

        The returned list consists of dictionaries with the name and ID
        of every custom field.
        """
        url = self._prefix + 'ci_types/{}.json'.format(type_id)
        custom_fields_raw = self._api.get(url)
        custom_fields = {}

        for field in custom_fields_raw:
            short_name = field['name'].strip('_{}'.format(field['ci_type_id']))
            custom_fields[short_name] = field['ci_type_id']

        return custom_fields

    def _load_custom_fields(self, asset_name):
        """Returns list of custom fields for given asset dictionary.

        First checks if the custom_fields are cached. If not, download
        the information and save it in a local data structure to prevent
        future API calls. Then return the list.
        """
        asset_type = self.asset_types[asset_name]

        if asset_type['custom_fields'] is None:
            custom_fields = self.get_custom_fields(asset_type['id'])
            self.asset_types[asset_name]['custom_fields'] = custom_fields

        return self.asset_types[asset_name]['custom_fields']

    def get(self, asset_id):
        """Return Asset object with given ID."""
        url = '{}items/{}.json'.format(self._prefix, asset_id)

        asset = self._api.get(url)
        asset_name = asset['config_item']['ci_type_name']
        custom_fields = self._load_custom_fields(asset_name)

        return Asset(custom_fields, **asset)

    def get_all(self, page_limit=200):
        """Return a list of all assets in the CMDB.

        The download will take a while and requires a lot of API calls,
        so please use the search function whenever possible. If you
        really need all assets, please save the result for later use.
        One page contains 50 asset objects.

        Keyword args:
            page_limit: Limits the number of pages, which will be downloaded.
                        This was added for safety reasons.
        """
        url = self._prefix + 'items.json?page={}'
        assets_raw = []
        assets = []
        page_number = 1

        while True:
            if page_number >= page_limit:
                logging.info('Reached page limit. Stopping download')
                logging.info('Downloaded %d pages of Asset information',
                             page_number - 1)
                break

            logging.debug('Downloading page %d', page_number)
            page = self._api.get(url.format(page_number))
            if not page:
                logging.debug('Page %d was empty.', page_number)
                logging.info('Downloaded %d pages of Asset information',
                             page_number - 1)
                break
            assets_raw += page
            page_number += 1

        for asset in assets_raw:
            custom_fields = self._load_custom_fields(asset['ci_type_name'])
            assets.append(Asset(custom_fields, **asset))

        return assets

    def search(self, field, value):
        """Returns a list of assets which match the search parameters.

        Args:
            field: The attribute that identifies the assets which are searched
                   for. Possible values are: 'name', 'asset_tag' and
                   'serial_number'. Note that a search for the 'name'
                   attribute will return all items with a name, that includes
                   the given value, not just those which match the name
                   exactly.
            value: The value that the field should have.
        """
        url = self._prefix + 'items/list.json?field={}&q={}'.format(field,
                                                                    value)
        assets_raw = self._api.get(url)
        assets = []
        for asset in assets_raw['config_items']:
            custom_fields = self._load_custom_fields(asset['ci_type_name'])
            assets.append(Asset(custom_fields, **asset))
        return assets

    def update(self, asset_id, **kwargs):
        """Use this function with care, it might overwrite data."""
        # get asset config
        asset = self.get(asset_id)
        custom_fields = self._load_custom_fields(asset.ci_type_name)
        if 'name' not in kwargs.keys():
            kwargs['name'] = asset.name

        # rename custom fields
        delete_after = []
        kwargs['level_field_attributes'] = {}
        for key, value in kwargs.items():
            if key in custom_fields.keys():
                new_name = '{}_{}'.format(key, custom_fields[key])
                kwargs['level_field_attributes'][new_name] = value
                delete_after.append(key)
        for key in delete_after:
            del kwargs[key]

        url = self._prefix + '/items/{}.json'.format(asset_id)
        asset = self._api.put(url, data={'cmdb_config_item': kwargs})
        return Asset(custom_fields, **asset)


class TicketAPI(object):

    """API for handling Tickets."""

    def __init__(self, api):
        self._api = api
        self._tickets_prefix = 'helpdesk/tickets'

        self.api_postfix = ''
        self.custom_fields = []

        ticket_fields = self.get_ticket_fields()
        for field in ticket_fields:
            field = field['ticket_field']
            if field['default'] is True:
                continue
            name = field['name'].split('_')
            self.api_postfix = '_' + name[len(name) - 1]
            short_name = field['name'].replace(self.api_postfix, '')
            self.custom_fields.append(short_name)

    def get_ticket_fields(self):
        """Used for getting domain specific ticket fields."""
        return self._api.get('ticket_fields.json')

    def get_ticket(self, ticket_id):
        """Return ticket object with given id."""
        url = self._tickets_prefix + '/{}.json'.format(ticket_id)
        ticket = self._api.get(url)
        return Ticket(self.custom_fields, self.api_postfix, **ticket)

    def create_ticket(self, subject, email, **kwargs):
        """Create a ticket.

        due_by must be passed in ISO 8601 format and may not
        be older than the current datetime.

        Args:
            subject: The subject and title of the ticket.
            email: The email address of the requester.
            kwargs: Any other fields can be passed as <key>=<value>
                pairs. Please refer to the Freshservice API
                documentation to see, which fields and values are legit.
                You can also compare with the content of any ticket.json
                file. Note, that the fields "status", "priority" and
                "source" use numeric values.
                They are defined in models.py.

        """
        url = self._tickets_prefix + '.json'

        data = self.create_freshservice_dict(kwargs)
        data['helpdesk_ticket']['email'] = email
        data['helpdesk_ticket']['subject'] = subject

        ticket = self._api.post(url, data)
        return Ticket(self.custom_fields, self.api_postfix, **ticket)

    def update_ticket(self, ticket_id, **kwargs):
        """Update a ticket.

        This function does not return a ticket object, because
        the JSON, which is returned by the API is not compliant
        with standard JSON format for Tickets.

        This method works the same as create_ticket, except that you are
        overwriting fields of an already existing ticket.

        Please note that it is not possible to update the description of a
        ticket.

        There is an update specific quirk, that you need to set
        manual_due_by to true, before you can update the due date.

        """
        url = self._tickets_prefix + '/{}.json'.format(ticket_id)
        data = self.create_freshservice_dict(kwargs)
        self._api.put(url, data)

    def create_freshservice_dict(self, kwargs):
        """Create data object for creating and updating tickets.

        The Freshservice API has some weird quirks, some of which are
        not even documented and can only be found in forums. This method
        is handling these special cases.
        """
        data = {'helpdesk_ticket': {}}

        if 'tags' in kwargs:
            data['helpdesk'] = {}
            data['helpdesk']['tags'] = ','.join(kwargs['tags'])
            del kwargs['tags']

        if 'cc_email' in kwargs:
            data['cc_emails'] = ','.join(kwargs['cc_email'])
            del kwargs['cc_email']

        if 'reply_cc' in kwargs:
            data['reply_cc'] = kwargs['reply_cc']
            del kwargs['reply_cc']

        data['helpdesk_ticket']['manual_dueby'] = True
        if 'due_by' in kwargs:
            data['helpdesk_ticket']['frDueBy'] = kwargs['due_by']

        data, kwargs = self.rename_custom_fields(data, kwargs)
        data['helpdesk_ticket'].update(kwargs)
        return data

    def rename_custom_fields(self, data, kwargs):
        """Automatically pack custom fields to make the interface simpler."""
        custom_fields = {}
        delete_after = []
        for field in kwargs.keys():
            if field in self.custom_fields:
                custom_fields[field + self.api_postfix] = kwargs[field]
                delete_after.append(field)
        for field in delete_after:
            del kwargs[field]

        data['helpdesk_ticket']['custom_field'] = custom_fields
        return data, kwargs

    def delete_ticket(self, ticket_id):
        """Delete a ticket."""
        url = self._tickets_prefix + '/{}.json'.format(ticket_id)
        self._api.delete(url)

    def get_ticket_list_by_view(self, view_id):
        """Get a list of tickets, predefined by a view.

        Args:
            view_id: To find the view_id, select a view in Helpdesk and
                     you will see the ID in the last part of the URL.
        """
        url = self._tickets_prefix + '/view/{}?format=json'.format(view_id)
        raw_list = self._api.get(url)
        ticket_list = []
        for ticket in raw_list:
            ticket_list.append(
                Ticket(self.custom_fields, self.api_postfix, **ticket))
        return ticket_list

    def add_note(self, ticket_id, description, public=False):
        """Add a note to the ticket conversation."""
        url = self._tickets_prefix + \
            '/{}/conversations/note.json'.format(ticket_id)
        data = {'helpdesk_note': {'body_html': description}}
        if public:
            data['helpdesk_note']['private'] = False
        self._api.post(url, data)


class TaskAPI(object):

    """Wrapper for Helpdesk tasks.

    Freshservice uniquely identifies a Task with the fields "ticket_id"
    and "id" in JSON. Tasks can be used for various modules in
    Freshservice, Helpdesk tickets are the most common use case.
    """

    def __init__(self, api, module='tickets'):
        """Constructor of TaskAPI.

        Args:
            api: An instance of API
            module(optional): May be one of: 'tickets', 'problems',
                              'changes', 'releases'.

        """
        self._api = api
        self._task_prefix = 'itil/{}/'.format(module)

    def create_task(self, title, description, item_id, **kwargs):
        """Create a task.

        Args:
            title: The title of the task
            description: The description in plain text, HTML is not supported.
            item_id: The "owner" of the ticket, for example the ID of a ticket.
        """
        url = self._task_prefix + '{}/it_tasks.json'.format(item_id)
        data = {'title': title, 'description': description}
        data.update(kwargs)
        task = self._api.post(url, {'it_task': data})
        return Task(**task)

    def update_task(self, item_id, task_id, **kwargs):
        """Update a task."""
        url = self._task_prefix + \
            '{}/it_tasks/{}.json'.format(item_id, task_id)
        self._api.put(url, data={'it_task': kwargs})

    def get_task(self, item_id, task_id):
        """Get a task."""
        url = self._task_prefix + \
            '{}/it_tasks/{}.json'.format(item_id, task_id)
        task = self._api.get(url)
        return Task(**task)

    def get_all_tasks(self, item_id):
        """Get all tasks for a given item ID.

        Returns a list of Tasks.
        """
        url = self._task_prefix + '{}/it_tasks.json'.format(item_id)
        task_list = self._api.get(url)
        tasks = []
        for task in task_list:
            tasks.append(Task(**task))
        return tasks

    def delete_task(self, item_id, task_id):
        """Delete a task."""
        url = self._task_prefix + \
            '{}/it_tasks/{}.json'.format(item_id, task_id)
        self._api.delete(url)


class UserAPI(object):

    """Very basic access to user information"""

    def __init__(self, api):
        self._api = api

    def search(self, email):
        """Returns user with given email

        Note that agents are not considered to be users and cannot be
        searched with this API.

        Raises:
            UserSearchFailed: Will be raised, if the user doesn't exist, or
                              the API returns multiple objects for the same
                              email.
        """
        url = 'itil/requesters.json?query=email%20is%20{}'.format(email)
        user = self._api.get(url)
        if len(user) != 1:
            raise UserSearchFailed
        return User(**user[0])

    def delete(self, user_id):
        """Delete a user"""
        url = 'itil/requesters/{}.json'.format(user_id)
        self._api.delete(url)


class AgentAPI(object):

    """Very basic access to Freshservice admin information"""

    def __init__(self, api):
        self._api = api

    def search(self, email):
        """Returns agent with given email

        Raises:
            AgentSearchFailed: Will be raised, if the user doesn't exist, or
                               the API returns multiple objects for the same
                               email.
        """
        url = 'agents.json?query=email%20is%20{}'.format(email)
        agent = self._api.get(url)
        if len(agent) != 1:
            raise AgentSearchFailed
        return Agent(**agent[0])


class API(object):

    """Freshservice API wrapper.

    For the most part, this is a wrapper for HTTP calls to Freshservice.
    For each required HTTP function there is a method, which basically
    creates the URL string and then calls _action with the function name.

    It also saves the API key to make authentication possible. Cookies
    will always be cleared, because the API instantly resets every
    session.

    """

    def __init__(self, api_key, domain):
        """Creates an object of API

        Args:
            api_key: The API key of an agent with sufficient rights.
            domain: The name of your Freshservice instance.
                    Example: If the URL of your instance is
                    https://domain.freshservice.com, you should pass 'domain'.

        """

        self._api_prefix = 'https://{}.freshservice.com/'.format(domain)
        self._session = Session()
        self._session.auth = (api_key, '')
        self._session.headers = {
            'Content-Type': 'application/json',
            'Connection': 'close'
        }

        # debug variables
        self.response = None
        self.request = None

    def _action(self, req):
        """Prepare and send the request, then handle errors.

        This method is used all accross this module. It provides
        functionality that all HTTP methods need. After making an API
        call, it will analyze the JSON response, look for errors and
        throw an exception if necessary.

        Raises:
            AuthenticationFailed: The API object was initialized with an
                                  invalid API key, or the associated agent
                                  does not have sufficient rights.
            ResponseError : Response is not in JSON format, or contains the
                           'error'/'errors' field.
        """
        self._session.cookies.clear()
        self.request = self._session.prepare_request(req)

        resp = self._session.send(self.request)
        try:
            j = resp.json()
            self.response = j
        except Exception:
            self.response = None
            raise ResponseError(self.request, self.response)

        if 'error' in j or 'errors' in j:
            raise ResponseError(self.request, self.response)

        if 'require_login' in j:
            raise AuthenticationFailed

        try:
            resp.raise_for_status()
        except Exception:
            raise ResponseError(self.request, self.response)

        return j

    def get(self, url):
        """Wrapper around request.get().

        Returns a dictionary with the parsed response.
        """
        req = Request('GET', self._api_prefix + url)
        return self._action(req)

    def post(self, url, data=None):
        """Wrapper around request.post().

        Returns a dictionary with the parsed response.
        """
        if data is None:
            data = {}
        req = Request('POST', self._api_prefix + url, json=data)
        return self._action(req)

    def put(self, url, data=None):
        """Wrapper around request.put().

        Returns a dictionary with the parsed response.
        """
        if data is None:
            data = {}
        req = Request('PUT', self._api_prefix + url, json=data)
        return self._action(req)

    def delete(self, url):
        """Wrapper around request.delete().

        Returns a dictionary with the parsed response.
        """
        req = Request('DELETE', self._api_prefix + url)
        return self._action(req)
