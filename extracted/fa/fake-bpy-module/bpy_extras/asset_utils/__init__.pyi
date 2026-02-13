"""
Helpers for asset management tasks.

"""

import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

class AssetBrowserPanel:
    """Mixin class for panels that should only show in the asset browser."""

class AssetMetaDataPanel:
    """Mixin class for panels that display asset metadata in the asset browser."""

class SpaceAssetInfo:
    """Utility class for checking if a space is an asset browser."""
