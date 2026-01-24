# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2025 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StatusConfigurationItem:
    key: str
    value: str


@dataclass
class ModelStatusConfiguration:
    status: str
    is_review_required: bool
    status_configuration_items: List[StatusConfigurationItem]
    comment: Optional[str] = None
    model_item_id: Optional[str] = None

    def to_payload_dict(self) -> Dict[str, Any]:
        status_configuration_items = [
            {"key": item.key, "value": item.value}
            for item in self.status_configuration_items
        ]

        res = {
            "status": self.status,
            "isReviewRequired": self.is_review_required,
            "statusConfiguration": status_configuration_items,
        }

        if self.comment:
            res["comment"] = self.comment

        return res

    @classmethod
    def from_parameters_dict(
        cls, parameters: Dict[str, Any]
    ) -> "ModelStatusConfiguration":
        if not parameters:
            raise ValueError("Status configuration dictionary cannot be empty")

        status = parameters.get("status")
        if not status:
            raise ValueError("Status configuration dictionary must have a status")

        is_review_required = parameters.get("is_review_required", False)

        status_configuration_items = []
        for item in parameters.get("status_configuration_items", []):
            status_configuration_items.append(
                StatusConfigurationItem(item["key"], item["value"])
            )

        comment = parameters.get("comment")

        return cls(
            status=status,
            is_review_required=is_review_required,
            status_configuration_items=status_configuration_items,
            comment=comment,
        )

    @classmethod
    def from_payload_dict(cls, payload: Dict[str, Any]) -> "ModelStatusConfiguration":
        status = payload.get("status")
        if not status:
            raise ValueError("Status configuration dictionary must have a status")

        model_item_id = payload.get("modelItemId")

        is_review_required = payload.get("isReviewRequired", False)

        status_configuration_items = []
        for item in payload.get("statusConfiguration", []):
            status_configuration_items.append(
                StatusConfigurationItem(item["key"], item["value"])
            )

        comment = payload.get("comment")

        return cls(
            status=status,
            is_review_required=is_review_required,
            status_configuration_items=status_configuration_items,
            comment=comment,
            model_item_id=model_item_id,
        )
