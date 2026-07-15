"""
Mypyc-compiled build configuration for matrice.

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
PACKAGE_NAME = "matrice"
SOURCE_DIR = f"src/{PACKAGE_NAME}"

# Modules left as pure Python (NOT mypyc-compiled). These do native
# C-interop (torch / torchvision / scikit-learn / pycocotools C extensions)
# whose native-compiled form segfaults at runtime; mypyc gives no benefit on
# this heavy-numeric / I/O-bound code anyway. Their generated .pyi stubs are
# also stripped before the compiled build so that importing (compiled) modules
# type-check against the real .py source.
MYPYC_EXCLUDE_MODULES = {
    # Uses an in-class `@staticmethod` (`log_decorator`) as a decorator on
    # later methods in the SAME class body. Pure Python resolves the bare
    # name from the class namespace during class-body execution; mypyc does
    # not, so the compiled module raises `KeyError: 'log_decorator'` at
    # import. (Also does pycocotools C-extension interop.) Kept pure Python.
    "testing.py",
    # References the module global `__file__` at TOP LEVEL (module-body
    # execution) for a vestigial `sys.path.append`. mypyc does not populate
    # `__file__` in the module dict during class/module-body execution, so the
    # compiled module raises `KeyError: '__file__'` at import. (Functions that
    # use `__file__` at call time are fine; only unconditional top-level use
    # breaks.) Kept pure Python.
    "streaming_benchmarking.py",
    # Defines `_dotdict(dict)`, a dict subclass that aliases
    # `__getattr__/__setattr__/__delattr__` to dict item methods for
    # dot-notation access. mypyc compiles this to a native class that does not
    # honour those dunder aliases, so `d.key` (the whole point of the class,
    # and how `get_job_params()` results are consumed by users) raises
    # AttributeError at runtime. `_dotdict` is public via both
    # `matrice.action_tracker` and the `matrice.actionTracker` shim, so the
    # module is kept pure Python to preserve behaviour.
    "action_tracker.py",
    # The following modules wrap `matrice_common.handle_response`, whose
    # `data` element is NOT always a dict -- several endpoints return a bare
    # string (e.g. application.request_publish_model_family documents
    # `data = "Model Family Publication Requested "`). Their public functions
    # nonetheless annotate the result as `tuple[dict | None, str | None, str]`
    # / `Tuple[Optional[Dict], Optional[str], str]`. Pure Python ignores the
    # annotation; mypyc ENFORCES it at the return boundary and raises
    # `TypeError: tuple[union[dict, None], ...] object expected; got
    # tuple[str, None, str]` on those real responses -- and callers that wrap
    # the call in `except Exception` (e.g.
    # streaming_automation.create_streaming_gateway) silently swallow it and
    # return None. Correcting the annotations is a product change, out of
    # scope here, so these stay pure Python.
    "application.py",
    "camera_management.py",
    "checkpoint.py",
    "inference_pipeline_management.py",
    "streaming_automation.py",
    "streaming_gateway_management.py",
    # `AppIntegrator.application` is annotated with the native class
    # `matrice.application.Application`. Compiled, that attribute becomes a
    # type-checked slot: assigning any other type raises TypeError -- and
    # mypyc's error path for that rejected assignment corrupts refcounts, so
    # the process SEGFAULTS at the next garbage collection (reproducible with
    # a plain `integrator.application = <wrong type>` + `gc.collect()`). A
    # hard interpreter crash on a would-be TypeError is not shippable.
    "app_integration.py",
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
        except Exception:
            pass
    return False


ENABLE_MYPYC = _resolve_enable_mypyc()


def get_version() -> str:
    """Get version from PACKAGE_VERSION environment variable."""
    version = os.environ.get("PACKAGE_VERSION", "0.0.0.dev0")
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
    subprocess.run([sys.executable, str(script_path)], check=True)


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
        if path.name == "__init__.py":
            # Compiling package __init__ modules breaks relative-import
            # resolution at runtime; keep them pure Python.
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

        # Strip the auto-generated .pyi stubs of the pure (excluded) modules.
        # The generator emits lossy stubs (dropping kwargs/attributes); if left
        # in place, the compiled modules that import these excluded ones
        # type-check against the lossy stub and fail. Removing them makes mypy
        # resolve those imports against the real .py source instead.
        _excluded_stems = {Path(m).stem for m in MYPYC_EXCLUDE_MODULES}
        for stub_path in Path(SOURCE_DIR).rglob("*.pyi"):
            if stub_path.stem in _excluded_stems:
                stub_path.unlink()
                print(f"Stripped lossy stub for excluded module: {stub_path}")

        # Dedicated type-checking config: keeps third-party packages opaque so
        # the build only checks our own modules.
        config_path = Path(__file__).parent / "typecheck.ini"
        mypyc_options = [
            f"--config-file={config_path}",
        ]
        return mypycify(mypyc_options + discover_modules(), opt_level="3")
    except Exception as exc:  # pragma: no cover - build-environment dependent
        # Never hard-fail the build on a mypyc problem (missing mypy in the
        # build env, codegen abort, toolchain issue). Fall back to shipping the
        # pure-Python package, which is always functionally correct.
        print(f"WARNING: mypyc compilation unavailable ({exc!r}); falling back to PURE PYTHON")
        return []


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    package_data={
        PACKAGE_NAME: ["py.typed", "*.pyi", "**/*.pyi"],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    ext_modules=get_ext_modules(),
    zip_safe=False,
    python_requires=">=3.8",
)
