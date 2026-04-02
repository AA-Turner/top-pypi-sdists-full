import requests

from nsj_multi_database_lib.settings import MULTIDATABASE_API_URL

class DatabaseValidationException(Exception):
    pass

class DatabaseUnknowException(Exception):
    pass

class DatabaseService():

    def get_by_tenant(self, tenant, token, token_type, service_account=None):

        headers = {token_type: token}
        params = {"tenant": tenant}

        if service_account is not None:
            params["service_account"] = service_account

        response = requests.get(
            MULTIDATABASE_API_URL,
            params=params,
            headers=headers,
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code >= 400 and response.status_code <= 499:
            data = response.json()
            raise DatabaseValidationException(response.status_code, data["detail"] if "detail" in data else response.text)
        else:
            data = response.json()
            raise DatabaseUnknowException(data["detail"] if "detail" in data else response.text)
