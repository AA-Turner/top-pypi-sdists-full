
from typing import Any, Dict, Optional
from code_loader.experiment_api.cli_config_utils import get_auth_config
from code_loader.experiment_api.utils import join_url, to_dict_no_none
import requests


class Client:
    def __init__(self, url: Optional[str] = None, token: Optional[str] = None):
        if url is None or token is None:
            configAuth = get_auth_config()
            if configAuth is None:
                raise Exception("No auth config found, either provide url and token or use `leap auth [url] [token]` to setup a config file")
            url = configAuth.api_url
            token = configAuth.api_key
        
        self.url = url
        self.token = token

    def __add_auth(self, headers: Dict[str, str]) -> Dict[str, str]:
        headers['Authorization'] = f'Bearer {self.token}'
        return headers
    
    def post(self, post_path: str, data: Any, headers: Dict[str, str] = {})-> requests.Response:
        headers = self.__add_auth(headers)
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json'
        url = join_url(self.url, post_path)
        json_data = to_dict_no_none(data)
        return requests.post(url, json=json_data, headers=headers)
    
    def check_response(self, response: requests.Response)-> None:
        if response.status_code >= 400:
            raise Exception(f"Error: {response.status_code} {response.text}")
