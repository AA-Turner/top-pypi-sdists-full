import logging
from abc import ABC, abstractmethod
from typing import List, Optional

from ..interface import DBPluginInterface, SettingsInterface
from ..model import Knowledge, Task, Tenant


class TaskEnginPluginInterface(ABC):
    settings: SettingsInterface
    db_plugin: Optional[DBPluginInterface] = None

    def __init__(
        self,
        settings: SettingsInterface,
    ):
        self.settings = settings
        self.logger = logging.getLogger("whisker")
        self._initialized: bool = False

    async def ensure_initialized(self, db_plugin: Optional[DBPluginInterface]) -> None:
        if not self._initialized:
            try:
                self.logger.info("TaskEngine plugin is initializing...")
                await self.init()
                if db_plugin:
                    if not db_plugin.is_initialized:
                        self.logger.info("Initializing DB plugin...")
                        await db_plugin.ensure_initialized()
                    self.db_plugin = db_plugin
                self._initialized = True
                self.logger.info("TaskEngine plugin is initialized")
            except Exception as e:
                self.logger.error(f"TaskEngine plugin init error: {e}")
                raise

    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @abstractmethod
    async def init(self) -> None:
        """
        Initialize the task engine plugin, such as loading middleware, establishing contact with the task execution engine, etc.
        """
        pass

    @abstractmethod
    async def init_task_from_knowledge(
        self, knowledge_list: List[Knowledge], tenant: Tenant
    ) -> List[Task]:
        """
        Initialize a list of tasks from the knowledge list.
        """
        pass

    @abstractmethod
    async def batch_execute_task(
        self, task_list: List[Task], knowledge_list: List[Knowledge]
    ) -> List[Task]:
        """
        Execute a list of tasks.
        """
        pass
