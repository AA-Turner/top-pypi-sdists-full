# IBM Confidential
# PID 5900-BAF
# Copyright StreamSets Inc., an IBM Company 2024
"""conftest module for pytest's user creation functionality."""

import base64
import json
import logging
import string
import subprocess
import time
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import requests

from streamsets.sdk.sch_api import LANDING_URL_SUBSTRING_AFTER_SCH_URL
from streamsets.sdk.utils import get_decoded_jwt, get_random_string, wait_for_condition

# Max age of a cached OIDC token, used to spam Google less so that we're less likely to hit a ratelimit.
max_cache_age = 1

logger = logging.getLogger(__name__)
oidc_cache = dict()


class BaseIdP(ABC):
    """BaseIdP is an abstract class to be inherited by IdP-related classes."""

    @abstractmethod
    def login(self, username, password, **kwargs):
        """Method to log in to IdP.

        Args:
            username (:obj:`str`): Username to login, can be an email.
            password (:obj:`str`): Password for the user.
            **kwargs: Additional arguments that may be consumed.

        Returns:
            A :obj:`str` containing the OIDC token of the user once they are logged in.
        """
        pass

    @abstractmethod
    def get_oidc_token_from_response(self, response, **kwargs):
        """Take a response from the IdP and get the OIDC token from it.

        Args:
            response: Response from the IdP.
            **kwargs: Additional arguments that may be consumed.

        Returns:
            A :obj:`str` containing the OIDC token for a user.
        """
        pass

    @abstractmethod
    def get_error_message_from_response(self, response, **kwargs):
        """Take a response from the IdP and get the error message from it.

        Args:
            response: Response from the IdP.
            **kwargs: Additional arguments that may be consumed.

        Returns:
            A :obj:`str` containing the error message. Can be None.
        """
        pass

    @abstractmethod
    def get_token_exchange_path(self):
        """This gets the token exchange path in ASTER.
           Different OIDC types have their own token-exchange have their own endpoints.

        Returns:
            A :obj:`str` containing the path to the token-exchange endpoint.
        """
        pass


class Firebase(BaseIdP):
    GAUTH_URL = 'https://identitytoolkit.googleapis.com'
    # Max retries for hitting the quota ratelimit, based at 10 arbitrarily.
    MAX_QUOTA_RATE_LIMIT = 10
    USER_DOES_NOT_EXIST_ERROR_MESSAGE = [
        'EMAIL_NOT_FOUND',
        'Incorrect username or password.',
        'INVALID_LOGIN_CREDENTIALS',
    ]

    def login(self, username, password, firebase_api_key, **kwargs):
        """

        Args:
            username (:obj:`str`): Username of the person, can be an email.
            password (:obj:`str`): Password for the user.
            **kwargs: Additional arguments that may be consumed.

        Returns:
            A :obj:`str` containing the OIDC token for the user.
        """
        headers = {'content-type': 'application/json'}
        data = {'email': username, 'password': password, 'returnSecureToken': True}
        oidc_token_url = '{}/v1/accounts:signInWithPassword?key={}'.format(self.GAUTH_URL, firebase_api_key)

        # we keep track of attempts and stop after a certain number of attempts if we exceed the quota.
        attempts = 0
        while attempts < self.MAX_QUOTA_RATE_LIMIT:
            response = requests.post(oidc_token_url, data=json.dumps(data), headers=headers)

            error_message = self.get_error_message_from_response(response)
            if error_message is None:
                return self.get_oidc_token_from_response(response)
            elif 'Exceeded quota for verifying passwords' in error_message:
                logger.warning("Quota for verifying passwords exceeded, retrying in a bit")
                time.sleep(min(60, attempts**2))
            else:
                raise requests.exceptions.HTTPError(error_message)

            attempts += 1

        # only if we have reached max retries
        raise requests.exceptions.HTTPError(f"Reached max retries for verifying password for user {username}")

    def get_oidc_token_from_response(self, response, **kwargs):
        return response.json()['idToken']

    def get_error_message_from_response(self, response, **kwargs):
        if response.status_code != 200:
            # we definitely have an error in this case
            try:
                return response.json()['error']['message']
            except KeyError:
                # if we don't get a response in the expected fashion
                return str(response.json())

        return response.json().get('error', {}).get('message', None)

    def get_token_exchange_path(self):
        return "api/security/oauth/token-exchange"


class IdPManager:

    _idp_instance = None

    @classmethod
    def get_instance(cls):
        if cls._idp_instance is None:
            cls._idp_instance = Firebase()

        return cls._idp_instance

    @classmethod
    def login(cls, username, password, firebase_api_key, **kwargs):
        # Caching
        if username + password in oidc_cache:
            if oidc_cache[username + password][0] > datetime.utcnow() + timedelta(hours=max_cache_age):
                logger.debug('OIDC token fetched from cache for user %s', username)
                return oidc_cache[username + password][1]

        oidc_token = cls.get_instance().login(
            username=username, password=password, firebase_api_key=firebase_api_key, **kwargs
        )

        oidc_cache[username + password] = [datetime.utcnow(), oidc_token]
        return oidc_token

    @classmethod
    def get_oidc_token_from_response(cls, *args, **kwargs):
        return cls.get_instance().get_oidc_token_from_response(*args, **kwargs)

    @classmethod
    def get_error_message_from_response(cls, *args, **kwargs):
        return cls.get_instance().get_error_message_from_response(*args, **kwargs)

    @classmethod
    def get_token_exchange_path(cls):
        return cls.get_instance().get_token_exchange_path()

    @classmethod
    def exchange_token_with_aster(cls, aster_server_url, oidc_token, org_id=None, skip_email_verify_secret=None):
        token_exchange_endpoint = cls.get_token_exchange_path()
        token_server_url = f"{aster_server_url}/{token_exchange_endpoint}"

        headers = {'content-type': 'application/json', 'Authorization': 'Bearer {}'.format(oidc_token)}

        data = None
        if org_id or skip_email_verify_secret:
            data = {"data": {}, "version": 2}
            if org_id:
                data['data']["org"] = org_id
            if skip_email_verify_secret:
                data['data']['skipEmailVerifySecret'] = skip_email_verify_secret

        response = requests.post(token_server_url, data=json.dumps(data), headers=headers)
        response.raise_for_status()
        return response.json()['access_token']


def get_decoded_token(token):
    """Decode the given token.
    Generally used for ASTER and SCH auth. token.

    Args:
        token (:obj:`str`): token.

    Returns:
        Decoded token
    """
    token_payload = token.split('.')[1]
    padding = (4 - len(token_payload) % 4) % 4 * '='
    return json.loads(base64.b64decode(token_payload + padding))


def _fetch_aster_token(aster_api_client, oidc_token):
    organization_id = get_org_id_from_aster_client(aster_api_client)
    return IdPManager.exchange_token_with_aster(
        aster_server_url=aster_api_client._base_url, oidc_token=oidc_token, org_id=organization_id
    )


def fetch_aster_authentication_token_for_existing_user(aster_api_client, user_email, user_email_password):
    """
    Fetches ASTER token for an existing ASTER user.

    Args:
        aster_api_client (:py:obj:`streamsets.sdk.aster_api.ApiClient`): Aster API client object
        user_email (:obj:`str`): User email.
        user_email_password (:obj:`str`): Password for the user email.
    Returns:
        ASTER token
    """
    # Get OIDC token
    oidc_token = IdPManager.login(username=user_email, password=user_email_password)

    # Get ASTER token
    return _fetch_aster_token(aster_api_client, oidc_token)


def wait_for_user(sch, user_email, *, timeout_sec=60 * 3, interval_sec=10):
    """
    Low-level utility to wait for a user to be reported by the API.

    Args:
        sch (:py:obj:`streamsets.sdk.ControlHub`): ControlHub object.
        user_email (:obj:`str`): User email as expected by `streamsets.sdk.sch_models.Users::get()`.
        timeout_sec (:obj:`int`): Amount of time to wait, in seconds.
        interval_sec (:obj:`int`): How often to poll the API, in seconds.

    Returns:
        A :py:class:`streamsets.sdk.sch_models.User` instance.
    """
    poll_until = time.time() + timeout_sec

    while True:
        try:
            user = sch.users.get(email_address=user_email)

        except Exception as ex:
            # use a middle-tested loop to ensure that we only sleep if we will do some useful work afterwards
            if time.time() + interval_sec > poll_until:
                error_message = f'Unable to fetch user matching {user_email!r} after waiting {timeout_sec} seconds'
                logging.getLogger(__name__).exception(error_message)
                raise TimeoutError(error_message) from ex

            time.sleep(interval_sec)

        else:
            return user


def make_localhost_domain_docker_compatible(url, parser=None):
    """Resolves domain for a given url.
    Since testing runs within a docker container, we should redirect `localhost` to `host.docker.internal`.
    Every other domain does not need to be redirected.

    Args:
        url (:obj:`str`): The SCH location returned on the response redirect.
        parser (:py:class:argparse.ArgumentParser, optional): Argparse parser to write an exception to. Default: `None`

    Returns:
        The url accessible from a docker container.
    """
    try:
        updated_url = url.replace('localhost', 'host.docker.internal')
        return updated_url

    except Exception as e:
        if parser:
            parser.error(f"{url} raised the following error while parsing {e}")
        else:
            raise


def fetch_sch_url_and_api_credentials(aster_url, aster_token):
    """
    Fetches SCH API credentials for the user whose aster token is passed.

    Args:
        aster_url (:obj:`str`): Aster URL.
        aster_token (:obj:`str`): ASTER token for the user, for whom the SCH API credentials are needed.

    Returns:
        An instance of :obj:`tuple` containing sch_url, component_id, auth_token
    """
    logger.debug('aster_url = %s', aster_url)
    # Get SCH token
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': f'Authorization=Bearer%20{aster_token}'}

    sch_token_url = f'{aster_url}/api/security/v3/goto-control-hub'
    response = requests.post(sch_token_url, headers=headers, allow_redirects=False)

    if not response.content:
        raise Exception('Could not fetch SCH token to proceed')

    # response.cookies does not work against localhost. However, we can still extract the cookies from headers.
    sch_cookie = _get_sch_session_cookie_from_response(response)
    sch_url = make_localhost_domain_docker_compatible(response.headers['location'])
    sch_url = sch_url.replace(LANDING_URL_SUBSTRING_AFTER_SCH_URL, '')
    decoded_aster_token = get_decoded_token(aster_token)
    organization_id = decoded_aster_token['t_o']
    return fetch_tokens(organization_id, sch_url, sch_cookie, aster_token)


def fetch_tokens(organization_id, sch_url, sch_cookie, aster_token):
    """Fetch SCH component and authToken

    Args:
        organization_id (:obj:`str`): The org ID.
        sch_url (:obj:`str`): The SCH URL.
        sch_cookie (:obj:`str`): The SCH cookies.
        aster_token (:obj:`str`): The Aster token.

    Returns:
        The SCH session cookie.
    """
    # Make the login audit available.
    cookies = {'S4_SESSION': sch_cookie, 'S4_ASTER': aster_token}
    sch_landing_url = f'{sch_url}/security/public-rest/v1/aster/landing'
    requests.get(sch_landing_url, cookies=cookies, allow_redirects=False)

    data = {'label': 'pytest-generated-token', 'active': True, 'generateAuthToken': True}
    headers = {'Content-Type': 'application/json', 'Cookie': f'SS-SSO-SESSION={sch_cookie}', 'X-Requested-By': 'pytest'}
    response = requests.post(
        url=f'{sch_url}/security/rest/v1/organization/{organization_id}/api-user-credentials',
        headers=headers,
        data=json.dumps(data),
    )
    if not response.ok:
        try:
            content = response.json()
            content_tabbed = json.dumps(content, indent=2).replace('\n', '\n\t\t')
            raise Exception(
                f'Could not fetch sch component and authToken.\n\tStatus code: {response.status_code}'
                f'\n\tResponse dict: \n\t\t{content_tabbed}'
            )
        except Exception as e:
            raise e(
                f'Could not fetch sch component and authToken.\n\tStatus code: {response.status_code}'
                f'\n\tPlain response: {response.text}'
            )
    content = response.json()
    return content['componentId'], content['authToken']


def _get_sch_session_cookie_from_response(response):
    """Get the SCH session cookie returned on the redirect response.
    Args:
        response (:py:class:`requests.Response`): Response object from which we want to get session cookie
    Returns:
        The SCH session cookie.
    """
    # check the response's cookie jar for sch cookie
    sch_cookie = response.cookies.get_dict().get('S4_SESSION')
    if sch_cookie is not None:
        return sch_cookie

    # on localhost, cookies are not set but can be found in the response headers
    cookies_dict = {}
    cookies = response.headers['Set-Cookie']
    for cookie_str in cookies.split(";"):
        name, value = cookie_str.split('=', 1)
        cookies_dict[name.strip()] = value.strip()

    return cookies_dict['S4_SESSION']


def execute_install_script_for_docker(sch, deployment):
    install_script = sch.get_self_managed_deployment_install_script(deployment)

    # Replace docker commands with podman for environments using podman
    install_script = install_script.replace('docker', 'podman')

    logger.debug('Install script = %s', install_script)
    result = subprocess.run(
        install_script,
        executable='/bin/bash',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    # Log stderr output for debugging
    if result.stderr:
        stderr_output = result.stderr.decode('utf-8')
        logger.error('Container install script stderr: %s', stderr_output)
        print(f'Container install script stderr: {stderr_output}')

    # Add to the list of container IDs of engines that are added by this SCH instance;
    # this is used later to clean them up
    if not hasattr(sch, '_added_engines_container_ids'):
        sch._added_engines_container_ids = []
    # Since container id is 12 characters long, from the output get those many characters.
    sch._added_engines_container_ids.append(result.stdout.decode('utf-8')[:12])


def wait_for_registered_engines(sch, deployment_id, timeout_sec=100):
    def condition():
        deployment = sch.deployments.get(id=deployment_id)
        return len(deployment.registered_engines) == deployment.desired_instances

    def failure(timeout):
        raise TimeoutError('Timed out after {} seconds while waiting for desired no. of instances.'.format(timeout))

    wait_for_condition(condition=condition, failure=failure, time_between_checks=10, timeout=timeout_sec)


def fetch_aster_token_for_org(aster_server_url, oidc_token, org_id):
    """
    Fetches the aster token of a user for the specific org, useful for users that are a part of multiple orgs.

    Args:
        aster_server_url (:py:obj:`str`): URL for the aster server
        oidc_token (:py:obj:`str`): The user's OIDC token from login
        org_id (:py:obj:`str`): Org ID for which to get the Aster token for

    Returns:
        An :py:obj:`str` containing the Aster token for the user.

    """
    return IdPManager.exchange_token_with_aster(aster_server_url=aster_server_url, oidc_token=oidc_token, org_id=org_id)


def get_test_instance(aster_api_client):
    """
    Returns the first healthy and enabled instance chosen from all enabled zones.

    Args:
        aster_api_client (:py:class:`streamsets.sdk.aster_api.ApiClient`): The Aster api_client instance

    Returns:
        A :py:obj:`str` that describes the test instance

    """

    zones = get_response_data(aster_api_client.get_admin_zones())['content']
    enabled_zones = {zone['id'] for zone in zones if zone['enabled']}
    instances = get_response_data(aster_api_client.get_admin_instances())['content']
    return next(
        i
        for i in instances
        if i['zone'] in enabled_zones
        and i['enabled']
        and i['healthStatus'] == 'HEALTHY'
        and i['allocationPriority'] == 'PRIMARY'
    )


def create_organization(
    aster_api_client,
    org_name=None,
    org_admin_email=None,
    account_type='PLATFORM_FREE_TRIAL',
    instance=None,
    saml_only=False,
    sch_configurations=None,
):
    """
    Creates a new organization in a specific instance. This is only available for Sys-Admin.

    Args:
        aster_api_client (:py:class:`streamsets.sdk.aster_api.ApiClient`): The Aster api_client instance
        org_name (:py:obj:`str`, optional): The organization name, default: `None`
        org_admin_email (:py:obj:`str`, optional): The organization admin email, default: `None`
        account_type (:py:obj:`str`, optional): The organization account type, default: `None`
        instance (:py:obj:`dict`, optional): The instance to create an org in, default: `None`
        saml_only (:py:obj:`bool`, optional): If true, the created org will be SAML-only, default: `None`
        sch_configurations (:py:obj:`dict`, optional): SCH configurations set from Aster.

    Returns:
        An instance of :py:obj:`tuple` containing a :py:obj:`str` representing the email of the org admin and a
        :py:obj:`dict` containing the response data from creating an org.

    """

    if not org_name:
        org_name = "test-org-" + get_random_string(string.ascii_letters, 5)

    if not org_admin_email:
        org_admin_email = f'sdktestsdc+noverify-{org_name}@gmail.com'

    if not instance:
        instance = get_test_instance(aster_api_client)

    sch_configurations = sch_configurations or {}
    # ensure projects and service accounts features are enabled in an org
    sch_configurations.update(
        {
            'org.level.projects.feature.enabled.on.org': 'true',
            'dpm.enable.serviceAccounts': 'true',
        }
    )

    org = {
        'name': org_name,
        'instance': instance['id'],
        'email': org_admin_email,
        'accountType': account_type,
        'samlAuthOnly': saml_only,
        'schSettings': sch_configurations or {},  # passing None for schSettings causes a NPE on platform
    }

    logger.info(f'creating a new organization {org}')
    return org_admin_email, get_response_data(aster_api_client.create_admin_organization(org))


def get_org_id_from_aster_client(aster_api_client):
    """
    Get the user's org ID from an aster client.

    Args:
        aster_api_client (:py:class:`streamsets.sdk.aster_api.ApiClient`): Aster client from which org id is to be
                                                                           extracted.

    Returns:
        A :py:obj:`str` containing the org id of the user.
    """

    if aster_api_client._authentication_token:
        decoded_aster_token = get_decoded_jwt(aster_api_client._authentication_token)
        org_id = decoded_aster_token['t_o']
    else:
        decoded_cred_token = get_decoded_jwt(aster_api_client._sch_auth_token)
        org_id = decoded_cred_token['o']

    return org_id


def get_response_data(command):
    """Gets the value at 'data' for an object of type :py:class:`streamsets.sdk.aster_api.Command`.

    Args:
        command (:py:class:`streamsets.sdk.aster_api.Command`): Command object to get info from.

    Returns:
        The value at 'data' of the response.
    """
    command.response.raise_for_status()
    response_json = command.response.json()
    return response_json.get('data')


def fetch_aster_auth_token(aster_server_url, aster_email, aster_email_password, sch_token, firebase_api_key):
    """Get the Aster authentication token on behalf of the user provided."""

    oidc_token = IdPManager.login(
        username=aster_email, password=aster_email_password, firebase_api_key=firebase_api_key
    )
    decoded_token = get_decoded_jwt(sch_token) if sch_token else {}
    org_id = decoded_token.get('o')

    return IdPManager.exchange_token_with_aster(aster_server_url=aster_server_url, oidc_token=oidc_token, org_id=org_id)
