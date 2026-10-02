import abc
import uuid
from typing import Any, Union

from teradataml import DataFrame

from tmo.api.iterator_base_api import IteratorBaseApi


class BaseEntityApiMixin(IteratorBaseApi):
    """
    Base API mixin for entities APIs
    Provides common methods for entities with pagination, sorting, and projection.
    This mixin is intended to be used in conjunction with @functional entity types like Dataset and DatasetTemplate, which have similar API patterns.
    """

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ) -> list[Any] | DataFrame:
        """
        returns a list of entities depending on the API implementation

        Parameters:
            projection (str): projection type
            page (int): page number for pagination
            size (int): page size for pagination
            sort (str): sorting criteria
            return_dataframe (bool): whether to return a DataFrame instead of a list
        Returns:
            (list | teradataml.Dataframe | pandas.Dataframe): list of entities
        """
        return self.find_all_entities(projection, page, size, sort, return_dataframe)

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ) -> list[Any] | DataFrame:
        """
        returns all entities by archived

        Parameters:
           archived (bool): whether to return archived or unarchived entities
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order e.g. name?asc / name?desc
           return_dataframe (bool): whether to return a DataFrame instead of a list
        Returns:
            (list | teradataml.Dataframe | pandas.Dataframe): list of entities
        """
        return self.find_by_archived_entities(
            archived, projection, page, size, sort, return_dataframe
        )

    def find_by_id(
        self,
        entity_id: Union[str, uuid.UUID],
        projection: str = None,
        return_dataframe: bool = False,
    ) -> Any | None | DataFrame:
        """
        returns a single entity (e.g., dataset or dataset template) by its ID, or None if not found

        Parameters:
            projection (str): projection type
            entity_id (Union[str, uuid.UUID]): entity id
            return_dataframe (bool): whether to return a DataFrame instead of an entity object
        Returns:
            Any | None | DataFrame: single entity object, DataFrame (if return_dataframe=True), or None if not found
        """
        return self.find_entity_by_id(entity_id, projection, return_dataframe)

    @abc.abstractmethod  # noqa
    def _parse_entity_from_dictionary(self, dictionary: dict) -> Any:
        """
        Helper method to parse an individual entity from API response data (dict).
        Must be implemented by child classes to convert raw response data into entity objects
        and provide functional behavior, these classes must use the @functional decorator.

        Returns:
            Parsed entity object
        """
        ...
