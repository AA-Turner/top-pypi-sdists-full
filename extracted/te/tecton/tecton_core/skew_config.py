import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class SkewConfig:
    """
    Define a config used to provide control over online/offline skew during offline retrieval queries (get_features_for_events, get_features_in_range).
    All defaults in SkewConfig are set to minimize online/offline skew.

    :param simulate_events_published_on_time: If True, pretend late data arrived on time by treating batch_publish_timestamp = event_timestamp for all events. If False, take into account the batch_publish_timestamp when calculating features in order to accurately mimic serving behavior. defaults to False
    :param simulate_offline_store_materialized_until: If set, pretend that the offline store is only materialized up to this time. Can be used to improve performance of offline retrieval queries when simulate_events_published_on_time = True. defaults to None.
    """

    simulate_events_published_on_time: bool = False
    simulate_offline_store_materialized_until: Optional[datetime.datetime] = None
