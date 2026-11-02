"""What a client gives the platform so that it can launch sandbox hosts for the client's project."""

from threading import Lock
from typing import ClassVar

from labqoat._generated.new_compute_run import NewComputeRun
from labqoat._generated.transport import Transport
from labqoat.assets_client import AssetsClient
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.publication import Publication
from labqoat.json_document import JsonValue
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_transport import SandboxTransport
from labqoat.schemas.schema_document import SchemaDocument


class SandboxHostTemplate:
    """The SDK's host function, published whole by a client outside the platform, or named by a run inside it.

    A client publishes the function's image, which carries this SDK, with an application of no source of its
    own: the host's module is imported from the SDK. A run instead names the function, and the platform runs
    it from the run's own image, which carries the same SDK as the run. However many requests find the project
    without one, a client gives it once.
    """

    APPLICATION: ClassVar[InputTree] = InputTree(
        (("labqoat_sandbox_host.py", b'"""Sandbox hosts run labqoat.sandbox.sandbox_host_app."""\n', 0o644),)
    )

    def __init__(self, transport: Transport | None = None) -> None:
        """Publish through a management client's transport, or name the function from inside a run."""
        self._transport = transport
        self._lock = Lock()
        self._given = False

    def give(self, sandboxes: SandboxTransport) -> None:
        """Give the platform the host function through its sandbox endpoint, unless this client already has."""
        with self._lock:
            if not self._given:
                sandboxes.send(SandboxRequest("PUT", "/sandbox-hosts/template", document=self.document()))
                self._given = True

    def document(self) -> dict[str, JsonValue]:
        """Return what the platform's template endpoint takes from this kind of client."""
        from labqoat.sandbox.sandbox_host_app import host

        if self._transport is None:
            return {"function": host.capture().to_dict(), "app_name": host.app_name}
        publication = Publication(AssetsClient(self._transport)).capture(host, self.APPLICATION)
        request = NewComputeRun(
            name=f"{host.app_name}/{publication.function.name}",
            publication=publication,
            arguments={},
            input_schema_digest=SchemaDocument.capture(dict(publication.function.input_schema)).digest,
        )
        return {"run": request.to_dict()}
