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
from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot._compat import String
from datarobot.models.api_object import APIObject
from datarobot.models.execution_environment_version import ExecutionEnvironmentVersion
from datarobot.models.sharing import SharingAccess
from datarobot.utils.pagination import unpaginate


class RequiredMetadataKey(APIObject):
    """Definition of a metadata key that custom models using this environment must define

    .. versionadded:: v2.25

    Attributes
    ----------
    field_name: str
        The required field key. This value will be added as an environment
        variable when running custom models.
    display_name: str
        A human readable name for the required field.
    """

    _converter = t.Dict({t.Key("field_name"): String(), t.Key("display_name"): String()})

    schema = _converter

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return "{}(field_name={!r}, display_name={!r})".format(
            self.__class__.__name__,
            self.field_name,
            self.display_name,
        )

    def _set_values(self, field_name, display_name):
        self.field_name = field_name
        self.display_name = display_name

    def to_dict(self):
        return self._converter.check(
            {"field_name": self.field_name, "display_name": self.display_name}
        )


class ExecutionEnvironment(APIObject):
    """An execution environment entity.

    .. versionadded:: v2.21

    Attributes
    ----------
    id: str
        The ID of the execution environment.
    name: str
        The name of the execution environment.
    description: Optional[str]
        The description of the execution environment.
    programming_language: Optional[str]
        The programming language of the execution environment.
        Can be "python", "r", "java" or "other".
    is_public: Optional[bool]
        Public accessibility of environment, visible only for admin user.
    created_at: Optional[str]
        ISO-8601 formatted timestamp of when the execution environment version was created.
    latest_version: ExecutionEnvironmentVersion, optional
        The latest version of the execution environment.
    latest_successful_version: ExecutionEnvironmentVersion, optional
        The latest version of the execution environment, which contains a successfully built image.
    required_metadata_keys: Optional[List[RequiredMetadataKey]]
        The definition of metadata keys that custom models using this environment must define.
    use_cases: Optional[List[str]]
        A list of use-cases this environment may be used for.
    """

    _path = "executionEnvironments/"
    _converter = t.Dict(
        {
            t.Key("id"): String(),
            t.Key("name"): String(max_length=255),
            t.Key("description", optional=True): t.Or(
                String(max_length=10000, allow_blank=True), t.Null()
            ),
            t.Key("programming_language", optional=True): String(),
            t.Key("is_public", optional=True): t.Bool(),
            t.Key("created", optional=True) >> "created_at": String(),
            t.Key("latest_version", optional=True): ExecutionEnvironmentVersion.schema,
            t.Key("latest_successful_version", optional=True): ExecutionEnvironmentVersion.schema,
            t.Key("required_metadata_keys", optional=True, default=list): t.List(
                RequiredMetadataKey.schema
            ),
            t.Key("use_cases", optional=True, default=list): t.List(String()),
        }
    ).ignore_extra("*")

    def __init__(self, **kwargs):
        self._set_values(**kwargs)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name or self.id!r})"

    def _set_values(  # pylint: disable=missing-function-docstring
        self,
        id,
        name,
        description=None,
        programming_language=None,
        is_public=None,
        created_at=None,
        latest_version=None,
        latest_successful_version=None,
        required_metadata_keys=None,
        use_cases=None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.programming_language = programming_language
        self.is_public = is_public
        self.created_at = created_at
        self.latest_version = None
        self.latest_successful_version = None
        self.required_metadata_keys = [
            RequiredMetadataKey.from_data(key) for key in required_metadata_keys
        ]
        self.use_cases = use_cases

        if latest_version is not None:
            self.latest_version = ExecutionEnvironmentVersion(**latest_version)

        if latest_successful_version is not None:
            self.latest_successful_version = ExecutionEnvironmentVersion(
                **latest_successful_version
            )

    @classmethod
    def create(
        cls,
        name,
        description=None,
        programming_language=None,
        required_metadata_keys=None,
        is_public=None,
        use_cases=None,
    ):
        """Create an execution environment.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: str
            execution environment name
        description: Optional[str]
            execution environment description
        programming_language: Optional[str]
            programming language of the environment to be created.
            Can be "python", "r", "java" or "other". Default value - "other"
        required_metadata_keys: List[RequiredMetadataKey]
            Definition of a metadata keys that custom models using this environment must define
        is_public: bool, optional
            public accessibility of environment
        use_cases: List[str], optional
             List of use-cases this environment may be used for

        Returns
        -------
        ExecutionEnvironment
            created execution environment

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        required_metadata_keys = required_metadata_keys or []
        payload = {
            "name": name,
            "description": description,
            "programming_language": programming_language,
            "is_public": is_public,
            "use_cases": use_cases,
        }
        if required_metadata_keys:
            payload["required_metadata_keys"] = [key.to_dict() for key in required_metadata_keys]
        response = cls._client.post(cls._path, data=payload)
        environment_id = response.json()["id"]
        return cls.get(environment_id)

    @classmethod
    def list(
        cls,
        search_for=None,
        is_own: Optional[bool] = None,
        use_cases: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 0,
    ):
        """List execution environments available to the user.

        .. versionadded:: v2.21

        Parameters
        ----------
        search_for: Optional[str]
            the string for filtering execution environment - only execution
            environments that contain the string in name or description will
            be returned.
        is_own: bool, optional
            Only return execution environments that were created by the current user.
        use_cases: str, optional
            Only return execution environments that contain the specified use case
        offset: Optional[int]
            The starting offset of the results. The default is 0.
        limit: Optional[int]
            The maximum number of objects to return. The default is 0 to maintain previous behavior.
            The default on the server is 20, with a maximum of 100.

        Returns
        -------
        List[ExecutionEnvironment]
            a list of execution environments.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        param: Dict[str, Any] = {"search_for": search_for}
        if is_own is not None:
            param["is_own"] = is_own
        if use_cases is not None:
            param["use_cases"] = use_cases

        if limit == 0:
            data = unpaginate(cls._path, param, cls._client)
        else:
            param["limit"] = limit
            param["offset"] = offset
            response = cls._client.get(cls._path, params=param).json()
            data = response["data"]

        return [cls.from_server_data(item) for item in data]

    @classmethod
    def get(cls, execution_environment_id):
        """Get execution environment by its ID.

        .. versionadded:: v2.21

        Parameters
        ----------
        execution_environment_id: str
            ID of the execution environment to retrieve

        Returns
        -------
        ExecutionEnvironment
            retrieved execution environment

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        path = f"{cls._path}{execution_environment_id}/"
        return cls.from_location(path)

    def delete(self):
        """Delete execution environment.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = f"{self._path}{self.id}/"
        self._client.delete(url)

    def update(
        self,
        name=None,
        description=None,
        required_metadata_keys=None,
        is_public=None,
        use_cases=None,
    ):
        """Update execution environment properties.

        .. versionadded:: v2.21

        Parameters
        ----------
        name: Optional[str]
            new execution environment name
        description: Optional[str]
            new execution environment description
        required_metadata_keys: List[RequiredMetadataKey]
            Definition of a metadata keys that custom models using this environment must define
        is_public: bool, optional
            public accessibility of environment
        use_cases: List[str], optional
             List of use-cases this environment may be used for

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        payload = {"name": name, "description": description}
        if required_metadata_keys is not None:
            payload["required_metadata_keys"] = [key.to_dict() for key in required_metadata_keys]
        if is_public is not None:
            payload["is_public"] = is_public
        if use_cases is not None:
            payload["use_cases"] = use_cases

        url = f"{self._path}{self.id}/"
        response = self._client.patch(url, data=payload)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def refresh(self):
        """Update execution environment with the latest data from server.

        .. versionadded:: v2.21

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status
        """
        url = f"{self._path}{self.id}/"
        response = self._client.get(url)

        data = response.json()
        self._set_values(**self._safe_data(data, do_recursive=True))

    def get_access_list(self) -> List[SharingAccess]:
        """Retrieve access control settings of this environment.

        .. versionadded:: v2.36

        Returns
        -------
        list of :class:`SharingAccess <datarobot.SharingAccess>`
        """
        url = f"{self._path}{self.id}/accessControl/"
        return [
            SharingAccess.from_server_data(datum) for datum in unpaginate(url, {}, self._client)
        ]

    def share(self, access_list: List[SharingAccess]) -> None:
        """Update the access control settings of this execution environment.

        .. versionadded:: v2.36

        Parameters
        ----------
        access_list : list of :class:`SharingAccess <datarobot.ExecutionEnvironment>`
            A list of SharingAccess to update.

        Raises
        ------
        datarobot.errors.ClientError
            if the server responded with 4xx status
        datarobot.errors.ServerError
            if the server responded with 5xx status

        Examples
        --------
        Transfer access to the execution environment from old_user@datarobot.com to new_user@datarobot.com

        .. code-block:: python

            import datarobot as dr

            new_access = dr.SharingAccess(new_user@datarobot.com,
                                          dr.enums.SHARING_ROLE.OWNER, can_share=True)
            access_list = [dr.SharingAccess(old_user@datarobot.com, None), new_access]

            dr.ExecutionEnvironment.get('environment-id').share(access_list)
        """
        payload = {
            "data": [access.collect_payload() for access in access_list],
        }
        nullable_query_params = {"role"}
        self._client.patch(
            f"{self._path}{self.id}/accessControl/",
            data=payload,
            keep_attrs=nullable_query_params,
        )
