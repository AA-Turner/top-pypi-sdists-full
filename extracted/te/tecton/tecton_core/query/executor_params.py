from enum import Enum
from typing import Iterable
from typing import Optional

import attrs

from tecton_core.duckdb_factory import DuckDBConfig
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_core.offline_store import OfflineStoreOptionsProvider
from tecton_core.secret_management import SecretResolver


class QueryTreeStep(Enum):
    """Query trees are composed of steps.

    Each step may have its own compute, and may stage its results in preparation for the next step.

    Query trees do not have to have all steps. For example, a materialization query tree for a batch feature view will
    not have any nodes in the ODFV step.
    """

    # Runs data source scans.
    DATA_SOURCE = 1
    # Runs feature view transformations to produce un-aggregated feature data.
    PIPELINE = 2
    # Runs model inference (only used by text embeddings right now).
    MODEL_INFERENCE = 3
    # Runs partial aggregations, full aggregations, and the as-of join.
    AGGREGATION = 4
    # Runs on-demand transformations.
    ODFV = 5
    # Scans the offline store node.
    OFFLINE_STORE = 6


@attrs.frozen
class ExecutionContext:
    offline_store_options_providers: Iterable[OfflineStoreOptionsProvider]
    secret_resolver: Optional[SecretResolver] = None
    model_artifact_provider: Optional[ModelArtifactProvider] = None
    duckdb_config: Optional[DuckDBConfig] = None
