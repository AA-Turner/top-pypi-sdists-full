from typing import Optional

from spotlight.api.data_rule.model import DataRuleRequest


def _get_data_rule_request_info(id: str) -> dict:
    return {"endpoint": f"config/data_rule/{id}"}


def _get_data_rules_request_info(override_find_all: Optional[bool] = False) -> dict:
    endpoint = "config/data_rule"
    params = {"override_find_all": override_find_all}

    filtered_params = {k: v for k, v in params.items() if v is not None}

    return {"endpoint": endpoint, "params": filtered_params}


def _create_data_rule_request_info(request: DataRuleRequest) -> dict:
    return {"endpoint": f"config/data_rule", "json": request.request_dict()}


def _update_data_rule_request_info(id: str, request: DataRuleRequest) -> dict:
    return {"endpoint": f"config/data_rule/{id}", "json": request.request_dict()}


def _delete_data_rule_request_info(id: str) -> dict:
    return {"endpoint": f"config/data_rule/{id}"}
