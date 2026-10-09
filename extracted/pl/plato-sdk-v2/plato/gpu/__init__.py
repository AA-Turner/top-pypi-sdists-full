"""GPU machines for worlds and tools: serverless renders and whole-machine pods.

Two kinds of work, one client:

- A **render** is headless: a ``.blend`` in, a tar of frames out, on a
  serverless GPU worker (``sims/gpu-box-runpod/serverless`` in the plato
  repo). ``GpuClient.render``.
- A **pod** is a whole GPU machine for one live session: a desktop, a game
  served over MCP, a recording of the whole thing. It bills for every hour it
  exists, so only the named :data:`~plato.gpu.profiles.PROFILES` exist, and
  the caller ends it. ``GpuClient.create_pod`` / ``terminate_pod``.

The provider (Runpod today, :mod:`plato.gpu.providers`) is behind
:class:`~plato.gpu.providers.base.GpuProvider`; the bucket the files move
through is behind :class:`~plato.gpu.storage.ObjectStore`. Credentials come
in as :class:`~plato.gpu.settings.GpuSettings`: a world gets them in its
launch config (the platform hands them only to worlds an admin allowed), a
person gets them from the environment (``plato gpu ...``).
"""

from plato.gpu.client import GpuClient, GpuUnavailable
from plato.gpu.pods import PodSession, PodStatus, PodView
from plato.gpu.profiles import PROFILES, PodImage, UnknownProfile
from plato.gpu.providers.base import GpuProviderError
from plato.gpu.render import RenderFailed, RenderOutcome, RenderResult
from plato.gpu.settings import GpuSettings

__all__ = [
    "PROFILES",
    "GpuClient",
    "GpuProviderError",
    "GpuSettings",
    "GpuUnavailable",
    "PodImage",
    "PodSession",
    "PodStatus",
    "PodView",
    "RenderFailed",
    "RenderOutcome",
    "RenderResult",
    "UnknownProfile",
]
