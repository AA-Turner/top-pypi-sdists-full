from datetime import datetime
from typing import Optional
from typing import Union

import pandas

from tecton.framework.data_frame import TectonDataFrame
from tecton_athena import sql_helper
from tecton_core.errors import TectonAthenaNotImplementedError
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.time_utils import get_timezone_aware_datetime


TEMP_INPUT_PREFIX = "_TT_TEMP_INPUT_"


def get_historical_features(
    feature_set_config: FeatureSetConfig,
    spine: Optional[Union[pandas.DataFrame, str]] = None,
    timestamp_key: Optional[str] = None,
    include_feature_view_timestamp_columns: bool = False,
    from_source: bool = False,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    entities: Optional[Union[pandas.DataFrame]] = None,
) -> TectonDataFrame:
    if from_source:
        msg = "Retrieving features directly from data sources (i.e. using from_source=True) is not supported with Athena retrieval. Use from_source=False and feature views that have offline materialization enabled."
        raise TectonAthenaNotImplementedError(msg)
    if timestamp_key is None and spine is not None:
        msg = "timestamp_key must be specified"
        raise TectonAthenaNotImplementedError(msg)
    if entities is not None:
        msg = "entities is not supported right now"
        raise TectonAthenaNotImplementedError(msg)
    if spine is not None and (start_time or end_time):
        msg = "If a spine is provided, start_time and end_time must not be provided"
        raise TectonAthenaNotImplementedError(msg)

    start_time = get_timezone_aware_datetime(start_time)
    end_time = get_timezone_aware_datetime(end_time)

    return TectonDataFrame._create(
        sql_helper.get_historical_features(
            spine=spine,
            timestamp_key=timestamp_key,
            feature_set_config=feature_set_config,
            include_feature_view_timestamp_columns=include_feature_view_timestamp_columns,
            start_time=start_time,
            end_time=end_time,
        )
    )
