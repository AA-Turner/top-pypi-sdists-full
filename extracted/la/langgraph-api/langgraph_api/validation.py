import copy
import pathlib
import re

import jsonschema_rs
import orjson

with open(pathlib.Path(__file__).parent.parent / "openapi.json") as f:
    openapi_str = f.read()

openapi = orjson.loads(openapi_str)


NO_NULL_OR_ESCAPED_PATTERN = r"^(?!.*\\[uU]0000)[^\u0000]*$"
RESERVED_CONFIGURABLE_KEYS = (
    "langgraph_auth_user",
    "langgraph_auth_user_id",
    "langgraph_auth_permissions",
    "langgraph_request_id",
    "__langsmith_project__",
    "__langsmith_example_id__",
    "__request_start_time_ms__",
    "__after_seconds__",
    "__otel_traceparent__",
    "__otel_tracestate__",
    "__pregel_node_finished",
)
RESERVED_OR_NULL_OR_ESCAPED_PATTERN = rf"^(?!.*\\[uU]0000)(?!({'|'.join(f'{re.escape(k)}$' for k in RESERVED_CONFIGURABLE_KEYS)}))[^\u0000]*$"
WRITE_SCHEMAS_WITH_CONFIG_OR_CONTEXT = (
    "AssistantCreate",
    "AssistantPatch",
    "CronCreate",
    "CronPatch",
    "RunCreateStateful",
    "RunCreateStateless",
    "ThreadCronCreate",
)


def _set_property_names_pattern(schema: dict, pattern: str) -> None:
    schema["propertyNames"] = {"pattern": pattern}


def _get_object_property(schema: dict, prop_name: str) -> dict | None:
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return None
    prop = properties.get(prop_name)
    if isinstance(prop, dict) and prop.get("type") == "object":
        return prop
    return None


def _apply_validator_only_security_guards(spec: dict) -> None:
    schemas = spec.get("components", {}).get("schemas")
    if not isinstance(schemas, dict):
        return

    config_schema = schemas.get("Config")
    if isinstance(config_schema, dict):
        _set_property_names_pattern(config_schema, NO_NULL_OR_ESCAPED_PATTERN)
        if configurable := _get_object_property(config_schema, "configurable"):
            _set_property_names_pattern(
                configurable, RESERVED_OR_NULL_OR_ESCAPED_PATTERN
            )

    for schema_name in WRITE_SCHEMAS_WITH_CONFIG_OR_CONTEXT:
        schema = schemas.get(schema_name)
        if not isinstance(schema, dict):
            continue

        config = _get_object_property(schema, "config")
        if config:
            _set_property_names_pattern(config, NO_NULL_OR_ESCAPED_PATTERN)
            if configurable := _get_object_property(config, "configurable"):
                _set_property_names_pattern(
                    configurable, RESERVED_OR_NULL_OR_ESCAPED_PATTERN
                )

        if context := _get_object_property(schema, "context"):
            _set_property_names_pattern(context, RESERVED_OR_NULL_OR_ESCAPED_PATTERN)


_validation_openapi = copy.deepcopy(openapi)
_apply_validator_only_security_guards(_validation_openapi)

ConfigValidator = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["Config"]
)
AssistantVersionsSearchRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantVersionsSearchRequest"]
)
AssistantSearchRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantSearchRequest"]
)
AssistantCountRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantCountRequest"]
)
ThreadSearchRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["ThreadSearchRequest"]
)
ThreadCountRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["ThreadCountRequest"]
)
AssistantCreate = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantCreate"]
)
AssistantPatch = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantPatch"]
)
AssistantVersionChange = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["AssistantVersionChange"]
)
ThreadCreate = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["ThreadCreate"],
        "components": {
            "schemas": {
                "ThreadSuperstepUpdate": _validation_openapi["components"]["schemas"][
                    "ThreadSuperstepUpdate"
                ],
                "Command": _validation_openapi["components"]["schemas"]["Command"],
                "Send": _validation_openapi["components"]["schemas"]["Send"],
            }
        },
    }
)
ThreadPatch = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["ThreadPatch"]
)
ThreadPruneRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["ThreadPruneRequest"]
)
ThreadStateUpdate = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["ThreadStateUpdate"],
        "components": {
            "schemas": {
                "CheckpointConfig": _validation_openapi["components"]["schemas"][
                    "CheckpointConfig"
                ]
            }
        },
    }
)

ThreadStateCheckpointRequest = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["ThreadStateCheckpointRequest"],
        "components": {
            "schemas": {
                "CheckpointConfig": _validation_openapi["components"]["schemas"][
                    "CheckpointConfig"
                ]
            }
        },
    }
)
ThreadStateSearch = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["ThreadStateSearch"],
        "components": {
            "schemas": {
                "CheckpointConfig": _validation_openapi["components"]["schemas"][
                    "CheckpointConfig"
                ]
            }
        },
    }
)
RunCreateStateless = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["RunCreateStateless"],
        "components": {
            "schemas": {
                "Command": _validation_openapi["components"]["schemas"]["Command"],
                "Send": _validation_openapi["components"]["schemas"]["Send"],
            }
        },
    }
)
RunBatchCreate = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["RunBatchCreate"],
        "components": {
            "schemas": {
                "RunCreateStateless": _validation_openapi["components"]["schemas"][
                    "RunCreateStateless"
                ],
                "Command": _validation_openapi["components"]["schemas"]["Command"],
                "Send": _validation_openapi["components"]["schemas"]["Send"],
            }
        },
    }
)
RunCreateStateful = jsonschema_rs.validator_for(
    {
        **_validation_openapi["components"]["schemas"]["RunCreateStateful"],
        "components": {
            "schemas": {
                "CheckpointConfig": _validation_openapi["components"]["schemas"][
                    "CheckpointConfig"
                ],
                "Command": _validation_openapi["components"]["schemas"]["Command"],
                "Send": _validation_openapi["components"]["schemas"]["Send"],
            }
        },
    }
)
RunsCancel = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["RunsCancel"]
)
CronCreate = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["CronCreate"]
)
ThreadCronCreate = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["ThreadCronCreate"]
)
CronPatch = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["CronPatch"]
)
CronSearch = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["CronSearch"]
)
CronCountRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["CronCountRequest"]
)


# Stuff around storage/BaseStore API
StorePutRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["StorePutRequest"]
)
StoreSearchRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["StoreSearchRequest"]
)
StoreDeleteRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["StoreDeleteRequest"]
)
StoreListNamespacesRequest = jsonschema_rs.validator_for(
    _validation_openapi["components"]["schemas"]["StoreListNamespacesRequest"]
)


DOCS_HTML = """<!doctype html>
<html>
  <head>
    <title>Scalar API Reference</title>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1" />
  </head>
  <body>
    <script id="api-reference" data-url="{mount_prefix}/openapi.json"></script>
    <script>
      var configuration = {{}}
      document.getElementById('api-reference').dataset.configuration =
        JSON.stringify(configuration)
    </script>
    <script src="https://cdn.jsdelivr.net/npm/@scalar/api-reference"></script>
  </body>
</html>"""
