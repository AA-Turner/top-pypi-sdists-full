import requests

from justnimbus.exceptions import InvalidClientID, JustNimbusError
from justnimbus.model import JustNimbusModel


class JustNimbusClient:
    def __init__(self, client_id: str, zip_code: str):
        self._client_id = client_id
        self._zip_code = zip_code

    def get_data(self) -> JustNimbusModel:
        url = f"https://dashboard.justnimbus.com/user/view.php?system={self._client_id}&zip={self._zip_code}&output=json"
        response = requests.get(url=url)

        try:
            response.raise_for_status()
            return JustNimbusModel.from_dict(response.json()[0])
        except requests.HTTPError as error:
            if response.status_code == 404:
                raise InvalidClientID(client_id=self._client_id) from error
            raise JustNimbusError() from error
        except LookupError as error:
            raise JustNimbusError() from error
