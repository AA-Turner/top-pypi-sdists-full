from whiskerrag_client.chunk_client import ChunkClient
from whiskerrag_client.http_client import HttpClient
from whiskerrag_client.knowledge_client import KnowledgeClient
from whiskerrag_client.retrieval_client import RetrievalClient
from whiskerrag_client.space_client import SpaceClient
from whiskerrag_client.task_client import TaskClient


class APIClient:

    def __init__(
        self,
        base_url: str,
        token: str,
        timeout: float = 10,
    ):
        self.http_client = HttpClient(base_url, token, timeout)
        self.knowledge = KnowledgeClient(self.http_client)
        self.retrieval = RetrievalClient(self.http_client)
        self.chunk = ChunkClient(self.http_client)
        self.task = TaskClient(self.http_client)
        self.space = SpaceClient(self.http_client)


__all__ = ["APIClient"]
