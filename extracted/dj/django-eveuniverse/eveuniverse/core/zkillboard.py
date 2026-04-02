"""Generates profile URLs for zKillboard."""

from enum import Enum, auto
from urllib.parse import urljoin


class _Category(Enum):
    ALLIANCE = auto()
    CHARACTER = auto()
    CORPORATION = auto()
    KILLMAIL = auto()
    REGION = auto()
    SOLARSYSTEM = auto()


_BASE_URL = "https://zkillboard.com"


def _build_url(category: _Category, eve_id: int) -> str:
    """URL to profile page for an eve entity."""
    partials = {
        _Category.ALLIANCE: "alliance",
        _Category.CHARACTER: "character",
        _Category.CORPORATION: "corporation",
        _Category.KILLMAIL: "kill",
        _Category.REGION: "region",
        _Category.SOLARSYSTEM: "system",
    }
    try:
        partial = partials[category]
    except KeyError:
        raise ValueError(f"Invalid category: {category}") from None
    return urljoin(_BASE_URL, f"{partial}/{int(eve_id)}/")


def alliance_url(eve_id: int) -> str:
    """url for page about given alliance on zKillboard"""
    return _build_url(_Category.ALLIANCE, eve_id)


def character_url(eve_id: int) -> str:
    """url for page about given character on zKillboard"""
    return _build_url(_Category.CHARACTER, eve_id)


def corporation_url(eve_id: int) -> str:
    """url for page about given corporation on zKillboard"""
    return _build_url(_Category.CORPORATION, eve_id)


def killmail_url(eve_id: int) -> str:
    """url for page about given kill on zKillboard"""
    return _build_url(_Category.KILLMAIL, eve_id)


def region_url(eve_id: int) -> str:
    """url for page about given region on zKillboard"""
    return _build_url(_Category.REGION, eve_id)


def solar_system_url(eve_id: int) -> str:
    """Return zKillboard URL for a solar system."""
    return _build_url(_Category.SOLARSYSTEM, eve_id)
