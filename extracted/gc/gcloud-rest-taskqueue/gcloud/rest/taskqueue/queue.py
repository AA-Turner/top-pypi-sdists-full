"""
An asynchronous push queue for Google Appengine Task Queues
"""
import json
import logging
import os
from typing import Any
from typing import AnyStr
from typing import IO

from gcloud.rest.auth import SyncSession  # pylint: disable=no-name-in-module
from gcloud.rest.auth import BUILD_GCLOUD_REST  # pylint: disable=no-name-in-module
from gcloud.rest.auth import Token  # pylint: disable=no-name-in-module

# Selectively load libraries based on the package
if BUILD_GCLOUD_REST:
    from requests import Session
else:
    from aiohttp import ClientSession as Session  # type: ignore[assignment]

SCOPES = [
    'https://www.googleapis.com/auth/cloud-tasks',
]

log = logging.getLogger(__name__)


def init_api_root(
        api_root: str | None, api_is_dev: bool | None = None,
) -> tuple[bool, str]:
    if api_root:
        return api_is_dev is None or api_is_dev, api_root

    host = os.environ.get('CLOUDTASKS_EMULATOR_HOST')
    if host:
        return True, f'http://{host}/v2beta3'

    return False, 'https://cloudtasks.googleapis.com/v2beta3'


class PushQueue:
    _api_root: str
    _api_is_dev: bool
    _queue_path: str

    def __init__(
            self,
            project: str,
            taskqueue: str,
            location: str = 'us-central1',
            service_file: str | IO[AnyStr] | None = None,
            session: Session | None = None,
            token: Token | None = None,
            api_root: str | None = None,
            api_is_dev: bool | None = None
    ) -> None:
        self._api_is_dev, self._api_root = init_api_root(api_root, api_is_dev)
        self._queue_path = (
            f'projects/{project}/locations/{location}/queues/{taskqueue}'
        )

        self.session = SyncSession(session)
        self.token = token or Token(
            service_file=service_file, scopes=SCOPES,
            session=self.session.session,  # type: ignore[arg-type]
        )

    def headers(self) -> dict[str, str]:
        if self._api_is_dev:
            return {'Content-Type': 'application/json'}

        token = self.token.get()
        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        }

    def task_name(self, task_id: str) -> str:
        return f'{self._queue_path}/tasks/{task_id}'

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/create
    def create(
        self, task: dict[str, Any],
        session: Session | None = None,
        timeout: int = 10,
    ) -> Any:
        url = f'{self._api_root}/{self._queue_path}/tasks'
        payload = json.dumps({
            'task': task,
            'responseView': 'FULL',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload,
                            timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/delete
    def delete(
        self, tname: str,
        session: Session | None = None,
        timeout: int = 10,
    ) -> Any:
        url = f'{self._api_root}/{tname}'

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.delete(url, headers=headers, timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/get
    def get(
        self, tname: str, full: bool = False,
        session: Session | None = None,
        timeout: int = 10,
    ) -> Any:
        url = f'{self._api_root}/{tname}'
        params = {
            'responseView': 'FULL' if full else 'BASIC',
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params,
                           timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/list
    def list(  # noqa: A003
        self, full: bool = False, page_size: int = 1000,
        page_token: str = '',
        session: Session | None = None,
        timeout: int = 10,
    ) -> Any:
        url = f'{self._api_root}/{self._queue_path}/tasks'
        params: dict[str, int | str] = {
            'responseView': 'FULL' if full else 'BASIC',
            'pageSize': page_size,
            'pageToken': page_token,
        }

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.get(url, headers=headers, params=params,
                           timeout=timeout)
        return resp.json()

    # https://cloud.google.com/tasks/docs/reference/rest/v2beta3/projects.locations.queues.tasks/run
    def run(
        self, tname: str, full: bool = False,
        session: Session | None = None,
        timeout: int = 10,
    ) -> Any:
        url = f'{self._api_root}/{tname}:run'
        payload = json.dumps({
            'responseView': 'FULL' if full else 'BASIC',
        }).encode('utf-8')

        headers = self.headers()

        s = SyncSession(session) if session else self.session
        resp = s.post(url, headers=headers, data=payload,
                            timeout=timeout)
        return resp.json()

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> 'PushQueue':
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
