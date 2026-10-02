from __future__ import absolute_import

import logging
import uuid
from typing import Any, Union, Optional

import pandas
from teradataml import DataFrame

from tmo.api.utils.strings import camel_to_normalized
from tmo.api_client import TmoClient

logger = logging.getLogger(__name__)


class BaseApi(object):
    name = "Base API"
    base_path = "/api/"
    path = ""
    json_type = "application/json"
    type = None  # to be defined in child classes, e.g. "trainedModels", "featureEngineeringTasks", etc.
    entities_container = "_embedded"

    def __init__(self, tmo_client: TmoClient):
        self.tmo_client = tmo_client

    def find_all(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns all entities

        Parameters:
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order
           e.g. name?asc: sort name in ascending order, name?desc: sort name in descending order

        Returns:
            (dict): all entities
        """
        header_params = self._get_header_params()

        query_vars = ["projection", "page", "size", "sort"]
        query_vals = [projection, page, size, sort]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            self.base_path + self.path, header_params, query_params
        )

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        """
        returns all entities by archived

        Parameters:
           archived (bool): whether to return archived or unarchived entities
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order e.g. name?asc / name?desc

        Returns:
            (list): all entities
        """
        header_params = self._get_header_params()

        query_vars = ["projection", "page", "size", "sort", "archived"]
        query_vals = [projection, page, size, sort, archived]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.base_path + self.path}/search/findByArchived",
            header_params,
            query_params,
        )

    def find_by_id(self, entity_id: Union[str, uuid.UUID], projection: str = None):
        """
        returns the entity

        Parameters:
           entity_id (str): entity id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): entity
        """
        entity_id = self.validate_uuid(entity_id)
        header_params = self._get_header_params()

        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.base_path + self.path}/{entity_id}", header_params, query_params
        )

    def find_all_entities(
        self,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        return_dataframe: bool = False,
    ) -> list[Any] | DataFrame:
        """
        returns all entities with consistent response processing and error handling for iterator support.

        Parameters:
            projection (str): projection type
            page (int): page number
            size (int): number of records in a page
            sort (str): column name and sorting order
            return_dataframe (bool): if True, returns DataFrame; if False, returns list of DatasetTemplate objects

        Returns:
            (list | teradataml.Dataframe | pandas.Dataframe): entities in a list or DataFrame format based on return_dataframe flag. Returns empty list or DataFrame on error.
        """

        return self.get_entities_request(
            path_suffix="",
            projection=projection,
            page=page,
            size=size,
            sort=sort,
            return_dataframe=return_dataframe,
        )

    def find_by_archived_entities(
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
            sort (str): column name and sorting order
            return_dataframe (bool): if True, returns DataFrame; if False, returns list of DatasetTemplate objects

        Returns:
            (list | teradataml.Dataframe | pandas.Dataframe): entities in a list or DataFrame format based on return_dataframe flag. Returns empty list or DataFrame on error.
        """

        return self.get_entities_request(
            path_suffix="/search/findByArchived",
            projection=projection,
            page=page,
            size=size,
            sort=sort,
            query_params={"archived": archived},
            return_dataframe=return_dataframe,
        )

    def find_entity_by_id(
        self,
        entity_id: Union[str, uuid.UUID],
        projection: str = None,
        return_dataframe: bool = False,
    ) -> None | DataFrame | Any:
        """
        returns a single entity by id

        Parameters:
            entity_id (str): entity id
            projection (str): projection type
            return_dataframe (bool): if True, returns DataFrame; if False, returns entity object

        Returns:
            entity object or DataFrame if found, None if not found or error occurs
        """

        entity_id = self.validate_uuid(entity_id)
        if entity_id is None:
            return None

        query_vars = ["id", "projection"]
        query_vals = [entity_id, projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.get_entity_request(
            path_suffix="/search/findById",
            projection=projection,
            query_params=query_params,
            return_dataframe=return_dataframe,
        )

    def archive(self, entity_id: Union[str, uuid.UUID]):
        """
        archives the entity
        Parameters:
           entity_id (str): entity id(uuid) to archive
        Returns:
            (dict): entity
        """
        entity_id = self.validate_uuid(entity_id)
        header_params = self._get_header_params()

        return self.tmo_client.post_request(
            f"{self.base_path}archives/{self.type}/{entity_id}",
            header_params,
            {},
            {},
        )

    def unarchive(self, entity_id: Union[str, uuid.UUID]):
        """
        unarchives the entity
        Parameters:
           entity_id (str): entity id(uuid) to unarchive
        Returns:
            (dict): entity
        """
        entity_id = self.validate_uuid(entity_id)
        header_params = self._get_header_params()

        return self.tmo_client.delete_request(
            f"{self.base_path}archives/{self.type}/{entity_id}",
            header_params,
            {},
            {},
        )

    def build_get_request(
        self,
        path_suffix: str = "",
        query_params: dict = None,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ) -> Any | None:
        """
        Helper method to build and execute a GET request for fetching entities with consistent parameters.

        Parameters:
            page (int | None): page number for pagination
            path_suffix (str): API path suffix for specific queries (e.g. "/search/findByArchived")
            projection (str | None): projection type
            query_params (dict | None): additional query parameters to include in the request
            size (int | None): page size for pagination
            sort (str | None): sorting criteria (e.g. "name?asc" for ascending sort by name, "name?desc" for descending sort by name)
        Returns:
            API response from the GET request, or None if an error occurs
        """
        query_vars = ["projection", "page", "size", "sort"]
        query_vals = [projection, page, size, sort]
        built_query_params = self.generate_params(query_vars, query_vals)

        response = self.tmo_client.get_request(
            path=self.base_path + self.path + path_suffix,
            header_params=self._get_header_params(),
            query_params=built_query_params | (query_params or {}),
        )
        return response

    @staticmethod
    def generate_params(params: list[str], values: list[str]):
        """
        returns list of parameters and values as dictionary

        Parameters:
           params (list[str]): list of parameter names
           values (list[str]): list of parameter values

        Returns:
            (dict): generated parameters
        """

        # bools in python start with upper case when converted to strs. APIs expect lowercase
        api_values = [str(v).lower() if type(v) is bool else v for v in values]

        return dict(zip(params, api_values))

    def handle_invalid_entities_response(
        self, return_dataframe: bool = False
    ) -> list[Any] | DataFrame:
        """
        Handle invalid API response by setting empty cache and pagination info.

        Parameters:
            return_dataframe (bool): if True, returns empty DataFrame; if False, returns empty list

        Returns:
            DataFrame or list: Empty result appropriate for the return type
        """
        # Set empty cache and pagination info for iterator
        self.set_iterator_cache([])
        self.set_iterator_page_info({})
        logger.error(f"Invalid response received for {camel_to_normalized(self.path)}.")
        return [] if not return_dataframe else pandas.DataFrame()

    def handle_invalid_entity_response(self) -> None:
        """
        Handle invalid API response for single entity operations (find_by_id).

        Returns:
            None: Always returns None when a single entity is not found
        """
        # Set empty cache and pagination info for iterator
        self.set_iterator_cache([])
        self.set_iterator_page_info({})
        logger.error(f"Invalid response received for {camel_to_normalized(self.path)}.")
        return None

    def get_entities_request(
        self,
        path_suffix: str = "",
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        query_params: dict = None,
        return_dataframe: bool = False,
    ) -> list[Any] | DataFrame:
        """
        Helper method to make API request for fetching entities with consistent parameters and error handling.

        Parameters:
            path_suffix (str): API path suffix for specific queries (e.g. "/search/findByArchived")
            projection (str): projection type
            page (int): page number
            size (int): number of records in a page
            sort (str): column name and sorting order
            query_params (dict, optional): additional query parameters to include in the request
            return_dataframe (bool): if True, returns DataFrame; if False, returns list of entity objects

        Returns:
            (list | teradataml.Dataframe | pandas.Dataframe): entities in a list or DataFrame format based on return_dataframe flag. Returns empty list or DataFrame on error.
        """

        response = self.build_get_request(
            path_suffix, query_params, projection, page, size, sort
        )

        return self.process_entities_response(
            response=response,
            return_dataframe=return_dataframe,
        )

    def get_entity_request(
        self,
        path_suffix: str = "",
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
        query_params: dict = None,
        return_dataframe: bool = False,
    ) -> Any | None | DataFrame:
        """
        Helper method to make API request for fetching a single entity with consistent parameters and error handling.

        Parameters:
            path_suffix (str): API path suffix for specific queries (e.g. "/search/findById")
            projection (str): projection type
            page (int): page number (usually not used for single entity queries)
            size (int): number of records in a page (usually not used for single entity queries)
            sort (str): column name and sorting order (usually not used for single entity queries)
            query_params (dict, optional): additional query parameters to include in the request
            return_dataframe (bool): if True, returns DataFrame; if False, returns entity object

        Returns:
            (Any | None | teradataml.Dataframe | pandas.Dataframe): single entity object or None if not found. Returns DataFrame if return_dataframe=True.
        """

        response = self.build_get_request(
            path_suffix, query_params, projection, page, size, sort
        )

        return self.process_entity_response(
            response=response,
            return_dataframe=return_dataframe,
        )

    def process_entities_response(
        self, response: dict, return_dataframe: bool = False, context: str = ""
    ) -> list[Any] | DataFrame:
        """
        Process find_all API response with consistent error handling and iterator setup.
        This method provides generic response processing for all child API classes.

        Parameters:
            response (dict): API response from find_all request
            return_dataframe (bool): if True, returns DataFrame; if False, returns list
            context (str): additional context to include in log messages for better debugging (e.g. " for project XYZ")

        Returns:
            DataFrame or list: Processed entities or empty result on error
        """
        entity_name = camel_to_normalized(self.path)
        try:
            # Validate response
            if response is None or self.entities_container not in response:
                return self.handle_invalid_entities_response(return_dataframe)

            # Extract entities and pagination info
            entities_data = response.get(self.entities_container, {}).get(self.path, [])
            page_info = response.get("page", {})

            # Handle empty results
            if not entities_data:
                logger.info(f"No {entity_name} found{context}.")
                self.set_iterator_cache([])
                self.set_iterator_page_info(page_info)
                return [] if not return_dataframe else pandas.DataFrame()

            # Parse entities
            entities = []
            for entity_data in entities_data:
                entity = self._parse_entity_from_dictionary(entity_data)
                if entity:
                    entities.append(entity)

            # Set pagination info and cache for iterator
            self.set_iterator_cache(entities)
            self.set_iterator_page_info(page_info)

            # Return appropriate format
            if return_dataframe:
                return self._entities_to_dataframe(entities)
            else:
                return entities

        except Exception as e:
            logger.error(f"Error parsing {entity_name}{context}: {str(e)}")
            return [] if not return_dataframe else pandas.DataFrame()

    def process_entity_response(
        self, response: dict, return_dataframe: bool = False, context: str = ""
    ) -> list[Any] | None | DataFrame:
        """
        Process find_by_id API response with consistent error handling.
        This method provides generic response processing for all child API classes.

        Parameters:
            response (dict): API response from find_by_id request
            return_dataframe (bool): if True, returns DataFrame; if False, returns entity object
            context (str): additional context to include in log messages for better debugging (e.g. " for project XYZ")
        Returns:
            entity object or DataFrame if found, None if not found or error occurs
        """
        entity_name = camel_to_normalized(self.path)
        try:
            # Validate response
            if response is None:
                return self.handle_invalid_entity_response()

            entity = self._parse_entity_from_dictionary(response)

            if entity is None:
                logger.error(f"{entity_name} not found{context}.")
                return None

            if return_dataframe:
                # Prefer using the entity's DataFrame template representation, if available,
                # to keep behavior consistent with other code paths (e.g. _entities_to_dataframe).
                get_df_template = getattr(entity, "get_df_template", None)
                if callable(get_df_template):
                    df_template = get_df_template()
                    return self.to_dataframe([df_template])
                # Fallback to previous behavior if no get_df_template is defined
                return self.to_dataframe(entity)
            else:
                return entity

        except Exception as e:
            logger.error(f"Error parsing {entity_name}{context}: {str(e)}")
            return None

    @staticmethod
    def required_params(param_names: list[str], dict_obj: dict[str, str]):
        """
        checks required parameters, raises exception if the required parameter is missing in the dictionary

        Parameters:
           param_names (list[str]): list of required parameter names
           dict_obj (Dict[str, str]): dictionary to check for required parameters
        """
        for param in param_names:
            if param not in dict_obj:
                raise ValueError(f"Missing required value {str(param)}")

    def set_iterator_cache(self, cache: list):
        """
        Default implementation for iterator cache management.
        Iterator-aware subclasses (e.g., those that support pagination/iteration)
        may override this method to provide custom behavior. For non-iterator
        subclasses, this safely stores the cache on the instance so that calls
        from BaseApi response handlers do not raise errors.
        """
        self._iterator_cache = cache  # noqa

    def set_iterator_page_info(self, page_info: dict):
        """
        Default implementation for iterator pagination info management.
        Iterator-aware subclasses may override this method to provide custom
        behavior. For non-iterator subclasses, this safely stores the page
        information on the instance.
        """
        self._iterator_page_info = page_info  # noqa

    def to_dataframe(self, obj: dict | list) -> Optional[DataFrame | pandas.DataFrame]:
        """
        Converts a list or single instance of the entity to a DataFrame.
        Falls back to returning a Pandas DataFrame if the Teradata conversion fails.

        Parameters:
            obj (dict, list): The entity or entity list to convert.
        Returns:
            Optional[teradataml.DataFrame | pandas.DataFrame]: A DataFrame representation of the entity or entity list.
        """
        from tmo.util.utils import to_dataframe as utils_to_dataframe

        try:
            # If obj has get_df_template method, convert it to dict first
            if hasattr(obj, "get_df_template"):
                obj = obj.get_df_template()

            # Wrap single dict in a list for consistent DataFrame conversion
            if isinstance(obj, dict):
                obj = [obj]

            return utils_to_dataframe(obj)
        except Exception as e:
            logger.error(
                f"Could not convert {self.__class__.__name__} to DataFrame: {str(e)}"
            )
            return None

    @staticmethod
    def validate_uuid(
        entity_id: Union[str, uuid.UUID], to_string: bool = True
    ) -> Optional[uuid.UUID] | str:
        """
        Validates that the provided ID is a valid UUID. If it's a string, attempts to convert it to a UUID.

        Parameters:
            entity_id (Union[str, uuid.UUID]): The ID to validate.
            to_string (bool): If True, returns the UUID as a string; if False, returns as uuid.UUID object.
        Returns:
            Optional[uuid.UUID]: The validated UUID, or None if validation fails.
        """
        if isinstance(entity_id, uuid.UUID):
            final_id = entity_id
        elif isinstance(entity_id, str):
            try:
                final_id = uuid.UUID(entity_id)
            except ValueError:
                logger.error(f"Invalid UUID format for id: {entity_id}")
                return None
        else:
            logger.error(f"ID must be a string or UUID instance, got {type(entity_id)}")
            return None

        return str(final_id) if to_string else final_id

    def _approve_entity(self, entity_id: str, comments: str):
        """
        Generic method to approve an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            comments (str): approval comments

        Returns:
            (dict): response
        """
        entity_id = self.validate_uuid(entity_id)

        approve_request = {"comments": comments}

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{entity_id}/approve",
            header_params=self._get_header_params(),
            query_params={},
            body=approve_request,
        )

    def _deploy_entity(self, entity_id: str, deploy_request: dict):
        """
        Generic method to deploy an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            deploy_request (dict): deployment request

        Returns:
            (dict): response
        """
        entity_id = self.validate_uuid(entity_id)

        self.required_params(["engineType"], deploy_request)

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{entity_id}/deploy",
            header_params=self._get_header_params(),
            query_params={},
            body=deploy_request,
        )

    def _entities_to_dataframe(self, entities: list) -> pandas.DataFrame | None:
        """
        Generic helper method to combine multiple entities into a single DataFrame.
        Works for Dataset, DatasetTemplate, and any other entity type.

        Parameters:
            entities (list): List of entity objects to combine

        Returns:
            DataFrame: Combined DataFrame containing all entities, or None if conversion fails
        """
        if not entities:
            return None

        try:
            from tmo.util.utils import to_dataframe

            combined_data = []
            for entity in entities:
                combined_data.append(entity.get_df_template())

            return to_dataframe(combined_data)
        except Exception as e:
            logger.error(
                f"Could not combine {camel_to_normalized(self.path)} to DataFrame:"
                f" {str(e)}"
            )
            return None

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def _get_standard_header_params(self, accept_types: list[str] = None):
        """
        Helper method to generate standard header parameters for API requests.

        Parameters:
            accept_types (list[str]): List of acceptable response types. If None, defaults to json_type only.

        Returns:
            (dict): generated header parameters
        """
        if accept_types is None:
            accept_value = self.json_type
        else:
            accept_value = self.tmo_client.select_header_accept(accept_types)

        header_vars = [
            "AOA-Project-ID",
            "VMO-Project-ID",
            "Content-Type",
            "Accept",
        ]  # AOA-Project-ID kept for backwards compatibility
        header_vals = [
            self.tmo_client.project_id,
            self.tmo_client.project_id,
            self.json_type,
            accept_value,
        ]

        return self.generate_params(header_vars, header_vals)

    def _parse_entity_from_dictionary(self, dictionary: dict) -> Any:
        """
        Helper method to parse an individual entity from API response data (dict).
        Must be implemented by child classes to convert raw response data into entity objects
        and provide functional behavior, these classes must use the @functional decorator.

        Returns:
            Parsed entity object
        """
        return dictionary

    def _reject_entity(self, entity_id: str, comments: str):
        """
        Generic method to reject an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            comments (str): rejection comments

        Returns:
            (dict): response
        """
        entity_id = self.validate_uuid(entity_id)

        reject_request = {"comments": comments}

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{entity_id}/reject",
            header_params=self._get_header_params(),
            query_params={},
            body=reject_request,
        )

    def _retire_entity(self, entity_id: str, retire_request: dict):
        """
        Generic method to retire an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            retire_request (dict): retire request

        Returns:
            (dict): response
        """
        entity_id = self.validate_uuid(entity_id)

        self.required_params(["deploymentId"], retire_request)

        return self.tmo_client.post_request(
            path=f"{self.base_path + self.path}/{entity_id}/retire",
            header_params=self._get_header_params(),
            query_params={},
            body=retire_request,
        )
