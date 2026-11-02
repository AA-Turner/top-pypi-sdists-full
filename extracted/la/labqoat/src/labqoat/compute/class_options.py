"""Immutable execution configuration for explicitly initialized compute classes."""

from dataclasses import dataclass, field

from labqoat.compute.image import Image
from labqoat.compute.images.app_images import AppImages
from labqoat.compute.workers import Workers
from labqoat.compute.volume import Volume
from labqoat.compute.sandboxes import Sandboxes
from labqoat.compute.secret import Secret
from labqoat.training.budgets.fit_allowance import FitAllowance


@dataclass(frozen=True)
class ClassOptions:
    """Keep class initialization and its methods on the same captured image and resource budget."""

    app_name: str
    image: Image
    cpu: float
    memory: int
    timeout: int
    gpu: str | None = None
    retries: int = 0
    registry: AppImages = field(default_factory=AppImages, compare=False, repr=False)
    workers: Workers | None = None
    volumes: tuple[tuple[str, Volume], ...] = ()
    secrets: tuple[Secret, ...] = ()
    sandboxes: Sandboxes | None = None
    gpu_memory: int | None = None
    gpu_count: int | None = None
    ephemeral_disk: int | None = None
    exact_resources: bool = False
    spot: bool = False
    queue_timeout: int | None = None
    location: str | None = None
    fit_allowance: FitAllowance | None = None
