from enum import Enum
from typing import TYPE_CHECKING, Any, cast

from pydantic import BaseModel
from typing_extensions import assert_never

from connector.generated import (
    AppInfo,
    AppInfoRequest,
    AppInfoResponse,
    AuthModel,
    BasicAuthentication,
    CapabilitySchema,
    JWTCredential,
    OAuth1Credential,
    OAuthAuthentication,
    OAuthAuthorization,
    OAuthClientCredentialAuthentication,
    OAuthClientCredentialAuthorization,
    ServiceAccountCredential,
    StandardCapabilityName,
    TokenAuthentication,
)
from connector.oai.capability import (
    generate_capability_schema,
)
from connector.oai.modules.base_module import BaseIntegrationModule
from connector.oai.modules.oauth_module_types import OAuthConfig, OAuthFlowType, OAuthSettings

if TYPE_CHECKING:
    from connector.oai.integration import CapabilityMetadata, Integration

"""
Some mappings for the info module.
These are used to safely map different auth models to correct types and divide the info output.
"""

AUTH_TYPE_MAPPING = {
    AuthModel.OAUTH: (OAuthAuthentication, OAuthAuthorization),
    AuthModel.OAUTH_CLIENT_CREDENTIALS: (
        OAuthClientCredentialAuthentication,
        OAuthClientCredentialAuthorization,
    ),
    AuthModel.OAUTH1: (OAuth1Credential, None),
    AuthModel.BASIC: (BasicAuthentication, None),
    AuthModel.TOKEN: (TokenAuthentication, None),
    AuthModel.JWT: (JWTCredential, None),
    AuthModel.SERVICE_ACCOUNT: (ServiceAccountCredential, None),
}

OAS_FLOW_TYPE_MAPPING = {
    OAuthFlowType.CLIENT_CREDENTIALS: "clientCredentials",
    OAuthFlowType.CODE_FLOW: "authorizationCode",
}


class InfoModule(BaseIntegrationModule):
    """
    Info module is responsible for generating the OpenAPI specification for the app.

    This module:
    - Registers the `app_info` capability on the app instance
    - Generates the OpenAPI specification for the app
    - Attaches custom information using the OAS extensions
    """

    def __init__(self):
        super().__init__()

    def register(self, integration: "Integration"):
        self.integration = integration

        self.register_info_capability()
        self.add_capability(StandardCapabilityName.APP_INFO.value)

    def register_info_capability(self):
        @self.integration.register_capability(StandardCapabilityName.APP_INFO)
        async def info_capability(args: AppInfoRequest) -> AppInfoResponse:
            """
            This is the `app_info` capability, it returns information about the app.
            This capability accepts optional settings/auth objects, just like if you were to run another capability.
            These optional objects can mutate the connector's "state" and could modify the info response,
            making this the `connected info` capability.
            """
            openapi_spec = self.generate_openapi_spec(args)
            response = AppInfoResponse(
                response=AppInfo(
                    app_id=self.integration.app_id,
                    app_schema=openapi_spec,
                )
            )

            return response

        return info_capability

    """
    Info methods
    """

    def generate_openapi_spec(self, args: AppInfoRequest) -> dict[str, Any]:
        capabilities = self.capability_schema_info()
        authentication, authorization, security_schemas = self.get_auth_schema(args)

        # Create the base specification
        spec: dict[str, Any] = self._create_base_spec()

        # Add security schemes
        spec["components"]["securitySchemes"] = security_schemas

        # Track used components
        used_refs: set[str] = set()

        # Settings schema
        if hasattr(self.integration, "settings_model"):
            self._add_settings_to_schema(
                spec,
                self.integration.settings_model,
                used_refs,
            )

        # Credentials schema
        if not self.integration.auth:
            credentials_schema = {
                "type": "array",
                "items": {
                    "allOf": [
                        {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string", "enum": [cred_id]},
                                auth_type: auth_info,
                            },
                            "required": ["id", auth_type],
                        }
                        for cred_id, auth_info in authentication.items()
                        if "type" in auth_info
                        for auth_type in [self._get_auth_type(auth_info)]
                    ]
                },
            }
        else:
            auth_schema = authentication[self.integration.app_id]

        if not self.integration.auth:
            spec["components"]["schemas"]["Credentials"] = credentials_schema

            # Add the credentials schema to the used refs and process everything
            used_refs.add("Credentials")
            self._collect_refs(credentials_schema, used_refs)
            self._process_definitions(credentials_schema, spec)
        else:
            spec["components"]["schemas"]["Auth"] = auth_schema
            used_refs.add("Auth")
            self._collect_refs(auth_schema, used_refs)
            self._process_definitions(auth_schema, spec)

        # Add paths/operations from capabilities
        for cap_name, cap_schema in capabilities.items():
            # API path
            path = f"/{cap_name.lower()}"

            # Convert Pydantic schemas to dictionaries
            request_schema = self._convert_null_type(cap_schema.argument)
            response_schema = self._convert_null_type(cap_schema.output)

            # Collect references
            self._collect_refs(request_schema, used_refs)
            self._collect_refs(response_schema, used_refs)

            # Setup proper definitions in the specification
            for schema in [request_schema, response_schema]:
                if isinstance(schema, dict):
                    self._process_definitions(schema, spec)

            # Get the processed payload references
            request_payload_schema = request_schema.get("properties", {}).get("request", {})
            response_payload_schema = response_schema.get("properties", {}).get("response", {})

            # Resolve the references
            if "$ref" in request_payload_schema:
                ref_path = request_payload_schema["$ref"].split("/")[-1]
                request_payload_schema = spec["components"]["schemas"][ref_path]
            if "$ref" in response_payload_schema:
                ref_path = response_payload_schema["$ref"].split("/")[-1]
                response_payload_schema = spec["components"]["schemas"][ref_path]

            # Determine operation category
            operation_category = "Capabilities"
            operation_subcategory: str | None = None
            if isinstance(request_payload_schema, dict):
                if "x-capability-category" in request_payload_schema:
                    operation_category = request_payload_schema[
                        "x-capability-category"
                    ].capitalize()
                if "x-capability-level" in request_payload_schema:
                    operation_subcategory = (
                        f"{request_payload_schema['x-capability-level'].capitalize()} Capabilities"
                    )

            # Request body schema
            request_body_schema: dict[str, Any] = {
                "type": "object",
                "properties": {
                    "request": request_payload_schema,
                    "settings": {
                        "$ref": f"#/components/schemas/{self.integration.settings_model.__name__}"
                        if hasattr(self.integration, "settings_model")
                        else {"type": "object", "example": "{}"},
                    },
                },
                "required": ["request", "credentials", "settings"],
            }

            # Add credentials schema to request if not an authorization capability
            if operation_category not in ["Authorization"] and not self.integration.auth:
                request_body_schema["properties"]["credentials"] = {
                    "$ref": "#/components/schemas/Credentials"
                }
            elif operation_category not in ["Authorization"] and self.integration.auth:
                request_body_schema["properties"]["auth"] = {"$ref": "#/components/schemas/Auth"}

            # Operation security schemes
            security_requirements = []
            for cred_id in authentication.keys():
                security_scheme_name = cred_id

                if authorization.get(cred_id) and "oauth_settings" in authorization[cred_id]:
                    scopes = authorization[cred_id]["oauth_settings"]["scopes"]
                    if scopes:
                        capability_scopes = list(scopes.keys())
                        security_requirements.append({security_scheme_name: capability_scopes})
                    else:
                        security_requirements.append({security_scheme_name: []})
                else:
                    security_requirements.append({security_scheme_name: []})

            # Tags
            tags = []
            if operation_subcategory:
                tags.append(operation_subcategory)
            else:
                tags.append(operation_category)  # fallback

            # Type annotations for operation
            operation: dict[str, Any] = {
                "operationId": cap_name,
                "tags": tags,
                "summary": cap_schema.display_name,
                "description": cap_schema.description,
                "requestBody": {"content": {"application/json": {"schema": request_body_schema}}},
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {"application/json": {"schema": response_payload_schema}},
                    }
                },
                "security": security_requirements,
            }

            spec["paths"][path] = {"post": operation}

        # Remove unused components
        spec["components"]["schemas"] = {
            name: schema
            for name, schema in spec["components"]["schemas"].items()
            if name in used_refs
        }

        return self._serialize_for_json(spec)

    def capabilities_info(self) -> list[str]:
        return [capability for capability in self.integration.capabilities]

    def capability_schema_info(self) -> dict[str, CapabilitySchema]:
        """Modified paste from Integration"""
        capability_names = sorted(self.integration.capabilities.keys())
        capability_schema: dict[str, CapabilitySchema] = {}
        for capability_name in capability_names:
            command_types = generate_capability_schema(
                impl=self.integration.capabilities[capability_name],
                full_schema=True,
            )

            # Capability metadata
            capability_metadata: CapabilityMetadata | None = None
            if capability_name in self.integration.capability_metadata:
                capability_metadata = self.integration.capability_metadata[capability_name]

            # Display name
            display_name: str | None = capability_name.replace("_", " ").title()
            if (
                capability_metadata is not None
                and capability_metadata.display_name is not None
                and isinstance(capability_metadata.display_name, str)
            ):
                display_name = capability_metadata.display_name

            # Description
            description = None
            if (
                capability_metadata is not None
                and capability_metadata.description is not None
                and isinstance(capability_metadata.description, str)
            ):
                description = capability_metadata.description

            # Without description, get the docstring from the capability method
            if description is None:
                description = self.integration.capabilities[capability_name].__doc__

            capability_schema[capability_name] = CapabilitySchema(
                argument=command_types.argument,
                output=command_types.output,
                display_name=display_name,
                description=description,
            )

        return capability_schema

    def get_auth_schema(
        self, args: AppInfoRequest
    ) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
        # Leaving these here for now, we can use these to mutate the spec
        # settings = get_settings(args, self.integration.settings_model)
        # auth = args.credentials

        authentication = {}
        authorization = {}
        security_schemas = {}

        if self.integration.credentials:
            """
            Forwards support for credentials
            """
            for credential in self.integration.credentials:
                security_schema_name = f"{credential.id}"

                # Model mappings
                (
                    authentication_model,
                    authorization_model,
                ) = AUTH_TYPE_MAPPING[credential.type]

                # Base models
                if credential.input_model:
                    # Custom input model provided by the app
                    authentication[credential.id] = self._get_model_extended_json_schema(
                        cast(type[BaseModel], credential.input_model)
                    )
                else:
                    # Standard input models mapped from the mapping
                    authentication[credential.id] = self._get_model_extended_json_schema(
                        cast(type[BaseModel], authentication_model)
                    )

                if authorization_model:
                    # Not every app has an authorization model
                    authorization[credential.id] = self._get_model_extended_json_schema(
                        cast(type[BaseModel], authorization_model)
                    )

                # Markdown data
                authentication[credential.id]["description"] = credential.description

                # Specific connector OAuth settings
                if isinstance(credential, OAuthConfig) and credential.oauth_settings:
                    oauth = credential.oauth_settings
                    scopes = self.get_oauth_scopes(credential.id, args)

                    token_url = ""
                    authorization_url = ""

                    # Get token URL and authorization URL
                    if callable(oauth.token_url):
                        try:
                            token_url = oauth.token_url(args)
                        except Exception as _:
                            token_url = ""
                    else:
                        token_url = oauth.token_url or ""

                    if callable(oauth.authorization_url):
                        try:
                            authorization_url = oauth.authorization_url(args)
                        except Exception as _:
                            authorization_url = ""
                    else:
                        authorization_url = oauth.authorization_url or ""

                    # Custom object
                    authorization[credential.id]["oauth_settings"] = {
                        "oauth_type": oauth.flow_type,
                        "token_url": token_url,
                        "authorization_url": authorization_url,
                        "scopes": scopes,
                        "pkce_enabled": oauth.pkce,
                    }

                    # Process OAS flows
                    flows: dict[str, Any] = {}
                    flow_type = OAS_FLOW_TYPE_MAPPING[oauth.flow_type]
                    if flow_type == "authorizationCode":
                        flows[flow_type] = {}
                        flows[flow_type]["authorizationUrl"] = authorization_url or ""
                        flows[flow_type]["tokenUrl"] = token_url or ""
                        flows[flow_type]["scopes"] = scopes or {}
                    elif flow_type == "clientCredentials":
                        flows[flow_type] = {}
                        flows[flow_type]["tokenUrl"] = token_url or ""
                        flows[flow_type]["scopes"] = scopes or {}

                    security_schemas[security_schema_name] = {
                        "type": "oauth2",
                        "flows": flows,
                    }
                else:
                    if credential.type == AuthModel.TOKEN or credential.type == AuthModel.JWT:
                        security_schemas[security_schema_name] = {
                            "type": "apiKey",
                            "in": "header",
                            "name": "Authorization",
                            "description": "API Token / API Key for authentication",
                        }
                    elif credential.type == AuthModel.BASIC:
                        security_schemas[security_schema_name] = {
                            "type": "http",
                        }
        elif self.integration.auth:
            """
            Backwards support for auth settings

            Note: This can be removed once 'auth' is phased out and only 'credentials' is used.
            """
            security_schema_name = f"{self.integration.app_id}"
            auth_model = self._get_model_extended_json_schema(self.integration.auth)
            auth_type = AuthModel(auth_model["x-credential-type"])

            authentication[self.integration.app_id] = {
                "properties": {
                    auth_type: {
                        "type": "object",
                        **auth_model,
                    },
                },
                "required": [auth_type],
            }
            integration_oauth_settings: OAuthSettings | None = self.integration.oauth_settings

            match auth_type:
                case AuthModel.OAUTH:
                    authorization_url = ""
                    if integration_oauth_settings is not None:
                        if callable(integration_oauth_settings.authorization_url):
                            try:
                                authorization_url = integration_oauth_settings.authorization_url(
                                    args
                                )
                            except Exception as _:
                                authorization_url = ""
                        else:
                            authorization_url = integration_oauth_settings.authorization_url or ""

                    security_schemas[security_schema_name] = {
                        "type": "oauth2",
                        "flows": {
                            "authorizationCode": {
                                "authorizationUrl": authorization_url,
                            },
                        },
                    }
                case AuthModel.OAUTH_CLIENT_CREDENTIALS:
                    token_url = ""
                    if integration_oauth_settings is not None:
                        if callable(integration_oauth_settings.token_url):
                            try:
                                token_url = integration_oauth_settings.token_url(args)
                            except Exception as _:
                                token_url = ""
                        else:
                            token_url = integration_oauth_settings.token_url or ""

                    security_schemas[security_schema_name] = {
                        "type": "oauth2",
                        "flows": {
                            "clientCredentials": {
                                "tokenUrl": token_url,
                            },
                        },
                    }
                case AuthModel.OAUTH1:
                    security_schemas[security_schema_name] = {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                        "description": "OAuth 1.0a signed request token for authentication",
                    }  # OAS does not support legacy OAuth officially
                case AuthModel.TOKEN:
                    security_schemas[security_schema_name] = {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                        "description": "API Token / API Key for authentication",
                    }
                case AuthModel.BASIC:
                    security_schemas[security_schema_name] = {
                        "type": "http",
                    }
                case AuthModel.JWT:
                    security_schemas[security_schema_name] = {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                        "description": "JWT Token for authentication",
                    }
                case AuthModel.SERVICE_ACCOUNT:
                    # TODO: this might not be 100% accurate
                    security_schemas[security_schema_name] = {
                        "type": "apiKey",
                        "in": "header",
                        "name": "Authorization",
                        "description": "Service Account Token for authentication",
                    }
                case _:
                    assert_never(auth_type)

        return authentication, authorization, security_schemas

    def get_oauth_scopes(self, credential_id: str, args: AppInfoRequest) -> dict[str, str]:
        oauth_scopes: dict[str, str] = {}

        for credential in self.integration.credentials:
            if credential.id == credential_id:
                if isinstance(credential.oauth_settings, OAuthConfig) and isinstance(
                    credential.oauth_settings, OAuthSettings
                ):
                    scopes = credential.oauth_settings.scopes

                    if scopes is None:
                        continue

                    if callable(scopes):
                        scopes = scopes(args)

                    oauth_scopes = {
                        scope: f"Required for {capability}"
                        for capability, scope in scopes.items()
                        if scope is not None
                    }

                break

        return oauth_scopes

    """
    Utilities
    """

    def _collect_refs(self, schema: dict[str, Any], refs: set[str]) -> None:
        if not isinstance(schema, dict):
            return

        if "$ref" in schema:
            ref_name = schema["$ref"].split("/")[-1]
            refs.add(ref_name)

        # Recursively process nested objects and arrays
        for value in schema.values():
            if isinstance(value, dict):
                self._collect_refs(value, refs)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._collect_refs(item, refs)

    def _create_base_spec(self) -> dict[str, Any]:
        """
        Creates the base specification for the app.
        """

        # App instance
        app = self.integration
        entitlement_types = app.entitlement_types
        resource_types = app.resource_types

        return {
            "openapi": "3.0.0",
            "info": {
                "x-app-id": app.app_id,
                "x-app-logo-url": app.description_data.logo_url,
                "title": app.description_data.user_friendly_name,
                "description": app.description_data.description,
                "version": app.version,
                "x-entitlement-types": [
                    entitlement_type.model_dump() for entitlement_type in entitlement_types
                ],
                "x-resource-types": [
                    resource_type.model_dump() for resource_type in resource_types
                ],
                "x-categories": {
                    "type": "enum",
                    "enum": [category.value for category in app.description_data.categories],
                },
            },
            "servers": [],
            "paths": {},
            "components": {"securitySchemes": {}, "schemas": {}},
            "tags": [
                {
                    "name": "Read Capabilities",
                    "description": "These capabilities only perform read operations.",
                },
                {
                    "name": "Write Capabilities",
                    "description": "These capabilities perform write operations on top of potential read operations.",
                },
                {
                    "name": "Authorization",
                    "description": "OAuth 2.0 authorization capabilities.",
                },
                {
                    "name": "Specification",
                    "description": "Capabilities used for specifying the connector's capabilities.",
                },
            ],
        }

    def _replace_entitlement_types(self, spec: dict[str, Any]) -> None:
        """
        Replaces the entitlement types in the spec with the entitlement types from the integration.
        Depends on the x-entitlement-type extension to be set on the property level.
        """
        spec["properties"]["entitlement_type"] = {
            "type": "string",
            "title": spec["properties"]["entitlement_type"]["title"],
            "description": spec["properties"]["entitlement_type"]["description"],
            "enum": [
                entitlement_type.type_id for entitlement_type in self.integration.entitlement_types
            ],
        }

    def _replace_resource_types(self, spec: dict[str, Any]) -> None:
        """
        Replaces the resource types in the spec with the resource types from the integration.
        Depends on the x-resource-type extension to be set on the property level.
        """
        spec["properties"]["resource_type"] = {
            "type": "string",
            "title": spec["properties"]["resource_type"]["title"],
            "description": spec["properties"]["resource_type"]["description"],
            "enum": [resource_type.type_id for resource_type in self.integration.resource_types],
        }

    def _convert_null_type(self, schema: dict[str, Any]) -> dict[str, Any]:
        """Convert types with null type to nullable recursively."""
        if not isinstance(schema, dict):
            return schema

        # Handle single-value enums (do we even use those? what is TokenType for?)
        if "const" in schema:
            schema["enum"] = [schema.pop("const")]
            return schema

        # Handle anyOf definitions
        if "anyOf" in schema:
            types = [item for item in schema["anyOf"] if item.get("type") != "null"]
            has_null = len(types) != len(schema["anyOf"])

            if has_null and len(types) == 1:
                result = types[0]
                result["nullable"] = True
                return result

        # Recursively process all objects, sometimes this is more nested
        for key, value in schema.items():
            if isinstance(value, dict):
                schema[key] = self._convert_null_type(value)
            elif isinstance(value, list):
                schema[key] = [
                    self._convert_null_type(item) if isinstance(item, dict) else item
                    for item in value
                ]

        return schema

    def _dump_credentials(self) -> list[dict[str, Any]]:
        credentials_dump = []
        for cred in self.integration.credentials:
            cred_dict = cred.model_dump()
            if "input_model" in cred_dict:
                del cred_dict["input_model"]
            credentials_dump.append(cred_dict)
        return credentials_dump

    def _get_model_extended_json_schema(self, model: type[BaseModel]) -> dict[str, Any]:
        json_schema = model.model_json_schema()
        field_order = list(model.model_fields.keys())
        json_schema["x-field_order"] = field_order
        return json_schema

    # Temp potentially
    def _serialize_for_json(self, obj: Any) -> Any:
        """Serialize Python objects for JSON output, handling special cases."""
        if obj is None:
            return None
        elif isinstance(obj, str | int | float | bool):
            return obj
        elif isinstance(obj, list | tuple | set):
            return [self._serialize_for_json(item) for item in obj]
        elif isinstance(obj, dict):
            return {
                key: self._serialize_for_json(value)
                for key, value in obj.items()
                if value is not None  # Skip None values
            }
        elif hasattr(obj, "model_dump"):  # Pydantic models
            return self._serialize_for_json(obj.model_dump())
        elif hasattr(obj, "__dict__"):  # Other objects with __dict__
            return self._serialize_for_json(obj.__dict__)
        else:
            return str(obj)  # Fallback to string representation

    def _process_definitions(self, obj: dict[str, Any] | list[Any], spec: dict[str, Any]) -> None:
        if isinstance(obj, dict):
            if "$defs" in obj:
                for def_name, def_schema in obj.pop("$defs").items():
                    if def_name not in spec["components"]["schemas"]:
                        spec["components"]["schemas"][def_name] = def_schema

                    # Perform some replace operations based on extensions
                    if any(
                        "x-entitlement-type" in property_schema
                        for property_schema in def_schema.get("properties", {}).values()
                    ):
                        self._replace_entitlement_types(def_schema)

                    if any(
                        "x-resource-type" in property_schema
                        for property_schema in def_schema.get("properties", {}).values()
                    ):
                        self._replace_resource_types(def_schema)

            if "$ref" in obj and obj["$ref"].startswith("#/$defs"):
                obj["$ref"] = "#/components/schemas/" + obj["$ref"].split("/")[-1]

        # Recursively process nested dictionaries and lists
        if isinstance(obj, dict):
            for value in obj.values():
                self._process_definitions(value, spec)

        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    self._process_definitions(item, spec)

    def _get_auth_type(self, auth_info: dict[str, Any]) -> str:
        credential_type = auth_info.get("x-credential-type", "unknown")

        if credential_type != "unknown":
            return AuthModel(credential_type).value

        return credential_type

    def _add_settings_to_schema(
        self, spec: dict[str, Any], model: type[BaseModel], used_refs: set[str]
    ):
        name = model.__name__
        if not hasattr(model, "model_json_schema"):
            raise ValueError(f"Model {name} does not have a model_json_schema method")

        schema = model.model_json_schema()
        spec["components"]["schemas"][name] = schema
        used_refs.add(name)

        # Clean up
        if "$defs" in schema:
            del schema["$defs"]

        # Add enum schemas
        for field_name, field in model.model_fields.items():
            annotation = field.annotation
            if isinstance(annotation, type) and issubclass(annotation, Enum):
                enum_schema = {
                    "type": "string",
                    "enum": [e.value for e in annotation],
                    "title": annotation.__name__,
                    "description": annotation.__doc__,
                }
                spec["components"]["schemas"][annotation.__name__] = enum_schema
                # Update the reference in the model schema
                if "properties" in schema:
                    schema["properties"][field_name][
                        "$ref"
                    ] = f"#/components/schemas/{annotation.__name__}"
                    used_refs.add(annotation.__name__)

        # Add other referenced schemas
        for ref_name, ref_schema in schema.get("definitions", {}).items():
            if ref_name not in spec["components"]["schemas"]:
                spec["components"]["schemas"][ref_name] = ref_schema
                used_refs.add(ref_name)
        for field_name, field in schema.get("properties", {}).items():
            if isinstance(field, dict) and "$ref" in field:
                ref_key = field["$ref"].split("/")[-1]  # Extract schema name from $ref
                if ref_key not in spec["components"]["schemas"]:
                    annotation = model.model_fields[field_name].annotation
                    if annotation and hasattr(annotation, "model_json_schema"):
                        nested_schema = annotation.model_json_schema(
                            ref_template="#/components/schemas/{model}"
                        )
                        spec["components"]["schemas"][ref_key] = nested_schema
                        used_refs.add(ref_key)
