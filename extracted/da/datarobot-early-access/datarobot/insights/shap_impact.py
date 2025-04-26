#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from typing import Any, cast, Dict, List, Optional, Union

import trafaret as t

from datarobot.enums import ENTITY_TYPES, INSIGHTS_SOURCES
from datarobot.insights.base import BaseInsight
from datarobot.utils import deprecation


class ShapImpact(BaseInsight):
    """Class for SHAP Impact calculations. Use the standard methods of BaseInsight to compute
    and retrieve: compute, create, list, get.
    """

    INSIGHT_NAME = "shapImpact"
    INSIGHT_DATA = {
        "shap_impacts": t.Or(
            t.List(t.List(t.Or(t.Int(), t.Float()))),
            t.Dict(
                {
                    t.Key("featureName"): t.String(),
                    t.Key("impactNormalized"): t.Float(),
                    t.Key("impactUnnormalized"): t.Float(),
                }
            ),
        ),
        "base_value": t.List(t.Float()),
        "capping": Optional[
            t.Or(
                t.Null(),
                t.Dict(
                    {
                        t.Key("right"): t.Or(t.String(), t.Float(), t.Null()),  # noqa: F821
                        t.Key("left"): t.Or(t.String(), t.Float(), t.Null()),  # noqa: F821
                    }
                ),
            )
        ],
        "link": t.Or(t.String(), t.Null()),
        "row_count": Optional[t.Int()],
    }

    @classmethod
    def _get_payload(
        cls,
        entity_id: str,
        source: str = INSIGHTS_SOURCES.TRAINING,
        data_slice_id: Optional[str] = None,
        external_dataset_id: Optional[str] = None,
        entity_type: Optional[ENTITY_TYPES] = None,
        quick_compute: Optional[bool] = None,
        row_count: Optional[int] = None,
        **kwargs: Any,
    ) -> Dict[str, Union[str, int, bool]]:
        """Construct a payload for a compute request"""
        payload = super()._get_payload(
            entity_id=entity_id,
            source=source,
            data_slice_id=data_slice_id,
            external_dataset_id=external_dataset_id,
            entity_type=entity_type,
            quick_compute=quick_compute,
            **kwargs,
        )

        if row_count:
            payload["rowCount"] = row_count

        return payload

    # deal with shap-impact specific data structure to pass impacts list to UI component
    def _get_datarobot_ui_data(self) -> Dict[str, Any]:
        return {"data": self.shap_impacts}

    def sort(self, key_name: str = "-impact_normalized") -> None:
        """
        Sorts insights data by key name.

        :param key_name: item key name to sort data.
            One of 'feature_name', 'impact_normalized' or 'impact_unnormalized'.
            Starting with '-' reverses sort order. Default '-impact_normalized'
        """
        reverse = False
        if not isinstance(key_name, str):
            raise TypeError
        if len(key_name) > 0 and key_name[0] == "-":
            reverse = True
            key_name = key_name[1:]
        self.data["shap_impacts"].sort(key=lambda x: x[key_name], reverse=reverse)

    @property
    def shap_impacts(self) -> List[List[Any]]:
        """SHAP impact values

        Returns
        -------
        shap impacts
            A list of the SHAP impact values
        """
        return cast(List[List[Any]], self.data["shap_impacts"])

    @property
    def base_value(self) -> List[float]:
        """A list of base prediction values"""
        return cast(List[float], self.data["base_value"])

    @property
    def capping(self) -> Optional[Dict[str, Any]]:
        """Capping for the models in the blender"""
        return cast(Optional[Dict[str, Any]], self.data.get("capping"))

    @property
    def link(self) -> Optional[str]:
        """Shared link function of the models in the blender"""
        return cast(Optional[str], self.data.get("link"))

    @property
    @deprecation.deprecated(
        deprecated_since_version="v3.6",
        will_remove_version="v3.7",
        message="row_count is deprecated.",
    )
    def row_count(self) -> Optional[int]:
        """Number of SHAP impact rows. This is deprecated."""
        return cast(Optional[int], self.data.get("row_count"))
