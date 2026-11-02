"""Declarative compute App with explicit host-side entrypoints."""

from collections.abc import Mapping, Sequence

from labqoat.compute.function_decorator import FunctionDecorator
from labqoat.compute.class_decorator import ClassDecorator
from labqoat.compute.class_options import ClassOptions
from labqoat.compute.image import Image
from labqoat.compute.images.app_images import AppImages
from labqoat.compute.local_entrypoint_decorator import LocalEntrypointDecorator
from labqoat.compute.workers import Workers
from labqoat.compute.volume import Volume
from labqoat.compute.volume_mounts import VolumeMounts
from labqoat.compute.sandboxes import Sandboxes
from labqoat.compute.secret import Secret


class App:
    """Group captured functions under one name without network or build side effects."""

    def __init__(self, name: str, *, image: Image | None = None) -> None:
        """Retain the application name and its default image, the minimal catalog image unless declared."""
        self.name = name
        self.image = image or Image.debian_slim()
        self._images = AppImages()

    @staticmethod
    def memory(memory: int | None, gpu: str | None, gpu_count: int | None) -> int:
        """The memory (MiB) a function reserves: as declared, else 1 GiB, or 8 GiB per GPU for a GPU function."""
        if memory is not None:
            return memory
        count = int(gpu is not None) if gpu_count is None else gpu_count
        return 8192 * count if count > 0 else 1024

    @property
    def registry(self) -> AppImages:
        """The App's declared callables, which every publication of one of them carries."""
        return self._images

    def function(  # noqa: PLR0913 -- Approved public decorator API keeps existing keyword compatibility.
        self,
        *,
        image: Image | None = None,
        cpu: float = 1,
        memory: int | None = None,
        timeout: int = 300,
        queue_timeout: int | None = None,
        location: str | None = None,
        gpu: str | None = None,
        gpu_memory: int | None = None,
        gpu_count: int | None = None,
        ephemeral_disk: int | None = None,
        exact_resources: bool = False,
        spot: bool = False,
        retries: int = 0,
        workers: Workers | None = None,
        volumes: Mapping[str, Volume] | None = None,
        secrets: Sequence[Secret] = (),
        sandboxes: Sandboxes | Sequence[str] | None = None,
        memory_snapshot: bool = False,
    ) -> FunctionDecorator:
        """Capture options alongside a typed root callable.

        With ``memory_snapshot``, the first run of the deployed function on a kind of machine saves its memory, GPU
        memory included, once its module is imported and, for a ``@web_server``, once its server answers on its
        port. Later runs on that kind of machine continue from the snapshot instead of starting again.
        """
        return FunctionDecorator(
            self.name,
            image or self.image,
            cpu,
            App.memory(memory, gpu, gpu_count),
            timeout,
            gpu,
            retries,
            self._images,
            workers=workers,
            volumes=VolumeMounts.capture(volumes),
            secrets=tuple(secrets),
            sandboxes=Sandboxes.declared(sandboxes),
            gpu_memory=gpu_memory,
            gpu_count=gpu_count,
            ephemeral_disk=ephemeral_disk,
            exact_resources=exact_resources,
            spot=spot,
            queue_timeout=queue_timeout,
            location=location,
            memory_snapshot=memory_snapshot,
        )

    def local_entrypoint(self) -> LocalEntrypointDecorator:
        """Mark a launcher for host execution with an explicitly supplied Client."""
        return LocalEntrypointDecorator(self.name)

    def cls(  # noqa: PLR0913 -- Approved public decorator API keeps existing keyword compatibility.
        self,
        *,
        image: Image | None = None,
        cpu: float = 1,
        memory: int | None = None,
        timeout: int = 300,
        queue_timeout: int | None = None,
        location: str | None = None,
        gpu: str | None = None,
        gpu_memory: int | None = None,
        gpu_count: int | None = None,
        ephemeral_disk: int | None = None,
        exact_resources: bool = False,
        spot: bool = False,
        retries: int = 0,
        workers: Workers | None = None,
        volumes: Mapping[str, Volume] | None = None,
        secrets: Sequence[Secret] = (),
        sandboxes: Sandboxes | Sequence[str] | None = None,
    ) -> ClassDecorator:
        """Declare fresh worker-owned class instances with typed constructor bindings and explicit initialization."""
        return ClassDecorator(
            ClassOptions(
                self.name,
                image or self.image,
                cpu,
                App.memory(memory, gpu, gpu_count),
                timeout,
                gpu,
                retries,
                self._images,
                workers=workers,
                volumes=VolumeMounts.capture(volumes),
                secrets=tuple(secrets),
                sandboxes=Sandboxes.declared(sandboxes),
                gpu_memory=gpu_memory,
                gpu_count=gpu_count,
                ephemeral_disk=ephemeral_disk,
                exact_resources=exact_resources,
                spot=spot,
                queue_timeout=queue_timeout,
                location=location,
            )
        )
