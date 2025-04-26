from datetime import datetime
from typing import Any

from typing_extensions import Annotated

from chalk.features.feature_field import Feature
from chalk.features.feature_wrapper import unwrap_feature

FeatureTime = Annotated[datetime, "__chalk_ts__"]
"""Marker for a feature time.

See https://docs.chalk.ai/docs/time for more details on feature time.

Examples
--------
>>> from chalk.features import features
>>> from chalk import FeatureTime
>>> @features
... class User:
...     id: str
...     updated_at: FeatureTime
"""


def feature_time() -> Any:
    """Declare a feature time (deprecated).
    Prefer to use the `FeatureTime` marker.
    See https://docs.chalk.ai/docs/time for more details on `FeatureTime`.

    Examples
    --------
    >>> from chalk.features import features
    >>> from chalk.features import feature_time
    >>> @features
    ... class User:
    ...     updated_at: datetime = feature_time()
    """
    return Feature(typ=datetime, is_feature_time=True)


def is_feature_time(f: Any) -> bool:
    """Determine whether a feature is a feature time.
    See https://docs.chalk.ai/docs/time for more details on `FeatureTime`.

    Parameters
    ----------
    f
        A feature (i.e. `User.ts`)

    Returns
    -------
    bool
        `True` if the feature is a `FeatureTime` and `False` otherwise.

    Examples
    --------
    >>> from chalk.features import features
    >>> @features
    ... class User:
    ...     id: str
    ...     updated_at: datetime = feature_time()
    >>> assert is_feature_time(User.updated_at) is True
    >>> assert is_feature_time(User.id) is False
    """
    return unwrap_feature(f).is_feature_time
