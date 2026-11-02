"""Write-only management of encrypted platform credentials."""

from collections.abc import Mapping

from labqoat._generated.secret import Secret
from labqoat._generated.secret_list import SecretList
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError


class SecretsClient(BaseClient):
    """Manage named bundles using explicit client credentials; reads return metadata only."""

    def list(self) -> SecretList:
        """List names, keys and timestamps in the client's selected environment."""
        path = "/api/v1/secrets"
        return self.decode(self.send("GET", path), path, SecretList.from_dict)

    def get(self, name: str) -> Secret:
        """Read bundle metadata without retrieving its values."""
        path = f"/api/v1/secrets/{self.encode_ref(name)}"
        return self.decode(self.send("GET", path), path, Secret.from_dict)

    def create(self, name: str, values: Mapping[str, str]) -> Secret:
        """Store a new bundle; obtain values from a local credential source rather than literals."""
        path = "/api/v1/secrets"
        response = self.send_json("POST", path, {"name": name, "values": dict(values)})
        return self.decode(response, path, Secret.from_dict)

    def update(self, name: str, values: Mapping[str, str]) -> Secret:
        """Replace a bundle for future container launches."""
        path = f"/api/v1/secrets/{self.encode_ref(name)}"
        response = self.send_json("PUT", path, {"values": dict(values)})
        return self.decode(response, path, Secret.from_dict)

    def delete(self, name: str) -> None:
        """Remove a stored bundle; running containers retain their existing environment."""
        path = f"/api/v1/secrets/{self.encode_ref(name)}"
        response = self.send("DELETE", path)
        if response.status_code != 204 or response.content:
            raise ApiError("Expected an empty deletion response.", status=response.status_code)
