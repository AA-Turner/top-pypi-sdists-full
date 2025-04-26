# Copyright 2021 StreamSets Inc.
"""Abstractions to interact with the Aster REST API."""

# fmt: off
import json
import logging

import requests
import urllib3
from requests.adapters import HTTPAdapter

from .exceptions import BadRequestError, InternalServerError, UnprocessableEntityError
from .utils import create_aster_envelope, get_params, join_url_parts, retry_on_connection_error

# fmt: off

logger = logging.getLogger(__name__)

# The `#:` constructs at the end of assignments are part of Sphinx's autodoc functionality.
DEFAULT_ASTER_API_VERSION = 3  #:

# Headers required to get an access token (after passing authentication_token to POST).
ACCESS_TOKEN_REQUIRED_HEADERS = {'content-Type': 'application/x-www-form-urlencoded', 'X-Requested-By': 'Aster'}

# Any headers that Aster requires for all calls should be added to this dictionary.
REQUIRED_HEADERS = {'X-Requested-By': 'Aster', 'X-SS-REST-CALL': 'true', 'content-type': 'application/json'}


class ApiClient(object):
    """
    API client to communicate with an Aster instance.
    Args:
        server_url (:obj:`str`): Aster instance's server URL.
        authentication_token (:obj:`str`, optional): Aster authentication_token. Default: ``None``
        sch_auth_token (:obj:`str`, optional): SCH API credential token. Default: ``None``
        sch_credential_id (:obj:`str`, optional): SCH API credential id. Default: ``None``
        api_version (:obj:`int`, optional): The API version.
            Default: :py:const:`aster_api.DEFAULT_ASTER_API_VERSION`
        session_attributes (:obj:`dict`, optional): A dictionary of attributes to set on the underlying
            :py:class:`requests.Session` instance at initialization. Default: ``None``
        headers (:obj:`dict`, optional): A dictionary of headers to with the :py:class:`requests.Session` instance.
            Default: ``None``
    """

    def __init__(
        self,
        server_url,
        authentication_token=None,
        sch_auth_token=None,
        sch_credential_id=None,
        api_version=DEFAULT_ASTER_API_VERSION,
        session_attributes=None,
        headers=None,
        **kwargs
    ):
        if not authentication_token and not (sch_auth_token and sch_credential_id):
            raise Exception(
                'Invalid authentication options provided. Either (sch_auth_token and sch_api_credential_id)'
                ' or authentication_token must be provided.'
            )
        self._base_url = server_url
        self._authentication_token = authentication_token
        self._sch_auth_token = sch_auth_token
        self._sch_credential_id = sch_credential_id
        self._api_version = api_version

        self._session = requests.Session()
        self._session.mount('http://', HTTPAdapter(pool_connections=1))
        self._session.mount('https://', HTTPAdapter(pool_connections=1))
        self._session.headers.update(REQUIRED_HEADERS)
        if headers:
            self._session.headers.update(headers)

        if session_attributes:
            for attribute, value in session_attributes.items():
                setattr(self._session, attribute, value)

        if not self._session.verify:
            # If we disable SSL cert verification, we should disable warnings about having disabled it.
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def login(self):
        """Login to Aster.

        This will set either the 'Authorization' header using an ASTER auth token, or the 'X-SS-App-Auth-Token' and
        'X-SS-App-Component-Id' headers using SCH API Credentials.
        """
        if self._sch_auth_token and self._sch_credential_id:
            self._session.headers['X-SS-App-Auth-Token'] = self._sch_auth_token
            self._session.headers['X-SS-App-Component-Id'] = self._sch_credential_id
        else:
            self._session.headers['Authorization'] = 'Bearer {}'.format(self._authentication_token)

    def logout(self):
        """Logout of Aster.
        Running this endpoint will remove the ``Authorization`` session header.
        """
        del self._session.headers['Authorization']

    def get_current_user(self):
        """
        Get currently logged-in user info
        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        response = self._get(app='security', endpoint='v{0}/user-info'.format(self._api_version))
        return Command(self, response)

    # Organization User Resources
    def get_admin_org_users(self, org, page=None, search=None, size=None, sort=None):
        """Get the users of an organization. This is only available for sys-admin.

        Args:
            org (:obj:`str`): Org ID
            page (:obj:`int`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            sort (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org'))
        response = self._get(
            app='security', endpoint='v{}/admin/orgs/{}/users'.format(self._api_version, org), params=params
        )
        return Command(self, response)

    def get_admin_org_user(self, org, user):
        """Get a user of an organization. This is only available for sys-admin.

        Args:
            org (:obj:`str`): Org ID
            user (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs/{}/users/{}'.format(self._api_version, org, user)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def update_admin_org_user(self, org, payload, user):
        """Update a user of an organization. This is only available for sys-admin.

        Args:
            org (:obj:`str`): Org ID
            payload (:obj:`dict`): data - that complies with Swagger definition.
            user (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs/{}/users/{}'.format(self._api_version, org, user)
        data = create_aster_envelope(payload)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def get_org_users(
        self,
        offset=None,
        page=None,
        size=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """Get the org-users.

        Args:
            offset (:obj:`int`, optional): Default: ``None``
            page (:obj:`int`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            paged (:obj:`str`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sort_sorted', 'sort_unsorted'))
        if sort_sorted is not None:
            params.update({'sort.sorted': sort_sorted})
        if sort_unsorted is not None:
            params.update({'sort.unsorted': sort_unsorted})
        response = self._get(app='security', endpoint='v{}/org-users'.format(self._api_version), params=params)
        return Command(self, response)

    def get_org_user(self, user_id):
        """Get the org-user for the given user ID.

        Args:
            user_id (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/org-users/{}'.format(self._api_version, user_id))
        return Command(self, response)

    def update_org_user(self, user_id, body):
        """Update an org user.

        Args:
            user_id (:obj:`str`): User ID
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users/{}'.format(self._api_version, user_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def delete_org_users(self, body):
        """Delete org user/s.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users.delete'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def delete_admin_org_users(self, org_id, body):
        """Delete org user/s.

        Args:
            org_id (:obj:`str`): Org ID.
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs/{}/users.delete'.format(self._api_version, org_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def activate_org_users(self, body):
        """Activate org user/s.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users.activate'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def deactivate_org_users(self, body):
        """Deactivate org user/s.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users.deactivate'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def invite_org_users(self, body):
        """Invite new user to join the org. An org admin can do this.

        Args:
            body (:obj:`dict`): Role and email - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users.invite'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def leave_org_users(self):
        """Leave org users.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/org-users.leave'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint)
        return Command(self, response)

    # Organization Resources
    def get_orgs(
        self,
        offset=None,
        page=None,
        size=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """Get the organizations.

        Args:
            offset (:obj:`int`, optional): Default: ``None``
            page (:obj:`int`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            paged (:obj:`str`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sort_sorted', 'sort_unsorted'))
        if sort_sorted is not None:
            params.update({'sort.sorted': sort_sorted})
        if sort_unsorted is not None:
            params.update({'sort.unsorted': sort_unsorted})
        response = self._get(app='security', endpoint='v{}/orgs'.format(self._api_version), params=params)
        return Command(self, response)

    def get_org(self, org_id):
        """Get the org for the given org ID.

        Args:
            org_id (:obj:`str`): Org ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/orgs/{}'.format(self._api_version, org_id))
        return Command(self, response)

    def update_org(self, org_id, body):
        """Update an org.

        Args:
            org_id (:obj:`str`): Org ID
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/orgs/{}'.format(self._api_version, org_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    # Organization Lookup Resource

    @classmethod
    def get_org_info(cls, org_id, server_url, verify=True):
        """Get org info.

        Args:
            org_id (:obj:`str`): Org ID
            server_url (:obj:`str`): ASTER instance's server URL
            verify (:obj:`bool` or :obj:`str`, optional): If bool, whether to verify SSL,
                                                          if a string, path of SSL certificate. Default: ``True``

        Returns:
            An instance of :py:class:`requests.models.Response`.
        """
        # Unlike most ASTER calls, getting org info requires no authentication. As such, while it's logically grouped
        # with other ASTER API-wrapping methods, it doesn't require the authentication token needed to create a typical
        # ApiClient, so we have implemented it as a class method.

        url = join_url_parts(
            server_url, '/api/security/public/v{}/orgs/{}/info'.format(DEFAULT_ASTER_API_VERSION, org_id)
        )
        response = requests.get(url, headers=REQUIRED_HEADERS, verify=verify)
        cls._handle_http_error(response)
        return response

    # User Resources
    def get_user(self, user_id):
        """Get the users.

        Args:
            user_id (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/users/{}'.format(self._api_version, user_id))
        return Command(self, response)

    def update_user(self, user_id, body):
        """Update an user.

        Args:
            user_id (:obj:`str`): User ID
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/users/{}'.format(self._api_version, user_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def accept_tos(self):
        """Accept TOS.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/users.accept-tos'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint)
        return Command(self, response)

    def create_org(self, body):
        """Create first org. after accepting TOS.

        Args:
            body (:obj:`dict`): Org name and zone - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/orgs'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    # Zone Resources
    def get_zones(self):
        """Get the zones.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/zones'.format(self._api_version))
        return Command(self, response)

    # Admin organization resources
    def activate_failure(self, body):
        """Activate failure.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/failure/activate'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def deactivate_failure(self):
        """Deactivate failure.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='/v{}/admin/failure/deactivate'.format(self._api_version))
        return Command(self, response)

    def get_admin_organizations(
        self,
        offset=None,
        page=None,
        size=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """Get all the organizations. This is only available for sys-admin.

        Args:
            offset (:obj:`int`, optional): Default: ``None``
            page (:obj:`int`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            paged (:obj:`str`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sort_sorted', 'sort_unsorted'))
        if sort_sorted is not None:
            params.update({'sort.sorted': sort_sorted})
        if sort_unsorted is not None:
            params.update({'sort.unsorted': sort_unsorted})
        response = self._get(app='security', endpoint='v{}/admin/orgs'.format(self._api_version), params=params)
        return Command(self, response)

    def get_admin_organization(self, org_id):
        """Get the organization. This is only available for sys-admin.

        Args:
            org_id (:obj:`str`): organization ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/admin/orgs/{}'.format(self._api_version, org_id))
        return Command(self, response)

    def create_admin_organization(self, body):
        """Create a new organization in a specific instance. This is only available for sys-admin.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def delete_admin_organizations(self, org_ids):
        """Delete the organizations. This is only available for sys-admin.

        Args:
            org_ids (:obj:`list`): the list of organization IDs to delete.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs.delete'.format(self._api_version)
        data = create_aster_envelope(org_ids)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def update_admin_organization(self, id, payload):
        """Update an organization. This is only available for sys-admin.

        Args:
            id (:obj:`str`): organization ID
            payload (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/orgs/{}'.format(self._api_version, id)
        data = create_aster_envelope(payload)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    # Admin instance Resources
    def get_admin_instances(
        self,
        offset=None,
        page=None,
        size=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """Get the admin instances.

        Args:
            offset (:obj:`int`, optional): Default: ``None``
            page (:obj:`int`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            paged (:obj:`str`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sort_sorted', 'sort_unsorted'))
        if sort_sorted is not None:
            params.update({'sort.sorted': sort_sorted})
        if sort_unsorted is not None:
            params.update({'sort.unsorted': sort_unsorted})
        response = self._get(app='security', endpoint='v{}/admin/instances'.format(self._api_version), params=params)
        return Command(self, response)

    def get_admin_instance(self, admin_instance_id):
        """Get an admin instance.

        Args:
            admin_instance_id (:obj:`str`): Admin instance ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(
            app='security', endpoint='v{}/admin/instances/{}'.format(self._api_version, admin_instance_id)
        )
        return Command(self, response)

    def create_admin_instance(self, body):
        """Create an admin instance.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/instances'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def update_admin_instance(self, admin_instance_id, body):
        """Update an admin instance.

        Args:
            admin_instance_id (:obj:`str`): Admin instance ID
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/instances/{}'.format(self._api_version, admin_instance_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def delete_admin_instances(self, admin_zone_ids):
        """Delete an admin instances.

        Args:
            admin_zone_ids (:obj:`str`): Admin instance IDs

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/instances.delete'.format(self._api_version)
        data = create_aster_envelope(admin_zone_ids)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    # Admin Zone Resources
    def get_admin_zones(
        self,
        offset=None,
        page=None,
        size=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """Get the admin zones.

        Args:
            offset (:obj:`int`, optional): Default: ``None``
            page (:obj:`int`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            paged (:obj:`str`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sort_sorted', 'sort_unsorted'))
        if sort_sorted is not None:
            params.update({'sort.sorted': sort_sorted})
        if sort_unsorted is not None:
            params.update({'sort.unsorted': sort_unsorted})
        response = self._get(app='security', endpoint='v{}/admin/zones'.format(self._api_version), params=params)
        return Command(self, response)

    def get_admin_zone(self, admin_zone_id):
        """Get an admin zone.

        Args:
            admin_zone_id (:obj:`str`): Admin zone ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._get(app='security', endpoint='v{}/admin/zones/{}'.format(self._api_version, admin_zone_id))
        return Command(self, response)

    def create_admin_zone(self, body):
        """Create an admin zone.

        Args:
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/zones'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def update_admin_zone(self, admin_zone_id, body):
        """Update an admin zone.

        Args:
            admin_zone_id (:obj:`str`): Admin zone ID
            body (:obj:`dict`): data - that complies with Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/zones/{}'.format(self._api_version, admin_zone_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def delete_admin_zones(self, admin_zone_ids):
        """Delete admin zones.

        Args:
            admin_zone_ids (:obj:`str`): Admin zone IDs

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = '/v{}/admin/zones.delete'.format(self._api_version)
        data = create_aster_envelope(admin_zone_ids)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    # Admin Users Resource
    def get_admin_users(self, page=None, search=None, size=None, sort=None):
        """Get admin users. This is only available for sys-admin.

        Args:
            page (:obj:`int`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            sort (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='security', endpoint='v{}/admin/users'.format(self._api_version), params=params)
        return Command(self, response)

    def get_admin_user(self, id):
        """Get admin users. This is only available for sys-admin.

        Args:
            id (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = 'v{}/admin/users/{}'.format(self._api_version, id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def get_all_migrations(self, page=None, search=None, size=None, sort=None):
        """Get the list of organization migrations.

        Args:
            page (:obj:`int`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            sort (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/admin/migrations'.format(self._api_version)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_migration_by_id(self, migration_id):
        """Get the migration details for the specified ID.

        Args:
             migration_id (:obj:`str`): migration ID.
        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/admin/migrations/{}'.format(self._api_version, migration_id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def get_migration_latest_events(self, migration_id):
        """Get the migration events for the specified ID.

        Args:
             migration_id (:obj:`str`): Migration ID.
        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/admin/migrations/{}/latestEvents'.format(self._api_version, migration_id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def migrate_organization(self, body):
        """Initiate a migration for the specified organization.

        Args:
            body (:obj:`dict`): data that complies with the Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/admin/migrations'.format(self._api_version)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def update_migration(self, migration_id, body):
        """Update a specific migration.

        Args:
            migration_id (:obj:`str`): Migration ID of the migration to be updated.
            body (:obj:`dict`): data that complies with the Swagger definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/admin/migrations/{}'.format(self._api_version, migration_id)
        data = create_aster_envelope(body)
        response = self._post(app='security', data=data, endpoint=endpoint)
        return Command(self, response)

    def cancel_migration(self, migration_id):
        """Cancel a migration.

        Args:
            migration_id (:obj:`str`): Migration ID of the migration to be cancelled.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/admin/migrations.cancel/{}'.format(self._api_version, migration_id)
        response = self._post(app='security', endpoint=endpoint)
        return Command(self, response)

    # Event logs related
    def get_event_log(
        self,
        app_name,
        offset=None,
        pageNumber=None,
        pageSize=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """
        Get event log for provided app

        Args:
            app_name (:obj:`str`): Name of the app e.g. security
            offset (:obj:`int`, optional): Default: ``None``
            pageNumber (:obj:`int`, optional): Default: ``None``
            pageSize (:obj:`str`, optional): Default: ``None``
            paged (:obj:`bool`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'app_name', 'sort_sorted', sort_unsorted))
        params.update({'sort.sorted': sort_sorted, 'sort.unsorted': sort_unsorted})
        response = self._get(app=app_name, endpoint='v{0}/eventlog'.format(self._api_version), params=params)
        return Command(self, response)

    def get_event_log_for_an_event(
        self,
        app_name,
        event_id,
        offset=None,
        pageNumber=None,
        pageSize=None,
        paged=None,
        search=None,
        sort_sorted=None,
        sort_unsorted=None,
        unpaged=None,
    ):
        """
        Get event log for provided app for an event with passed id

        Args:
            app_name (:obj:`str`): Name of the app e.g. security
            event_id (:obj:`str`): ID of the event
            offset (:obj:`int`, optional): Default: ``None``
            pageNumber (:obj:`int`, optional): Default: ``None``
            pageSize (:obj:`str`, optional): Default: ``None``
            paged (:obj:`bool`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            sort_sorted (:obj:`bool`, optional): Default: ``None``
            sort_unsorted (:obj:`bool`, optional): Default: ``None``
            unpaged (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(
            parameters=locals(), exclusions=('self', 'event_id', 'app_name', 'sort_sorted', sort_unsorted)
        )
        params.update({'sort.sorted': sort_sorted, 'sort.unsorted': sort_unsorted})
        response = self._get(
            app=app_name, endpoint='v{}/eventlog/{}'.format(self._api_version, event_id), params=params
        )
        return Command(self, response)

    def return_all_releases(self):
        """
        Get all releases. e.g. SDC or Transformer

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        response = self._get(
            app='entitlements', endpoint='v{0}/releases'.format(self._api_version), params={'verify': True}
        )
        return Command(self, response)

    def get_distribution(self, distribution_key, platform):
        """
        Get distribution. e.g. SDC or Transformer

        Args:
            distribution_key (:obj:`str`): Distribution key of the downloadable entity
            platform (:obj:`str`): Platform to download for

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'distribution_key', 'platform'))
        params.update({'distributionKey': distribution_key, 'platform': platform})
        response = self._get(
            app='entitlements', endpoint='v{}/releases/{}'.format(self._api_version, distribution_key), params=params
        )
        return Command(self, response)

    def get_saml_configuration(self, draft, org=None):
        """Get the SAML configuration resource.

        Args:
            draft (:obj:`bool`): Whether this is a draft or not.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='security', endpoint='v{}/saml'.format(self._api_version), params=params)
        return Command(self, response)

    def create_saml_configuration(self, payload, org=None):
        """Create the SAML configuration resource.

        Args:
            payload (:obj:`dict`): data - that complies with Swagger definition.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'payload'))
        endpoint = 'v{}/saml'.format(self._api_version)
        data = create_aster_envelope(payload)
        response = self._post(app='security', endpoint=endpoint, params=params, data=data)
        return Command(self, response)

    def copy_saml_configuration_to_production(self, org=None):
        """Copy the SAML configuration resource to production.

        Args:
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml.copy-to-production'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def delete_saml_configuration(self, org=None):
        """Delete the SAML configuration resource.

        Args:
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml.delete'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def disable_saml_configuration(self, org=None):
        """Disable the SAML configuration resource.

        Args:
            org (:obj:`str`): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml.disable'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def enable_saml_configuration(self, org=None):
        """Enable the SAML configuration resource.

        Args:
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml.enable'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def reset_saml_draft_configuration(self, org=None):
        """Reset the SAML draft configuration resource.

        Args:
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml.reset-draft'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def update_saml_configuration(self, payload, org=None):
        """Update the SAML configuration resource.

        Args:
            payload (:obj:`dict`): data - that complies with Swagger definition.
            org (:obj:`str`, optional): Organization id. Default: ``None``
        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'payload'))
        endpoint = 'v{}/saml.update'.format(self._api_version)
        data = create_aster_envelope(payload)
        response = self._post(app='security', endpoint=endpoint, data=data, params=params)
        return Command(self, response)

    def update_saml_configuration_with_idp_metadata(self, idp_metadata_xml, org=None):
        """Update the SAML configuration resource with idp metadata.

        Args:
            idp_metadata_xml (:obj:`dict`): idp metadata - that complies with Swagger definition.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'idp_metadata_xml'))
        endpoint = 'v{}/saml.update-with-idp-metadata'.format(self._api_version)
        data = create_aster_envelope(idp_metadata_xml)
        response = self._post(app='security', endpoint=endpoint, data=data, params=params)
        return Command(self, response)

    def create_saml_certificate(self, days_valid, key_len, org=None):
        """Create a SAML certificate.

        Args:
            days_valid (:obj:`int`): The number of days the certificate should be valid.
            key_len (:obj:`str`): The length of the key. Acceptable values are 'K2048', 'K3072', 'K4096'.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml/certificate'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def delete_saml_certificate(self, serial_number, org=None):
        """Delete a SAML certificate.

        Args:
            serial_number (:obj:`str`): The serial number of the certificate.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/saml/certificate.delete'.format(self._api_version)
        response = self._post(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_saml_metadata(self, draft, org=None):
        """Get the SAML configuration resource.

        Args:
            draft (:obj:`bool`): Whether this is a draft or not.
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        endpoint = 'v{}/saml/metadata'.format(self._api_version)
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_saml_login_url(self, draft=False, org=None):
        """Get the SAML login URL.

        Args:
            draft (:obj:`bool`, optional): Default: ``False``
            org (:obj:`str`, optional): Organization id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saml/login-url'.format(self._api_version)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def trigger_saml_automated_task(self):
        """Trigger the automated task that generates banners for expiring SAML certificates.
           Call can only be made by Sys-Admins.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        response = self._post(
            app='security',
            endpoint='/v{}/admin/task/saml-cert.trigger'.format(self._api_version)
        )
        return Command(self, response)

    def get_all_subscriptions(self, page=None, search=None, size=None, sort=None):
        """Get the list of all subscriptions. Available to SYS-ADMINS.

        Args:
            page (:obj:`int`, optional): Default: ``None``
            search (:obj:`str`, optional): Default: ``None``
            size (:obj:`int`, optional): Default: ``None``
            sort (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = 'v{}/admin/subscriptions'.format(self._api_version)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_subscription_by_id(self, subscription_id):
        """Get a subscription by ID. Available to SYS-ADMINS.

        Args:
            subscription_id (:py:obj:`str`): The ID of the subscription to get.

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`.
        """
        endpoint = 'v{}/admin/subscriptions/{}'.format(self._api_version, subscription_id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    @retry_on_connection_error
    def _delete(self, app, endpoint, params=None):
        url = join_url_parts(self._base_url, '/api/{}'.format(app), endpoint)
        response = self._session.delete(url, params=params or {})
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _get(self, app, endpoint, params=None):
        url = join_url_parts(self._base_url, '/api/{}'.format(app), endpoint)
        response = self._session.get(url, params=params or {})
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _post(self, app, endpoint, params=None, data=None, files=None, headers=None):
        url = join_url_parts(self._base_url, '/api/{}'.format(app), endpoint)
        if data and not isinstance(data, str):
            data = json.dumps(data or {})

        response = self._session.post(url, params=params or {}, data=data, files=files, headers=headers)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _put(self, app, endpoint, params=None, data=None):
        url = join_url_parts(self._base_url, '/api/{}'.format(app), endpoint)
        body = {'data': (data or {})}
        response = self._session.put(url, params=params or {}, data=json.dumps(body))
        self._handle_http_error(response)
        return response

    @staticmethod
    def _handle_http_error(response):
        """Specific error handling for Aster, to make better error reporting where applicable."""
        if response.status_code == 500:
            raise InternalServerError(response)
        elif response.status_code == 422:
            raise UnprocessableEntityError(response)
        elif response.status_code == 400:
            raise BadRequestError(response)
        # Delegating to response object error handling as last resort.
        response.raise_for_status()


class Command:
    """Command to allow users to interact with commands submitted through Aster REST API.
    Args:
        api_client (:py:class:`streamsets.sdk.aster_api.ApiClient`): Aster API client.
        response (:py:class:`requests.Response`): Command response.
    """

    def __init__(self, api_client, response):
        self.api_client = api_client
        self.response = response
