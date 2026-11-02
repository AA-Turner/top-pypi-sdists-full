"""Sandboxes the platform places on hosts it launches, reached through its API from anywhere in a project."""

import asyncio
import base64
import os
import re
from dataclasses import replace
from collections.abc import Mapping
from threading import Lock
from typing import TYPE_CHECKING, ClassVar, Unpack, cast

from labqoat._generated.transport import Transport
from labqoat.compute.image import Image
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.sandbox.sandbox import Sandbox
from labqoat.sandbox.sandbox_creation import SandboxCreation
from labqoat.sandbox.sandbox_host_template import SandboxHostTemplate
from labqoat.sandbox.sandbox_image_builds import SandboxImageBuilds
from labqoat.sandbox.sandbox_not_found_error import SandboxNotFoundError
from labqoat.sandbox.sandbox_options import SandboxOptions
from labqoat.sandbox.sandbox_placement import SandboxPlacement
from labqoat.sandbox.sandbox_platform_options import SandboxPlatformOptions
from labqoat.sandbox.sandbox_request import SandboxRequest
from labqoat.sandbox.sandbox_response import SandboxResponse
from labqoat.sandbox.sandbox_route import SandboxRoute
from labqoat.sandbox.sandbox_transport import SandboxTransport

if TYPE_CHECKING:
    from labqoat.client import Client


class SandboxPlatform:
    """Create sandboxes the platform places, and find them again by identifier, as a client or as a run.

    A client outside the platform acts in the project it names, with its management credentials. A run acts in
    its own project with its own credentials. The platform starts hosts for the project when sandboxes need room
    and stops them when they have had none for a while; every request about a sandbox reaches the host that has
    it. Handles are the same ``Sandbox`` a function's own sandbox host gives.
    """

    WORKER_VARIABLES: ClassVar[tuple[str, str, str]] = (
        "LABQOAT_API_URL",
        "LABQOAT_CREDENTIAL_ID",
        "LABQOAT_WORKER_SECRET",
    )
    WAIT_SECONDS: ClassVar[float] = 900.0
    TRANSFER_SECONDS: ClassVar[float] = 600.0
    _default: ClassVar["SandboxPlatform | None"] = None
    _default_lock: ClassVar[Lock] = Lock()

    def __init__(
        self, transport: SandboxTransport, template: SandboxHostTemplate, images: SandboxImageBuilds | None
    ) -> None:
        """Bind where the platform answers, what publishes the host function, and what builds declared images."""
        self._transport = transport
        self._template = template
        self._images = images

    @classmethod
    def for_client(cls, client: "Client", *, timeout: float = 180.0) -> "SandboxPlatform":
        """Act through a management client in the project it names.

        Publishing the host function and building images upload archives, which may take longer than the
        client's own requests are allowed; those get ``TRANSFER_SECONDS`` at least.
        """
        transport = client.transport
        headers = {**Transport.basic_headers(transport.username, transport.password), **transport.default_headers()}
        route = SandboxRoute.served(transport.base_url.rstrip("/") + "/api/v1", headers)
        patient = max(transport.timeout_seconds, cls.TRANSFER_SECONDS)
        transfers = replace(transport, timeout_seconds=patient, _client=None)
        return cls(SandboxTransport(route, timeout), SandboxHostTemplate(transfers), SandboxImageBuilds(transfers))

    @classmethod
    def for_run(cls, environ: Mapping[str, str] | None = None, *, timeout: float = 180.0) -> "SandboxPlatform":
        """Act as the run whose credentials the platform gave this process."""
        values = os.environ if environ is None else environ
        url, credential, secret = (values[name] for name in cls.WORKER_VARIABLES)
        authorization = "Basic " + base64.b64encode(f"{credential}:{secret}".encode()).decode()
        headers = {"X-Labqoat-Worker-Authorization": authorization}
        route = SandboxRoute.served(url.rstrip("/") + "/api/v1/worker", headers)
        return cls(SandboxTransport(route, timeout), SandboxHostTemplate(), None)

    @classmethod
    def default(cls) -> "SandboxPlatform":
        """Act as this run inside the platform, or outside it as the CLI's saved profile in the selected project.

        The choice is made once per process and kept, so credentials are looked up once.
        """
        with cls._default_lock:
            if cls._default is None:
                cls._default = cls.for_run() if cls.WORKER_VARIABLES[2] in os.environ else cls._profile()
            return cls._default

    @classmethod
    def _profile(cls) -> "SandboxPlatform":
        """Use the credentials and project the CLI would, which the CLI resolves."""
        from labqoat.cli.profile_client import ProfileClient

        return cls.for_client(ProfileClient.default())

    def create(self, *entrypoint: str, image: str | Image, **options: Unpack[SandboxPlatformOptions]) -> Sandbox:
        """Start a sandbox and return its handle; see ``labqoat.Sandbox.create``."""
        request = self._request(entrypoint, image, options)
        placement = SandboxPlacement(self._transport, self._template, options.get("wait", self.WAIT_SECONDS))
        return SandboxResponse.decoded(placement.send(request), self._sandbox)

    async def create_async(
        self, *entrypoint: str, image: str | Image, **options: Unpack[SandboxPlatformOptions]
    ) -> Sandbox:
        """Start a sandbox without blocking the event loop; see ``create``."""
        request = await asyncio.to_thread(self._request, entrypoint, image, options)
        placement = SandboxPlacement(self._transport, self._template, options.get("wait", self.WAIT_SECONDS))
        return SandboxResponse.decoded(await placement.send_async(request), self._sandbox)

    def from_id(self, sandbox_id: str) -> Sandbox:
        """Return a handle on a sandbox of this project by identifier, wherever it was created, without asking.

        Like ``SandboxClient.from_id``; the first operation on a sandbox that is gone raises
        ``SandboxNotFoundError``.
        """
        return Sandbox(sandbox_id, self._transport)

    def from_name(self, name: str) -> Sandbox:
        """Return the project's sandbox created under ``name``, on whichever host, or raise ``SandboxNotFoundError``.

        A name belongs to one of a project's sandboxes at a time.
        """
        return self._named(name, self._transport.send(self._listing({"name": name})))

    async def from_name_async(self, name: str) -> Sandbox:
        """Find a sandbox by name without blocking the event loop; see ``from_name``."""
        return self._named(name, await self._transport.send_async(self._listing({"name": name})))

    def list(self, tags: Mapping[str, str] | None = None) -> tuple[Sandbox, ...]:
        """Return the project's sandboxes on every host, only those carrying every one of ``tags`` when given."""
        return self._listed(self._transport.send(self._listing(self._tags(tags))))

    async def list_async(self, tags: Mapping[str, str] | None = None) -> tuple[Sandbox, ...]:
        """List the project's sandboxes without blocking the event loop; see ``list``."""
        return self._listed(await self._transport.send_async(self._listing(self._tags(tags))))

    @staticmethod
    def _listing(query: Mapping[str, str]) -> SandboxRequest:
        """Ask the platform, not a host, which of the project's sandboxes match."""
        return SandboxRequest("GET", "/sandboxes", query=query)

    @staticmethod
    def _tags(tags: Mapping[str, str] | None) -> dict[str, str]:
        """Spell wanted tags as the platform reads them from a query."""
        return {f"tags[{key}]": value for key, value in (tags or {}).items()}

    def _listed(self, content: bytes) -> tuple[Sandbox, ...]:
        """Bind every listed sandbox to this platform's transport; a malformed listing is the platform's failure."""
        return SandboxResponse.decoded(content, self._each)

    def _each(self, listing: JsonDocument) -> tuple[Sandbox, ...]:
        """The sandboxes a listing names, in its order."""
        return tuple(
            self._sandbox(JsonDocument.expect_dict(item)) for item in JsonDocument.expect_list(listing["sandboxes"])
        )

    def _named(self, name: str, content: bytes) -> Sandbox:
        """The one listed sandbox with a name."""
        found = self._listed(content)
        if not found:
            raise SandboxNotFoundError(f"No sandbox of this project is named {name}")
        return found[0]

    def _request(
        self, entrypoint: tuple[str, ...], image: str | Image, options: SandboxPlatformOptions
    ) -> SandboxRequest:
        """Describe the sandbox as a host would be told, its image by reference, and the secrets it is given."""
        reference = image if isinstance(image, str) else self._built(image)
        gpus = self._gpus(options.get("gpu"))
        hosted = cast(SandboxOptions, {**options, "image": reference, "gpu": gpus.get("gpu")})
        created = SandboxCreation.request(entrypoint, hosted)
        secrets: list[JsonValue] = [secret.name for secret in options.get("secrets", ())]
        document: dict[str, JsonValue] = {**(created.document or {}), **({"secrets": secrets} if secrets else {})}
        return SandboxRequest("POST", "/sandboxes", document=document | gpus)

    @staticmethod
    def _gpus(gpu: str | None) -> dict[str, JsonValue]:
        """Read ``"model"`` or ``"model:count"`` as the GPUs' count and model, nothing when none were asked for."""
        if gpu is None:
            return {}
        if not isinstance(gpu, str) or not re.fullmatch(r"[A-Za-z0-9-]+(:[1-8])?", gpu):
            raise ValueError(
                f"gpu names a model and optionally a count from 1 to 8, such as 'a10g' or 'l4:2', not {gpu!r}"
            )
        model, _, count = gpu.lower().partition(":")
        return {"gpu": int(count or 1), "gpu_model": model}

    def _built(self, image: Image) -> str:
        """Build a declared image, which only a client outside the platform can."""
        if self._images is None:
            raise TypeError("A run names its sandbox's image by reference; build a compute.Image from a client first")
        return self._images.reference(image)

    def _sandbox(self, document: JsonDocument) -> Sandbox:
        """Bind the identifier the platform confirmed to this platform's transport."""
        return Sandbox(JsonDocument.expect_scalar(document["id"], str), self._transport)
