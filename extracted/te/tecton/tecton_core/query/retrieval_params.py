from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import Optional
from typing import Union

import pandas

from tecton_core import specs
from tecton_core import tecton_pendulum as pendulum
from tecton_core.compute_mode import ComputeMode
from tecton_core.feature_definition_wrapper import FeatureDefinitionWrapper
from tecton_core.feature_set_config import FeatureSetConfig
from tecton_core.mock_context import MockContext
from tecton_core.query.node_interface import NodeRef
from tecton_core.skew_config import SkewConfig


@dataclass
class GetFeaturesForEventsParams:
    fco: Union[specs.FeatureServiceSpec, FeatureDefinitionWrapper]
    events: Union[pandas.DataFrame, str]
    compute_mode: ComputeMode
    timestamp_key: Optional[str] = None
    from_source: Optional[bool] = None
    mock_data_sources: Optional[Dict[str, NodeRef]] = None
    mock_context: Optional[MockContext] = None
    # Only used for batch and stream feature view
    skew_config: Optional[SkewConfig] = None
    # Only used for feature service
    feature_set_config: Optional[FeatureSetConfig] = None

    @property
    def join_keys(self):
        if self.feature_set_config:
            return self.feature_set_config.join_keys

        assert isinstance(self.fco, FeatureDefinitionWrapper)
        return self.fco.join_keys


@dataclass
class GetFeaturesInRangeParams:
    fco: FeatureDefinitionWrapper
    start_time: datetime
    end_time: datetime
    compute_mode: ComputeMode
    entities: Optional[Union[pandas.DataFrame, str]] = None
    max_lookback: Optional[timedelta] = None
    from_source: Optional[bool] = None
    mock_data_sources: Optional[Dict[str, NodeRef]] = None
    mock_context: Optional[MockContext] = None
    # Only used for batch and stream feature view
    skew_config: Optional[SkewConfig] = None

    @property
    def join_keys(self):
        return self.fco.join_keys


@dataclass
class FeatureDataTimeLimits:
    start_time: Optional[pendulum.datetime]
    end_time: Optional[pendulum.datetime]

    @property
    def batch_publish_timestamp_time_limits(self) -> Optional[pendulum.Period]:
        return pendulum.Period(start=self.start_time, end=self.end_time)

    @property
    def event_timestamp_time_limits(self):
        return pendulum.Period(start=self.start_time, end=self.end_time)
