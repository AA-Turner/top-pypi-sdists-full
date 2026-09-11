"""Kinds for the image-verification pair: reverse image search + EXIF metadata.

ONE kind per capability, shared by the workflow node and the agent tool — the
precedent set by ``regex_extract_result`` (one shape, both surfaces) rather than
a node kind and a near-identical twin tool kind, which is exactly the
near-duplicate the kind doctrine forbids:

* ``reverse_image_search_results`` — ``web.google.reverse_image_search`` node
  and the ``reverse_image_search`` tool.
* ``image_metadata_report`` — ``image.metadata.read`` node and the
  ``image_metadata`` tool.

Both mirror their node's ``output_schema`` model field-for-field
(``aidream/graph_actions/web/reverse_image.py`` and
``aidream/graph_actions/image/metadata.py``). They live in the package, not in
``aidream/kinds/``, because the TOOL implementations import them and a package
never imports aidream (``scripts/check_package_boundaries.py``).

Family ``media_forensics``: what a file and the open web say about an image,
without anyone drawing a conclusion. Neither kind carries a verdict field on
purpose — "is this photo fake" is a judgement a human or an agent makes from
these facts, and a score field here would launder that judgement into data.

Publish: ``scripts/publish_kind_catalog.py matrx_ai.tools.kinds.media_forensics --apply``.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from pydantic import BaseModel, ConfigDict, Field, JsonValue

# ---------------------------------------------------------------------------
# reverse_image_search_results
# ---------------------------------------------------------------------------


class ReverseImageMatchItem(BaseModel):
    """Mirrors ``ReverseImageMatch`` — closed, because the node normalises each
    engine's payload INTO this shape rather than passing provider keys through."""

    model_config = ConfigDict(extra="forbid")

    match_type: str = Field(
        description="'exact' (the page carries this image) or 'visual' (merely similar)."
    )
    engine: str = Field(description="SerpAPI engine that returned this match.")
    position: int | None = None
    title: str | None = None
    link: str | None = None
    source: str | None = None
    displayed_link: str | None = None
    snippet: str | None = None
    date_text: str | None = Field(default=None, description="Date exactly as Google wrote it.")
    date: str | None = Field(default=None, description="ISO-8601 UTC; null when unparseable.")
    date_is_approximate: bool = False
    thumbnail: str | None = None
    image: str | None = None
    image_width: int | None = None
    image_height: int | None = None


@kind(
    "reverse_image_search_results",
    label="Reverse Image Search Results",
    family="media_forensics",
    example={
        "source_kind": "url",
        "image_url": "https://example.com/suspect-photo.jpg",
        "file_id": None,
        "engines_used": ["google_lens"],
        "exact_matches": [
            {
                "match_type": "exact",
                "engine": "google_lens",
                "position": 1,
                "title": "Fact Check: FAKE Images Illustrate Story Of Bear Carrying Injured Animals",
                "link": "https://example.com/fact-check-bear-images",
                "source": "Example Fact Check",
                "displayed_link": "example.com",
                "snippet": "The images were generated, not photographed.",
                "date_text": "7 hours ago",
                "date": "2026-09-10T07:12:00+00:00",
                "date_is_approximate": True,
                "thumbnail": "https://example.com/thumb.jpg",
                "image": None,
                "image_width": None,
                "image_height": None,
            }
        ],
        "visual_matches": [
            {
                "match_type": "visual",
                "engine": "google_lens",
                "position": 1,
                "title": "Black bear at a wildlife centre",
                "link": "https://example.com/bear-story",
                "source": "Example News",
                "displayed_link": None,
                "snippet": None,
                "date_text": None,
                "date": None,
                "date_is_approximate": False,
                "thumbnail": "https://example.com/bear-thumb.jpg",
                "image": "https://example.com/bear.jpg",
                "image_width": 1200,
                "image_height": 800,
            }
        ],
        "exact_match_count": 1,
        "visual_match_count": 1,
        "earliest_seen": "2026-09-10T07:12:00+00:00",
        "earliest_seen_is_approximate": True,
        "earliest_seen_link": "https://example.com/fact-check-bear-images",
        "earliest_seen_date_text": "7 hours ago",
        "dated_match_count": 1,
        "elapsed_ms": 3120,
    },
)
class ReverseImageSearchResults(KindModel):
    """Where else an image appears online — exact matches and visual matches
    kept apart, with an earliest-seen hint. Output of
    ``web.google.reverse_image_search`` and the ``reverse_image_search`` tool."""

    source_kind: str = Field(description="'url' or 'file_id' — how the caller supplied the image.")
    image_url: str | None = Field(
        default=None,
        description=(
            "The caller's own external image URL. Null for one of our files: the URL "
            "handed to Google there is a short-lived provider handoff, never an identity."
        ),
    )
    file_id: str | None = None
    engines_used: list[str] = Field(default_factory=list)
    exact_matches: list[ReverseImageMatchItem] = Field(
        default_factory=list, description="Pages Google reports as CONTAINING this image."
    )
    visual_matches: list[ReverseImageMatchItem] = Field(
        default_factory=list, description="Visually similar images — leads, not proof."
    )
    exact_match_count: int = 0
    visual_match_count: int = 0
    earliest_seen: str | None = Field(
        default=None, description="ISO-8601 UTC of the oldest dated match. A hint, not a fact."
    )
    earliest_seen_is_approximate: bool = False
    earliest_seen_link: str | None = None
    earliest_seen_date_text: str | None = None
    dated_match_count: int = 0
    elapsed_ms: int = 0


# ---------------------------------------------------------------------------
# image_metadata_report
# ---------------------------------------------------------------------------


class ImageMetadataContainers(BaseModel):
    """Mirrors ``MetadataContainers`` — which metadata blocks the file carries."""

    model_config = ConfigDict(extra="forbid")

    exif: bool
    xmp: bool
    iptc: bool
    icc_profile: bool
    png_text: bool
    comment: bool


@kind(
    "image_metadata_report",
    label="Image Metadata Report",
    family="media_forensics",
    example={
        "file_id": None,
        "image_url": "https://example.com/photo.jpg",
        "format": "JPEG",
        "mime_type": "image/jpeg",
        "width": 4032,
        "height": 3024,
        "color_mode": "RGB",
        "frame_count": 1,
        "camera_make": "Apple",
        "camera_model": "iPhone 15 Pro",
        "lens_model": "iPhone 15 Pro back triple camera 6.765mm f/1.78",
        "software": "17.5.1",
        "artist": None,
        "copyright": None,
        "image_description": None,
        "datetime_original": "2026-03-04T05:06:07",
        "datetime_original_text": "2026:03:04 05:06:07",
        "datetime_digitized": "2026-03-04T05:06:07",
        "datetime_modified": "2026-03-04T05:06:07",
        "orientation": 1,
        "gps_latitude": 37.7749667,
        "gps_longitude": -122.4087,
        "gps_altitude_m": 152.0,
        "gps_timestamp": "2026:03:04",
        "has_exif": True,
        "metadata_stripped": False,
        "stripped_note": "EXIF metadata is present (34 tags).",
        "containers": {
            "exif": True,
            "xmp": True,
            "iptc": False,
            "icc_profile": True,
            "png_text": False,
            "comment": False,
        },
        "tag_count": 34,
        "raw_tags": {"Make": "Apple", "Model": "iPhone 15 Pro", "Orientation": 1},
        "raw_tags_truncated": False,
        "size_bytes": 2841923,
        "elapsed_ms": 84,
    },
)
class ImageMetadataReport(KindModel):
    """What an image file says about itself — camera, capture time, GPS, writing
    software, dimensions, and whether the metadata survived. Output of
    ``image.metadata.read`` and the ``image_metadata`` tool.

    Facts only. There is deliberately no authenticity field: EXIF absence is
    normal on every social network, so a verdict here would be a guess wearing
    a data field's clothes."""

    file_id: str | None = None
    image_url: str | None = None

    format: str | None = None
    mime_type: str | None = None
    width: int
    height: int
    color_mode: str
    frame_count: int = 1

    camera_make: str | None = None
    camera_model: str | None = None
    lens_model: str | None = None
    software: str | None = Field(
        default=None, description="The app that last wrote the file — often the giveaway."
    )
    artist: str | None = None
    copyright: str | None = None
    image_description: str | None = None

    datetime_original: str | None = Field(
        default=None, description="ISO-8601 capture time. Null when absent — never inferred."
    )
    datetime_original_text: str | None = None
    datetime_digitized: str | None = None
    datetime_modified: str | None = None
    orientation: int | None = None

    gps_latitude: float | None = Field(
        default=None, description="Signed decimal degrees; negative is south."
    )
    gps_longitude: float | None = Field(
        default=None, description="Signed decimal degrees; negative is west."
    )
    gps_altitude_m: float | None = None
    gps_timestamp: str | None = None

    has_exif: bool
    metadata_stripped: bool | None = Field(
        default=None,
        description=(
            "True = a format that normally carries EXIF had none. False = EXIF present. "
            "Null = the format does not normally carry EXIF. An observation, never a verdict."
        ),
    )
    stripped_note: str
    containers: ImageMetadataContainers
    tag_count: int = 0
    raw_tags: dict[str, JsonValue] = Field(default_factory=dict)
    raw_tags_truncated: bool = False
    size_bytes: int | None = None
    elapsed_ms: int = 0


MEDIA_FORENSICS_TOOL_RESULT_KINDS: dict[str, type[KindModel]] = {
    "reverse_image_search": ReverseImageSearchResults,
    "image_metadata": ImageMetadataReport,
}


__all__ = [
    "MEDIA_FORENSICS_TOOL_RESULT_KINDS",
    "ImageMetadataContainers",
    "ImageMetadataReport",
    "ReverseImageMatchItem",
    "ReverseImageSearchResults",
]
