import json
import logging
import os
from enum import Enum
from typing import Any
from typing import AnyStr
from typing import Dict
from typing import IO
from typing import Optional
from typing import Tuple
from typing import Union

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]


SCOPES = [
    'https://www.googleapis.com/auth/bigquery.insertdata',
    'https://www.googleapis.com/auth/bigquery',
]

log = logging.getLogger(__name__)


def init_api_root(api_root: Optional[str]) -> Tuple[bool, str]:
    if api_root:
        return True, api_root

    host = os.environ.get('BIGQUERY_EMULATOR_HOST')
    if host:
        return True, f'http://{host}/bigquery/v2'

    return False, 'https://www.googleapis.com/bigquery/v2'


class SourceFormat(Enum):
    AVRO = 'AVRO'
    CSV = 'CSV'
    DATASTORE_BACKUP = 'DATASTORE_BACKUP'
    NEWLINE_DELIMITED_JSON = 'NEWLINE_DELIMITED_JSON'
    ORC = 'ORC'
    PARQUET = 'PARQUET'


class Disposition(Enum):
    WRITE_APPEND = 'WRITE_APPEND'
    WRITE_EMPTY = 'WRITE_EMPTY'
    WRITE_TRUNCATE = 'WRITE_TRUNCATE'


class SchemaUpdateOption(Enum):
    ALLOW_FIELD_ADDITION = 'ALLOW_FIELD_ADDITION'
    ALLOW_FIELD_RELAXATION = 'ALLOW_FIELD_RELAXATION'


class BigqueryBase:
    _project: Optional[str]
    _api_root: str
    _api_is_dev: bool

    def __init__(
            self, project: Optional[str] = None,
            service_file: Optional[Union[str, IO[AnyStr]]] = None,
            session: Optional[Session] = None, token: Optional[Token] = None,
            api_root: Optional[str] = None,
    ) -> None:
        self._api_is_dev, self._api_root = init_api_root(api_root)
        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

        self._project = project
        if self._api_is_dev and not project:
            self._project = (
                os.environ.get('BIGQUERY_PROJECT_ID')
                or os.environ.get('GOOGLE_CLOUD_PROJECT')
                or 'dev'
            )

    def project(self) -> str:
        if self._project:
            return self._project

        self._project = self.token.get_project()
        if self._project:
            return self._project

        raise Exception('could not determine project, please set it manually')

    def headers(self) -> Dict[str, str]:
        if self._api_is_dev:
            return {}

        token = self.token.get()
        return {
            'Authorization': f'Bearer {token}',
        }

    def _post_json(
            self, url: str, body: Dict[str, Any], session: Optional[Session],
            timeout: int, params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = json.dumps(body).encode('utf-8')

        headers = self.headers()
        headers.update({
            'Content-Length': str(len(payload)),
            'Content-Type': 'application/json',
        })

        s = SyncSession(session) if session else self.session
        resp = s.post(url, data=payload, headers=headers,
                            timeout=timeout, params=params or {})
        data: Dict[str, Any] = resp.json()
        return data

    def _get_url(
            self, url: str, session: Optional[Session], timeout: int,
            params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, timeout=timeout,
                           params=params or {})
        data: Dict[str, Any] = resp.json()
        return data

    def _delete(
        self, url: str, session: Optional[Session], timeout: int,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.delete(url, headers=headers, timeout=timeout,
                              params=params or {})
        data: Dict[str, Any] = resp.json()
        return data

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> 'BigqueryBase':
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
