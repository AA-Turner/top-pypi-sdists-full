"""Typed client for the Labqoat starter API."""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping
from typing import TYPE_CHECKING, TypeVar
from urllib.parse import urlsplit

from labqoat._generated.api_index import ApiIndex
from labqoat._generated.location_registry import LocationRegistry
from labqoat._generated.new_note import NewNote
from labqoat._generated.note import Note
from labqoat._generated.note_page import NotePage
from labqoat._generated.note_patch import NotePatch
from labqoat._generated.status import Status
from labqoat.base_client import BaseClient
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat._generated.transport import Transport
    from labqoat.net.response import Response
    from labqoat.assets_client import AssetsClient
    from labqoat.compute.client_group import ClientGroup
    from labqoat.compute.upload_memo import UploadMemo
    from labqoat.compute_client import ComputeClient
    from labqoat.coordination.dict import Dict
    from labqoat.coordination.dicts_client import DictsClient
    from labqoat.coordination.management_channel import ManagementChannel
    from labqoat.coordination.queue import Queue
    from labqoat.coordination.queues_client import QueuesClient
    from labqoat.datasets_client import DatasetsClient
    from labqoat.runs_client import RunsClient
    from labqoat.worker_pools_client import WorkerPoolsClient
    from labqoat.memory_client import MemoryClient
    from labqoat.projects_client import ProjectsClient
    from labqoat.endpoints_client import EndpointsClient
    from labqoat.secrets_client import SecretsClient
    from labqoat.volumes_client import VolumesClient

ModelT = TypeVar("ModelT")


class Client:
    """HTTP Basic client sharing one transport across calls."""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        timeout_seconds: float = 30.0,
        transport: Transport | None = None,
        environment: str = "default",
        project: str | None = None,
        agent: str | None = None,
    ) -> None:
        """Configure the endpoint, credentials, timeout and the project every request acts on."""
        if transport is None:
            from labqoat._generated.transport import Transport

            transport = Transport(
                base_url=base_url,
                username=username,
                password=password,
                timeout_seconds=timeout_seconds,
                environment=environment,
                project=project,
                agent=agent,
            )
        self._transport = transport
        self._uploads: UploadMemo | None = None

    def with_uploads(self, uploads: UploadMemo | None) -> Client:
        """Share one upload memo with this client's submissions and hand the client back."""
        self._uploads = uploads
        return self

    def status(self) -> Status:
        """Read the service status, verifying credentials."""
        response = self.send("GET", "/api/v1/status")
        return self.decode_model(response, "/api/v1/status", Status.from_dict)

    @property
    def assets(self) -> AssetsClient:
        """Upload and read immutable assets through this client's explicit credentials."""
        from labqoat.assets_client import AssetsClient

        return AssetsClient(self._transport)

    @property
    def endpoints(self) -> EndpointsClient:
        """Deploy web server functions for the world to call and manage the tokens that call them."""
        from labqoat.endpoints_client import EndpointsClient

        return EndpointsClient(self._transport)

    @property
    def secrets(self) -> SecretsClient:
        """Manage environment-scoped credentials without exposing stored values."""
        from labqoat.secrets_client import SecretsClient

        return SecretsClient(self._transport)

    @property
    def volumes(self) -> VolumesClient:
        """Create, list and remove the selected project's volumes and copy files in and out of them."""
        from labqoat.volumes_client import VolumesClient

        return VolumesClient(self._transport)

    @property
    def projects(self) -> ProjectsClient:
        """List, create, delete and reorganize the projects of this client's environment."""
        from labqoat.projects_client import ProjectsClient

        return ProjectsClient(self._transport)

    @property
    def datasets(self) -> DatasetsClient:
        """Use the shared explicit-credential transport for dataset publications."""
        from labqoat.datasets_client import DatasetsClient

        return DatasetsClient(self._transport)

    @property
    def transport(self) -> Transport:
        """The explicit transport this client sends through."""
        return self._transport

    @property
    def uploads(self) -> UploadMemo | None:
        """The upload memo shared by clients of one service."""
        return self._uploads

    def group(self, name: str) -> ClientGroup:
        """Open a group for the runs submitted inside ``with client.group(name) as group:``."""
        from labqoat.compute.client_group import ClientGroup

        return ClientGroup(self, name)

    @property
    def runs(self) -> RunsClient:
        """Submit and read executions using the shared explicit-credential transport."""
        from labqoat.runs_client import RunsClient

        return RunsClient(self._transport, uploads=self._uploads)

    @property
    def worker_pools(self) -> WorkerPoolsClient:
        """Manage retained warm fleets with explicit host authority."""
        from labqoat.worker_pools_client import WorkerPoolsClient

        return WorkerPoolsClient(self._transport)

    @property
    def compute(self) -> ComputeClient:
        """Manage shared compute limits, location policy and connected hosts."""
        from labqoat.compute_client import ComputeClient

        return ComputeClient(self._transport)

    def locations(self) -> LocationRegistry:
        """Inspect permitted execution destinations and the exact environment default."""
        path = "/api/v1/locations"
        return self.decode_model(self.send("GET", path), path, LocationRegistry.from_dict)

    def api_index(self) -> ApiIndex:
        """Read the API discovery resource."""
        response = self.send("GET", "/api/v1")
        return self.decode_model(response, "/api/v1", ApiIndex.from_dict)

    @property
    def memory(self) -> MemoryClient:
        """Use the durable research memory of this client's project."""
        from labqoat.memory_client import MemoryClient

        return MemoryClient(self._transport)

    def dict(self, name: str) -> Dict:
        """A dict of this client's project, shared with its runs; the first write creates it."""
        from labqoat.coordination.dict import Dict

        return Dict(self._channel(), name)

    def queue(self, name: str) -> Queue:
        """A queue of this client's project, shared with its runs; the first put creates it."""
        from labqoat.coordination.queue import Queue

        return Queue(self._channel(), name)

    @property
    def dicts(self) -> DictsClient:
        """List and delete this project's dicts, or use a throwaway one."""
        from labqoat.coordination.dicts_client import DictsClient

        return DictsClient(self._channel())

    @property
    def queues(self) -> QueuesClient:
        """List and delete this project's queues, or use a throwaway one."""
        from labqoat.coordination.queues_client import QueuesClient

        return QueuesClient(self._channel())

    def _channel(self) -> ManagementChannel:
        """Dicts and queues travel under this client's credentials and project."""
        from labqoat.coordination.management_channel import ManagementChannel

        return ManagementChannel(self._transport)

    def list_notes(self, limit: int | None = None, cursor: str | None = None) -> NotePage:
        """Read one bounded page of notes."""
        path = Client.page_path(limit, cursor)
        response = self.send("GET", path)
        return self.decode_model(response, path, NotePage.from_dict)

    def iter_notes(self, page_size: int = 20) -> Iterator[Note]:
        """Yield notes lazily by following returned pagination links."""
        cursor: str | None = None
        while True:
            page = self.list_notes(limit=page_size, cursor=cursor)
            yield from page.items
            cursor = Client.next_cursor(page)
            if cursor is None:
                return

    def create_note(self, title: str, body: str | None = None) -> Note:
        """Create a note from its submitted representation."""
        request = NewNote(title=title, body=body)
        response = self.send_json("POST", "/api/v1/notes", request.to_dict())
        return self.decode_model(response, "/api/v1/notes", Note.from_dict)

    def get_note(self, note_id: str) -> Note:
        """Retrieve a note by ID."""
        path = f"/api/v1/notes/{note_id}"
        response = self.send("GET", path)
        return self.decode_model(response, path, Note.from_dict)

    def update_note(self, note_id: str, patch: NotePatch) -> Note:
        """Apply a merge-patch document atomically."""
        path = f"/api/v1/notes/{note_id}"
        response = self.send_json(
            path=path, payload=patch.to_dict(), method="PATCH", content_type="application/merge-patch+json"
        )
        return self.decode_model(response, path, Note.from_dict)

    def delete_note(self, note_id: str) -> None:
        """Remove a note, accepting an empty response."""
        path = f"/api/v1/notes/{note_id}"
        response = self.send("DELETE", path)
        if response.status_code != 204:
            BaseClient.raise_for_status(path, response)
            raise ApiError("Expected an empty deletion response.", status=response.status_code)
        if response.content:
            raise ApiError("Expected an empty deletion response.", status=204)

    def close(self) -> None:
        """Release the underlying HTTP client."""
        self._transport.close()

    def __enter__(self) -> Client:
        """Open the client for a managed block."""
        self._transport.open_client()
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        """Close the client after a managed block."""
        self.close()

    def send(self, method: str, path: str) -> Response:
        """Send one authenticated request, mapping transport failures."""
        return BaseClient(self._transport).request(method, path)

    def send_json(
        self, method: str, path: str, payload: Mapping[str, JsonValue], content_type: str = "application/json"
    ) -> Response:
        """Send one JSON request with an explicit content type."""
        import json as json_module

        content = json_module.dumps(payload).encode("utf-8")
        return BaseClient(self._transport).request(method, path, content=content, content_type=content_type)

    def decode_body(self, response: Response, path: str) -> JsonDocument:
        """Decode a response body or raise the matching typed error."""
        BaseClient.raise_for_status(path, response)
        try:
            import json as json_module

            decoded = json_module.loads(response.content.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as error:
            raise ApiError(f"Malformed response from {path}.") from error
        if not isinstance(decoded, dict):
            raise ApiError(f"Malformed response from {path}.")
        return JsonDocument(decoded)

    def decode_model(
        self,
        response: Response,
        path: str,
        factory: Callable[[Mapping[str, JsonValue]], ModelT],
    ) -> ModelT:
        """Decode a body and build a typed model from it."""
        try:
            return factory(self.decode_body(response, path))
        except (KeyError, TypeError, ValueError) as error:
            raise ApiError(f"Malformed response from {path}.") from error

    @staticmethod
    def page_path(limit: int | None, cursor: str | None) -> str:
        """Build a collection path with explicit pagination parameters."""
        from urllib.parse import urlencode

        params: dict[str, str] = {}
        if limit is not None:
            params["limit"] = str(limit)
        if cursor is not None:
            params["cursor"] = cursor
        if not params:
            return "/api/v1/notes"
        return f"/api/v1/notes?{urlencode(params)}"

    @staticmethod
    def next_cursor(page: NotePage) -> str | None:
        """Extract the next cursor from page links, if present."""
        raw = page.links.get("next")
        if not isinstance(raw, str) or not raw:
            return None
        return Client.cursor_from_link(raw)

    @staticmethod
    def cursor_from_link(link: str) -> str | None:
        """Parse the cursor query value from a pagination link."""
        from urllib.parse import parse_qs

        query = parse_qs(urlsplit(link).query)
        values = query.get("cursor", [])
        if not values:
            return None
        return values[0]

    @staticmethod
    def resolve_link(base_url: str, link: str) -> str:
        """Resolve a server link against the base URL with origin checks."""
        from urllib.parse import urljoin

        resolved = urljoin(base_url.rstrip("/") + "/", link.lstrip("/"))
        Client.ensure_same_origin(base_url, resolved)
        return resolved

    @staticmethod
    def ensure_same_origin(base_url: str, target: str) -> None:
        """Reject server links pointing at another origin."""
        base = urlsplit(base_url)
        other = urlsplit(target)
        if (base.scheme, base.hostname, base.port) != (other.scheme, other.hostname, other.port):
            raise ApiError("Server link points at another origin.")
