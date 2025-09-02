from typing import Any, Union

from httpx import Client, Timeout
from pydantic import BaseModel, PrivateAttr

from ipfabric.models.matrix import Version, SupportMatrix


class FeatureMatrix(BaseModel):
    timeout: Any = Timeout(timeout=5.0)
    proxy: Any = None
    _client: Client = PrivateAttr(None)
    _versions: list[Version] = PrivateAttr(None)
    _matrix_version: Version = PrivateAttr(None)
    _matrix: Any = PrivateAttr(None)

    def model_post_init(self, __context: Any) -> None:
        self._client = Client(base_url="https://matrix.ipfabric.io/api/", timeout=self.timeout, proxy=self.proxy)
        self._versions = [Version(**_) for _ in self._client.get("version").json()]
        self._versions.sort(key=lambda p: [int(_) for _ in p.name.split(".")], reverse=True)
        self.create_matrix()

    @property
    def versions(self) -> list[Version]:
        """Descending Ordered List of Versions; Newest is index 0."""
        return self._versions

    @property
    def matrix_version(self) -> Version:
        return self._matrix_version

    @property
    def matrix(self) -> SupportMatrix:
        return self._matrix

    def create_matrix(self, version: Union[Version, str] = None) -> SupportMatrix:
        """Creates a matrix based on the version

        Args:
            version: Version object or string, defaults to latest

        Returns:
        """
        if isinstance(version, str):
            version = {_.name: _ for _ in self._versions}[version]
        elif version is None:
            version = self.versions[0]
        if version == self._matrix_version:
            return self._matrix
        vid = version.id
        categories = {_["id"]: _ for _ in self._client.get("task/category", params={"versionId": vid}).json()}
        tasks = {_["id"]: _ for _ in self._client.get("task", params={"versionId": vid}).json()}
        vendors = {_["id"]: _ for _ in self._client.get("vendor", params={"versionId": vid}).json()}
        families = {_["id"]: _ for _ in self._client.get("vendor/family", params={"versionId": vid}).json()}

        matrix = [
            dict(
                category=categories[tasks[status["taskId"]]["categoryId"]],
                task=tasks[status["taskId"]],
                vendor=vendors[status["vendorId"]],
                family=families[status["familyId"]],
                status=status,
            )
            for status in self._client.get("task/status", params={"versionId": vid}).json()
        ]
        matrix = SupportMatrix(matrix=matrix, version=version)

        self._matrix, self._matrix_version = matrix, version
        return self._matrix
