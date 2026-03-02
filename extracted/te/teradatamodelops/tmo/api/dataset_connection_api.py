from __future__ import absolute_import

from typing import Any

from tmo.api.iterator_base_api import IteratorBaseApi


class DatasetConnectionApi(IteratorBaseApi):
    path = "/api/datasetConnections"
    type = "DATASET_CONNECTION"

    def find_by_archived(
        self,
        archived: bool = False,
        projection: str = None,
        page: int = None,
        size: int = None,
        sort: str = None,
    ):
        raise NotImplementedError("Archiving not supported for DatasetConnections")

    def _get_header_params(self):
        return self._get_standard_header_params(
            accept_types=[
                self.json_type,
                "application/hal+json",
                "text/uri-list",
                "application/x-spring-data-compact+json",
            ]
        )

    def save(
        self,
        name: str,
        description: str,
        val_db: str,
        byom_db: str,
        password: str,
        personal: bool = True,
        creds_encrypted: bool = False,
        context: Any = None,
        log_mech: str = "TDNEGO",
        host: str = None,
        database: str = None,
        username: str = None,
    ):
        """
        register a dataset connection

        Parameters:
            name (str): dataset name
            description (str): dataset description
            val_db (str): val database
            byom_db (str): byom database
            password (str): password for Teradata Vantage connection
            personal (bool): flag to indicate if the dataset connection is personal
            creds_encrypted (bool): flag to indicate if credentials are encrypted
            context (any): teradataml context object containing connection information
            log_mech (str): log mechanism for Teradata Vantage connection. Default is "TDNEGO". Options are TDNEGO, TD2, LDAP, KRBS.
            host (str): Teradata Vantage host
            database (str): Teradata Vantage database
            username (str): Teradata Vantage username

        Raises:
            ValueError: If context is not provided and host, database, and username are not specified.
            HTTPError: If the request fails

        Returns:
            (dict): dataset template
        """

        if context:
            username = context.url.username
            host = context.url.host
            database = context.url.database
        else:
            if not all([host, database, username]):
                raise ValueError(
                    "If context is not provided, 'host', 'database', and 'username'"
                    " must be specified."
                )

        dataset_connection = {
            "name": name,
            "description": description,
            "metadata": {
                "host": host,
                "log_mech": log_mech,
                "database": database,
                "valDb": val_db,
                "byomDb": byom_db,
            },
            "credentials": {
                "username": username,
                "password": password,
                "credsEncrypted": creds_encrypted,
            },
            "personal": personal,
        }

        return self.tmo_client.post_request(
            path=self.path,
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_connection,
        )

    def validate(
        self, dataset_connection: dict[str, Any], encrypted_credentials: bool = False
    ):
        """
        validate a dataset connection

        Parameters:
           dataset_connection (dict): dataset connection to validate
           encrypted_credentials (bool): flag to indicate if credentials are encrypted

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """

        dataset_connection["credentials"]["credsEncrypted"] = encrypted_credentials

        return self.tmo_client.post_request(
            path=f"{self.path}/validate",
            header_params=self._get_header_params(),
            query_params={},
            body=dataset_connection,
        )
