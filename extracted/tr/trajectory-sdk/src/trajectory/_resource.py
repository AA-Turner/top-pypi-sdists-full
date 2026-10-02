# File generated from our OpenAPI spec by Spotless. See CONTRIBUTING.md for details.

from trajectory._base_client import APIClient


class APIResource:
  def __init__(self, client: APIClient) -> None:
    self._client = client
    self._get = client.get
    self._post = client.post
    self._put = client.put
    self._patch = client.patch
    self._delete = client.delete
