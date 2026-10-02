# flake8: noqa: TAE002
from pydantic import BaseModel, create_model
from typing import Dict, Any, List, Optional, Type, Union
import inspect

CellValue = Union[
    str,
    float,
    int,
    bool,
    Dict[str, Any],
    List[Any],
]

ColumnData = List[CellValue]

class FunctionMetadata:
    def __init__(self, name: str):
        self.function_name = name
        self.paths = {}
        self.components = {}

    def add_path(self, path_name: str, path_details: dict):
        self.paths[path_name] = path_details
    
    def add_component(self, component_name: str, component: dict):
        self.components[component_name] = component


class OpenAPISpecification:
    """
    Represents the OpenAPI specification object.
    """

    def __init__(self):
        self.openapi: Optional[str] = None
        self.info: Optional[Dict[str, Any]] = None
        self.servers: Optional[List[Dict[str, Any]]] = None
        self.paths: Optional[Dict[str, Dict[str, Any]]] = None
        self.components: Optional[Dict[str, Dict[str, Any]]] = None
        self.security: Optional[List[Dict[str, List[str]]]] = None
        self.tags: Optional[List[Dict[str, Any]]] = None
        self.externalDocs: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the OpenAPI specification object to a Python dictionary.
        """
        spec = {}
        if self.openapi:
            spec["openapi"] = self.openapi
        if self.info:
            spec["info"] = self.info
        if self.servers:
            spec["servers"] = self.servers
        if self.paths:
            spec["paths"] = self.paths
        if self.components:
            spec["components"] = self.components
        if self.security:
            spec["security"] = self.security
        if self.tags:
            spec["tags"] = self.tags
        if self.externalDocs:
            spec["externalDocs"] = self.externalDocs
        return spec
    
    def to_json(self) -> str:
        """
        Converts the OpenAPI specification object to a JSON string.
        """
        import json
        return json.dumps(self.to_dict(), indent=2)
    
    def to_yaml(self) -> str:
        """
        Converts the OpenAPI specification object to a YAML string.
        """
        import yaml
        return yaml.dump(self.to_dict(), indent=2)
    
    def serialize(self, format: str = "json") -> str:
        """
        Serializes the OpenAPI specification object to a string in the specified format.
        
        Args:
            format: The serialization format to use. Can be "json" or "yaml".
        """
        if format == "json":
            return self.to_json()
        elif format == "yaml":
            return self.to_yaml()
        else:
            raise ValueError("Invalid format. Must be 'json' or 'yaml'.")


class OpenAPISpecificationBuilder:
    """
    Builder class for constructing the OpenAPI specification object step by step.
    """

    def __init__(self, spec: Optional[OpenAPISpecification]):
        self._spec = spec

    def with_openapi(self, version: str) -> "OpenAPISpecificationBuilder":
        """
        Sets the OpenAPI version.
        """
        self._spec.openapi = version
        return self

    def with_info(
        self, title: str, version: str, description: Optional[str] = None
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the info section of the OpenAPI specification.
        """
        self._spec.info = {
            "title": title,
            "version": version,
        }
        if description:
            self._spec.info["description"] = description
        return self

    def with_servers(
        self, servers: List[Dict[str, Any]]
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the servers section of the OpenAPI specification.

        Args:
            servers: A list of server objects (dictionaries) as defined in the OpenAPI specification.
        """
        self._spec.servers = servers
        return self

    def add_server(
        self,
        url: str,
        description: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a single server to the servers section of the OpenAPI specification. If the URL is already present, it will not be added again.

        Args:
            url: The URL of the server.
            description: An optional description of the server.
            variables: An optional dictionary of variables used in the URL template.
        """
        # Append only if url is unique
        if self._spec.servers is None:
            self._spec.servers = []
        if not any(server["url"] == url for server in self._spec.servers):
            server = {"url": url}
            if description:
                server["description"] = description
            if variables:
                server["variables"] = variables
            self._spec.servers.append(server)
        return self

    def with_paths(
        self, paths: Dict[str, Dict[str, Any]]
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the paths section of the OpenAPI specification.
        """
        self._spec.paths = paths
        return self

    def add_path(
        self,
        path: str,
        operations: Dict[str, Any],
        operation_ids: Optional[Dict[str, str]] = None,
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a single path and its operations to the specification.

        Args:
            path: The path URL (e.g., "/items").
            operations: A dictionary where keys are HTTP methods (e.g., "get", "post")
                        and values are the corresponding operation definitions.
            operation_ids: An optional dictionary where keys are HTTP methods and values
                           are the unique operationIds for those methods.
        """
        if self._spec.paths is None:
            self._spec.paths = {}
        self._spec.paths[path] = operations
        if operation_ids:
            for method, operation_id in operation_ids.items():
                if method in self._spec.paths[path] and operation_id:
                    self._spec.paths[path][method]["operationId"] = operation_id
        return self

    def with_components(
        self, components: Dict[str, Dict[str, Any]]
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the components section of the OpenAPI specification.
        """
        self._spec.components = components
        return self

    def add_component(
        self, component_type: str, name: str, definition: Dict[str, Any]
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a single component to the specification.
        component_type can be 'schemas', 'responses', 'parameters', etc.
        """
        if self._spec.components is None:
            self._spec.components = {}
        if component_type not in self._spec.components:
            self._spec.components[component_type] = {}
        self._spec.components[component_type][name] = definition
        return self

    def add_schema_from_model(
        self, schema_name: str, model_class: Type[BaseModel]
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a schema definition to the components section based on a Pydantic model.

        Args:
            schema_name: The name to use for the schema in the components section.
            model_class: The Pydantic model class to generate the schema from.
        """
        schema = model_class.model_json_schema()
        self.add_component("schemas", schema_name, schema)
        return self

    def add_security_scheme(
        self, name: str, definition: Dict[str, Any]
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a security scheme definition to the components section.

        Args:
            name: The name to use for the security scheme.
            definition: A dictionary defining the security scheme (e.g., type, description, etc.).
        """
        if self._spec.components is None:
            self._spec.components = {}
        if "securitySchemes" not in self._spec.components:
            self._spec.components["securitySchemes"] = {}
        self._spec.components["securitySchemes"][name] = definition
        return self

    def with_security(
        self, security: List[Dict[str, List[str]]]
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the security section at the root level of the OpenAPI specification.
        This defines global security requirements.
        """
        self._spec.security = security
        return self

    def add_security_requirement(
        self, security_requirement: Dict[str, List[str]]
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a security requirement to the root level security section.
        This defines a global security requirement that applies to all operations.
        """
        if self._spec.security is None:
            self._spec.security = []
        self._spec.security.append(security_requirement)
        return self

    def with_tags(self, tags: List[Dict[str, Any]]) -> "OpenAPISpecificationBuilder":
        """
        Sets the tags section of the OpenAPI specification.
        """
        self._spec.tags = tags
        return self

    def add_tag(
        self, name: str, description: Optional[str] = None
    ) -> "OpenAPISpecificationBuilder":
        """
        Adds a single tag to the specification.
        """
        if self._spec.tags is None:
            self._spec.tags = []
        tag = {"name": name}
        if description:
            tag["description"] = description
        self._spec.tags.append(tag)
        return self

    def with_external_docs(
        self, description: str, url: str
    ) -> "OpenAPISpecificationBuilder":
        """
        Sets the externalDocs section of the OpenAPI specification.
        """
        self._spec.externalDocs = {
            "description": description,
            "url": url,
        }
        return self

    def build(self) -> OpenAPISpecification:
        """
        Builds and returns the final OpenAPI specification object.
        """
        return self._spec


def create_pydantic_model(
    model_name: str, parameters: List[inspect.Parameter]
) -> Type[BaseModel]:
    """
    Dynamically creates a Pydantic model class from a list of inspect.Parameter
    objects, converting pandas DataFrame/Series annotations to compatible types.

    Args:
        model_name: The name of the Pydantic model to create.
        parameters: A list of inspect.Parameter objects representing the model's fields.

    Returns:
        The dynamically created Pydantic model class.

    Raises:
        ImportError: If pandas is not installed but DataFrame/Series annotations are used.
    """
    processed_params_dict = {}  # Use a dict to build field definitions

    for param in parameters:
        annotation = param.annotation
        param_name = param.name
        param_default = param.default

        final_annotation = Any  # Default if no annotation
        final_default = ...  # Default to required (Ellipsis)

        # 1. Determine the correct annotation
        if annotation is not inspect.Parameter.empty:
            try:
                # Check for DataFrame
                if annotation.__name__ == "DataFrame":
                    final_annotation = Dict[str, ColumnData]
                # Check for Series
                elif annotation.__name__ == "Series":
                    final_annotation = Dict[str, ColumnData]
                # Otherwise, use the original annotation
                else:
                    final_annotation = annotation
            except Exception:  # Catch other potential issues with the annotation type
                final_annotation = Any
        else:
            # No annotation provided
            final_annotation = Any

        # 2. Determine the default value (or required status)
        if param_default is not inspect.Parameter.empty:
            final_default = param_default  # Use the actual default value
        # else: keep final_default = ... (Ellipsis for required)

        # 3. Add to field definitions dictionary
        processed_params_dict[param_name] = (final_annotation, final_default)

    # 4. Create the Pydantic model using the processed field definitions
    try:
        # Use type('BaseModel', (BaseModel,), {}) as base if BaseModel directly causes issues
        # But usually inheriting from BaseModel is fine.
        return create_model(
            model_name, __base__=BaseModel, **processed_params_dict
        )
    except Exception as e:
        error_msg = f"Error creating Pydantic model '{model_name}': {str(e)}"
        raise Exception(error_msg)
