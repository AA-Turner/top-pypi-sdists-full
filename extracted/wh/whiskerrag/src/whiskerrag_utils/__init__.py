import asyncio
import logging
from typing import List, Optional, Tuple, TypedDict, Union

from whiskerrag_types.interface.embed_interface import BaseEmbedding
from whiskerrag_types.model.chunk import Chunk
from whiskerrag_types.model.knowledge import Knowledge, KnowledgeTypeEnum
from whiskerrag_types.model.multi_modal import Image, Text

from .registry import RegisterTypeEnum, get_register, init_register, register

logger = logging.getLogger("whisker")


class DiffResult(TypedDict):
    to_add: List[Knowledge]
    to_delete: List[Knowledge]
    unchanged: List[Knowledge]


async def _process_parse_item(
    parse_item: Union[Text, Image],
    knowledge: Knowledge,
    EmbeddingCls: type[BaseEmbedding],
    semaphore: asyncio.Semaphore,
) -> Optional[Chunk]:
    async with semaphore:
        try:
            if isinstance(parse_item, Text):
                embedding = await EmbeddingCls().embed_text(
                    parse_item.content, timeout=30
                )
            elif isinstance(parse_item, Image):
                embedding = await EmbeddingCls().embed_image(parse_item, timeout=30)
            else:
                print(f"[warn]: illegal split item :{parse_item}")
                return None

            combined_metadata = {**knowledge.metadata}
            if isinstance(parse_item, Text) and parse_item.metadata:
                combined_metadata.update(parse_item.metadata)

            # Extract specific fields from metadata according to rules
            # knowledge.metadata._tags, _f1, _f2, _f3, _f4, _f5 -> chunk.tags, chunk.f1, chunk.f2, etc.
            tags = combined_metadata.get("_tags")
            if isinstance(tags, str):
                tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
            elif not isinstance(tags, list):
                tags = None

            return Chunk(
                context=(
                    parse_item.content
                    if isinstance(parse_item, Text)
                    else parse_item.url
                ),
                enabled=knowledge.enabled,
                metadata=combined_metadata,
                # Assign specific fields from metadata
                tags=tags,
                f1=combined_metadata.get("_f1"),
                f2=combined_metadata.get("_f2"),
                f3=combined_metadata.get("_f3"),
                f4=combined_metadata.get("_f4"),
                f5=combined_metadata.get("_f5"),
                embedding=embedding,
                knowledge_id=knowledge.knowledge_id,
                embedding_model_name=knowledge.embedding_model_name,
                space_id=knowledge.space_id,
                tenant_id=knowledge.tenant_id,
            )
        except Exception as e:
            logger.error(f"Error processing parse item: {e}")
            return None


def _get_unique_origin_list(
    origin_list: List[Knowledge],
) -> Tuple[List[Knowledge], List[Knowledge]]:
    to_delete = []
    seen_file_shas = set()
    unique_origin_list = []
    for item in origin_list:
        if item.file_sha not in seen_file_shas:
            seen_file_shas.add(item.file_sha)
            unique_origin_list.append(item)
        else:
            to_delete.append(item)
    return to_delete, unique_origin_list


async def decompose_knowledge(
    knowledge: Knowledge,
    semaphore: Optional[asyncio.Semaphore] = None,
    max_concurrency: int = 4,
) -> List[Knowledge]:
    if semaphore is None:
        semaphore = asyncio.Semaphore(max_concurrency)
    LoaderCls = get_register(RegisterTypeEnum.KNOWLEDGE_LOADER, knowledge.source_type)
    async with semaphore:
        knowledge_list = await LoaderCls(knowledge).decompose()
    if not knowledge_list:
        return []
    tasks = [decompose_knowledge(k, semaphore) for k in knowledge_list]
    results = await asyncio.gather(*tasks)
    flat = [item for sublist in results for item in sublist]
    return flat if flat else knowledge_list


async def get_chunks_by_knowledge(
    knowledge: Knowledge, semaphore_num: int = 4
) -> List[Chunk]:
    """
    Convert knowledge into vectorized chunks with controlled concurrency
    """
    source_type = knowledge.source_type
    knowledge_type = knowledge.knowledge_type
    parse_type = getattr(
        knowledge.split_config,
        "type",
        "base_image" if knowledge_type is KnowledgeTypeEnum.IMAGE else "base_text",
    )
    LoaderCls = get_register(RegisterTypeEnum.KNOWLEDGE_LOADER, source_type)
    ParserCls = get_register(RegisterTypeEnum.PARSER, parse_type)
    EmbeddingCls = get_register(
        RegisterTypeEnum.EMBEDDING, knowledge.embedding_model_name
    )
    # If no parser, return empty list
    if ParserCls is None:
        logger.warn(f"No parser found for type: {parse_type}")
        return []
    # If no embedding model, return empty list
    if EmbeddingCls is None:
        logger.warn(
            f"[warn]: No embedding model found for name: {knowledge.embedding_model_name}"
        )
        return []
    loaded_contents = []
    if LoaderCls is None:
        # If no loader, directly parse the knowledge object itself
        logger.warn(
            f"No loader found for source type: {knowledge.source_type}, attempting to parse knowledge directly."
        )
        parse_results = await ParserCls().parse(knowledge, None)
    else:
        # Use loader to load contents
        loaded_contents = await LoaderCls(knowledge).load()
        if not loaded_contents:
            logger.warn(
                f"Loader returned no content for source type: {knowledge.source_type}."
            )
            return []
        # Parse loaded contents
        parse_results = []
        for content in loaded_contents:
            split_result = await ParserCls().parse(knowledge, content)
            parse_results.extend(split_result)

    semaphore = asyncio.Semaphore(semaphore_num)
    tasks = [
        _process_parse_item(parse_item, knowledge, EmbeddingCls, semaphore)
        for parse_item in parse_results
    ]
    chunks = await asyncio.gather(*tasks)
    return [chunk for chunk in chunks if chunk is not None]


def get_diff_knowledge_by_sha(
    origin_list: Optional[List[Knowledge]] = None,
    new_list: Optional[List[Knowledge]] = None,
) -> DiffResult:
    try:
        origin_list = origin_list or []
        new_list = new_list or []

        to_delete = []
        to_delete_origin, unique_origin_list = _get_unique_origin_list(origin_list)
        to_delete.extend(to_delete_origin)
        _, unique_new_list = _get_unique_origin_list(new_list)

        origin_map = {item.file_sha: item for item in unique_origin_list}

        to_add = []
        unchanged = []
        for new_item in unique_new_list:
            if new_item.file_sha not in origin_map:
                to_add.append(new_item)
            else:
                unchanged.append(new_item)
                del origin_map[new_item.file_sha]

        to_delete.extend(list(origin_map.values()))

        return {"to_add": to_add, "to_delete": to_delete, "unchanged": unchanged}
    except Exception as error:
        logger.error(f"Error in _get_diff_knowledge_by_sha: {error}")
        return {"to_add": [], "to_delete": [], "unchanged": []}


__all__ = [
    "get_register",
    "register",
    "RegisterTypeEnum",
    "init_register",
    "SplitterEnum",
    "decompose_knowledge",
    "get_chunks_by_knowledge",
    "DiffResult",
    "get_diff_knowledge_by_sha",
]
