"""Creates STAC collections and items for Met Office deterministic forecast data."""

import datetime
import importlib.resources
import json
from collections import defaultdict
from typing import Any, Sequence, cast

import shapely.geometry
from pystac import (
    Asset,
    Collection,
    Item,
    Link,
    Provider,
    ProviderRole,
)

from .constants import DESCRIPTIONS, KEYWORDS, TITLES, Model, Theme
from .href import Href


def create_collection(model: Model, theme: Theme) -> Collection:
    """Creates a STAC collection for a model and theme combination.

    Args:
        model: The Met Office model (global or UK).
        theme: The theme (height, pressure-level, near-surface, or whole-atmosphere).

    Returns:
        A STAC Collection object configured for the model and theme.
    """
    collection = Collection(
        id=model.get_collection_id(theme),
        description=DESCRIPTIONS[model][theme],
        title=TITLES[model][theme],
        license="CC-BY-SA-4.0",
        keywords=["MetOffice"] + KEYWORDS[model][theme],
        providers=[
            Provider(
                url="https://www.metoffice.gov.uk/",
                name="Met Office",
                roles=[
                    ProviderRole.PRODUCER,
                    ProviderRole.LICENSOR,
                    ProviderRole.PROCESSOR,
                ],
            ),
        ],
        extent=model.extent,
        stac_extensions=[
            "https://stac-extensions.github.io/storage/v1.0.0/schema.json",
            "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
        ],
        extra_fields={
            "storage:schemes": {
                "aws": {
                    "type": "aws-s3",
                    "platform": "https://{bucket}.s3.{region}.amazonaws.com",
                    "bucket": "met-office-atmospheric-model-data",
                    "region": "eu-west-2",
                    "requester_pays": False,
                }
            },
            "auth:schemes": {"aws": {"type": "s3"}},
        },
    )
    collection.links = [
        Link(
            rel="license",
            target="https://creativecommons.org/licenses/by-sa/4.0/deed.en",
            media_type="text/html",
            title="Creative Commons Attribution-ShareAlike 4.0",
        ),
        Link(
            rel="describedby",
            target="https://www.metoffice.gov.uk/services/data/external-data-channels",
            title="Met Office Dataset Documentation",
        ),
    ]
    return collection


def create_items(
    source_hrefs: Sequence[str | Href],
    model: Model | None = None,
    theme: Theme | None = None,
) -> list[Item]:
    """Creates one or more STAC items from a sequence of hrefs.

    Groups hrefs by collection and item ID, then creates STAC items with assets
    for each unique combination of valid time and forecast horizon.

    Args:
        source_hrefs: A sequence of href strings or Href objects pointing to
            NetCDF forecast files.
        model: Optional model to override automatic detection from hrefs.
        theme: Optional theme to override automatic detection from hrefs.

    Returns:
        A list of STAC Item objects, one for each unique combination of
        valid time and forecast horizon.
    """
    hrefs: defaultdict[str, defaultdict[str, list[Href]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for source_href in source_hrefs:
        if isinstance(source_href, Href):
            href = source_href
        else:
            href = Href.parse(source_href, model=model, theme=theme)
        hrefs[href.collection_id][href.item_id].append(href)
    items = list()
    for items_hrefs in hrefs.values():
        for item_id, item_hrefs in items_hrefs.items():
            items.append(_create_item(item_id, item_hrefs))
    return items


def _create_item(
    item_id: str,
    hrefs: list[Href],
) -> Item:
    assert hrefs
    href = hrefs[0]
    item = Item(
        id=item_id,
        datetime=href.datetime,
        bbox=list(href.model.bbox),
        geometry=href.model.geometry,
        stac_extensions=[
            "https://stac-extensions.github.io/forecast/v0.2.0/schema.json",
        ],
        properties={
            "forecast:reference_datetime": datetime.datetime.strptime(
                href.reference_datetime, "%Y%m%dT%H%MZ"
            ).isoformat()
            + "Z",
            "forecast:horizon": href.forecast_horizon,
            "met_office_deterministic:model": href.model,
            "met_office_deterministic:theme": href.theme,
        },
        assets=dict(_create_asset(href) for href in hrefs),
    )
    item.ext.add("proj")
    item.ext.proj.wkt2 = href.model.proj_wkt2
    if href.model == Model.uk:
        item.ext.proj.geometry = shapely.geometry.mapping(
            shapely.geometry.box(-1159000.0, -1037000.0, 925000.0, 903000.0)
        )
    return item


def _create_asset(href: Href) -> tuple[str, Asset]:
    extra_fields = {}
    if variable := href.variable:
        extra_fields["forecast:variable"] = variable
    if href.duration:
        extra_fields["forecast:duration"] = href.duration
    item_assets = _get_item_assets(href.model, href.theme)
    asset_dict = item_assets[href.parameter]
    asset_dict["href"] = str(href)
    asset = Asset.from_dict(asset_dict)
    asset.extra_fields = extra_fields
    return (href.parameter, asset)


def _get_item_assets(model: Model, theme: Theme) -> dict[str, dict[str, Any]]:
    file_name = f"{model.value}-{theme.value}.json"
    item_assets_path = importlib.resources.files(
        "stactools.met_office_deterministic.item_assets"
    ).joinpath(file_name)
    with item_assets_path.open() as f:
        return cast(dict[str, dict[str, Any]], json.load(f))
