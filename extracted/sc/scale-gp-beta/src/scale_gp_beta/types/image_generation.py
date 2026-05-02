# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ImageGeneration", "InputImageMask"]


class InputImageMask(BaseModel):
    file_id: Optional[str] = None

    image_url: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class ImageGeneration(BaseModel):
    type: Literal["image_generation"]

    background: Optional[Literal["transparent", "opaque", "auto"]] = None

    input_fidelity: Optional[Literal["high", "low"]] = None

    input_image_mask: Optional[InputImageMask] = None

    model: Optional[Literal["gpt-image-1"]] = None

    moderation: Optional[Literal["auto", "low"]] = None

    output_compression: Optional[int] = None

    output_format: Optional[Literal["png", "webp", "jpeg"]] = None

    partial_images: Optional[int] = None

    quality: Optional[Literal["low", "medium", "high", "auto"]] = None

    size: Optional[Literal["1024x1024", "1024x1536", "1536x1024", "auto"]] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
