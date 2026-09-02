"""Which fields a caller wants back from a scrape, and the filter that applies it.

This lives apart from `service.py` on purpose. `service.py` is the FastAPI/SSE
adapter and hard-imports matrx-connect and the matrx-orm models, so a consumer
that only wants "scrape these URLs and give me text_data + links" — a desktop
client, a CLI, a graph node — could not touch the options shape without pulling
in a DB stack it has no use for. The shape is also the ONE definition of which
keys a scrape result may carry to a caller: a second copy in a client is how
the two ends silently drift.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ScrapeOptions:
    get_organized_data: bool = False
    get_structured_data: bool = False
    get_overview: bool = False
    get_text_data: bool = True
    get_main_image: bool = False
    get_links: bool = False
    get_content_filter_removal_details: bool = False
    include_highlighting_markers: bool = True
    include_media: bool = True
    include_media_links: bool = True
    include_media_description: bool = True
    include_anchors: bool = True
    anchor_size: int = 100


def apply_field_flags(page_dict: dict[str, Any], options: ScrapeOptions) -> dict[str, Any]:
    """Remove fields the caller did not request so we don't waste bandwidth."""
    if not options.get_overview:
        page_dict.pop("overview", None)
    if not options.get_organized_data:
        page_dict.pop("organized_data", None)
    if not options.get_structured_data:
        page_dict.pop("structured_data", None)
    if not options.get_text_data:
        page_dict.pop("text_data", None)
    if not options.get_main_image:
        page_dict.pop("main_image", None)
    if not options.get_links:
        page_dict.pop("links", None)
        # `link_records` is the same evidence with anchor text attached — ONE
        # flag governs both, so a caller that didn't ask for links never pays
        # for up to 2000 anchor rows.
        page_dict.pop("link_records", None)
    if not options.get_content_filter_removal_details:
        page_dict.pop("content_filter_removal_details", None)
        page_dict.pop("noise_remover_removal_details", None)
    return page_dict
