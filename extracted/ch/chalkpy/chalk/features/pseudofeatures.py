from datetime import datetime
from typing import List

from chalk.features.feature_field import DUMMY_FEATURE, Feature

__all__ = [
    "CHALK_TS_FEATURE",
    "Now",
    "DUMMY_FEATURE",
    "ID_FEATURE",
    "OBSERVED_AT_FEATURE",
    "REPLACED_OBSERVED_AT_FEATURE",
    "Distance",
    "PSEUDOFEATURES",
    "FQN_OR_NAME_TO_PSEUDOFEATURE",
    "FQN_TO_PSEUDOFEATURE",
    "PSEUDONAMESPACE",
]

PSEUDONAMESPACE = "__chalk__"

CHALK_TS_FEATURE = Feature(
    name="CHALK_TS",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

Now = Feature(
    name="now",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

ID_FEATURE = Feature(
    name="__id__",
    namespace=PSEUDONAMESPACE,
    typ=str,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

OBSERVED_AT_FEATURE = Feature(
    name="__observed_at__",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

REPLACED_OBSERVED_AT_FEATURE = Feature(
    name="__replaced_observed_at__",
    namespace=PSEUDONAMESPACE,
    typ=datetime,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

Distance = Feature(
    name="__distance__",
    namespace=PSEUDONAMESPACE,
    typ=float,
    max_staleness=None,
    etl_offline_to_online=False,
    primary=False,
    is_feature_time=False,
    is_pseudofeature=True,
)

PSEUDOFEATURES: List[Feature] = [
    CHALK_TS_FEATURE,
    DUMMY_FEATURE,
    Distance,
    ID_FEATURE,
    Now,
    OBSERVED_AT_FEATURE,
    REPLACED_OBSERVED_AT_FEATURE,
]

FQN_TO_PSEUDOFEATURE = {f.fqn: f for f in PSEUDOFEATURES}
FQN_OR_NAME_TO_PSEUDOFEATURE = dict(**FQN_TO_PSEUDOFEATURE, **{f.name: f for f in PSEUDOFEATURES})
