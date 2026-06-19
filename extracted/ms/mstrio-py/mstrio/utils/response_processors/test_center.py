import json

from mstrio.api import test_center as tc_api
from mstrio.connection import Connection
from mstrio.utils.helper import camel_to_snake, rename_dict_keys

# _REST_ATTR_MAP is defined further up, in EntityBase
SETTINGS_ATTR_MAP = {
    "sourcePrecedence": "promptAnswerSourcePrecedence",
    "dossierSqlEnabled": "dashboardSqlEnabled",
    "dossierDataEnabled": "dashboardDataEnabled",
    "dossierVisualizationScreenshotEnabled": "dashboardVisualizationScreenshotEnabled",
}


def _wrangle_settings_incoming(settings: dict) -> dict:
    """Wrangle settings for test creation and update."""
    settings = settings.copy()

    if "analyzer" in settings:
        settings.update(settings.pop("analyzer"))
    if "promptAnswer" in settings:
        settings.update(settings.pop("promptAnswer"))

    settings = rename_dict_keys(settings, SETTINGS_ATTR_MAP)
    settings = camel_to_snake(settings)

    return settings


def get_all_baseline_tests(connection: Connection, error_msg: str | None = None):
    res = tc_api.get_all_baseline_tests(connection=connection).json()
    baseline_tests = res.get("integrityTests", [])
    for blt in baseline_tests:
        blt["settings"] = _wrangle_settings_incoming(blt.get("settings", {}))
    return baseline_tests


def get_baseline_test(connection: Connection, id: str, error_msg: str | None = None):
    res = tc_api.get_baseline_test(connection=connection, id=id).json()
    res["settings"] = _wrangle_settings_incoming(res.get("settings", {}))
    return res


def _wrangle_summary(summary: dict) -> dict:
    """Wrangle summary for test result."""
    summary = summary.copy()

    summary.update(summary.pop("stats", {}))

    return {"summary": summary}


def get_baseline_result_summary(
    connection: Connection,
    test_id: str,
    id: str,
):
    res = tc_api.get_baseline_result_summary(
        connection=connection, test_id=test_id, id=id
    ).json()
    return _wrangle_summary(res)


def get_comparison_result_summary(
    connection: Connection,
    test_id: str,
    id: str,
):
    res = tc_api.get_comparison_result_summary(
        connection=connection, test_id=test_id, id=id
    ).json()
    return _wrangle_summary(res)


def _wrangle_settings_outgoing(settings: dict) -> dict:
    """Wrangle settings for test retrieval."""
    settings = settings.copy()
    attr_map = {v: k for k, v in SETTINGS_ATTR_MAP.items()}
    settings = rename_dict_keys(settings, attr_map)

    non_analyzer_settings = {
        "promptAnswer": {
            "sourcePrecedence": settings.pop("sourcePrecedence", None),
        },
        "executeContent": settings.pop("executeContent", None),
    }

    return {**non_analyzer_settings, "analyzer": settings}


def create_baseline_test(
    connection: Connection,
    body: dict,
):
    body["settings"] = _wrangle_settings_outgoing(body.get("settings", {}))
    res = tc_api.create_baseline_test(connection=connection, body=body).json()
    res["settings"] = _wrangle_settings_incoming(res.get("settings", {}))
    return res


def update_baseline_test(
    connection: Connection,
    id: str,
    body: dict,
):
    body["settings"] = _wrangle_settings_outgoing(body.get("settings", {}))
    res = tc_api.update_baseline_test(connection=connection, id=id, body=body).json()
    res["settings"] = _wrangle_settings_incoming(res.get("settings", {}))
    return res


def _wrangle_baseline_result(
    object_result: dict, test_id: str, test_result_id: str
) -> dict:
    """Wrangle object result for test result."""
    object_result = object_result.copy()

    tested_object = {
        "id": object_result.pop("objectId", None),
        "name": object_result.pop("objectName", None),
        "type": object_result.pop("objectType", None),
        "subtype": object_result.pop("objectSubType", None),
        "viewMedia": object_result.pop("viewMedia", None),
        "extType": object_result.pop("extType", None),
        "projectId": object_result.pop("projectId", None),
        "ancestors": object_result.pop("ancestors", []),
    }
    object_result["testedObject"] = tested_object

    tree_structure_str: str = object_result.pop("treeStructure", None)
    tree_structure = json.loads(tree_structure_str) if tree_structure_str else None
    object_result["treeStructure"] = tree_structure

    object_result["settings"] = _wrangle_settings_incoming(
        object_result.get("settings", {})
    )
    object_result["testId"] = test_id  # backlink
    object_result["testResultId"] = test_result_id  # backlink

    return object_result


def get_baseline_result(
    connection: Connection,
    test_id: str,
    id: str,
):
    res = tc_api.get_baseline_result(
        connection=connection, test_id=test_id, id=id
    ).json()

    res["objectResults"] = [
        _wrangle_baseline_result(source, test_id=test_id, test_result_id=id)
        for source in res.pop("testObjectBaselines", [])
    ]

    return res
