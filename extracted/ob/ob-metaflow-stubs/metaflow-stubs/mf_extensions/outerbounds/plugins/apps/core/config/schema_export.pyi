######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.600127                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


HAS_YAML: bool

def to_openapi_schema(config_class) -> typing.Dict[str, typing.Any]:
    """
    Generate OpenAPI schema for a configuration class.
    
    Args:
        config_class: The configuration class to generate schema for
    
    Returns:
        OpenAPI schema dictionary
    """
    ...

def to_json_schema(config_class) -> typing.Dict[str, typing.Any]:
    """
    Generate JSON schema for a configuration class.
    
    Args:
        config_class: The configuration class to generate schema for
    
    Returns:
        JSON schema dictionary
    """
    ...

def export_schema(config_class, filepath: str, schema_type: str = 'openapi', format: str = 'yaml'):
    """
    Export configuration schema to file.
    
    Args:
        config_class: The configuration class to export schema for
        filepath: Path to save the schema file
        schema_type: Type of schema to generate ('openapi' or 'json')
        format: Output format ('yaml' or 'json')
    
    Examples:
        # Export OpenAPI schema as YAML (default)
        export_schema(CoreConfig, "schema.yaml")
    
        # Export JSON schema as YAML
        export_schema(CoreConfig, "schema.yaml", schema_type="json")
    
        # Export OpenAPI schema as JSON
        export_schema(CoreConfig, "schema.json", schema_type="openapi", format="json")
    
        # Export JSON schema as JSON
        export_schema(CoreConfig, "schema.json", schema_type="json", format="json")
    """
    ...

