"""YouTube's fixed external origin keeps the shared media wire contract."""

from typing import Literal

import pytest
from pydantic import ValidationError

from matrx_connect.context.media_block import MediaBlockShared, YouTubeBlock


class ExternalMedia(MediaBlockShared[Literal["external"]]):
    origin: Literal["external"] = "external"


def test_fixed_external_origin_keeps_exact_schema_and_validation() -> None:
    value = YouTubeBlock(external_url="https://www.youtube.com/watch?v=example")
    assert value.origin == "external"
    assert YouTubeBlock.model_json_schema()["properties"]["origin"] == {
        "const": "external", "default": "external", "title": "Origin", "type": "string",
    }
    with pytest.raises(ValidationError):
        YouTubeBlock.model_validate({"origin": "matrx", "file_id": "file"})
    with pytest.raises(ValidationError, match="external_url or base64"):
        ExternalMedia()


def test_bare_media_origin_keeps_both_branches_and_file_requirement() -> None:
    assert MediaBlockShared.model_json_schema()["properties"]["origin"] == {
        "enum": ["matrx", "external"], "title": "Origin", "type": "string",
    }
    assert MediaBlockShared(origin="matrx", file_id="file").origin == "matrx"
    assert MediaBlockShared(origin="external", base64="bytes").origin == "external"
    with pytest.raises(ValidationError, match="requires file_id"):
        MediaBlockShared(origin="matrx")
