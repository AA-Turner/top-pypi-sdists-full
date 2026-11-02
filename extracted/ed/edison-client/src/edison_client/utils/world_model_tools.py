import os
from uuid import UUID

from aviary.core import Tool

from edison_client.clients.rest_client import RestClient
from edison_client.models.app import Stage
from edison_client.models.rest import SearchCriterion, SearchOperator, WorldModel


class WorldModelTools:
    _client: RestClient | None = None

    @classmethod
    def _get_client(cls) -> RestClient:
        """Lazy initialization of the RestClient to avoid validation errors during import."""
        if cls._client is None:
            api_key = os.getenv("FH_PLATFORM_API_KEY")
            if not api_key:
                raise ValueError(
                    "FH_PLATFORM_API_KEY environment variable is required for WorldModelTools"
                )
            cls._client = RestClient(
                stage=Stage.from_string(os.getenv("CROW_ENV", "dev")),
                api_key=api_key,
            )
        return cls._client

    @staticmethod
    def create_world_model(name: str, description: str, content: str) -> UUID:
        """Create a new world model.

        Args:
            name: The name of the world model.
            description: A description of the world model.
            content: The content/data of the world model.

        Returns:
            UUID: The ID of the newly created world model.
        """
        world_model = WorldModel(
            name=name,
            description=description,
            content=content,
        )
        return WorldModelTools._get_client().create_world_model(world_model)

    @staticmethod
    def search_world_models(query: str, size: int = 10) -> list[str]:
        """Search for world models using a text query.

        Args:
            query: The search query string to match against world model content.
            size: The number of results to return (default: 10).

        Returns:
            list[str]: A list of world model IDs that match the search query.
        """
        criteria = (
            [
                SearchCriterion(
                    field="name", operator=SearchOperator.CONTAINS, value=query
                ),
                SearchCriterion(
                    field="description", operator=SearchOperator.CONTAINS, value=query
                ),
                SearchCriterion(
                    field="content", operator=SearchOperator.CONTAINS, value=query
                ),
            ]
            if query
            else []
        )

        results = WorldModelTools._get_client().search_world_models(
            criteria=criteria, size=size
        )
        return [str(model.id) for model in results]


create_world_model_tool = Tool.from_function(WorldModelTools.create_world_model)
search_world_model_tool = Tool.from_function(WorldModelTools.search_world_models)


def make_world_model_tools() -> list[Tool]:
    return [
        search_world_model_tool,
        create_world_model_tool,
    ]
