"""Image content parts for chat completions on vision models."""

from __future__ import annotations

import base64
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx2

from trajectory import Client

# The API refuses larger images, inline or uploaded.
MAX_IMAGE_BYTES = 16 * 1024 * 1024
_SIGNATURES = ((b"\x89PNG\r\n\x1a\n", "image/png"), (b"\xff\xd8\xff", "image/jpeg"))
DEFAULT_IMAGE_UPLOAD_TIMEOUT = 120.0


@dataclass(frozen=True)
class ImageInput:
  """A PNG or JPEG to show a vision model in a chat completion message."""

  data: bytes = field(repr=False)
  media_type: str = field(init=False)

  def __post_init__(self) -> None:
    if not isinstance(self.data, bytes):
      raise TypeError("data must be bytes; use ImageInput.from_path for a file")
    if len(self.data) > MAX_IMAGE_BYTES:
      raise ValueError(f"image is larger than the {MAX_IMAGE_BYTES}-byte limit")
    for signature, media_type in _SIGNATURES:
      if self.data.startswith(signature):
        object.__setattr__(self, "media_type", media_type)
        return
    raise ValueError("image must be a PNG or JPEG")

  @classmethod
  def from_path(cls, path: str | Path) -> ImageInput:
    # Read one byte past the limit so an oversized file is refused without loading all of it.
    with Path(path).expanduser().open("rb") as source:
      return cls(source.read(MAX_IMAGE_BYTES + 1))

  def part(self) -> dict[str, Any]:
    """Return an inline ``image_url`` content part carrying the image as a data URL.

    Inline images count toward the request body's 32 MiB cap. Use ``upload`` for large
    images or ones you send on many turns.
    """
    url = f"data:{self.media_type};base64,{base64.b64encode(self.data).decode()}"
    return {"type": "image_url", "image_url": {"url": url}}

  def upload(
    self,
    client: Client,
    trajectory_id: str,
    *,
    http_client: httpx2.Client | None = None,
    timeout: float | None = None,
  ) -> dict[str, Any]:
    """Attach the image to a trajectory and return the ``image`` part that names it.

    The part is valid only in model requests for the same trajectory. ``timeout`` applies
    to the signed upload; an injected ``http_client`` keeps its own timeout unless set.
    """
    upload = client.trajectories.artifacts.create_upload(
      trajectory_id,
      media_type=self.media_type,
      size_bytes=len(self.data),
      md5=base64.b64encode(hashlib.md5(self.data, usedforsecurity=False).digest()).decode(),
    )
    if http_client is None:
      with httpx2.Client(
        timeout=DEFAULT_IMAGE_UPLOAD_TIMEOUT if timeout is None else timeout,
        follow_redirects=True,
      ) as http:
        response = http.put(upload.upload_url, content=self.data, headers=upload.headers)
    elif timeout is None:
      response = http_client.put(upload.upload_url, content=self.data, headers=upload.headers)
    else:
      response = http_client.put(
        upload.upload_url, content=self.data, headers=upload.headers, timeout=timeout
      )
    response.raise_for_status()
    artifact = client.trajectories.artifacts.complete_upload(trajectory_id, upload.artifact_id)
    return {"type": "image", "artifact_id": artifact.artifact_id}
