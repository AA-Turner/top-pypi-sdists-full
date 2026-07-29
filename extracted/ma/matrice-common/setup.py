"""
Mypyc-compiled build configuration for matrice_common.

This setup.py can build in two modes:
- With mypyc: Compiles Python to native extensions (faster, platform-specific wheels)
- Without mypyc: Pure Python package (cross-platform, slower)

Set ENABLE_MYPYC=true environment variable to enable mypyc compilation.
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

# Package configuration
PACKAGE_NAME = "matrice_common"
SOURCE_DIR = f"src/{PACKAGE_NAME}"

# Modules left as pure Python (NOT mypyc-compiled). These do low-level
# CUDA-IPC / shared-memory / ctypes pointer work whose native-compiled form
# segfaults at runtime; mypyc gives no benefit on this I/O-bound code anyway.
# Their generated .pyi stubs are also stripped before the compiled build so
# that importing (compiled) modules type-check against the real .py source.
MYPYC_EXCLUDE_MODULES = {
    "cuda_shm_ring_buffer.py",  # CUDA IPC handles via ctypes -> segfaults compiled
    "shm_ring_buffer.py",  # POSIX shared-memory pointer work (same class of issue)
    "kafka_stream.py",  # confluent-kafka/aiokafka C-extension interop -> segfaults compiled
    # MetricsReporterMixin lives here and is subclassed by KafkaUtils /
    # AsyncKafkaUtils in the (pure) kafka_stream.py above. A compiled native
    # class cannot be a base of an interpreted class -- "TypeError: interpreted
    # classes cannot inherit from compiled" at import/instantiation -- so the
    # mixin's module must stay pure too. It is also the public base class that
    # downstream SDKs subclass.
    "_stream_helpers.py",
    # The redis clients are created with decode_responses=False, so redis-py
    # hands back *bytes* where several helpers/returns are annotated `str`.
    # Pure Python shrugs; compiled code enforces the annotation and raises
    # "TypeError: str or None object expected; got bytes" on the real read
    # path. Same for the deliberately-loose _safe_decode(Union[str, bytes]).
    "redis_stream.py",
    # extract_service_from_path(path: str) guards with `not isinstance(path,
    # str)` -- i.e. it is documented to accept non-str -- but compiled code
    # rejects that before the guard runs. Raising a TypeError from inside the
    # error-formatting path is exactly where robustness matters most.
    "errors.py",
    # _loads(data: bytes) explicitly supports str too (`data if isinstance(
    # data, str) else data.decode()`); compiled enforcement rejects the str.
    "databus_status.py",
    # MatriceStream.add_message is annotated `-> Optional[int]` but on the redis
    # path it returns RedisUtils.add_message()'s *str* stream id ("1234-0").
    # Pure Python never notices; compiled code raises "TypeError: int or None
    # object expected; got str" against a real redis. (The annotation is the
    # bug, but fixing types here is out of scope for the packaging change.)
    "matrice_stream.py",
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
    logger.info("Building version: %s", version)
    return version


def ensure_py_typed():
    """Create py.typed marker file for PEP 561 compliance."""
    py_typed = Path(SOURCE_DIR) / "py.typed"
    if not py_typed.exists():
        py_typed.write_text("")
        logger.info("Created py.typed file")


def run_stub_generator():
    """Run stub generator script to create .pyi files."""
    script_path = Path(__file__).parent / "stub_generation.py"
    if not script_path.exists():
        logger.warning("Stub generator not found: %s", script_path)
        return

    logger.info("Running stub generator: %s", script_path)
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
        # Leave package __init__.py files as pure Python. They are thin
        # re-export shims, and compiling them makes mypyc resolve their
        # relative imports against the wrong package, breaking import at
        # runtime. The compiled leaf submodules are imported by these
        # shims normally.
        if path.name == "__init__.py":
            continue
        if path.name in MYPYC_EXCLUDE_MODULES:
            continue
        modules.append(str(path).replace("\\", "/"))

    logger.info("Discovered %s Python files for mypyc compilation", len(modules))
    return modules


def get_ext_modules():
    """Get extension modules - mypyc compiled or empty for pure Python."""
    if not ENABLE_MYPYC:
        logger.info("Building PURE PYTHON package (mypyc disabled)")
        return []

    logger.info("Building MYPYC COMPILED package")
    try:
        from mypyc.build import mypycify

        # Strip the auto-generated .pyi stubs of the pure (excluded) modules. The
        # generator emits lossy stubs (dropping kwargs/attributes); if left in
        # place, the compiled modules that import these excluded ones type-check
        # against the lossy stub and fail. Removing them makes mypy resolve those
        # imports against the real .py source instead.
        # The same applies to every package __init__.pyi: __init__.py is never
        # compiled (see discover_modules), and its generated stub flattens all
        # re-exported names into one namespace, which does not type-check.
        _excluded_stems = {Path(m).stem for m in MYPYC_EXCLUDE_MODULES}
        for stub_path in Path(SOURCE_DIR).rglob("*.pyi"):
            if stub_path.stem in _excluded_stems or stub_path.name == "__init__.pyi":
                stub_path.unlink()
                logger.info("Stripped lossy stub for pure module: %s", stub_path)

        # Dedicated type-checking config: keeps third-party packages opaque so the
        # build only checks our own modules.
        config_path = Path(__file__).parent / "typecheck.ini"
        mypyc_options = [
            f"--config-file={config_path}",
        ]
        return mypycify(mypyc_options + discover_modules(), opt_level="3")
    # SystemExit is included on purpose: mypyc calls sys.exit() when its
    # type-check/codegen step fails, so a bare `except Exception` would not
    # catch it.
    except (Exception, SystemExit):  # pragma: no cover - build-time fallback
        # Degrade to a pure-Python wheel rather than hard-failing the build:
        # a missing mypy, an unsupported toolchain, or a codegen abort must not
        # break packaging. The pure wheel is functionally identical, just slower.
        logger.exception("mypyc compilation failed; falling back to a PURE PYTHON package")
        return []


# Build preparation
ensure_py_typed()
run_stub_generator()

# Setup
setup(
    name=PACKAGE_NAME,
    version=get_version(),
    package_dir={"": "src"},
    # Only ship the matrice_common package; exclude any orphan top-level
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
