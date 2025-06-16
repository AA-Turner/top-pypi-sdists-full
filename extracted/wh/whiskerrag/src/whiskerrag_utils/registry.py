import importlib
import logging
import os
from enum import Enum
from pathlib import Path
from typing import (
    Callable,
    Dict,
    Generic,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from whiskerrag_types.interface.embed_interface import BaseEmbedding
from whiskerrag_types.interface.llm_interface import BaseLLM
from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.interface.parser_interface import BaseParser
from whiskerrag_types.interface.retriever_interface import BaseRetriever
from whiskerrag_types.model.knowledge import (
    EmbeddingModelEnum,
    KnowledgeSourceEnum,
    KnowledgeTypeEnum,
)

logger = logging.getLogger("whisker")


class RegisterTypeEnum(str, Enum):
    """Register component types for whisker rag flow"""

    DECOMPOSER = "decomposer"
    """Decomposer: Breaks down folder type knowledge into simple type knowledge
    Example: Extracting files from a GitHub repository"""

    EMBEDDING = "embedding"
    """Embedding: Converts data into vector representations
    Used for semantic search and similarity comparisons"""

    KNOWLEDGE_LOADER = "knowledge_loader"
    """Knowledge Loader: Extracts information from various sources
    Example: Extracting text or image content from know"""

    RETRIEVER = "retriever"
    """Retriever: Finds and retrieves relevant information
    Used for searching and accessing stored knowledge"""

    PARSER = "parser"
    """Parser: Processes and divides knowledge into smaller units
    Example: parse text into chunks or segments"""

    LLM = "llm"
    """LLM: Large Language Model for text generation and conversation
    Example: GPT-4, Claude, LLaMA for chat and text generation"""


RegisterKeyType = Union[KnowledgeSourceEnum, KnowledgeTypeEnum, EmbeddingModelEnum, str]
T = TypeVar("T")
T_Embedding = TypeVar("T_Embedding", bound=BaseEmbedding)
T_Loader = TypeVar("T_Loader", bound=BaseLoader)
T_Retriever = TypeVar("T_Retriever", bound=BaseRetriever)
T_Parser = TypeVar("T_Parser", bound=BaseParser)
T_LLM = TypeVar("T_LLM", bound=BaseLLM)

RegisteredType = Union[
    Type[T_Embedding],
    Type[T_Loader],
    Type[T_Retriever],
    Type[T_Parser],
    Type[T_LLM],
]


class RegisterDict(Generic[T]):
    def __init__(self) -> None:
        self._dict: Dict[RegisterKeyType, Type[T]] = {}

    def __contains__(self, key: RegisterKeyType) -> bool:
        return key in self._dict

    def __getitem__(self, key: RegisterKeyType) -> Type[T]:
        return self._dict[key]

    def __setitem__(self, key: RegisterKeyType, value: Type[T]) -> None:
        if not isinstance(value, type):
            raise TypeError(f"Value must be a class, got {type(value)}")
        self._dict[key] = value

    def get(self, key: RegisterKeyType) -> Optional[Type[T]]:
        return self._dict.get(key)


EmbeddingRegistry = RegisterDict[BaseEmbedding]
LoaderRegistry = RegisterDict[BaseLoader]
RetrieverRegistry = RegisterDict[BaseRetriever]
ParserRegistry = RegisterDict[BaseParser]
LLMRegistry = RegisterDict[BaseLLM]


_registry: Dict[
    RegisterTypeEnum,
    Union[
        LoaderRegistry,
        EmbeddingRegistry,
        RetrieverRegistry,
        ParserRegistry,
        LLMRegistry,
    ],
] = {
    RegisterTypeEnum.EMBEDDING: RegisterDict[BaseEmbedding](),
    RegisterTypeEnum.KNOWLEDGE_LOADER: RegisterDict[BaseLoader](),
    RegisterTypeEnum.RETRIEVER: RegisterDict[BaseRetriever](),
    RegisterTypeEnum.PARSER: RegisterDict[BaseParser](),
    RegisterTypeEnum.LLM: RegisterDict[BaseLLM](),
}

BaseRegisterClsType = Union[
    Type[BaseLoader],
    Type[BaseEmbedding],
    Type[BaseRetriever],
    Type[BaseParser],
    Type[BaseLLM],
    None,
]

_loaded_packages = set()


def register(
    register_type: RegisterTypeEnum,
    register_key: RegisterKeyType,
    order: int = 0,
) -> Callable[[RegisteredType], RegisteredType]:
    def decorator(cls: RegisteredType) -> RegisteredType:
        setattr(cls, "_is_register_item", True)
        setattr(cls, "_register_type", register_type)
        setattr(cls, "_register_key", register_key)

        expected_base: BaseRegisterClsType = None
        if register_type == RegisterTypeEnum.EMBEDDING:
            expected_base = BaseEmbedding
        elif register_type == RegisterTypeEnum.KNOWLEDGE_LOADER:
            expected_base = BaseLoader
        elif register_type == RegisterTypeEnum.RETRIEVER:
            expected_base = BaseRetriever
        elif register_type == RegisterTypeEnum.PARSER:
            expected_base = BaseParser
        elif register_type == RegisterTypeEnum.LLM:
            expected_base = BaseLLM
        else:
            raise ValueError(f"Unknown register type: {register_type}")

        if not issubclass(cls, expected_base):
            raise TypeError(
                f"Class {cls.__name__} must inherit from {expected_base.__name__}"
            )

        # Perform health check before registering
        if hasattr(cls, "health_check") and callable(getattr(cls, "health_check")):
            health_check_result = cls.sync_health_check()
            if not health_check_result:
                logger.info(
                    f"Health check failed for class {cls.__name__}. Registration aborted."
                )
                return cls
        logger.info(
            f"Registering {cls.__name__} as {register_type} with key {register_key}"
        )
        if register_key in _registry[register_type]:
            existing_cls = _registry[register_type][register_key]
            existing_order = getattr(existing_cls, "_register_order", 0)
            if order <= existing_order:
                logger.debug(
                    f"Skipping registration of {cls.__name__}: "
                    f"existing implementation {existing_cls.__name__} "
                    f"has higher or equal priority ({existing_order} >= {order})"
                )
                return cls

            logger.info(
                f"Overriding {existing_cls.__name__} (order={existing_order}) "
                f"with {cls.__name__} (order={order})"
            )

        _registry[register_type][register_key] = cls
        return cls

    return decorator


def init_register(package_name: str = "whiskerrag_utils") -> None:
    if package_name in _loaded_packages:
        return
    try:
        package = importlib.import_module(package_name)
        if package.__file__ is None:
            raise ValueError(
                f"Package {package_name} does not have a __file__ attribute"
            )

        package_path = Path(package.__file__).parent
        current_file = Path(__file__).name

        for root, _, files in os.walk(package_path):
            for file in files:
                if file == current_file or not file.endswith(".py"):
                    continue

                module_name = (
                    Path(root, file)
                    .relative_to(package_path)
                    .with_suffix("")
                    .as_posix()
                    .replace("/", ".")
                )

                if module_name == "__init__":
                    continue

                try:
                    importlib.import_module(f"{package_name}.{module_name}")
                except ImportError as e:
                    logger.error(f"Error importing module {module_name}: {e}")

        _loaded_packages.add(package_name)

    except ImportError as e:
        logger.error(f"Error importing package {package_name}: {e}")


@overload
def get_register(
    register_type: Literal[RegisterTypeEnum.KNOWLEDGE_LOADER],
    register_key: KnowledgeSourceEnum,
) -> Type[BaseLoader]: ...


@overload
def get_register(
    register_type: Literal[RegisterTypeEnum.EMBEDDING],
    register_key: Union[EmbeddingModelEnum, str],
) -> Type[BaseEmbedding]: ...


@overload
def get_register(
    register_type: Literal[RegisterTypeEnum.RETRIEVER],
    register_key: str,
) -> Type[BaseRetriever]: ...


@overload
def get_register(
    register_type: Literal[RegisterTypeEnum.PARSER],
    register_key: str,
) -> Type[BaseParser]: ...


@overload
def get_register(
    register_type: Literal[RegisterTypeEnum.LLM],
    register_key: str,
) -> Type[BaseLLM]: ...


def get_register(
    register_type: RegisterTypeEnum,
    register_key: RegisterKeyType,
) -> Union[
    Type[BaseLoader],
    Type[BaseEmbedding],
    Type[BaseRetriever],
    Type[BaseParser],
    Type[BaseLLM],
    None,
]:
    registry = _registry.get(register_type)
    if registry is None:
        logger.warn(f"No registry for type: {register_type}")
        return None

    if register_type == RegisterTypeEnum.KNOWLEDGE_LOADER:
        registry = cast(LoaderRegistry, registry)
    elif register_type == RegisterTypeEnum.EMBEDDING:
        registry = cast(EmbeddingRegistry, registry)
    elif register_type == RegisterTypeEnum.RETRIEVER:
        registry = cast(RetrieverRegistry, registry)
    elif register_type == RegisterTypeEnum.PARSER:
        registry = cast(ParserRegistry, registry)
    elif register_type == RegisterTypeEnum.LLM:
        registry = cast(LLMRegistry, registry)

    cls = registry.get(register_key)

    if cls is None:
        raise KeyError(
            f"No implementation registered for type: {register_type}.{register_key}"
        )
    return cls


def get_registry_list() -> Dict[
    RegisterTypeEnum,
    Union[
        LoaderRegistry,
        EmbeddingRegistry,
        RetrieverRegistry,
        ParserRegistry,
        LLMRegistry,
    ],
]:
    return _registry
