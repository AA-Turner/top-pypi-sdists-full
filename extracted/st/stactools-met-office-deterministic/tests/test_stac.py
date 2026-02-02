import datetime

import pytest
from pystac import Item

from stactools.met_office_deterministic import stac
from stactools.met_office_deterministic.constants import Model, Theme


@pytest.mark.parametrize(
    "theme",
    (Theme.height, Theme.pressure_level, Theme.near_surface, Theme.whole_atmosphere),
)
@pytest.mark.parametrize("model", (Model.global_, Model.uk))
def test_collection(model: Model, theme: Theme) -> None:
    collection = stac.create_collection(model, theme)
    assert collection.title
    assert len(collection.links) == 2

    license_link = next(link for link in collection.links if link.rel == "license")
    assert license_link.href == "https://creativecommons.org/licenses/by-sa/4.0/deed.en"
    assert license_link.media_type == "text/html"

    describedy_link = next(
        link for link in collection.links if link.rel == "describedby"
    )
    assert (
        describedy_link.href
        == "https://www.metoffice.gov.uk/services/data/external-data-channels"
    )

    collection.validate()


def test_items(items: list[Item]) -> None:
    for item in items:
        datetime.datetime.strptime(
            item.properties["forecast:reference_datetime"], "%Y-%m-%dT%H:%M:%SZ"
        )

        for key, asset in item.assets.items():
            assert asset.roles == ["data"]
            assert asset.media_type == "application/netcdf", "No media type: " + key
            assert asset.title

            if should_have_descriptions(item):
                assert asset.description

        assert item.ext.has("proj")

        item.validate()


def test_forcing_the_items(items: list[Item]) -> None:
    for item in items:
        datetime.datetime.strptime(
            item.properties["forecast:reference_datetime"], "%Y-%m-%dT%H:%M:%SZ"
        )

        for key, asset in item.assets.items():
            assert asset.roles == ["data"]
            assert asset.media_type == "application/netcdf", "No media type: " + key
            assert asset.title

            if should_have_descriptions(item):
                assert asset.description

        item.validate()


def test_forcing_the_collection() -> None:
    items = stac.create_items(
        [
            "https://ukmoeuwest.blob.core.windows.net/staging/global/height/20251202T0600Z/20251203T2100Z-PT0039H00M-cloud_amount_on_height_levels.nc"
        ],
        model=Model.global_,
        theme=Theme.height,
    )
    for item in items:
        assert item.properties["met_office_deterministic:model"] == Model.global_
        assert item.properties["met_office_deterministic:theme"] == Theme.height


def should_have_descriptions(item: Item) -> bool:
    # Temporary helper function while we wait for more descriptions from the met office
    model = item.properties["met_office_deterministic:model"]
    return model == Model.uk or item.properties["met_office_deterministic:theme"] in [
        Theme.near_surface,
    ]


def test_geopotential_height() -> None:
    # https://github.com/stactools-packages/met-office-deterministic/issues/42
    href = "https://ukmoeuwest.blob.core.windows.net/deterministic/global/pressure/20260128T0000Z/20260128T0100Z-PT0001H00M-geopotential_height_on_pressure_levels.nc"
    stac.create_items([href], model=Model.global_)
