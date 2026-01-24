"""
"""

import httpx

from .._vendor.sseclient import SSEClient

from .types import ApiGetStatusRequest
from .types import ApiGetStatusResponse
from .types import ApiFetchContentsRequest
from .types import ApiFetchContentsResponse
from .types import ApiCreateReloadRequest
from .types import ApiCreateReloadResponse
from .types import ApiGetReloadEventSourceData
from .types import ApiGetReloadRequest


class ReloadClient:
    def __init__(self, http_client: httpx.Client):
        self.client = http_client

    def get_status(self, revision: str): # pragma: no cover
        req = ApiGetStatusRequest(revision=revision)
        res = self.client.post('/get-status', json=req.model_dump())
        assert res.status_code == 200, res.status_code
        return ApiGetStatusResponse.model_validate(res.json())

    def fetch_contents(self, filepath: str):
        req = ApiFetchContentsRequest(filepath=filepath)
        res = self.client.post('/fetch-contents', json=req.model_dump())
        assert res.status_code == 200, res.status_code
        return ApiFetchContentsResponse.model_validate(res.json())

    def create_reload(self, filepath: str, contents: str):
        req = ApiCreateReloadRequest(filepath=filepath, contents=contents)
        res = self.client.post('/create-reload', json=req.model_dump())
        assert res.status_code == 200, res.status_code
        return ApiCreateReloadResponse.model_validate(res.json())

    def get_reload(self, reload_id: str):
        req = ApiGetReloadRequest(reloadId=reload_id)
        with self.client.stream('POST', '/get-reload', json=req.model_dump()) as res:
            assert res.status_code == 200, res.status_code
            for event in SSEClient(res.iter_bytes()).events():
                if event.event == 'message':
                    yield ApiGetReloadEventSourceData.model_validate_json(event.data)
