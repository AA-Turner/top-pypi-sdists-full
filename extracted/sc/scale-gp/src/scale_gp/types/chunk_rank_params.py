# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .shared_params.chunk import Chunk

__all__ = [
    "ChunkRankParams",
    "RankStrategy",
    "RankStrategyCrossEncoderRankStrategy",
    "RankStrategyCrossEncoderRankStrategyParams",
    "RankStrategyRougeRankStrategy",
    "RankStrategyRougeRankStrategyParams",
    "RankStrategyModelRankStrategy",
    "RankStrategyModelRankStrategyParams",
    "RankStrategyAzureAIFoundryRankStrategy",
    "RankStrategyAzureAIFoundryRankStrategyParams",
]


class ChunkRankParams(TypedDict, total=False):
    query: Required[str]
    """Natural language query to re-rank chunks against.

    If a vector store query was originally used to retrieve these chunks, please use
    the same query for this ranking
    """

    rank_strategy: Required[RankStrategy]
    """The ranking strategy to use.

    Rank strategies determine how the ranking is done, They consist of the ranking
    method name and additional params needed to compute the ranking.

    Use the built-in `cross_encoder` or `rouge` strategies or create a custom one
    with the Models API.
    """

    relevant_chunks: Required[Iterable[Chunk]]
    """List of chunks to rank"""

    account_id: str
    """Account to rank chunks with.

    If you have access to more than one account, you must specify an account_id
    """

    top_k: int
    """Number of chunks to return.

    Must be greater than 0 if specified. If not specified, all chunks will be
    returned.
    """


class RankStrategyCrossEncoderRankStrategyParams(TypedDict, total=False):
    """The parameters needed for ranking."""

    cross_encoder_model: Literal[
        "cross-encoder/ms-marco-MiniLM-L-12-v2",
        "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1",
        "Qwen/Qwen3-Reranker-0.6B",
        "Qwen/Qwen3-Reranker-4B",
        "Qwen/Qwen3-Reranker-8B",
    ]
    """Cross encoder model to use when ranking.

    Supports
    [cross-encoder/ms-marco-MiniLM-L-12-v2](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-12-v2),
    [cross-encoder/mmarco-mMiniLMv2-L12-H384-v1](https://huggingface.co/cross-encoder/mmarco-mMiniLMv2-L12-H384-v1),
    [Qwen/Qwen3-Reranker-0.6B](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B),
    [Qwen/Qwen3-Reranker-4B](https://huggingface.co/Qwen/Qwen3-Reranker-4B), and
    [Qwen/Qwen3-Reranker-8B](https://huggingface.co/Qwen/Qwen3-Reranker-8B).
    """


class RankStrategyCrossEncoderRankStrategy(TypedDict, total=False):
    method: Literal["cross_encoder"]
    """The name of the rank strategy. Must be `cross_encoder`."""

    params: RankStrategyCrossEncoderRankStrategyParams
    """The parameters needed for ranking."""


class RankStrategyRougeRankStrategyParams(TypedDict, total=False):
    """The parameters needed for ranking."""

    metric: str
    """Rouge type, can be n-gram based (e.g.

    rouge1, rouge2) or longest common subsequence (rougeL or rougeLsum)
    """

    score: Literal["precision", "recall", "fmeasure"]
    """Metric to use from Rouge score"""


class RankStrategyRougeRankStrategy(TypedDict, total=False):
    method: Literal["rouge"]
    """The name of the rank strategy."""

    params: RankStrategyRougeRankStrategyParams
    """The parameters needed for ranking."""


class RankStrategyModelRankStrategyParams(TypedDict, total=False):
    """The parameters needed for ranking."""

    base_model_name: str
    """The name of a base model to use for reranking"""

    model_deployment_id: str
    """The model deployment id of a custom model to use for reranking"""

    model_params: Dict[str, object]


class RankStrategyModelRankStrategy(TypedDict, total=False):
    method: Literal["model"]
    """Use a model from Models API for ranking."""

    params: RankStrategyModelRankStrategyParams
    """The parameters needed for ranking."""


class RankStrategyAzureAIFoundryRankStrategyParams(TypedDict, total=False):
    """The parameters needed for ranking."""

    endpoint_api_key: Required[str]
    """Azure AI Foundry Endpoint API key to use for reranking."""

    endpoint_url: Required[str]
    """Azure AI Foundry model endpoint to use for reranking.

    Example url:
    https://cohere-rerank-v3-multilingual-xyz.eastus.models.ai.azure.com/v2/rerank
    """


class RankStrategyAzureAIFoundryRankStrategy(TypedDict, total=False):
    params: Required[RankStrategyAzureAIFoundryRankStrategyParams]
    """The parameters needed for ranking."""

    method: Literal["azure_ai_foundry"]
    """Use a model from Azure AI Foundry for ranking."""


RankStrategy: TypeAlias = Union[
    RankStrategyCrossEncoderRankStrategy,
    RankStrategyRougeRankStrategy,
    RankStrategyModelRankStrategy,
    RankStrategyAzureAIFoundryRankStrategy,
]
