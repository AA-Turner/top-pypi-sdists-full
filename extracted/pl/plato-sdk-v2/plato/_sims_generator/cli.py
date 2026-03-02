"""CLI for generating SDK from OpenAPI specs."""

import json
from pathlib import Path
from typing import Any

import click
import yaml

from .parser import parse_openapi
from .python import PythonGenerator


def fix_spec(spec: dict[str, Any]) -> dict[str, Any]:
    """Fix common issues in OpenAPI specs.

    - Convert integer response codes to strings
    - Strip whitespace from tags
    """
    # Fix response codes (must be strings)
    paths = spec.get("paths", {})
    for path_item in paths.values():
        if not isinstance(path_item, dict):
            continue
        for method in ["get", "post", "put", "patch", "delete", "head", "options"]:
            operation = path_item.get(method)
            if not operation or not isinstance(operation, dict):
                continue

            # Fix tags - strip whitespace
            if "tags" in operation:
                operation["tags"] = [t.strip() if isinstance(t, str) else t for t in operation["tags"]]

            # Fix response codes
            responses = operation.get("responses")
            if responses and isinstance(responses, dict):
                fixed_responses = {}
                for code, response in responses.items():
                    fixed_responses[str(code)] = response
                operation["responses"] = fixed_responses

    return spec


@click.command()
@click.option("--path", type=click.Path(exists=True), required=True, help="Path to OpenAPI spec file")
@click.option("--output", "-o", type=click.Path(), required=True, help="Output directory")
@click.option("--package", "-p", default="generated", help="Package name for imports")
@click.option("--env-prefix", "-e", default="API", help="Environment variable prefix (e.g., SPREE, FIREFLY)")
def generate(path: str, output: str, package: str, env_prefix: str):
    """Generate Python SDK from OpenAPI spec."""
    click.echo(f"Loading spec from {path}...")
    with open(path) as f:
        if path.endswith((".yml", ".yaml")):
            spec = yaml.safe_load(f)
        else:
            spec = json.load(f)

    # Fix common spec issues
    spec = fix_spec(spec)

    # Parse spec
    click.echo("Parsing OpenAPI spec...")
    api = parse_openapi(spec)
    click.echo(f"Found {len(api.endpoints)} endpoints and {len(api.schemas)} schemas")

    # Generate
    output_path = Path(output)
    click.echo(f"Generating Python SDK to {output_path} (env prefix: {env_prefix.upper()})...")

    generator = PythonGenerator(api, output_path, spec=spec, package_name=package, env_prefix=env_prefix)
    generator.generate()

    click.echo("Done!")


def main():
    """Entry point for CLI."""
    generate()


if __name__ == "__main__":
    main()
