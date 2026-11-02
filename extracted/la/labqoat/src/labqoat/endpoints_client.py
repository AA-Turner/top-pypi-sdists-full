"""Deploy web server functions as endpoints the world calls, and manage the tokens that call them."""

from labqoat._generated.endpoint import Endpoint
from labqoat._generated.endpoint_list import EndpointList
from labqoat._generated.endpoint_token import EndpointToken
from labqoat._generated.endpoint_token_list import EndpointTokenList
from labqoat.assets_client import AssetsClient
from labqoat.base_client import BaseClient
from labqoat.compute.function import Function
from labqoat.compute.publication import Publication
from labqoat.compute.run_options import RunOptions
from labqoat.compute.submission import Submission
from labqoat.compute.web_servers import WebServer
from labqoat.errors.api_error import ApiError


class EndpointsClient(BaseClient):
    """Endpoints of the client's selected project, called at ``/e/<project>/<name>/`` on the platform's host."""

    def deploy(self, function: Function[..., object]) -> Endpoint:
        """Publish a ``@web_server`` function's source and image and serve it under its name.

        Deploying a changed function replaces the endpoint's replicas with ones of the new revision; deploying
        only changed scaling or access keeps them.
        """
        server = WebServer.of(function.local)
        publication = Publication(AssetsClient(self._transport)).capture(function)
        request = Submission.compose(function, {}, publication, RunOptions())
        path = f"/api/v1/endpoints/{self.encode_ref(server.name)}"
        response = self.send_json("PUT", path, {"request": request.to_dict(), **server.settings()})
        return self.decode(response, path, Endpoint.from_dict)

    def list(self) -> EndpointList:
        """List the project's endpoints with their scaling and replicas."""
        path = "/api/v1/endpoints"
        return self.decode(self.send("GET", path), path, EndpointList.from_dict)

    def get(self, name: str) -> Endpoint:
        """Read one endpoint with its scaling and replicas."""
        path = f"/api/v1/endpoints/{self.encode_ref(name)}"
        return self.decode(self.send("GET", path), path, Endpoint.from_dict)

    def delete(self, name: str) -> None:
        """Stop an endpoint: its replicas are cancelled and its URL answers 404."""
        self._deleted(f"/api/v1/endpoints/{self.encode_ref(name)}")

    def create_token(self, name: str) -> EndpointToken:
        """Create a named bearer token for the project's endpoints; its secret is in this response only."""
        path = "/api/v1/endpoint-tokens"
        return self.decode(self.send_json("POST", path, {"name": name}), path, EndpointToken.from_dict)

    def list_tokens(self) -> EndpointTokenList:
        """List the project's endpoint tokens without their secrets."""
        path = "/api/v1/endpoint-tokens"
        return self.decode(self.send("GET", path), path, EndpointTokenList.from_dict)

    def delete_token(self, name: str) -> None:
        """Revoke a token; calls with it are refused from now on."""
        self._deleted(f"/api/v1/endpoint-tokens/{self.encode_ref(name)}")

    def _deleted(self, path: str) -> None:
        """Expect the empty answer of a deletion."""
        response = self.send("DELETE", path)
        if response.status_code != 204 or response.content:
            raise ApiError("Expected an empty deletion response.", status=response.status_code)
