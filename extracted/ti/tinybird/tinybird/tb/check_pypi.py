from typing import Optional

import requests

from tinybird.tb.modules.common import getenv_bool

PYPY_URL = "https://pypi.org/pypi/tinybird/json"


class CheckPypi:
    def get_latest_version(self) -> Optional[str]:
        try:
            disable_ssl: bool = getenv_bool("TB_DISABLE_SSL_CHECKS", False)
            response = requests.get(PYPY_URL, verify=not disable_ssl)
            if response.status_code != 200:
                return None
            return response.json()["info"]["version"]
        except Exception:
            return None
