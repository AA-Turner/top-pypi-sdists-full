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
from urllib.error import HTTPError
from urllib.parse import urljoin, urlencode, urlparse, urlunparse

from requests import request

from mailmanclient.constants import __version__

__metaclass__ = type
__all__ = [
    'MailmanConnectionError',
    'Connection'
]


class MailmanConnectionError(Exception):
    """Custom Exception to catch connection errors."""


class Connection:
    """A connection to the REST client."""

    def __init__(self, baseurl, name=None, password=None, request_hooks=None):
        """Initialize a connection to the REST API.

        :param baseurl: The base url to access the Mailman 3 REST API.
        :param name: The Basic Auth user name.  If given, the `password` must
            also be given.
        :param password: The Basic Auth password.  If given the `name` must
            also be given.
        :param request_hooks: A list of callables that can receive the request
            parameters and return them with some changes or unchanged.
        """
        if baseurl[-1] != '/':
            baseurl += '/'
        self.baseurl = baseurl
        self.name = name
        self.password = password
        if name is not None and password is None:
            raise TypeError('`password` is required when `name` is given')
        if name is None and password is not None:
            raise TypeError('`name` is required when `password` is given')
        if name is None:
            self.auth = None
        else:
            self.auth = (name, password)
        self.request_hooks = request_hooks

    def add_hooks(self, request_hooks):
        """Add a list of hooks to an existing connection object.

        :param request_hooks: A list of Request hook which receive the request
            parameters.
        :type request_hooks: List[callables]
        """
        if self.request_hooks is None:
            self.request_hooks = request_hooks
        else:
            self.request_hooks.extend(request_hooks)

    def rewrite_url(self, url):
        """rewrite url component with self.baseurl prefix "scheme://netloc"

        :param url: the URL to rewrite
        :type url: str
        :return: modified URL
        :rtype: str
        """
        # rewrite url component with self.baseurl prefix "scheme://netloc"
        pbaseurl = urlparse(self.baseurl)
        parsed = urlparse(url)
        parsed = parsed._replace(scheme=pbaseurl.scheme,
                                 netloc=pbaseurl.netloc)
        return urlunparse(parsed)

    def _process_request_hooks(self, params):
        """Given the request parameters, pass them through the list of hooks.

        Hooks are simple callables that are provided with request parameters
        and return the same parameters, possibly with some modification or not.

        :param params: The HTTP request parameters.
        :returns: The HTTP request parameters.
        """
        for hook in self.request_hooks:
            try:
                params = hook(params)
            except Exception:
                print('[DEBUG] Failed to run hook {hook}')
        return params

    def _prepare_request(self, path, data, method):
        headers = {
            'User-Agent': 'GNU Mailman REST client v{0}'.format(__version__),
            }
        data_str = None
        if data is not None:
            data_str = urlencode(data, doseq=True, encoding='utf-8')
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if method is None:
            if data_str is None:
                method = 'GET'
            else:
                method = 'POST'
        method = method.upper()
        url = urljoin(self.baseurl, path)
        url = self.rewrite_url(url)
        return dict(url=url, method=method, data=data_str,
                    headers=headers)

    def call(self, path, data=None, method=None):
        """Make a call to the Mailman REST API.

        :param path: The url path to the resource.
        :type path: str
        :param data: Data to send, implies POST (default) or PUT.
        :type data: dict
        :param method: The HTTP method to call.  Defaults to GET when `data`
            is None or POST if `data` is given.
        :type method: str
        :return: The response content, which will be None, a dictionary, or a
            list depending on the actual JSON type returned.
        :rtype: None, list, dict
        :raises HTTPError: when a non-2xx status code is returned.
        """
        params = self._prepare_request(path, data, method)
        if self.request_hooks:
            params = self._process_request_hooks(params)

        try:
            response = request(**params, auth=self.auth)
            # content = response.content
            # If we did not get a 2xx status code, make this look like a
            # urllib2 exception, for backward compatibility.
            if response.status_code // 100 != 2:
                try:
                    err = response.json()
                    # If this fails, a ValueError is raised. It means either
                    # the response is malformed JSON or None.
                    error_msg = err['description']
                    # This can fail if the error message does not container
                    # description field.
                except (KeyError, ValueError):
                    error_msg = response.text

                raise HTTPError(params.get('url'), response.status_code,
                                error_msg, response, None)
            if len(response.content) == 0:
                return response, None
            return response, response.json()
        except HTTPError:
            raise
        except IOError as e:
            raise MailmanConnectionError(
                'Could not connect to Mailman API: ', repr(e))
