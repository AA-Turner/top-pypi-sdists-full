"""Main module."""
import json
import requests


class HandleClient:
    def __init__(
        self,
        hdl_user,
        hdl_pw,
        hdl_provider="http://pid.gwdg.de/handles/",
        hdl_prefix="21.11115",
        hdl_resolver="https://hdl.handle.net/",
    ):
        """initializes the class

        :param hdl_user: handle-username, e.g. 'user12.12345-06'
        :type hdl_user: str

        :param hdl_user: handle-password, e.g. 'verysecret'
        :type hdl_user: str

        :param hdl_provider: the base url of your handle-provider
        :type hdl_provider: str

        :param hdl_prefix: the prefix of you institution
        :type hdl_prefix: str

        :param hdl_resolver: An URL resolving your handle-id
        :type hdl_resolver: str

        :return: A HandleClient instance
        :rtype: `client.HandleClient`

        """

        self.user = hdl_user
        self.pw = hdl_pw
        self.provider = hdl_provider
        self.prefix = hdl_prefix
        if hdl_resolver.endswith("/"):
            self.resolver = hdl_resolver
        else:
            self.resolver = f"{hdl_resolver}/"
        if f"{self.provider}{hdl_prefix}".endswith("/"):
            self.url = f"{self.provider}{self.prefix}"
        else:
            self.url = f"{self.provider}{self.prefix}/"
        self.json_header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.auth = (self.user, self.pw)

    def strip_resolver(self, url_to_process):
        try:
            to_update = url_to_process.split(self.resolver)[1]
        except IndexError:
            to_update = url_to_process
        return to_update

    def update_handle(self, old_handle, new_url, verbose=True):
        """updates an existing HANDLE-PID and returns to API reponse object'

        :param old_handle: The Handle to update, can be full url or the handle only
        :type old_handle: str

        :param new_url: The new url the existing handle should point to
        :type new_url: str

        :return: The request response object, you should check if its `status_code` equals 204
        :rtype: `requests.models.Response`
        """
        to_update = f"{self.provider}{self.strip_resolver(old_handle)}"
        payload = json.dumps([{"type": "URL", "parsed_data": new_url}])
        if verbose:
            print(f"update {old_handle} via {to_update} to {new_url}")
        response = requests.request(
            "PUT", to_update, headers=self.json_header, data=payload, auth=self.auth
        )
        return response

    def register_handle(self, parsed_data, full_url=True):
        """registers an handle-id for the passed in URL aka 'parsed_data'

        :param parsed_data: An URL to register a HANDLE-ID for
        :type parsed_data: str

        :return: The created HANDLE-ID
        :rtype: str
        """
        payload = json.dumps([{"type": "URL", "parsed_data": parsed_data}])
        response = requests.request(
            "POST", self.url, headers=self.json_header, data=payload, auth=self.auth
        )
        handle = response.json()["epic-pid"]
        if full_url:
            return f"{self.resolver}{handle}"
        else:
            return handle
