from eumdac.tailor_models import RegionOfInterest, Filter, Quicklook
from eumdac.cli import json_clean_unwrap, json_to_yaml


def test_json_clean_unwrap():
    # Chain that includes all types
    chain_dic = {
        "id": "test_chain",
        "product": "HRSEVIRI",
        "format": "geotiff",
        "name": "test_chain",
        "description": "",
        "aggregation": None,
        "projection": "mercator",
        "roi": RegionOfInterest(id=None, name=None, NSWE=[54, 47, 6, 15], description=None),
        "filter": Filter(
            id=None, bands=["channel_3", "channel_2", "channel_1"], name=None, product=None
        ),
        "quicklook": Quicklook(
            id=None,
            name=None,
            resample_method=None,
            stretch_method="min_max",
            product=None,
            format="png_rgb",
            nodatacolor=None,
            filter=Filter(
                id=None, bands=["channel_3", "channel_2", "channel_1"], name=None, product=None
            ),
            x_size=None,
            y_size=None,
        ),
        "resample_method": "bilinear",
        "resample_resolution": [500, 500],
        "compression": {"format": "zip"},
        "xrit_segments": None,
    }
    output = json_clean_unwrap(chain_dic)
    expected = {
        "id": "test_chain",
        "product": "HRSEVIRI",
        "format": "geotiff",
        "name": "test_chain",
        "description": "",
        "projection": "mercator",
        "roi": {"NSWE": [54, 47, 6, 15]},
        "filter": {"bands": ["channel_3", "channel_2", "channel_1"]},
        "quicklook": {
            "stretch_method": "min_max",
            "format": "png_rgb",
            "filter": {"bands": ["channel_3", "channel_2", "channel_1"]},
        },
        "resample_method": "bilinear",
        "resample_resolution": [500, 500],
        "compression": {"format": "zip"},
    }
    assert output == expected


def test_json_to_yaml():
    chain_dic = {
        "id": "test_chain",
        "product": "HRSEVIRI",
        "format": "geotiff",
        "name": "Test Chain",
        "roi": {"NSWE": [42, 36, -9, -7]},
    }
    output = json_to_yaml(chain_dic)
    expected = "id: test_chain, product: HRSEVIRI, format: geotiff, name: Test Chain, roi: {NSWE: [42, 36, -9, -7]}"
    assert output == expected
