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

from typing import Sequence, Union

from datarobot.models.genai.comparison_chat import get_entity_id
from datarobot.models.genai.insights_configuration import InsightsConfiguration
from datarobot.models.genai.playground import Playground


class MetricInsights(InsightsConfiguration):
    """Metric insights for playground."""

    _path = "api/v2/genai/playgrounds/{}/supportedInsights/"

    @classmethod
    def list(
        cls, playground: Union[str, Playground], llm_blueprint_ids: Sequence[str] | None = None
    ) -> list[InsightsConfiguration]:
        """Get metric insights for playground.

        Parameters
        ----------
        playground : str or Playground
            Playground to get the supported metrics from.
        llm_blueprint_ids : Optional[Sequence[str]]
            LLM Blueprint IDs to check for additional metrics support for.

        Returns
        -------
        insights: list[InsightsConfiguration]
            Metric insights for playground.

        """
        path = cls._path.format(get_entity_id(playground))

        params = {}
        if llm_blueprint_ids:
            params["llmBlueprintIds"] = llm_blueprint_ids
        response_data = cls._client.get(url=f"{cls._client.domain}/{path}", params=params)
        return [
            cls.from_server_data(insight)
            for insight in response_data.json()["insightsConfiguration"]
        ]

    @classmethod
    def copy_to_playground(
        cls,
        source_playground: Union[str, Playground],
        target_playground: Union[str, Playground],
        add_to_existing: bool = True,
        with_evaluation_datasets: bool = False,
    ) -> None:
        """Copy metric insights from one playground to another.

        Parameters
        ----------
        source_playground : str or Playground
            Playground to copy metric insights from.
        target_playground : str or Playground
            Playground to copy metric insights to.
        add_to_existing : Optional[bool]
            Add metric insights to existing ones in the target playground, by default True.
        with_evaluation_datasets : Optional[bool]
            Copy evaluation datasets from the source playground.
        """
        payload = {
            "add_to_existing": add_to_existing,
            "with_evaluation_datasets": with_evaluation_datasets,
        }
        path = (
            cls._path.format(get_entity_id(target_playground))
            + f"{get_entity_id(source_playground)}/"
        )
        cls._client.put(f"{cls._client.domain}/{path}", json=payload)
