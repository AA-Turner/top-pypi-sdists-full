from __future__ import annotations

from chalk._validation.validation import Validation
from chalk._version import __version__
from chalk.features import (
    Cron,
    DataFrame,
    Environments,
    Features,
    FeatureTime,
    Primary,
    Tags,
    after,
    before,
    description,
    embed,
    feature,
    has_many,
    has_one,
    is_primary,
    op,
    owner,
    tags,
)
from chalk.features._document import Document
from chalk.features._last import Last
from chalk.features.filter import freeze_time
from chalk.features.pseudofeatures import Distance, Now
from chalk.features.resolver import OfflineResolver, OnlineResolver, Resolver, offline, online
from chalk.features.tag import BranchId, EnvironmentId
from chalk.features.underscore import _, __, underscore
from chalk.importer import get_resolver
from chalk.logging import chalk_logger
from chalk.operators import StaticOperator, scan_parquet
from chalk.prompts import Prompt, completion, run_prompt
from chalk.queries.named_query import NamedQuery
from chalk.queries.query_context import ChalkContext
from chalk.queries.scheduled_query import ScheduledQuery
from chalk.sql import make_sql_file_resolver
from chalk.state import State
from chalk.streams import MaterializationWindowConfig, Windowed, group_by_windowed, stream, windowed
from chalk.utils import AnyDataclass
from chalk.utils.duration import CronTab, Duration, ScheduleOptions
from chalk.utils.json import JSON

batch = offline
realtime = online
embedding = embed

__all__ = (
    "AnyDataclass",
    "BranchId",
    "ChalkContext",
    "Cron",
    "CronTab",
    "DataFrame",
    "Distance",
    "Document",
    "Duration",
    "EnvironmentId",
    "Environments",
    "FeatureTime",
    "Features",
    "JSON",
    "Last",
    "MaterializationWindowConfig",
    "NamedQuery",
    "Now",
    "OfflineResolver",
    "OnlineResolver",
    "Primary",
    "Prompt",
    "Resolver",
    "ScheduleOptions",
    "ScheduledQuery",
    "State",
    "StaticOperator",
    "Tags",
    "Validation",
    "Windowed",
    "_",
    "__",
    "__version__",
    "after",
    "batch",
    "before",
    "chalk_logger",
    "completion",
    "description",
    "embed",
    "embedding",
    "feature",
    "freeze_time",
    "get_resolver",
    "group_by_windowed",
    "has_many",
    "has_one",
    "is_primary",
    "make_sql_file_resolver",
    "offline",
    "online",
    "op",
    "owner",
    "realtime",
    "run_prompt",
    "scan_parquet",
    "stream",
    "tags",
    "underscore",
    "windowed",
)
