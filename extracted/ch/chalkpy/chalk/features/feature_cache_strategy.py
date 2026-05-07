from typing import Union, Literal, Optional
from enum import Enum

CacheNullsType = Union[bool, Literal["evict_nulls"]]
CacheDefaultsType = Union[bool, Literal["evict_defaults"]]

class CacheStrategy(Enum):
    """Strategy that preserves whether None was passed"""
    ALL = "all"
    ALL_WITH_NULLS_UNSET = "all_with_nulls_unset"  # None, True
    ALL_WITH_DEFAULTS_UNSET = "all_with_defaults_unset"  # True, None
    ALL_WITH_BOTH_UNSET = "all_with_both_unset"  # None, None
    NO_NULLS = "no_nulls"
    NO_NULLS_WITH_DEFAULTS_UNSET = "no_nulls_with_defaults_unset"  # False, None
    NO_DEFAULTS = "no_defaults"
    NO_DEFAULTS_WITH_NULLS_UNSET = "no_defaults_with_nulls_unset"  # None, False
    NO_NULLS_OR_DEFAULTS = "no_nulls_or_defaults"
    EVICT_NULLS = "evict_nulls"
    EVICT_NULLS_WITH_DEFAULTS_UNSET = "evict_nulls_with_defaults_unset"  # "evict_nulls", None
    EVICT_DEFAULTS = "evict_defaults"
    EVICT_DEFAULTS_WITH_NULLS_UNSET = "evict_defaults_with_nulls_unset"  # None, "evict_defaults"
    EVICT_NULLS_AND_DEFAULTS = "evict_nulls_and_defaults"

def get_cache_strategy_from_cache_settings(
        cache_nulls: Optional[CacheNullsType],
        cache_defaults: Optional[CacheDefaultsType],
) -> CacheStrategy:
    if cache_nulls == "evict_nulls":
        if cache_defaults == "evict_defaults":
            return CacheStrategy.EVICT_NULLS_AND_DEFAULTS
        elif cache_defaults is False:
            raise ValueError(
                'Cannot evict nulls and not cache defaults. Did you mean to set `cache_nulls=False` or `cache_defaults="evict_defaults"`?'
            )
        elif cache_defaults is True:
            return CacheStrategy.EVICT_NULLS
        elif cache_defaults is None:
            return CacheStrategy.EVICT_NULLS_WITH_DEFAULTS_UNSET
        else:
            raise ValueError(f'Expected value of cache_defaults to be True, False, None, or "evict_defaults". Received {cache_defaults}')

    elif cache_nulls is False:
        if cache_defaults == "evict_defaults":
            raise ValueError(
                'Cannot evict defaults and not cache nulls. Did you mean to set `cache_defaults=False` or `cache_nulls="evict_nulls"`?'
            )
        elif cache_defaults is False:
            return CacheStrategy.NO_NULLS_OR_DEFAULTS
        elif cache_defaults is True:
            return CacheStrategy.NO_NULLS
        elif cache_defaults is None:
            return CacheStrategy.NO_NULLS_WITH_DEFAULTS_UNSET
        else:
            raise ValueError(f'Expected value of cache_defaults to be True, False, None, or "evict_defaults". Received {cache_defaults}')

    elif cache_nulls is True or cache_nulls is None:
        if cache_defaults == "evict_defaults":
            if cache_nulls is None:
                return CacheStrategy.EVICT_DEFAULTS_WITH_NULLS_UNSET
            else:
                return CacheStrategy.EVICT_DEFAULTS
        elif cache_defaults is False:
            if cache_nulls is None:
                return CacheStrategy.NO_DEFAULTS_WITH_NULLS_UNSET
            else:
                return CacheStrategy.NO_DEFAULTS
        elif cache_defaults is True:
            if cache_nulls is None:
                return CacheStrategy.ALL_WITH_NULLS_UNSET
            else:
                return CacheStrategy.ALL
        elif cache_defaults is None:
            if cache_nulls is None:
                return CacheStrategy.ALL_WITH_BOTH_UNSET
            else:
                return CacheStrategy.ALL_WITH_DEFAULTS_UNSET
        else:
            raise ValueError(f'Expected value of cache_defaults to be True, False, None, or "evict_defaults". Received {cache_defaults}')

    else:
        raise ValueError(f'Expected value of cache_nulls to be True, False, None, or "evict_nulls". Received {cache_nulls}')


def get_cache_settings_from_strategy(
        cache_strategy: CacheStrategy,
) -> tuple[Optional[CacheNullsType], Optional[CacheDefaultsType]]:

    mapping: dict[CacheStrategy, tuple[Optional[CacheNullsType], Optional[CacheDefaultsType]]] = {
        CacheStrategy.ALL: (True, True),
        CacheStrategy.ALL_WITH_NULLS_UNSET: (None, True),
        CacheStrategy.ALL_WITH_DEFAULTS_UNSET: (True, None),
        CacheStrategy.ALL_WITH_BOTH_UNSET: (None, None),
        CacheStrategy.NO_NULLS: (False, True),
        CacheStrategy.NO_NULLS_WITH_DEFAULTS_UNSET: (False, None),
        CacheStrategy.NO_DEFAULTS: (True, False),
        CacheStrategy.NO_DEFAULTS_WITH_NULLS_UNSET: (None, False),
        CacheStrategy.NO_NULLS_OR_DEFAULTS: (False, False),
        CacheStrategy.EVICT_NULLS: ("evict_nulls", True),
        CacheStrategy.EVICT_NULLS_WITH_DEFAULTS_UNSET: ("evict_nulls", None),
        CacheStrategy.EVICT_DEFAULTS: (True, "evict_defaults"),
        CacheStrategy.EVICT_DEFAULTS_WITH_NULLS_UNSET: (None, "evict_defaults"),
        CacheStrategy.EVICT_NULLS_AND_DEFAULTS: ("evict_nulls", "evict_defaults"),
    }

    return mapping[cache_strategy]