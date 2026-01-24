"""
CSSL Compiler Configuration - Special handling for CSSL C++ acceleration.

CSSL is a special case in IncludeCPP:
- Pre-built modules are bundled in the PyPI package for instant use
- If bundled module doesn't match user's platform, it rebuilds ONCE
- Global compiler/platform info stored in %AppData%/IncludeCPP/general.json
- IncludeCPP works normally for everything else

This module handles:
- Global compiler detection and caching
- Platform detection for module matching
- Auto-rebuild to bundled folder if needed
"""

import os
import sys
import json
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List


# =============================================================================
# Global IncludeCPP Config (shared across all projects)
# =============================================================================

def get_includecpp_config_dir() -> Path:
    """
    Get global IncludeCPP config directory.

    Returns:
        Windows: %APPDATA%/IncludeCPP/
        Linux/macOS: ~/.config/IncludeCPP/
    """
    if sys.platform == 'win32':
        base = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
    else:
        base = Path.home() / '.config'

    config_dir = base / 'IncludeCPP'
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_global_config_path() -> Path:
    """Get path to global IncludeCPP config file."""
    return get_includecpp_config_dir() / 'general.json'


def get_cssl_bundled_dir() -> Path:
    """
    Get the bundled output directory for CSSL modules.
    This is inside the PyPI package so users get pre-built modules.

    Returns:
        Path to includecpp/core/cssl/cpp/build/
    """
    cssl_dir = Path(__file__).parent
    build_dir = cssl_dir / 'cpp' / 'build'
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir


# Legacy function for compatibility
def get_cssl_config_dir() -> Path:
    """Legacy: Get CSSL config directory. Now uses global config."""
    return get_includecpp_config_dir()


def get_cssl_config_path() -> Path:
    """Legacy: Get CSSL config path. Now uses global config."""
    return get_global_config_path()


def get_cssl_build_dir() -> Path:
    """
    Get build directory for CSSL modules.
    CSSL is special: builds go to the PyPI bundled folder.
    """
    return get_cssl_bundled_dir()


# =============================================================================
# Global Config Manager
# =============================================================================

class GlobalConfig:
    """
    Global IncludeCPP configuration.

    Stores compiler, platform info in %AppData%/IncludeCPP/general.json
    Shared across all IncludeCPP projects.
    """

    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GlobalConfig._config is None:
            self.config_path = get_global_config_path()
            GlobalConfig._config = self._load_config()

    @property
    def config(self) -> Dict[str, Any]:
        return GlobalConfig._config

    @config.setter
    def config(self, value: Dict[str, Any]):
        GlobalConfig._config = value

    def _load_config(self) -> Dict[str, Any]:
        """Load config from file, or return empty dict if not exists."""
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text(encoding='utf-8'))
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    def _save_config(self):
        """Save config to file."""
        try:
            self.config_path.write_text(
                json.dumps(self.config, indent=2),
                encoding='utf-8'
            )
        except OSError:
            pass

    def detect_compiler(self) -> Optional[str]:
        """
        Detect available C++ compiler.
        Checks: g++, clang++, cl (MSVC on Windows)
        """
        compilers = ['g++', 'clang++']
        if sys.platform == 'win32':
            compilers.append('cl')

        for compiler in compilers:
            if shutil.which(compiler):
                try:
                    result = subprocess.run(
                        [compiler, '--version'],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return compiler
                except (subprocess.SubprocessError, OSError):
                    continue
        return None

    def detect_compiler_version(self, compiler: str) -> Optional[str]:
        """Get compiler version string."""
        try:
            result = subprocess.run(
                [compiler, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.split('\n')[0].strip()
        except (subprocess.SubprocessError, OSError):
            pass
        return None

    def detect_platform(self) -> Dict[str, str]:
        """Detect platform info for module matching."""
        return {
            'system': platform.system(),
            'machine': platform.machine(),
            'python_version': f"{sys.version_info.major}{sys.version_info.minor}",
            'python_full_version': platform.python_version(),
            'platform': sys.platform,
        }

    def get_module_suffix(self) -> str:
        """Get expected module suffix for current platform."""
        info = self.detect_platform()
        py_ver = info['python_version']

        if info['platform'] == 'win32':
            return f".cp{py_ver}-win_amd64.pyd"
        elif info['platform'] == 'linux':
            return f".cpython-{py_ver}-x86_64-linux-gnu.so"
        elif info['platform'] == 'darwin':
            arch = 'arm64' if info['machine'] == 'arm64' else 'x86_64'
            return f".cpython-{py_ver}-{arch}-darwin.so"
        return ".pyd" if info['platform'] == 'win32' else ".so"

    def setup(self) -> Dict[str, Any]:
        """
        First-run setup - detect and store compiler/platform info.
        Called automatically on first import.
        """
        if self.config.get('initialized'):
            return self.config

        compiler = self.detect_compiler()
        compiler_version = self.detect_compiler_version(compiler) if compiler else None
        platform_info = self.detect_platform()

        self.config = {
            'initialized': True,
            'compiler': compiler,
            'compiler_version': compiler_version,
            'platform': platform_info,
            'module_suffix': self.get_module_suffix(),
            'can_compile': compiler is not None,
        }

        self._save_config()
        return self.config

    def refresh(self) -> Dict[str, Any]:
        """Force refresh of compiler/platform detection."""
        self.config['initialized'] = False
        return self.setup()


# =============================================================================
# CSSL-Specific Compiler Config (wraps GlobalConfig)
# =============================================================================

class CSSLCompilerConfig:
    """
    CSSL-specific compiler configuration.

    CSSL is special:
    - Uses global config from %AppData%/IncludeCPP/general.json
    - Builds output to PyPI bundled folder (includecpp/core/cssl/cpp/build/)
    - Auto-rebuilds if bundled module doesn't match platform
    """

    def __init__(self):
        self.global_config = GlobalConfig()
        self.config_path = get_global_config_path()

    @property
    def config(self) -> Dict[str, Any]:
        return self.global_config.config

    def _load_config(self) -> Dict[str, Any]:
        return self.global_config._load_config()

    def _save_config(self):
        self.global_config._save_config()

    def detect_compiler(self) -> Optional[str]:
        return self.global_config.detect_compiler()

    def detect_compiler_version(self, compiler: str) -> Optional[str]:
        return self.global_config.detect_compiler_version(compiler)

    def detect_platform(self) -> Dict[str, str]:
        return self.global_config.detect_platform()

    def get_prebuilt_suffix(self) -> str:
        return self.global_config.get_module_suffix()

    def get_all_possible_suffixes(self) -> List[str]:
        """Get all possible module suffixes for current platform."""
        info = self.detect_platform()
        py_ver = info['python_version']

        suffixes = [self.get_prebuilt_suffix()]

        if info['platform'] == 'win32':
            suffixes.extend(['.pyd', f'.cp{py_ver}-win32.pyd'])
        elif info['platform'] == 'linux':
            suffixes.extend(['.so', f'.cpython-{py_ver}-linux-gnu.so'])
        elif info['platform'] == 'darwin':
            suffixes.extend(['.so', '.dylib'])

        return suffixes

    def setup_first_run(self) -> Dict[str, Any]:
        """Setup global config on first run."""
        return self.global_config.setup()

    def refresh(self) -> Dict[str, Any]:
        """Force refresh of config."""
        return self.global_config.refresh()

    def can_compile(self) -> bool:
        """Check if compilation is possible."""
        if not self.config.get('initialized'):
            self.setup_first_run()
        return self.config.get('can_compile', False)

    def get_compiler(self) -> Optional[str]:
        """Get configured compiler."""
        if not self.config.get('initialized'):
            self.setup_first_run()
        return self.config.get('compiler')

    def get_platform_info(self) -> Dict[str, str]:
        """Get stored platform info."""
        if not self.config.get('initialized'):
            self.setup_first_run()
        return self.config.get('platform', self.detect_platform())

    def get_build_dir(self) -> Path:
        """Get CSSL build directory (bundled in PyPI folder)."""
        return get_cssl_bundled_dir()


# =============================================================================
# CSSL Module Compilation
# =============================================================================

def compile_cssl_core(force: bool = False) -> Optional[Path]:
    """
    Compile cssl_core module to the bundled PyPI folder.

    CSSL builds go directly to includecpp/core/cssl/cpp/build/
    so they're bundled with the package for other users.

    Args:
        force: If True, rebuild even if module exists

    Returns:
        Path to compiled module, or None if failed
    """
    config = CSSLCompilerConfig()
    config.setup_first_run()

    if not config.can_compile():
        return None

    # Output to bundled folder
    build_dir = get_cssl_bundled_dir()
    suffix = config.get_prebuilt_suffix()
    output_path = build_dir / f'cssl_core{suffix}'

    # Check if already built
    if output_path.exists() and not force:
        return output_path

    # Get source directory
    cssl_dir = Path(__file__).parent
    cpp_dir = cssl_dir / 'cpp'

    if not (cpp_dir / 'cpp.proj').exists():
        return None

    # Build using includecpp with output to bundled folder
    try:
        # IncludeCPP builds to AppData by default, so we build then copy
        result = subprocess.run(
            [sys.executable, '-m', 'includecpp', 'rebuild', '--clean'],
            cwd=cpp_dir,
            capture_output=True,
            text=True,
            timeout=300
        )

        if result.returncode == 0:
            # Find built module and copy to bundled folder
            if sys.platform == 'win32':
                appdata = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming'))
            else:
                appdata = Path.home() / '.local' / 'share'
            icpp_build = appdata / 'cssl_core-g-build-proj' / 'bindings'

            # Copy api.pyd to bundled folder
            api_path = icpp_build / 'api.pyd'
            if not api_path.exists():
                api_path = icpp_build / 'api.so'

            if api_path.exists():
                # Copy as api.pyd (IncludeCPP format)
                dest = build_dir / api_path.name
                shutil.copy2(api_path, dest)

                # Also copy as cssl_core.{suffix} for direct loading
                shutil.copy2(api_path, output_path)
                return output_path

    except (subprocess.SubprocessError, OSError):
        pass

    return None


def get_cssl_core_path() -> Optional[Path]:
    """
    Get path to cssl_core module.

    CSSL special handling:
    1. Check bundled folder in PyPI package
    2. If not found and can compile, rebuild to bundled folder

    Returns:
        Path to module, or None if not found
    """
    config = CSSLCompilerConfig()
    config.setup_first_run()

    suffixes = config.get_all_possible_suffixes()
    build_dir = get_cssl_bundled_dir()

    # Check for cssl_core.{suffix}
    for suffix in suffixes:
        module_path = build_dir / f'cssl_core{suffix}'
        if module_path.exists():
            return module_path

    # Check for api.pyd (IncludeCPP format)
    api_path = build_dir / 'api.pyd'
    if not api_path.exists():
        api_path = build_dir / 'api.so'
    if api_path.exists():
        return api_path

    return None


def ensure_cssl_module() -> Optional[Path]:
    """
    Ensure CSSL C++ module is available.

    If bundled module doesn't exist or doesn't match platform,
    automatically rebuild to the bundled folder (ONCE).

    Returns:
        Path to module, or None if unavailable
    """
    # Check if bundled module exists
    module_path = get_cssl_core_path()
    if module_path:
        return module_path

    # No bundled module - try to compile
    config = CSSLCompilerConfig()
    config.setup_first_run()

    if config.can_compile():
        # Rebuild to bundled folder
        return compile_cssl_core(force=True)

    return None
