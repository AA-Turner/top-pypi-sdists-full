from collections.abc import Callable
from dataclasses import dataclass

from connector.oai.integration import Integration
from connector_sdk_types import OAS
from connector_sdk_types.generated import OpenAPISpecificationInfo, StandardCapabilityName


@dataclass
class SchemaLinterCheck:
    """A single schema linter check rule."""

    name: str
    description: str
    check: Callable[[OAS.OpenAPI, OpenAPISpecificationInfo, Integration, str], None]
    severity: str = "error"  # "error" or "warning"


def check_capabilities_not_empty(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    assert (
        info.x_capabilities is not None and info.x_capabilities != []
    ), f"{name}: x-capabilities should not be empty"


def check_logo_url(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    assert (
        info.x_app_logo_url is not None and info.x_app_logo_url != ""
    ), f"{name}: x-app-logo-url should not be empty"


def check_multi_auth_consistency(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that multi-auth flag matches actual credentials."""
    is_multi_auth = info.x_multi_credential
    has_multiple_creds = len(integration.credentials) >= 1 if integration.credentials else False

    if is_multi_auth != has_multiple_creds:
        raise AssertionError(
            f"{name}: x-multi-credential ({is_multi_auth}) doesn't match "
            f"actual credentials count ({len(integration.credentials) if integration.credentials else 0})"
        )


def check_allowed_credentials_valid(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that allowed credentials reference valid credential IDs."""
    if not info.x_multi_credential:
        return  # Skip for single-auth connectors

    if not info.x_allowed_credentials:
        raise AssertionError(f"{name}: x-allowed-credentials should not be empty for multi-auth")

    credential_ids = {cred.id for cred in (integration.credentials or [])}
    for allowed_group in info.x_allowed_credentials:
        for cred_id in allowed_group:
            assert (
                cred_id in credential_ids
            ), f"{name}: x-allowed-credentials references unknown credential {cred_id}"


def check_capabilities_match_integration(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that spec capabilities match integration capabilities."""
    spec_caps = set(info.x_capabilities or [])
    integration_caps = set(integration.capabilities.keys())

    # Spec should include all integration capabilities
    missing = integration_caps - spec_caps
    assert not missing, f"{name}: Missing capabilities in spec: {missing}"

    # Spec shouldn't have extra capabilities (unless they're standard ones)
    extra = spec_caps - integration_caps
    if extra:
        # Allow standard capabilities that might be auto-added
        standard_caps = {StandardCapabilityName.APP_INFO.value}
        unexpected = extra - standard_caps
        assert not unexpected, f"{name}: Unexpected capabilities in spec: {unexpected}"


def check_paths_have_operations(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that all paths have at least one operation."""
    for path, path_item in spec.paths.items():
        assert path_item, f"{name}: Path {path} has no operations"
        # Check that operations have required fields
        assert path_item.post is not None, f"{name}: {path} missing post operation"

        operation = path_item.post

        assert operation.operationId is not None, f"{name}: {path} missing operationId"
        assert (
            operation.responses is not None and operation.responses != {}
        ), f"{name}: {path} missing responses"


def check_settings_schema_present(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that settings schema is present if integration has settings."""
    if hasattr(integration, "settings_model") and integration.settings_model:
        assert (
            spec.components is not None and spec.components.schemas is not None
        ), f"{name}: components and schemas must be present"

        assert (
            spec.components.schemas.get("Settings") is not None
        ), f"{name}: Missing Settings schema in components"


def check_components_and_schemas_present(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that components and schemas are present."""
    assert isinstance(spec.components, OAS.Components), f"{name}: components must be a dict"
    assert (
        spec.components.schemas is not None and spec.components.schemas != {}
    ), f"{name}: components.schemas must be present"


def check_vendor_domain_and_types(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that vendor domain, entitlement and resource types are present."""
    assert info.x_app_vendor_domain is not None, f"{name}: x-app-vendor-domain should be set"
    assert info.x_entitlement_types is not None, f"{name}: x-entitlement-types should not be empty"
    assert info.x_resource_types is not None, f"{name}: x-resource-types should not be empty"


def check_allowed_credentials_groups_non_empty(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that each allowed credentials group is non-empty when multi-auth is enabled."""
    if not info.x_multi_credential:
        return

    if not info.x_allowed_credentials:
        raise AssertionError(f"{name}: x-allowed-credentials should not be empty for multi-auth")

    for allowed_group in info.x_allowed_credentials:
        assert len(allowed_group) > 0, f"{name}: x-allowed-credentials groups should not be empty"


def check_app_categories_present(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that app categories are present."""
    assert (
        info.x_categories is not None and info.x_categories != {}
    ), f"{name}: x-categories must be present"
    assert info.x_categories.get("type") == "enum", f"{name}: x-categories type must be enum"
    assert info.x_categories.get("enum") is not None, f"{name}: x-categories enum must be present"


def check_entitlement_rules_reference_valid_types(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that access graph entitlement rules reference valid entitlement and resource types."""
    if not info.x_access_graph_entitlement_rules:
        return

    valid_entitlement_type_ids = {t.type_id for t in (info.x_access_graph_entitlement_types or [])}
    valid_resource_type_ids = {t.type_id for t in (info.x_resource_types or [])}

    for rule in info.x_access_graph_entitlement_rules:
        assert rule.entitlement_type in valid_entitlement_type_ids, (
            f"{name}: access_graph_entitlement_rule references unknown entitlement type "
            f"'{rule.entitlement_type}' (valid: {sorted(valid_entitlement_type_ids)})"
        )
        assert rule.resource_type in valid_resource_type_ids, (
            f"{name}: access_graph_entitlement_rule references unknown resource type "
            f"'{rule.resource_type}' (valid: {sorted(valid_resource_type_ids)})"
        )


def check_implied_access_rules_reference_valid_types(
    spec: OAS.OpenAPI, info: OpenAPISpecificationInfo, integration: Integration, name: str
) -> None:
    """Check that implied access rules reference valid entitlement and resource types."""
    if not info.x_implied_access_rules:
        return

    valid_entitlement_type_ids = {t.type_id for t in (info.x_access_graph_entitlement_types or [])}
    valid_resource_type_ids = {t.type_id for t in (info.x_resource_types or [])}

    for rule in info.x_implied_access_rules:
        assert rule.from_entitlement_type in valid_entitlement_type_ids, (
            f"{name}: implied_access_rule references unknown from_entitlement_type "
            f"'{rule.from_entitlement_type}' (valid: {sorted(valid_entitlement_type_ids)})"
        )
        assert rule.from_resource_type in valid_resource_type_ids, (
            f"{name}: implied_access_rule references unknown from_resource_type "
            f"'{rule.from_resource_type}' (valid: {sorted(valid_resource_type_ids)})"
        )
        assert rule.to_entitlement_type in valid_entitlement_type_ids, (
            f"{name}: implied_access_rule references unknown to_entitlement_type "
            f"'{rule.to_entitlement_type}' (valid: {sorted(valid_entitlement_type_ids)})"
        )
        assert rule.to_resource_type in valid_resource_type_ids, (
            f"{name}: implied_access_rule references unknown to_resource_type "
            f"'{rule.to_resource_type}' (valid: {sorted(valid_resource_type_ids)})"
        )


# All schema linter checks
SCHEMA_CHECK_LIST: list[SchemaLinterCheck] = [
    SchemaLinterCheck(
        "capabilities_not_empty",
        "Connector must expose at least one capability",
        check_capabilities_not_empty,
    ),
    SchemaLinterCheck(
        "logo_url_present",
        "Connector must have a logo URL",
        check_logo_url,
    ),
    SchemaLinterCheck(
        "multi_auth_consistency",
        "Multi-auth flag must match actual credentials",
        check_multi_auth_consistency,
    ),
    SchemaLinterCheck(
        "allowed_credentials_valid",
        "Allowed credentials must reference valid credential IDs",
        check_allowed_credentials_valid,
    ),
    SchemaLinterCheck(
        "capabilities_match",
        "Spec capabilities must match integration capabilities",
        check_capabilities_match_integration,
    ),
    SchemaLinterCheck(
        "paths_have_operations",
        "All paths must have at least one operation",
        check_paths_have_operations,
    ),
    SchemaLinterCheck(
        "settings_schema_present",
        "Settings schema must be present if integration has settings",
        check_settings_schema_present,
    ),
    SchemaLinterCheck(
        "components_and_schemas_present",
        "Components and schemas must be present",
        check_components_and_schemas_present,
    ),
    SchemaLinterCheck(
        "vendor_domain_and_types_present",
        "Vendor domain, entitlement types and resource types must be present",
        check_vendor_domain_and_types,
    ),
    SchemaLinterCheck(
        "allowed_credentials_groups_non_empty",
        "Each allowed credentials group must be non-empty for multi-auth connectors",
        check_allowed_credentials_groups_non_empty,
    ),
    SchemaLinterCheck(
        "app_categories_present",
        "App categories must be an enum",
        check_app_categories_present,
    ),
    SchemaLinterCheck(
        "entitlement_rules_reference_valid_types",
        "Access graph entitlement rules must reference declared entitlement and resource types",
        check_entitlement_rules_reference_valid_types,
    ),
    SchemaLinterCheck(
        "implied_access_rules_reference_valid_types",
        "Implied access rules must reference declared entitlement and resource types",
        check_implied_access_rules_reference_valid_types,
    ),
]
