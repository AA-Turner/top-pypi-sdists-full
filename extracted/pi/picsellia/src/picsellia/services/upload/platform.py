from urllib.parse import urljoin
from uuid import UUID

import requests
from orjson import orjson
from requests import Session

from picsellia.decorators import retry


class PlatformAdapter:
    def __init__(self, connector_id: UUID, session: Session, host: str, headers: dict):
        self.connector_id = connector_id
        self.host = host
        self.session = session
        self.headers = headers

    @retry(requests.ConnectionError)
    def generate_presigned_url(
        self, object_name: str, content_type: str
    ) -> requests.Response:
        payload = {"object_name": object_name, "content_type": content_type}
        path = f"/api/object-storage/{self.connector_id}/generate_presigned_url"
        url = urljoin(self.host, path)
        response = self.session.post(
            url=url, data=orjson.dumps(payload), headers=self.headers
        )
        response.raise_for_status()
        return response

    @retry(requests.ConnectionError)
    def init_multipart_upload(
        self, object_name: str, content_type: str
    ) -> requests.Response:
        payload = {"object_name": object_name, "content_type": content_type}
        path = f"/api/object-storage/{self.connector_id}/init_multipart_upload"
        url = urljoin(self.host, path)
        response = self.session.post(
            url=url, data=orjson.dumps(payload), headers=self.headers
        )
        response.raise_for_status()
        return response

    @retry(requests.ConnectionError)
    def generate_part_presigned_url(
        self, object_name: str, additional_payload: dict
    ) -> requests.Response:
        payload = {"object_name": object_name, **additional_payload}
        path = f"/api/object-storage/{self.connector_id}/generate_part_presigned_url"
        url = urljoin(self.host, path)
        response = self.session.post(
            url=url, data=orjson.dumps(payload), headers=self.headers
        )
        response.raise_for_status()
        return response

    @retry(requests.ConnectionError)
    def complete_part_upload(
        self, object_name: str, additional_payload: dict
    ) -> requests.Response:
        payload = {"object_name": object_name, **additional_payload}
        path = f"/api/object-storage/{self.connector_id}/complete_part_upload"
        url = urljoin(self.host, path)
        response = self.session.post(
            url=url, data=orjson.dumps(payload), headers=self.headers
        )
        response.raise_for_status()
        return response
