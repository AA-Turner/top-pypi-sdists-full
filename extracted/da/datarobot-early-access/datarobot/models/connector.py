#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.models.api_object import APIObject

from ..enums import DEFAULT_MAX_WAIT, DataTypes
from ..utils import get_id_from_location
from ..utils.waiters import wait_for_async_resolution


class Connector(APIObject):
    """A connector.

    Attributes
    ----------
    id : str
        The ID of the connector.
    creator_id : str
        The ID of the user who created the connector.
    base_name : str
        The filename of the jar file.
    canonical_name : str
        The user-friendly name of the connector.
    configuration_id : str
        The ID of the configuration of the connector.
    """

    _path = "externalConnectors/"
    _converter = t.Dict({
        t.Key("id"): String(),
        t.Key("creator_id"): String(),
        t.Key("configuration_id"): String(),
        t.Key("base_name", optional=True): t.Or(String, t.Null),
        t.Key("canonical_name"): String(),
        t.Key("connector_type", optional=True): t.Or(String, t.Null),
    }).allow_extra("*")

    def __init__(
        self,
        id: Optional[str] = None,
        creator_id: Optional[str] = None,
        configuration_id: Optional[str] = None,
        base_name: Optional[str] = None,
        canonical_name: Optional[str] = None,
        connector_type: Optional[str] = None,
    ):
        self._id = id
        self._creator_id = creator_id
        self._configuration_id = configuration_id
        self._base_name = base_name
        self._canonical_name = canonical_name
        self._connector_type = connector_type

    @classmethod
    def list(cls, data_type: Optional[DataTypes] = None) -> List[Connector]:
        """
        Returns a list of available connectors.

        Parameters
        ----------
        data_type : DataTypes
            If specified, returns the connectors that support the specified data type. If not
            specified, defaults to ``DataTypes.ALL``.

        Returns
        -------
        connectors : list of Connector instances
            Contains a list of available connectors.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> connectors = dr.Connector.list()
            >>> connectors
            [Connector('Google Drive'), Connector('S3')]
        """
        if data_type is not None:
            r_data = cls._client.get(cls._path, params={"dataType": str(data_type)}).json()
        else:
            r_data = cls._client.get(cls._path).json()
        return [cls.from_server_data(item) for item in r_data["data"]]

    @classmethod
    def get(cls, connector_id: str) -> Connector:
        """
        Gets the connector.

        Parameters
        ----------
        connector_id : str
            The identifier of the connector.

        Returns
        -------
        connector : Connector
            The required connector.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> connector = dr.Connector.get('5fe1063e1c075e0245071446')
            >>> connector
            Connector('Google Drive')
        """
        return cls.from_location(f"{cls._path}{connector_id}/")

    @classmethod
    def create(cls, *, connector_type: str) -> Connector:
        """
        Creates the connector from a jar file. Only available to administrator users.

        Parameters
        ----------
        connector_type: str
            The type of the native connector to create.

        Returns
        -------
        connector : Connector
            The created connector.

        Raises
        ------
        ClientError
            Raised if the user is not granted the `Can manage connectors` feature.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> connector = dr.Connector.create(connector_type='gdrive')
            >>> connector
            Connector('Google Drive')
        """
        resp = cls._client.post(cls._path, data={"connector_type": connector_type})
        if resp.status_code == 202:
            finished_location = wait_for_async_resolution(
                cls._client, resp.headers["Location"], max_wait=DEFAULT_MAX_WAIT
            )
            return cls.get(get_id_from_location(finished_location))
        return cls.from_server_data(resp.json())

    def delete(self) -> None:
        """
        Removes the connector. Only available to administrator users.

        Raises
        ------
        ClientError
            Raised if the user is not granted the `Can manage connectors` feature.
        """
        self._client.delete(f"{self._path}{self.id}/")

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def creator(self) -> Optional[str]:
        return self._creator_id

    @property
    def configuration_id(self) -> Optional[str]:
        return self._configuration_id

    @property
    def base_name(self) -> Optional[str]:
        return self._base_name

    @property
    def canonical_name(self) -> Optional[str]:
        return self._canonical_name

    @property
    def connector_type(self) -> Optional[str]:
        return self._connector_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.canonical_name or self.id}')"
