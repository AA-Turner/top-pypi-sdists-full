# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the spec and discovered-catalog comparators.

The rule under test is asymmetric on purpose: a spec is compared for
compatibility with the configs users already saved, while a discovered catalog
is compared strictly, because anything that moves there moves the data the
platform writes.
"""

from __future__ import annotations

from typing import Any

import pytest
from airbyte_protocol.models import (
    AirbyteCatalog,
    AirbyteStream,
    ConnectorSpecification,
    SyncMode,
)

from airbyte_ops_mcp.regression_tests.regression import (
    compare_catalog_schemas,
    compare_specs,
)

pytestmark = pytest.mark.unit


def _spec(
    properties: dict[str, Any],
    required: list[str] | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """A connector spec carrying the given config properties."""
    return {
        "documentationUrl": "https://docs.airbyte.com/integrations/sources/test",
        "connectionSpecification": {
            "type": "object",
            "required": required if required is not None else ["api_key"],
            "properties": properties,
        },
        **extra,
    }


_BASE_PROPERTIES: dict[str, Any] = {
    "api_key": {"type": "string", "title": "API key", "airbyte_secret": True},
    "start_date": {"type": "string", "format": "date-time"},
}


def _catalog(json_schema: dict[str, Any], name: str = "users") -> AirbyteCatalog:
    """A discovered catalog with one stream carrying the given schema."""
    return AirbyteCatalog(
        streams=[
            AirbyteStream(
                name=name,
                json_schema=json_schema,
                supported_sync_modes=[SyncMode.full_refresh],
            )
        ]
    )


_BASE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
}


# ---------------------------------------------------------------------------
# compare_specs
# ---------------------------------------------------------------------------


def test_an_added_optional_property_passes():
    """The additive case the compatibility rule exists for.

    No saved config becomes invalid by a new optional field, so a connector that
    grows one must not be blocked -- but the reviewer is still told what it grew.
    """
    control = _spec(_BASE_PROPERTIES)
    target = _spec({**_BASE_PROPERTIES, "page_size": {"type": "integer"}})

    result = compare_specs(control, target)

    assert result.passed
    assert not result.errors
    assert any("page_size" in change for change in result.warnings)


def test_a_removed_property_fails():
    """Every config that set the property is now carrying an unknown field."""
    control = _spec(_BASE_PROPERTIES)
    target = _spec({"api_key": _BASE_PROPERTIES["api_key"]})

    result = compare_specs(control, target)

    assert not result.passed
    assert result.errors == [
        "`connectionSpecification.properties.start_date` was removed"
    ]


def test_a_changed_property_type_fails():
    """A saved config's value no longer validates against its own field."""
    control = _spec(_BASE_PROPERTIES)
    target = _spec({**_BASE_PROPERTIES, "start_date": {"type": "integer"}})

    result = compare_specs(control, target)

    assert not result.passed
    assert (
        "`connectionSpecification.properties.start_date.type` no longer allows string"
    ) in result.errors
    # The dropped `format` went the other way: a constraint that disappears
    # widens what a config may say, so it is reported without failing.
    assert (
        "`connectionSpecification.properties.start_date.format` was removed, "
        "widening what a config may set"
    ) in result.warnings


def test_a_newly_required_property_fails_even_when_it_is_new():
    """Adding a property is additive; adding it to `required` is not.

    A config saved before the change omits it, so the connector rejects a
    connection that worked yesterday.
    """
    control = _spec(_BASE_PROPERTIES)
    target = _spec(
        {**_BASE_PROPERTIES, "region": {"type": "string"}},
        required=["api_key", "region"],
    )

    result = compare_specs(control, target)

    assert not result.passed
    assert "`region` is now required" in result.errors[0]


def test_a_first_required_list_fails():
    """A node that gains its first `required` list has made a field mandatory.

    Routing `required` only when the control node already had the key let the
    most common shape of this break -- a low-code spec that required nothing and
    now requires `start_date` -- through as "`required` was added".
    """
    control = _spec(_BASE_PROPERTIES, required=[])
    del control["connectionSpecification"]["required"]
    target = _spec(_BASE_PROPERTIES, required=["start_date"])

    result = compare_specs(control, target)

    assert not result.passed
    assert "`start_date` is now required" in result.errors[0]


@pytest.mark.parametrize(
    "added",
    [
        pytest.param({"enum": ["us", "eu"]}, id="enum"),
        pytest.param({"pattern": "^[0-9]+$"}, id="pattern"),
        pytest.param({"const": "fixed"}, id="const"),
        pytest.param({"maxLength": 8}, id="maxLength"),
        pytest.param({"format": "date-time"}, id="format"),
    ],
)
def test_an_added_constraint_fails(added):
    """A constraint that appears rejects configs that were valid yesterday.

    Treating every target-only key as "a property was added" waved all of these
    through, including the maximal narrowing of an unconstrained string.
    """
    control = _spec({"region": {"type": "string"}})
    target = _spec({"region": {"type": "string", **added}})

    result = compare_specs(control, target)

    assert not result.passed
    assert "narrowing what a config may set" in result.errors[0]


def test_an_added_additional_properties_false_fails():
    """Sealing an object rejects every config carrying an extra key."""
    control = _spec({"options": {"type": "object", "properties": {}}})
    target = _spec(
        {"options": {"type": "object", "properties": {}, "additionalProperties": False}}
    )

    result = compare_specs(control, target)

    assert not result.passed


def test_becoming_nullable_passes():
    """`"string"` -> `["null", "string"]` accepts strictly more than before.

    It is also the shape every CDK-generated spec takes when a field becomes
    optional, so comparing the raw values would fail routine regenerations.
    """
    control = _spec({"start_date": {"type": "string"}})
    target = _spec({"start_date": {"type": ["null", "string"]}})

    result = compare_specs(control, target)

    assert result.passed
    assert "also allows null" in result.warnings[0]


def test_a_changed_default_passes_and_is_reported_as_behaviour():
    """A new default cannot invalidate a saved config, but it does change a sync."""
    control = _spec({"page_size": {"type": "integer", "default": 100}})
    target = _spec({"page_size": {"type": "integer", "default": 500}})

    result = compare_specs(control, target)

    assert result.passed
    assert "changes behaviour, not validity" in result.warnings[0]


@pytest.mark.parametrize(
    "key,control_bound,target_bound,expected_pass",
    [
        pytest.param("maximum", 100, 1000, True, id="raised-maximum-relaxes"),
        pytest.param("maximum", 1000, 100, False, id="lowered-maximum-tightens"),
        pytest.param("minLength", 8, 1, True, id="lowered-minimum-relaxes"),
        pytest.param("minLength", 1, 8, False, id="raised-minimum-tightens"),
    ],
)
def test_a_moved_bound_is_judged_by_its_direction(
    key, control_bound, target_bound, expected_pass
):
    """Widening a bound admits configs that were invalid; narrowing rejects some."""
    control = _spec({"page_size": {"type": "integer", key: control_bound}})
    target = _spec({"page_size": {"type": "integer", key: target_bound}})

    result = compare_specs(control, target)

    assert result.passed is expected_pass


@pytest.mark.parametrize(
    "key,control_value,target_value,expected_pass",
    [
        pytest.param("additionalProperties", False, True, True, id="unsealed-relaxes"),
        pytest.param("additionalProperties", True, False, False, id="sealed-tightens"),
        pytest.param("uniqueItems", True, False, True, id="duplicates-allowed-relaxes"),
        pytest.param("uniqueItems", False, True, False, id="uniqueness-tightens"),
    ],
)
def test_a_flipped_boolean_constraint_is_judged_by_its_direction(
    key, control_value, target_value, expected_pass
):
    """Relaxing a constraint in place is the same change as deleting it.

    Deleting `additionalProperties` was already treated as the widening it is,
    while setting it to `true` -- the identical change, written differently --
    failed as "changed from False to True".
    """
    control = _spec({"options": {"type": "object", key: control_value}})
    target = _spec({"options": {"type": "object", key: target_value}})

    result = compare_specs(control, target)

    assert result.passed is expected_pass


def test_a_widened_enum_of_objects_passes_like_a_widened_enum_of_strings():
    """JSON Schema says an `enum` is a set whatever its entries are.

    Requiring scalars made the two forms of the same change read as opposite
    verdicts: `also allows 'b'` for strings, a failure for objects.
    """
    control = _spec({"mode": {"enum": [{"kind": "full"}]}})
    target = _spec({"mode": {"enum": [{"kind": "full"}, {"kind": "incremental"}]}})

    result = compare_specs(control, target)

    assert result.passed
    assert "also allows" in result.warnings[0]


def test_a_narrowed_enum_of_objects_still_fails():
    """Set semantics cut both ways: a dropped option is still a dropped option."""
    control = _spec({"mode": {"enum": [{"kind": "full"}, {"kind": "incremental"}]}})
    target = _spec({"mode": {"enum": [{"kind": "full"}]}})

    result = compare_specs(control, target)

    assert not result.passed
    assert "no longer allows" in result.errors[0]


def test_a_finding_does_not_quote_a_whole_subtree():
    """The payload bound counts findings; nothing bounded their length.

    A node that changed shape quoted both sides in full, so one finding could
    run to thousands of characters and a hundred of them could blow the
    `GITHUB_OUTPUT` budget the bound exists to protect.
    """
    wide = {
        f"field_{index}": {"type": "string", "description": "x" * 40}
        for index in range(30)
    }
    control = _spec({"cfg": {"properties": wide}})
    target = _spec({"cfg": {"properties": [1, 2]}})

    result = compare_specs(control, target)

    assert len(result.errors) == 1
    assert len(result.errors[0]) < 400
    # Clamped side by side: the wide object is elided, the short one is quoted
    # whole, and the reader still sees which node changed shape and into what.
    assert "…" in result.errors[0]
    assert result.errors[0].endswith("to [1, 2]")


def test_two_specs_that_declare_no_configuration_fail():
    """The same rule the catalog follows: nothing declared is nothing compared."""
    result = compare_specs({}, {})

    assert not result.passed
    assert result.message == "Neither version declared a connection specification"


def test_reordered_oneof_branches_pass():
    """Promoting OAuth above API-key is a no-op the platform resolves by `const`.

    Compared positionally it reads as every field of both branches being
    replaced by the other's -- red, and claiming fields were removed that are
    still there.
    """
    oauth = {
        "title": "OAuth",
        "properties": {
            "auth_type": {"type": "string", "const": "oauth2.0"},
            "client_id": {"type": "string"},
        },
        "required": ["auth_type", "client_id"],
    }
    api_key = {
        "title": "API key",
        "properties": {
            "auth_type": {"type": "string", "const": "api_key"},
            "api_key": {"type": "string"},
        },
        "required": ["auth_type", "api_key"],
    }
    control = _spec({"credentials": {"oneOf": [api_key, oauth]}})
    target = _spec({"credentials": {"oneOf": [oauth, api_key]}})

    result = compare_specs(control, target)

    assert result.passed
    assert not result.warnings


def test_a_removed_branch_is_still_caught_when_the_rest_are_reordered():
    """Matching by discriminator must not become a way to miss a dropped branch."""
    oauth = {"properties": {"auth_type": {"const": "oauth2.0"}}}
    api_key = {"properties": {"auth_type": {"const": "api_key"}}}
    token = {"properties": {"auth_type": {"const": "token"}}}
    control = _spec({"credentials": {"oneOf": [api_key, oauth, token]}})
    target = _spec({"credentials": {"oneOf": [oauth, api_key]}})

    result = compare_specs(control, target)

    assert not result.passed
    assert "`connectionSpecification.properties.credentials.oneOf[2]` was removed" in (
        result.errors
    )


def test_a_branch_with_two_discriminators_matches_whatever_the_property_order():
    """The key was whichever const came first in the dict, so order decided it.

    Reordering a branch's own properties then gave the two sides different keys,
    the branch found no partner, and a compatible edit read as one auth method
    removed and another added.
    """
    control = _spec(
        {
            "credentials": {
                "oneOf": [
                    {
                        "properties": {
                            "auth_type": {"const": "oauth2.0"},
                            "flavor": {"const": "std"},
                            "client_id": {"type": "string"},
                        }
                    }
                ]
            }
        }
    )
    target = _spec(
        {
            "credentials": {
                "oneOf": [
                    {
                        "properties": {
                            "flavor": {"const": "std"},
                            "auth_type": {"const": "oauth2.0"},
                            "client_id": {"type": "string"},
                            "scopes": {"type": "string"},
                        }
                    }
                ]
            }
        }
    )

    result = compare_specs(control, target)

    assert result.passed
    assert not any("was removed" in change for change in result.errors)
    assert any("scopes` was added" in change for change in result.warnings)


def test_a_swapped_auth_method_reads_as_one_removed_and_one_added():
    """A branch with a discriminator and no partner is not "the other branch".

    Diffing it against whichever unmatched branch happened to be left would
    describe a dropped auth method as a pile of field changes.
    """
    control = _spec(
        {
            "credentials": {
                "oneOf": [{"properties": {"auth_type": {"const": "api_key"}}}]
            }
        }
    )
    target = _spec(
        {
            "credentials": {
                "oneOf": [{"properties": {"auth_type": {"const": "oauth2.0"}}}]
            }
        }
    )

    result = compare_specs(control, target)

    assert not result.passed
    assert result.errors == [
        "`connectionSpecification.properties.credentials.oneOf[0]` was removed"
    ]
    assert result.warnings == [
        "`connectionSpecification.properties.credentials.oneOf[0]` was added"
    ]


def test_a_reordered_config_path_fails():
    """`path_in_connector_config` is a location, not a set of allowed values.

    Moving the OAuth output under a `credentials` object rewires where the
    platform writes the token; set semantics called it "also allows".
    """
    control = _spec(
        {"credentials": {"type": "object"}},
        advanced_auth={
            "auth_flow_type": "oauth2.0",
            "oauth_config_specification": {
                "complete_oauth_output_specification": {
                    "properties": {
                        "access_token": {"path_in_connector_config": ["client_id"]}
                    }
                }
            },
        },
    )
    target = _spec(
        {"credentials": {"type": "object"}},
        advanced_auth={
            "auth_flow_type": "oauth2.0",
            "oauth_config_specification": {
                "complete_oauth_output_specification": {
                    "properties": {
                        "access_token": {
                            "path_in_connector_config": ["credentials", "client_id"]
                        }
                    }
                }
            },
        },
    )

    result = compare_specs(control, target)

    assert not result.passed


def test_a_config_field_named_properties_keeps_its_own_documentation():
    """The exemption is structural: a field's `title` is prose wherever it sits.

    Testing the literal parent key `properties` got this backwards for a field
    a connector happens to call `properties`, failing a reworded title.
    """
    control = _spec({"properties": {"type": "object", "title": "Extra properties"}})
    target = _spec({"properties": {"type": "object", "title": "Additional properties"}})

    result = compare_specs(control, target)

    assert result.passed


def test_a_dropped_requirement_passes():
    """Relaxing a requirement cannot invalidate a config that already met it."""
    control = _spec(_BASE_PROPERTIES, required=["api_key", "start_date"])
    target = _spec(_BASE_PROPERTIES, required=["api_key"])

    result = compare_specs(control, target)

    assert result.passed
    assert any("no longer required" in change for change in result.warnings)


def test_documentation_changes_pass():
    """A reworded description must not fail a release."""
    control = _spec(_BASE_PROPERTIES)
    target = _spec(
        {
            **_BASE_PROPERTIES,
            "api_key": {
                "type": "string",
                "title": "API token",
                "description": "The token to authenticate with.",
                "airbyte_secret": True,
            },
        }
    )

    result = compare_specs(control, target)

    assert result.passed
    assert not result.errors


def test_a_config_field_named_description_is_still_a_property():
    """The documentation exemption is by position, not by name.

    `properties.description` is a field a user fills in, not prose about a
    field, and dropping it breaks the configs that set it.
    """
    control = _spec({**_BASE_PROPERTIES, "description": {"type": "string"}})
    target = _spec(_BASE_PROPERTIES)

    result = compare_specs(control, target)

    assert not result.passed
    assert result.errors == [
        "`connectionSpecification.properties.description` was removed"
    ]


def test_a_narrowed_enum_fails_and_a_widened_one_passes():
    """An allowed value that disappears invalidates the configs that chose it."""
    control = _spec({"auth_type": {"type": "string", "enum": ["oauth", "token"]}})
    target_narrowed = _spec({"auth_type": {"type": "string", "enum": ["oauth"]}})
    target_widened = _spec(
        {"auth_type": {"type": "string", "enum": ["oauth", "token", "jwt"]}}
    )

    narrowed = compare_specs(control, target_narrowed)
    widened = compare_specs(control, target_widened)

    assert not narrowed.passed
    assert "no longer allows 'token'" in narrowed.errors[0]
    assert widened.passed
    assert "also allows 'jwt'" in widened.warnings[0]


def test_a_removed_oneof_branch_fails():
    """Dropping an auth method breaks every config that authenticated that way."""
    control = _spec(
        {
            "credentials": {
                "oneOf": [
                    {"title": "OAuth", "properties": {"token": {"type": "string"}}},
                    {"title": "Key", "properties": {"key": {"type": "string"}}},
                ]
            }
        }
    )
    target = _spec(
        {
            "credentials": {
                "oneOf": [
                    {"title": "OAuth", "properties": {"token": {"type": "string"}}},
                ]
            }
        }
    )

    result = compare_specs(control, target)

    assert not result.passed
    assert "`connectionSpecification.properties.credentials.oneOf[1]` was removed" in (
        result.errors
    )


def test_an_unchanged_spec_passes_with_nothing_to_report():
    result = compare_specs(_spec(_BASE_PROPERTIES), _spec(_BASE_PROPERTIES))

    assert result.passed
    assert result.message == "Spec is unchanged"
    assert not result.warnings


def test_the_protocol_model_is_accepted_as_well_as_a_dict():
    """The comparator is handed whatever `ExecutionResult.get_spec()` yields."""
    control = ConnectorSpecification(
        connectionSpecification={
            "type": "object",
            "properties": {"api_key": {"type": "string"}},
        }
    )
    target = ConnectorSpecification(
        connectionSpecification={
            "type": "object",
            "properties": {"api_key": {"type": "integer"}},
        }
    )

    result = compare_specs(control, target)

    assert not result.passed
    assert "no longer allows string" in result.errors[0]


@pytest.mark.parametrize(
    "control,target,expected",
    [
        pytest.param(None, _spec(_BASE_PROPERTIES), "control", id="control-missing"),
        pytest.param(_spec(_BASE_PROPERTIES), None, "target", id="target-missing"),
        pytest.param(None, None, "control and target", id="both-missing"),
    ],
)
def test_a_missing_spec_fails_rather_than_passing_vacuously(control, target, expected):
    """A command that emitted no spec cannot be shown to be unchanged."""
    result = compare_specs(control, target)

    assert not result.passed
    assert expected in result.message


# ---------------------------------------------------------------------------
# compare_catalog_schemas
# ---------------------------------------------------------------------------


def test_an_unchanged_catalog_passes():
    result = compare_catalog_schemas(_catalog(_BASE_SCHEMA), _catalog(_BASE_SCHEMA))

    assert result.passed
    assert result.stream_results["users"].passed
    assert result.stream_results["users"].schema_diff is None


@pytest.mark.parametrize(
    "target_schema,reason",
    [
        pytest.param(
            {
                "type": "object",
                "properties": {"id": {"type": "string"}, "name": {"type": "string"}},
            },
            "a field's type changed",
            id="type-changed",
        ),
        pytest.param(
            {"type": "object", "properties": {"id": {"type": "integer"}}},
            "a field was dropped",
            id="field-removed",
        ),
        pytest.param(
            {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "email": {"type": "string"},
                },
            },
            "a field was added",
            id="field-added",
        ),
    ],
)
def test_any_schema_change_fails(target_schema, reason):
    """Strict by design: even an added field changes what a sync writes."""
    result = compare_catalog_schemas(_catalog(_BASE_SCHEMA), _catalog(target_schema))

    assert not result.passed, reason
    assert result.failed_streams == ["users"]
    assert result.stream_results["users"].schema_diff


def test_the_diff_survives_json_serialisation():
    """The diff travels into the run's JSON payload, which must not blow up."""
    import json

    result = compare_catalog_schemas(
        _catalog(_BASE_SCHEMA),
        _catalog({"type": "object", "properties": {"id": {"type": "string"}}}),
    )

    round_tripped = json.loads(json.dumps(result.stream_results["users"].schema_diff))

    assert round_tripped


def test_a_stream_that_disappears_fails():
    result = compare_catalog_schemas(_catalog(_BASE_SCHEMA), AirbyteCatalog(streams=[]))

    assert not result.passed
    assert "missing from the target catalog" in result.stream_results["users"].message


def test_a_new_stream_fails_and_says_it_is_new():
    """Strict includes additions, and the reviewer is told which kind it is."""
    result = compare_catalog_schemas(AirbyteCatalog(streams=[]), _catalog(_BASE_SCHEMA))

    assert not result.passed
    assert "is new in the target catalog" in result.stream_results["users"].message


def test_a_changed_sync_mode_fails():
    """The stream's declared capabilities are part of the contract too."""
    control = _catalog(_BASE_SCHEMA)
    target = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="users",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh, SyncMode.incremental],
            )
        ]
    )

    result = compare_catalog_schemas(control, target)

    assert not result.passed


@pytest.mark.parametrize(
    "control,target,expected",
    [
        pytest.param(None, _catalog(_BASE_SCHEMA), "control", id="control-missing"),
        pytest.param(_catalog(_BASE_SCHEMA), None, "target", id="target-missing"),
        pytest.param(None, None, "control and target", id="both-missing"),
    ],
)
def test_a_missing_catalog_fails_rather_than_passing_vacuously(
    control, target, expected
):
    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert expected in result.message


def test_two_empty_catalogs_are_inconclusive_not_a_match():
    """Zero streams on both sides means nothing about the schema was checked.

    A config scoped to nothing, or a discover that degrades the same way on both
    versions, is the inconclusive run the epic says must never read as a pass --
    and "unchanged across 0 streams" asserts the opposite of what happened.
    """
    result = compare_catalog_schemas(
        AirbyteCatalog(streams=[]), AirbyteCatalog(streams=[])
    )

    assert not result.passed
    assert "Neither version discovered any stream" in result.message


def test_streams_are_keyed_by_namespace_so_one_cannot_shadow_another():
    """`public.users` and `reporting.users` are two streams, not one.

    Keying on the name alone let the second entry overwrite the first, taking a
    real type change in the shadowed stream with it.
    """
    changed = {"type": "object", "properties": {"id": {"type": "string"}}}

    def _namespaced(public_schema):
        return AirbyteCatalog(
            streams=[
                AirbyteStream(
                    name="users",
                    namespace="public",
                    json_schema=public_schema,
                    supported_sync_modes=[SyncMode.full_refresh],
                ),
                AirbyteStream(
                    name="users",
                    namespace="reporting",
                    json_schema=_BASE_SCHEMA,
                    supported_sync_modes=[SyncMode.full_refresh],
                ),
            ]
        )

    result = compare_catalog_schemas(_namespaced(_BASE_SCHEMA), _namespaced(changed))

    assert not result.passed
    assert result.failed_streams == ["public.users"]
    assert result.stream_results["reporting.users"].passed


def test_a_stream_named_like_a_namespaced_one_is_a_different_stream():
    """`public.users` the name is not `users` in the `public` namespace.

    Keying on the formatted label made those the same stream, so a schema
    change in one could be compared against -- or hidden by -- the other.
    """
    changed = {"type": "object", "properties": {"id": {"type": "string"}}}
    control = {"streams": [{"name": "public.users", "json_schema": _BASE_SCHEMA}]}
    target = {
        "streams": [{"name": "users", "namespace": "public", "json_schema": changed}]
    }

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    # Two findings, not one comparison: the literal-name stream is gone and the
    # namespaced one is new. Both survive as separate results, since a display
    # label they happen to share must not collapse them into one entry either.
    assert len(result.errors) == 2
    assert len(result.stream_results) == 2
    assert any("missing from the target" in error for error in result.errors)
    assert any("is new in the target" in error for error in result.errors)


def test_a_stream_that_cannot_be_indexed_is_reported_not_dropped():
    """An unreadable catalog entry is not an unchanged one."""
    control = {"streams": [{"json_schema": _BASE_SCHEMA}]}
    target = {"streams": [{"name": "users", "json_schema": _BASE_SCHEMA}]}

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert any("has no name" in error for error in result.errors)


def test_the_message_counts_findings_by_kind():
    """ "Changed in N streams" lied in two directions at once.

    An entry that could not be read is not a stream, and a stream that is new is
    not changed -- but both were counted as changed streams.
    """
    result = compare_catalog_schemas(
        {"streams": [{"json_schema": _BASE_SCHEMA}]},
        {"streams": [{"name": "users", "json_schema": _BASE_SCHEMA}]},
    )

    assert (
        result.message
        == "Discovered catalog: 1 stream new in the target, 1 unreadable entry"
    )


def test_the_message_names_every_kind_it_found():
    """Each kind is counted separately, and pluralised."""
    control = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name=name,
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
            )
            for name in ("gone_a", "gone_b", "changed")
        ]
    )
    target = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="changed",
                json_schema={
                    "type": "object",
                    "properties": {"id": {"type": "string"}},
                },
                supported_sync_modes=[SyncMode.full_refresh],
            ),
            AirbyteStream(
                name="fresh",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
            ),
        ]
    )

    result = compare_catalog_schemas(control, target)

    assert result.message == (
        "Discovered catalog: 2 streams missing from the target, 1 stream changed, "
        "1 stream new in the target"
    )


def test_findings_are_ordered_by_severity():
    """A summary that lists the first few findings must not spend them on additions."""
    control = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name=name,
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
            )
            for name in ("gone", "users")
        ]
    )
    target = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="a_new",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
            ),
            AirbyteStream(
                name="users",
                json_schema={
                    "type": "object",
                    "properties": {"id": {"type": "string"}},
                },
                supported_sync_modes=[SyncMode.full_refresh],
            ),
        ]
    )

    result = compare_catalog_schemas(control, target)

    assert [error.split()[1] for error in result.errors] == ["gone", "users", "a_new"]


def test_a_catalog_that_only_grew_is_marked_additive():
    """New streams and new fields are a change to report, not one to block on."""
    control = _catalog(_BASE_SCHEMA)
    target = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="users",
                json_schema={
                    "type": "object",
                    "properties": {
                        **_BASE_SCHEMA["properties"],
                        "email": {"type": "string"},
                    },
                },
                supported_sync_modes=[SyncMode.full_refresh],
            ),
            AirbyteStream(
                name="events",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
            ),
        ]
    )

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert result.additive_only


@pytest.mark.parametrize(
    "added_key,added_value",
    [
        pytest.param("is_file_based", False, id="is_file_based"),
        pytest.param("is_resumable", True, id="is_resumable"),
        pytest.param("some_future_cdk_flag", True, id="a-key-that-does-not-exist-yet"),
    ],
)
def test_stream_metadata_a_new_cdk_adds_is_additive(added_key, added_value):
    """Found in the wild: `5.9.0` -> `master` added `is_file_based` to 47 streams.

    Every connector picks up CDK stream metadata on a routine base-image bump,
    so counting it as destructive reddened `discover` for effectively every
    certified release. The rule names the keys that carry behaviour rather than
    the ones that do not, so the next such key is additive without an edit here.
    """
    control = {"streams": [{"name": "coupons", "json_schema": _BASE_SCHEMA}]}
    target = {
        "streams": [
            {"name": "coupons", "json_schema": _BASE_SCHEMA, added_key: added_value}
        ]
    }

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert result.additive_only


@pytest.mark.parametrize(
    "control_field,target_field,expected_additive,reason",
    [
        pytest.param(
            {"id": {"type": "integer"}},
            {"id": {"type": "integer"}, "email": {"type": "string"}},
            True,
            "a new field is the case the exemption exists for",
            id="new-field",
        ),
        pytest.param(
            {"address": {"type": "object", "properties": {"city": {"type": "string"}}}},
            {
                "address": {
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "zip": {"type": "string"},
                    },
                }
            },
            True,
            "a new field one level down is still a new field",
            id="nested-new-field",
        ),
        pytest.param(
            {"created_at": {"type": "string"}},
            {"created_at": {"type": "string", "format": "date-time"}},
            False,
            "a keyword on an existing field redeclares how it is typed",
            id="format-on-existing-field",
        ),
        pytest.param(
            {"created_at": {"type": "string"}},
            {
                "created_at": {
                    "type": "string",
                    "airbyte_type": "timestamp_with_timezone",
                }
            },
            False,
            "airbyte_type decides the destination column type",
            id="airbyte-type-on-existing-field",
        ),
        pytest.param(
            {"status": {"type": "string"}},
            {"status": {"type": "string", "enum": ["a", "b"]}},
            False,
            "an enum on an existing field constrains it",
            id="enum-on-existing-field",
        ),
    ],
)
def test_growth_means_a_new_field_not_a_new_keyword_on_an_old_one(
    control_field, target_field, expected_additive, reason
):
    """The exemption said "a new field here" and accepted anything under one.

    Adding `format` or `airbyte_type` to a field that already existed changes
    how the platform types that destination column -- the "retyped or
    re-declared" class that has to gate -- and it was passing as growth.
    """
    control = {
        "streams": [{"name": "users", "json_schema": {"properties": control_field}}]
    }
    target = {
        "streams": [{"name": "users", "json_schema": {"properties": target_field}}]
    }

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert result.additive_only is expected_additive, reason


@pytest.mark.parametrize(
    "added_key,added_value",
    [
        pytest.param("namespace", "public", id="namespace-decides-where-data-lands"),
        pytest.param(
            "default_cursor_field", ["updated_at"], id="a-stream-gains-a-cursor"
        ),
        pytest.param("source_defined_primary_key", [["id"]], id="dedup-behaviour"),
        pytest.param("source_defined_cursor", True, id="who-defines-the-cursor"),
    ],
)
def test_stream_keys_that_carry_behaviour_are_not_additive(added_key, added_value):
    """The denylist is what keeps the metadata exemption from swallowing these."""
    control = {"streams": [{"name": "coupons", "json_schema": _BASE_SCHEMA}]}
    target = {
        "streams": [
            {"name": "coupons", "json_schema": _BASE_SCHEMA, added_key: added_value}
        ]
    }

    result = compare_catalog_schemas(control, target)

    assert not result.passed
    assert not result.additive_only


@pytest.mark.parametrize(
    "target_schema,reason",
    [
        pytest.param(
            {"type": "object", "properties": {"id": {"type": "string"}}},
            "a retyped field is a redeclaration",
            id="type-changed",
        ),
        pytest.param(
            {"type": "object", "properties": {}},
            "a dropped field is not growth",
            id="field-removed",
        ),
        pytest.param(
            {
                "type": "object",
                "required": ["id"],
                "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
            },
            "a key added outside the field map changes how the stream is read",
            id="required-added",
        ),
    ],
)
def test_anything_but_growth_is_not_additive(target_schema, reason):
    result = compare_catalog_schemas(_catalog(_BASE_SCHEMA), _catalog(target_schema))

    assert not result.passed
    assert not result.additive_only, reason


def test_a_removed_stream_beside_a_new_one_is_not_additive():
    """One destructive finding is enough; the additions do not dilute it."""
    control = _catalog(_BASE_SCHEMA, name="vanished")
    target = _catalog(_BASE_SCHEMA, name="brand_new")

    result = compare_catalog_schemas(control, target)

    assert not result.additive_only


def test_an_unchanged_catalog_is_not_additive_either():
    """`additive_only` answers "is this change safe", not "did nothing happen"."""
    result = compare_catalog_schemas(_catalog(_BASE_SCHEMA), _catalog(_BASE_SCHEMA))

    assert result.passed
    assert not result.additive_only


def test_a_reordered_cursor_path_fails():
    """`default_cursor_field` is a path into the record; its order is its meaning."""
    control = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="users",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
                default_cursor_field=["updated", "at"],
            )
        ]
    )
    target = AirbyteCatalog(
        streams=[
            AirbyteStream(
                name="users",
                json_schema=_BASE_SCHEMA,
                supported_sync_modes=[SyncMode.full_refresh],
                default_cursor_field=["at", "updated"],
            )
        ]
    )

    result = compare_catalog_schemas(control, target)

    assert not result.passed
