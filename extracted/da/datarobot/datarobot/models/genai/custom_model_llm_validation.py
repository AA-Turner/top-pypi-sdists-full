#
# Copyright 2023-2025 DataRobot, Inc. and its affiliates.
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

from typing import Any, Dict, Optional, Union

import trafaret as t

from datarobot.models.deployment import Deployment
from datarobot.models.genai.custom_model_validation import (
    custom_model_validation_trafaret,
    CustomModelValidation,
    get_entity_id,
)
from datarobot.models.model import Model
from datarobot.models.use_cases.use_case import UseCase
from datarobot.models.use_cases.utils import get_use_case_id
from datarobot.utils.waiters import wait_for_async_resolution

custom_model_llm_validation_trafaret = (
    t.Dict(
        {
            t.Key("chat_model_id", optional=True, default=None): t.Or(t.Null, t.String),
        }
    )
    .merge(custom_model_validation_trafaret)
    .ignore_extra("*")
)


class CustomModelLLMValidation(CustomModelValidation):
    """
    Validation record checking the ability of the deployment to serve
    as a custom model LLM.

    Attributes
    ----------
    id : str
        The ID of the validation.
    prompt_column_name : str
        The name of the column the deployed model uses for prompt text input.
    target_column_name : str
        The name of the column the deployed model uses for prediction output.
    chat_model_id : Optional[str]
        The model ID to specify when calling the chat completion API of the deployment.
    deployment_id : str
        The ID of the deployment.
    model_id : str
        The ID of the underlying deployed model, which can be found using `Deployment.model["id"]`.
    validation_status : str
        Can be TESTING, FAILED, or PASSED. Only PASSED is allowed for use.
    deployment_access_data : dict, optional
        The data that will be used for accessing the deployment prediction server.
        This field is only available for deployments that pass validation.
        Dict fields are as follows:
        - prediction_api_url - The URL for the deployment prediction server.
        - datarobot_key - The first of two auth headers for the prediction server.
        - authorization_header - The second of two auth headers for the prediction server.
        - input_type - The input type the model expects, either JSON or CSV.
        - model_type - The target type of the deployed custom model.
    tenant_id : str
        The creating user's tenant ID.
    name : str
        The display name of the validated custom model.
    creation_date : str
        The creation date of the validation (ISO 8601 formatted).
    user_id : str
        The ID of the creating user.
    error_message : Optional[str]
        Additional information for the errored validation.
    deployment_name : Optional[str]
        The name of the validated deployment.
    user_name : Optional[str]
        The name of the creating user.
    use_case_id : Optional[str]
        The ID of the Use Case associated with the validation.
    prediction_timeout: int
        The timeout in seconds for the prediction API used in this custom model validation.
    """

    _path = "api/v2/genai/customModelLLMValidations"
    _converter = custom_model_llm_validation_trafaret

    def __init__(
        self,
        id: str,
        prompt_column_name: str,
        target_column_name: str,
        chat_model_id: Optional[str],
        deployment_id: str,
        model_id: str,
        validation_status: str,
        deployment_access_data: Optional[Dict[str, Any]],
        tenant_id: str,
        name: str,
        creation_date: str,
        user_id: str,
        error_message: Optional[str],
        deployment_name: Optional[str],
        user_name: Optional[str],
        use_case_id: Optional[str],
        prediction_timeout: int,
    ):
        super().__init__(
            id=id,
            prompt_column_name=prompt_column_name,
            target_column_name=target_column_name,
            deployment_id=deployment_id,
            model_id=model_id,
            validation_status=validation_status,
            deployment_access_data=deployment_access_data,
            tenant_id=tenant_id,
            name=name,
            creation_date=creation_date,
            user_id=user_id,
            error_message=error_message,
            deployment_name=deployment_name,
            user_name=user_name,
            use_case_id=use_case_id,
            prediction_timeout=prediction_timeout,
        )
        self.id = id
        self.prompt_column_name = prompt_column_name
        self.target_column_name = target_column_name
        self.chat_model_id = chat_model_id
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

    @classmethod
    def create(
        cls,
        deployment_id: Union[Deployment, str],
        model: Optional[Union[Model, str]] = None,
        use_case: Optional[Union[UseCase, str]] = None,
        name: Optional[str] = None,
        wait_for_completion: bool = False,
        prediction_timeout: Optional[int] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        chat_model_id: Optional[str] = None,
    ) -> CustomModelLLMValidation:
        """
        Start the validation of the deployment that will serve as an LLM.

        Parameters
        ----------
        deployment_id : Union[Deployment, str]
            The deployment to validate, either `Deployment` or the deployment ID.
        model : Optional[Union[Model, str]], optional
            The specific model within the deployment, either `Model` or the model ID.
            If not specified, the underlying model ID will be automatically derived from the
            deployment information.
        use_case : Optional[Union[UseCase, str]], optional
            The Use Case to link the validation to, either `UseCase` or the Use Case ID.
        name : Optional[str], optional
            The name of the validation.
        wait_for_completion : bool
            If set to `True`, the code will wait for the validation job to complete before returning
            results. If the job does not finish in 10 minutes, this method call raises a timeout
            error.
            If set to `False`, the code does not wait for the job to complete. Instead,
            `CustomModelLLMValidation.get` can be used to poll for the status of the job using
            the validation ID returned by the method.
        prediction_timeout : Optional[int], optional
            The timeout, in seconds, for the prediction API used in this custom model validation.
        prompt_column_name : Optional[str], optional
            The name of the column the deployed model uses for prompt text input.
            This value is used to call the Prediction API of the deployment.
            For LLM deployments that support the chat completion API, it is recommended to
            specify `chatModelId` instead.
        target_column_name : Optional[str], optional
            The name of the column the deployed model uses for prediction output.
            This value is used to call the Prediction API of the deployment.
            For LLM deployments that support the chat completion API, it is recommended to
            specify `chatModelId` instead.
        chat_model_id : Optional[str], optional
            The model ID to specify when calling the chat completion API of the deployment.
            If this parameter is specified, the deployment must support the chat completion API.

        Returns
        -------
        CustomModelLLMValidation
        """

        payload = {
            "prompt_column_name": prompt_column_name,
            "target_column_name": target_column_name,
            "chat_model_id": chat_model_id,
            "deployment_id": get_entity_id(deployment_id),
            "model_id": get_entity_id(model) if model else None,
            "use_case_id": get_use_case_id(use_case, is_required=False),
            "name": name,
        }
        if prediction_timeout is not None:
            payload["prediction_timeout"] = prediction_timeout  # type: ignore[assignment]
        url = f"{cls._client.domain}/{cls._path}/"
        response = cls._client.post(url, data=payload)
        if wait_for_completion:
            location = wait_for_async_resolution(cls._client, response.headers["Location"])
            return cls.from_location(location)
        return cls.from_server_data(response.json())

    def update(
        self,
        name: Optional[str] = None,
        prompt_column_name: Optional[str] = None,
        target_column_name: Optional[str] = None,
        chat_model_id: Optional[str] = None,
        deployment: Optional[Union[Deployment, str]] = None,
        model: Optional[Union[Model, str]] = None,
        prediction_timeout: Optional[int] = None,
    ) -> CustomModelLLMValidation:
        """
        Update a custom model validation.

        Parameters
        ----------
        name : Optional[str], optional
            The new name of the custom model validation.
        prompt_column_name : Optional[str], optional
            The new name of the prompt column.
        target_column_name : Optional[str], optional
            The new name of the target column.
        chat_model_id : Optional[str], optional
            The new model ID to specify when calling the chat completion API of the deployment.
        deployment : Optional[Union[Deployment, str]]
            The new deployment to validate.
        model : Optional[Union[Model, str]], optional
            The new model within the deployment to validate.
        prediction_timeout : Optional[int], optional
            The new timeout, in seconds, for the prediction API used in this custom model validation.

        Returns
        -------
        CustomModelLLMValidation
        """
        payload = {
            "name": name,
            "prompt_column_name": prompt_column_name,
            "target_column_name": target_column_name,
            "chat_model_id": chat_model_id,
            "deployment_id": get_entity_id(deployment) if deployment else None,
            "model_id": get_entity_id(model) if model else None,
            "prediction_timeout": prediction_timeout,
        }
        url = f"{self._client.domain}/{self._path}/{self.id}/"
        response = self._client.patch(url, data=payload)
        return self.from_server_data(response.json())
