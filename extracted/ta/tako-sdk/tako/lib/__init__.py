"""Hand-written additions to the Tako SDK.

Never produced by openapi-generator (protected by `.openapi-generator-ignore`
and preserved across regeneration). Houses the `Tako`/`AsyncTako` facade; the
SSE streaming layer will live here too.
"""

from tako.lib.client import AsyncTako, Tako
from tako.lib.dataset import TakoDatasetView
from tako.lib.schema import derive_response_schema
from tako.lib.streaming import (
    AnswerAgentStream,
    AsyncAnswerAgentStream,
    AsyncRetrievalAgentStream,
    RetrievalAgentStream,
)

__all__ = [
    "Tako",
    "AsyncTako",
    "RetrievalAgentStream",
    "AsyncRetrievalAgentStream",
    "AnswerAgentStream",
    "AsyncAnswerAgentStream",
    "derive_response_schema",
    "TakoDatasetView",
]
