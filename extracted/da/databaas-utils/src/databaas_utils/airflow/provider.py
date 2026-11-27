"""Airflow provider metadata, discovered through the `apache_airflow_provider`
entry point declared in pyproject.toml.

Registering a real connection type is the largest usability win available here:
the admin gets a form with labelled, individually described fields and a working
**Test** button, instead of pasting a JSON extras blob and finding out at the
first DAG run whether it was right.

Extra fields are declared as `conn-fields` rather than WTForms widgets. The
declarative form needs no flask-appbuilder, wtforms or flask-babel — none of
which are installed in a task-runner environment — so this module imports
nothing beyond stdlib and stays safe to load anywhere.
"""

from __future__ import annotations

from typing import Any

CONNECTION_TYPE = "databaas_lakehouse"
HOOK_CLASS = "databaas_utils.airflow.hook.LakehouseHook"


def _string_field(label: str, description: str, placeholder: str = "") -> dict[str, Any]:
    field: dict[str, Any] = {
        "label": label,
        "description": description,
        "schema": {"type": ["string", "null"]},
    }
    if placeholder:
        field["placeholder"] = placeholder
    return field


def get_provider_info() -> dict[str, Any]:
    """Provider metadata, read by Airflow via the ``apache_airflow_provider`` entry point.

    It registers the ``databaas_lakehouse`` connection type, which gives the
    admin a labelled form and a working *Test* button.
    """
    return {
        "package-name": "databaas-utils",
        "name": "DataBaas Lakehouse",
        "description": "Lakekeeper/Iceberg lakehouse access for DataBaas.\n",
        "hooks": [
            {
                "integration-name": "DataBaas Lakehouse",
                "python-modules": ["databaas_utils.airflow.hook"],
            }
        ],
        "connection-types": [
            {
                "hook-class-name": HOOK_CLASS,
                "hook-name": "DataBaas Lakehouse",
                "connection-type": CONNECTION_TYPE,
                "ui-field-behaviour": {
                    "hidden-fields": ["port"],
                    "relabeling": {
                        "host": "Lakekeeper URL",
                        "schema": "Warehouse",
                        "login": "Client ID",
                        "password": "Client secret",
                    },
                    "placeholders": {
                        "host": (
                            "Empty: same as databaas_lakehouse "
                            "(server root, NOT /catalog)"
                        ),
                        "schema": "Empty: same as databaas_lakehouse",
                        "login": "Zitadel service-account client id",
                        "password": "Zitadel service-account client secret",
                    },
                },
                # Settings read from `extra` but kept off the form: the platform
                # connection already carries them. Still honoured when present:
                # service_account_key, audience, scope, namespace, region,
                # endpoint and verify.
                "conn-fields": {
                    "token_url": _string_field(
                        "Token URL",
                        "The Zitadel address, e.g. https://auth.example.com. "
                        "Leave empty to use the one on databaas_lakehouse.",
                        "Empty: same as databaas_lakehouse",
                    ),
                    "project_id": _string_field(
                        "Zitadel project ID",
                        "Leave empty to use the one on databaas_lakehouse.",
                        "Empty: same as databaas_lakehouse",
                    ),
                },
            }
        ],
    }
