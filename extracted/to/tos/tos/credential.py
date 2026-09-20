import logging
import os
import random
import threading
import time
import uuid
from datetime import datetime, timedelta

import requests
from deprecated import deprecated
from tos.consts import ECS_DATE_FORMAT

from tos.exceptions import TosClientError

logger = logging.getLogger(__name__)

DEFAULT_FETCH_TIME = 5 * 60
DEFAULT_OIDC_STS_ENDPOINT = 'https://sts.volcengineapi.com'
DEFAULT_OIDC_DURATION_SECONDS = 3600
DEFAULT_OIDC_TIMEOUT = 30
DEFAULT_OIDC_REFRESH_RETRY_INTERVAL_SECONDS = 10
DEFAULT_OIDC_REFRESH_RETRY_JITTER_SECONDS = 5
DEFAULT_OIDC_HARD_EXPIRY_WINDOW_SECONDS = 60

OIDC_ROLE_TRN_ENV = 'VOLCENGINE_OIDC_ROLE_TRN'
OIDC_TOKEN_FILE_ENV = 'VOLCENGINE_OIDC_TOKEN_FILE'
OIDC_ROLE_SESSION_NAME_ENV = 'VOLCENGINE_OIDC_ROLE_SESSION_NAME'
OIDC_ROLE_POLICY_ENV = 'VOLCENGINE_OIDC_ROLE_POLICY'
OIDC_STS_ENDPOINT_ENV = 'VOLCENGINE_OIDC_STS_ENDPOINT'


class Credentials():
    def __init__(self, access_key_id, access_key_secret, security_token=None):
        self.access_key_id = access_key_id.strip()
        self.access_key_secret = access_key_secret.strip()
        self.security_token = security_token

    def get_ak(self):
        return self.access_key_id

    def get_sk(self):
        return self.access_key_secret

    def get_security_token(self):
        return self.security_token

    @deprecated(version='2.6.6', reason="please use get_ak")
    def get_access_key_id(self):
        return self.get_ak()

    @deprecated(version='2.6.6', reason="please use get_sk")
    def get_access_key_secret(self):
        return self.get_sk()


class CredentialsProvider():
    def get_credentials(self):
        return


class StaticCredentials(CredentialsProvider):
    """
    This class is deprecated and should not be used anymore.
    """
    @deprecated(version='2.6.6', reason="please use StaticCredentialsProvider")
    def __init__(self, access_key_id, access_key_secret, security_token=None):
        self.credentials = Credentials(access_key_id, access_key_secret, security_token)

    @deprecated(version='2.6.6', reason="please use StaticCredentialsProvider")
    def get_credentials(self):
        return self.credentials


class FederationToken():
    def __init__(self, access_key_id, access_key_secret, security_token, expiration, pre_fetch_sec=DEFAULT_FETCH_TIME):
        self.credential = Credentials(access_key_id, access_key_secret, security_token)
        self.expiration = expiration
        self.pre_fetch_sec = pre_fetch_sec

    def get_credentials(self):
        return self.credential

    def will_soon_expire(self):
        now = int(time.time())
        return now + self.pre_fetch_sec - self.expiration > 0

    def expire(self):
        return int(time.time()) > self.expiration


class FederationCredentials(CredentialsProvider):
    def __init__(self, get_credentials_func):
        self.get_credentials_func = get_credentials_func
        self.federationToken = None
        self.refreshing = 0
        self.__lock = threading.Lock()

    def get_credentials(self):
        # 不存在或者已经过期直接获取token
        if self.federationToken is None or self.federationToken.expire():
            return self._try_get_credential()
        # 快要过期且没有其他正在获取token的任务时，尝试去获取token
        if self.federationToken.will_soon_expire() and self.refreshing == 0:
            return self._try_get_credential()
        return self.federationToken.get_credentials()

    def _try_get_credential(self):
        with self.__lock:
            try:
                self.refreshing = 1
                # 再判断一次，因为可能已经被更新过了
                if self.federationToken is None or self.federationToken.will_soon_expire():
                    self.federationToken = self.get_credentials_func()
            except Exception as e:
                logger.error("get_credentials error: {0}".format(e))
                if self.federationToken is None:
                    raise
            finally:
                self.refreshing = 0
        return self.federationToken.get_credentials()


class StaticCredentialsProvider(CredentialsProvider):
    def __init__(self, access_key_id, access_key_secret, security_token=None):
        self.credentials = Credentials(access_key_id, access_key_secret, security_token)

    def get_credentials(self):
        return self.credentials


class EnvCredentialsProvider(CredentialsProvider):
    def __init__(self):
        access_key = os.environ.get('TOS_ACCESS_KEY')
        secret_key = os.environ.get('TOS_SECRET_KEY')
        security_token = os.environ.get('TOS_SECURITY_TOKEN')

        if access_key is None or secret_key is None:
            raise TosClientError('ak or sk is empty')

        self.credentials = Credentials(access_key, secret_key, security_token)

    def get_credentials(self):
        return self.credentials


class EcsCredentialsProvider(CredentialsProvider):
    ecs_url = 'http://100.96.0.96/volcstack/latest/iam/security_credentials/{}'

    def __init__(self, role_name):
        if role_name == '':
            raise TosClientError('ecs role name is empty')
        self._lock = threading.Lock()
        self.expires = None
        self.credentials = None
        self._ecs_url = EcsCredentialsProvider.ecs_url.format(role_name)

    def get_credentials(self):
        res = self._try_get_credentials()
        if res is not None:
            return res
        with self._lock:
            try:
                res = self._try_get_credentials()
                if res is not None:
                    return res

                res = requests.get(self._ecs_url, timeout=30)
                res_body = res.json()
                self.credentials = Credentials(res_body.get('AccessKeyId'), res_body.get('SecretAccessKey'),
                                               res_body.get('SessionToken'))
                self.expires = datetime.strptime(res_body.get('ExpiredTime'), ECS_DATE_FORMAT)
                return self.credentials
            except Exception as e:
                if self.expires is not None and datetime.now().timestamp() < self.expires.timestamp():
                    return self.credentials
                raise TosClientError('get ecs token failed', e)

    def _try_get_credentials(self):
        if self.expires is None or self.credentials is None:
            return None
        if datetime.now().timestamp() > (self.expires - timedelta(minutes=10)).timestamp():
            return None
        return self.credentials


class OIDCCredentialsProvider(CredentialsProvider):
    """Get temporary credentials from STS by using a projected OIDC token.

    Explicit constructor arguments take precedence over the environment. When
    omitted, the provider reads the variables injected by VKE IRSA:

    * VOLCENGINE_OIDC_ROLE_TRN
    * VOLCENGINE_OIDC_TOKEN_FILE
    * VOLCENGINE_OIDC_ROLE_SESSION_NAME (optional)
    * VOLCENGINE_OIDC_ROLE_POLICY (optional)
    * VOLCENGINE_OIDC_STS_ENDPOINT (optional)

    The token file is read again on every refresh so Kubernetes token rotation
    is respected. Temporary credentials are cached in memory only. Failed
    refreshes are briefly backed off with jitter, and cached credentials are
    never returned during the hard expiry safety window. After fork, the child
    creates its own refresh lock and fetches credentials independently.
    """

    def __init__(self, role_trn=None, oidc_token_file=None, role_session_name=None,
                 duration_seconds=DEFAULT_OIDC_DURATION_SECONDS, policy=None,
                 sts_endpoint=None, timeout=DEFAULT_OIDC_TIMEOUT,
                 pre_fetch_sec=DEFAULT_FETCH_TIME):
        self.role_trn = self._argument_or_env(role_trn, OIDC_ROLE_TRN_ENV)
        self.oidc_token_file = self._argument_or_env(oidc_token_file, OIDC_TOKEN_FILE_ENV)
        self.role_session_name = self._argument_or_env(role_session_name, OIDC_ROLE_SESSION_NAME_ENV)
        self.policy = self._argument_or_env(policy, OIDC_ROLE_POLICY_ENV)
        self.sts_endpoint = self._argument_or_env(sts_endpoint, OIDC_STS_ENDPOINT_ENV)

        if not isinstance(self.role_trn, str) or not self.role_trn.strip():
            raise TosClientError('OIDC role TRN is empty; set role_trn or {0}'.format(OIDC_ROLE_TRN_ENV))
        if not isinstance(self.oidc_token_file, str) or not self.oidc_token_file.strip():
            raise TosClientError('OIDC token file is empty; set oidc_token_file or {0}'.format(OIDC_TOKEN_FILE_ENV))
        if (not isinstance(duration_seconds, int) or isinstance(duration_seconds, bool) or
                not 900 <= duration_seconds <= 43200):
            raise TosClientError('OIDC duration_seconds must be an integer in [900, 43200]')
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
            raise TosClientError('OIDC timeout must be greater than 0')
        if (not isinstance(pre_fetch_sec, (int, float)) or isinstance(pre_fetch_sec, bool) or
                pre_fetch_sec < 0):
            raise TosClientError('OIDC pre_fetch_sec must be greater than or equal to 0')
        if pre_fetch_sec >= duration_seconds:
            raise TosClientError('OIDC pre_fetch_sec must be less than duration_seconds')
        if self.role_session_name is not None and not isinstance(self.role_session_name, str):
            raise TosClientError('OIDC role_session_name must be a string')
        if self.policy is not None and not isinstance(self.policy, str):
            raise TosClientError('OIDC policy must be a string')

        self.role_trn = self.role_trn.strip()
        self.oidc_token_file = self.oidc_token_file.strip()
        self.role_session_name = (self.role_session_name or self._new_role_session_name()).strip()
        if not self.role_session_name:
            self.role_session_name = self._new_role_session_name()
        self.sts_endpoint = self._normalize_sts_endpoint(self.sts_endpoint)
        self.duration_seconds = duration_seconds
        self.timeout = timeout
        self.pre_fetch_sec = pre_fetch_sec

        self._lock = threading.Lock()
        self._pid = os.getpid()
        self._fork_locks = {self._pid: self._lock}
        self._expiration_timestamp = None
        self._next_refresh_timestamp = None
        self._last_refresh_error = None
        self.credentials = None

    @staticmethod
    def _argument_or_env(argument, env_name):
        if argument is not None:
            return argument
        return os.environ.get(env_name)

    @staticmethod
    def _new_role_session_name():
        return 'tos-python-sdk-' + uuid.uuid4().hex

    @staticmethod
    def _normalize_sts_endpoint(endpoint):
        endpoint = endpoint or DEFAULT_OIDC_STS_ENDPOINT
        if not isinstance(endpoint, str):
            raise TosClientError('OIDC STS endpoint must be a string')
        endpoint = endpoint.strip().rstrip('/')
        if '://' not in endpoint:
            endpoint = 'https://' + endpoint
        if not endpoint.startswith('https://'):
            raise TosClientError('OIDC STS endpoint must use https')
        return endpoint

    def get_credentials(self):
        self._ensure_fork_safe()
        credentials = self._try_get_credentials()
        if credentials is not None:
            return credentials

        with self._lock:
            credentials = self._try_get_credentials()
            if credentials is not None:
                return credentials
            self._raise_if_refresh_in_backoff()
            try:
                return self._refresh_credentials()
            except Exception as e:
                refresh_error = self._to_refresh_error(e)
                retry_delay = self._schedule_refresh_retry(refresh_error)
                if self._credentials_safely_valid():
                    logger.warning(
                        'failed to refresh OIDC credentials; reuse credentials outside the hard expiry window '
                        'and retry after %.1f seconds', retry_delay)
                    return self.credentials
                raise refresh_error

    def _ensure_fork_safe(self):
        current_pid = os.getpid()
        if self._pid == current_pid:
            return

        # Never acquire the inherited refresh lock: its owning thread may not
        # exist in the child. setdefault gives concurrent child callers one lock.
        lock = self._fork_locks.get(current_pid)
        if lock is None:
            lock = self._fork_locks.setdefault(current_pid, threading.Lock())
        with lock:
            if self._pid == current_pid:
                return
            # A fork can interrupt publication of credentials/expiry/backoff.
            # Discard that snapshot and refresh from the child's token file.
            self.credentials = None
            self._expiration_timestamp = None
            self._next_refresh_timestamp = None
            self._last_refresh_error = None
            self._lock = lock
            self._pid = current_pid

    def _try_get_credentials(self):
        if self.credentials is None or self._expiration_timestamp is None:
            return None
        now = time.time()
        refresh_window = max(self.pre_fetch_sec, DEFAULT_OIDC_HARD_EXPIRY_WINDOW_SECONDS)
        if now < self._expiration_timestamp - refresh_window:
            return self.credentials
        if (self._next_refresh_timestamp is not None and now < self._next_refresh_timestamp and
                self._credentials_safely_valid(now)):
            return self.credentials
        return None

    def _credentials_safely_valid(self, now=None):
        if now is None:
            now = time.time()
        return (self.credentials is not None and self._expiration_timestamp is not None and
                now < self._expiration_timestamp - DEFAULT_OIDC_HARD_EXPIRY_WINDOW_SECONDS)

    def _raise_if_refresh_in_backoff(self):
        if (self._next_refresh_timestamp is not None and time.time() < self._next_refresh_timestamp and
                self._last_refresh_error is not None):
            raise TosClientError(self._last_refresh_error.message, self._last_refresh_error.cause)

    def _schedule_refresh_retry(self, refresh_error):
        now = time.time()
        retry_delay = (DEFAULT_OIDC_REFRESH_RETRY_INTERVAL_SECONDS +
                       random.uniform(0, DEFAULT_OIDC_REFRESH_RETRY_JITTER_SECONDS))
        next_refresh_timestamp = now + retry_delay
        if self._credentials_safely_valid(now):
            hard_expiry_timestamp = self._expiration_timestamp - DEFAULT_OIDC_HARD_EXPIRY_WINDOW_SECONDS
            next_refresh_timestamp = min(next_refresh_timestamp, hard_expiry_timestamp)
        self._last_refresh_error = refresh_error
        self._next_refresh_timestamp = next_refresh_timestamp
        return max(0, next_refresh_timestamp - now)

    @staticmethod
    def _to_refresh_error(error):
        if isinstance(error, TosClientError):
            return error
        return TosClientError('get OIDC credentials failed', error)

    def _refresh_credentials(self):
        oidc_token = self._read_oidc_token()
        params = {
            'RoleTrn': self.role_trn,
            'OIDCToken': oidc_token,
            'RoleSessionName': self.role_session_name,
            'DurationSeconds': str(self.duration_seconds),
        }
        if self.policy:
            params['Policy'] = self.policy

        url = self.sts_endpoint + '/?Action=AssumeRoleWithOIDC&Version=2018-01-01'
        try:
            response = requests.post(url, data=params, timeout=self.timeout, allow_redirects=False)
        except requests.RequestException as e:
            raise TosClientError('failed to request STS AssumeRoleWithOIDC', e)

        if 300 <= response.status_code < 400:
            raise TosClientError(
                'STS AssumeRoleWithOIDC redirect HTTP {0} is not allowed'.format(response.status_code))

        try:
            response_body = response.json()
        except (TypeError, ValueError) as e:
            if response.status_code < 200 or response.status_code >= 300:
                raise TosClientError(
                    'STS AssumeRoleWithOIDC returned HTTP {0}'.format(response.status_code), e)
            raise TosClientError('invalid JSON response from STS AssumeRoleWithOIDC', e)
        if not isinstance(response_body, dict):
            raise TosClientError('invalid JSON response from STS AssumeRoleWithOIDC')

        response_metadata = response_body.get('ResponseMetadata') or {}
        if not isinstance(response_metadata, dict):
            raise TosClientError('invalid ResponseMetadata in STS AssumeRoleWithOIDC response')
        sts_error = response_metadata.get('Error') or {}
        if not isinstance(sts_error, dict):
            raise TosClientError('invalid Error in STS AssumeRoleWithOIDC response')
        request_id = response_metadata.get('RequestId')
        if response.status_code < 200 or response.status_code >= 300:
            raise TosClientError(self._format_sts_error(
                'STS AssumeRoleWithOIDC returned HTTP {0}'.format(response.status_code),
                sts_error, request_id))
        if sts_error:
            raise TosClientError(self._format_sts_error(
                'STS AssumeRoleWithOIDC returned an error', sts_error, request_id))

        result = response_body.get('Result') or {}
        if not isinstance(result, dict):
            raise TosClientError('invalid Result in STS AssumeRoleWithOIDC response')
        credential_data = result.get('Credentials') or {}
        if not isinstance(credential_data, dict):
            raise TosClientError('invalid Credentials in STS AssumeRoleWithOIDC response')
        access_key = credential_data.get('AccessKeyId')
        secret_key = credential_data.get('SecretAccessKey')
        security_token = credential_data.get('SessionToken')
        expiration = credential_data.get('Expiration') or credential_data.get('ExpiredTime')

        if not all(isinstance(value, str) and value.strip()
                   for value in (access_key, secret_key, security_token, expiration)):
            raise TosClientError('STS AssumeRoleWithOIDC response is missing credentials or expiration')

        expiration_timestamp = self._parse_expiration(expiration)
        if expiration_timestamp <= time.time() + DEFAULT_OIDC_HARD_EXPIRY_WINDOW_SECONDS:
            raise TosClientError('STS AssumeRoleWithOIDC returned credentials too close to expiration')

        credentials = Credentials(access_key.strip(), secret_key.strip(), security_token.strip())
        self.credentials = credentials
        self._expiration_timestamp = expiration_timestamp
        self._next_refresh_timestamp = None
        self._last_refresh_error = None
        return credentials

    def _read_oidc_token(self):
        try:
            with open(self.oidc_token_file, 'r', encoding='utf-8') as token_file:
                oidc_token = token_file.read().strip()
        except (IOError, OSError) as e:
            raise TosClientError('failed to read OIDC token file', e)
        if not oidc_token:
            raise TosClientError('OIDC token file is empty')
        return oidc_token

    @staticmethod
    def _parse_expiration(expiration):
        value = expiration.strip()
        if value.endswith('Z'):
            value = value[:-1] + '+0000'
        elif len(value) >= 6 and value[-3] == ':' and value[-6] in ('+', '-'):
            value = value[:-3] + value[-2:]

        for date_format in ('%Y-%m-%dT%H:%M:%S.%f%z', '%Y-%m-%dT%H:%M:%S%z'):
            try:
                return datetime.strptime(value, date_format).timestamp()
            except ValueError:
                pass
        raise TosClientError('invalid expiration in STS AssumeRoleWithOIDC response')

    @staticmethod
    def _format_sts_error(prefix, sts_error, request_id):
        details = []
        if sts_error.get('Code'):
            details.append('code={0}'.format(sts_error.get('Code')))
        if request_id:
            details.append('request_id={0}'.format(request_id))
        if details:
            return '{0}: {1}'.format(prefix, ', '.join(details))
        return prefix
