from uuid import UUID

from pydantic import BaseModel

from .fingerprint import Fingerprint
from .image import Image

class Container(BaseModel):
    """
    The Container object describes an instance of a specific container. A container
    is a prepackaged, portable system image that runs isolated on an existing system
    using a container runtime like containerd.
    """

    # Recommended:
    name: str | None = None # The container name.
    image: Image | None = None # The container image used as a template to run the container.
    uid: str | None = None # The full container unique identifier for this instantiation of the
                           # container. For example: `ac2ea168264a08f9aaca0dfc82ff3551418dfd22d02b
                           # 713142a6843caa2f61bf`.
    size: int | None = None # The size of the container image.
    hash: Fingerprint | None = None # Commit hash of image created for docker or the SHA256 hash of the
                                    # container. For example: `13550340a8681c84c861aac2e5b440161c2
                                    # b33a3e4f302ac680ca5b686de48de`.

    # Optional:
    runtime: str | None = None
    orchestrator: str | None = None
    pod_uuid: UUID | None = None
    tag: str | None = None # The tag used by the container. It can indicate version, format, OS.
    network_driver: str | None = None
