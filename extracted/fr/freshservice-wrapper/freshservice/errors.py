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

"""Defines errors thrown by lib-freshservice."""
import logging


class FreshserviceError(Exception):
    """An error occurred in the Freshservice module."""


class BadInput(FreshserviceError):
    """The user passed something, that doesn't match the model."""


class AuthenticationFailed(FreshserviceError):
    """Invalid or missing API key."""


class UnexpectedValue(FreshserviceError):
    """The API passed a value, that this wrapper doesn't understand."""


class UserSearchFailed(FreshserviceError):
    """Couldn't find user with given email"""


class AgentSearchFailed(FreshserviceError):
    """Couldn't find agent with given email"""


class ResponseError(FreshserviceError):

    """Response is not JSON or contains errors."""

    def __init__(self, request, response):
        """Log error and raise parent error

        Args:
            request: The request object.
            response: The response string in JSON format. Pass None or '' in
                case the response was not in JSON.
        """
        super().__init__()
        self.request = request
        self.response = response

        logging.error('-----------Request-----------\n' + str(request.body))
        if response:
            logging.error('-----------Response-----------\n' + str(response))
        else:
            logging.error('The Freshservice response is not in JSON format')

    def __str__(self):
        return self.request.method + ' ' + self.request.url
