import logging
from abc import ABC, abstractmethod
from typing import Any, List, Optional, TypeVar, Union

from pydantic import BaseModel

from whiskerrag_types.model import (
    APIKey,
    GlobalRule,
    Knowledge,
    PageQueryParams,
    PageResponse,
    Space,
    SpaceRule,
    Task,
    TaskStatus,
    Tenant,
    Wiki,
)
from whiskerrag_types.model.chunk import Chunk
from whiskerrag_types.model.page import QueryParams
from whiskerrag_types.model.retrieval import (
    RetrievalByKnowledgeRequest,
    RetrievalBySpaceRequest,
    RetrievalChunk,
    RetrievalRequest,
)

from .settings_interface import SettingsInterface

T = TypeVar("T", bound=BaseModel)


class DBPluginInterface(ABC):
    settings: SettingsInterface

    def __init__(self, settings: SettingsInterface) -> None:
        self.settings = settings
        self.logger = logging.getLogger("whisker")
        self._initialized: bool = False

    async def ensure_initialized(self) -> None:
        if not self._initialized:
            try:
                self.logger.info("DBEngine plugin is initializing...")
                await self.init()
                self._initialized = True
                self.logger.info("DBEngine plugin is initialized")
            except Exception as e:
                self.logger.error(f"DBEngine plugin init error: {e}")
                raise

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @abstractmethod
    async def init(self) -> None:
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        pass

    @abstractmethod
    def get_db_client(self) -> Any:
        pass

    # =================== knowledge ===================
    @abstractmethod
    async def save_knowledge_list(
        self, knowledge_list: List[Knowledge]
    ) -> List[Knowledge]:
        pass

    @abstractmethod
    async def get_knowledge_list(
        self, tenant_id: str, page_params: PageQueryParams[Knowledge]
    ) -> PageResponse[Knowledge]:
        pass

    @abstractmethod
    async def get_knowledge(self, tenant_id: str, knowledge_id: str) -> Knowledge:
        pass

    @abstractmethod
    async def update_knowledge(self, knowledge: Knowledge) -> None:
        pass

    @abstractmethod
    async def delete_knowledge(
        self, tenant_id: str, knowledge_id_list: List[str]
    ) -> None:
        pass

    @abstractmethod
    async def batch_update_knowledge_retrieval_count(
        self, knowledge_id_list: dict[str, int]
    ) -> None:
        pass

    @abstractmethod
    async def update_knowledge_enabled_status(
        self, tenant_id: str, knowledge_id: str, enabled: bool
    ) -> None:
        pass

    # =================== Space ===================
    @abstractmethod
    async def save_space(self, space: Space) -> Space:
        pass

    @abstractmethod
    async def update_space(self, space: Space) -> Space:
        pass

    @abstractmethod
    async def get_space_list(
        self, tenant_id: str, page_params: PageQueryParams[Space]
    ) -> PageResponse[Space]:
        pass

    @abstractmethod
    async def get_space(self, tenant_id: str, space_id: str) -> Space:
        pass

    @abstractmethod
    async def delete_space(
        self, tenant_id: str, space_id: str
    ) -> Union[List[Space], None]:
        pass

    # =================== chunk ===================
    @abstractmethod
    async def save_chunk_list(self, chunks: List[Chunk]) -> List[Chunk]:
        pass

    @abstractmethod
    async def update_chunk_list(self, chunks: List[Chunk]) -> List[Chunk]:
        pass

    @abstractmethod
    async def get_chunk_list(
        self, tenant_id: str, page_params: PageQueryParams[Chunk]
    ) -> PageResponse[Chunk]:
        pass

    @abstractmethod
    async def get_all_chunk(
        self, tenant_id: str, query_params: QueryParams[Chunk]
    ) -> List[Chunk]:
        pass

    @abstractmethod
    async def get_chunk_by_id(
        self, tenant_id: str, chunk_id: str, embedding_model_name: str
    ) -> Union[Chunk, None]:
        pass

    @abstractmethod
    async def delete_chunk_by_id(
        self, tenant_id: str, chunk_id: str, embedding_model_name: str
    ) -> Union[Chunk, None]:
        pass

    @abstractmethod
    async def delete_knowledge_chunk(
        self, tenant_id: str, knowledge_ids: List[str]
    ) -> Union[List[Chunk], None]:
        pass

    # =================== retrieval ===================
    @abstractmethod
    async def search_space_chunk_list(
        self,
        tenant_id: str,
        params: RetrievalBySpaceRequest,
    ) -> List[RetrievalChunk]:
        pass

    @abstractmethod
    async def search_knowledge_chunk_list(
        self,
        tenant_id: str,
        params: RetrievalByKnowledgeRequest,
    ) -> List[RetrievalChunk]:
        pass

    @abstractmethod
    async def retrieve(
        self,
        tenant_id: str,
        params: RetrievalRequest,
    ) -> List[RetrievalChunk]:
        pass

    # =================== task ===================
    @abstractmethod
    async def save_task_list(self, task_list: List[Task]) -> List[Task]:
        pass

    @abstractmethod
    async def update_task_list(self, task_list: List[Task]) -> None:
        pass

    @abstractmethod
    async def get_task_list(
        self, tenant_id: str, page_params: PageQueryParams[Task]
    ) -> PageResponse[Task]:
        pass

    @abstractmethod
    async def get_task_by_id(self, tenant_id: str, task_id: str) -> Union[Task, None]:
        pass

    @abstractmethod
    async def delete_task_by_id(
        self, tenant_id: str, task_id: str
    ) -> Union[Task, None]:
        pass

    @abstractmethod
    async def task_statistics(
        self, space_id: str, status: TaskStatus
    ) -> Union[dict[TaskStatus, int], int]:
        pass

    @abstractmethod
    async def delete_knowledge_task(
        self, tenant_id: str, knowledge_ids: List[str]
    ) -> Union[List[Task], None]:
        pass

    # =================== tenant ===================
    @abstractmethod
    async def save_tenant(self, tenant: Tenant) -> Union[Tenant, None]:
        pass

    @abstractmethod
    async def get_tenant_by_sk(self, secret_key: str) -> Union[Tenant, None]:
        pass

    @abstractmethod
    async def update_tenant(self, tenant: Tenant) -> Union[Tenant, None]:
        pass

    @abstractmethod
    async def validate_tenant_name(self, tenant_name: str) -> bool:
        pass

    @abstractmethod
    async def get_tenant_by_id(self, tenant_id: str) -> Union[Tenant, None]:
        pass

    @abstractmethod
    async def get_tenant_list(
        self, page_params: PageQueryParams[Tenant]
    ) -> PageResponse[Tenant]:
        pass

    @abstractmethod
    async def delete_tenant_by_id(self, tenant_id: str) -> Union[Tenant, None]:
        pass

    # =================== api-key ===================
    @abstractmethod
    async def get_api_key_by_value(self, key_value: str) -> Union[APIKey, None]:
        pass

    @abstractmethod
    async def get_api_key_by_id(
        self, tenant_id: str, key_id: str
    ) -> Union[APIKey, None]:
        pass

    @abstractmethod
    async def get_tenant_api_keys(
        self, tenant_id: str, page_params: PageQueryParams[APIKey]
    ) -> PageResponse[APIKey]:
        pass

    @abstractmethod
    async def save_api_key(self, create_params: APIKey) -> APIKey:
        pass

    @abstractmethod
    async def update_api_key(self, update_params: APIKey) -> Union[APIKey, None]:
        pass

    @abstractmethod
    async def delete_api_key(self, key_id: str) -> bool:
        pass

    @abstractmethod
    async def get_all_expired_api_keys(self, tenant_id: str) -> List[APIKey]:
        pass

    # =================== rule ===================
    @abstractmethod
    async def create_rule(
        self, tenant_id: str, rule: Union[GlobalRule, SpaceRule]
    ) -> None:
        pass

    @abstractmethod
    async def update_rule(
        self, tenant_id: str, rule_id: str, rule: Union[GlobalRule, SpaceRule]
    ) -> Union[GlobalRule, SpaceRule]:
        pass

    @abstractmethod
    async def get_tenant_rule(self, tenant_id: str) -> Optional[str]:
        pass

    @abstractmethod
    async def get_space_rule(self, space_id: str) -> Optional[str]:
        pass

    # =================== wiki ===================
    @abstractmethod
    async def create_wiki(self, wiki: Wiki) -> None:
        pass
