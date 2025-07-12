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

from datarobot.models.genai.custom_model_validation import NonChatAwareCustomModelValidation


class CustomModelEmbeddingValidation(NonChatAwareCustomModelValidation):
    """
    Validation record checking the ability of the deployment to serve as a custom model embedding.

    Attributes
    ----------
    id : str
        The ID of the validation.
    prompt_column_name : str
        The column name the deployed model expect as the input.
    target_column_name : str
        The target name that the deployed model will output.
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

    _path = "api/v2/genai/customModelEmbeddingValidations"
