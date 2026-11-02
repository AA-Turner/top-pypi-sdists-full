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
                            "https://lakekeeper.example.com (server root, NOT /catalog)"
                        ),
                        "schema": "databaas-lakehouse (default when empty)",
                        "login": "Zitadel service-account client id",
                        "password": "Zitadel service-account client secret",
                    },
                },
                "conn-fields": {
                    "service_account_key": _string_field(
                        "Service account JSON key",
                        "Paste the whole downloaded JSON key here (keyId/key/"
                        "userId) when your Zitadel console only offers a JSON "
                        "key for this machine user, not a client secret. Takes "
                        "priority over Client ID/secret when set. Still needs "
                        "Token URL and Project ID below.",
                    ),
                    "audience": _string_field(
                        "JWT audience",
                        "Only for a service account JSON key. Defaults to the "
                        "Token URL with '/oauth/v2/token' stripped — override "
                        "only if that default is wrong.",
                    ),
                    "token_url": _string_field(
                        "Token URL",
                        "Zitadel OAuth2 token endpoint. Required with a Client ID "
                        "or a service account JSON key.",
                        "https://auth.example.com/oauth/v2/token",
                    ),
                    "project_id": _string_field(
                        "Zitadel project ID",
                        "Expands to the audience scope Lakekeeper requires. "
                        "Required unless an explicit scope is given.",
                    ),
                    "scope": _string_field(
                        "OAuth scope",
                        "Explicit scope, overriding the one derived from the "
                        "project ID. Leave empty unless you know you need it.",
                    ),
                    "namespace": _string_field(
                        "Default namespace",
                        "Namespace used when a DAG does not pass one.",
                        "default",
                    ),
                    "region": _string_field(
                        "S3 region", "Region used in signing payloads.", "nl-ams"
                    ),
                    "endpoint": _string_field(
                        "S3 endpoint",
                        "Leave empty to take it from the catalog's table config.",
                    ),
                    "verify": _string_field(
                        "TLS verification",
                        "'false' to disable, or a path to a CA bundle. Defaults to "
                        "verifying.",
                    ),
                },
            }
        ],
    }
