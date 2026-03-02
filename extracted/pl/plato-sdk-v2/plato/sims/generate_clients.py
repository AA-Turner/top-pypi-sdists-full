#!/usr/bin/env python
"""Generate API clients for all sims from their OpenAPI specs.

Auto-discovers sims from the specs/ directory:
- If a sim has default.yaml/default.json: generates directly into sims/{sim}/
- If a sim has multiple specs (no default): generates into sims/{sim}/{spec_name}/

Usage:
    uv run python -m plato.sims.generate_clients
"""

import json
import shutil
from pathlib import Path

import yaml

from plato._sims_generator import AuthConfig, PythonGenerator, parse_openapi

SIMS_DIR = Path(__file__).parent
SPECS_DIR = SIMS_DIR / "specs"


def _fix_spec(spec: dict) -> dict:
    """Fix common OpenAPI spec issues."""
    # Fix response codes that are integers instead of strings
    if "paths" in spec:
        for path, methods in spec["paths"].items():
            if isinstance(methods, dict):
                for method, details in methods.items():
                    if isinstance(details, dict) and "responses" in details:
                        responses = details["responses"]
                        if isinstance(responses, dict):
                            new_responses = {}
                            for code, response in responses.items():
                                new_responses[str(code)] = response
                            details["responses"] = new_responses
    return spec


def _load_spec(spec_path: Path) -> dict:
    """Load and fix an OpenAPI spec."""
    with open(spec_path) as f:
        if spec_path.suffix == ".json":
            spec = json.load(f)
        else:
            spec = yaml.safe_load(f)
    return _fix_spec(spec)


def _get_spec_files(sim_dir: Path) -> list[Path]:
    """Get all spec files in a sim directory (excluding auth.yaml)."""
    specs = []
    for ext in (".yaml", ".yml", ".json"):
        for f in sim_dir.glob(f"*{ext}"):
            if f.name != "auth.yaml":
                specs.append(f)
    return sorted(specs)


def _generate_single(
    name: str,
    spec_path: Path,
    auth_config: AuthConfig,
    output_dir: Path,
    package_name: str,
) -> None:
    """Generate a single client from a spec."""
    # Clean output dir
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load and parse spec
    spec = _load_spec(spec_path)
    api = parse_openapi(spec)
    print(f"    Parsed {len(api.endpoints)} endpoints from {spec_path.name}")
    print(f"    API title: {api.title}")

    # Generate
    generator = PythonGenerator(
        api=api,
        output_path=output_dir,
        spec=spec,
        package_name=package_name,
        auth_config=auth_config,
    )
    generator.generate()
    print(f"    Generated to: {output_dir}")


def generate_sim(name: str) -> None:
    """Generate client(s) for a single sim."""
    print(f"\n{'=' * 60}")
    print(f"Generating {name} client(s)...")
    print(f"{'=' * 60}")

    spec_dir = SPECS_DIR / name
    auth_path = spec_dir / "auth.yaml"

    if not auth_path.exists():
        print(f"  Skipping {name}: no auth.yaml found")
        return

    # Load auth config
    auth_config = AuthConfig.from_yaml(auth_path)
    print(f"  Auth type: {auth_config.type}")
    print(f"  Env prefix: {auth_config.env_prefix}")

    # Get spec files
    spec_files = _get_spec_files(spec_dir)
    if not spec_files:
        print(f"  Skipping {name}: no spec files found")
        return

    # Check for default spec
    default_spec = None
    for sf in spec_files:
        if sf.stem == "default":
            default_spec = sf
            break

    if default_spec:
        # Single default spec - generate directly into sims/{name}/
        print(f"  Found default spec: {default_spec.name}")
        output_dir = SIMS_DIR / name
        _generate_single(name, default_spec, auth_config, output_dir, name)
    else:
        # Multiple specs - generate into sims/{name}/{spec_name}/
        print(f"  Found {len(spec_files)} specs: {[f.stem for f in spec_files]}")

        # Clean parent dir first
        parent_dir = SIMS_DIR / name
        if parent_dir.exists():
            shutil.rmtree(parent_dir)
        parent_dir.mkdir(parents=True, exist_ok=True)

        for spec_path in spec_files:
            spec_name = spec_path.stem
            print(f"\n  Generating {name}.{spec_name}...")
            output_dir = SIMS_DIR / name / spec_name
            _generate_single(name, spec_path, auth_config, output_dir, spec_name)

        # Create parent __init__.py that re-exports sub-modules
        sub_modules = [sf.stem for sf in spec_files]
        parent_init = parent_dir / "__init__.py"
        parent_init.write_text(f'''"""Generated {name.title()} API clients.

This sim has multiple APIs:
{chr(10).join(f"- {name}.{m}: {m.title()} API" for m in sub_modules)}

Usage:
    from plato.sims.{name} import {", ".join(sub_modules)}

    client = await {sub_modules[0]}.AsyncClient.create(base_url="...")
"""

{"".join(f"from . import {m}{chr(10)}" for m in sub_modules)}
__all__ = {sub_modules!r}
''')


def discover_sims() -> list[str]:
    """Discover all sims from the specs directory."""
    sims = []
    for d in SPECS_DIR.iterdir():
        if d.is_dir() and (d / "auth.yaml").exists():
            sims.append(d.name)
    return sorted(sims)


def main():
    """Generate all sim clients."""
    print("Generating sim clients from OpenAPI specs...")
    print(f"Specs directory: {SPECS_DIR}")

    sims = discover_sims()
    print(f"Discovered sims: {sims}")

    generated = []
    for name in sims:
        try:
            generate_sim(name)
            generated.append(name)
        except Exception as e:
            print(f"  ERROR generating {name}: {e}")
            import traceback

            traceback.print_exc()

    print("\n" + "=" * 60)
    print("Done! Generated clients:")
    for name in generated:
        print(f"  - plato.sims.{name}")
    print("=" * 60)


if __name__ == "__main__":
    main()
