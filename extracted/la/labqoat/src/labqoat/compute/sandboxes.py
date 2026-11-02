"""A block of a function's own machine set aside for the sandboxes it starts."""

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import ClassVar

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class Sandboxes:
    """Declare the images a function's sandboxes may start from and the share its own process keeps.

    The function's ``cpu`` and ``memory`` are the whole block. ``driver_cpu`` and ``driver_memory`` are what the
    function's own process runs with, one core and 1024 MiB unless it needs more; the rest is the budget of
    the sandboxes it creates through ``labqoat.sandbox.SandboxClient``. A function that is happy with that
    share declares only the images: ``sandboxes=["registry/image:tag"]``. ``Sandboxes.ANY`` instead of a list
    starts whatever image each sandbox names, pulling it anonymously unless the platform placed it. The function
    keeps all its GPUs unless ``driver_gpu`` says how many; the rest go to sandboxes that ask for ``gpu``.
    """

    images: Sequence[str]
    driver_cpu: float = 1
    driver_memory: int = 1024
    driver_gpu: int | None = None

    IMAGE: ClassVar[re.Pattern[str]] = re.compile(r"[a-z0-9][A-Za-z0-9._/:-]{0,199}(@sha256:[0-9a-f]{64})?")
    MAXIMUM: ClassVar[int] = 256
    ANY: ClassVar[str] = "any"

    def __post_init__(self) -> None:
        """Freeze the image list and validate it and the driver share without contacting a host."""
        images = self.ANY if self.images == self.ANY else tuple(self.images)
        object.__setattr__(self, "images", images)
        if images != self.ANY:
            self._validate_images(tuple(images))
        if self.driver_cpu <= 0 or type(self.driver_memory) is not int or self.driver_memory < 1:
            raise ValueError("The driver share needs positive CPU and a positive integer number of MiB")
        if self.driver_gpu is not None and (type(self.driver_gpu) is not int or self.driver_gpu < 0):
            raise ValueError("driver_gpu is how many of the function's GPUs it keeps: a whole number, 0 or more")

    def _validate_images(self, images: tuple[str, ...]) -> None:
        """Require a short list of distinct references that no tool could read as an option."""
        if not 1 <= len(images) <= self.MAXIMUM or len(set(images)) != len(images):
            raise ValueError(f"Sandboxes need 1..{self.MAXIMUM} distinct images")
        if not all(type(image) is str and self.IMAGE.fullmatch(image) for image in images):
            raise ValueError("Sandbox images must be registry references such as registry/name:tag or name@sha256:...")

    @classmethod
    def declared(cls, block: "Sandboxes | Sequence[str] | None") -> "Sandboxes | None":
        """Read what a function wrote: nothing, a block, or only the images, or any image, with the usual share."""
        if block is None or isinstance(block, Sandboxes):
            return block
        if block == cls.ANY:
            return cls(cls.ANY)
        if isinstance(block, str):
            raise TypeError("sandboxes is a list of images, such as sandboxes=['registry/image:tag']")
        return cls(block)

    def validate_block(self, cpu: float, memory: int) -> None:
        """Require the function's resources to leave room for sandboxes beside its own process."""
        if int(self.driver_cpu * 1000) >= int(cpu * 1000) or self.driver_memory >= memory:
            raise ValueError(
                f"This function declares cpu={cpu:g}, memory={memory}, which leaves its sandboxes nothing: its "
                f"own process keeps cpu={self.driver_cpu:g}, memory={self.driver_memory} (driver_cpu, "
                "driver_memory) and its sandboxes share the rest. Declare cpu and memory as the total, for example "
                f"cpu={self.driver_cpu + 4:g}, memory={self.driver_memory + 8192} for sandboxes using 4 CPUs and "
                "8192 MiB together"
            )

    def to_dict(self) -> dict[str, JsonValue]:
        """Capture the images and the driver share in the units the platform reserves."""
        driver: dict[str, JsonValue] = {
            "cpu_millicores": int(self.driver_cpu * 1000),
            "memory_mb": self.driver_memory,
            **({} if self.driver_gpu is None else {"gpu_count": self.driver_gpu}),
        }
        images: JsonValue = self.ANY if self.images == self.ANY else list(self.images)
        return {"images": images, "driver": driver}
