# /// script
# requires-python = ">=3.13"
# dependencies = []
# ///

"""Generate protobuf files from .proto definitions."""

import shutil
import subprocess
import sys
from pathlib import Path

try:
    from hatchling.builders.hooks.plugin.interface import BuildHookInterface  # type: ignore
except ImportError:
    # BuildHookInterface not available (not in build context)
    BuildHookInterface = object


def find_proto_files(proto_dir: Path) -> list[str]:
    """Find all .proto files in the given directory."""
    return [str(p) for p in proto_dir.rglob("*.proto")]


def generate_protos():
    """Generate protobuf files."""

    # Paths
    proto_root = Path("protos")
    # Only generate protos for the orby package
    input_proto_dir = proto_root / "orby/va/public"
    # Generate directly into the va package
    out_dir = Path("va/protos")

    # Clear previous generated files if the output directory exists; otherwise, create it.
    if out_dir.exists():
        for item in out_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    else:
        out_dir.mkdir(parents=True, exist_ok=True)

    # Find all proto files
    proto_files = find_proto_files(input_proto_dir)
    if not proto_files:
        print("No .proto files found")
        return

    print(f"Found {len(proto_files)} proto files")

    # Build protoc command
    cmd = [
        sys.executable,
        "-m",
        "grpc_tools.protoc",
        f"--proto_path={proto_root}",
        f"--python_out={out_dir}",
        f"--grpc_python_out={out_dir}",
        f"--mypy_out={out_dir}",
        *proto_files,
    ]

    print("Generating protobuf files...")
    result = subprocess.run(cmd, check=False)

    if result.returncode == 0:
        print("✅ Protobuf generation completed successfully!")
        print(f"Generated files in: {out_dir}")

        # Fix import paths in generated files
        _fix_import_paths(out_dir)
    else:
        print("❌ Protobuf generation failed")
        sys.exit(1)


def _fix_import_paths(out_dir: Path):
    """Fix import paths in generated files."""
    print("Fixing import paths...")

    # HACK: The protobuf compiler generates import statements that reference the original
    # proto package structure (orby.va.public.*), but since we're generating the Python
    # files into a different location (va/protos/), we need to rewrite these imports
    # to include the proper Python package prefix.
    # This is a temporary workaround until we have a better proto build system.

    for py_file in out_dir.rglob("*.py"):
        content = py_file.read_text()

        # Replace any import starting with "from orby.va.public" to include the va.protos prefix
        # This handles patterns like:
        # - from orby.va.public import something
        # - from orby.va.public.subpackage import something
        # - from orby.va.public.sub.package.etc import something
        content = content.replace(
            "from orby.va.public", "from va.protos.orby.va.public"
        )

        py_file.write_text(content)
        print(f"Fixed imports in {py_file}")


# Build hook for Hatchling
class ProtoBuildHook(BuildHookInterface):
    """Build hook that generates protobuf files before building."""

    PLUGIN_NAME = "proto_hook"

    def initialize(self, version, build_data):
        """Generate protos before building."""
        print("🔨 Build hook: Generating protobuf files...")
        try:
            generate_protos()
            print("✅ Build hook: Protobuf files generated successfully!")
        except Exception as e:
            print(f"❌ Build hook: Failed to generate protobuf files: {e}")
            raise


if __name__ == "__main__":
    generate_protos()
