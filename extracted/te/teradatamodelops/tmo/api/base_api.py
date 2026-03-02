from __future__ import absolute_import

import abc

from tmo.api_client import TmoClient


class BaseApi(object):
    path = ""
    json_type = "application/json"

    def __init__(self, tmo_client: TmoClient):
        self.tmo_client = tmo_client

    @abc.abstractmethod  # noqa
    def _get_header_params(self):
        pass

    def _get_standard_header_params(self, accept_types: list[str] = None):
        """
        Helper method to generate standard header parameters for API requests.

        Parameters:
            accept_types (list[str]): List of acceptable response types.
                                     If None, defaults to json_type only.

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

    def _approve_entity(self, entity_id: str, comments: str):
        """
        Generic method to approve an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            comments (str): approval comments

        Returns:
            (dict): response
        """
        approve_request = {"comments": comments}

        return self.tmo_client.post_request(
            path=f"{self.path}/{entity_id}/approve",
            header_params=self._get_header_params(),
            query_params={},
            body=approve_request,
        )

    def _reject_entity(self, entity_id: str, comments: str):
        """
        Generic method to reject an entity (trained model, feature engineering task, etc.)

        Parameters:
            entity_id (str): entity id(uuid)
            comments (str): rejection comments

        Returns:
            (dict): response
        """
        reject_request = {"comments": comments}

        return self.tmo_client.post_request(
            path=f"{self.path}/{entity_id}/reject",
            header_params=self._get_header_params(),
            query_params={},
            body=reject_request,
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
        self.required_params(["engineType"], deploy_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{entity_id}/deploy",
            header_params=self._get_header_params(),
            query_params={},
            body=deploy_request,
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
        self.required_params(["deploymentId"], retire_request)

        return self.tmo_client.post_request(
            path=f"{self.path}/{entity_id}/retire",
            header_params=self._get_header_params(),
            query_params={},
            body=retire_request,
        )

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

        return self.tmo_client.get_request(self.path, header_params, query_params)

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
           projection (str): projection type
           page (int): page number
           size (int): number of records in a page
           sort (str): column name and sorting order e.g. name?asc / name?desc
           archived (bool): whether to return archived or unarchived entities

        Returns:
            (dict): all entities
        """
        header_params = self._get_header_params()

        query_vars = ["projection", "page", "size", "sort", "archived"]
        query_vals = [projection, page, size, sort, archived]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.path}/search/findByArchived", header_params, query_params
        )

    def find_by_id(self, id: str, projection: str = None):
        """
        returns the entity

        Parameters:
           id (str): entity id(uuid) to find
           projection (str): projection type

        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        query_vars = ["projection"]
        query_vals = [projection]
        query_params = self.generate_params(query_vars, query_vals)

        return self.tmo_client.get_request(
            f"{self.path}/{id}", header_params, query_params
        )

    def archive(self, id: str):
        """
        archives the entity
        Parameters:
           id (str): entity id(uuid) to archive
        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        return self.tmo_client.post_request(
            f"/api/archives/{self.type}/{id}", header_params, {}, {}
        )

    def unarchive(self, id: str):
        """
        unarchives the entity
        Parameters:
           id (str): entity id(uuid) to unarchive
        Returns:
            (dict): entity
        """
        header_params = self._get_header_params()

        return self.tmo_client.delete_request(
            f"/api/archives/{self.type}/{id}", header_params, {}, {}
        )
