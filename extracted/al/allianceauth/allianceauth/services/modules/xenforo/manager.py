import json
import logging
from typing import Any

import requests

from django.conf import settings
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


class XenForoManager:
    def __init__(self) -> None:
        if not settings.XENFORO_ENDPOINT:
            logger.debug("Could not find XenForo endpoint")
        if not settings.XENFORO_APIKEY:
            logger.debug("XenForo API Key not found")
        pass

    @staticmethod
    def __sanitize_username(username: str) -> str:
        sanitized = username.replace(" ", "_")
        return sanitized

    @staticmethod
    def exec_http_request(http_params: dict[str, Any]) -> requests.Response:
        default_params = {
            'hash': settings.XENFORO_APIKEY
        }
        http_params.update(default_params)
        r = requests.get(settings.XENFORO_ENDPOINT, params=http_params)
        return r

    @staticmethod
    def add_user(username: str, email: str) -> dict[str, Any]:

        sanitized = XenForoManager.__sanitize_username(username)
        password = get_random_string(length=20)

        data = {
            'action': 'register',
            'username': sanitized,
            'password': password,
            'email': email,
            'group': settings.XENFORO_DEFAULT_GROUP,
            'visible': '1',
            'user_state': 'valid'
        }

        r = XenForoManager.exec_http_request(data)

        # check if the user already exist but was disabled
        if r.status_code != 200:
            if json.loads(r.text)['error'] == 7:
                data = XenForoManager.reactivate_user(sanitized)
                return data

        response = {
            'response': {
                'message': r.text,
                'status_code': r.status_code
            }
        }
        data.update(response)
        return data

    @staticmethod
    def reset_password(username: str) -> dict[str, Any]:
        password = get_random_string(length=20)

        data = {
            'action': 'editUser',
            'user': username,
            'password': password
        }

        r = XenForoManager.exec_http_request(data)

        response = {
            'response': {
                'message': r.text,
                'status_code': r.status_code
            }
        }
        data.update(response)
        return data

    @staticmethod
    def disable_user(username: str) -> requests.Response:
        data = {
            'action': 'editUser',
            'user': username,
            'remove_groups': settings.XENFORO_DEFAULT_GROUP
        }
        r = XenForoManager.exec_http_request(data)
        return r

    @staticmethod
    def reactivate_user(username: str) -> dict[str, Any]:
        data = {
            'action': 'editUser',
            'user': username,
            'add_groups': settings.XENFORO_DEFAULT_GROUP,
            'password': get_random_string(length=20)
        }
        r = XenForoManager.exec_http_request(data)
        response = {
            'response': {
                'message': r.text,
                'status_code': r.status_code
            },
            'username': username
        }
        data.update(response)
        return data

    @staticmethod
    def update_user_password(username: str, raw_password: str) -> dict[str, Any]:
        data = {
            'action': 'editUser',
            'user': username,
            'password': raw_password
        }
        r = XenForoManager.exec_http_request(data)
        response = {
            'response': {
                'message': r.text,
                'status_code': r.status_code
            },
            'username': username
        }
        data.update(response)
        return data
