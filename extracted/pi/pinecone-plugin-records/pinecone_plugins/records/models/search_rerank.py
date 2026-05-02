from typing import NamedTuple, Optional, Dict, Any, List


class SearchRerank(NamedTuple):
    """
    SearchRerank represents a rerank request when searching within a specific namespace.
    """

    model: str
    """
    The name of the [reranking model](https://docs.pinecone.io/guides/inference/understanding-inference#reranking-models) to use.
    Required.
    """

    rank_fields: List[str]
    """
    The fields to use for reranking.
    Required.
    """

    top_n: Optional[int] = None
    """
    The number of top results to return after reranking. Defaults to top_k.
    Optional.
    """

    parameters: Optional[Dict[str, Any]] = None
    """
    Additional model-specific parameters. Refer to the [model guide](https://docs.pinecone.io/guides/inference/understanding-inference#models)
    for available model parameters.
    Optional.
    """

    query: Optional[str] = None
    """
    The query to rerank documents against. If a specific rerank query is specified, it overwrites
    the query input that was provided at the top level.
    """

    def as_dict(self):
        """
        Returns the SearchRerank as a dictionary.
        """
        return self._asdict()
