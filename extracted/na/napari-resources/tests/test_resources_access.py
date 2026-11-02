import importlib.resources as resources

import pytest

from napari_resources import logo_path, logo_templates, logo_variants

# These tests validate the packaging contract: the generated SVGs must be
# present at runtime, either because they were packaged in the wheel or because
# the build hook generated them during an editable install (`uv sync` /
# `pip install -e .`). If you run pytest from a fresh source checkout without
# installing first, they will fail with a helpful error.


def test_logo_resource_reachable_via_importlib():
    path = resources.files("napari_resources.resources.logos") / "generated" / "gradient-plain-dark.svg"
    assert path.is_file()


def test_logo_path_helper():
    assert logo_path().is_file()
    assert logo_path("flat", "text", "light").is_file()


def test_logo_path_missing_raises():
    with pytest.raises(ValueError):
        logo_path("not", "real", "dark")


def test_logo_variants_and_templates():
    variants = logo_variants()
    templates = logo_templates()
    assert "gradient" in variants
    assert "plain" in templates
    assert variants == sorted(variants)
