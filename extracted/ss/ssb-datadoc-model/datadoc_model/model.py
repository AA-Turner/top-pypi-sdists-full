"""This module is a backwards compatibility shim, to support `from datadoc_model.model import xxx` formats"""

import warnings

warnings.warn(
    message="datadoc_model.model has been moved to datadoc_model.all_optional.model. Please update imports accordingly. This will be removed in the next major release.",
    category=DeprecationWarning,
    stacklevel=2,
)

from .all_optional.model import *  # noqa: E402, F403
