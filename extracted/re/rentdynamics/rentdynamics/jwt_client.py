import base64
import hashlib
import json
import logging
from datetime import datetime, timedelta, timezone

import requests


logger = logging.getLogger(__name__)


def aware_utcnow():
    return datetime.now(tz=timezone.utc)


def datetime_from_epoch(timestamp):
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def decode_jwt_payload(token):
    _, payload_segment, _ = token.split('.')
    padded_payload = payload_segment + '=' * (-len(payload_segment) % 4)
    payload = json.loads(base64.urlsafe_b64decode(padded_payload).decode('utf-8'))
    if not isinstance(payload, dict):
        raise ValueError('JWT payload must be a JSON object')
    return payload


class JWTClient:

    EXPIRED_MESSAGE = 'Token is invalid or expired'
    DRIFT_COMPENSATION = 30
    REQUEST_TIMEOUT = 30

    username = None
    password = None
    development = False
    base_url = None
    base_development_url = None
    _access_token = None
    _access_token_payload = None
    _refresh_token = None

    def __init__(self, username, password, development=False, base_url=None,
                 base_development_url=None):
        cls = type(self)
        previous_auth = (cls.username, cls.password, cls.get_base_url())
        cls.username = username
        cls.password = password
        cls.development = development
        cls.base_url = base_url.rstrip('/') if base_url else None
        cls.base_development_url = (
            base_development_url.rstrip('/') if base_development_url else None
        )
        if previous_auth != (cls.username, cls.password, cls.get_base_url()):
            cls.reset()

    @classmethod
    def get_base_url(cls):
        if cls.development:
            return cls.base_development_url or 'https://api.rentdynamics.dev'
        return cls.base_url or 'https://api.rentdynamics.com'

    @classmethod
    def get(cls, url, headers=None):
        return cls._request(requests.get, url, headers=headers)

    @classmethod
    def post(cls, url, body, headers=None):
        return cls._request(requests.post, url, headers=headers, json=body)

    @classmethod
    def put(cls, url, body, headers=None):
        return cls._request(requests.put, url, headers=headers, json=body)

    @classmethod
    def _request(cls, request, url, headers=None, retried=False, **kwargs):
        request_headers = dict(headers or {})
        request_headers['Authorization'] = cls._get_authorization()
        response = request(
            url=url,
            headers=request_headers,
            timeout=cls.REQUEST_TIMEOUT,
            **kwargs,
        )

        if cls._is_token_expired_error(response) and not retried:
            cls._access_token = None
            cls._access_token_payload = None
            return cls._request(
                request,
                url,
                headers=headers,
                retried=True,
                **kwargs,
            )

        return response

    @classmethod
    def _get_authorization(cls):
        if cls._access_token is None or cls._token_is_expiring():
            if cls._refresh_token is None:
                cls._obtain_tokens()
            else:
                cls._refresh_or_obtain_tokens()

        return 'Bearer {}'.format(cls._access_token)

    @classmethod
    def _refresh_or_obtain_tokens(cls):
        try:
            cls._refresh_tokens()
        except Exception:
            logger.warning(
                'JWT refresh failed; performing login for a new token pair.',
                exc_info=True
            )
            cls.reset()
            cls._obtain_tokens()

    @classmethod
    def _obtain_tokens(cls):
        password_digest = hashlib.sha1(
            cls.password.encode('utf-8'),
        ).hexdigest()
        response = requests.post(
            url='{}/auth/login'.format(cls.get_base_url()),
            json={
                'username': cls.username,
                'password': password_digest,
            },
            timeout=cls.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        cls._cache_tokens(response.json())

    @classmethod
    def _refresh_tokens(cls):
        response = requests.post(
            url='{}/auth/token/refresh'.format(cls.get_base_url()),
            json={'refresh': cls._refresh_token},
            timeout=cls.REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        cls._cache_tokens(response.json())

    @classmethod
    def _cache_tokens(cls, token_response):
        access_token = token_response['access']
        access_token_payload = decode_jwt_payload(access_token)
        refresh_token = token_response['refresh']
        cls._access_token = access_token
        cls._access_token_payload = access_token_payload
        cls._refresh_token = refresh_token

    @classmethod
    def _token_is_expiring(cls):
        expiration_time = datetime_from_epoch(
            float(cls._access_token_payload['exp']),
        )
        drift_compensation = timedelta(seconds=cls.DRIFT_COMPENSATION)
        return expiration_time - drift_compensation <= aware_utcnow()

    @classmethod
    def _is_token_expired_error(cls, response):
        if response.status_code != requests.codes.forbidden:
            return False
        try:
            return json.loads(response.text)['errorMessage'] == cls.EXPIRED_MESSAGE
        except (json.JSONDecodeError, KeyError, TypeError):
            return False

    @classmethod
    def reset(cls):
        cls._access_token = None
        cls._access_token_payload = None
        cls._refresh_token = None
