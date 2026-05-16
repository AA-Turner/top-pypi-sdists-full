from mstrio.api import test_center as tc_api
from mstrio.connection import Connection
from mstrio.utils.helper import camel_to_snake, rename_dict_keys


def _wrangle_settings(settings: dict) -> dict:
    """Wrangle settings for test creation and update."""
    settings = settings.copy()

    if "analyzer" in settings:
        settings.update(settings.pop("analyzer"))
    if "promptAnswer" in settings:
        settings.update(settings.pop("promptAnswer"))

    ATTR_MAP = {
        "source_precedence": "prompt_answer_source_precedence",
    }
    settings = camel_to_snake(settings)
    settings = rename_dict_keys(settings, ATTR_MAP)

    return settings


def get_all_baseline_tests(connection: Connection, error_msg: str | None = None):
    res = tc_api.get_all_baseline_tests(connection=connection).json()
    baseline_tests = res.get("integrityTests", [])
    for blt in baseline_tests:
        blt["settings"] = _wrangle_settings(blt.get("settings", {}))
    return baseline_tests


def get_baseline_test(connection: Connection, id: str, error_msg: str | None = None):
    res = tc_api.get_baseline_test(connection=connection, id=id).json()
    res["settings"] = _wrangle_settings(res.get("settings", {}))
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
    error_msg: str | None = None,
):
    res = tc_api.get_baseline_result_summary(
        connection=connection, test_id=test_id, id=id
    ).json()
    return _wrangle_summary(res)


def get_comparison_result_summary(
    connection: Connection,
    test_id: str,
    id: str,
    error_msg: str | None = None,
):
    res = tc_api.get_comparison_result_summary(
        connection=connection, test_id=test_id, id=id
    ).json()
    return _wrangle_summary(res)
