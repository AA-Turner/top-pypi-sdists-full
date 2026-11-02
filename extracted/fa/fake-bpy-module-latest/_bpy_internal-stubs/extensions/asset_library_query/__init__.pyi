import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

def token_from_asset_url(remote_url) -> None:
    """Return the access token of the extension repository an asset library was installed from,
    or None when the library isnt from an extension or the repository doesnt define the token
    for its asset libraries.

    """
