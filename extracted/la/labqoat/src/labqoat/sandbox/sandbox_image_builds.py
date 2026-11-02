"""Images a client declares with ``compute.Image``, built by the platform's builder before a sandbox starts."""

from collections.abc import Callable
from threading import Lock
from time import monotonic, sleep
from typing import ClassVar

from labqoat._generated.build import Build
from labqoat._generated.transport import Transport
from labqoat.assets_client import AssetsClient
from labqoat.builds_client import BuildsClient
from labqoat.compute.image import Image
from labqoat.compute.publication import Publication
from labqoat.sandbox.sandbox_host_template import SandboxHostTemplate
from labqoat.sandbox.sandbox_invalid_request_error import SandboxInvalidRequestError


class SandboxImageBuilds:
    """Build a declared image once and name it by the digest-pinned reference the builder pushed.

    The platform keeps one build per recipe, so an image any earlier client built is named at once. Within one
    client each image is resolved once.
    """

    POLL_SECONDS: ClassVar[float] = 2.0
    LONGEST_SECONDS: ClassVar[float] = 3600.0

    def __init__(self, transport: Transport, pause: Callable[[float], None] = sleep) -> None:
        """Bind the management transport builds are registered and read through."""
        self._transport = transport
        self._builds = BuildsClient(transport)
        self._pause = pause
        self._lock = Lock()
        self._known: dict[Image, str] = {}

    def reference(self, image: Image) -> str:
        """Return the image's pullable reference, building it first when the platform has none yet."""
        with self._lock:
            if image not in self._known:
                self._known[image] = self._built(image)
            return self._known[image]

    def _built(self, image: Image) -> str:
        """Register the image's recipe, start it when nobody has, and wait for its result."""
        recipe = Publication(AssetsClient(self._transport)).image_build(image, SandboxHostTemplate.APPLICATION)
        build = self._builds.create_build({"recipe": recipe})
        if build.status == "upload_pending":
            build = self._builds.start_build(build.id)
        deadline = monotonic() + self.LONGEST_SECONDS
        while build.status not in ("succeeded", "failed") and monotonic() < deadline:
            self._pause(self.POLL_SECONDS)
            build = self._builds.get_build(build.id)
        return self._pulled(build)

    @staticmethod
    def _pulled(build: Build) -> str:
        """Name the built image, or say why there is none."""
        if build.status != "succeeded" or build.image_ref is None:
            reason = build.failure_detail or build.status
            raise SandboxInvalidRequestError(f"Image build {build.id} did not produce an image: {reason}")
        return build.image_ref
