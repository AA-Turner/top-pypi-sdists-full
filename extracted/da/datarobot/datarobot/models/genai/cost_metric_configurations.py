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

from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot.models.api_object import APIObject

llm_cost_configuration = t.Dict(
    {
        t.Key("input_token_price"): t.Float,
        t.Key("reference_input_token_count"): t.Int,
        t.Key("output_token_price"): t.Float,
        t.Key("reference_output_token_count"): t.Int,
        t.Key("currency_code"): t.String,
        t.Key("llm_id"): t.String,
        t.Key("custom_model_llm_validation_id", optional=True): t.Or(t.String, t.Null),
    }
).ignore_extra("*")


cost_metric_configuration = t.Dict(
    {
        t.Key("cost_configuration_id"): t.String,
        t.Key("use_case_id"): t.String,
        t.Key("playground_id"): t.String,
        t.Key("cost_metric_configurations"): t.List(llm_cost_configuration),
        # New configurations require a name, old ones might not have it
        t.Key("name", optional=True): t.Or(t.String(allow_blank=True), t.Null),
    }
).ignore_extra("*")


class LLMCostConfiguration(APIObject):
    """Cost configuration for a specific LLM model; used for cost metric calculation.
    Price-per-token is price/reference token count.

    Attributes
    ----------
    input_token_price (float): The price of the input token.
    reference_input_token_count (int): The reference input token count.
    output_token_price (float): The price of the output token.
    reference_output_token_count (int): The reference output token count.
    currency_code (str): The currency code.
    llm_id (str): The LLM ID.
    custom_model_llm_validation_id (Optional[str]): The custom model LLM validation ID if llm_id is custom-model.

    """

    _converter = llm_cost_configuration

    def __init__(
        self,
        input_token_price: float,
        reference_input_token_count: int,
        output_token_price: float,
        reference_output_token_count: int,
        currency_code: str,
        llm_id: str,
        custom_model_llm_validation_id: Optional[str] = None,
    ):
        self.input_token_price = input_token_price
        self.reference_input_token_count = reference_input_token_count
        self.output_token_price = output_token_price
        self.reference_output_token_count = reference_output_token_count
        self.currency_code = currency_code
        self.llm_id = llm_id
        self.custom_model_llm_validation_id = custom_model_llm_validation_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.llm_id})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_token_price": self.input_token_price,
            "reference_input_token_count": self.reference_input_token_count,
            "output_token_price": self.output_token_price,
            "reference_output_token_count": self.reference_output_token_count,
            "currency_code": self.currency_code,
            "llm_id": self.llm_id,
            "custom_model_llm_validation_id": self.custom_model_llm_validation_id,
        }


class CostMetricConfiguration(APIObject):
    """Cost metric configuration for a use case.

    Attributes
    ----------
    cost_configuration_id (str): The cost configuration ID.
    use_case_id (str): The use case ID.
    cost_metric_configurations (List[LLMCostConfiguration]): The list of LLM cost configurations.
    """

    _path = "api/v2/genai/costMetricConfigurations"
    _converter = cost_metric_configuration

    def __init__(
        self,
        cost_configuration_id: str,
        playground_id: str,
        use_case_id: str,
        cost_metric_configurations: List[Dict[str, Any]],
        name: str,
    ):
        self.cost_configuration_id = cost_configuration_id
        self.use_case_id = use_case_id
        self.cost_metric_configurations = [
            LLMCostConfiguration.from_server_data(config) for config in cost_metric_configurations
        ]
        self.playground_id = playground_id
        self.name = name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.cost_configuration_id})"

    @classmethod
    def get(cls, cost_metric_configuration_id: str) -> CostMetricConfiguration:
        """Get cost metric configuration by ID."""
        response_data = cls._client.get(
            f"{cls._client.domain}/{cls._path}/{cost_metric_configuration_id}/"
        )
        return cls.from_server_data(response_data.json())

    def update(
        self, cost_metric_configurations: List[LLMCostConfiguration], name: Union[str, None] = None
    ) -> CostMetricConfiguration:
        """Update the cost configurations."""
        payload: dict[str, Any] = {
            "cost_metric_configurations": [
                config.to_dict() for config in cost_metric_configurations
            ],
        }
        if name:
            payload["name"] = name
        url = f"{self._client.domain}/{self._path}/{self.cost_configuration_id}/"
        r_data = self._client.patch(url, data=payload)
        return self.from_server_data(r_data.json())

    @classmethod
    def create(
        cls,
        use_case_id: str,
        playground_id: str,
        name: str,
        cost_metric_configurations: List[LLMCostConfiguration],
    ) -> CostMetricConfiguration:
        """Create a new cost metric configuration."""
        payload = {
            "use_case_id": use_case_id,
            "cost_metric_configurations": [
                config.to_dict() for config in cost_metric_configurations
            ],
            "name": name,
            "playground_id": playground_id,
        }
        url = f"{cls._client.domain}/{cls._path}/"
        r_data = cls._client.post(url, data=payload)
        return cls.from_server_data(r_data.json())

    def delete(self) -> None:
        """Delete the cost metric configuration."""
        url = f"{self._client.domain}/{self._path}/{self.cost_configuration_id}/"
        self._client.delete(url)
