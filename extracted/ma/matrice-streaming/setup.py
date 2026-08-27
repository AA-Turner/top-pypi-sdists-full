"""
Mypyc-compiled build configuration for matrice_streaming.

This setup.py can build in two modes:
- With mypyc: Compiles Python to native extensions (faster, platform-specific wheels)
- Without mypyc: Pure Python package (cross-platform, slower)

Set ENABLE_MYPYC=true environment variable to enable mypyc compilation.
"""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

# Package configuration
PACKAGE_NAME = "matrice_streaming"
SOURCE_DIR = f"src/{PACKAGE_NAME}"

# Modules left as pure Python (NOT mypyc-compiled). Entries are matched by file
# name during discovery. The generated .pyi stubs of these modules are also
# stripped before the compiled build so that importing (compiled) modules
# type-check against the real .py source rather than the lossy stub.
MYPYC_EXCLUDE_MODULES = {
    "nvdec.py",  # ctypes/mmap POSIX shared-memory pointer work -> segfaults compiled
    "streaming_gateway.py",  # unannotated @property active_worker_manager -> mypyc codegen abort
    "streaming_gateway_utils.py",  # class ConnectionAuthError(RuntimeError) -> mypyc cannot inherit builtins
    "frame_pool.py",  # class PoolExhaustedError(RuntimeError) -> mypyc cannot inherit builtins
    "constants.py",  # GatewayStatus(str, Enum) str-mixin enum -> emits undeclared C statics
    "orin_nvdec.py",  # @dataclass field typed threading.Lock -> KeyError: 'Lock' at import
    # The five below violate their own declared/inferred types in ways pure
    # Python tolerates but a native class/function does not (mypyc enforces
    # attribute, parameter and return types at runtime -> TypeError). They are
    # flagged by `mypy --check-untyped-defs` once the existing `# type: ignore`
    # comments are stripped; fixing them means changing product types, so they
    # stay interpreted.
    "manager.py",  # self.last_report_time inferred int, assigned time.time() float -> TypeError
    "collector.py",  # returns None from methods declared -> Dict[str, Any] -> TypeError
    "dynamic_camera_manager.py",  # passes Optional into _resolve_camera_host(camera_id: str) -> TypeError
    "async_camera_worker.py",  # avg_encoding_ms inferred int, reassigned float -> TypeError
    "video_capture_manager.py",  # open_capture() falls through declared -> Tuple[...] return -> TypeError
}


# Check if mypyc compilation is enabled.
# Falls back to build-config.json if env var is not set.
def _resolve_enable_mypyc() -> bool:
    env_val = os.environ.get("ENABLE_MYPYC")
    if env_val is not None:
        return env_val.lower() in ("true", "1", "yes")
    config_path = Path(__file__).parent / "build-config.json"
    if config_path.exists():
        import json

        try:
            with open(config_path) as f:
                config = json.load(f)
            return bool(config.get("build", {}).get("enable_mypyc", False))
        except (OSError, ValueError) as exc:
            print(f"Warning: failed to read build-config.json: {exc}")
    return False


ENABLE_MYPYC = _resolve_enable_mypyc()


# Patch level for a local/manual build. CI never reads this — the central
# py-release-channel-build.yml computes the version from git tags + the index
# and passes it in via PACKAGE_VERSION, which still wins here.
DEFAULT_VERSION = "1.1.1"


def get_version() -> str:
    """Get version from PACKAGE_VERSION environment variable."""
    version = os.environ.get("PACKAGE_VERSION", DEFAULT_VERSION)
    print(f"Building version: {version}")
    return version


def ensure_py_typed():
    """Create py.typed marker file for PEP 561 compliance."""
    py_typed = Path(SOURCE_DIR) / "py.typed"
    if not py_typed.exists():
        py_typed.write_text("")
        print("Created py.typed file")


def run_stub_generator():
    """Run stub generator script to create .pyi files."""
    script_path = Path(__file__).parent / "stub_generation.py"
    if not script_path.exists():
        print(f"Warning: Stub generator not found: {script_path}")
        return

    print(f"Running stub generator: {script_path}")
    subprocess.run(  # nosec B603 - invokes trusted local script with fixed args
        [sys.executable, str(script_path)], check=True
    )


def discover_modules() -> "list[str]":
    """Discover Python modules for mypyc compilation."""
    src_root = Path(SOURCE_DIR)
    if not src_root.exists():
        return []

    exclude = {"__pycache__", "tests", "test", "docs"}
    modules = []

    for path in src_root.rglob("*.py"):
        if any(part in exclude for part in path.parts):
            continue
        # Leave package __init__.py files as pure Python. They are thin
        # re-export shims, and compiling them makes mypyc resolve their
        # relative imports against the wrong package, breaking import at
        # runtime. matrice_streaming/__init__.py additionally uses a PEP-562
        # module-level __getattr__ for lazy imports, which a native module
        # cannot express. The compiled leaf submodules are imported by these
        # shims normally.
        if path.name == "__init__.py":
            continue
        if path.name in MYPYC_EXCLUDE_MODULES:
            continue
        modules.append(str(path).replace("\\", "/"))

    print(f"Discovered {len(modules)} Python files for mypyc compilation")
    return modules


def get_ext_modules():
    """Get extension modules - mypyc compiled or empty for pure Python."""
    if not ENABLE_MYPYC:
        print("Building PURE PYTHON package (mypyc disabled)")
        return []

    print("Building MYPYC COMPILED package")
    try:
        from mypyc.build import mypycify
    except ImportError as exc:  # pragma: no cover - build env without mypy
        print(f"Warning: mypyc unavailable ({exc}); falling back to pure Python")
        return []

    # Strip the auto-generated .pyi stubs of the pure (excluded) modules. The
    # generator emits lossy stubs (dropping kwargs/attributes); if left in
    # place, the compiled modules that import these excluded ones type-check
    # against the lossy stub and fail. Removing them makes mypy resolve those
    # imports against the real .py source instead.
    # The same applies to every __init__.pyi: package __init__.py files are
    # never compiled (see discover_modules), and the generator's "flat" package
    # stub for matrice_streaming/__init__.pyi is not even valid syntax (it emits
    # docstrings after `...` bodies). Strip them so mypy reads the real
    # __init__.py instead.
    _excluded_stems = {Path(m).stem for m in MYPYC_EXCLUDE_MODULES}
    for stub_path in Path(SOURCE_DIR).rglob("*.pyi"):
        if stub_path.name == "__init__.pyi" or stub_path.stem in _excluded_stems:
            stub_path.unlink()
            print(f"Stripped lossy stub for excluded module: {stub_path}")

    # Dedicated type-checking config: keeps third-party packages opaque so the
    # build only checks our own modules.
    config_path = Path(__file__).parent / "typecheck.ini"
    mypyc_options = [
        f"--config-file={config_path}",
    ]
    return mypycify(mypyc_options + discover_modules(), opt_level="3")


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    # Only ship the matrice_streaming package; exclude any orphan top-level
    # packages or template scaffolding that may exist under src/.
    packages=find_packages(where="src", include=[PACKAGE_NAME, f"{PACKAGE_NAME}.*"]),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    ext_modules=get_ext_modules(),
    zip_safe=False,
    python_requires=">=3.8",
)
