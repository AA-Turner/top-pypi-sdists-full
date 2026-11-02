"""Napari resources such as logos."""

from __future__ import annotations

# `importlib.resources` is aliased to `_resources`: this package contains a
# subpackage also named `resources`, and importing it would overwrite the plain
# `resources` name on this module (a classic name clash).
from importlib import resources as _resources
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from pathlib import Path

__all__ = ["logo_path", "logo_templates", "logo_variants"]

logos_dir = _resources.files("napari_resources.resources.logos")


def logo_path(variant: str = "gradient", template: str = "plain", mode: Literal["dark", "light"] = "dark") -> Path:
    """Return the path to a generated logo SVG.

    Parameters
    ----------
    variant : str
        One of logo_variants()
    template : str
        One of logo_templates()
    mode : str
        One of `dark` or `light`

    Returns
    -------
    Path
        Path handle to the logo. The generated SVGs are produced at build
        time (see ``hatch_build.py``), so this works for both installed wheels
        and editable installs.

    Raises
    ------
    FileNotFoundError
        If the generated asset is not present, e.g. the package was not built
        (or the working tree is a fresh checkout).
    """
    if variant not in logo_variants():
        raise ValueError(f"variant must be one of {set(logo_variants())}; got '{variant}'")
    if template not in logo_templates():
        raise ValueError(f"template must be one of {set(logo_templates())}; got '{template}'")
    if mode not in ("dark", "light"):
        raise ValueError(f"mode must be either 'light' or 'dark'; got '{mode}'")

    name = f"{variant}-{template}-{mode}"
    resource = logos_dir / "generated" / f"{name}.svg"
    if not resource.is_file():
        raise FileNotFoundError(
            f"Generated logo {name!r} not found at {resource}. "
            "The SVGs are produced at build time; reinstall the package "
            "(e.g. `pip install -e .` or `uv sync --reinstall-package "
            "napari-resources`) or run the generator "
            "(`python -m napari_resources.generate_logos <dest_dir>`) first."
        )
    # materialize traversable to real file system path
    with _resources.as_file(resource) as path:
        return path


def logo_variants() -> list[str]:
    """List the available logo variant names (e.g. ``"gradient"``).

    These are the ``<variant>`` components of generated filenames, e.g.
    ``"gradient-plain-dark.svg"``.
    """
    variants = _resources.files("napari_resources.resources.logos.variants")
    return sorted(p.name.removesuffix(".svg") for p in variants.iterdir() if p.name.endswith(".svg"))


def logo_templates() -> list[str]:
    """List the available logo template names (e.g. ``"plain"``).

    These are the ``<template>`` components of generated filenames, e.g.
    ``"gradient-plain-dark.svg"``.
    """
    templates = _resources.files("napari_resources.resources.logos.templates")
    return sorted(p.name.removesuffix(".svg") for p in templates.iterdir() if p.name.endswith(".svg"))
