#
# Copyright 2026 DataRobot, Inc. and its affiliates.
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

from typing import List, Optional, Union

from strenum import StrEnum
import trafaret as t

from datarobot.enums import enum_to_list
from datarobot.models.api_object import APIObject
from datarobot.models.genai.playground import Playground
from datarobot.models.use_cases.use_case import UseCase
from datarobot.models.use_cases.utils import UseCaseLike, get_use_case_id, resolve_use_cases
from datarobot.utils.pagination import unpaginate
from datarobot.utils.waiters import wait_for_async_resolution


class ExtraBodyParamStage(StrEnum):
    """Describes when parameter should be used, during VDB creation or prompting."""

    BOTH = "both"
    INDEXING = "indexing"
    PROMPTING = "prompting"


extra_body_param_trafaret = t.Dict({
    t.Key("key"): t.String,
    t.Key("value"): t.String,
    t.Key("stage"): t.Enum(*enum_to_list(ExtraBodyParamStage)),
}).ignore_extra("*")

openai_embedding_model_validation_trafaret = t.Dict({
    t.Key("id"): t.String,
    t.Key("name"): t.String,
    t.Key("validation_status"): t.String,
    t.Key("model"): t.String,
    t.Key("base_url"): t.String,
    t.Key("credential_id", optional=True, default=None): t.Or(t.Null, t.String),
    t.Key("tenant_id"): t.String,
    t.Key("user_id"): t.String,
    t.Key("creation_date"): t.String,
    t.Key("extra_body_params", optional=True, default=None): t.Or(t.Null, t.List(extra_body_param_trafaret)),
    t.Key("error_message", optional=True, default=None): t.Or(t.Null, t.String),
    t.Key("user_name", optional=True, default=None): t.Or(t.Null, t.String(allow_blank=True)),
    t.Key("use_case_id", optional=True, default=None): t.Or(t.Null, t.String),
}).ignore_extra("*")


def get_entity_id(entity: Union[Playground, str]) -> str:
    """
    Get the entity ID from the entity parameter.

    Parameters
    ----------
    entity : APIObject or str
        Specifies either the entity ID or the entity.

    Returns
    -------
    id : str
        The entity ID.
    """
    return entity if isinstance(entity, str) else entity.id


class ExtraBodyParam(APIObject):
    def __init__(self, key: str, value: str, stage: ExtraBodyParamStage):
        self.key = key
        self.value = value
        self.stage = stage


class OpenAIEmbeddingModelValidation(APIObject):
    _converter = openai_embedding_model_validation_trafaret
    _path = "api/v2/genai/openaiEmbeddingValidations"

    def __init__(
        self,
        id: str,
        model: str,
        base_url: str,
        validation_status: str,
        tenant_id: str,
        name: str,
        creation_date: str,
        user_id: str,
        credential_id: Optional[str],
        error_message: Optional[str],
        user_name: Optional[str],
        use_case_id: Optional[str],
        extra_body_params: Optional[List[ExtraBodyParam]],
    ):
        self.id = id
        self.model = model
        self.base_url = base_url
        self.credential_id = credential_id
        self.validation_status = validation_status
        self.tenant_id = tenant_id
        self.error_message = error_message
        self.name = name
        self.creation_date = creation_date
        self.user_id = user_id
        self.user_name = user_name
        self.use_case_id = use_case_id
        self.extra_body_params = extra_body_params

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"

    @classmethod
    def create(
        cls,
        name: str,
        model: str,
        base_url: str,
        use_case: Union[UseCase, str],
        credential_id: str,
        extra_body_params: Optional[List[ExtraBodyParam]] = None,
        wait_for_completion: bool = False,
    ) -> OpenAIEmbeddingModelValidation:
        """
        Start the validation of the OpenAI-compatible embedding model.

        Parameters
        ----------
        model : str
            The name of the validated OpenAI embeddings model.
        base_url : str
            Base URL to OpenAI-compatible deployment.
        credential_id : str
            The ID of credentials that hold token for OpenAI-compatible deployment.
        use_case : Union[UseCase, str]
            The Use Case to link the validation to, either `UseCase` or the Use Case ID.
        name : str
            The name of the validation.
        extra_body_params: list
            Parameters used as `extra_body` in request to OpenAI-compatible embeddings model.
        wait_for_completion : bool
            If set to `True`, the code will wait for the validation job to complete before returning
            results. If the job does not finish in 10 minutes, this method call raises a timeout
            error.
            If set to `False`, the code does not wait for the job to complete. Instead,
            `OpenAIEmbeddingModelValidation.get` can be used to poll for the status of the job using
            the validation ID returned by the method.

        Returns
        -------
        OpenAIEmbeddingModelValidation
        """

        payload = {
            "name": name,
            "model": model,
            "base_url": base_url,
            "credential_id": credential_id,
            "use_case_id": get_use_case_id(use_case, is_required=True),
            "extra_body_params": extra_body_params,
        }

        url = f"{cls._client.domain}/{cls._path}/"
        response = cls._client.post(url, data=payload)

        if wait_for_completion:
            location = wait_for_async_resolution(cls._client, response.headers["Location"])
            return cls.from_location(location)

        return cls.from_server_data(response.json())

    @classmethod
    def get(cls, validation_id: str) -> OpenAIEmbeddingModelValidation:
        """
        Get the OpenAI-compatible embedding model validation record by ID.

        Parameters
        ----------
        validation_id : str
            ID of OpenAIEmbeddingModelValidation to retrieve.

        Returns
        -------
        OpenAIEmbeddingModelValidation
        """

        url = f"{cls._client.domain}/{cls._path}/{validation_id}/"
        response = cls._client.get(url)
        return cls.from_server_data(response.json())

    @classmethod
    def list(
        cls,
        use_cases: Optional[UseCaseLike] = None,
        playground: Optional[Union[Playground, str]] = None,
        model: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        completed_only: bool = True,
    ) -> List[OpenAIEmbeddingModelValidation]:
        """
        List the validation records by field values.

        Parameters
        ----------
        model : str, optional
            The name of embeddings model.
        use_cases : list[Union[UseCase, str]], optional
            The returned validations are filtered to those associated with specific Use Cases
            if specified, either `UseCase` objects or the Use Case IDs.
        playground : Union[Playground, str], optional
            The returned validations are filtered to those used in a specific playground
            if specified, either `Playground` or playground ID.
        completed_only : bool
            Whether to retrieve only completed validations.
        search : str, optional
            String for filtering validations.
            Validations that contain the string in name will be returned.
        sort : str, optional
            Property to sort validations by.
            Prefix the attribute name with a dash to sort in descending order,
            e.g., sort='-name'.
            Currently supported options are listed in ListOpenAIEmbeddingValidationSortQueryParam
            but the values can differ with different platform versions.
            By default, the sort parameter is None which will result in
            validations being returned in order of creation time descending.

        Returns
        -------
        List[OpenAIEmbeddingModelValidation]
        """

        url = f"{cls._client.domain}/{cls._path}/"
        params = {
            "model": model,
            "playground_id": get_entity_id(playground) if playground else None,
            "completed_only": completed_only,
            "search": search,
            "sort": sort or "-creationDate",
        }
        params = resolve_use_cases(use_cases=use_cases, params=params, use_case_key="use_case_id")
        r_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in r_data]

    def update(
        self,
        name: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        credential_id: Optional[str] = None,
        extra_body_params: Optional[List[ExtraBodyParam]] = None,
    ) -> OpenAIEmbeddingModelValidation:
        """
        Update a OpenAI-compatible embedding model validation.

        Parameters
        ----------
        name : str, optional
            The new name of the validation.
        model : str, optional
            The new model within the deployment to validate.
        base_url  : str, optional
            Base URL to OpenAI-compatible deployment.
        credential_id : str, optional
            The ID of credentials that hold token for OpenAI-compatible deployment.
        extra_body_params : list, optional
            Parameters used as `extra_body` in request to OpenAI-compatible embeddings model.
            If empty list is passed then all existing `extra_body_params` will be erased.

        Returns
        -------
        OpenAIEmbeddingModelValidation
        """
        payload = {
            "name": name,
            "model": model,
            "base_url": base_url,
            "credential_id": credential_id,
            "extra_body_params": extra_body_params,
        }

        url = f"{self._client.domain}/{self._path}/{self.id}/"
        response = self._client.patch(url, data=payload)
        return self.from_server_data(response.json())

    def delete(self) -> None:
        """
        Delete the OpenAI-compatible embedding model validation.
        """
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)
