"""OpenAPI SDK Generator for Plato.

This module provides tools to generate Python SDKs from OpenAPI specifications,
as well as instruction-based SDKs for sims that don't need API clients.

Usage (OpenAPI-based):
    from plato._sims_generator import parse_openapi, PythonGenerator, OAuthConfig

    api = parse_openapi(spec_dict)
    generator = PythonGenerator(
        api,
        output_path,
        spec=spec_dict,
        package_name="spree",
        env_prefix="SPREE",
        oauth_config=OAuthConfig(
            client_id="...",
            client_secret="...",
            token_endpoint="/spree_oauth/token",
            scope="admin",
        ),
    )
    generator.generate()

Usage (Instruction-based):
    from plato._sims_generator import InstructionConfig, InstructionGenerator

    config = InstructionConfig.from_yaml(Path("specs/instructions.yaml"))
    generator = InstructionGenerator(
        config,
        output_path,
        package_name="localstack",
    )
    generator.generate()

Or via CLI:
    plato sims publish --config plato-config.yml
"""

from .instruction import InstructionConfig, InstructionGenerator
from .parser import API, Endpoint, Schema, Type, parse_openapi
from .python import AuthConfig, BasicAuthConfig, BearerTokenConfig, OAuthConfig, PythonGenerator, SessionAuthConfig

__all__ = [
    "API",
    "Endpoint",
    "Schema",
    "Type",
    "parse_openapi",
    "PythonGenerator",
    "AuthConfig",
    "OAuthConfig",
    "BearerTokenConfig",
    "BasicAuthConfig",
    "SessionAuthConfig",
    "InstructionConfig",
    "InstructionGenerator",
]
