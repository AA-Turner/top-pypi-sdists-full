import inspect
from ast import parse
from importlib.util import module_from_spec, spec_from_file_location
from itertools import chain
from traceback import format_exc
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Union, get_args
from uuid import UUID

from galileo_core.exceptions.execution import ExecutionError
from galileo_core.helpers.logger import logger
from galileo_core.schemas.shared.metric import UserMetricType
from galileo_core.schemas.shared.scorers.base_configs import ScoreType
from galileo_core.schemas.shared.scorers.chain_aggregation import ChainAggregationStrategy
from galileo_core.schemas.shared.workflows.node_type import NodeType

DEFAULT_SCOREABLE_NODE_TYPES: List[NodeType] = [NodeType.llm, NodeType.chat]
SCORER_FN_REQUIRED_ARGS = ["kwargs"]
AGGREGATOR_FN_REQUIRED_ARGS = ["scores"]


def default_scorer_fn(*, index: Union[int, UUID], **kwargs: Any) -> UserMetricType:
    """
    Default scorer function that is used when the user-registered scorer does not provide a scorer function.

    All args are keyword-only.

    Parameters
    ----------
    index : Union[int, UUID]
        Index of the node.

    Returns
    -------
    UserMetricType
        Score.
    """
    return None


def default_aggregator_fn(*, scores: List[UserMetricType], **kwargs: Any) -> Dict[str, UserMetricType]:
    """
    Default aggregator function that is used when the user-registered scorer does not provide an aggregator function.

    All args are keyword-only.

    Parameters
    ----------
    scores : List[UserMetricType]
        List of scores from the scorer function.

    Returns
    -------
    Dict[str, Any]
        Aggregated scores.
    """
    return dict()


def validate_registered_scorer(file_path: str, extra: dict, exec_module: bool = True) -> ModuleType:
    """
    Validate the registered scorer file.

    Args:
        file_path: The path to the registered scorer Python file.
        extra: Extra information to log.

    Returns:
        The module object of the registered scorer file.

    Raises:
        ExecutionError:
            If the scorer file contains invalid Python code or if the scorer function is not found.
    """
    with open(file_path) as open_file:
        try:
            content = open_file.read()

            parse(content)
        except SyntaxError as exception:
            raise ExecutionError(
                f"Invalid Python code in scorer file. SyntaxError when parsing: {exception.msg}.", extra
            )

    spec = spec_from_file_location("scorer", file_path)
    if spec is None or spec.loader is None:
        raise ExecutionError("Error loading registered scorer module spec.", extra)
    user_module = module_from_spec(spec)

    if exec_module:  # Allow this to be turned off (for G2.0 sandbox mode)
        try:
            spec.loader.exec_module(user_module)
        except Exception:
            raise ExecutionError(f"Error while loading your custom metric code: \n\n {format_exc(chain=False)}.", extra)

    if scorer_fn := getattr(user_module, "scorer_fn", None):
        if not callable(scorer_fn):
            raise ExecutionError("scorer_fn must be a function.", extra)

    logger.info("Successfully validated scorer file.", extra=extra)
    return user_module


def validate_score_type_fn(user_module: ModuleType, extra: dict) -> type:
    """
    Validate the score_type function in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        extra: Extra information to log.

    Returns:
        The score type returned by the score_type function.

    Raises:
        ExecutionError: If the score_type function is not a function or does not return a valid score type.
    """
    if score_type_fn := getattr(user_module, "score_type", None):
        if not callable(score_type_fn):
            raise ExecutionError("score_type must be a function.", extra)

        score_type = score_type_fn()
        if score_type not in get_args(ScoreType):
            raise ExecutionError(f"score_type must return one of {get_args(ScoreType)}.", extra)

        return score_type

    return float


def validate_scoreable_node_types_fn(user_module: ModuleType, extra: dict) -> List[NodeType]:
    """
    Validate the scoreable_node_types function in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        extra: Extra information to log.

    Returns:
        The list of scorable node types returned by the scoreable_node_types function.

    Raises:
        ExecutionError:
            If the scoreable_node_types function is not a function
            or does not return a valid list of scorable node types.
    """
    if scoreable_node_types_fn := getattr(user_module, "scoreable_node_types_fn", None):
        if not callable(scoreable_node_types_fn):
            raise ExecutionError("scoreable_node_types_fn must be a function.", extra)

        scoreable_node_types = scoreable_node_types_fn()
        if not isinstance(scoreable_node_types, list):
            raise ExecutionError("scoreable_node_types_fn must return a list.", extra)

        for value in scoreable_node_types:
            if value not in NodeType.__members__:
                raise ExecutionError(
                    f"Node type {value} is invalid. Must be one of {', '.join(NodeType.__members__.keys())}.", extra
                )

        return scoreable_node_types

    return DEFAULT_SCOREABLE_NODE_TYPES


def validate_include_llm_credentials(user_module: ModuleType, extra: dict) -> bool:
    """
    Validate the include_llm_credentials function in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        extra: Extra information to log.

    Returns:
        The value returned by the include_llm_credentials function.

    Raises:
        ExecutionError: If the include_llm_credentials is not a boolean.
    """
    if include_llm_credentials := getattr(user_module, "include_llm_credentials", False):
        if not isinstance(include_llm_credentials, bool):
            raise ExecutionError("include_llm_credentials must be a boolean.", extra)
    return include_llm_credentials or False


def validate_chain_aggregation(
    user_module: ModuleType, score_type: type, extra: dict
) -> Optional[ChainAggregationStrategy]:
    """
    Validate the chain_aggregation strategy in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        score_type: The score type returned by the score_type function.
        Used to determine the default chain aggregation strategy if not provided.
        extra: Extra information to log.

    Returns:
        The value returned by the chain_aggregation strategy.

    Raises:
        ExecutionError: If the chain_aggregation is not a string or is an invalid string.
    """
    if chain_aggregation := getattr(user_module, "chain_aggregation", None):
        if not isinstance(chain_aggregation, str):
            raise ExecutionError("chain_aggregation must be a string.", extra)
        chain_aggregation = chain_aggregation.lower()
        if chain_aggregation not in chain.from_iterable(
            [strategy, strategy.name, strategy.value] for strategy in ChainAggregationStrategy
        ):
            raise ExecutionError("chain_aggregation is not a valid strategy.", extra)
        return ChainAggregationStrategy(chain_aggregation)
    if score_type in (int, float, bool):
        return ChainAggregationStrategy.average
    return None


def validate_scorer_fn(user_module: ModuleType, extra: dict) -> Optional[Callable]:
    """
    Validate the scorer_fn function in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        extra: Extra information to log.

    Raises:
        ExecutionError: If the scorer_fn function is not a function or does
        not have the required arguments.
    """
    if scorer_fn := getattr(user_module, "scorer_fn", None):
        if not callable(scorer_fn):
            raise ExecutionError("scorer_fn must be a function.", extra)

        params = inspect.signature(scorer_fn).parameters

        for arg in SCORER_FN_REQUIRED_ARGS:
            if arg not in params:
                raise ExecutionError(f"scorer_fn must have the argument '{arg}'.", extra)

        return scorer_fn

    return None


def validate_aggregator_fn(user_module: ModuleType, extra: dict) -> Optional[Callable]:
    """
    Validate the aggregator_fn function in the registered scorer file.

    Args:
        user_module: The module object of the registered scorer file.
        extra: Extra information to log.

    Raises:
        ExecutionError: If the aggregator_fn function is not a function or
        does not have the required arguments.
    """
    if aggregator_fn := getattr(user_module, "aggregator_fn", None):
        if not callable(aggregator_fn):
            raise ExecutionError("aggregator_fn must be a function.", extra)

        params = inspect.signature(aggregator_fn).parameters

        for arg in AGGREGATOR_FN_REQUIRED_ARGS:
            if arg not in params:
                raise ExecutionError(f"aggregator_fn must have the argument '{arg}'.", extra)

        return aggregator_fn

    return None


def validate_node_type_input(
    scorer_fn: Callable, node_type: NodeType, expected_score_type: type, data: dict, extra: dict
) -> Optional[ScoreType]:
    """
    Test the scorer_fn function by running it with sample input data.

    Args:
        scorer_fn: The scorer function to test.
        node_type: The node type to test the scorer function with.
        expected_score_type: The expected score type.
        data: The input data to test the scorer function with.
        extra: Extra information to log.

    Returns:
        The score type returned by the scorer function.

    Raises:
        ExecutionError: If the scorer function raises an error.
    """

    try:
        score = scorer_fn(node_type=node_type, **data)
    except Exception as e:
        msg = f"Error running scorer function on node type '{node_type.name}': {e}"
        logger.error(msg, exc_info=True)
        raise ExecutionError(msg, extra)

    try:
        return coerce_type(score, expected_score_type)
    except ExecutionError as e:
        msg = f"Error running scorer function on node type '{node_type.name}': {e}"
        logger.error(msg, exc_info=True)
        raise ExecutionError(msg, extra)


def coerce_type(value: Any, expected_score_type: type) -> Optional[ScoreType]:
    """
    Coerce the value to the expected type.

    Parameters
    ----------
    value : Any
        Value to coerce.
    expected_score_type : Type
        Expected type.

    Returns
    -------
    UserMetricType
        Coerced value.

    Raises
    ------
    ExecutionError
        If the value cannot be coerced.
    """
    if value is None:
        return None

    try:
        return expected_score_type(value)
    except (ValueError, TypeError):
        raise ExecutionError(f"Failed to coerce value '{value}' to type {expected_score_type.__name__}.")
