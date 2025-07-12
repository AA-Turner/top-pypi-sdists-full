#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.models.api_object import APIObject
from datarobot.utils.pagination import unpaginate

sidecar_model_metric_validation_trafaret = t.Dict(
    {
        t.Key("id"): t.String,
        t.Key("name"): t.String(allow_blank=True),
        t.Key("target_column_name", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("prompt_column_name", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("deployment_id"): t.String,
        t.Key("validation_status"): t.String,
        t.Key("model_id"): t.String,
        t.Key("deployment_access_data", optional=True, default=None): t.Or(
            t.Null,
            t.Dict(
                {
                    t.Key("prediction_api_url"): t.String,
                    t.Key("datarobot_key", optional=True, default=None): t.Or(t.Null, t.String),
                    t.Key("authorization_header"): t.String,
                    t.Key("input_type"): t.String,
                    t.Key("model_type"): t.String,
                }
            ).ignore_extra("*"),
        ),
        t.Key("tenant_id"): t.String,
        t.Key("user_id"): t.String,
        t.Key("creation_date"): t.String,
        t.Key("error_message", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("deployment_name", optional=True, default=None): t.Or(
            t.Null, t.String(allow_blank=True)
        ),
        t.Key("user_name", optional=True, default=None): t.Or(t.Null, t.String(allow_blank=True)),
        t.Key("use_case_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("prediction_timeout"): t.Int,
        t.Key("playground_id", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("citations_prefix_column_name", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("response_column_name", optional=True, default=None): t.Or(t.Null, t.String),
        t.Key("expected_response_column_name", optional=True, default=None): t.Or(t.Null, t.String),
    }
).ignore_extra("*")


class SidecarModelMetricValidation(APIObject):
    """A sidecar model metric validation for LLMs.

    Attributes
    ----------
    id : str
        The ID of the sidecar model metric validation.
    prompt_column_name : str
        The name of the prompt column for the sidecar model.
    deployment_id : str
        The ID of the deployment associated with the sidecar model.
    model_id : str
        The ID of the sidecar model.
    validation_status : str
        The status of the validation job.
    deployment_access_data : dict
        The data that will be used for accessing the deployment prediction server.
        This field is only available for deployments that pass validation.
        Dict fields are as follows:
        - prediction_api_url - The URL for the deployment prediction server.
        - datarobot_key - The first of two auth headers for the prediction server.
        - authorization_header - The second of two auth headers for the prediction server.
        - input_type - The input type the model expects, either JSON or CSV.
        - model_type - The target type of the deployed custom model.
    tenant_id : str
        The ID of the tenant that created the sidecar model metric validation.
    name : str
        The name of the sidecar model metric.
    creation_date : str
        The date the sidecar model metric validation was created.
    user_id : str
        The ID of the user that created the sidecar model metric validation.
    deployment_name : str
        The name of the deployment associated with the sidecar model.
    user_name : str
        The name of the user that created the sidecar model metric validation.
    use_case_id : str
        The ID of the Use Case associated with the sidecar model metric validation.
    prediction_timeout : int
        The timeout in seconds for the prediction API used in this sidecar model metric validation.
    error_message : str
        Additional information for the errored validation.
    citations_prefix_column_name : str
        The name of the prefix in the citations column for the sidecar model.
    response_column_name : str
        The name of the response column for the sidecar model.
    expected_response_column_name : str
        The name of the expected response column for the sidecar model.
    target_column_name : str
        The name of the target column for the sidecar model.
    """

    _path = "api/v2/genai/sidecarModelMetricValidations"

    _converter = sidecar_model_metric_validation_trafaret

    def __init__(
        self,
        id: str,
        playground_id: str,
        prompt_column_name: str,
        deployment_id: str,
        model_id: str,
        validation_status: str,
        deployment_access_data: Optional[Dict[str, Any]],
        tenant_id: str,
        name: str,
        creation_date: str,
        user_id: str,
        deployment_name: Optional[str],
        user_name: Optional[str],
        use_case_id: Optional[str],
        prediction_timeout: int,
        error_message: Optional[str],
        citations_prefix_column_name: Optional[str],
        response_column_name: Optional[str],
        target_column_name: Optional[str],
        expected_response_column_name: Optional[str],
    ):
        self.id = id
        self.playground_id = playground_id
        self.prompt_column_name = prompt_column_name
        self.deployment_id = deployment_id
        self.model_id = model_id
        self.validation_status = validation_status
        self.deployment_access_data = deployment_access_data
        self.tenant_id = tenant_id
        self.error_message = error_message
        self.name = name
        self.creation_date = creation_date
        self.user_id = user_id
        self.deployment_name = deployment_name
        self.user_name = user_name
        self.use_case_id = use_case_id
        self.prediction_timeout = prediction_timeout
        self.error_message = error_message
        self.citations_prefix_column_name = citations_prefix_column_name
        self.response_column_name = response_column_name
        self.target_column_name = target_column_name
        self.expected_response_column_name = expected_response_column_name

    @classmethod
    def create(
        cls,
        deployment_id: str,
        name: str,
        prediction_timeout: int,
        model_id: Optional[str] = None,
        use_case_id: Optional[str] = None,
        playground_id: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        response_column_name: Optional[str] = None,
        citation_prefix_column_name: Optional[str] = None,
        expected_response_column_name: Optional[str] = None,
    ) -> SidecarModelMetricValidation:
        """Create a sidecar model metric validation.

        Parameters
        ----------
        deployment_id : str
            The ID of the deployment to validate.
        name : str
            The name of the validation.
        prediction_timeout : int
            The timeout in seconds for the prediction API used in this validation.
        model_id : Optional[str]
            The ID of the model to validate.
        use_case_id : Optional[str]
            The ID of the Use Case associated with the validation.
        playground_id : Optional[str]
            The ID of the playground associated with the validation.
        prompt_column_name : Optional[str]
            The name of the prompt column for the sidecar model.
        target_column_name : Optional[str]
            The name of the target column for the sidecar model.
        response_column_name : Optional[str]
            The name of the response column for the sidecar model.
        citation_prefix_column_name : Optional[str]
            The name of the prefix for citations column for the sidecar model.
        expected_response_column_name : Optional[str]
            The name of the expected response column for the sidecar model.

        Returns
        -------
        SidecarModelMetricValidation
            The created sidecar model metric validation.
        """

        payload = {
            "deployment_id": deployment_id,
            "name": name,
            "prediction_timeout": prediction_timeout,
            "model_id": model_id,
            "use_case_id": use_case_id,
            "playground_id": playground_id,
            "prompt_column_name": prompt_column_name,
            "target_column_name": target_column_name,
            "response_column_name": response_column_name,
            "citation_prefix_column_name": citation_prefix_column_name,
            "expected_response_column_name": expected_response_column_name,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.post(url, data=payload)
        return cls.from_server_data(r_data.json())

    @classmethod
    def list(
        cls,
        use_case_ids: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        completed_only: Optional[bool] = True,
        deployment_id: Optional[str] = None,
        model_id: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        citation_prefix_column_name: Optional[str] = None,
    ) -> List[SidecarModelMetricValidation]:
        """List sidecar model metric validations.

        Parameters
        ----------
        use_case_ids : List[str], optional
            The IDs of the use cases to filter by.
        offset : Optional[int]
            The number of records to skip.
        limit : Optional[int]
            The maximum number of records to return.
        search : Optional[str]
            The search string.
        sort : Optional[str]
            The sort order.
        completed_only : Optional[bool]
            Whether to return only completed validations.
        deployment_id : Optional[str]
            The ID of the deployment to filter by.
        model_id : Optional[str]
            The ID of the model to filter by.
        prompt_column_name : Optional[str]
            The name of the prompt column to filter by.
        target_column_name : Optional[str]
            The name of the target column to filter by.
        citation_prefix_column_name : Optional[str]
            The name of the prefix for citations column to filter by.

        Returns
        -------
        List[SidecarModelMetricValidation]
            The list of sidecar model metric validations.

        """
        params = {
            "use_case_id": use_case_ids,
            "offset": offset,
            "limit": limit,
            "search": search,
            "sort": sort,
            "completed_only": completed_only,
            "deployment_id": deployment_id,
            "model_id": model_id,
            "prompt_column_name": prompt_column_name,
            "target_column_name": target_column_name,
            "citation_prefix_column_name": citation_prefix_column_name,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        response_data = unpaginate(url, params, cls._client)
        return [cls.from_server_data(data) for data in response_data]

    @classmethod
    def get(cls, validation_id: str) -> SidecarModelMetricValidation:
        """Get a sidecar model metric validation by ID.

        Parameters
        ----------
        validation_id : str
            The ID of the validation to get.

        Returns
        -------
        SidecarModelMetricValidation
            The sidecar model metric validation.
        """
        url = f"{cls._client.domain}/{cls._path}/{validation_id}/"
        response_data = cls._client.get(url)
        return cls.from_server_data(response_data.json())

    def revalidate(self) -> SidecarModelMetricValidation:
        """Revalidate the sidecar model metric validation.

        Returns
        -------
        SidecarModelMetricValidation
            The sidecar model metric validation.

        """
        url = f"{self._client.domain}/{self._path}/{self.id}/revalidate/"
        response_data = self._client.post(url)
        return self.from_server_data(response_data.json())

    def update(
        self,
        name: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        response_column_name: Optional[str] = None,
        expected_response_column_name: Optional[str] = None,
        citation_prefix_column_name: Optional[str] = None,
        deployment_id: Optional[str] = None,
        model_id: Optional[str] = None,
        prediction_timeout: Optional[int] = None,
    ) -> SidecarModelMetricValidation:
        """Update the sidecar model metric validation.

        Parameters
        ----------
        name : Optional[str]
            The name of the validation.
        prompt_column_name : Optional[str]
            The name of the prompt column for the sidecar model.
        target_column_name : Optional[str]
            The name of the target column for the sidecar model.
        response_column_name : Optional[str]
            The name of the response column for the sidecar model.
        expected_response_column_name : Optional[str]
            The name of the expected response column for the sidecar model.
        citation_prefix_column_name : Optional[str]
            The name of the prefix for citations column for the sidecar model.
        deployment_id : Optional[str]
            The ID of the deployment to validate.
        model_id : Optional[str]
            The ID of the model to validate.
        prediction_timeout : Optional[int]
            The timeout in seconds for the prediction API used in this validation.

        Returns
        -------
        SidecarModelMetricValidation
            The updated sidecar model metric validation.
        """
        payload = {
            "name": name,
            "prompt_column_name": prompt_column_name,
            "target_column_name": target_column_name,
            "deployment_id": deployment_id,
            "model_id": model_id,
            "prediction_timeout": prediction_timeout,
            "response_column_name": response_column_name,
            "citation_prefix_column_name": citation_prefix_column_name,
            "expected_response_column_name": expected_response_column_name,
        }
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        response = self._client.patch(url, data=payload)
        return self.from_server_data(response.json())

    def delete(self) -> None:
        """Delete the sidecar model metric validation."""
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        self._client.delete(url)
