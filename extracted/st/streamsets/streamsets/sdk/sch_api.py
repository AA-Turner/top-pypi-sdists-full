# Copyright 2021 StreamSets Inc.

"""Abstractions to interact with the ControlHub REST API."""

# fmt: off
import base64
import calendar
import enum
import io
import json
import logging
import re
from time import gmtime, sleep, time
from urllib.parse import quote_plus, urlparse

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError

from . import aster_api, st_models
from .__version__ import __version__
from .analytics import FUNCTION_CALLS_HEADERS_KEY, INTERACTIVE_MODE_HEADERS_KEY, AnalyticsHeaders
from .constants import STATUS_ERRORS
from .exceptions import (
    ConnectionError, InvalidCredentialsError, JobInactiveError, JobRunnerError, LegacyDeploymentInactiveError,
    MultipleIssuesError,
)
from .utils import (
    SDC_DEFAULT_EXECUTION_MODE, get_decoded_jwt, get_params, join_url_parts, retry_on_connection_error,
    wait_and_retry_on_http_error, wait_for_condition,
)

# fmt: on

logger = logging.getLogger(__name__)

# The `#:` constructs at the end of assignments are part of Sphinx's autodoc functionality.
DEFAULT_BANNER_API_VERSION = 1  #:
DEFAULT_EXPLORER_API_VERSION = 1
DEFAULT_SCH_API_VERSION = 1  #:
DEFAULT_SDP_API_VERSION = 2  #:
DEFAULT_METERING_API_VERSION = 3  #:
DEFAULT_JOBRUNNER2_API_VERSION = 3  #:

DEFAULT_ASTER_URL = 'https://cloud.login.streamsets.com/'
# Any headers that DPM requires for all calls should be added to this dictionary.
REQUIRED_HEADERS = {
    'X-Requested-By': 'sch',
    'X-SS-Sdk-Version': 'SDK {}'.format(__version__),
    'X-SS-REST-CALL': 'true',
    'content-type': 'application/json',
    FUNCTION_CALLS_HEADERS_KEY: None,
    INTERACTIVE_MODE_HEADERS_KEY: None,
}


# Headers accepted by get_metering_daily_report_by_content endpoint.
class MeteringDailyReportContentTypes(enum.Enum):
    TEXT_CSV = 'text/csv'
    APPLICATION_JSON = 'application/json'
    REPORT_JSON = 'report/json'


class ApiClient(object):
    """
    API client to communicate with a ControlHub instance.

    Args:
        component_id (:obj:`str`): Control Hub component ID.
        auth_token (:obj:`str`): Control Hub auth token.
        api_version (:obj:`int`, optional): The DPM API version. Default: :py:const:`DEFAULT_DPM_API_VERSION`
        session_attributes (:obj:`dict`, optional): A dictionary of attributes to set on the underlying
            :py:class:`requests.Session` instance at initialization. Default: ``None``
    """

    # pylint: disable=R0913
    def __init__(
        self,
        component_id,
        auth_token,
        api_version=DEFAULT_SCH_API_VERSION,
        banner_api_version=DEFAULT_BANNER_API_VERSION,
        sdp_api_version=DEFAULT_SDP_API_VERSION,
        metering_api_version=DEFAULT_METERING_API_VERSION,
        explorer_api_version=DEFAULT_EXPLORER_API_VERSION,
        session_attributes=None,
        **kwargs,
    ):
        self.component_id = component_id
        self.auth_token = auth_token
        self.api_version = api_version
        self.banner_api_version = banner_api_version
        self.sdp_api_version = sdp_api_version
        self.metering_api_version = metering_api_version
        self.explorer_api_version = explorer_api_version

        try:
            # Query ASTER with the org ID to determine the SCH instance URL.
            org_id = get_decoded_jwt(self.auth_token)['o']
            if org_id == 'admin':
                if kwargs.get('landing_url') is not None:
                    parsed_url = urlparse(kwargs.get('landing_url'))
                else:
                    raise ValueError('Sys-admin must supply landing_url when instantiating SCH')
            else:
                r = aster_api.ApiClient.get_org_info(
                    org_id=org_id,
                    server_url=kwargs.get('aster_url') or DEFAULT_ASTER_URL,
                    verify=session_attributes.get('verify', True),
                )
                parsed_url = urlparse(r.json()['data']['landingUrl'])
            self.base_url = '{}://{}'.format(parsed_url.scheme, parsed_url.netloc)
        except Exception as e:
            raise ValueError('Encountered error while decoding auth token: {}'.format(e))

        self.session = requests.Session()
        self.session.mount('http://', HTTPAdapter(pool_connections=1))
        self.session.mount('https://', HTTPAdapter(pool_connections=1))

        self.session.headers.update(
            {'X-SS-App-Component-Id': self.component_id, 'X-SS-App-Auth-Token': self.auth_token, 'X-SS-Org-Id': org_id}
        )
        self.session.headers.update(REQUIRED_HEADERS)
        if session_attributes:
            for attribute, value in session_attributes.items():
                setattr(self.session, attribute, value)

        if not self.session.verify:
            # If we disable SSL cert verification, we should disable warnings about having disabled it.
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def update_session_headers_with_analytics_data(self):
        analytics_instance = AnalyticsHeaders.get_instance()
        self.session.headers.update(analytics_instance.headers)
        analytics_instance.reset_headers()

    def get_available_add_ons(self):
        """Get lists of available and unavailable add-ons.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='security', endpoint='/v{}/currentUser/availableAddOns'.format(self.api_version))
        return Command(self, response)

    def get_current_user(self):
        """Get current user.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='security', endpoint='/v{}/currentUser'.format(self.api_version))
        return Command(self, response)

    def get_component_types(self):
        """Returns component types.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='security', endpoint='/v{}/componentTypes'.format(self.api_version))
        return Command(self, response)

    def get_components(
        self, org_id, component_type_id, offset, len, order_by='LAST_VALIDATED_ON', order='ASC', with_wrapper=False
    ):
        """Get all registered components for given Organization ID.

        Args:
            org_id (:obj:`str`)
            component_type_id (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``'LAST_VALIDATED_ON'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._get(
            app='security', endpoint='/v{}/organization/{}/components'.format(self.api_version, org_id), params=params
        )
        return Command(self, response)

    def create_components(self, org_id, component_type, number_of_components, active=True):
        """Create components for given organization ID.

        Args:
            org_id (:obj:`str`): Organization ID.
            component_type (:obj:`str`)
            number_of_components (:obj:`int`)
            active (:obj:`bool`, optional): Whether component is active. Default: ``True``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # pylint: disable=unused-argument

        # We call get_params using local(), so we define a local variable called `organization` to make sure
        # it ends up in the data dictionary we generate.
        organization = org_id  # pylint: disable=unused-variable

        data = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._put(
            app='security', endpoint='/v{}/organization/{}/components'.format(self.api_version, org_id), data=data
        )
        return CreateComponentsCommand(self, response)

    def activate_components(self, org_id, components_json):
        """Activate Components for all given Component IDs.

        Args:
            org_id (:obj:`str`): Organization ID.
            components_json (:obj:`str`): Components in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='security',
            endpoint='/v{}/organization/{}/components/activate'.format(self.api_version, org_id),
            data=components_json,
        )
        return Command(self, response)

    def deactivate_components(self, org_id, components_json):
        """Deactivate Components for all given Component IDs.

        Args:
            org_id (:obj:`str`): Organization ID.
            components_json (:obj:`str`): Components in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='security',
            endpoint='/v{}/organization/{}/components/deactivate'.format(self.api_version, org_id),
            data=components_json,
        )
        return Command(self, response)

    def delete_components(self, org_id, components_json):
        """Delete Components for all given list of components IDs.

        Args:
            org_id (:obj:`str`): Organization ID.
            components_json (:obj:`str`): Components in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='security',
            endpoint='/v{}/organization/{}/components/delete'.format(self.api_version, org_id),
            data=components_json,
        )
        return Command(self, response)

    def get_all_login_audits(
        self, org_id, offset=None, len_=None, sort_field=None, sort_order=None, start_time=0, end_time=-1
    ):
        """Get all login audits between a time frame.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``None``
            sort_order (:obj:`str`, optional): Default: ``None``
            start_time (:obj:`long`, optional): Default: ``0``
            end_time (:obj:`long`, optional): Default: ``-1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))

        endpoint = '/v{}/metrics/{}/loginAudits'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_action_audits(
        self, org_id, offset=None, len_=None, sort_field=None, sort_order=None, start_time=0, end_time=-1
    ):
        """Get all action audits between a time frame.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``None``
            sort_order (:obj:`str`, optional): Default: ``None``
            start_time (:obj:`long`, optional): Default: ``0``
            end_time (:obj:`long`, optional): Default: ``-1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))

        endpoint = '/v{}/metrics/{}/actionAudits'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_organization(self, body):
        """Create a new organization.

        Args:
            body (:obj:`str`): Organization in JSON format. Complies to Swagger NewOrganizationJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='security', endpoint='/v{}/organizations'.format(self.api_version), data=body)
        return Command(self, response)

    def update_organization(self, org_id, body):
        response = self._post(
            app='security', endpoint='/v{}/organization/{}'.format(self.api_version, org_id), data=body
        )
        return Command(self, response)

    def get_all_organizations(
        self, offset=None, len=None, orderBy='ID', order='ASC', active=None, filterText=None, with_wrapper=False
    ):
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='security', endpoint='/v{}/organizations'.format(self.api_version), params=params)
        return Command(self, response)

    def get_organization_configuration(self, org_id):
        response = self._get(app='security', endpoint='/v{}/organization/{}/configs'.format(self.api_version, org_id))
        return Command(self, response)

    def update_organization_configuration(self, org_id, body):
        response = self._post(
            app='security', endpoint='/v{}/organization/{}/configs'.format(self.api_version, org_id), data=body
        )
        return Command(self, response)

    def get_organization_configuration_v2(self, org_id):
        """Get an organization's configuration. Can be used by Org-Admin and Sys-Admin.

        Args:
            org_id(:py:obj:`str`): The organization's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command` containing the response from the API call.
        """
        response = self._get(app="security", endpoint='/v{}/organizationConfig/{}'.format(self.api_version, org_id))
        return Command(self, response)

    def update_organization_configuration_v2(self, data, org_id):
        """Update an organization's configuration. Can be used by Org-Admin and Sys-Admin.

        Args:
            data (:py:obj:`dict`): A dictionary with the updated configuration for a given organization.
            org_id(:py:obj:`str`): The organization's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command` containing the response from the API call.
        """
        response = self._post(
            app="security", data=data, endpoint='/v{}/organizationConfig/{}'.format(self.api_version, org_id)
        )
        return Command(self, response)

    def get_organization_global_configurations(self):
        response = self._get(app='security', endpoint='/v{}/organizations/globalConfigs'.format(self.api_version))
        return Command(self, response)

    def update_organization_global_configurations(self, body):
        response = self._post(
            app='security', endpoint='/v{}/organizations/globalConfigs'.format(self.api_version), data=body
        )
        return Command(self, response)

    def create_user(self, org_id, body):
        """Create a new user for the given User model.

        Args:
            org_id (:obj:`str`): Organization ID
            body (:obj:`dict`): User object that complies to Swagger UserJson definition

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/users'.format(self.api_version, org_id)
        response = self._put(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def update_user_password(self, org_id, user_id, body):
        """Update user password.

        Args:
            org_id (:obj:`str`): Organization ID.
            user_id (:obj:`str`): User ID.
            body (:obj:`dict`): Passwords object that complies to Swagger PasswordsJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/user/{}/updatePassword'.format(self.api_version, org_id, user_id)
        response = self._post(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def get_all_users(
        self,
        org_id,
        offset=None,
        len=None,
        order_by='ID',
        order='ASC',
        active=None,
        filter_text=None,
        deleted=None,
        with_wrapper=False,
    ):
        """Get all users.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'ID'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            active (:obj:`str`, optional): Default: ``None``
            filter_text (:obj:`str`, optional): Default: ``None``
            deleted (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/users'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_user(self, org_id, user_id):
        """Get the user for the given user ID.

        Args:
            org_id (:obj:`str`): Organization ID
            user_id (:obj:`str`): User ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/user/{}'.format(self.api_version, org_id, user_id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def update_user(self, org_id, user_id, body):
        """Update a user for the given User model.

        Args:
            org_id (:obj:`str`): Organization ID
            user_id (:obj:`str`): User ID
            body (:obj:`dict`): User object that complies to Swagger UserJson definition

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/user/{}'.format(self.api_version, org_id, user_id)
        response = self._post(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def create_group(self, org_id, body):
        """Create a new group for the given Group model.

        Args:
            org_id (:obj:`str`): Organization ID.
            body (:obj:`dict`): Group object that complies to Swagger GroupJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/groups'.format(self.api_version, org_id)
        response = self._put(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def get_all_groups(
        self,
        org_id,
        offset=None,
        len=None,
        order_by='ID',
        order='ASC',
        filter_text=None,
        deleted=None,
        with_wrapper=False,
    ):
        """Get all groups.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'ID'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
            filter_text (:obj:`str`, optional): Default: ``None``.
            deleted (:obj:`str`, optional): Default: ``None``.
            with_wrapper (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/groups'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_group(self, org_id, group_id):
        """Get the group for the given group ID.

        Args:
            org_id (:obj:`str`): Organization ID.
            group_id (:obj:`str`): Group ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/group/{}'.format(self.api_version, org_id, group_id)
        response = self._get(app='security', endpoint=endpoint)
        return Command(self, response)

    def update_group(self, org_id, group_id, body):
        """Update a group for the given Group model.

        Args:
            org_id (:obj:`str`): Organization ID.
            group_id (:obj:`str`): Group ID.
            body (:obj:`dict`): Group object that complies to Swagger GroupJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/group/{}'.format(self.api_version, org_id, group_id)
        response = self._post(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def delete_group(self, org_id, group_id):
        """Delete a group for the given group ID.

        Args:
            org_id (:obj:`str`): Organization ID.
            group_id (:obj:`str`): Group ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/group/{}'.format(self.api_version, org_id, group_id)
        response = self._delete(app='security', endpoint=endpoint)
        return Command(self, response)

    def delete_groups(self, org_id, body):
        """Delete all groups for the given group IDs.

        Args:
            org_id (:obj:`str`): Organization ID.
            body (:obj:`list`): Group IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/groups/delete'.format(self.api_version, org_id)
        response = self._post(app='security', data=body, endpoint=endpoint)
        return Command(self, response)

    def create_connection(self, body):
        """Create a new connection.

        Args:
            body (:obj:`dict`): Connection object that complies to Swagger ConnectionJson definition

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/connections'.format(self.api_version)
        response = self._put(app='connection', data=body, endpoint=endpoint)
        return Command(self, response)

    def get_all_connections(
        self,
        organization,
        connection_type=None,
        filter_text=None,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        with_total_count=False,
    ):
        """Get all connections.

        Args:
            organization (:obj:`str`)
            connection_type (:obj:`str`, optional): Default: ``None``
            filter_text (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_total_count (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/connections'.format(self.api_version)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_connections_types(self, offset=None, len=None, with_wrapper=False):
        """Get all connection types.

        Args:
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            with_wrapper (obj:`bool`): Default: ``None``.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/connections/types'.format(self.api_version)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_connection(self, connection_id):
        """Get the connection for the given connection ID.

        Args:
            connection_id (:obj:`str`): Connection ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/connection/{}'.format(self.api_version, connection_id)
        response = self._get(app='connection', endpoint=endpoint)
        return Command(self, response)

    def update_connection(self, connection_id, body):
        """Update connection.

        Args:
            connection_id (:obj:`str`): Connection ID
            body (:obj:`dict`): Connection object that complies to Swagger ConnectionJson definition

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/connection/{}'.format(self.api_version, connection_id)
        response = self._post(app='connection', data=body, endpoint=endpoint)
        return Command(self, response)

    def delete_connection(self, connection_id):
        """Delete connection.

        Args:
            connection_id (:obj:`str`): Connection ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        endpoint = '/v{}/connection/{}'.format(self.api_version, connection_id)
        response = self._delete(app='connection', endpoint=endpoint)
        return Command(self, response)

    def get_pipeline_commits_using_connection(self, connection_id, offset=None, len=None, with_wrapper=False):
        """Get all pipeline commits using given connection.

        Args:
            connection_id (:obj:`str`)
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            with_wrapper (:obj:`bool`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'connection_id'))
        endpoint = '/v{}/connection/{}/getPipelineCommits'.format(self.api_version, connection_id)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_pipeline_commit_counts_using_connection(self, connection_id):
        """Get count of pipeline commits using given connection.

        Args:
            connection_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/connection/{}/countPipelineCommits'.format(self.api_version, connection_id)
        response = self._get(app='connection', endpoint=endpoint)
        return Command(self, response)

    def get_pipelines_by_query(self, org_id, search, order_by=None, offset=None, len=None):
        """Get all pipelines that match query.

        Args:
            org_id (:obj:`str`)
            search (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/search'.format(self.api_version)
        response = self._get(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_finish_conditions(self, sequence_id):
        """Get all the finish conditions for the Sequence ID.

        Args:
            sequence_id (:obj:`str`) Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/sequencing/{}'.format(self.api_version, sequence_id)
        response = self._get(app='sequencing', endpoint=endpoint)
        return Command(self, response)

    def delete_finish_condition(self, sequence_id, step_job_instance_id, finish_condition_id):
        """Delete finish condition.

        Args:
            sequence_id (:obj:`str`) Sequence ID.
            step_job_instance_id (:obj:`str`) Step Job Instance ID.
            finish_condition_id (:obj:`str`) Finish Condition ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/sequencing/{}/{}/{}'.format(
            self.api_version, sequence_id, step_job_instance_id, finish_condition_id
        )
        response = self._delete(app='sequencing', endpoint=endpoint)
        return Command(self, response)

    def create_finish_condition(self, sequence_id, step_job_instance_id, finish_condition_json):
        """Delete finish condition.

        Args:
            sequence_id (:obj:`str`) Sequence ID.
            step_job_instance_id (:obj:`str`) Step Job Instance ID.
            finish_condition_json (:obj:`dict`) Finish Condition JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/sequencing/{}/createFinishCondition/{}'.format(
            self.api_version, sequence_id, step_job_instance_id
        )
        response = self._post(app='sequencing', endpoint=endpoint, data=finish_condition_json)
        return Command(self, response)

    def update_finish_condition(
        self, sequence_id, step_job_instance_id, finish_condition_id, update_finish_condition_json
    ):
        """Delete finish condition.

        Args:
            sequence_id (:obj:`str`) Sequence ID.
            step_job_instance_id (:obj:`str`) Step Job Instance ID.
            finish_condition_id (:obj:`str`) Finish Condition ID.
            update_finish_condition_json (:obj:`dict`) Finish Condition JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/sequencing/{}/{}/{}'.format(
            self.api_version, sequence_id, step_job_instance_id, finish_condition_id
        )
        response = self._put(app='sequencing', endpoint=endpoint, data=update_finish_condition_json)
        return Command(self, response)

    def create_saql_fav_pipeline(self, search_id):
        """Creates a favorite saql pipeline search query.
            In other words, it stars an existing pipeline search
            query.

        Args:
            search_id (:obj:`str`): ID of aql search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/savedFilters/fav'.format(self.api_version)
        response = self._post(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_saql_pipeline_search(self, aql_search_json):
        """Create a saql pipeline search query.

        Args:
            aql_search_json (:obj:`str`): Aql search in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/savedFilters'.format(self.api_version)
        response = self._post(app='pipelinestore', endpoint=endpoint, data=aql_search_json)
        return Command(self, response)

    def update_saql_pipeline_search(self, search_id, aql_search_json):
        """Update a saql pipeline search query.

        Args:
            search_id (:obj:`str`): ID of aql search object.
            aql_search_json (:obj:`str`): Aql search in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/saql/pipelines/savedFilters/{}'.format(self.api_version, search_id)
        response = self._put(app='pipelinestore', endpoint=endpoint, data=aql_search_json)
        return Command(self, response)

    def get_saql_pipeline_searches(self, name, type, offset=None, len=None, order_by='ASC'):
        """Get all saql pipeline searches that match the name.

        Args:
            name (:obj:`str`) Name of aql search object.
            type (:obj:`str`) Type of aql search object, limited to``'PIPELINE'`` or ``'FRAGMENT'``.
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'ASC'``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/savedFilters'.format(self.api_version)
        response = self._get(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def remove_saql_pipeline_search(self, search_id):
        """Remove a saql pipeline search.

        Args:
            search_id (:obj:`str`): ID of aql search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/savedFilters'.format(self.api_version)
        response = self._delete(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_job_sequence_aql_search(self, search, offset=None, len=None):
        """Get all Job Sequence AQL searches that match the query.

        Args:
            search (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/sequencing/search'.format(self.api_version)
        response = self._get(app='sequencing', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_fragments_by_query(self, org_id, search, order_by=None, offset=None, len=None):
        """Get all pipelines that match query.

        Args:
            org_id (:obj:`str`)
            search (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/pipelines/search/fragments'.format(self.api_version)
        response = self._get(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def is_first_time_user(self):
        """Determine if the user is a “first time user” for designer mode.
            Users who have at least one created pipeline, have an engine, or more than 1 user in their organization
            (as another user could have a pipeline not shared with them)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/designer/firstTimeUser'.format(self.api_version)
        response = self._get(app='pipelinestore', endpoint=endpoint)
        return Command(self, response)

    def create_designer_pipeline(self, engine_version_id, pipeline_id=None):
        """Create an empty pipeline template for the given engine version.

        Args:
            pipeline_id (:obj:`str`, optional): Pipeline ID in string format.
            engine_version_id (:obj:`str`): Engine Version ID in string format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', engine_version_id))
        endpoint = '/v{}/designer/{}/newPipeline'.format(self.api_version, engine_version_id)
        response = self._post(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_designer_engine_definition(self, engine_version_id):
        """Return result for engine and combination of stagelibs.

        Args:
            engine_version_id (:obj:`str`): Engine Version ID in string format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """

        def translate_schema_definition(definitions):
            """Translate schema defintions from v2 to v1.
            Note that this mutates the passed dict."""
            schema_version = int(definitions.pop("schemaVersion", 1))
            if schema_version < 2:
                return  # No need for migration
            stage_definition_map: dict[str, any] = definitions.pop("stageDefinitionMap")
            stages = []
            for entry in definitions["stageDefinitionMinimalList"]:
                key = "{}::{}".format(entry['name'], entry['version'])
                stage_def = stage_definition_map[key]
                stages.append(stage_def)
            definitions["stages"] = stages

        endpoint = '/v{}/designer/{}/definitions'.format(self.api_version, engine_version_id)
        response = self._get(app='pipelinestore', endpoint=endpoint)
        engine_definitions = response.json()
        translate_schema_definition(engine_definitions)
        response._content = json.dumps(engine_definitions).encode("utf-8")
        return Command(self, response)

    def get_designer_connection_definition(self, engine_version_id):
        """Return result for engine and combination of stagelibs.

        Args:
            engine_version_id (:obj:`str`): Engine Version ID in string format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/designer/{}/connections'.format(self.api_version, engine_version_id)
        response = self._get(app='pipelinestore', endpoint=endpoint)
        return Command(self, response)

    def validate_snowflake_account(self, body):
        """Validate snowflake account.

        Args:
            body (:obj:`dict`): Body for the API call.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/credential/snowflake/validate'.format(self.api_version)
        response = self._post(app='pipelinestore', endpoint=endpoint, data=body)
        return Command(self, response)

    def validate_snowflake_account_status(self, token):
        """Check the status of a snowflake account validation process.

        Args:
            token (:obj:`str`): Token of the snowflake account validation process.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/credential/snowflake/validate'.format(self.api_version)
        response = self._get(app='pipelinestore', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_default_designer_deployment(self):
        """Return (and create if not exists) default deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployments/default'.format(self.api_version)
        response = self._post(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_all_connection_audits(
        self, org_id, offset=None, len_=None, sort_field=None, sort_order=None, start_time=0, end_time=-1
    ):
        """Get all connection audits between a time frame.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``None``
            sort_order (:obj:`str`, optional): Default: ``None``
            start_time (:obj:`long`, optional): Default: ``0``
            end_time (:obj:`long`, optional): Default: ``-1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        if 'len_' in params:
            params['len'] = params.pop('len_')
        endpoint = '/v{}/connections/{}/connectionAuditsTime'.format(self.api_version, org_id)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_connection_audits_last_30_days(self, org_id, offset=None, len_=None, sort_field=None, sort_order=None):
        """Get all connection audits for last 30 days.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``None``
            sort_order (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        if 'len_' in params:
            params['len'] = params.pop('len_')
        # This endpoint returns connection audits for last 30 days even though the endpoint name is generic
        endpoint = '/v{}/connections/{}/connectionAudits'.format(self.api_version, org_id)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_audits_for_connection(self, connection_id):
        """Get all audits for connection.

        Args:
            connection_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/connections/{}/audit'.format(self.api_version, connection_id)
        response = self._get(app='connection', endpoint=endpoint)
        return Command(self, response)

    def get_all_connection_tags(self, organization, parent_id=None, offset=None, len_=None, order='ASC'):
        """Get all connections.

        Args:
            organization (:obj:`str`)
            parent_id (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`str`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        if 'len_' in params:
            params['len'] = params.pop('len_')
        endpoint = '/v{}/connections/tags'.format(self.api_version)
        response = self._get(app='connection', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_classification_catalog_list(self):
        response = self._get(
            app='sdp_classification',
            endpoint=('/v{}/classification/catalog/' 'o:list/pageId=CatalogListPage').format(self.sdp_api_version),
        )
        return Command(self, response)

    def commit_classification_rules(self, id_):
        response = self._post(
            app='sdp_classification',
            endpoint=('/v{}/classification/catalog/' 'o:commit/{}/pageId=CatalogManagePage').format(
                self.sdp_api_version, id_
            ),
        )
        return Command(self, response)

    def get_new_classification_rule(self, id_):
        response = self._get(
            app='sdp_classification',
            endpoint=('/v{}/classification/rule/' 'o:new/{}/pageId=RuleNewPage').format(self.sdp_api_version, id_),
        )
        return Command(self, response)

    def get_protection_policy_list(self):
        response = self._get(
            app='policy', endpoint='/v{}/policy/o:list/pageId=PolicyListPage'.format(self.sdp_api_version)
        )
        return Command(self, response)

    def get_new_protection_policy(self):
        response = self._get(
            app='policy', endpoint='/v{}/policy/o:new/pageId=PolicyNewPage'.format(self.sdp_api_version)
        )
        return Command(self, response)

    def create_protection_policy(self, body):
        response = self._put(
            app='policy',
            endpoint='/v{}/policy/o:create/pageId=PolicyManagePage'.format(self.sdp_api_version),
            data=body,
        )
        return Command(self, response)

    def set_default_write_protection_policy(self, policy_id):
        response = self._post(
            app='policy',
            endpoint=('/v{}/policy/o:default/write/' '{}/pageId=PolicyManagePage').format(
                self.sdp_api_version, policy_id
            ),
        )
        return Command(self, response)

    def set_default_read_protection_policy(self, policy_id):
        response = self._post(
            app='policy',
            endpoint=('/v{}/policy/o:default/read/' '{}/pageId=PolicyManagePage').format(
                self.sdp_api_version, policy_id
            ),
        )
        return Command(self, response)

    def export_protection_policies(self, policy_ids):
        response = self._get(
            app='policy',
            endpoint=('/v{}/policy/o:exportPolicies' '/pageId=PolicyManagePage').format(self.sdp_api_version),
            params={'id': policy_ids},
        )
        return Command(self, response)

    def import_protection_policies(self, policies_file):
        response = self._post(
            app='policy',
            endpoint=('/v{}/policy/o:importPolicies/' 'pageId=PolicyManagePage').format(self.sdp_api_version),
            files={'file': policies_file},
            headers={'content-type': None},
        )
        return Command(self, response)

    def get_new_policy_procedure(self, id_):
        response = self._get(
            app='policy', endpoint='/v{}/procedure/o:new/{}/pageId=ProcedureNewPage'.format(self.sdp_api_version, id_)
        )
        return Command(self, response)

    def create_policy_procedure(self, body):
        response = self._put(
            app='policy',
            endpoint='/v{}/procedure/o:create/pageId=ProcedureManagePage'.format(self.sdp_api_version),
            data=body,
        )
        return Command(self, response)

    def create_classification_rule(self, body):
        response = self._put(
            app='sdp_classification',
            endpoint=('/v{}/classification/rule/' 'o:create/pageId=RuleManagePage').format(self.sdp_api_version),
            data=body,
        )
        return Command(self, response)

    def get_new_classification_classifier(self, id_):
        response = self._get(
            app='sdp_classification',
            endpoint=('/v{}/classification/classifier/' 'o:new/{}/pageId=ClassifierNewPage').format(
                self.sdp_api_version, id_
            ),
        )
        return Command(self, response)

    def create_classification_classifier(self, body):
        response = self._put(
            app='sdp_classification',
            endpoint=('/v{}/classification/classifier/' 'o:create/pageId=ClassifierManagePage').format(
                self.sdp_api_version
            ),
            data=body,
        )
        return Command(self, response)

    def get_classification_classifier_list(self, id_):
        response = self._get(
            app='sdp_classification',
            endpoint=('/v{}/classification/classifier/' 'o:list/{}/pageId=ClassifierListPage').format(
                self.sdp_api_version, id_
            ),
        )
        return Command(self, response)

    def delete_classification_classifier(self, id_):
        response = self._delete(
            app='sdp_classification',
            endpoint=('/v{}/classification/classifier/' 'o:delete/{}/pageId=ClassifierManagePage').format(
                self.sdp_api_version, id_
            ),
        )
        return Command(self, response)

    def commit_pipeline(
        self,
        organization=None,
        new_pipeline=None,
        execution_mode=SDC_DEFAULT_EXECUTION_MODE,
        template_commit_id=None,
        import_pipeline=None,
        fragment=None,
        pipeline_type=None,
        body=None,
        remove_missing_connection=False,
    ):
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._put(
            app='pipelinestore', endpoint='/v{}/pipelines'.format(self.api_version), params=params, data=body
        )
        return Command(self, response)

    def get_pipeline_commit(self, commit_id):
        response = self._get(app='pipelinestore', endpoint='/v{}/pipelineCommit/{}'.format(self.api_version, commit_id))
        return Command(self, response)

    def get_pipeline_commits(
        self,
        pipeline_id,
        organization=None,
        offset=None,
        len_=None,
        order='ASC',
        only_published=None,
        with_wrapper=False,
    ):
        """Get the commits for a pipeline.

        Args:
            pipeline_id (:obj:`str`)
            organization (:obj:`str`): Default: ``None``.
            offset (:obj:`int`): Default: ``None``.
            len_ (:obj:`int`): Default: ``None``.
            order (:obj:`str`): Default: ``'ASC'``.
            only_published (:obj:`str`): Default: ``None``.
            with_wrapper (:obj:`bool`): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipeline/{}/log'.format(self.api_version, pipeline_id), params=params
        )
        return Command(self, response)

    def get_pipelines_commit(self, body):
        response = self._post(app='pipelinestore', endpoint='/v{}/pipelineCommit'.format(self.api_version), data=body)
        return Command(self, response)

    def get_latest_pipeline_commit(self, pipeline_id, user=None, only_published=None):
        """Get the latest pipeline commit for a given pipeline ID.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID.
            user (:obj:`str`, optional): Default: ``None``.
            only_published (:obj:`boolean`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipeline/{}/latest'.format(self.api_version, pipeline_id), params=params
        )
        return Command(self, response)

    def save_pipeline_commit(self, commit_id, validate=None, include_library_definitions=None, body=None):
        params = get_params(parameters=locals(), exclusions=('self', 'commit_id', 'body'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelineCommit/{}'.format(self.api_version, commit_id),
            params=params,
            data=body,
        )
        return Command(self, response)

    def publish_pipeline_commit(self, commit_id, commit_message=None):
        params = get_params(parameters=locals(), exclusions=('self', 'commit_id'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelineCommit/{}/publish'.format(self.api_version, commit_id),
            params=params,
        )
        return Command(self, response)

    def get_pipelines_definitions(self, executor_type):
        """Get pipeline definitions.

        Args:
            executor_type (:obj:`str`): Executor type of the pipeline.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='pipelinestore', endpoint='/v{}/definitions'.format(self.api_version), params=params)
        return Command(self, response)

    def get_all_pipeline_labels(self, organization, parent_id=None, offset=None, len=None, order=None):
        """Get pipeline labels for a given organization.

        Args:
            organization (:obj:`str`)
            parent_id (:obj:`str`, optional): Default: ``None``
            offset (:obj:`int`, optional): Default: ``None``
            len (obj:`int`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipelineLabels'.format(self.api_version), params=params
        )
        return Command(self, response)

    def delete_pipeline_labels(self, body):
        """Delete pipeline labels.

        Args:
            body (:obj:`list`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='pipelinestore', endpoint='/v{}/pipelineLabels/deleteLabels'.format(self.api_version), data=body
        )
        return Command(self, response)

    def get_pipelines_count(self, organization, system):
        """Returns the number of pipelines for the current user.

        Args:
            organization (:obj:`str`).
            system (:obj:`bool`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipelines/count'.format(self.api_version), params=params
        )
        return Command(self, response)

    def create_snowflake_pipeline(self, pipeline_title, description=None, auto_generate_pipeline_id=None, draft=None):
        """Add a new Snowflake pipeline configuration to the store.

        Args:
            pipeline_title (:obj:`str`)
            description (:obj:`str`, optional): Default: ``None``
            auto_generate_pipeline_id (:obj:`bool`, optional): If True, pipeline ID will be generated by
                concatenating a UUID to a whitespace-stripped version of the pipeline title. If
                False, the pipeline title will be used as the pipeline ID. Default: ``None``
            draft (:obj:`bool`, optional): If True, pipeline will be created but not added to pipeline store.
                Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_title'))
        response = self._put(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}'.format(
                self.api_version, self.api_version, pipeline_title
            ),
            params=params,
        )
        return Command(self, response)

    def get_snowflake_pipeline(self, pipeline_id, rev=0, only_if_exists=None):
        """Get status of a Snowflake pipeline.

        Args:
            pipeline_id (:obj:`str`)
            rev (:obj:`int`, optional): Revision of the pipeline. Default: ``0``
            only_if_exists (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.SnowflakePipelineCommand`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._get(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/status'.format(
                self.api_version, self.api_version, pipeline_id
            ),
            params=params,
        )
        return SnowflakePipelineCommand(self, response)

    def get_snowflake_pipeline_configuration(self, pipeline_id, rev=0, get='pipeline'):
        """Get Snowflake pipeline configuration.

        Args:
            pipeline_id (:obj:`str`)
            rev (:obj:`int`, optional): Revision of the pipeline. Default: 0
            get (:obj:`str`, optional): Default: ``pipeline``

        Returns:
            A :obj:`dict` of pipeline configuration information.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._get(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}'.format(
                self.api_version, self.api_version, pipeline_id
            ),
            params=params,
        )
        return response.json() if response.content else {}

    def reset_snowflake_origin_offset(self, pipeline_id, rev=0):
        """Reset Snowflake pipeline origin offset.

        Args:
            pipeline_id (:obj:`str`)
            rev (:obj:`int`, optional): Revision of the pipeline. Default: ``0``

        Returns:
            An instance of :py:class:`streamsets.sdk.st_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        endpoint = '/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/resetOffset'
        response = self._post(
            app='pipelinestore',
            endpoint=endpoint.format(self.api_version, self.api_version, pipeline_id),
            params=params,
        )
        return Command(self, response)

    def run_snowflake_pipeline_preview(
        self,
        pipeline_id,
        rev=0,
        batches=1,
        batch_size=10,
        skip_targets=True,
        end_stage=None,
        only_schema=None,
        push_limit_down=True,
        timeout=2000,
        test_origin=False,
        stage_outputs_to_override_json=None,
    ):
        """Run Snowflake pipeline preview.

        Args:
            pipeline_id (:obj:`str`)
            rev (:obj:`int`, optional): Default: 0
            batches (:obj:`int`, optional): Default: 1
            batch_size (:obj:`int`, optional): Default: 10
            skip_targets (:obj:`bool`, optional): Default: ``True``
            end_stage (:obj:`str`, optional): Default: ``None``
            only_schema (:obj:`bool`, optional): Only schema. Default: ``None``.
            push_limit_down (:obj:`bool`, optional): Push limit down. Default: ``True``
            timeout (:obj:`int`, optional): Default: 2000
            test_origin (:obj:`bool`, optional): Test origin. Default: ``False``
            stage_outputs_to_override_json (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.PreviewCommand`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/preview'.format(
                self.api_version, self.api_version, pipeline_id
            ),
            params=params,
        )
        previewer_id = response.json()['previewerId']
        return PreviewCommand(self, response, pipeline_id, previewer_id)

    def validate_snowflake_pipeline(self, pipeline_id, rev=0, timeout=2000):
        """Validate Snowflake pipeline.

        Args:
            pipeline_id (:obj:`str`)
            rev (:obj:`int`, optional): Default: 0
            timeout (:obj:`int`, optional): Default: 2000

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.ValidateCommand`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id'))
        response = self._get(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/validate'.format(
                self.api_version, self.api_version, pipeline_id
            ),
            params=params,
        )
        previewer_id = response.json()['previewerId']
        return ValidateCommand(self, response, pipeline_id, previewer_id)

    def get_snowflake_preview_status(self, pipeline_id, previewer_id):
        """Get the status of a Snowflake preview.

        Args:
            pipeline_id (:obj:`str`)
            previewer_id (:obj:`int`): Id of the preview.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        endpoint = '/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/preview/{}/status'
        response = self._get(
            app='pipelinestore', endpoint=endpoint.format(self.api_version, self.api_version, pipeline_id, previewer_id)
        )
        return Command(self, response)

    def get_snowflake_preview_data(self, pipeline_id, previewer_id):
        """Get Snowflake preview data.

        Args:
            pipeline_id (:obj:`str`)
            previewer_id (:obj:`str`): Id of the preview.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.PreviewCommand`
        """
        response = self._get(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}/preview/{}'.format(
                self.api_version, self.api_version, pipeline_id, previewer_id
            ),
        )
        return PreviewCommand(self, response, pipeline_id, previewer_id)

    def update_snowflake_pipeline(self, pipeline_id, pipeline, rev=0, description=None):
        """Update a Snowflake pipeline.

        Args:
            pipeline_id (:obj:`str`)
            pipeline (:obj:`str`): Pipeline configuration in JSON format.
            rev (:obj:`int`, optional): Revision of the pipeline. Default: ``0``.
            description (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id', 'pipeline'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipeline/snowflake/rest/v{}/pipeline/{}'.format(
                self.api_version, self.api_version, pipeline_id
            ),
            params=params,
            data=pipeline,
        )
        return Command(self, response)

    def validate_engine_pipeline(self, engine_id, pipeline_id, tunneling_instance_id, rev=0, timeout=2000):
        """Validate Datacollector or Transformer pipeline.

        Args:
            pipeline_id (:obj:`str`)
            engine_id (:obj:`str`)
            tunneling_instance_id (:obj:`str`)
            rev(:obj:`int`, optional): Default: ``0``
            timeout (:obj:`int`, optional): Default: ``2000``

        Returns: An instance of :py:class:`streamsets.sdk.sch_api.ValidateCommand`
        """
        params = get_params(
            parameters=locals(), exclusions=('self', 'engine_id', 'pipeline_id', 'tunneling_instance_id')
        )
        endpoint = '/v{}/pipeline/{}/validate'.format(self.api_version, pipeline_id)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        previewer_id = response.json()['previewerId']
        return ValidateCommand(self, response, pipeline_id, previewer_id)

    def get_pipeline_preview_status(self, engine_id, pipeline_id, previewer_id, tunneling_instance_id):
        """Get the status of a pipeline preview.

        Args:
            engine_id (:obj:`str`)
            pipeline_id (:obj:`str`)
            previewer_id (:obj:`int`): Id of the preview.
            tunneling_instance_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        endpoint = '/v{}/pipeline/{}/preview/{}/status'.format(self.api_version, pipeline_id, previewer_id)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id
        )
        return Command(self, response)

    def get_pipeline_preview_data(self, engine_id, pipeline_id, previewer_id, tunneling_instance_id):
        """Get pipeline preview data.

        Args:
            engine_id (:obj:`str`)
            pipeline_id (:obj:`str`)
            previewer_id (:obj:`str`): Id of the preview.
            tunneling_instance_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.PreviewCommand`
        """
        endpoint = '/v{}/pipeline/{}/preview/{}'.format(self.api_version, pipeline_id, previewer_id)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id
        )
        return PreviewCommand(self, response, pipeline_id, previewer_id)

    def get_pipeline_tags(self, pipeline_id):
        """Get pipeline tags.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipeline/{}/tags'.format(self.api_version, pipeline_id)
        )
        return Command(self, response)

    def create_pipeline_draft(self, commit_id, authoring_sdc_id=None, authoring_sdc_version=None):
        params = get_params(parameters=locals(), exclusions=('self', 'commit_id'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelineCommit/{}/createDraft'.format(self.api_version, commit_id),
            params=params,
        )
        return Command(self, response)

    def delete_pipeline(self, pipeline_id):
        """Delete all versions of pipeline.

        Args:
            pipeline_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='pipelinestore', endpoint='/v{}/pipeline/{}'.format(self.api_version, pipeline_id))
        return Command(self, response)

    def delete_pipeline_commit(self, pipeline_commit_id):
        """Delete only the selected version of pipeline.

        Args:
            pipeline_commit_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='pipelinestore', endpoint='/v{}/pipelineCommit/{}'.format(self.api_version, pipeline_commit_id)
        )
        return Command(self, response)

    def duplicate_pipeline(self, pipeline_commit_id, body):
        """Duplicate an existing pipleine.

        Args:
            pipeline_commit_id (:obj:`str`)
            body (:obj:`dict`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelineCommit/{}/duplicate'.format(self.api_version, pipeline_commit_id),
            data=body,
        )
        return Command(self, response)

    def export_pipelines(self, fragments=None, body=None, include_plain_text_credentials=False):
        """Export pipelines.

        Args:
            body (:obj:`list`): A list of :obj:`str` commit ids.
            fragments (:obj:`bool`): Indicates if exporting fragments is needed.
            include_plain_text_credentials (:obj:`bool`): Indicates if plain text credentials should be included.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelines/exportPipelineCommits'.format(self.api_version),
            params=params,
            data=body,
        )
        return Command(self, response)

    def return_all_pipelines(
        self,
        organization,
        pipeline_label_id,
        offset,
        len,
        order_by,
        order,
        system,
        filter_text,
        only_published,
        execution_modes,
        start_time=-1,
        end_time=-1,
        user_ids=None,
        draft=None,
    ):
        """Returns all pipelines.

        Args:
            organization (:obj:`str`)
            pipeline_label_id (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            system (:obj:`str`)
            filter_text (:obj:`str`)
            only_published (:obj:`bool`)
            execution_modes (:obj:`str`)
            start_time (:obj:`int`, optional): Default: ``-1``
            end_time (:obj:`int`, optional): Default: ``-1``
            user_ids (:obj:`list`, optional): List of strings. Default: ``None``
            draft (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='pipelinestore', endpoint='/v{}/pipelines'.format(self.api_version), params=params)
        return Command(self, response)

    def return_all_pipeline_fragments(
        self,
        organization,
        pipeline_label_id,
        offset,
        len,
        order_by,
        order,
        system,
        filter_text,
        only_published,
        execution_modes,
        start_time=-1,
        end_time=-1,
        user_ids=None,
        draft=None,
    ):
        """Returns all pipeline fragments.

        Args:
            organization (:obj:`str`)
            pipeline_label_id (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            system (:obj:`str`)
            filter_text (:obj:`str`)
            only_published (:obj:`bool`)
            execution_modes (:obj:`str`)
            start_time (:obj:`int`, optional): Default: ``-1``
            end_time (:obj:`int`, optional): Default: ``-1``
            user_ids (:obj:`list`, optional): List of strings. Default: ``None``
            draft (:obj:`bool`, optional): Default: ``None``
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipelines/fragments'.format(self.api_version), params=params
        )
        return Command(self, response)

    def import_pipeline_new_version_by_id(self, pipeline_json, pipeline_id, commit_message=None):
        """Import pipeline new version by ID.

        Args:
            pipeline_json (:obj:`str`): Pipeline underlying data in JSON format.
            pipeline_id (:obj:`str`): Pipeline ID.
            commit_message (:obj:`str`, optional): Commit message.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id', 'pipeline_json'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipeline/{}/importPipelineNewVersionById'.format(self.api_version, pipeline_id),
            params=params,
            data=pipeline_json,
        )
        return Command(self, response)

    def import_pipelines(
        self,
        commit_message,
        pipelines_file,
        fragments,
        fail_if_exists=False,
        import_as_new=False,
        remove_missing_connection=False,
    ):
        """Import pipelines from archived zip directory.

        Args:
            commit_message (:obj:`str`): Commit message
            pipelines_file (:obj:`file`): file containing the pipelines
            fragments (:obj:`bool`): Indicates if pipeline contains fragments.
            fail_if_exists (:obj:`bool`, optional): Default: ``False``.
            import_as_new (:obj:`bool`, optional): Default: ``False``.
            remove_missing_connection (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command` that wraps a list of
            :py:class:`streamsets.sdk.sch_models.Pipeline`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipelines_file'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelines/importPipelineCommits'.format(self.api_version),
            files={'file': pipelines_file},
            params=params,
            headers={'content-type': None},
        )
        return Command(self, response)

    def import_pipelines_v2(self, import_pipeline_json):
        """Import pipelines from importPipelinesJson
        Args:
            import_pipeline_json (:obj:`str`): Import pipeline in json format .

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'import_pipeline_json'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelines/importPipelineCommitsV2'.format(self.api_version),
            params=params,
            data=import_pipeline_json,
        )
        return Command(self, response)

    def verify_import_pipelines(
        self, commit_message, pipelines_file, fragments=False, fail_if_exists=False, import_as_new=False
    ):
        """Verify import Pipelines from compressed archive.

        Args:
            commit_message (:obj:`str`): Commit message
            pipelines_file (:obj:`file`): File containing the pipelines
            fragments (:obj:`bool`, optional): Indicates if pipeline contains fragments. Default: ``False``.
            fail_if_exists (:obj:`bool`, optional): Default: ``False``.
            import_as_new (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipelines_file'))
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelines/verifyPipelineCommits'.format(self.api_version),
            files={'file': pipelines_file},
            params=params,
            headers={'content-type': None},
        )
        return Command(self, response)

    def get_pipeline_acl(self, pipeline_id):
        """Get pipeline ACL.

        Args:
            pipeline_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='pipelinestore', endpoint='/v{}/pipeline/{}/acl'.format(self.api_version, pipeline_id))
        return Command(self, response)

    def set_pipeline_acl(self, pipeline_id, pipeline_acl_json):
        """Update pipeline ACL.

        Args:
            pipeline_id (:obj:`str`)
            pipeline_acl_json (:obj:`str`): Pipeline ACL in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipeline/{}/acl'.format(self.api_version, pipeline_id),
            data=pipeline_acl_json,
        )
        return Command(self, response)

    def get_snowflake_pipeline_defaults(self):
        """Get the Snowflake pipeline defaults for this user (if it exists).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='pipelinestore', endpoint='/v{}/defaults/snowflake'.format(self.api_version))
        return Command(self, response)

    def update_snowflake_pipeline_defaults(self, body):
        """Create or update the Snowflake pipeline defaults for this user.

        Args:
            body (:obj:`dict`): JSON representation of the default parameters to update.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='pipelinestore', endpoint='/v{}/defaults/snowflake'.format(self.api_version), data=body
        )
        return Command(self, response)

    def delete_snowflake_pipeline_defaults(self):
        """Delete the Snowflake pipeline defaults for this user.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='pipelinestore', endpoint='/v{}/defaults/snowflake'.format(self.api_version))
        return Command(self, response)

    def get_snowflake_user_credentials(self):
        """Get the Snowflake user credentials (if they exist). They will be redacted.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='pipelinestore', endpoint='/v{}/credential/snowflake'.format(self.api_version))
        return Command(self, response)

    def update_snowflake_user_credentials(self, body):
        """Create or update the Snowflake user credential.

        Args:
            body (:obj:`dict`): JSON representation of the default parameters to update.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='pipelinestore', endpoint='/v{}/credential/snowflake'.format(self.api_version), data=body
        )
        return Command(self, response)

    def delete_snowflake_user_credentials(self):
        """Delete the Snowflake user credential.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='pipelinestore', endpoint='/v{}/credential/snowflake'.format(self.api_version))
        return Command(self, response)

    def get_snowflake_generated_queries(self, job_id, run_count, len=-1, offset=0, order='DESC'):
        """Return Snowflake generated queries for given job id and run.

        Args:
            job_id (:obj:`str`)
            run_count (:obj:`int`)
            len (:obj:`int`, optional): Default: ``-1``
            offset (:obj:`int`, optional): Default: ``0``
            order (:obj:`str`, optional): Default: ``DESC``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/snowflakeQueries'.format(self.api_version), params=params)
        return Command(self, response)

    def get_topology_acl(self, topology_id):
        """Get the ACL of a Topology.

        Args:
            topology_id (:obj:`str`): ID of the Topology.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='topology', endpoint='/v{}/topology/{}/acl'.format(self.api_version, topology_id))
        return Command(self, response)

    def set_topology_acl(self, topology_id, topology_acl_json):
        """Update the ACL of a Topology.

        Args:
            topology_id (:obj:`str`): ID of the Topology.
            topology_acl_json (:obj:`str`): ACL of the Topology in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._post(
            app='topology',
            endpoint='/v{}/topology/{}/acl'.format(self.api_version, topology_id),
            data=topology_acl_json,
        )
        return Command(self, response)

    def update_topology_permissions(self, body, topology_id, subject_id):
        """Update the permissions of a Topology for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            topology_id (:obj:`str:): ID of the Topology.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._post(
            app='topology',
            endpoint='/v{}/topology/{}/permissions/{}'.format(self.api_version, topology_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_subscription_acl(self, subscription_id):
        """Get the ACL of an Event Subscription.

        Args:
            subscription_id (:obj:`str`): ID of the Subscription.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='notification', endpoint='/v{}/eventsub/{}/acl'.format(self.api_version, subscription_id)
        )
        return Command(self, response)

    def set_subscription_acl(self, subscription_id, subscription_acl_json):
        """Set the ACL of an Event Subscription.

        Args:
            subscription_id (:obj:`str`): ID of the Subscription.
            subscription_acl_json (:obj:`str`): ACL of the Subscription in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification',
            endpoint='/v{}/eventsub/{}/acl'.format(self.api_version, subscription_id),
            data=subscription_acl_json,
        )
        return Command(self, response)

    def update_subscription_permissions(self, body, subscription_id, subject_id):
        """Update the permissions of an Event Subscription for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            subscription_id (:obj:`str:): ID of the Subscription.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification',
            endpoint='/v{}/eventsub/{}/permissions/{}'.format(self.api_version, subscription_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_provisioning_agent_acl(self, dpm_agent_id):
        """Get the ACL of a Provisioning Agent.

        Args:
            dpm_agent_id (:obj:`str`): ID of the Provisioning Agent.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='provisioning', endpoint='/v{}/dpmAgent/{}/acl'.format(self.api_version, dpm_agent_id))
        return Command(self, response)

    def set_provisioning_agent_acl(self, dpm_agent_id, dpm_agent_acl_json):
        """Set the ACL of a Provisioning Agent.

        Args:
            dpm_agent_id (:obj:`str`): ID of the Provisioning Agent.
            dpm_agent_acl_json (:obj:`str`): ACL of the Subscription in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/dpmAgent/{}/acl'.format(self.api_version, dpm_agent_id),
            data=dpm_agent_acl_json,
        )
        return Command(self, response)

    def update_provisioning_agent_permissions(self, body, dpm_agent_id, subject_id):
        """Update the permissions of a Provisioning Agent for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            dpm_agent_id (:obj:`str:): ID of the Provisioning Agent.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/dpmAgent/{}/permissions/{}'.format(self.api_version, dpm_agent_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_legacy_deployment_acl(self, deployment_id):
        """Get the ACL of a Deployment.

        Args:
            deployment_id (:obj:`str`): ID of the Deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='provisioning', endpoint='/v{}/deployment/{}/acl'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def set_legacy_deployment_acl(self, deployment_id, deployment_acl_json):
        """Set the ACL of a Deployment.

        Args:
            deployment_id (:obj:`str`): ID of the Deployment.
            deployment_acl_json (:obj:`str`): ACL of the Deployment in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/deployment/{}/acl'.format(self.api_version, deployment_id),
            data=deployment_acl_json,
        )
        return Command(self, response)

    def update_legacy_deployment_permissions(self, body, deployment_id, subject_id):
        """Update the permissions of a Deployment for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            deployment_id (:obj:`str:): ID of the Deployment.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/deployment/{}/permissions/{}'.format(self.api_version, deployment_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_scheduled_task_acl(self, scheduled_task_id):
        """Get the ACL of a Scheduled Task.

        Args:
            scheduled_task_id (:obj:`str`): ID of the Scheduled Task.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='scheduler', endpoint='/v{}/jobs/{}/acl'.format(self.api_version, scheduled_task_id))
        return Command(self, response)

    def set_scheduled_task_acl(self, scheduled_task_id, scheduled_task_acl_json):
        """Set the ACL of a Scheduled Task.

        Args:
            scheduled_task_id (:obj:`str`): ID of the Scheduled Task.
            scheduled_task_acl_json (:obj:`str`): ACL of the Scheduled Task in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='scheduler',
            endpoint='/v{}/jobs/{}/acl'.format(self.api_version, scheduled_task_id),
            data=scheduled_task_acl_json,
        )
        return Command(self, response)

    def update_scheduled_task_permissions(self, body, scheduled_task_id, subject_id):
        """Update the permissions of a Scheduled Task for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            scheduled_task_id (:obj:`str:): ID of the Scheduled Task.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='scheduler',
            endpoint='/v{}/jobs/{}/permissions/{}'.format(self.api_version, scheduled_task_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_alert_acl(self, alert_id):
        """Get the ACL of an Alert.

        Args:
            alert_id (:obj:`str`): ID of the Alert.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='notification', endpoint='/v{}/alerts/{}/acl'.format(self.api_version, alert_id))
        return Command(self, response)

    def set_alert_acl(self, alert_id, alert_acl_json):
        """Set the ACL of an Alert.

        Args:
            alert_id (:obj:`str`): ID of the Alert.
            alert_acl_json (:obj:`str`): ACL of the Alert in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification', endpoint='/v{}/alerts/{}/acl'.format(self.api_version, alert_id), data=alert_acl_json
        )
        return Command(self, response)

    def update_alert_permissions(self, body, alert_id, subject_id):
        """Update the permissions of an Alert for a specific subject.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            alert_id (:obj:`str:): ID of the Alert.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification',
            endpoint='/v{}/alerts/{}/permissions/{}'.format(self.api_version, alert_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def wait_for_job_status(self, job_id, status, timeout_sec=300):
        """Wait for job status.

        Args:
            job_id (:obj:`str`)
            status (:obj:`str`): Job status.
            timeout_sec (:obj:`int`): Timeout for wait, in seconds. Default: 300
        """

        def condition(job_id):
            current_status = self.get_current_job_status(job_id).response.json()['status']
            logger.debug('Status of job (id: %s) is %s ...', job_id, current_status)
            if current_status == 'INACTIVE_ERROR':
                raise JobInactiveError('Job status changed to INACTIVE_ERROR')
            return current_status == status

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for status.'.format(timeout))

        def success(time):
            logger.debug('Job reached desired status after %s s.', time)

        logger.debug('Job %s waiting for status %s ...', job_id, status)
        wait_for_condition(
            condition=condition,
            condition_kwargs={'job_id': job_id},
            timeout=timeout_sec,
            failure=failure,
            success=success,
        )

    def return_all_jobs(
        self,
        organization,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        removed=False,
        system=False,
        filter_text=None,
        job_search_operation='EQUALS',
        job_search_text=None,
        job_status=None,
        job_label=None,
        edge=False,
        executor_type=None,
        job_status_color=None,
        job_tag=None,
        with_wrapper=False,
        job_template=None,
        template_job_id=None,
        archived=False,
        draft_run=False,
    ):
        """Returns all jobs. Offset and length are deliberately set to default values because of their limited usage.

        Args:
            organization (:obj:`str`).
            offset (:obj:`int`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            removed (:obj:`bool`, optional): Default: ``False``
            system (:obj:`bool`, optional): Default: ``False``
            filter_text (:obj:`str`, optional): Default: ``None``
            job_search_operation (:obj:`str`, optional): Default: ``'EQUALS'``
            job_search_text (:obj:`str`, optional): Default: ``None``
            job_status (:obj:`str`, optional): Default: ``None``
            job_label (:obj:`str`, optional): Default: ``None``
            edge (:obj:`bool`, optional): Default: ``False``
            executor_type (:obj:`str`, optional): Default: ``None``
            job_status_color (:obj:`str`, optional): Default: ``None```
            job_tag (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``
            job_template (:obj:`str`, optional): Default: ``None``
            template_job_id (:obj:`str`, optional): ID of the Job Template. Default: ``None``
            archived (:obj:`bool`, optional): Default: ``False``
            draft_run (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/jobs'.format(self.api_version), params=params)
        return Command(self, response)

    def get_jobs_count(self, organization, removed, system):
        """Returns the number of jobs for the current user.

        Args:
            organization (:obj:`str`).
            removed (:obj:`bool`).
            system (:obj:`bool`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/jobs/count'.format(self.api_version), params=params)
        return Command(self, response)

    def get_jobs(self, body):
        """Returns Jobs for all give Job IDs.

        Args:
            body (:obj:`list`): A list of job IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/jobs'.format(self.api_version), data=body)
        return Command(self, response)

    def return_all_job_labels(self):
        """Returns all job labels

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/jobs/labels'.format(self.api_version))
        return Command(self, response)

    def get_jobs_by_status(
        self,
        organization,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        removed=False,
        system=False,
        filter_text=None,
        job_search_operation='EQUALS',
        job_search_text=None,
        job_status=None,
        edge=False,
        executor_type=None,
        job_tag=None,
        with_wrapper=False,
    ):
        """Get all jobs by status.

        Args:
            organization (:obj:`str`)
            offset (:obj:`int`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            removed (:obj:`bool`, optional): Default: ``False``
            system (:obj:`bool`, optional): Default: ``False``
            filter_text (:obj:`str`, optional): Default: ``None``
            job_search_operation (:obj:`str`, optional): Default: ``'EQUALS'``
            job_search_text (:obj:`str`, optional): Default: ``None``
            job_status (:obj:`str`, optional): Default: ``None``
            edge (:obj:`bool`, optional): Default: ``False``
            executor_type (:obj:`str`, optional): Default: ``None``
            job_tag (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/jobs/byStatus'.format(self.api_version)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_active_jobs(
        self,
        organization,
        pipeline_commit_id,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        template_job_id=None,
        job_template=None,
        draft_run=False,
        with_wrapper=False,
    ):
        """Returns all active Jobs for given Pipeline Commit ID.

        Args:
            organization (:obj:`str`)
            pipeline_commit_id (:obj:`str`)
            offset (:obj:`int`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            template_job_id (:obj:`str`, optional): ID of the Job Template. Default: ``None``
            job_template (:obj:`str`, optional): Default: ``None``
            draft_run (:obj:`bool`, optional): Default: ``False``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner', endpoint='/v{}/jobs/forPipelineCommit'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_job_run_logs(self, job_id, run_count, len=-1, offset=0, order='DESC'):
        """Return log messages for given job id and run.

        Args:
            job_id (:obj:`str`)
            run_count (:obj:`int`)
            len (:obj:`int`, optional): Default: ``-1``
            offset (:obj:`int`, optional): Default: ``0``
            order (:obj:`str`, optional): Default: ``DESC``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/job/logMessages'.format(self.api_version), params=params)
        return Command(self, response)

    def get_template_history(self, template_job_id, offset=None, len=None, with_total_count=False):
        """Returns Run History of a Job Template.

        Args:
            template_job_id (:obj:`str`): ID of the Job Template.
            offset (:obj:`int`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            with_total_count (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'template_job_id'))
        response = self._get(
            app='jobrunner', endpoint='/v{}/job/{}/runHistory'.format(self.api_version, template_job_id), params=params
        )
        return Command(self, response)

    def archive_templates(self, body):
        """Archive Job Template for all given Job Template IDs.

        Args:
            body (:obj:`list`): List of Job Template IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/archiveJobTemplates'.format(self.api_version), data=body
        )
        return Command(self, response)

    def create_job(self, body):
        """Create a new job.

        Args:
           body (:obj:`str`): Job in JSON format. Complies to Swagger NewJobJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='jobrunner', endpoint='/v{}/jobs'.format(self.api_version), data=body)
        return Command(self, response)

    def create_jobs(self, body):
        """Create a new job.

        Args:
           body (:obj:`list`): List of Jobs. Complies to Swagger NewJobJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='jobrunner', endpoint='/v{}/jobs/createJobs'.format(self.api_version), data=body)
        return Command(self, response)

    def create_and_start_job_instances(self, template_job_id, body, inherit_permissions=False):
        """Create and Start Job Instances from Job Template.

        Args:
            template_job_id (:obj:`str`): ID of the Job Template.
            body (:obj:`dict`): Job instance in JSON format. Complies to Swagger JobTemplateCreationInfoJson definition.
            inherit_permissions (:obj:`bool`, optional): Parameter to determine if the user wants to inherit the ACL
                                                         from the template instead of getting the default ACL for it.
                                                         Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'template_job_id', 'body'))
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/job/{}/createAndStartJobInstances'.format(self.api_version, template_job_id),
            data=body,
            params=params,
        )
        return Command(self, response)

    def create_and_start_job_instances_async(self, template_job_id, body, inherit_permissions=False):
        """Create and Start Job Instances from Job Template asynchronously.

        Args:
            template_job_id (:obj:`str`): ID of the Job Template.
            body (:obj:`dict`): Job instance in JSON format. Complies to Swagger JobTemplateCreationInfoJson definition.
            inherit_permissions (:obj:`bool`, optional): Parameter to determine if the user wants to inherit the ACL
                                                         from the template instead of getting the default ACL for it.
                                                         Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'template_job_id', 'body'))
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/job/{}/createAndStartJobInstancesAsync'.format(self.api_version, template_job_id),
            data=body,
            params=params,
        )
        return Command(self, response)

    def get_job(self, job_id):
        """Returns the job for given job id.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._get(app='jobrunner', endpoint='/v{}/job/{}'.format(self.api_version, job_id))
        return Command(self, response)

    def get_job_committed_offsets(self, job_id):
        """Returns the committed offsets for a given job id.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._get(app='jobrunner', endpoint='/v{}/job/{}/committedOffsets'.format(self.api_version, job_id))
        return Command(self, response)

    def get_job_latest_committed_offsets(self, job_id):
        """Returns the latest committed offsets for a given job id.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._get(
            app='jobrunner', endpoint='/v{}/job/{}/latestCommittedOffsets'.format(self.api_version, job_id)
        )
        return Command(self, response)

    def update_job(self, job_id, job_json):
        """Update a job.

        Args:
            job_id (:obj:`str`)
            job_json (:obj:`str`): Job in JSON format. Complies to Swagger JobJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/{}'.format(self.api_version, job_id), data=job_json)
        return Command(self, response)

    def upgrade_jobs(self, job_ids):
        """Upgrade a job to the latest version of pipeline.

        Args:
          job_ids (:obj:`list`): List of job ids to upgrade.

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        repsonse = self._post(app='jobrunner', endpoint='/v{}/jobs/upgradeJobs'.format(self.api_version), data=job_ids)
        return Command(self, repsonse)

    def delete_job(self, job_id, api_version=None):
        """Delete job.

        Args:
            job_id (:obj:`str`)
            api_version (:obj:`int`, optional): Control Hub API version. Default: :py:const:`DEFAULT_SCH_API_VERSION`

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        if api_version is None:
            api_version = self.api_version
        response = self._delete(app='jobrunner', endpoint='/v{}/job/{}'.format(api_version, job_id))
        return Command(self, response)

    def delete_jobs(self, job_ids_json):
        """Deletes Job for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/deleteJobs'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def cascade_delete_job_template(self, job_template_ids_json):
        """Deletes Job Template for all given Job Template IDs as well as cascade deleting all the child jobs.

        Args:
            job_template_ids_json (:obj:`str`): Job Template IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/jobs/deleteJobTemplates'.format(self.api_version),
            data=job_template_ids_json,
        )
        return Command(self, response)

    def import_jobs(
        self,
        jobs_file,
        update_pipeline_refs=True,
        update_num_instances=False,
        update_runtime_parameters=False,
        update_labels=False,
        update_migrate_offsets=True,
    ):
        """Import jobs from archived zip directory.

        Args:
            jobs_file (:obj:`file`): file containing the jobs.
            update_pipeline_refs (:obj:`boolean`, optional): Default: ``True``.
            update_num_instances (:obj:`boolean`, optional): Default: ``False``.
            update_runtime_parameters (:obj:`boolean`, optional): Default: ``False``.
            update_labels (:obj:`boolean`, optional): Default: ``False``.
            update_migrate_offsets (:obj:`boolean`, optional): Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'jobs_file'))
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/jobs/importJobs'.format(self.api_version),
            files={'file': jobs_file},
            params=params,
            headers={'content-type': None},
        )
        return Command(self, response)

    def import_jobs_from_json(
        self,
        body,
        force_import=False,
        update_pipeline_refs=True,
        update_num_instances=False,
        update_runtime_parameters=False,
        update_labels=False,
        update_migrate_offsets=True,
    ):
        """Import jobs from raw JSON.

        Args:
            body (:obj:`dict`): JSON representation of a job.
            force_import (:obj:`boolean`, optional): Default: ``False``.
            update_pipeline_refs (:obj:`boolean`, optional): Default: ``True``.
            update_num_instances (:obj:`boolean`, optional): Default: ``False``.
            update_runtime_parameters (:obj:`boolean`, optional): Default: ``False``.
            update_labels (:obj:`boolean`, optional): Default: ``False``.
            update_migrate_offsets (:obj:`boolean`, optional): Default: ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/importJobsFromJson'.format(self.api_version), data=body, params=params
        )
        return Command(self, response)

    def duplicate_job(self, job_id, body):
        """Duplicate an existing job.

        Args:
            job_id (:obj:`str`)
            body (:obj:`dict`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/job/{}/duplicate'.format(self.api_version, job_id), data=body
        )
        return Command(self, response)

    def export_jobs(self, body):
        """Export jobs as a compressed archive.

        Args:
            body (:obj:`list`): A list of job IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/jobs/exportJobs'.format(self.api_version), data=body)
        return Command(self, response)

    def get_jobs_status(self, body):
        """Return job status for all given job IDs.

        Args:
            body (:obj:`list`): A list of job IDs.

        Returns:
            A :obj:`dict` with job ID keys and job data as values.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/jobs/status'.format(self.api_version), data=body)
        return Command(self, response)

    def get_current_job_status(self, job_id):
        """Returns the current job status for given job id.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._get(app='jobrunner', endpoint='/v{}/job/{}/currentStatus'.format(self.api_version, job_id))
        return Command(self, response)

    def get_all_jobs_status(self, organization, offset, len, with_wrapper=False):
        """Return all job status.

        Args:
            organization (:obj:`str`).
            offset (:obj:`str`).
            len (:obj:`str`).
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/jobs/status'.format(self.api_version), params=params)
        return Command(self, response)

    def get_job_status_history(self, job_id, offset, len, with_wrapper=False):
        """Returns history of Job Status for given Job ID.

        Args:
            job_id (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='jobrunner', endpoint='/v{}/job/{}/history'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_job_tags_bulk(self, job_ids):
        """Returns job tags for a list of jobs

        Args:
            job_ids (:obj:`list` of :obj:`str`): List of Job IDs for which we need to fetch job tags.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/jobTagsBulk'.format(self.api_version), data=job_ids)
        return Command(self, response)

    def get_saql_job_status_history(self, job_id, search, offset, len):
        """Returns history of Job Status for given Job ID.

        Args:
            job_id (:obj:`str`)
            search (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='jobrunner', endpoint='/v{}/saql/jobs/search/{}/runs'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_job_status_history_for_run(self, job_status_id, offset, len, with_wrapper=False):
        """Returns Job Status History of a Job for a particular run.

        Args:
            job_status_id (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_status_id'))
        response = self._get(
            app='jobrunner',
            endpoint='/v{}/job/{}/jobStatusHistory'.format(self.api_version, job_status_id),
            params=params,
        )
        return Command(self, response)

    def get_job_acl(self, job_id):
        """Get job ACL.

        Args:
            job_id (:obj:`str`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/job/{}/acl'.format(self.api_version, job_id))
        return Command(self, response)

    def set_job_acl(self, job_id, job_acl_json):
        """Update job ACL.

        Args:
            job_id (:obj:`str`).
            job_acl_json (:obj:`str`): Job ACL in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/job/{}/acl'.format(self.api_version, job_id), data=job_acl_json
        )
        return Command(self, response)

    def get_draft_run_job_for_pipeline_id(self, pipeline_id):
        """Get the draft run job for a given pipeline ID.

        Args:
            pipeline_id (:obj:`str`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner', endpoint='/v{}/jobs/draftRunJobForPipelineId'.format(self.api_version), params=params
        )
        return Command(self, response)

    def validate_access_to_job(self, job_id):
        """Validate whether a user has read permissions for a given job ID or not.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/{}/validateAccess'.format(self.api_version, job_id))
        return Command(self, response)

    def start_job(self, job_id, start_and_capture_snapshot=False):
        """Starts the job.

        Args:
            job_id (:obj:`str`)
            start_and_capture_snapshot (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.JobStartStopCommand`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._post(
            app='jobrunner', endpoint='/v{}/job/{}/start'.format(self.api_version, job_id), params=params
        )
        return JobStartStopCommand(self, response)

    def start_jobs(self, job_ids_json):
        """Starts Job for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/startJobs'.format(self.api_version), data=job_ids_json
        )
        return StartJobsCommand(self, response)

    def stop_job(self, job_id):
        """Stops the job.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.JobStartStopCommand`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/{}/stop'.format(self.api_version, job_id))
        return JobStartStopCommand(self, response)

    def force_stop_job(self, job_id):
        """Force stop Job for given Job ID.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.JobStartStopCommand`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/{}/forceStop'.format(self.api_version, job_id))
        return JobStartStopCommand(self, response)

    def stop_jobs(self, job_ids_json):
        """Stops Job for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/stopJobs'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def force_stop_jobs(self, job_ids_json):
        """Force Stops Job for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/forceStopJobs'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def job_acknowledge_error(self, job_id):
        """Acknowledge Error for given Job ID.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/{}/acknowledgeError'.format(self.api_version, job_id))
        return Command(self, response)

    def jobs_acknowledge_errors(self, job_ids_json):
        """Acknowledge Errors for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/acknowledgeErrors'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def sync_job(self, job_id):
        """Sync job.

        Args:
            job_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/job/{}/sync'.format(self.api_version, job_id))
        return Command(self, response)

    def sync_jobs(self, job_ids_json):
        """Sync Job for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/syncJobs'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def balance_jobs(self, job_ids_json):
        """Balance Jobs for all given Job IDs.

        Args:
            job_ids_json (:obj:`str`): Job IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/jobs/balanceJobs'.format(self.api_version), data=job_ids_json
        )
        return Command(self, response)

    def update_job_policies(self, body, organization=None):
        """Update a Job's configured Policies.

        Args:
            body (:obj:`dict`)
            organization (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(app='jobrunner', endpoint='/v{}/jobPolicy'.format(self.api_version), data=body)
        return Command(self, response)

    def get_job_policies(self, job_id, organization=None):
        """Get a Job's configured Policies.

        Args:
            job_id (:obj:`str`)
            organization (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='jobrunner', endpoint='/v{}/jobPolicy/{}'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_job_sankey_metrics(
        self, job_id, metric_type, pipeline_version, sdc_id, time_filter_condition, include_error_count
    ):
        """Get a Job's metrics.

        Args:
            job_id (:obj:`str`)
            metric_type (:obj:`str`)
            pipeline_version (:obj:`str`)
            sdc_id (:obj:`str`)
            time_filter_condition (:obj:`str`)
            include_error_count (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries', endpoint='/v{}/metrics/job/{}/sankey'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_job_time_series_metrics(self, body, time_filter_condition, limit=1000):
        """Get a Job's time series metrics.

        Args:
            body (:obj:`dict`)
            time_filter_condition (:obj:`str`)
            limit (:obj:`str`, optional): Default: ``1000``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(
            app='timeseries', endpoint='/v{}/metrics/query'.format(self.api_version), params=params, data=body
        )
        return Command(self, response)

    def reset_jobs_offset(self, job_ids):
        """Reset all pipeline offsets for given job ids.

        Args:
            job_ids (:obj:`list`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/jobs/resetOffset'.format(self.api_version), data=job_ids)
        return Command(self, response)

    def upload_job_offset(self, job_id, offset_file):
        """Upload offset for a given job.

        Args:
            job_id (:obj:`str`)
            offset_file (:obj:`file`): File containing offsets.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/job/{}/uploadOffset'.format(self.api_version, job_id),
            files={'file': offset_file},
            headers={'content-type': None},
        )
        return Command(self, response)

    def upload_job_offset_as_json(self, job_id, offset_json):
        """Upload offset for a given job as json.

        Args:
            job_id (:obj:`str`)
            offset_json (:obj:`dict`): offsets json.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/job/{}/uploadOffsetAsJson'.format(self.api_version, job_id),
            data=offset_json,
        )
        return Command(self, response)

    def list_job_sets(self, search=None, page=None, size=None, sort=None):
        """Returns a list of Job-Sets.

        Args:
            search (:obj:`str`, optional): The search query. Default: ``None``.
            page (:obj:`int`, optional): Zero Based Page Index. Default: ``None``.
            size (:obj:`int`, optional): The size of the page to be returned. Default: ``None``.
            sort (:obj:`str` or list of :obj:`str`, optional): Sorting criteria. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner2', endpoint='/v{}/job-sets'.format(DEFAULT_JOBRUNNER2_API_VERSION), params=params
        )
        return Command(self, response)

    def create_job_set(self, job_set_json):
        """Create a Job-Set.

        Args:
            job_set_json (:obj:`dict`): The Job-Set json.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2', endpoint='/v{}/job-sets'.format(DEFAULT_JOBRUNNER2_API_VERSION), data=job_set_json
        )
        return Command(self, response)

    def get_job_set(self, job_set_id):
        """Get a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2', endpoint='/v{}/job-sets/{}'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id))
        )
        return Command(self, response)

    def update_job_set(self, job_set_id, job_set_json):
        """Update a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_set_json (:obj:`dict`): The Job-Set JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            data=job_set_json,
        )
        return Command(self, response)

    def delete_job_set(self, job_set_id):
        """Delete a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='jobrunner2', endpoint='/v{}/job-sets/{}'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id))
        )
        return Command(self, response)

    def update_pipeline_commit_id_in_job_set(self, job_set_id, pipeline_id, new_commit_id_json):
        """Update Pipeline Commit ID of Job Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            pipeline_id (:obj:`str`): The Pipeline ID.
            new_commit_id_json (:obj:`str`): The New Commit ID JSON data.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_set_id', 'pipeline_id'))
        response = self._post(
            app='jobrunner2',
            endpoint='v{}/job-sets/{}/pipeline/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(pipeline_id)
            ),
            data=new_commit_id_json,
        )
        return Command(self, response)

    def clone_job_sets(self, job_set_id, job_set_json):
        """Clone a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_set_json (:obj:`dict`): The Job-Set JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/clone'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            data=job_set_json,
        )
        return Command(self, response)

    def list_jobs_in_job_set(self, job_set_id, search=None, page=None, size=None, sort=None):
        """List jobs in a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            search (:obj:`str`, optional): The search query. Default: ``None``.
            page (:obj:`int`, optional): Zero Based Page Index. Default: ``None``.
            size (:obj:`int`, optional): The size of the page to be returned. Default: ``None``.
            sort (:obj:`str` or list of :obj:`str`, optional): Sorting criteria. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_set_id'))
        response = self._get(
            app='jobrunner2',
            endpoint='v{}/job-sets/{}/jobs'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            params=params,
        )
        return Command(self, response)

    def add_job_to_job_set(self, job_set_id, job_json):
        """Add a job to a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_json (:obj:`dict`): The Job's JSON data.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/jobs/'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            data=job_json,
        )
        return Command(self, response)

    def get_job_from_job_set(self, job_set_id, job_id):
        """Get a job from a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_id (:obj:`str`): The Job's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/jobs/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(job_id)
            ),
        )
        return Command(self, response)

    def update_job_in_job_set(self, job_set_id, job_id, job_json):
        """Update a job in a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_id (:obj:`str`): The Job's ID.
            job_json (:obj:`dict`): The Job's JSON data.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/jobs/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(job_id)
            ),
            data=job_json,
        )
        return Command(self, response)

    def delete_job_in_job_set(self, job_set_id, job_id):
        """Delete a job in a Job-Set.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_id (:obj:`str`): The Job's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/jobs/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(job_id)
            ),
        )
        return Command(self, response)

    def update_job_set_submission(self, job_set_id, job_set_submission_json):
        """Update a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_set_submission_json (:obj:`dict`): The Job-Set Submission JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/run.update'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            data=job_set_submission_json,
        )
        return Command(self, response)

    def stop_job_set_submission(self, job_set_id):
        """Stop a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/run.stop'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
        )
        return Command(self, response)

    def start_job_set_submission(self, job_set_id, job_set_submission_json):
        """Start a Job-Set submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_set_submission_json (:obj:`dict`): The Job-Set Submission JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/run.start'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            data=job_set_submission_json,
        )
        return Command(self, response)

    def refresh_job_set_submission(self, job_set_id):
        """Refresh a Job-Set submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/run.refresh'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
        )
        return Command(self, response)

    def get_job_set_submission(self, job_set_id):
        """Get a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/job-sets/{}/run'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
        )
        return Command(self, response)

    def get_job_set_submissions(self, search=None, page=None, size=None, sort=None):
        """Get a Job-Set Submissions.

        Args:
            search (:obj:`str`, optional): The search query. Default: ``None``.
            page (:obj:`int`, optional): Zero Based Page Index. Default: ``None``.
            size (:obj:`int`, optional): The size of the page to be returned. Default: ``None``.
            sort (:obj:`str` or list of :obj:`str`, optional): Sorting criteria. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner2', endpoint='/v{}/job-sets.runs'.format(DEFAULT_JOBRUNNER2_API_VERSION), params=params
        )
        return Command(self, response)

    def stop_job_submission_from_job_set_submission(self, job_set_id, job_id):
        """Stop a Job Submission from a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_id (:obj:`str`): The Job's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/job-set/{}/jobs/{}/run.stop'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(job_id)
            ),
        )
        return Command(self, response)

    def get_job_submission_from_job_set_submission(self, job_set_id, job_id):
        """Get a Job Submission from a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            job_id (:obj:`str`): The Job's ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/job-set/{}/jobs/{}/run'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id), quote_plus(job_id)
            ),
        )
        return Command(self, response)

    def list_job_submissions_from_job_set_submission(self, job_set_id, search=None, page=None, size=None, sort=None):
        """List Job Submissions from a Job-Set Submission.

        Args:
            job_set_id (:obj:`str`): The Job-Set ID.
            search (:obj:`str`, optional): The search query. Default: ``None``.
            page (:obj:`int`, optional): Zero Based Page Index. Default: ``None``.
            size (:obj:`int`, optional): The size of the page to be returned. Default: ``None``.
            sort (:obj:`str` or list of :obj:`str`, optional): Sorting criteria. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_set_id'))
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/job-set/{}/jobs.runs'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(job_set_id)),
            params=params,
        )
        return Command(self, response)

    def get_access_control_lists_for_objects(self, object_type, object_ids):
        """Get the Access Control Lists for Objects.

        Args:
            object_type (:obj:`str`): The Object Type.
            object_ids (:obj:`dict`): IDs of objects to retrieve their ACLs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # Note: This call does not make any changes, it is a POST to be able to query for several objects without
        # running into URL length limits.
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}'.format(DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type)),
            data=object_ids,
        )
        return Command(self, response)

    def get_objects_for_user_filtered_with_privileges(self, object_type, user, privileges, privileges_json):
        """Get Objects for User filtered with Privileges.

        Args:
            object_type (:obj:`str`): The Object Type.
            user (:obj:`str`): User ID.
            privileges (:obj:`str` or list of :obj:`str`): A list of Privileges.
            privileges_json (:obj:`dict`): The Privileges JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        privileges = ','.join(privileges)
        endpoint = 'v{}/access-control/objects/{}/users/{}/filter-with-privileges/{}'.format(
            DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type), quote_plus(user), privileges
        )

        # Note: This call does not make any changes, it is a POST to be able to query for several objects without
        # running into URL length limits.
        response = self._post(app='jobrunner2', endpoint=endpoint, data=privileges_json)
        return Command(self, response)

    def revoke_permissions_for_object_type(self, object_type, u_access_json):
        """Revoke the specified privileges to the specified users and groups for the specified object.

        Args:
            object_type (:obj:`str`): The Object Type.
            u_access_json (:obj:`dict`): Specifies a list of IDs, the users and groups, and privileges.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}/revoke'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type)
            ),
            data=u_access_json,
        )
        return Command(self, response)

    def grant_permissions_for_object_type(self, object_type, u_access_json):
        """Grant the specified privileges to the specified users and groups for the specified object.

        Args:
            object_type (:obj:`str`): The Object Type.
            u_access_json (:obj:`dict`): Specifies a list of IDs, the users and groups, and privileges.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}/grant'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type)
            ),
            data=u_access_json,
        )
        return Command(self, response)

    def change_owner_of_object(self, object_type, new_owner, object_ids):
        """Change the owner of the specified object.

        Args:
            object_type (:obj:`str`): The Object Type.
            new_owner (:obj:`str`): New Owner ID.
            object_ids (:obj:`dict`): IDs of objects to change the owner.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}/change-owner/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type), quote_plus(new_owner)
            ),
            data=object_ids,
        )
        return Command(self, response)

    def get_privileges_of_object_type(self, object_type):
        """Get a Job-Set Submission.

        Args:
            object_type (:obj:`str`): The Object Type.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/access-control/privileges/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type)
            ),
        )
        return Command(self, response)

    def get_objects_for_user(self, object_type, user):
        """Get Objects a User Has Access to.

        Args:
            object_type (:obj:`str`): The Object Type.
            user (:obj:`str`): User ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}/users/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type), quote_plus(user)
            ),
        )
        return Command(self, response)

    def get_objects_for_group(self, object_type, group):
        """Get Objects a Group Has Access to.

        Args:
            object_type (:obj:`str`): The Object Type.
            group (:obj:`str`): Group ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2',
            endpoint='/v{}/access-control/objects/{}/groups/{}'.format(
                DEFAULT_JOBRUNNER2_API_VERSION, quote_plus(object_type), quote_plus(group)
            ),
        )
        return Command(self, response)

    def get_object_types(self):
        """Get all Object Types.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner2', endpoint='/v{}/access-control/object-types'.format(DEFAULT_JOBRUNNER2_API_VERSION)
        )
        return Command(self, response)

    def get_job_set_history(self, search=None, page=None, size=None, sort=None):
        """Get Job-Set History.

        Args:
            search (:obj:`str`, optional): The search query. Default: ``None``.
            page (:obj:`int`, optional): Zero Based Page Index. Default: ``None``.
            size (:obj:`int`, optional): The size of the page to be returned. Default: ``None``.
            sort (:obj:`str` or list of :obj:`str`, optional): Sorting criteria. Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner2', endpoint='/v{}/history'.format(DEFAULT_JOBRUNNER2_API_VERSION), params=params
        )
        return Command(self, response)

    def get_job_sequence_acl_audits_list(
        self, organization_id=None, offset=None, len=None, sort_field=None, sort_order=None
    ):
        """Get all user actions for given Organization ID.

        Args:
            organization_id (:obj:`str`, optional): The Organization ID. Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='sequencing', endpoint='/v{}/sequencing/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_all_job_sequences(self, organization=None, len=None, offset=None, order_by='NAME', order='ASC'):
        """Get all job sequences.

        Args:
            organization (:obj:`str`): Default: ``None``.
            len (:obj:`str`): Default: ``None``.
            offset (:obj:`str`): Default: ``None``.
            order_by (:obj:`str`): Default: ``NAME``.
            order (:obj:`str`): The sort. Default: ``ASC``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='sequencing', endpoint='/v{}/sequencing'.format(self.api_version), params=params)
        return Command(self, response)

    def get_job_sequence(self, sequence_id):
        """Get sequence with given ID.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='sequencing', endpoint='/v{}/sequencing/{}'.format(self.api_version, sequence_id))
        return Command(self, response)

    def get_job_sequence_for_job_id(self, job_id):
        """Get Job Sequence for the corresponding Job ID.

        Args:
            job_id (:obj:`str`): The Job ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='sequencing', endpoint='/v{}/sequencing/job/{}/sequence'.format(self.api_version, job_id)
        )
        return Command(self, response)

    def get_job_sequence_log_history(
        self,
        sequence_id,
        offset=None,
        len=None,
        log_type=None,
        log_level=None,
        last_run_only=None,
        run_id=None,
        from_date=None,
        to_date=None,
    ):
        """Get the history log for a given sequence ID.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            log_type (:obj:`str`, optional): Default: `None`.
            log_level (:obj:`str`, optional): Default: `None`.
            last_run_only (:obj:`str`, optional): Default: `None`.
            run_id (:obj:`str`, optional): Default: `None`.
            from_date (:obj:`str`, optional): Default: `None`.
            to_date (:obj:`str`, optional): Default: `None`.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sequence_id'))
        response = self._get(
            app='sequencing',
            endpoint='/v{}/sequencing/{}/historyLog'.format(self.api_version, sequence_id),
            params=params,
        )
        return Command(self, response)

    def delete_job_sequence_history_logs(self, history_log_ids):
        """Delete the history logs for a given sequence ID.

        Args:
            history_log_ids (:obj:`list` of :obj:`str`): The History Log IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing',
            endpoint='/v{}/sequencing/deleteHistoryLogs'.format(self.api_version),
            data=history_log_ids,
        )
        return Command(self, response)

    def get_all_run_ids_of_job_sequence(self, sequence_id, len=None, offset=None):
        """Get the history log for a given sequence ID.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='sequencing',
            endpoint='/v{}/sequencing/{}/getAllRunIds'.format(self.api_version, sequence_id),
        )
        return Command(self, response)

    def update_job_sequence(self, sequence_id, job_sequence_json):
        """Update the basic information of a job sequence.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            job_sequence_json (:obj:`dict`): The Job Sequence data we wish to update the job sequence with.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(
            app='sequencing',
            endpoint='/v{}/sequencing/{}'.format(self.api_version, sequence_id),
            data=job_sequence_json,
        )
        return Command(self, response)

    def delete_job_sequence(self, sequence_id):
        """Delete the job sequence.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='sequencing', endpoint='/v{}/sequencing/{}'.format(self.api_version, sequence_id))
        return Command(self, response)

    def delete_job_sequences(self, sequence_ids):
        """Delete the job sequences.

        Args:
            sequence_ids (a :obj:`list` of :obj:`str`): The Sequence IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing/deleteSequences'.format(self.api_version), data=sequence_ids
        )
        return Command(self, response)

    def create_job_sequence(self, job_sequence_json):
        """Create new empty job Sequence.

        Args:
            job_sequence_json (:obj:`dict`): The Job Sequence JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing'.format(self.api_version), data=job_sequence_json
        )
        return Command(self, response)

    def add_step_jobs_to_job_sequence(self, sequence_id, step_job_json):
        """Add step jobs to a sequence.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            step_job_json (:obj:`dict`): The Job Sequence JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing',
            endpoint='/v{}/sequencing/{}/addStepJobs'.format(self.api_version, sequence_id),
            data=step_job_json,
        )
        return Command(self, response)

    def move_step_job_in_job_sequence(self, sequence_id, step_job_instance_id, from_step_job_id, to_step_job_id):
        """Move a step job instance to another step job of a sequence.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            step_job_instance_id (:obj:`str`): The step job instance ID.
            from_step_job_id (:obj:`str`): The from step job ID.
            to_step_job_id (:obj:`str`): The to step job ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing',
            endpoint='/v{}/sequencing/{}/moveStepJobInstance/{}/{}/{}'.format(
                self.api_version, sequence_id, step_job_instance_id, from_step_job_id, to_step_job_id
            ),
        )
        return Command(self, response)

    def run_job_sequence(self, sequence_id, step_number=1, single_step=False):
        """Runs the sequence with given id.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            step_number (:obj:`int`): The Step Number to execute.
            single_step (:obj:`bool`): Whether to execute a single step or not.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'sequence_id'))
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing/{}/run'.format(self.api_version, sequence_id), params=params
        )
        return Command(self, response)

    def stop_job_sequence(self, sequence_id):
        """Stops the sequence with given id.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing/{}/stop'.format(self.api_version, sequence_id)
        )
        return Command(self, response)

    def enable_job_sequence(self, sequence_id):
        """Enable the sequence with given id.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing/{}/enable'.format(self.api_version, sequence_id)
        )
        return Command(self, response)

    def disable_job_sequence(self, sequence_id):
        """Disable the sequence with given id.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing', endpoint='/v{}/sequencing/{}/disable'.format(self.api_version, sequence_id)
        )
        return Command(self, response)

    def update_steps_of_job_sequence(self, sequence_id, update_step_json):
        """Update generic info of the steps of a sequence.

        Args:
            sequence_id (:obj:`str`): The Sequence ID.
            update_step_json (:obj:`dict`): The update step JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing',
            endpoint='/v{}/sequencing/{}/updateSteps'.format(self.api_version, sequence_id),
            data=update_step_json,
        )
        return Command(self, response)

    def mark_job_as_finished(self, job_id, step_job_json):
        """Mark a job in a sequence as finished.

        Args:
            job_id (:obj:`str`): The Job ID.
            step_job_json (:obj:`dict`): The Step Job JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='sequencing',
            endpoint='/v{}/sequencing/job/{}/event'.format(self.api_version, job_id),
            data=step_job_json,
        )
        return Command(self, response)

    def get_all_registered_engines(
        self, organization, executor_type, edge, label, version, offset, len_, order_by, order, with_wrapper=False
    ):
        """Gets all registered Engines.

        Args:
            organization (:obj:`str`)
            executor_type (:obj:`str`)
            edge (:obj:`str`)
            label (:obj:`str`)
            version (:obj:`str`)
            offset (:obj:`str`)
            len_ (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/sdcs'.format(self.api_version), params=params)
        return Command(self, response)

    def get_engine(self, engine_id):
        """Get a specific registered Engine by ID.

        Args:
            engine_id (:obj:`str`): the ID of the engine to retrieve.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{api_version}/sdc/{sdc_id}'.format(api_version=self.api_version, sdc_id=engine_id)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def delete_non_registered_components(self, organization, executor_type):
        """Delete auth tokens for engines that have been unregistered.

        Args:
            organization (:obj:`str`)
            executor_type (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='security',
            endpoint='/v{}/organization/{}/components/deleteNonRegistered/{}'.format(
                self.api_version, organization, executor_type
            ),
        )
        return Command(self, response)

    def get_all_registered_executor_labels(
        self, organization, executor_type, edge=False, offset=0, len=-1, with_wrapper=False
    ):
        """Return labels for all registered SDC instances.

        Args:
            organization (:obj:`str`)
            executor_type (:obj:`str`)
            edge (:obj:`bool`, optional): Default: ``False``
            offset (:obj:`int`, optional): Default: ``0``
            len (:obj:`int`, optional): Default: ``-1``
            with_wrapper (:obj:`bool`): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/sdcs/labels'.format(self.api_version), params=params)
        return Command(self, response)

    def get_all_registered_executor_versions(
        self, organization, executor_type, edge=False, offset=0, len=-1, with_wrapper=False
    ):
        """Return versions for all registered SDC instances.

        Args:
            organization (:obj:`str`)
            executor_type (:obj:`str`)
            edge (:obj:`bool`, optional): Default: ``False``
            offset (:obj:`int`, optional): Default: ``0``
            len (:obj:`int`, optional): Default: ``-1``
            with_wrapper (:obj:`bool`): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/sdcs/versions'.format(self.api_version), params=params)
        return Command(self, response)

    def get_sdc(self, data_collector_id):
        """Return SDC for given SDC ID.

        Args:
            data_collector_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/sdc/{}'.format(self.api_version, data_collector_id))
        return Command(self, response)

    def delete_sdc(self, data_collector_id):
        """Delete SDC for given SDC ID.

        Args:
            data_collector_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='jobrunner', endpoint='/v{}/sdc/{}'.format(self.api_version, data_collector_id))
        return Command(self, response)

    def update_sdc_labels(self, data_collector_id, data_collector_json):
        """Update labels for given SDC ID.

        Args:
            data_collector_id (:obj:`str`)
            data_collector_json (:obj:`str`): Data collector in JSON format. Complies to Swagger SDCJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/sdc/{}/updateLabels'.format(self.api_version, data_collector_id),
            data=data_collector_json,
        )
        return Command(self, response)

    def get_sdc_labels(self, data_collector_id):
        """Returns all labels assigned to SDC.

        Args:
            data_collector_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/sdc/{}/labels'.format(self.api_version, data_collector_id))
        return Command(self, response)

    def get_pipelines_running_in_sdc(self, data_collector_id):
        """Returns pipelines running inside an sdc.

        Args:
            data_collector_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='jobrunner', endpoint='/v{}/sdc/{}/pipelines'.format(self.api_version, data_collector_id)
        )
        return Command(self, response)

    def balance_data_collectors(self, body):
        """Balance all jobs running on given Data Collectors.

        Args:
            body (:obj:`list`): List of pipeline ids.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='jobrunner', endpoint='/v{}/jobs/balanceSDCs'.format(self.api_version), data=body)
        return Command(self, response)

    def update_sdc_resource_thresholds(self, data_collector_id, data_collector_json):
        """Update data collector resource thresholds.

        Args:
            data_collector_id (:obj:`str`)
            data_collector_json (:obj:`str`): Data collector in JSON format. Complies to Swagger SDCJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/sdc/{}/updateSdcResourceThresholds'.format(self.api_version, data_collector_id),
            data=data_collector_json,
        )
        return Command(self, response)

    def clear_pipelines_committed_from_data_collector(self, data_collector_id):
        """Clear pipelines committed set for given Data Collector Instance.

        Args:
            data_collector_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/sdc/clearPipelinesCommitted/{}'.format(self.api_version, data_collector_id)
        )
        return Command(self, response)

    def get_all_job_tags(self, organization, parent_id=None, offset=None, len=None, order=None):
        """Get job tags for a given organization.

        Args:
            organization (:obj:`str`)
            parent_id (:obj:`str`, optional): Default: ``None``
            offset (:obj:`int`, optional): Default: ``None``
            len (obj:`int`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/jobs/tags'.format(self.api_version), params=params)
        return Command(self, response)

    def get_draft_runs_by_query(self, org_id, search, order_by=None, offset=None, len=None):
        """Get all jobs that match query.

        Args:
            org_id (:obj:`str`)
            search (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/search/draftRuns'.format(self.api_version)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    @wait_and_retry_on_http_error
    def get_draft_run_logs(self, engine_id, engine_pipeline_id, tunneling_instance_id, ending_offset=-1):
        """Get the logs for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            engine_pipeline_id (:obj:`str`): Engine pipeline ID.
            tunneling_instance_id (:obj:`str`): Tunneling connection.
            ending_offset (:obj:`int`, optional): Offset of the ending of the logs. Default: ``-1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('engine_id', 'tunneling_instance_id', 'self'))
        params["pipeline"] = engine_pipeline_id
        endpoint = 'v{}/system/logs'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        return Command(self, response)

    @wait_and_retry_on_http_error
    def get_draft_run_snapshots(self, engine_id, engine_pipeline_id, job_id, tunneling_instance_id, job_run_count=1):
        """Get the snapshots for the draft run.

        Args:
            engine_id (:obj:`str`): Engine ID.
            engine_pipeline_id (:obj:`str`): Engine pipeline ID.
            job_id (:obj:`str`): Job ID.
            tunneling_instance_id (:obj:`str`): Tunneling connection.
            job_run_count (:obj:`int`, optional): Default: ``1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(
            parameters=locals(), exclusions=('engine_id', 'engine_pipeline_id', 'tunneling_instance_id', 'self')
        )
        endpoint = 'v{}/pipeline/{}/snapshots'.format(self.api_version, engine_pipeline_id)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        return Command(self, response)

    @wait_and_retry_on_http_error
    def get_snapshot_data(
        self, engine_id, engine_pipeline_id, snapshot_id, job_id, tunneling_instance_id, job_run_count=1
    ):
        """Get snapshot data.

        Args:
            engine_id (:obj:`str`): Engine ID.
            engine_pipeline_id (:obj:`str`): Engine pipeline ID.
            snapshot_id (:obj:`str`): Snapshot ID.
            job_id (:obj:`str`): Job ID.
            tunneling_instance_id (:obj:`str`): Tunneling connection.
            job_run_count (:obj:`int`, optional): Default: ``1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(
            parameters=locals(),
            exclusions=('engine_id', 'engine_pipeline_id', 'tunneling_instance_id', 'snapshot_id', 'self'),
        )
        endpoint = 'v{}/pipeline/{}/snapshot/{}'.format(self.api_version, engine_pipeline_id, snapshot_id)
        response = self._get_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        return Command(self, response)

    @wait_and_retry_on_http_error
    def generate_snapshot(self, engine_id, engine_pipeline_id, snapshot_label, tunneling_instance_id, batch_size=50000):
        """Generate a snapshot.

        Args:
            engine_id (:obj:`str`): Engine ID.
            engine_pipeline_id (:obj:`str`): Engine pipeline ID.
            snapshot_label (:obj:`str`): Snapshot label.
            tunneling_instance_id (:obj:`str`): Tunneling connection.
            batch_size(:obj:`int`, optional): Default: ``50000``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(
            parameters=locals(), exclusions=('engine_id', 'engine_pipeline_id', 'tunneling_instance_id', 'self')
        )
        current_gmt = gmtime()
        time_stamp = calendar.timegm(current_gmt)
        endpoint = 'v{}/pipeline/{}/snapshot/snapshot{}'.format(self.api_version, engine_pipeline_id, time_stamp)
        response = self._put_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        return Command(self, response)

    @wait_and_retry_on_http_error
    def remove_snapshot(self, engine_id, engine_pipeline_id, snapshot_id, tunneling_instance_id, job_run_count=1):
        """Remove a snapshot.

        Args:
            engine_id (:obj:`str`): Engine ID.
            engine_pipeline_id (:obj:`str`): Engine pipeline ID.
            snapshot_id (:obj:`str`): Snapshot ID.
            tunneling_instance_id (:obj:`str`): Tunneling connection.
            job_run_count (:obj:`int`, optional): Default: ``1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(
            parameters=locals(),
            exclusions=('engine_id', 'engine_pipeline_id', 'snapshot_id', 'tunneling_instance_id', 'self'),
        )
        endpoint = 'v{}/pipeline/{}/snapshot/{}'.format(self.api_version, engine_pipeline_id, snapshot_id)
        response = self._delete_via_tunneling(
            endpoint=endpoint, tunneling_instance_id=tunneling_instance_id, engine_id=engine_id, params=params
        )
        return Command(self, response)

    def get_jobs_by_query(self, org_id, search, order_by=None, offset=None, len=None):
        """Get all jobs that match query.

        Args:
            org_id (:obj:`str`)
            search (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/search'.format(self.api_version)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_saql_fav_job(self, search_id):
        """Creates a favorite saql job search query.
            In other words, it stars an existing job search
            query.

        Args:
            search_id (:obj:`str`): ID of aql search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/savedFilters/fav'.format(self.api_version)
        response = self._post(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_saql_job_search(self, aql_search_json):
        """Create a saql job search query.

        Args:
            aql_search_json (:obj:`str`): Aql search in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/savedFilters'.format(self.api_version)
        response = self._post(app='jobrunner', endpoint=endpoint, data=aql_search_json)
        return Command(self, response)

    def update_saql_job_search(self, search_id, aql_search_json):
        """Update a saql job search query.

        Args:
            search_id (:obj:`str`): ID of aql search object.
            aql_search_json (:obj:`str`): Aql search in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/saql/jobs/savedFilters/{}'.format(self.api_version, search_id)
        response = self._put(app='jobrunner', endpoint=endpoint, data=aql_search_json)
        return Command(self, response)

    def get_saql_job_searches(self, name, type, offset=None, len=None, order_by='ASC'):
        """Get all saql job searches that match the name.

        Args:
            name (:obj:`str`) Name of aql search object.
            type (:obj:`str`) Type of aql search object, limited to ``'JOB_INSTANCE'``, ``'JOB_TEMPLATE'`` and
                ``'JOB_DRAFT_RUN'``.
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'ASC'``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/savedFilters'.format(self.api_version)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def remove_saql_job_search(self, search_id):
        """Remove a job search.

        Args:
            search_id (:obj:`str`): ID of aql search object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/saql/jobs/savedFilters'.format(self.api_version)
        response = self._delete(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_job_templates_by_query(self, org_id, search, order_by=None, offset=None, len=None):
        """Get all jobs that match query.

        Args:
            org_id (:obj:`str`)
            search (:obj:`str`)
            order_by (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions='self')
        endpoint = '/v{}/saql/jobs/search/templates'.format(self.api_version)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def return_all_provisioning_agents(
        self, organization, offset, len, order_by, order, version=None, with_wrapper=False
    ):
        """Returns all provisioning agents.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            version (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='provisioning', endpoint='/v{}/dpmAgents'.format(self.api_version), params=params)
        return Command(self, response)

    def return_all_provisioning_agent_versions(self, organization, offset, len, with_wrapper=False):
        """Returns the versions of all provisioning agents.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='v{}/dpmAgents/versions'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_provisioning_agent(self, agent_id):
        """Returns a provisioning agent by id.

        Args:
            agent_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='provisioning', endpoint='/v{}/dpmAgent/{}'.format(self.api_version, agent_id))
        return Command(self, response)

    def delete_provisioning_agent(self, agent_id):
        """Deletes a provisioning agent by id.

        Args:
            agent_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(app='provisioning', endpoint='/v{}/dpmAgent/{}'.format(self.api_version, agent_id))
        return Command(self, response)

    def return_all_legacy_deployments(
        self, organization, offset, len, order_by, order, dpm_agent_id, deployment_status, with_wrapper=False
    ):
        """Returns all provisioning agents.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            dpm_agent_id (:obj:`str`)
            deployment_status (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='provisioning', endpoint='/v{}/deployments'.format(self.api_version), params=params)
        return Command(self, response)

    def get_legacy_deployment(self, deployment_id):
        """Returns a deployment by id.

        Args:
            deployment_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='provisioning', endpoint='/v{}/deployment/{}'.format(self.api_version, deployment_id))
        return Command(self, response)

    def get_legacy_deployments_by_status(
        self, organization, offset, len, order_by, order, deployment_status, with_wrapper=False
    ):
        """Returns all legacy deployments, filtered by status.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            deployment_status (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/deployments/byStatus'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_legacy_deployment_status(self, organization, offset, len, with_wrapper=False):
        """Returns all legacy deployment statuses.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/deployments/status'.format(self.api_version), params=params
        )
        return Command(self, response)

    def create_legacy_deployment(self, body):
        """Create a new deployment for the given Deployment model.

        Args:
            body (:obj:`dict`): JSON representation of deployment object.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='provisioning', data=body, endpoint='/v{}/deployments'.format(self.api_version))
        return Command(self, response)

    def update_legacy_deployment(self, deployment_id, body):
        """Update a deployment for the given Deployment model.

        Args:
            deployment_id (:obj:`str`): Deployment ID.
            body (:obj:`dict`): Deployment object json.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', data=body, endpoint='/v{}/deployment/{}'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def scale_legacy_deployment(self, deployment_id, num_instances):
        """Scale up/down active deployment.

        Args:
            deployment_id (:obj:`str`): Deployment ID.
            num_instances (:obj:`int`): Number of sdc instances.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/deployment/{}/scale'.format(self.api_version, deployment_id),
            params=params,
        )
        return Command(self, response)

    def wait_for_legacy_deployment_statuses(self, deployment_id, statuses, timeout_sec=300):
        """Wait for deployment status.

        Args:
            deployment_id (:obj:`str`)
            statuses (:obj:`list`): List of Deployment statuses.
            timeout_sec (:obj:`int`, optional): Timeout for wait, in seconds. Default: ``300``.
        """

        def condition(deployment_id):
            status_json = self.get_legacy_deployment(deployment_id).response.json()
            current_status = status_json['currentDeploymentStatus']['status']
            logger.debug('Status of deployment (id: %s) is %s ...', deployment_id, current_status)
            if current_status == 'INACTIVE_ERROR':
                raise LegacyDeploymentInactiveError('Deployment status changed to INACTIVE_ERROR')
            return current_status in statuses

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for status.'.format(timeout))

        def success(time):
            logger.debug('Deployment reached desired status after %s s.', time)

        logger.debug('Deployment %s waiting for status %s ...', deployment_id, statuses)
        wait_for_condition(
            condition=condition,
            condition_kwargs={'deployment_id': deployment_id},
            timeout=timeout_sec,
            failure=failure,
            success=success,
        )

    def start_legacy_deployment(self, deployment_id, dpm_agent_id):
        """Starts a deployment.

        Args:
            deployment_id (:obj:`str`)
            dpm_agent_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/deployment/{}/start'.format(self.api_version, deployment_id),
            params=params,
        )
        return DeploymentStartStopCommand(self, response)

    def stop_legacy_deployment(self, deployment_id):
        """Starts a deployment.

        Args:
            deployment_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/deployment/{}/stop'.format(self.api_version, deployment_id)
        )
        return DeploymentStartStopCommand(self, response)

    def legacy_deployments_acknowledge_errors(self, body):
        """Acknowledge deployment errors.

        Args:
            body (:obj:`list`): Deployment IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', data=body, endpoint='/v{}/deployments/acknowledgeErrors'.format(self.api_version)
        )
        return Command(self, response)

    def delete_legacy_deployment(self, deployment_id):
        """Delete a deployment for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='provisioning', endpoint='/v{}/deployment/{}'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def delete_legacy_deployments(self, body):
        """Delete all deployments for the given deployment IDs.

        Args:
            body (:obj:`list`): Deployment IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', data=body, endpoint='/v{}/deployments/deleteDeployments'.format(self.api_version)
        )
        return Command(self, response)

    def return_all_topologies(self, organization, offset, len, order_by, order, with_wrapper=False, filter_text=None):
        """Returns all jobs.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            with_wrapper (:obj:`bool`, optional): Default: ``False``
            filter_text (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='topology', endpoint='/v{}/topologies'.format(self.api_version), params=params)
        return Command(self, response)

    def get_topology_for_commit_id(self, commit_id, organization=None, validate=None):
        """Get topology for given commit ID.

        Args:
            commit_id (:obj:`str`)
            organization (:obj:`str`)
            validate (:obj:`bool`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'commit_id'))
        response = self._get(
            app='topology', endpoint='/v{}/topology/{}'.format(self.api_version, commit_id), params=params
        )
        return Command(self, response)

    def get_topology_commits(self, topology_id, organization, offset=0, len=-1, order='ASC', with_wrapper=False):
        """Get all topology commits for given topology ID.

        Args:
            topology_id (:obj:`str`)
            organization (:obj:`str`)
            offset (:obj:`int`, optional): Default: ``0``
            len (:obj:`int`, optional): Default: ``-1``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'topology_id'))
        response = self._get(
            app='topology', endpoint='v{}/topology/{}/log'.format(self.api_version, topology_id), params=params
        )
        return Command(self, response)

    def create_topology(self, topology_json):
        """Create new topology.

        Args:
           topology_json (:obj:`str`): Topology in JSON format. Complies to Swagger TopologyJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='topology', endpoint='/v{}/topologies'.format(self.api_version), data=topology_json)
        return Command(self, response)

    def create_topology_draft(self, commit_id):
        """Create a new draft for an existing Topology

        Args:
            commit_id (:obj:`str`): Commit ID for the topology you wish to create a draft. This should usually be the
            latest commit ID.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology', endpoint='/v{}/topology/{}/createDraft'.format(self.api_version, commit_id)
        )
        return Command(self, response)

    def update_topology(self, commit_id, topology_json):
        """Update topology.

        Args:
            commit_id (:obj:`str`)
            topology_json (:obj:`str`): Topology in JSON format. Complies to Swagger TopologyJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology', endpoint='/v{}/topology/{}'.format(self.api_version, commit_id), data=topology_json
        )
        return Command(self, response)

    def validate_topology(self, commit_id):
        """Validate an existing topology.

        Args:
            commit_id (:obj:`str`): The commit ID for the topology to be validated.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='topology', endpoint='/v{}/topology/{}/validate'.format(self.api_version, commit_id))
        return Command(self, response)

    def import_topologies(
        self,
        topologies_file,
        force_import=False,
        update_num_instances=False,
        update_runtime_parameters=False,
        update_labels=False,
        update_migrate_offsets=False,
    ):
        """Import topologies from compressed archive.

        Args:
            topologies_file (:obj:`file`): file containing the topologies.
            force_import (:obj:`boolean`, optional): Default: ``False``.
            update_num_instances (:obj:`boolean`, optional): Default: ``False``.
            update_runtime_parameters (:obj:`boolean`, optional): Default: ``False``.
            update_labels (:obj:`boolean`, optional): Default: ``False``.
            update_migrate_offsets (:obj:`boolean`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'topologies_file'))
        response = self._post(
            app='topology',
            endpoint='/v{}/topologies/importTopologies'.format(self.api_version),
            files={'file': topologies_file},
            params=params,
            headers={'content-type': None},
        )
        return Command(self, response)

    def export_topologies(self, body=None):
        """Export topologies.

        Args:
            body (:obj:`list`): A list of :obj:`str` commit ids.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology', endpoint='/v{}/topologies/exportTopologies'.format(self.api_version), data=body
        )
        return Command(self, response)

    def delete_topologies(self, topologies_json):
        """Delete topologies for all given topology IDs.

        Args:
            topologies_json (:obj:`str`): Topologies in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology', endpoint='/v{}/topologies/deleteTopologies'.format(self.api_version), data=topologies_json
        )
        return Command(self, response)

    def delete_topology_versions(self, commits_json):
        """Delete topologies commit for all given topology commit IDs.

        Args:
            commits_json (:obj:`str`): Topology commit IDs in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology',
            endpoint='/v{}/topologies/deleteTopologyVersions'.format(self.api_version),
            data=commits_json,
        )
        return Command(self, response)

    def publish_topology(self, commit_id, commit_message):
        """Publish topology.

        Args:
            commit_id (:obj:`str`)
            commit_message (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='topology',
            endpoint='/v{}/topology/{}/publish'.format(self.api_version, commit_id),
            params={'commitMessage': commit_message},
        )
        return Command(self, response)

    def return_all_report_definitions(self, organization, offset, len, order_by, order, filter_text):
        """Returns all jobs.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            filter_text (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='reporting', endpoint='/v{}/reports'.format(self.api_version), params=params)
        return Command(self, response)

    def return_all_reports_from_definition(self, report_definition_id, offset, len):
        """Return all Reports generated using given Report Definition Id.

        Args:
            report_definition_id (:obj:`str`): Report Definition Id.
            offset (:obj:`int`): Offset for the results returned.
            len (:obj:`int`): Total number of results returned.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', report_definition_id))
        response = self._get(
            app='reporting',
            endpoint='/v{}/report/{}/reports'.format(self.api_version, report_definition_id),
            params=params,
        )
        return Command(self, response)

    def get_report_for_given_report_id(self, report_definition_id, report_id):
        """Get report for given Report Id and Report Definition Id.

        Args:
            report_definition_id (:obj:`str`): Report Definition Id.
            report_id (:obj:`str`): Report Id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='reporting', endpoint='/v{}/report/{}/{}'.format(self.api_version, report_definition_id, report_id)
        )
        return Command(self, response)

    def create_new_report_definition(self, body):
        """Create a new Report Definition.

        Args:
            body (:obj:`dict`): Report Definition in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='reporting', endpoint='/v{}/reports'.format(self.api_version), data=body)
        return Command(self, response)

    def update_report_definition(self, report_definition_id, body):
        """Update an existing Report Definition.

        Args:
            body (:obj:`dict`): Report Definition in JSON format.
            report_definition_id (:obj:`str`): Report Definition Id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='reporting', endpoint='/v{}/report/{}'.format(self.api_version, report_definition_id), data=body
        )
        return Command(self, response)

    def delete_report_definition(self, report_definition_id):
        """Delete an existing Report Definition.

        Args:
            report_definition_id (:obj:`str`): Report Definition id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='reporting', endpoint='/v{}/report/{}'.format(self.api_version, report_definition_id)
        )
        return Command(self, response)

    def generate_report_for_report_definition(self, report_definition_id, trigger_time):
        """Generate Report for given Report Definition.

        Args:
            report_definition_id (:obj:`str`): Report Definition id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'report_definition_id'))
        response = self._post(
            app='reporting',
            endpoint='/v{}/report/{}/generateReport'.format(self.api_version, report_definition_id),
            params=params,
        )
        return Command(self, response)

    def download_report(self, report_definition_id, report_id, report_format):
        """Download Report in a report format for given report definition and report id.

        Args:
            report_definition_id (:obj:`str`): Report Definition id.
            report_id (:obj:`str`): Report id.
            report_format (:obj:`str`): Report Format ('PDF')

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'report_definition_id', 'report_id'))
        response = self._get(
            app='reporting',
            endpoint='/v{}/report/{}/{}/download'.format(self.api_version, report_definition_id, report_id),
            params=params,
        )
        return Command(self, response)

    def get_report_definition_acl(self, report_definition_id):
        """Get Report Definition ACL.

        Args:
            report_definition_id (:obj:`str`): Report Definition id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='reporting', endpoint='/v{}/report/{}/acl'.format(self.api_version, report_definition_id)
        )
        return Command(self, response)

    def set_report_definition_acl(self, report_definition_id, report_definition_acl_json):
        """Update Report Definition ACL.

        Args:
            report_definition_id (:obj:`str`): Report Definition id.
            report_definition_acl_json (:obj:`str`): Report Definition ACL in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='reporting',
            endpoint='/v{}/report/{}/acl'.format(self.api_version, report_definition_id),
            data=report_definition_acl_json,
        )
        return Command(self, response)

    def update_report_definition_permissions(self, data, report_definition_id, subject_id):
        """Update the Report Definition permissions.

        Args:
            data (:obj:`dict`): JSON representation of permission attributes to update.
            report_definition_id (:obj:`str`): Report Definition id.
            subject_id (:obj:`str`): Id of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='reporting',
            endpoint='/v{}/report/{}/permissions/{}'.format(self.api_version, report_definition_id, subject_id),
            data=data,
        )
        return Command(self, response)

    def get_metering_daily_report(
        self, start, end, search=None, zone=None, allow_incomplete_days=True, report_type=None
    ):
        """Get the daily metering report.

        Args:
            start (:obj:`long`)
            end (:obj:`long`)
            search (:obj:`str`, optional): Default: ``None``.
            zone (:obj:`str`, optional): Default: ``None``.
            allow_incomplete_days (:obj:`bool`, optional): Default: ``True``.
            report_type (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='metering', endpoint='v{}/reports/daily'.format(self.metering_api_version), params=params
        )
        return Command(self, response)

    def get_metering_daily_report_by_content_type(
        self, start, end, allow_incomplete_days=True, content_type="text/csv", report_type=None, search=None, zone=None
    ):
        """Get the daily metering report.

        Args:
            start (:obj:`long`)
            end (:obj:`long`)
            allow_incomplete_days (:obj:`bool`, optional): Default: ``True``.
            content_type (:py:obj:`str`, optional): Format of the returned data. Default: ``"text/csv"``.
            report_type (:obj:`str`, optional): Default: ``None``.
            search (:obj:`str`, optional): Default: ``None``.
            zone (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        content_type = MeteringDailyReportContentTypes(content_type)

        params = get_params(
            parameters=locals(),
            exclusions=(
                'self',
                'content_type',
            ),
        )
        additional_headers = {'Content-type': content_type.value}
        response = self._get(
            app='metering',
            endpoint='v4/reports/daily',
            params=params,
            headers=additional_headers,
        )
        return Command(self, response)

    def get_metering_report_for_job(self, job_id, start, end, zone=None, allow_incomplete_days=True, report_type=None):
        """Get the metering report for a job.

        Args:
            job_id (:obj:`str`)
            start (:obj:`long`)
            end (:obj:`long`)
            zone (:obj:`str`, optional): Default: ``None``.
            allow_incomplete_days (:obj:`bool`, optional): Default: ``True``.
            report_type (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='metering', endpoint='v{}/reports/job/{}'.format(self.metering_api_version, job_id), params=params
        )
        return Command(self, response)

    def get_metering_event(self, order_by=None, order=None, page=None, size=None, search=None, with_wrapper=False):
        """Get raw metering data from the metering app.

        Args:
            order_by (:obj:`str`, optional): Default: ``None``.
            order (:obj:`str`, optional): Default: ``None``.
            page (:obj:`int`, optional): Default: ``None``.
            size (:obj:`int`, optional): Default: ``None``.
            search (:obj:`str`, optional): Default: ``None``.
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='metering', endpoint='v{}/event'.format(self.metering_api_version), params=params)
        return Command(self, response)

    def get_metering_record_count_events(
        self, order_by=None, order=None, page=None, size=None, search=None, with_wrapper=False
    ):
        """Get raw metering data from the record count metering app.

        Args:
            order_by (:obj:`str`, optional): Default: ``None``.
            order (:obj:`str`, optional): Default: ``None``.
            page (:obj:`int`, optional): Default: ``None``.
            size (:obj:`int`, optional): Default: ``None``.
            search (:obj:`str`, optional): Default: ``None``.
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.aster_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='metering', endpoint='v{}/record-count/event'.format(self.metering_api_version), params=params
        )
        return Command(self, response)

    def return_all_pipeline_templates(
        self,
        pipeline_label_id,
        offset,
        len,
        order_by,
        order,
        system,
        filter_text,
        execution_modes,
        start_time=-1,
        end_time=-1,
        user_ids=None,
    ):
        """Returns all pipeline templates.

        Args:
            pipeline_label_id (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            system (:obj:`str`)
            filter_text (:obj:`str`)
            execution_modes (:obj:`str`)
            start_time (:obj:`int`, optional): Default: ``-1``
            end_time (:obj:`int`, optional): Default: ``-1``
            user_ids (:obj:`list`, optional): List of strings. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='v{}/pipelines/templates'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_pipelines_using_fragment(self, fragment_commit_id, offset, len, order_by, order):
        """Get Latest Committed Pipelines using given fragment Commit ID.

        Args:
            fragment_commit_id (:obj:`str`): Pipeline Commit Id of fragment.
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self', 'fragment_commit_id'))
        response = self._get(
            app='pipelinestore',
            endpoint='/v{}/pipelineCommit/{}/pipelinesUsingFragment'.format(self.api_version, fragment_commit_id),
            params=params,
        )
        return Command(self, response)

    def update_pipelines_with_fragment_commit_version(self, body, from_fragment_commit_id, to_fragment_commit_id):
        """Update pipelines with latest pipeline fragment commit version.

        Args:
            body (:obj:`list`): List of pipeline commit IDs.
            from_fragment_commit_id (:obj:`str`): commit ID of fragment from which the pipeline needs to be updated.
            to_fragment_commit_id (obj: `str`): commit ID of fragment to which the pipeline needs to be updated.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipelines/updateFragmentVersion/{}/{}'.format(
                self.api_version, from_fragment_commit_id, to_fragment_commit_id
            ),
            data=body,
        )
        return Command(self, response)

    def set_labels_to_pipelines(self, labels, pipeline_commit_ids):
        """Add labels to given pipelines.

        Args:
            labels (:obj:`list`): List of labels
            pipeline_commit_ids (:obj:`list`): List of pipeline commit IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._post(
            app='pipelinestore', endpoint='/v{}/pipelines/setLabelsToPipelines'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_all_user_roles(self):
        response = self._get(app='security', endpoint='/v{}/roles'.format(self.api_version))
        return response.json()

    def get_server_info(self):
        """Get the Control Hub server info.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app=None, endpoint='/v{}/server/info'.format(self.api_version), rest='rest')
        return Command(self, response)

    def update_job_permissions(self, data, job_id, subject_id):
        """Update the job permissions.

        Args:
            data (:obj:`dict`): JSON representation of permission attributes to update.
            job_id (:obj:`str`): Id of the job.
            subject_id (:obj:`str`): Id of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/job/{}/permissions/{}'.format(self.api_version, job_id, subject_id),
            data=data,
        )
        return Command(self, response)

    def update_pipeline_permissions(self, data, pipeline_id, subject_id):
        """Update the pipeline permissions.

        Args:
            data (:obj:`dict`): JSON representation of permission attributes to update.
            pipeline_id (:obj:`str`): Id of the pipeline.
            subject_id (:obj:`str`): Id of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='pipelinestore',
            endpoint='/v{}/pipeline/{}/permissions/{}'.format(self.api_version, pipeline_id, subject_id),
            data=data,
        )
        return Command(self, response)

    def update_sdc_permissions(self, data, sdc_id, subject_id):
        """Update the DataCollector permissions.

        Args:
            data (:obj:`dict`): JSON representation of permission attributes to update.
            sdc_id (:obj:`str`): Id of the DataCollector.
            subject_id (:obj:`str`): Id of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner',
            endpoint='/v{}/sdc/{}/permissions/{}'.format(self.api_version, sdc_id, subject_id),
            data=data,
        )
        return Command(self, response)

    def get_engine_acl(self, engine_id):
        """Get Engine ACL.

        Args:
            engine_id (:obj:`str`): Id of the engine.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/sdc/{}/acl'.format(self.api_version, engine_id))
        return Command(self, response)

    def set_engine_acl(self, engine_id, engine_acl_json):
        """Set Engine ACL.

        Args:
            engine_id (:obj:`str`): Id of the engine.
            engine_acl_json (:obj:`dict`): Python Object representation of ACL JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/sdc/{}/acl'.format(self.api_version, engine_id), data=engine_acl_json
        )
        return Command(self, response)

    def get_connection_acl(self, connection_id):
        """Get Connection ACL.

        Args:
            connection_id (:obj:`str`): ID of the Connection.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='connection', endpoint='/v{}/connection/{}/acl'.format(self.api_version, connection_id)
        )
        return Command(self, response)

    def update_connection_acl(self, connection_id, body):
        """Set Connection ACL.

        Args:
            connection_id (:obj:`str`): ID of the Connection.
            body (:obj:`dict`): Python Object representation of ACL JSON.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='connection', endpoint='/v{}/connection/{}/acl'.format(self.api_version, connection_id), data=body
        )
        return Command(self, response)

    def update_connection_permissions(self, body, connection_id, subject_id):
        """Update the connection permissions.

        Args:
            body (:obj:`dict`): JSON representation of permission attributes to update.
            connection_id (:obj:`str`): ID of the connection.
            subject_id (:obj:`str`): ID of the subject.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='connection',
            endpoint='/v{}/connection/{}/permissions/{}'.format(self.api_version, connection_id, subject_id),
            data=body,
        )
        return Command(self, response)

    def get_job_selection_types(self, api_version):
        """Fetches available job selection type in Scheduler.

        Args:
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        pageId = 'SchedulerJobTypeSelectorPage'
        response = self._get(
            app='scheduler', endpoint='/v{}/jobs/o:jobTypeSelector/pageId={}'.format(api_version, pageId)
        )
        return Command(self, response)

    def trigger_selection_info(self, data, api_version):
        """Triggers selection info for a given job type.

        Args:
            data (:obj:`dict`): Python Object representation for RestRequestRSchedulerTypeJobSelector.
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        pageId = 'SchedulerJobCreatePage'
        response = self._post(
            app='scheduler', endpoint='/v{}/jobs/o:new/pageId={}'.format(api_version, pageId), data=data
        )
        return Command(self, response)

    def get_scheduled_tasks(self, order_by, offset, len, api_version, filter_by=None):
        """List the scheduled tasks.

        Args:
            order_by (:obj:`str`): Order results by this field.
            offset (:obj:`int`): Offset for the results returned.
            len (:obj:`int`): Total number of results returned.
            api_version (:obj:`int`): Control Hub API Version to use.
            filter_by (:obj:`str`): To filter by.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'api_version', 'filter_by'))
        pageId = 'SchedulerJobListPage'

        url = '/v{}/jobs/pageId={}'.format(api_version, pageId)
        if filter_by:
            url += '?filterBy:name={}'.format(filter_by)

        response = self._get(app='scheduler', endpoint=url, params=params)
        return Command(self, response)

    def get_scheduled_task(self, id, run_info, audit_info, api_version):
        """Fetch the scheduled task for a given job.

        Args:
            id (:obj:`str`): Task id.
            run_info (:obj:`boolean`): Param to specify if run info is needed.
            audit_info (:obj:`boolean`): Param to specify if audit info is needed.
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'id', 'api_version'))
        pageId = 'SchedulerJobManagePage'
        response = self._get(
            app='scheduler', endpoint='/v{}/jobs/{}/pageId={}'.format(api_version, id, pageId), params=params
        )
        return Command(self, response)

    def create_scheduled_task(self, data, api_version):
        """Creates a new Scheduled Task.

        Args:
            data (:obj:`dict`): Python Object representation for RestRequestRSchedulerJob.
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        pageId = 'SchedulerJobManagePage'
        response = self._put(app='scheduler', endpoint='/v{}/jobs/pageId={}'.format(api_version, pageId), data=data)
        return Command(self, response)

    def update_scheduled_task(self, data, id, api_version):
        """Updates an existing Scheduled Task.

        Args:
            data (:obj:`dict`): Python Object representation of a Scheduled Task.
            id (:obj:`str`): ID of the Scheduled Task.
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        page_id = 'SchedulerJobManagePage'
        response = self._post(
            app='scheduler', endpoint='/v{}/jobs/{}/pageId={}'.format(api_version, id, page_id), data=data
        )
        return Command(self, response)

    def perform_bulk_action_on_scheduled_tasks(self, task_ids, action, api_version):
        """Performs a given action on all the given scheduled tasks.

        Args:
            task_ids (:obj:`list` of :obj:`str`): IDs of the scheduled task.
            action (:obj:`str`): Action to be performed on task (['PAUSE', 'RESUME', 'KILL', 'DELETE']).
            api_version (:obj:`int`): Control Hub API Version to use.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        # get_params uses the same name as the variable, we want to send `id` as a parameter key not task_ids
        params = get_params(parameters=locals(), exclusions=('self', 'task_ids', 'api_version'))
        params['id'] = task_ids
        pageId = 'SchedulerJobListPage'
        response = self._post(
            app='scheduler', endpoint='/v{}/jobs/o:action/pageId={}'.format(api_version, pageId), params=params
        )
        return Command(self, response)

    def get_all_event_subscriptions(self, organization, offset, len, order_by, order, with_wrapper=False):
        """Get all event subscriptions.

        Args:
            organization (:obj:`str`): Id of the organization.
            offset (:obj:`int`): Offset for the results returned.
            len (:obj:`int`): Total number of results returned.
            order_by (:obj:`str`): Order results by this field.
            order (:obj:`str`): One of {``'ASC'``, ``'DESC'``}.
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='notification', endpoint='/v{}/eventsub'.format(self.api_version), params=params)
        return Command(self, response)

    def create_event_subscription(self, body):
        """Create a new event subscription.

        Args:
            body (:obj:`dict`): Subscription object that complies to Swagger EventSubscriptionJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(
            app='notification', endpoint='/v{}/eventsub/createEventSub'.format(self.api_version), data=body
        )
        return Command(self, response)

    def update_event_subscription(self, body):
        """Update an existing event subscription.

        Args:
            body (:obj:`dict`): Subscription object that complies to Swagger EventSubscriptionJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification', endpoint='/v{}/eventsub/updateEventSub'.format(self.api_version), data=body
        )
        return Command(self, response)

    def delete_event_subscription(self, subscription_id):
        """Delete an existing event subscription.

        Args:
            subscription_id (:obj:`str`): Id of the Subscription.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification', endpoint='/v{}/eventsub/deleteEventSub'.format(self.api_version), data=subscription_id
        )
        return Command(self, response)

    def event_subscription_acknowledge_error(self, subscription_id):
        """Acknowledge an error on given Event Subscription.

        Args:
            subscription_id (:obj:`str`): Id of the Subscription.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification', endpoint='/v{}/eventsub/ackEventSubError'.format(self.api_version), data=subscription_id
        )
        return Command(self, response)

    def get_all_subscription_audits(
        self, offset=None, len_=None, order_by='CREATED_TIME', order='ASC', with_wrapper=False
    ):
        """Get all external action audits.

        Args:
            offset (:obj:`str`, optional): Default: ``None``
            len_ (:obj:`str`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'CREATED_TIME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        if 'len_' in params:
            params['len'] = params.pop('len_')
        endpoint = '/v{}/externalActions/audits'.format(self.api_version)
        response = self._get(app='notification', endpoint=endpoint, params=params)
        return Command(self, response)

    def is_ldap_enabled(self):
        """Check if ldap is enabled.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='security', endpoint='/v{}/ldap'.format(self.api_version))
        return Command(self, response)

    def get_all_executor_stats(
        self, label=None, offset=None, len=None, order_by='LAST_REPORTED_TIME', order='ASC', executor_type='COLLECTOR'
    ):
        """Returns executor uptime, Memory/CPU usage by executor at JVM level.

        Args:
            label (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (obj:`int`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``LAST_REPORTED_TIME``.
            order (:obj:`str`, optional): Default: ``ASC``.
            executor_type (:obj:`str`, optional): Default: ``COLLECTOR``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/metrics/executors'.format(self.api_version), params=params)
        return Command(self, response)

    def get_job_metrics(self, job_id, run_count=None, sdc_id=None):
        """Get job metrics. If runCount is empty or 0, latest run metrics are returned. Otherwise, metrics for the given
        run count are returned.

        Args:
            job_id (:obj:`str`)
            run_count (:obj:`int`, optional): Default ``None``.
            sdc_id (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner', endpoint='/v{}/metrics/job/{}'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_tunneling_instance_id(self, engine_id):
        """Get tunneling instance ID related to an execution engine.

        Args:
            engine_id (:obj:`str`): ID of an execution engine.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        fetched_response = None

        def _fetch_tunneling_instance_id(api_client):
            try:
                url = '{}/tunneling/rest/connection/{}'.format(self.base_url, engine_id)
                response = self._get(absolute_endpoint=True, endpoint=url)
                if not response:
                    raise Exception(
                        'This Engine is not accessible. There is no active WebSocket session to the'
                        'Tunneling application from this engine. Trying again ...'
                    )
                tunneling_instance_id = response.json()['instanceId']
                logger.debug('Fetched tunneling_instance_id is %s', tunneling_instance_id)
                nonlocal fetched_response
                fetched_response = response
                return response
            except requests.exceptions.HTTPError as http_error:
                logger.debug('Call to fetch tunneling instance ID endpoint failed: %s. Trying again ...', http_error)
            except KeyError:
                logger.debug('Invalid tunneling instance ID received. Trying again ...')
            except Exception as ex:
                logger.debug(ex)

        wait_for_condition(_fetch_tunneling_instance_id, [self], timeout=300)
        return Command(self, fetched_response)

    def get_tunneling_pipelines_definitions(self, engine_id, tunneling_instance_id):
        """Get engine's pipeline definitions for a given tunnel.

        Args:
            engine_id (:obj:`str`): ID of an execution engine.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID of an engine.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        url = '{}/tunneling/rest/{}/rest/v{}/definitions'.format(self.base_url, engine_id, self.api_version)
        response = self._get(
            absolute_endpoint=True, endpoint=url, params={'TUNNELING_INSTANCE_ID': tunneling_instance_id}
        )
        return Command(self, response)

    def get_job_realtime_summary(self, engine_id, pipeline_id):
        """Get job realtime summary.

        Args:
            engine_id (:obj:`str`)
            pipeline_id (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'engine_id', 'pipeline_id'))

        tunneling_instance_id = self.get_tunneling_instance_id(engine_id).response.json()['instanceId']
        url_template = '{}/tunneling/rest/{}/rest/v{}/pipeline/{}/metrics'
        url = url_template.format(self.base_url, engine_id, self.api_version, pipeline_id)
        params.update({'onlyIfExists': True, 'TUNNELING_INSTANCE_ID': tunneling_instance_id})

        response = self._get(absolute_endpoint=True, endpoint=url, params=params)
        return Command(self, response)

    def get_job_latest_metrics(self, job_id, sdc_id=None):
        """Returns latest job metrics.

        Args:
            job_id (:obj:`str`)
            sdc_id (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/job/{}/latestMetrics'.format(self.api_version, job_id),
            params=params,
        )
        return Command(self, response)

    def get_job_count_by_status(self):
        """Get job status and job counts mapping.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='jobrunner', endpoint='/v{}/metrics/jobCountByStatus'.format(self.api_version))
        return Command(self, response)

    def get_job_record_count_for_all_runs(self, job_id, sdc_id=None, with_all_engines=False):
        """Get record counts of all runs of a job.

        Args:
            job_id (:obj:`str`)
            sdc_id (:obj:`str`, optional): Default: ``None``.
            with_all_engines (:obj:`str`, optional): Default: ``False``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/job/{}/recordCountsForAllRuns'.format(self.api_version, job_id),
            params=params,
        )
        return Command(self, response)

    def get_all_current_metrics_engines(self, job_id, sdc_id=None):
        """Get all current metrics engines for a job.

        Args:
            job_id (:obj:`str`)
            sdc_id (:obj:`str`, optional): Default: ``None``.
        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/job/{}/getAllMetricsEngines'.format(self.api_version, job_id),
            params=params,
        )
        return Command(self, response)

    def list_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner', endpoint='/v{}/metrics/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def list_pipelinestore_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/pipelines/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def list_provisioning_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/aws/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def list_jobrunner_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(app='jobrunner', endpoint='/v{}/csp/listAclAudits'.format(self.api_version), params=params)
        return Command(self, response)

    def list_topology_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='topology', endpoint='/v{}/topology/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def list_topologies_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='topology', endpoint='/v{}/topologies/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def list_connection_acl_audits(self, organization=None, offset=None, len=None, sort_field=None, sort_order=None):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            sort_field (:obj:`str`, optional): Default: ``None``.
            sort_order (:obj:`str`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='connection', endpoint='/v{}/connection/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_problematic_jobs(
        self,
        organization=None,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        removed=None,
        system=None,
        filter_text=None,
        job_status='INACTIVE',
        job_label=None,
        executor_type='COLLECTOR',
    ):
        """Get all jobs with red state.

        Args:
            organization (:obj:`str`, optional): Default: ``None``.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            order_by (:obj:`str`, optional): Default: ``'NAME'``.
            order (:obj:`str`, optional): Default: ``'ASC'``.
            removed (:obj:`boolean`, optional): Default: ``None``.
            system (:obj:`boolean`, optional): Default: ``None``.
            filter_text (:obj:`str`, optional): Default: ``None``.
            job_status (:obj:`str`, optional): Default: ``'INACTIVE'``.
            job_label (:obj:`str`, optional): Default: ``None``.
            executor_type (:obj:`str`, optional): Default: ``'COLLECTOR'``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='jobrunner', endpoint='/v{}/metrics/problematicJobs'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_executor_cpu_usage_time_series(
        self, executor_id, time_filter_condition='LAST_5M', limit=None, start_time=None, end_time=None
    ):
        """Returns CPU usage by executor at JVM level overtime.

        Args:
            executor_id (:obj:`str`)
            time_filter_condition (:obj:`str`, optional): Default: ``'LAST_5M'``.
            limit (:obj:`str`, optional): Default: ``None``.
            start_time (:obj:`int`, optional): Default: ``None``.
            end_time (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'executor_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/executor/{}/cpu'.format(self.api_version, executor_id),
            params=params,
        )
        return Command(self, response)

    def get_executor_memory_usage_time_series(
        self, executor_id, time_filter_condition='LAST_5M', limit=None, start_time=None, end_time=None
    ):
        """Returns memory usage by executor at JVM level overtime.

        Args:
            executor_id (:obj:`str`)
            time_filter_condition (:obj:`str`, optional): Default: ``'LAST_5M'``.
            limit (:obj:`str`, optional): Default: ``None``.
            start_time (:obj:`int`, optional): Default: ``None``.
            end_time (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'executor_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/executor/{}/memory'.format(self.api_version, executor_id),
            params=params,
        )
        return Command(self, response)

    def get_job_record_count_time_series(
        self, job_id, sdc_id=None, time_filter_condition='LAST_5M', limit=None, start_time=None, end_time=None
    ):
        """Returns input, output, and error record count for the job run overtime.

        Args:
            job_id (:obj:`str`)
            sdc_id (:obj:`str`, optional): Default: ``None``.
            ime_filter_condition (:obj:`str`, optional): Default: ``'LAST_5M'``.
            limit (:obj:`str`, optional): Default: ``None``.
            start_time (:obj:`int`, optional): Default: ``None``.
            end_time (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries', endpoint='/v{}/metrics/job/{}/recordCount'.format(self.api_version, job_id), params=params
        )
        return Command(self, response)

    def get_job_record_throughput_time_series(
        self, job_id, sdc_id=None, time_filter_condition='LAST_5M', limit=None, start_time=None, end_time=None
    ):
        """Returns input, output, and error record throughput for the job run overtime.

        Args:
            job_id (:obj:`str`)
            sdc_id (:obj:`str`, optional): Default: ``None``.
            ime_filter_condition (:obj:`str`, optional): Default: ``'LAST_5M'``.
            limit (:obj:`str`, optional): Default: ``None``.
            start_time (:obj:`int`, optional): Default: ``None``.
            end_time (:obj:`int`, optional): Default: ``None``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'job_id'))
        response = self._get(
            app='timeseries',
            endpoint='/v{}/metrics/job/{}/recordThroughput'.format(self.api_version, job_id),
            params=params,
        )
        return Command(self, response)

    def delete_job_latest_metrics(self, job_ids):
        """Delete all latest metrics of given jobIds

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='timeseries',
            endpoint='/v{}/metrics/purgeLatestMetricsOfDeletedJobs'.format(self.api_version),
            data=job_ids,
        )
        return Command(self, response)

    def get_pipelines_created_by_users_in_a_group(
        self,
        group,
        organization,
        offset,
        len,
        order_by,
        order,
        system,
        filter_text,
        only_published,
        execution_modes,
        start_time,
        end_time,
    ):
        """Returns all Pipelines created by users in a group between a start and end time.

        Args:
            group (:obj:`str`)
            organization (:obj:`str`)
            offset (:obj:`str`)
            len (:obj:`str`)
            order_by (:obj:`str`)
            order (:obj:`str`)
            system (:obj:`str`)
            filter_text (:obj:`str`)
            only_published (:obj:`bool`)
            execution_modes (:obj:`str`)
            start_time (:obj:`int`)
            end_time (:obj:`int`)
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='pipelinestore', endpoint='/v{}/metrics/pipelines'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_users_not_belonging_to_group(self, org_id, offset, len, sort_field, sort_order, group):
        """Get all users that don't belong to group specified.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            sort_field (:obj:`str`)
            sort_order (:obj:`str`)
            group (:obj:`str`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._get(
            app='security', endpoint='/v{}/metrics/{}/usersNotInGroup'.format(self.api_version, org_id), params=params
        )
        return Command(self, response)

    def get_logged_in_users(self, org_id, offset, len, sort_field, sort_order, group, start_time, end_time):
        """Get all users with login activity between start time and end time.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            sort_field (:obj:`str`)
            sort_order (:obj:`str`)
            group (:obj:`str`)
            start_time (:obj:`int`)
            end_time (:obj:`int`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._get(
            app='security', endpoint='/v{}/metrics/{}/loggedInUsers'.format(self.api_version, org_id), params=params
        )
        return Command(self, response)

    def get_user_with_no_login_activity(self, org_id, offset, len, sort_field, sort_order, group, start_time, end_time):
        """Get all users with no login activity between start time and end time.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            sort_field (:obj:`str`)
            sort_order (:obj:`str`)
            group (:obj:`str`)
            start_time (:obj:`int`)
            end_time (:obj:`int`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._get(
            app='security', endpoint='/v{}/metrics/{}/notLoggedInUsers'.format(self.api_version, org_id), params=params
        )
        return Command(self, response)

    def get_users_created_during_time_frame(
        self, org_id, group, offset, len, sort_field, sort_order, start_time, end_time
    ):
        """Get all users created between start time and end time.

        Args:
            org_id (:obj:`str`)
            group (:obj:`str`)
            offset (:obj:`int`)
            len (:obj:`int`)
            sort_field (:obj:`str`)
            sort_order (:obj:`str`)
            start_time (:obj:`int`)
            end_time (:obj:`int`)

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        response = self._get(
            app='security', endpoint='/v{}/metrics/{}/usersCreated'.format(self.api_version, org_id), params=params
        )
        return Command(self, response)

    def get_all_alerts(
        self,
        offset=None,
        len=None,
        order_by='TRIGGERED_ON',
        order='ASC',
        alert_status='ACTIVE',
        filter_text=None,
        with_wrapper=False,
    ):
        """Get all alerts.

        Args:
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'TRIGGERED_ON'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            alert_status (:obj:`str`, optional): Default: ``'ACTIVE'``
            filter_text (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/alerts'.format(self.api_version)
        response = self._get(app='notification', endpoint=endpoint, params=params)
        return Command(self, response)

    def acknowledge_alert(self, body):
        """Acknowledge an active Alert.

        Args:
            body (:obj:`list`): ID of an Active Alert in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='notification', endpoint='/v{}/alerts/ackAlerts'.format(self.api_version), data=body)
        return Command(self, response)

    def delete_alert(self, body):
        """Delete an acknowledged Alert.

        Args:
            body (:obj:`list`): ID of an Acknowledged Alert in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='notification', endpoint='/v{}/alerts/deleteAlerts'.format(self.api_version), data=body
        )
        return Command(self, response)

    def get_resource_alerts(
        self,
        resource_id,
        offset=None,
        len=None,
        order_by='TRIGGERED_ON',
        order='ASC',
        alert_status='ACTIVE',
        with_wrapper=False,
    ):
        """Get all alerts for a given Resource ID.

        Args:
            resource_id (:obj:`list`): ID of the Resource.
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'TRIGGERED_ON'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            alert_status (:obj:`str`, optional): Default: ``'ACTIVE'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'resource_id'))
        endpoint = '/v{}/alerts/resource/{}'.format(self.api_version, resource_id)
        response = self._get(app='notification', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_user_actions_for_user(
        self, user_id, org_id, offset=None, len=None, sort_field='TIME', sort_order=None, with_wrapper=False
    ):
        """Get user actions done for given user ID.

        Args:
            user_id (:obj:`str`)
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'TIME'``
            sort_order (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'user_id', 'org_id'))
        endpoint = '/v{}/organization/{}/user/{}/listActions'.format(self.api_version, org_id, user_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_user_actions_for_org(
        self, org_id, offset=None, len=None, sort_field='TIME', sort_order=None, with_wrapper=False
    ):
        """Get user actions done for given user ID.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'TIME'``
            sort_order (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/users/listActions'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_user_actions_requested_by_user(
        self, user_id, org_id, offset=None, len=None, sort_field='TIME', sort_order=None, with_wrapper=False
    ):
        """Get user actions requested by given user ID.

        Args:
            user_id (:obj:`str`)
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'TIME'``
            sort_order (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'user_id', 'org_id'))
        endpoint = '/v{}/organization/{}/user/{}/listActionsRequested'.format(self.api_version, org_id, user_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_login_audits_for_user(
        self, user_id, org_id, offset=None, len=None, sort_field=None, sort_order=None, with_wrapper=False
    ):
        """List audit logs for user logins for given User ID and Organization ID.

        Args:
            user_id (:obj:`str`)
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'None'``
            sort_order (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'user_id', 'org_id'))
        endpoint = '/v{}/organization/{}/user/{}/listLogins'.format(self.api_version, org_id, user_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_login_audits_for_org(
        self, org_id, offset=None, len=None, sort_field=None, sort_order=None, with_wrapper=False
    ):
        """List audit logs for all user logins in the organization for given Organization ID.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``None``
            sort_order (:obj:`str`, optional): Default: ``None``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/users/listLogins'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_active_user_sessions_for_org(
        self, org_id, offset=None, len=None, sort_field='EXPIRY_TIME', sort_order='DESC', with_wrapper=False
    ):
        """Get all active user sessions for given Organization ID.

        Args:
            org_id (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'EXPIRY_TIME'``
            sort_order (:obj:`str`, optional): Default: ``'DESC'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/sessions/{}/active'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_active_user_sessions_for_all_orgs(
        self, offset=None, len=None, sort_field='EXPIRY_TIME', sort_order='DESC', with_wrapper=False
    ):
        """Get all active user sessions for all organizations.

        Args:
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'EXPIRY_TIME'``
            sort_order (:obj:`str`, optional): Default: ``'DESC'``
            with_wrapper (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/sessions/active'.format(self.api_version)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def add_data_sla(self, sla_json):
        """Add Data SLA.

        Args:
            sla_json (:obj:`dict`)

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='sla', endpoint='/v{}/dataSlas'.format(self.api_version), data=sla_json)
        return Command(self, response)

    def get_data_sla(self, organization, topology_commit_id, offset=None, len=None, with_wrapper=False):
        """Get Data SLAs for given topology.

        Args:
            organization (:obj:`str`): Organization ID.
            topology_commit_id (:obj:`str`): Topology commit ID.
            offset (:obj:`int`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            with_wrapper (:obj:`bool`, optional): Default: ``False``.

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/dataSlas'.format(self.api_version)
        response = self._get(app='sla', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_environment(self, body, complete=False, process_if_enabled=False):
        """Create a new environment.

        Args:
           body (:obj:`str`): environment in JSON format. Complies to Swagger CreateCspEnvironmentJson definition.
           complete (:obj:`bool`, optional): Default: ``False``
           process_if_enabled (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._put(
            app='provisioning', endpoint='/v{}/csp/environments'.format(self.api_version), data=body, params=params
        )
        return Command(self, response)

    def delete_environment(self, environment_id):
        """Delete an existing environment.

        Args:
            environment_id (:obj:`str`): Id of the environment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='provisioning', endpoint='/v{}/csp/environment/{}'.format(self.api_version, environment_id)
        )
        return Command(self, response)

    def delete_environments(self, environment_ids):
        """Delete existing environments.

        Args:
            environment_ids (:obj:`list`): Environment IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/environments/deleteEnvironments'.format(self.api_version),
            data=environment_ids,
        )
        return Command(self, response)

    def update_environment(self, environment_id, body, complete='undefined', process_if_enabled='undefined'):
        """Update an existing environment.

        Args:
            environment_id (:obj:`str`): Id of the environment.
            body (:obj:`str`): environment in JSON format. Complies to Swagger CspEnvironmentJson definition.
            complete (:obj:`str`, optional): Default: ``undefined``
            process_if_enabled (:obj:`str`, optional): Default: ``undefined``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/environment/{}'.format(self.api_version, environment_id),
            data=body,
            params=params,
        )
        return Command(self, response)

    def get_api_user_credentials_for_org(self, org_id, user_id=None):
        """List API User Credentials for the organization.

        Args:
            org_id (:obj:`str`): Organization id.
            user_id (:obj:`str`): User id. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/api-user-credentials-for-org'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_api_user_credentials(self, org_id):
        """List API User Credentials for the current user.

        Args:
            org_id (:obj:`str`): Organization id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'org_id'))
        endpoint = '/v{}/organization/{}/api-user-credentials'.format(self.api_version, org_id)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def delete_api_user_credential(self, org_id, credential_id):
        """Delete an API User Credentials.

        Args:
            org_id (:obj:`str`): Organization id.
            credential_id (:obj:`str`): Credential id.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/api-user-credentials/{}'.format(self.api_version, org_id, credential_id)
        response = self._delete(app='security', endpoint=endpoint)
        return Command(self, response)

    def create_api_user_credential(self, org_id, api_user_credential_json):
        """Create an API User Credential.

        Args:
            org_id (:obj:`str`): Organization id.
            api_user_credential_json (:obj:`str`): Credential in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/api-user-credentials'.format(self.api_version, org_id)
        response = self._post(app='security', endpoint=endpoint, data=api_user_credential_json)
        return Command(self, response)

    def update_api_user_credential(self, org_id, credential_id, api_user_credential_json):
        """Update an API User Credential.

        Args:
            org_id (:obj:`str`): Organization id.
            credential_id (:obj:`str`): Credential id.
            api_user_credential_json (:obj:`str`): Credential in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/organization/{}/api-user-credentials/{}'.format(self.api_version, org_id, credential_id)
        response = self._post(app='security', endpoint=endpoint, data=api_user_credential_json)
        return Command(self, response)

    def get_environment(self, environment_id):
        """Get the environment for the given environment ID.

        Args:
            environment_id (:obj:`str`): environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/environment/{}'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_all_environments(
        self,
        organization,
        type=None,
        state_display_label=None,
        status=None,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        with_total_count=False,
        tag=None,
    ):
        """Get environments a user has access to.

        Args:
            org_id (:obj:`str`)
            type (:obj:`str`, optional): Default: ``None``
            state_display_labelf (:obj:`str`, optional): Default: ``None``
            status (:obj:`str`, optional): Default: ``'OK'``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'DESC'``
            with_total_count (:obj:`bool`, optional): Default: ``True``
            tag (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/environments'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_all_environment_tags(self, organization, parent_id=None, offset=None, len=None, order=None):
        """Get environment tags for a given organization.

        Args:
            organization (:obj:`str`)
            parent_id (:obj:`str`, optional): Default: ``None``
            offset (:obj:`int`, optional): Default: ``None``
            len (obj:`int`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/environments/tags'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_environment_acl(self, environment_id):
        """Get environment ACL.

        Args:
            environment_id (:obj:`str`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/environment/{}/acl'.format(self.api_version, environment_id)
        )
        return Command(self, response)

    def set_environment_acl(self, environment_id, environment_acl_json):
        """Update environment ACL.

        Args:
            environment_id (:obj:`str`).
            environment_acl_json (:obj:`str`): environment ACL in JSON format.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/environment/{}/acl'.format(self.api_version, environment_id),
            data=environment_acl_json,
        )
        return Command(self, response)

    def get_environment_permissions(self, deployment_id, subject_id):
        """Get permissions on a given deployment for a given subject.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            subject_id (:obj:`str`): Subject ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/environment/{}/permissions/{}'.format(self.api_version, deployment_id, subject_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def update_environment_permissions(self, body, deployment_id, subject_id):
        """Update permissions on a given deployment for a given subject.

        Args:
            body (:obj:`str`): deployment ACL in JSON format. Complies to Swagger CspEngineEventJson definition.
            deployment_id (:obj:`str`): Id of the deployment.
            subject_id (:obj:`str`): Subject ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/environment/{}/permissions/{}'.format(self.api_version, deployment_id, subject_id)
        response = self._post(app='provisioning', endpoint=endpoint, data=body)
        return Command(self, response)

    def get_aws_external_id(self, organization):
        """Get the external id to use for Cross Account Roles for the user's Org.

        Args:
            organization (:obj:`str`).

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/aws/externalId'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_azure_network_security_groups(self, environment_id, region):
        """Returns the available network security groups for the given environment and region

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/networkSecurityGroups/{}'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_subnets(self, environment_id, network_id):
        """Returns the available subnets for the given environment and network

        Args:
            environment_id (:obj:`str`): Environment id
            network_id (:obj:`str`): network id

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'environment_id'))
        endpoint = '/v{}/csp/azure/{}/subnets'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_azure_networks(self, environment_id, region):
        """Returns the available networks for the given environment

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/networks/{}'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_managed_entities(self, environment_id, region):
        """Returns the available managed identities for the given environment

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/identities/{}'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_vm_sizes(self, environment_id, region, zones=None):
        """Returns the available VM sizes for the given environment, Azure region

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): region
            zones (:obj:`list`, optional): List of zones. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'environment_id', 'region'))
        endpoint = '/v{}/csp/azure/{}/regions/{}/vmSizes'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_azure_resource_groups(self, environment_id, region):
        """Returns the available resource groups for the given environment and region

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/resourceGroups/{}'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_sshkeypairs(self, environment_id):
        """Returns the available Azure SSH key pairs for the given environment

        Args:
            environment_id (:obj:`str`): Environment id

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/sshkeypairs'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_regions(self):
        """Returns the available regions for Azure

        Args:
            environment_id (:obj:`str`): Environment id

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/regions'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_azure_zones(self, environment_id, region):
        """Returns the available zones for for the given environment, Azure region

        Args:
            environment_id (:obj:`str`): Environment id
            region (:obj:`str`): Region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/azure/{}/regions/{}/zones'.format(self.api_version, environment_id, region)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def activate_data_sla(self, sla_ids):
        """Activate SLAs.

        Args:
            sla_ids (:obj:`list`): List of string IDs of SLAs

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='sla', endpoint='/v{}/dataSlas/activateSlas'.format(self.api_version), data=sla_ids)
        return Command(self, response)

    def deactivate_data_sla(self, sla_ids):
        """Deactivate SLAs.

        Args:
            sla_ids (:obj:`list`): List of string IDs of SLAs

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='sla', endpoint='/v{}/dataSlas/deactivateSlas'.format(self.api_version), data=sla_ids)
        return Command(self, response)

    def delete_data_sla(self, sla_ids):
        """Delete SLAs.

        Args:
            sla_ids (:obj:`list`): List of string IDs of SLAs

        Returns:
          An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='sla', endpoint='/v{}/dataSlas/deleteSlas'.format(self.api_version), data=sla_ids)
        return Command(self, response)

    def get_component_version_range(self, id):
        """Get the min/max component versions that can work with Control Hub.

        Args:
            id (:obj:`str`): Type of component you wish to retrieve the version range for.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/componentVersionRange'.format(self.api_version)
        response = self._get(app='security', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_aws_environment_regions(self, environment_id):
        """Returns the available regions for the given Environment.

        Args:
            environment_id (:obj:`str`): environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_aws_environment_ec2_instance_types(self, environment_id, region_id):
        """Returns the available EC2 instance types for the given Environment and AWS Region.

        Args:
            environment_id (:obj:`str`): environment ID
            region_id (:obj:`str`): Region ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions/{}/ec2/instancetypes'.format(self.api_version, environment_id, region_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_aws_environment_ec2_ssh_key_pairs(self, environment_id, region_id):
        """Returns the available EC2 SSH Key Pairs for the given Environment and AWS Region.

        Args:
            environment_id (:obj:`str`): environment ID
            region_id (:obj:`str`): Region ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions/{}/ec2/sshkeypairs'.format(self.api_version, environment_id, region_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_aws_environment_vpcs(self, environment_id, region_id):
        """Returns the available VPCs for the given Environment and AWS Region.

        Args:
            environment_id (:obj:`str`): environment ID
            region_id (:obj:`str`): Region ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions/{}/vpcs'.format(self.api_version, environment_id, region_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_aws_environment_security_groups(self, environment_id, region_id, vpc_id):
        """Returns the available Security Groups for the given Environment, AWS Region, and VPC.

        Args:
            environment_id (:obj:`str`): environment ID
            region_id (:obj:`str`): Region ID
            vpc_id (:obj:`str`): VPC ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions/{}/vpcs/{}/securitygroups'.format(
            self.api_version, environment_id, region_id, vpc_id
        )
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_aws_environment_subnets(self, environment_id, region_id, vpc_id):
        """Returns the available Subnets for the given Environment, AWS Region, and VPC.

        Args:
            environment_id (:obj:`str`): environment ID
            region_id (:obj:`str`): Region ID
            vpc_id (:obj:`str`): VPC ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/aws/{}/regions/{}/vpcs/{}/subnets'.format(
            self.api_version, environment_id, region_id, vpc_id
        )
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_projects(self, environment_id):
        """Returns the available projects for the given Environment.

        Args:
            environment_id (:obj:`str`): environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_networks(self, environment_id, project_id):
        """Returns the available Networks for the given Environment and GCP Project.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/networks'.format(self.api_version, environment_id, project_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_regions(self, environment_id, project_id):
        """Returns the available regions for the given Environment and GCP Project.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/regions'.format(self.api_version, environment_id, project_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_subnetworks(self, environment_id, project_id, network_id, region_id):
        """Returns the available subnetworks for the given Environment and GCP Project, network and region.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID
            network_id (:obj:`str`): network ID
            region_id (:obj:`str`): region ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/network/{}/region/{}/subnetworks'.format(
            self.api_version, environment_id, project_id, network_id, region_id
        )
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_service_accounts(self, environment_id, project_id):
        """Returns the available service accounts for the given Environment and GCP Project.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/serviceAccounts'.format(self.api_version, environment_id, project_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_zones(self, environment_id, project_id, region_id):
        """Returns the available zones for the given environment and GCP project and GCP region.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID
            region (:obj:`str`): region

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/zones/{}'.format(
            self.api_version, environment_id, project_id, region_id
        )
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_gcp_environment_machine_types(self, environment_id, project_id, zone_id):
        """Returns the available machine types for the given Environment and GCP Project and GCP Zone.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID
            zone_id (:obj:`str`): project ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/gcp/{}/projects/{}/zones/{}/machineTypes'.format(
            self.api_version, environment_id, project_id, zone_id
        )
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_machine_types_zones(self, environment_id, project_id, zones):
        """Returns the available machine types for the given Environment and GCP Project.

        Args:
            environment_id (:obj:`str`): environment ID
            project_id (:obj:`str`): project ID
            zones (:obj:`list`): List of zones

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'environment_id', 'project_id'))
        endpoint = '/v{}/csp/gcp/{}/projects/{}/zones/machineTypes'.format(self.api_version, environment_id, project_id)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_gcp_external_id(self, organization):
        """Get the external id to use for Service Accounts for the user's Org.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))

        endpoint = '/v{}/csp/gcp/externalId'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_kubernetes_agent_versions(
        self, releases_only=None, disabled_filter='ONLY_ALLOWED', offset=None, len=None, with_total_count=None
    ):
        """Returns all Kubernetes Agent Versions.

        Args:
            releases_only (:obj:`bool`, optional): Default: ``None``
            disabled_filter (:obj:`str`, optional): Default: ``'ONLY_ALLOWED'``
            offset (:obj:`int`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            with_total_count (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/kubernetes/agentVersions'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_kubernetes_apply_agent_yaml_command(self, environment_id):
        """Gets the command to apply the Kubernetes Agent YAML.

        Args:
            environment_id (:obj:`str`): Environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`. Response content-type is text/plain.
        """
        endpoint = '/v{}/csp/kubernetes/{}/applyAgentYamlCommand'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_kubernetes_delete_agent_yaml_command(self, environment_id):
        """Gets the command to delete the Kubernetes Agent YAML.

        Args:
            environment_id (:obj:`str`): Environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`. Response content-type is text/plain.
        """
        endpoint = '/v{}/csp/kubernetes/{}/deleteAgentYamlCommand'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_kubernetes_environment_agent_yaml(self, environment_id):
        """Gets the YAML for the calling the Kubernetes Agent.

        Args:
            environment_id (:obj:`str`): Environment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`. Response content-type is application/json.
        """
        endpoint = '/v{}/csp/kubernetes/{}/agentYaml'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def validate_and_sync_kubernetes_deployment_yaml(self, body):
        """Validate and Sync the YAML and fields in a Kubernetes Deployment (for use with Advanced Mode).
         Note that this does NOT save changes to the deployment.

        Args:
            body (:obj:`str`): deployment in JSON format. Complies to Swagger KubernetesCspDeploymentJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/kubernetes/validateAndSyncDeploymentYaml'.format(self.api_version),
            data=body,
        )
        return Command(self, response)

    def get_kubernetes_environment_agent_events(self, environment_id, offset=None, len=None, order='ASC'):
        """Retrieve the event logs for a Kubernetes environment's agent.

        Args:
            environment_id (:obj:`str`): The id of the environment.
            offset (:obj:`str`, optional): Default: ``None``.
            len (:obj:`int`, optional): Default: ``None``.
            order (:obj:`str`, optional): Default: ``'ASC'``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'environment_id'))
        endpoint = '/v{}/csp/kubernetes/{}/events'.format(self.api_version, environment_id)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def wait_for_kubernetes_environment_agent_status(self, environment_id, agent_status, timeout_sec=900):
        """Block until a Kubernetes environment agent reaches the desired status.

        Args:
            environment_id (:obj:`str`): The environment id.
            agent_status (:obj:`str`): The desired agent status to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``environment`` to reach ``agent status``,
             in seconds. Default: ``900``.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``environment`` reaching ``agent status``.
        """

        def condition():
            response_json = self.get_environment(environment_id).response.json()
            current_agent_status = response_json['agent']['status']
            logger.debug('Environment has current agent status %s  ...', current_agent_status)
            return current_agent_status == agent_status

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for agent status.'.format(timeout))

        def success(time):
            logger.debug('Environment reached desired agent status after %s s.', time)

        logger.debug('Environment with id %s waiting for agent status %s ...', environment_id, agent_status)
        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure, success=success)

    def enable_environment(self, environment_id):
        """Enable the Environment for the given Environment ID.

        Args:
            environment_id (:obj:`str`): Id of the environment.
            body (:obj:`str`): environment in JSON format. Complies to Swagger CspEnvironmentJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/environment/{}/enable'.format(self.api_version, environment_id)
        )
        return Command(self, response)

    def enable_environments(self, environment_ids):
        """Enable the environments.

        Args:
            environment_ids (:obj:`str`): environment IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/environments/enableEnvironments'.format(self.api_version),
            data=environment_ids,
        )
        return Command(self, response)

    def disable_environment(self, environment_id):
        """Disable the Environment for the given Environment ID.

        Args:
            environment_id (:obj:`str`): Id of the environment.
            body (:obj:`str`): environment in JSON format. Complies to Swagger CspEnvironmentJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/environment/{}/disable'.format(self.api_version, environment_id)
        )
        return Command(self, response)

    def disable_environments(self, environment_ids):
        """Disable the environments.

        Args:
            environment_ids (:obj:`list`): environment IDs.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/environments/disableEnvironments'.format(self.api_version),
            data=environment_ids,
        )
        return Command(self, response)

    def wait_for_environment_status(self, environment_id, status, timeout_sec=900):
        """Block until an environment reaches the desired status.

        Args:
            environment_id (:obj:`str`): The environment id.
            status (:obj:`str`): The desired status to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``environment`` to reach ``status``, in seconds.
                Default: ``300``.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``environment`` reaching ``status``.
        """

        def condition():
            response_json = self.get_environment(environment_id).response.json()
            current_status = response_json['status']
            logger.debug(
                'Environment has current status %s and status_detail as %s ...',
                current_status,
                response_json['statusDetail'],
            )

            if current_status == "ERROR":
                raise RuntimeError(
                    'Environment entered unexpected state: {} while trying to enter state: {} due to: {}'.format(
                        current_status, status, response_json['statusDetail']
                    )
                )

            return current_status == status

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for status.'.format(timeout))

        def success(time):
            logger.debug('environment reached desired status after %s s.', time)

        logger.debug('environment %s waiting for status %s ...', environment_id, status)
        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure, success=success)

    def wait_for_environment_state_display_label(self, environment_id, state_display_label, timeout_sec=300):
        """Block until an environment reaches the desired status.

        Args:
            environment_id (:obj:`str`): The environment id.
            state_display_label (:obj:`str`): The desired state_display_label to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``environment`` to reach ``status``, in seconds.
                Default: ``300``.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``environment`` reaching ``state_display_label``.
        """

        def condition():
            response_json = self.get_environment(environment_id).response.json()
            current_state_display_label = response_json['stateDisplayLabel']
            logger.debug('Environment has current current_state_display_label %s  ...', current_state_display_label)
            if current_state_display_label in ("ACTIVATION_ERROR", "DEACTIVATION_ERROR"):
                raise RuntimeError(
                    'Environment entered unexpected state: {} while trying to enter state: {} due to: {}'.format(
                        current_state_display_label, state_display_label, response_json['statusDetail']
                    )
                )
            return current_state_display_label == state_display_label

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for state_display_label.'.format(timeout))

        def success(time):
            logger.debug('Environment reached desired state_display_label after %s s.', time)

        logger.debug(
            'Environment with id %s waiting for state_display_label %s ...', environment_id, state_display_label
        )
        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure, success=success)

    def get_deployment_engine_acl_audits(
        self, organization, offset=None, len=None, sort_field='NAME', sort_order='ASC'
    ):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'NAME'``
            sort_order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/deployment/engine/listAclAudits'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_deployment_post_stop_script(self, deployment_id):
        """Get Post Stop Script for the Engine for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/engine/{}/postStopScript'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_deployment_pre_start_script(self, deployment_id):
        """Get Post Stop Script for the Engine for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/engine/{}/preStartScript'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_deployment_acl_audits(self, organization, offset=None, len=None, sort_field='NAME', sort_order='ASC'):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'NAME'``
            sort_order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/deployment/listAclAudits'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_deployment_self_acl_audits(self, organization, offset=None, len=None, sort_field='NAME', sort_order='ASC'):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'NAME'``
            sort_order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/deployment/self/listAclAudits'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_self_managed_deployment_download_and_start_script(self, deployment_id):
        """Get download and start script for Self Managed Deployment with Tarball installation.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.Response content-type is application/octet-stream.
        """
        endpoint = '/v{}/csp/deployment/self/{}/downloadAndStartEngine'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_self_managed_deployment_install_command(
        self, deployment_id, install_mechanism='DEFAULT', install_type=None, java_version=None
    ):
        """Get install Command for Self Managed Deployment.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            install_mechanism (:obj:`str`, optional): Possible values for install are "DEFAULT", "BACKGROUND" and
                                                      "FOREGROUND". Default: ``DEFAULT``
            install_type (:obj:`str`, optional): Possible values for install are "DOCKER", and "TARBALL".
                Default: ``None``.
            java_version (:obj:`int`, optional): Supported Java version. Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.Response content-type is text/plain.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        endpoint = '/v{}/csp/deployment/self/{}/installCommand'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_deployment_engine_url(self, deployment_id):
        """Get the URL, with port number, of the self-managed engine that is about to start. Domain name may be blank.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/self/{}/getEngineUrl'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_deployment_has_engine(self, deployment_id, engine_id):
        """Does the given engine ID exist for the given Deployment ID?

        Args:
            deployment_id (:obj:`str`): Deployment ID
            engine_id (:obj:`str`): Engine ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/hasEngine/{}'.format(self.api_version, deployment_id, engine_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_deployment(self, deployment_id):
        """Return deployment for given deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def delete_deployment(self, deployment_id):
        """Delete an existing deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._delete(
            app='provisioning', endpoint='/v{}/csp/deployment/{}'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def can_delete_deployment(self, deployment_id):
        """Check if the user can delete a given deployment ID.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/canDelete'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def delete_deployments(self, deployment_ids, stop=True):
        """Delete existing deployments.

        Args:
            deployment_ids (py:obj:`list`): Ids of the deployments.
            stop (:obj:`bool`): Stop the deployment. Default ``True``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_ids'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployments/deleteDeployments'.format(self.api_version),
            params=params,
            data=deployment_ids,
        )
        return Command(self, response)

    def update_deployment(self, deployment_id, body, complete='undefined', process_if_enabled='undefined'):
        """Update an existing deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.
            body (:obj:`str`): deployment in JSON format. Complies to Swagger CspEnvironmentJson definition.
            complete (:obj:`str`, optional): Default: ``undefined``
            process_if_enabled (:obj:`str`, optional): Default: ``undefined``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'body'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployment/{}'.format(self.api_version, deployment_id),
            data=body,
            params=params,
        )
        return Command(self, response)

    def get_deployment_acl(self, deployment_id):
        """Return ACL for a given deployment.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/acl'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def update_deployment_acl(self, deployment_id, body):
        """Update ACL for a given deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.
            body (:obj:`str`): deployment ACL in JSON format. Complies to Swagger AclJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/acl'.format(self.api_version, deployment_id), data=body
        )
        return Command(self, response)

    def enable_deployments(self, deployment_ids):
        """Enable deployments for the given deployment IDs.

        Args:
            deployment_ids (:obj:`list`): Ids of the deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployments/enableDeployments'.format(self.api_version),
            data=deployment_ids,
        )
        return Command(self, response)

    def enable_deployment(self, deployment_id):
        """Enable the deployment for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/enable'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def disable_deployment(self, deployment_id):
        """Disable the deployment for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/disable'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def disable_deployments(self, deployment_ids):
        """Disable the deployments for the given deployment IDs.

        Args:
            deployment_ids (:obj:`list`): Ids of the deployments.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployments/disableDeployments'.format(self.api_version),
            data=deployment_ids,
        )
        return Command(self, response)

    def lock_deployment(self, deployment_id):
        """Lock the deployment for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/lock'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def unlock_deployment(self, deployment_id):
        """Unlock the deployment for the given deployment ID.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/unlock'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def wait_for_deployment_status(self, deployment_id, status, timeout_sec=900):
        """Block until a deployment reaches the desired status.

        Args:
            deployment_id (:obj:`str`): The deployment id.
            status (:obj:`str`): The desired status to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``deployment`` to reach ``status``, in seconds.
                Default: ``300``.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``deployment`` reaching ``status``.
        """

        def condition():
            response_json = self.get_deployment(deployment_id).response.json()
            current_status = response_json['status']
            logger.debug(
                'Deployment has current status %s and status_detail as %s ...',
                current_status,
                response_json['statusDetail'],
            )

            if current_status == "ERROR":
                raise RuntimeError(
                    'Deployment entered unexpected state: {} while trying to enter state: {} due to: {}'.format(
                        current_status, status, response_json['statusDetail']
                    )
                )

            return current_status == status

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for status.'.format(timeout))

        def success(time):
            logger.debug('deployment reached desired status after %s s.', time)

        logger.debug('deployment %s waiting for status %s ...', deployment_id, status)
        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure, success=success)

    def wait_for_deployment_state_display_label(self, deployment_id, state_display_label, timeout_sec=900):
        """Block until a deployment reaches the desired state_display_label.

        Args:
            deployment_id (:obj:`str`): The deployment id.
            state_display_label (:obj:`str`): The desired state_display_label to wait for.
            timeout_sec (:obj:`int`, optional): Timeout to wait for ``deployment`` to reach ``status``, in seconds.
                Default: ``300``.

        Raises:
            TimeoutError: If ``timeout_sec`` passes without ``deployment`` reaching ``state_display_label``.
        """

        def condition():
            response_json = self.get_deployment(deployment_id).response.json()
            current_state_display_label = response_json['stateDisplayLabel']
            logger.debug('Deployment has current current_state_display_label %s  ...', current_state_display_label)
            if current_state_display_label in ("ACTIVATION_ERROR", "DEACTIVATION_ERROR"):
                raise RuntimeError(
                    'Deployment entered unexpected state: {} while trying to enter state: {} due to: {}'.format(
                        current_state_display_label, state_display_label, response_json['statusDetail']
                    )
                )

            return current_state_display_label == state_display_label

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for state_display_label.'.format(timeout))

        def success(time):
            logger.debug('deployment reached desired state_display_label after %s s.', time)

        logger.debug('deployment %s waiting for state_display_label %s ...', deployment_id, state_display_label)
        wait_for_condition(condition=condition, timeout=timeout_sec, failure=failure, success=success)

    def get_deployment_engine_token(self, deployment_id):
        """Fetches a Engine Token for the Deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/engineToken'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def get_deployment_engine_configs(self, deployment_id):
        """Get Engine Configuration for Deployment.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/engineConfigs'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_deployment_events(
        self, deployment_id, source_type=None, source_id=None, hostname=None, offset=None, len=None, order='ASC'
    ):
        """Get Deployment events.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            source_type (:obj:`str`, optional): Default: ``None``
            source_id (:obj:`str`, optional): Default: ``None``
            hostname (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        endpoint = '/v{}/csp/deployment/{}/events'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def report_deployment_engine_event(self, deployment_id, body):
        """Report an event from an engine.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.
            body (:obj:`str`): deployment ACL in JSON format. Complies to Swagger CspEngineEventJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployment/{}/events'.format(self.api_version, deployment_id),
            data=body,
        )
        return Command(self, response)

    def get_deployment_permissions(self, deployment_id, subject_id):
        """Get permissions on a given deployment for a given subject.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            subject_id (:obj:`str`): Subject ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/permissions/{}'.format(self.api_version, deployment_id, subject_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def update_deployment_permissions(self, body, deployment_id, subject_id):
        """Update permissions on a given deployment for a given subject.

        Args:
            body (:obj:`str`): deployment ACL in JSON format. Complies to Swagger CspEngineEventJson definition.
            deployment_id (:obj:`str`): Id of the deployment.
            subject_id (:obj:`str`): Subject ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/permissions/{}'.format(self.api_version, deployment_id, subject_id)
        response = self._post(app='provisioning', endpoint=endpoint, data=body)
        return Command(self, response)

    def restart_deployment_engines(self, engine_ids):
        """Request a restart for all given Deployment managed Engine IDs.

        Args:
            engine_ids (:obj:`list`): Ids of the engines.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/sdcs/restartEngines'.format(self.api_version), data=engine_ids
        )
        return Command(self, response)

    def shutdown_deployment_engines(self, engine_ids):
        """Request a shutdown for all given Deployment managed Engine IDs.

        Args:
            engine_ids (:obj:`list`): Ids of the engines.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='jobrunner', endpoint='/v{}/sdcs/shutdownEngines'.format(self.api_version), data=engine_ids
        )
        return Command(self, response)

    def restart_deployment_all_engines(self, deployment_id):
        """Restart all engines from a deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployment/{}/restartEngines'.format(self.api_version, deployment_id)
        )
        return Command(self, response)

    def get_deployment_registered_engines(
        self, deployment_id, offset=0, len=5, order_by='LAST_REPORTED_TIME', order='ASC', with_wrapper=True
    ):
        """Returns all registered engines' list for a Deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_total_count (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        endpoint = '/v{}/sdcs/cspDeployment/{}'.format(self.api_version, deployment_id)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_legacy_deployment_sdcs(
        self, deployment_id, offset=None, len=None, order_by='LAST_REPORTED_TIME', order='ASC', with_wrapper=False
    ):
        """Returns all registered SDCs list for a Legacy Deployment ID.

        Args:
            deployment_id (:obj:`str`): Deployment ID
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'LAST_REPORTED_TIME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_wrapper (:obj:`bool`, optional): Default: ``None``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id'))
        endpoint = '/v{}/sdcs/legacyDeployment/{}'.format(self.api_version, deployment_id)
        response = self._get(app='jobrunner', endpoint=endpoint, params=params)
        return Command(self, response)

    def get_deployment_stale_engines(self, deployment_id):
        """Get Engines with stale configuration for the Deployment.

        Args:
            deployment_id (:obj:`str`): Deployment ID

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/staleEngines'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_all_deployments(
        self,
        organization,
        type=None,
        state_display_label=None,
        deployment_status=None,
        environment=None,
        tag=None,
        engine_type=None,
        offset=None,
        len=None,
        order_by='NAME',
        order='ASC',
        with_total_count=False,
    ):
        """Returns deployments a user has access to.

        Args:
            organization (:obj:`str`)
            type (:obj:`str`, optional): deployment type Default: ``None``
            state_display_label (:obj:`str`, optional): Default: ``None``
            deployment_status (:obj:`str`, optional): Default: ``None``
            environment (:obj:`str`, optional): Default: ``None``
            tag (:obj:`str`, optional): Default: ``None``
            engine_type (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            with_total_count (:obj:`bool`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        endpoint = '/v{}/csp/deployments'.format(self.api_version)
        response = self._get(app='provisioning', endpoint=endpoint, params=params)
        return Command(self, response)

    def create_deployment(self, body):
        """Create a new deployment.

        Args:
           body (:obj:`str`): deployment in JSON format. Complies to Swagger CreateCspdeploymentJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._put(app='provisioning', endpoint='/v{}/csp/deployments'.format(self.api_version), data=body)
        return Command(self, response)

    def get_deployment_acls(self, body):
        """Returns Acls for all given Deployment IDs.

        Args:
            body (:obj:`str`): deployment ACL in JSON format. Complies to Swagger AclJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning', endpoint='/v{}/csp/deployments/acls'.format(self.api_version), data=body
        )
        return Command(self, response)

    def update_one_file_for_advanced_config(self, deployment_id, file_name, file_to_update):
        """Update one file of the advanced configuration.

        Args:
            deployment_id (:obj:`str`): Deployment ID.
            file_name (:obj:`str`): Name of the file to be updated.
            file_to_update (:obj:`file`): file to be updated

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'deployment_id', 'file_to_update'))
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployment/{}/advancedConfiguration'.format(self.api_version, deployment_id),
            files={'file': file_to_update},
            headers={'content-type': None},
            params=params,
        )
        return Command(self, response)

    def get_all_deployment_audits(self, organization, offset=None, len=None, sort_field='NAME', sort_order='ASC'):
        """Get all deployment audits.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            sort_field (:obj:`str`, optional): Default: ``'NAME'``
            sort_order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/deployments/audits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_all_deployment_acl_audits(self, organization, offset=None, len=None, order_by='NAME', sort_order='ASC'):
        """Get all user actions for given Organization ID.

        Args:
            organization (:obj:`str`)
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'NAME'``
            sort_order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/deployments/listAclAudits'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_all_deployment_tags(self, organization, parent_id=None, offset=None, len=None, order='ASC'):
        """Returns all available deployment Tags.

        Args:
            organization (:obj:`str`)
            parent_id (:obj:`str`, optional): Default: ``None``
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order (:obj:`str`, optional): Default: ``'ASC'``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/deployments/tags'.format(self.api_version), params=params
        )
        return Command(self, response)

    def clone_deployment(self, deployment_id, body=None):
        """Clones existing deployment.

        Args:
            deployment_id (:obj:`str`): Id of the deployment.
            body (:obj:`str`, optional): Complies to Swagger CspCloneDeploymentJson definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='provisioning',
            endpoint='/v{}/csp/deployment/{}/clone'.format(self.api_version, deployment_id),
            data=body,
        )
        return Command(self, response)

    def get_cloned_deployment_metadata(self, deployment_id):
        """
        Return Metadata associated with cloned deployment

        Args:
            deployment_id (:obj:`str`): Id of the deployment.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/deployment/{}/clonedDeploymentMetadata'.format(self.api_version, deployment_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_all_engine_versions(
        self,
        offset=None,
        len=None,
        order_by='CREATE_TIME',
        order='ASC',
        engine_type='DC',
        disabled_filter='ONLY_ALLOWED',
        with_total_count=None,
        designer=False,
        releases_only=False,
    ):
        """Returns all Engine Versions.

        Args:
            offset (:obj:`str`, optional): Default: ``None``
            len (:obj:`int`, optional): Default: ``None``
            order_by (:obj:`str`, optional): Default: ``'CREATE_TIME'``
            order (:obj:`str`, optional): Default: ``'ASC'``
            engine_type (:obj:`str`, optional): Default: ``'DC'``
            disabled_filter (:obj:`str`, optional): Default: ``'ONLY_ALLOWED'``
            with_total_count (:obj:`str`, optional): Default: ``None``
            designer (:obj:`boolean`, optional): Default: ``False``
            releases_only (:obj:`boolean`, optional): Default: ``False``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        response = self._get(
            app='provisioning', endpoint='/v{}/csp/engineVersions'.format(self.api_version), params=params
        )
        return Command(self, response)

    def get_engine_version(self, engine_version_id):
        """Returns Engine Version for given Engine Version Id.

        Args:
            engine_version_id (:obj:`str`): engine version ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/csp/engineVersion/{}'.format(self.api_version, engine_version_id)
        response = self._get(app='provisioning', endpoint=endpoint)
        return Command(self, response)

    def get_engine_configuration(self, engine_id, tunneling_instance_id):
        """Returns the Engine configuration for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/system/configuration'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def get_engine_external_resources(self, engine_id, tunneling_instance_id):
        """Returns the external resources for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/resources/list'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def add_external_resource_to_engine(self, engine_id, resource, tunneling_instance_id):
        """Upload resources to an engine.

        Args:
            engine_id (:obj:`str`): Engine ID.
            resource (:obj:`file`): Resource file in binary format, an io.BufferedReader object.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.

        Raises:
            TypeError: Thrown if and when 'resource' is not an io.BufferedReader object
        """
        endpoint = '/v{}/resources/upload'.format(self.api_version)
        if not isinstance(resource, io.BufferedReader):
            raise TypeError('Resource should be an io.BufferedReader object')
        file_size = resource.seek(0, 2)
        resource.seek(0)

        response = self._post_via_tunneling(
            endpoint=endpoint,
            engine_id=engine_id,
            tunneling_instance_id=tunneling_instance_id,
            form_data='formData',
            files={'file': resource, 'fileSize': file_size},
            headers={'content-type': None},
        )
        return Command(self, response)

    def delete_external_resources_from_engine(self, engine_id, resources, tunneling_instance_id):
        """Delete a resource from an engine.

        Args:
            engine_id (:obj:`str`): Engine ID.
            resources: A :obj:`list` of one or more :py:class:`streamsets.sdk.sch_models.ExternalResource` instances
                in JSON format.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/resources/delete'.format(self.api_version)
        response = self._post_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id, data=resources
        )
        return Command(self, response)

    def get_engine_external_libraries(self, engine_id, tunneling_instance_id):
        """Returns the external libraries for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/stageLibraries/extras/list'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def add_external_libraries_to_engine(self, engine_id, stage_library, external_lib, tunneling_instance_id):
        """Add external libraries to an engine.

        Args:
            engine_id (:obj:`str`): Engine ID.
            stage_library (:obj:`str`): Stage library name.
            external_lib (:obj:`file`): Library file in binary format, an io.BufferedReader object.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.

        Raises:
            TypeError: Thrown if and when 'external_lib' is not an io.BufferedReader object
        """
        endpoint = '/v{}/stageLibraries/extras/{}/upload'.format(self.api_version, stage_library)
        if not isinstance(external_lib, io.BufferedReader):
            raise TypeError('Library should be an io.BufferedReader object')
        file_size = external_lib.seek(0, 2)
        external_lib.seek(0)
        response = self._post_via_tunneling(
            endpoint=endpoint,
            engine_id=engine_id,
            tunneling_instance_id=tunneling_instance_id,
            form_data='formData',
            files={'file': external_lib, 'fileSize': file_size},
            headers={'content-type': None},
        )
        return Command(self, response)

    def delete_external_libraries_from_engine(self, engine_id, external_libs, tunneling_instance_id):
        """Add external libraries to an engine.

        Args:
            engine_id (:obj:`str`): Engine ID.
            external_libs: A :obj:`list` of one or more :py:class:`streamsets.sdk.sch_models.ExternalLibrary`
                instances in JSON format.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/stageLibraries/extras/delete'.format(self.api_version)
        response = self._post_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id, data=external_libs
        )
        return Command(self, response)

    def get_engine_user_stage_libraries(self, engine_id, tunneling_instance_id):
        """Returns the external resources for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/userStageLibraries/list'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def get_engine_logs(self, engine_id, tunneling_instance_id, ending_offset=-1):
        """Get the logs for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.
            ending_offset (:obj:`int`, optional): Offset of the ending of the logs. Default: ``-1``

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('engine_id', 'tunneling_instance_id', 'self'))
        endpoint = '/v{}/system/logs'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id, params=params
        )
        return Command(self, response)

    def get_engine_thread_dump(self, engine_id, tunneling_instance_id):
        """Returns a thread dump for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = '/v{}/system/threads'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def get_engine_directories(self, engine_id, tunneling_instance_id=None):
        """Returns a thread dump for the given engine_id using the engine's tunneling endpoint.

        Args:
            engine_id (:obj:`str`): Engine ID.
            tunneling_instance_id (:obj:`str`, optional): Tunneling instance ID.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        endpoint = 'v{}/system/directories'.format(self.api_version)
        response = self._get_via_tunneling(
            endpoint=endpoint, engine_id=engine_id, tunneling_instance_id=tunneling_instance_id
        )
        return Command(self, response)

    def start_streamflake_explorer_search(
        self,
        pipeline_id,
        rev,
        stage_id,
        element='',
        extra_depth=0,
        fixed_params=None,
        len_=100,
        offset=0,
        search='',
        up_truncate=False,
        timeout=60000,
    ):
        """Start a System Explorer search for a stage.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            rev (:obj:`str`): Pipeline revision ID.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.
            element (:obj:`str`, optional): The Explorer schema element for the search result, to set in the
                stage configuration. Default: ''
            extra_depth (:obj:`int`, optional): How many levels of children elements of the schema element being
                searched should be returned. Default: 0
            fixed_params (:obj:`dict`, optional): Fixed elements of the search. Defult: None
            len_ (:obj:`str`, optional): Maximum number of records to retrieve. Default: 100
            offset (:obj:`int`, optional): The offset from where to return data. Search result data pages have a fixed
                size of 1000. Default: 0
            search (:obj:`str`, optional):  The search query, an RSQL predicate where the Explorer schema elements of
                the stage are the valid RSQL selector names. Default: ''
            up_truncate (:obj:`bool`, optional): Return the result tree starting from the searched schema element.
                Default: False
            timeout (:obj:`int`, optional): Timeout in milliseconds for the search request. Default: 60000

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self', 'pipeline_id', 'stage_id'))
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer/{}'.format(pipeline_id, stage_id)

        if 'fixedParams' in params:
            fixed = params.pop('fixedParams')
            for parm, value in fixed.items():
                params.update({f'fixed.{parm}': value})

        response = self._post(endpoint=endpoint, app='pipelinestore', params=params)
        return Command(self, response)

    def check_streamflake_explorer_search(self, explorer_id, pipeline_id, stage_id):
        """Return a System Explorer search status/data.

        Args:
            explorer_id (:obj:`str`): Explorer search id.
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer/{}/{}'.format(pipeline_id, stage_id, explorer_id)
        response = self._get(endpoint=endpoint, app='pipelinestore')
        return Command(self, response)

    def stop_streamflake_explorer_search(self, explorer_id, pipeline_id, stage_id):
        """Cancels a System Explorer search.

        Args:
            explorer_id (:obj:`str`): Explorer search id.
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer/{}/{}'.format(pipeline_id, stage_id, explorer_id)
        response = self._delete(endpoint=endpoint, app='pipelinestore')
        return Command(self, response)

    def start_streamflake_explorer_load(self, pipeline_id, rev, stage_id, reload=False, timeout=60000):
        """Loads System Explorer data of a stage.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            rev (:obj:`str`): Pipeline revision ID.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.
            reload (:obj:`bool`, optional): Force the Explorer to reload metadata from the connection before
                performing the search. Default: False
            timeout (:obj:`int`, optional): Timeout in milliseconds for the search request. Default: 60000

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('stage_id', 'pipeline_id', 'self'))
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer-load/{}'.format(pipeline_id, stage_id)
        response = self._post(endpoint=endpoint, app='pipelinestore', params=params)
        return Command(self, response)

    def check_streamflake_explorer_load(self, pipeline_id, rev, stage_id):
        """Returns System Explorer data load state of a stage.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            rev (:obj:`str`): Pipeline revision ID.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('stage_id', 'pipeline_id', 'self'))
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer-load/{}'.format(pipeline_id, stage_id)
        response = self._get(endpoint=endpoint, app='pipelinestore', params=params)
        return Command(self, response)

    def stop_streamflake_explorer_load(self, pipeline_id, rev, stage_id):
        """Cancels the System Explorer data load of a stage.

        Args:
            pipeline_id (:obj:`str`): Pipeline ID of the stage.
            rev (:obj:`str`): Pipeline revision ID.
            stage_id (:obj:`str`):  Stage ID on which the system explorer search is performed.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('stage_id', 'pipeline_id', 'self'))
        sf_endpoint = '/v{}/pipeline/snowflake/rest/v{}'.format(self.api_version, self.explorer_api_version)
        endpoint = sf_endpoint + '/pipeline/{}/streamflake-explorer-load/{}'.format(pipeline_id, stage_id)
        response = self._delete(endpoint=endpoint, app='pipelinestore', params=params)
        return Command(self, response)

    def expire_free_trial_orgs(self):
        """Make the call to start expire free trial background task, should be made by SYS-ADMINS.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='security', endpoint='/v{}/organizations/expireFreeTrial'.format(self.api_version))
        return Command(self, response)

    def get_organization_ids_by_configuration_filters(self, filters):
        """Get organization IDs based on their configuration. To be run as a SYS-ADMIN.

        Arguments:
            filters (:py:obj:`list`): A `list` of :py:obj:`dict` containing filters for organizations.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.

        """
        # we need to dump it to be able to pass it as a query string param
        filters = json.dumps(filters)
        params = get_params(locals(), exclusions=('self',))
        response = self._get(
            app='security', endpoint='/v{}/organizations/configs'.format(self.api_version), params=params
        )
        return Command(self, response)

    def create_banner(self, body):
        """Create a banner, call should be made as a Sys-Admin.

        Args:
            body (:py:obj:`dict`): Request body conforming to the Swagger API definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='banner', endpoint='/v{}/banners'.format(self.banner_api_version), data=body)
        return Command(self, response)

    def get_all_banners(self, page=0, size=10, sort="endsOn"):
        """Get all banners, call made by Sys-Admins. (Paginated)

        Args:
            page (:py:obj:`int`, optional): Page number to get.
            size (:py:obj:`int`, optional): Number of items in response.
            sort (:py:obj:`str`, optional): How to sort items before getting the response.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=(self,))
        response = self._get(app='banner', endpoint='/v{}/banners'.format(self.banner_api_version), params=params)
        return Command(self, response)

    def get_session_banners(self):
        """Get session banners for a user, call made by Org-User.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='banner', endpoint='/v{}/banners/me'.format(self.banner_api_version))
        return Command(self, response)

    def get_banner_by_id(self, banner_id):
        """Get a banners, call made by Sys-Admins.

        Args:
            banner_id (:py:obj:`str`): ID of the banner to retrieve.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app='banner', endpoint='/v{}/banners/{}'.format(self.banner_api_version, banner_id))
        return Command(self, response)

    def delete_banner(self, banner_id):
        """Delete a banner, call should be made as a Sys-Admin.

        Args:
            banner_id (:py:obj:`str`): ID of banner to delete.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(
            app='banner', endpoint='/v{}/banners/delete/{}'.format(self.banner_api_version, banner_id)
        )
        return Command(self, response)

    def batch_delete_banner(self, body):
        """Delete a banner, call should be made as a Sys-Admin.

        Args:
            body (:py:obj:`dict`): Request body conforming to the Swagger API definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='banner', endpoint='/v{}/banners/delete'.format(self.banner_api_version), data=body)
        return Command(self, response)

    def dismiss_banner(self, body):
        """Dismiss a banner by ID.

        Args:
            body (:py:obj:`dict`): Request body conforming to the Swagger API definition.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._post(app='banner', endpoint='/v{}/dismissals'.format(self.banner_api_version), data=body)

        return Command(self, response)

    def get_banner_api(self):
        try:
            response = self._get(app='banner', endpoint='swagger.json')
            return response.json()
        except HTTPError:
            return None

    def get_provisioning_api(self):
        response = self._get(app='provisioning', endpoint='swagger.json')
        return response.json()

    def get_connection_api(self):
        response = self._get(app='connection', endpoint='swagger.json')
        return response.json()

    def get_security_api(self):
        response = self._get(app='security', endpoint='swagger.json')
        return response.json()

    def get_pipelinestore_api(self):
        response = self._get(app='pipelinestore', endpoint='swagger.json')
        return response.json()

    def get_job_api(self):
        response = self._get(app='jobrunner', endpoint='swagger.json')
        return response.json()

    def get_topology_api(self):
        response = self._get(app='topology', endpoint='swagger.json')
        return response.json()

    def get_scheduler_api(self):
        response = self._get(app='scheduler', endpoint='swagger.json')
        return response.json()

    def get_notification_api(self):
        response = self._get(app='notification', endpoint='swagger.json')
        return response.json()

    def get_translations_json(self):
        response = self._get(app='assets', rest='i18n', endpoint='en.json')
        return response.json()

    def get_sla_api(self):
        response = self._get(app='sla', endpoint='swagger.json')
        return response.json()

    def get_sequencing_api(self):
        try:
            response = self._get(app='sequencing', endpoint='swagger.json')
            return response.json()
        except Exception:
            return None

    # Internal functions only below.
    @retry_on_connection_error
    def _delete(self, app, endpoint, rest='rest', params=None):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.delete(url, params=params or {})
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _delete_via_tunneling(
        self, endpoint, tunneling_instance_id, rest='rest', tunneling='tunneling', engine_id=None, params=None
    ):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(
            self.base_url,
            '/{}'.format(tunneling),
            '/{}'.format(rest),
            '/{}'.format(engine_id),
            '/{}'.format(rest),
            endpoint,
        )
        if params is None:
            params = {}
        # Platform's APIs use an unconventional parameter for tunneling instance ID that doesn't conform to the
        # same naming convention as other parameters, thus we have to set it manually here
        params.update({'TUNNELING_INSTANCE_ID': tunneling_instance_id})
        response = self.session.delete(url, params=params)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _get(self, endpoint, app=None, rest='rest', params=None, headers=None, absolute_endpoint=False):
        self.update_session_headers_with_analytics_data()
        url = endpoint if absolute_endpoint else join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.get(url, params=params or {}, headers=headers)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _get_via_tunneling(
        self, endpoint, tunneling_instance_id, rest='rest', tunneling='tunneling', engine_id=None, params=None
    ):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(
            self.base_url,
            '/{}'.format(tunneling),
            '/{}'.format(rest),
            '/{}'.format(engine_id),
            '/{}'.format(rest),
            endpoint,
        )
        if params is None:
            params = {}
        # Platform's APIs use an unconventional parameter for tunneling instance ID that doesn't conform to the
        # same naming convention as other parameters, thus we have to set it manually here
        params.update({'TUNNELING_INSTANCE_ID': tunneling_instance_id})
        response = self.session.get(url, params=params)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _post(
        self, endpoint, app=None, rest='rest', params=None, data=None, files=None, headers=None, absolute_endpoint=False
    ):
        self.update_session_headers_with_analytics_data()
        url = endpoint if absolute_endpoint else join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        if not data:
            data = None
        else:
            data = data if isinstance(data, str) else json.dumps(data)
        response = self.session.post(url, params=params or {}, data=data, files=files, headers=headers)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _post_via_tunneling(
        self,
        endpoint,
        tunneling_instance_id,
        rest='rest',
        tunneling='tunneling',
        form_data=None,
        params=None,
        data=None,
        files=None,
        headers=None,
        engine_id=None,
    ):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(self.base_url, tunneling, rest, form_data, engine_id, rest, endpoint)
        if params is None:
            params = {}
        # Platform's APIs use an unconventional parameter for tunneling instance ID that doesn't conform to the
        # same naming convention as other parameters, thus we have to set it manually here
        params.update({'TUNNELING_INSTANCE_ID': tunneling_instance_id})
        if data:
            data = data if isinstance(data, str) else json.dumps(data)
        response = self.session.post(url, params=params, data=data, files=files, headers=headers)
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _put(self, app, endpoint, rest='rest', params=None, data=None):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.put(url, params=params or {}, data=json.dumps(data or {}))
        self._handle_http_error(response)
        return response

    @retry_on_connection_error
    def _put_via_tunneling(
        self,
        endpoint,
        tunneling_instance_id,
        rest='rest',
        tunneling='tunneling',
        engine_id=None,
        params=None,
        data=None,
    ):
        self.update_session_headers_with_analytics_data()
        url = join_url_parts(
            self.base_url,
            '/{}'.format(tunneling),
            '/{}'.format(rest),
            '/{}'.format(engine_id),
            '/{}'.format(rest),
            endpoint,
        )
        if params is None:
            params = {}
        # Platform's APIs use an unconventional parameter for tunneling instance ID that doesn't conform to the
        # same naming convention as other parameters, thus we have to set it manually here
        params.update({'TUNNELING_INSTANCE_ID': tunneling_instance_id})
        response = self.session.put(url, params=params, data=json.dumps(data or {}))
        self._handle_http_error(response)
        return response

    @staticmethod
    def _handle_http_error(response):
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            try:
                errors = []
                for issue in response.json().get('ISSUES', []):
                    code = issue.get('code', '')
                    if code.startswith('JOBRUNNER'):
                        errors.append(JobRunnerError(code=code, message=issue['message']))
                    elif code.startswith('CONNECTION'):
                        errors.append(ConnectionError(code=code, message=issue['message']))
                if errors:
                    raise MultipleIssuesError(errors) if len(errors) > 1 else errors[0]
            except ValueError:
                # If response cannot be decoded using json, do the normal re-raise below
                pass
            # If the HTTPError isn't handled above, re-raise it with the response text as the message and the
            # response itself as an attribute for further handling.
            raise requests.exceptions.HTTPError(response.text, response=response)


class Command:
    """Command to allow users to interact with commands submitted through DPM REST API.
    Args:
        api_client (:obj:`ApiClient`): DPM API client.
        response (:obj:`requests.Response`): Command reponse.
    """

    # pylint: disable=too-few-public-methods
    def __init__(self, api_client, response):
        self.api_client = api_client
        self.response = response


class CreateComponentsCommand(Command):
    """Command to interact with the response from create_components."""

    # pylint: disable=too-few-public-methods

    @property
    def full_auth_token(self):
        """Full auth token. This is needed by SDC."""
        return self.response.json()[0]['fullAuthToken']


class PreviewCommand(Command):
    """Command returned by preview operations.

    Args:
        api_client (:obj:`ApiClient`): SCH API client.
        response (:obj:`requests.Response`): Command response.
        pipeline_id (:obj:`str`)
        previewer_id (:obj:`str`): Previewer_id.
    """

    def __init__(self, api_client, response, pipeline_id, previewer_id):
        super().__init__(api_client=api_client, response=response)
        self.pipeline_id = pipeline_id
        self.previewer_id = previewer_id

    @property
    def preview(self):
        """The Preview object returned by this preview command.

        Returns:
            (:obj:`st_models.Preview`)
        """
        return st_models.Preview(
            pipeline_id=self.pipeline_id,
            previewer_id=self.previewer_id,
            preview=self.api_client.get_snowflake_preview_data(
                pipeline_id=self.pipeline_id, previewer_id=self.previewer_id
            ).response.json(),
        )

    def wait_for_finished(self, timeout_sec=30):
        """Wait for preview to be finished.

        Args:
            timeout_sec (:obj:`int`, optional): Timeout for wait, in seconds. Default: 30
        """
        logger.info('Waiting for preview to be finished...')
        stop_waiting_time = time() + timeout_sec

        while time() < stop_waiting_time:
            self.response = self.api_client.get_snowflake_preview_status(
                pipeline_id=self.pipeline_id, previewer_id=self.previewer_id
            ).response
            logger.debug('response.content: %s', self.response.content)
            # Loop back until response content starts coming through.
            if not self.response.content:
                continue

            current_status = self.response.json()['status']
            if current_status == 'FINISHED':
                logger.debug(
                    'Pipeline (%s) preview (%s) reached state : %s', self.pipeline_id, self.previewer_id, current_status
                )
                return self

            sleep(1)

        raise TimeoutError('Timed out after {} seconds while waiting for status FINISHED.'.format(timeout_sec))


# At the moment, this class only makes sense for Snowflake pipelines. When we extend ControlHub.validate_pipeline
# to Data Collector, etc., we'll need to refactor this extensively.
class ValidateCommand(Command):
    """State holder for a pipeline validation call.

    Args:
        api_client (:obj:`streamsets.sdk.sch_api.ApiClient`): API client.
        response (:obj:`requests.Response`): Command response.
        pipeline_id (:obj:`str`): Pipeline ID.
        previewer_id (:obj:`str`): Previewer ID.
    """

    def __init__(self, api_client, response, pipeline_id, previewer_id):
        super().__init__(api_client=api_client, response=response)
        self.pipeline_id = pipeline_id
        self.previewer_id = previewer_id

    def wait_for_validate(self, timeout_sec=30, engine_id=None, tunneling_instance_id=None):
        """Wait for validate to be finished.

        Args:
            timeout_sec (:obj:`int`, optional): Timeout for wait, in seconds. Default: 30
            engine_id (:obj:`str`, optional): Default: ``None``
            tunneling_instance_id (:obj:`str`, optional): Default: ``None``
        """
        logger.info('Waiting for validate to be finished...')
        stop_waiting_time = time() + timeout_sec

        while time() < stop_waiting_time:
            if engine_id:
                self.response = self.api_client.get_pipeline_preview_status(
                    engine_id=engine_id,
                    pipeline_id=self.pipeline_id,
                    previewer_id=self.previewer_id,
                    tunneling_instance_id=tunneling_instance_id,
                ).response
            else:
                self.response = self.api_client.get_snowflake_preview_status(
                    pipeline_id=self.pipeline_id, previewer_id=self.previewer_id
                ).response
            logger.debug('response.content: %s', self.response.content)
            # Loop back until response content starts coming through.
            if not self.response.content:
                continue

            current_status = self.response.json()['status']
            if current_status not in ['VALIDATING', 'RUNNING']:
                if current_status != 'VALID':
                    if engine_id:
                        preview = self.api_client.get_pipeline_preview_data(
                            engine_id=engine_id,
                            pipeline_id=self.pipeline_id,
                            previewer_id=self.previewer_id,
                            tunneling_instance_id=tunneling_instance_id,
                        )
                    else:
                        preview = self.api_client.get_snowflake_preview_data(
                            pipeline_id=self.pipeline_id, previewer_id=self.previewer_id
                        )
                    self.response = preview.response

                logger.debug(
                    'Pipeline (%s) validate (%s) reached state : %s',
                    self.pipeline_id,
                    self.previewer_id,
                    current_status,
                )
                return self

            sleep(1)

        raise TimeoutError('Timed out after {} seconds while waiting for validation.'.format(timeout_sec))


class SnowflakePipelineCommand(Command):
    """Pipeline Command to allow users to interact with commands submitted through SCH REST API.

    Args:
        api_client (:py:class:`streamsets.sdk.sch_api.ApiClient`): SCH API client.
        response (:py:class:`requests.Response`): Command reponse.
    """

    def wait_for_status(self, status, ignore_errors=False, timeout_sec=300):
        """Wait for pipeline status.

        Args:
            status (:obj:`str`): Pipeline status.
            ignore_errors(:obj:`boolean`): If set to true then this method will not throw
                exception if an error state is detected. Particularly useful if the caller
                needs to wait on one of the terminal error states. Default: ``False``
            timeout_sec (:obj:`int`): Timeout for wait, in seconds. Default: 300
        """
        logger.info('Waiting for status %s ...', status)
        start_waiting_time = time()
        stop_waiting_time = start_waiting_time + timeout_sec

        while time() < stop_waiting_time:
            try:
                pipeline_id = self.response.json()['pipelineId']
            except KeyError:
                pipeline_id = self.response.json()['name']

            current_status = self.response.json()['status']
            logger.debug('Status of pipeline %s is %s ...', pipeline_id, current_status)

            if (isinstance(status, list) and current_status in status) or current_status == status:
                logger.info(
                    'Pipeline %s reached status %s (took %.2f s).',
                    pipeline_id,
                    current_status,
                    time() - start_waiting_time,
                )
                break
            elif not ignore_errors and current_status in STATUS_ERRORS:
                raise STATUS_ERRORS.get(current_status)(self.response.json())
            else:
                sleep(1)
                self.response = self.api_client.get_snowflake_pipeline(pipeline_id).response
        else:
            raise TimeoutError('Timed out after {} seconds while waiting for status {}.'.format(timeout_sec, status))


class StartJobsCommand(Command):
    """Command returned when using startJobs endpoint."""

    def wait_for_pipelines(self, timeout_sec=300):
        """Waits for all jobs' pipelines to reach RUNNING status.

        Args:
            timeout_sec (:py:obj:`int`): Timeout for wait, in seconds. Default: ``300``

        Raises:
            An instance of :py:class:`streamsets.sdk.sdc_api.StatusError` if the pipeline reaches an error state.
        """

        # Utility function to be run by wait_for_condition that returns True when the correct number of pipeline
        # instances are running on engine instances.
        def all_pipeline_instances_running(job):
            job.refresh()
            pipeline_instance_engines = (
                job.data_collectors if getattr(job, 'executor_type', 'COLLECTOR') == 'COLLECTOR' else job.transformers
            )
            logger.debug(
                'Pipeline instance engines: %s', ', '.join(engine.url for engine in pipeline_instance_engines) or 'none'
            )
            return len(pipeline_instance_engines) == job.number_of_instances

        # Another utility function that returns True unless a non-RUNNING status is seen in running pipelines or
        # an Exception is raised. For full details on the algorithm being used, check out TLKT-523.
        def pipelines_started(job):
            job.refresh()
            logger.debug('Saw job status <%s, %s>.', job.status.status, job.status.color)
            pipeline_instance_engines = (
                job.data_collectors if getattr(job, 'executor_type', 'COLLECTOR') == 'COLLECTOR' else job.transformers
            )
            for pipeline_status in job.pipeline_status:
                logger.debug(
                    'Saw pipeline on engine (%s) in status %s.',
                    pipeline_instance_engines.get(id=pipeline_status.sdc_id).url,
                    pipeline_status.status,
                )
                if pipeline_status.status in STATUS_ERRORS:
                    raise STATUS_ERRORS[pipeline_status.status]({'message': pipeline_status.message})

                if pipeline_status.status != 'RUNNING':
                    break
            else:
                return True

        # Transformer for Snowflake pipelines are treated differently since there's no accessible engine to
        # communicate with. Instead, we introspect on the job status' run history.
        def snowflake_pipeline_started(job):
            job.refresh()
            logger.debug('Saw job status <%s, %s>.', job.status.status, job.status.color)
            for job_run_event in job.status.run_history:
                match = re.search(r"pipeline in status '(\w+)'", job_run_event.message)
                # Go on to the next event if no status was displayed in the message.
                if not match:
                    continue
                status = match.group(1)
                if status == 'RUNNING':
                    return True

        def success(time):
            logger.debug('Job reached desired state after %s s.', time)

        def failure(timeout):
            raise TimeoutError('Timed out after {} seconds while waiting for status.'.format(timeout))

        # Actual execution of code starts here.
        for job in self.jobs:
            # A job can sometimes have it’s number_of_instances configuration set to -1,
            # meaning it will run on all available engines that are applicable
            if job.number_of_instances < 0:
                continue

            logger.debug('Waiting for job %s to start successfully ...', job.job_name)
            if job.executor_type != 'SNOWPARK':
                logger.debug(
                    'Waiting for %s pipeline %s ...',
                    job.number_of_instances,
                    'instances' if job.number_of_instances > 1 else 'instance',
                )
                wait_for_condition(
                    all_pipeline_instances_running, [job], timeout=timeout_sec, success=success, failure=failure
                )

                wait_for_condition(pipelines_started, [job], timeout=timeout_sec, success=success, failure=failure)
            else:
                wait_for_condition(
                    snowflake_pipeline_started, [job], timeout=timeout_sec, success=success, failure=failure
                )


class JobStartStopCommand(Command):
    """Command to interact with the response of Start/Stop Job."""

    def wait_for_job_status(self, status, timeout_sec=300):
        """Wait for job status.

        Args:
            status (:obj:`str`): Job status.
            timeout_sec (:obj:`int`): Timeout for wait, in seconds. Default: 300
        """
        self.api_client.wait_for_job_status(self.response.json()['jobId'], status, timeout_sec)


class DeploymentStartStopCommand(Command):
    """Command to interact with the response of Start/Stop Deployment."""

    def wait_for_legacy_deployment_statuses(self, statuses, timeout_sec=300):
        """Wait for deployment statuses.

        Args:
            statuses (:obj:`list`): List of Deployment statuses.
            timeout_sec (:obj:`int`, optional): Timeout for wait, in seconds. Default: ``300``.
        """
        self.api_client.wait_for_legacy_deployment_statuses(self.response.json()['deploymentId'], statuses, timeout_sec)


class AdminToolApiClient(object):
    """
    API client to communicate with a ControlHub admin tool.

    Args:
        base_url (:obj:`str`): ControlHub instance's server URL.
        username (:obj:`str`): ControlHub username.
        password (:obj:`str`): ControlHub password.
        api_version (:obj:`int`, optional): The DPM API version. Default: :py:const:`DEFAULT_DPM_API_VERSION`
    """

    def __init__(self, base_url, username, password, api_version=DEFAULT_SCH_API_VERSION):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.api_version = api_version
        self._base_admin_http_url = None  # This gets filled up in login and back to None in logout
        self.session = requests.Session()
        self.session.headers.update(REQUIRED_HEADERS)

    def login(self):
        """Login to ControlHub admin tool."""
        # Perform basic authentication
        binary_user_pass = '{}:{}'.format(self.username, self.password).encode()
        encoded_auth = base64.encodebytes(binary_user_pass).decode('ascii').strip()
        self.session.headers.update({'Authorization': 'Basic {}'.format(encoded_auth)})
        try:
            command = self.get_system_components()
            response_json = command.response.json()
            list_records = [record for record in response_json if record['attributes']]
            self._base_admin_http_url = list_records[0]['attributes']['baseAdminHttpUrl']
        except requests.exceptions.HTTPError as ex:
            if ex.response.status_code == 401:
                raise InvalidCredentialsError('Invalid credentials specified')
            raise

    def logout(self):
        """Logout from the admin tool."""
        del self.session.headers['Authorization']
        self._base_admin_http_url = None

    def get_system_components(self):
        """Get system components from admin tool.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        response = self._get(app=None, endpoint='v{}/system/components'.format(self.api_version))
        return Command(self, response)

    def get_system_logs(self, ending_offset=-1):
        """Get ControlHub logs.

        Args:
            ending_offset (:obj:`int`, optional): Ending offset for log. Default: ``-1``.

        Returns:
            An instance of :py:class:`streamsets.sdk.sch_api.Command`.
        """
        params = get_params(parameters=locals(), exclusions=('self',))
        params.update({'componentURL': self._base_admin_http_url})
        response = self._get(app=None, endpoint='v{}/system/log'.format(self.api_version), params=params)
        return Command(self, response)

    # Internal functions only below.
    def _delete(self, app, endpoint, rest='rest', params=None):
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.get(url, params=params or {})
        self._handle_http_error(response)
        return response

    def _get(self, app, endpoint, rest='rest', params=None, base_url=None):
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.get(url, params=params or {})
        self._handle_http_error(response)
        return response

    def _post(self, app, endpoint, rest='rest', params=None, data=None, files=None, headers=None, base_url=None):
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        if not data:
            data = None
        else:
            data = data if isinstance(data, str) else json.dumps(data)
        response = self.session.post(url, params=params or {}, data=data, files=files, headers=headers)
        self._handle_http_error(response)
        return response

    def _put(self, app, endpoint, rest='rest', params=None, data=None, base_url=None):
        url = join_url_parts(self.base_url, app, '/{}'.format(rest), endpoint)
        response = self.session.put(url, params=params or {}, data=json.dumps(data or {}))
        self._handle_http_error(response)
        return response

    def _handle_http_error(self, response):
        # Delegating to response object error handling as last resort.
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            logger.error(
                'Encountered an error while doing %s on %s. Response: %s, Error: %s',
                response.request.method,
                response.request.url,
                response.__dict__,
                http_error,
            )
            raise
