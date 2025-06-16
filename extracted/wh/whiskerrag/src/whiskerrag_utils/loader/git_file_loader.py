from typing import List, Optional

from whiskerrag_types.interface.loader_interface import BaseLoader
from whiskerrag_types.model import (
    GithubFileSourceConfig,
    Knowledge,
    KnowledgeSourceEnum,
)
from whiskerrag_types.model.multi_modal import Text
from whiskerrag_utils.loader.git_repo_loader import GithubRepoLoader
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.KNOWLEDGE_LOADER, KnowledgeSourceEnum.GITHUB_FILE)
class GithubFileLoader(BaseLoader[Text]):
    """
    Load a file from a GitHub repository.
    """

    knowledge: Knowledge
    path: str
    commit_id: Optional[str]
    repo_loader: GithubRepoLoader

    def __init__(
        self,
        knowledge: Knowledge,
    ):
        self.knowledge = knowledge
        if not isinstance(knowledge.source_config, GithubFileSourceConfig):
            raise ValueError("source_config should be GithubFileSourceConfig")
        self.path = knowledge.source_config.path
        self.repo_loader = GithubRepoLoader(knowledge)

    async def load(self) -> List[Text]:
        file_element = await self.repo_loader.get_file_by_path(self.path)
        return [
            Text(
                content=file_element.content,
                metadata=self.knowledge.metadata,
            )
        ]

    async def decompose(self) -> List[Knowledge]:
        return []

    async def on_load_finished(self) -> None:
        """
        Lifecycle method called when the loading task is finished.
        Subclasses can implement this to perform any cleanup or post-processing.
        """
        pass
