from typing import List

import requests

from pipebio.shared_python.util_no_dependencies import UtilNoDependencies


class UsersService:
    url: str
    session: requests.sessions

    def __init__(self, url: str, session: requests.sessions):
        self._url = url
        self.url = f'{url}/api/v2/users'
        self.session = session

    def list(self) -> List[any]:
        response = self.session.get(self.url)

        UtilNoDependencies.raise_detailed_error(response)

        all = response.json()

        return all['data']

    def admin_list(self) -> List[any]:
        response = self.session.get(f'{self._url}/api/v2/admin/users')

        UtilNoDependencies.raise_detailed_error(response)

        all = response.json()

        return all['data']

    def get_benchling_details(self):
        response = self.session.get(f'{self.url}/_benchling/details')

        UtilNoDependencies.raise_detailed_error(response)

        return response.json()
