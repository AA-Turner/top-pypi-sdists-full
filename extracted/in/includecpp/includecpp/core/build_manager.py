import sys
import os
import subprocess
import hashlib
import shutil
import json
import platform
from pathlib import Path
from typing import List, Optional, Dict, Any

from .exceptions import CppBuildError, CppValidationError

class BuildManager:
    # Class-level cache for MSYS2 environment
    _msys2_env_cache = None

    def __init__(self, project_root: Path, build_dir: Path, config):
        """Initialize BuildManager for PyPI-installed package.

        Args:
            project_root: User's project directory (with cpp.proj)
            build_dir: AppData build directory
            config: CppProjectConfig instance
        """
        self.project_root = project_root
        self.build_dir = build_dir
        self.config = config

        self.plugins_dir = config.plugins_dir
        self.include_dir = config.include_dir

        self.bin_dir = build_dir / "bin" / ".appc"
        self.bindings_dir = build_dir / "bindings"
        self.cmake_build_dir = build_dir / "build"

        self.gen_exe = self.bin_dir / self._get_exe_name("plugin_gen")
        self.registry_file = build_dir / ".module_registry.json"

        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.bindings_dir.mkdir(parents=True, exist_ok=True)
        self.cmake_build_dir.mkdir(parents=True, exist_ok=True)

    def _get_exe_name(self, base_name: str) -> str:
        """Get platform-specific executable name."""
        if platform.system() == "Windows":
            return f"{base_name}.exe"
        return base_name

    def _compute_hash(self, filepath: Path) -> str:
        """Compute SHA256 hash of file (full 64-char digest for v2.3.5+)."""
        if not filepath.exists():
            return "0"
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception:
            return "0"

    def _compute_generator_hash(self, parser_cpp: Path, parser_h: Path) -> str:
        """Compute combined hash of generator source files."""
        hasher = hashlib.sha256()
        for filepath in [parser_cpp, parser_h]:
            if filepath.exists():
                try:
                    with open(filepath, 'rb') as f:
                        hasher.update(f.read())
                except Exception:
                    pass
        return hasher.hexdigest()

    def _get_generator_source(self) -> Path:
        """Get path to parser.cpp in installed package."""
        package_dir = Path(__file__).parent.parent
        parser_cpp = package_dir / "generator" / "parser.cpp"

        if not parser_cpp.exists():
            raise CppBuildError(
                f"Generator source not found: {parser_cpp}\n"
                "This is a package installation error."
            )

        return parser_cpp

    def _build_generator(self, verbose: bool = False):
        """Compile plugin_gen.exe from parser.cpp with hash checking."""
        parser_cpp = self._get_generator_source()
        parser_h = parser_cpp.with_suffix('.h')
        package_generator_dir = parser_cpp.parent

        # Check if rebuild needed via hash comparison
        gen_hash_file = self.bin_dir / ".generator_hash"
        if self.gen_exe.exists() and gen_hash_file.exists():
            try:
                stored_hash = gen_hash_file.read_text().strip()
                current_hash = self._compute_generator_hash(parser_cpp, parser_h)
                if stored_hash == current_hash:
                    if verbose:
                        print(f"Generator up-to-date: {self.gen_exe}")
                    return
                elif verbose:
                    print("Generator source changed, rebuilding...")
            except Exception:
                pass  # Hash check failed, rebuild anyway

        if self.gen_exe.exists():
            if verbose:
                print(f"Generator exists but needs rebuild")
        else:
            if verbose:
                print(f"Generator not found, building...")

        if verbose:
            print(f"Compiling generator from: {parser_cpp}")

        compiler = self._detect_cpp_compiler(verbose=verbose)

        if compiler == "g++":
            cmd = [
                "g++",
                "-std=c++17",
                "-O2",
                f"-I{package_generator_dir}",
                str(parser_cpp),
                "-o",
                str(self.gen_exe)
            ]
        elif compiler == "clang++":
            cmd = [
                "clang++",
                "-std=c++17",
                "-O2",
                f"-I{package_generator_dir}",
                str(parser_cpp),
                "-o",
                str(self.gen_exe)
            ]
        elif compiler == "cl":
            cmd = [
                "cl",
                "/std:c++17",
                "/O2",
                f"/I{package_generator_dir}",
                str(parser_cpp),
                f"/Fe:{self.gen_exe}"
            ]
        else:
            raise CppBuildError("No C++ compiler found (g++, clang++, or cl)")

        self._run_compiler_command(cmd, verbose=verbose)

        if not self.gen_exe.exists():
            raise CppBuildError(f"Generator executable not created: {self.gen_exe}")

        # Save hash for future comparisons
        try:
            current_hash = self._compute_generator_hash(parser_cpp, parser_h)
            gen_hash_file = self.bin_dir / ".generator_hash"
            gen_hash_file.write_text(current_hash)
        except Exception:
            pass  # Hash save failed, not critical

        if verbose:
            print(f"Generator compiled: {self.gen_exe}")

    def _get_msys2_env(self) -> dict:
        """Get MSYS2 MINGW64 environment variables for g++ on Windows.

        Uses class-level caching to avoid repeated os.environ.copy() calls.
        """
        if BuildManager._msys2_env_cache is not None:
            return BuildManager._msys2_env_cache

        env = os.environ.copy()
        if platform.system() == "Windows":
            # Set MSYS2 MINGW64 environment
            env["MINGW_PREFIX"] = "/mingw64"
            env["MSYSTEM"] = "MINGW64"
            env["PKG_CONFIG_PATH"] = "/mingw64/lib/pkgconfig:/mingw64/share/pkgconfig"

            # Prepend MSYS2 paths - check MSYS2_ROOT env var first, then default
            msys_root = os.environ.get("MSYS2_ROOT", "C:/msys64")
            msys_paths = [
                f"{msys_root}/mingw64/bin",
                f"{msys_root}/usr/local/bin",
                f"{msys_root}/usr/bin",
                f"{msys_root}/bin"
            ]
            existing_path = env.get("PATH", "")
            env["PATH"] = os.pathsep.join(msys_paths) + os.pathsep + existing_path

        BuildManager._msys2_env_cache = env
        return env

    def _run_compiler_command(self, cmd: list, verbose: bool = False, cwd: str = None):
        """Run compiler command with appropriate environment (MSYS2 on Windows)."""
        env = self._get_msys2_env()

        try:
            if verbose:
                print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, env=env, cwd=cwd)
            if verbose and result.stdout:
                print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            raise CppBuildError(
                f"Compilation failed:\nCommand: {' '.join(cmd)}\nStderr: {e.stderr}\nStdout: {e.stdout}"
            ) from e

    def _detect_cpp_compiler(self, verbose: bool = False) -> str:
        """Detect available C++ compiler with caching.

        Cache is stored in build_dir/.compiler_cache and cleared with --clean.
        """
        cache_file = self.build_dir / ".compiler_cache"

        # Check cache first
        if cache_file.exists():
            try:
                cached = cache_file.read_text().strip()
                if cached and shutil.which(cached):
                    if verbose:
                        print(f"  Using cached compiler: {cached}")
                    return cached
            except Exception:
                pass  # Cache read failed, detect fresh

        # Detect compiler
        if verbose:
            print("  Detecting C++ compiler...")
        for compiler in ['g++', 'clang++', 'cl']:
            if shutil.which(compiler):
                # Save to cache
                try:
                    cache_file.write_text(compiler)
                    if verbose:
                        print(f"  Found and cached: {compiler}")
                except Exception:
                    pass  # Cache write failed, not critical
                return compiler
        return None

    def _clear_compiler_cache(self):
        """Clear all build caches (called with --clean)."""
        # Clear compiler cache
        cache_file = self.build_dir / ".compiler_cache"
        if cache_file.exists():
            try:
                cache_file.unlink()
            except Exception:
                pass

        # Clear CMake generator cache
        generator_cache = self.build_dir / ".cmake_generator"
        if generator_cache.exists():
            try:
                generator_cache.unlink()
            except Exception:
                pass

        # Clear object cache
        obj_cache_dir = self.build_dir / "obj_cache"
        if obj_cache_dir.exists():
            try:
                shutil.rmtree(obj_cache_dir)
            except Exception:
                pass

    def _scan_plugins(self, verbose: bool = False) -> List[Path]:
        """Scan user's plugins directory for .cp files."""
        if not self.plugins_dir.exists():
            raise CppBuildError(
                f"Plugins directory not found: {self.plugins_dir}\n"
                f"Create it with: mkdir {self.plugins_dir}"
            )

        cp_files = list(self.plugins_dir.glob("*.cp"))

        if not cp_files:
            raise CppBuildError(
                f"No .cp files found in {self.plugins_dir}\n"
                "Create plugin definitions first."
            )

        if verbose:
            print(f"Found {len(cp_files)} user plugin(s): {[f.name for f in cp_files]}")

        return cp_files

    def _generate_bindings(self, verbose: bool = False):
        """Run plugin_gen.exe to generate bindings.cpp for user plugins."""

        # Scan user plugins
        user_plugins = self._scan_plugins(verbose)

        if len(user_plugins) == 0:
            raise CppBuildError("No plugins found in plugins directory")

        bindings_cpp = self.bindings_dir / "bindings.cpp"
        sources_txt = self.bindings_dir / "sources.txt"

        # Run generator on plugins directory
        cmd = [
            str(self.gen_exe),
            str(self.plugins_dir),
            str(bindings_cpp),
            str(sources_txt),
            str(self.registry_file)
        ]

        try:
            if verbose:
                print(f"Running generator on {len(user_plugins)} plugin(s)...")
                print(f"  Plugins dir: {self.plugins_dir}")
                print(f"  Bindings output: {bindings_cpp}")

            # Important: Run from project_root so relative paths in .cp files work
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, cwd=str(self.project_root))

            # ALWAYS print stdout/stderr in verbose mode, even on success
            if verbose:
                if result.stdout:
                    print("Generator stdout:")
                    print(result.stdout)
                if result.stderr:
                    print("Generator stderr:")
                    print(result.stderr)

        except subprocess.CalledProcessError as e:
            error_msg = f"Plugin generation failed (exit code {e.returncode}):\n"
            error_msg += f"Command: {' '.join(cmd)}\n"
            if e.stdout:
                error_msg += f"Stdout:\n{e.stdout}\n"
            if e.stderr:
                error_msg += f"Stderr:\n{e.stderr}\n"
            raise CppBuildError(error_msg) from e

        # Verify outputs were created
        if not bindings_cpp.exists():
            error_msg = f"bindings.cpp not generated: {bindings_cpp}\n"
            error_msg += f"Plugin generator ran successfully but did not create output file.\n"
            error_msg += f"This usually means no .cp files were found or parsed successfully.\n"
            error_msg += f"Total plugins: {len(user_plugins)}"
            raise CppBuildError(error_msg)

        if verbose:
            print(f"Generated: {bindings_cpp}")
            print(f"Generated: {sources_txt}")
            print(f"Generated: {self.registry_file}")

    def _generate_cmake(self, verbose: bool = False):
        """Generate CMakeLists.txt in build directory."""
        sources_txt = self.bindings_dir / "sources.txt"

        if not sources_txt.exists():
            raise CppBuildError(f"sources.txt not found: {sources_txt}")

        with open(sources_txt, encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip()]

        source_paths = []
        for src in sources:
            src_path = self.project_root / src
            if not src_path.exists():
                raise CppBuildError(f"Source file not found: {src_path}")
            source_paths.append(str(src_path))

        bindings_cpp = self.bindings_dir / "bindings.cpp"

        cmake_content = f'''cmake_minimum_required(VERSION 3.15)
project(includecpp_api VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(api
    "{bindings_cpp}"
{chr(10).join(f'    "{src}"' for src in source_paths)}
)

target_include_directories(api PRIVATE
    "{self.project_root}"
    "{self.include_dir}"
)

if(MSVC)
    # /wd4018: disable signed/unsigned comparison warning (pybind11 enum issue)
    target_compile_options(api PRIVATE /W3 /O2 /EHsc /MT /wd4018 /wd4267)
else()
    # -Wno-sign-compare: disable signed/unsigned comparison warning (pybind11 enum issue)
    target_compile_options(api PRIVATE -Wall -O3 -pthread -Wno-sign-compare)
    # MinGW on Windows: static linking for MinGW runtime and pthread
    if(WIN32)
        target_link_options(api PRIVATE -static-libgcc -static-libstdc++ -Wl,-Bstatic -lpthread -Wl,-Bdynamic -lws2_32)
    endif()
endif()
'''

        cmake_file = self.build_dir / "CMakeLists.txt"
        cmake_file.write_text(cmake_content)

        if verbose:
            print(f"Generated CMakeLists.txt with {len(source_paths)} source(s)")

    def _configure_cmake(self, verbose: bool = False):
        """Configure CMake build with generator caching."""
        generator_cache = self.build_dir / ".cmake_generator"
        if generator_cache.exists():
            cached = generator_cache.read_text().strip()
            if cached == "NONE":
                # No working generator found previously
                raise CppBuildError("CMake not available (cached). Use direct compilation.")
            if cached:
                # Try cached generator
                if verbose:
                    print(f"Using cached CMake generator: {cached}")
                try:
                    env = self._get_msys2_env()
                    cmd = ["cmake", "-B", str(self.cmake_build_dir), "-S", str(self.build_dir), "-G", cached]
                    subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, env=env)
                    if verbose:
                        print(f"CMake configured with {cached}")
                    return
                except subprocess.CalledProcessError:
                    # Cached generator no longer works, re-detect
                    generator_cache.unlink()
                    if verbose:
                        print(f"Cached generator failed, re-detecting...")

        generators = []
        if platform.system() == "Windows":
            generators = ["MinGW Makefiles", "Ninja", "Visual Studio 17 2022", "Visual Studio 16 2019"]
        else:
            generators = ["Unix Makefiles", "Ninja"]

        env = self._get_msys2_env()
        last_error = None

        for generator in generators:
            try:
                cmd = ["cmake", "-B", str(self.cmake_build_dir), "-S", str(self.build_dir), "-G", generator]
                if verbose:
                    print(f"Trying CMake generator: {generator}")

                subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, env=env)

                # Success - cache this generator
                generator_cache.write_text(generator)
                if verbose:
                    print(f"CMake configured with {generator} (cached)")
                return

            except subprocess.CalledProcessError as e:
                last_error = e
                if verbose:
                    print(f"Generator {generator} failed, trying next...")

                # Clean CMake cache before trying next generator
                cmake_cache = self.cmake_build_dir / "CMakeCache.txt"
                cmake_files = self.cmake_build_dir / "CMakeFiles"
                if cmake_cache.exists():
                    cmake_cache.unlink()
                if cmake_files.exists():
                    shutil.rmtree(cmake_files)

        # No generator worked - cache this result
        generator_cache.write_text("NONE")
        raise CppBuildError(
            f"CMake configuration failed with all generators.\n"
            f"Last error: {last_error.stderr if last_error else 'Unknown'}"
        ) from last_error

    def _compile_cpp(self, verbose: bool = False):
        """Compile C++ code with CMake."""
        # Use MSYS2 environment for proper g++/cmake operation
        env = self._get_msys2_env()

        cmd = [
            "cmake",
            "--build", str(self.cmake_build_dir),
            "--config", "Release"
        ]

        try:
            if verbose:
                print(f"Running: {' '.join(cmd)}")

            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', check=True, env=env)

            if verbose and result.stdout:
                print(result.stdout)

        except subprocess.CalledProcessError as e:
            raise CppBuildError(
                f"C++ compilation failed:\n{e.stderr}"
            ) from e

        if verbose:
            print("C++ compilation successful")

    def _compile_direct(self, verbose: bool = False):
        """Direct compilation with g++/clang++ without CMake (fallback)."""
        compiler = self._detect_cpp_compiler(verbose=verbose)
        if not compiler:
            raise CppBuildError("No C++ compiler found (g++, clang++, or cl)")

        # Get source files
        sources_txt = self.bindings_dir / "sources.txt"
        if not sources_txt.exists():
            raise CppBuildError(f"sources.txt not found: {sources_txt}")

        with open(sources_txt, encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip()]

        source_paths = [str(self.project_root / src) for src in sources]
        bindings_cpp = str(self.bindings_dir / "bindings.cpp")

        # Get Python include and lib paths
        python_include = subprocess.check_output(
            [sys.executable, "-c", "import sysconfig; print(sysconfig.get_path('include'))"],
            text=True, encoding='utf-8'
        ).strip()

        pybind11_include = subprocess.check_output(
            [sys.executable, "-c", "import pybind11; print(pybind11.get_include())"],
            text=True, encoding='utf-8'
        ).strip()

        # Output file
        output_file = str(self.bindings_dir / f"api{self._get_pyd_suffix()}")

        # Build command
        if compiler in ['g++', 'clang++']:
            cmd = [
                compiler,
                "-O3",
                "-Wall",
                "-shared",
                "-std=c++17",
                "-fPIC",
                f"-I{python_include}",
                f"-I{pybind11_include}",
                f"-I{self.project_root}",
                f"-I{self.include_dir}",
                bindings_cpp,
                *source_paths,
                "-o", output_file
            ]

            # Platform-specific flags
            if platform.system() == "Windows":
                # MinGW on Windows: Need to link Python library for symbols
                # Find Python libs directory
                python_libs_cmd = [sys.executable, "-c",
                    "import sysconfig; import os; "
                    "libdir = sysconfig.get_config_var('LIBDIR'); "
                    "prefix = sysconfig.get_config_var('prefix'); "
                    "print(libdir if libdir and os.path.exists(libdir) else os.path.join(prefix, 'libs'))"]
                python_libs_dir = subprocess.check_output(python_libs_cmd, text=True, encoding='utf-8').strip()

                # Get Python library name (e.g., python312)
                py_version = f"python{sys.version_info.major}{sys.version_info.minor}"

                cmd.extend([
                    "-static-libgcc",
                    "-static-libstdc++",
                    "-Wl,-Bstatic",
                    "-lpthread",
                    "-Wl,-Bdynamic",
                    "-lws2_32",
                    f"-L{python_libs_dir}",
                    f"-l{py_version}"
                ])
                if verbose:
                    print(f"Linking with {py_version} from {python_libs_dir}")
            else:
                # Linux/macOS
                cmd.append("-pthread")

        elif compiler == 'cl':  # MSVC
            cmd = [
                "cl",
                "/O2",
                "/EHsc",
                "/std:c++17",
                "/LD",  # Create DLL
                f"/I{python_include}",
                f"/I{pybind11_include}",
                f"/I{self.project_root}",
                f"/I{self.include_dir}",
                bindings_cpp,
                *source_paths,
                f"/Fe:{output_file}"
            ]
        else:
            raise CppBuildError(f"Unsupported compiler: {compiler}")

        if verbose:
            print(f"Direct compilation with {compiler}")
            print(f"Command: {' '.join(cmd)}")

        self._run_compiler_command(cmd, verbose=verbose, cwd=str(self.bindings_dir))

        if verbose:
            print(f"Module compiled: {output_file}")

        # Copy MinGW DLLs if on Windows (after direct compilation)
        self._copy_mingw_dlls(verbose=verbose)

    def _compile_direct_incremental(self, verbose: bool = False):
        """Incremental direct compilation - only recompile changed .o files."""
        compiler = self._detect_cpp_compiler(verbose=verbose)
        if not compiler:
            raise CppBuildError("No C++ compiler found (g++, clang++, or cl)")

        if compiler == 'cl':
            # MSVC doesn't support our incremental approach, fall back
            return self._compile_direct(verbose=verbose)

        # Create object cache directory
        obj_cache_dir = self.build_dir / "obj_cache"
        obj_cache_dir.mkdir(parents=True, exist_ok=True)

        # Get source files
        sources_txt = self.bindings_dir / "sources.txt"
        if not sources_txt.exists():
            raise CppBuildError(f"sources.txt not found: {sources_txt}")

        with open(sources_txt, encoding='utf-8') as f:
            sources = [line.strip() for line in f if line.strip()]

        source_paths = [self.project_root / src for src in sources]
        bindings_cpp = self.bindings_dir / "bindings.cpp"

        # Get includes
        python_include = subprocess.check_output(
            [sys.executable, "-c", "import sysconfig; print(sysconfig.get_path('include'))"],
            text=True, encoding='utf-8'
        ).strip()
        pybind11_include = subprocess.check_output(
            [sys.executable, "-c", "import pybind11; print(pybind11.get_include())"],
            text=True, encoding='utf-8'
        ).strip()

        include_flags = [
            f"-I{python_include}",
            f"-I{pybind11_include}",
            f"-I{self.project_root}",
            f"-I{self.include_dir}",
        ]

        # Compile each source to .o if needed
        objects_to_link = []
        recompiled = 0

        # Compile bindings.cpp
        bindings_obj = obj_cache_dir / "bindings.o"
        if not bindings_obj.exists() or bindings_cpp.stat().st_mtime > bindings_obj.stat().st_mtime:
            if verbose:
                print(f"  Compiling bindings.cpp...")
            cmd = [compiler, "-c", "-O3", "-std=c++17", "-fPIC", *include_flags,
                   str(bindings_cpp), "-o", str(bindings_obj)]
            self._run_compiler_command(cmd, verbose=verbose, cwd=str(self.bindings_dir))
            recompiled += 1
        objects_to_link.append(str(bindings_obj))

        # Compile source files
        for src_path in source_paths:
            if not src_path.exists():
                continue
            obj_file = obj_cache_dir / (src_path.stem + ".o")

            if not obj_file.exists() or src_path.stat().st_mtime > obj_file.stat().st_mtime:
                if verbose:
                    print(f"  Compiling {src_path.name}...")
                cmd = [compiler, "-c", "-O3", "-std=c++17", "-fPIC", *include_flags,
                       str(src_path), "-o", str(obj_file)]
                self._run_compiler_command(cmd, verbose=verbose, cwd=str(self.bindings_dir))
                recompiled += 1

            objects_to_link.append(str(obj_file))

        if verbose:
            print(f"  Recompiled {recompiled} file(s), linking...")

        # Link all .o files
        output_file = str(self.bindings_dir / f"api{self._get_pyd_suffix()}")
        link_cmd = [compiler, "-shared", "-o", output_file, *objects_to_link]

        # Platform-specific link flags
        if platform.system() == "Windows":
            python_libs_cmd = [sys.executable, "-c",
                "import sysconfig; import os; "
                "libdir = sysconfig.get_config_var('LIBDIR'); "
                "prefix = sysconfig.get_config_var('prefix'); "
                "print(libdir if libdir and os.path.exists(libdir) else os.path.join(prefix, 'libs'))"]
            python_libs_dir = subprocess.check_output(python_libs_cmd, text=True, encoding='utf-8').strip()
            py_version = f"python{sys.version_info.major}{sys.version_info.minor}"

            link_cmd.extend([
                "-static-libgcc", "-static-libstdc++",
                "-Wl,-Bstatic", "-lpthread", "-Wl,-Bdynamic",
                "-lws2_32", f"-L{python_libs_dir}", f"-l{py_version}"
            ])
        else:
            link_cmd.append("-pthread")

        self._run_compiler_command(link_cmd, verbose=verbose, cwd=str(self.bindings_dir))

        if verbose:
            print(f"Module compiled: {output_file}")

        self._copy_mingw_dlls(verbose=verbose)

    def _copy_mingw_dlls(self, verbose: bool = False):
        """Copy required MinGW DLLs to bindings directory on Windows."""
        if platform.system() != "Windows":
            return

        msys_root = os.environ.get("MSYS2_ROOT", "C:/msys64")
        msys_bin = Path(msys_root) / "mingw64" / "bin"
        if not msys_bin.exists():
            return

        required_dlls = ["libwinpthread-1.dll", "libgcc_s_seh-1.dll", "libstdc++-6.dll"]

        for dll_name in required_dlls:
            source = msys_bin / dll_name
            dest = self.bindings_dir / dll_name

            if source.exists() and not dest.exists():
                shutil.copy2(str(source), str(dest))
                if verbose:
                    print(f"Copied {dll_name} to bindings directory")

    def _generate_cpp_api_extensions(self, modules: Dict, verbose: bool = False):
        """Generate cpp_api_extensions.pyi in package directory for VSCode IntelliSense.

        This is the critical file that makes VSCode autocomplete work!
        It provides type hints for the ModuleWrapper class that show what
        attributes will be available for each module.
        """
        # Find package directory
        package_root = Path(__file__).parent.parent
        pyi_file = package_root / "core" / "cpp_api_extensions.pyi"

        with open(pyi_file, 'w', encoding='utf-8') as f:
            f.write('"""Auto-generated type stubs for IncludeCPP module wrappers.\n\n')
            f.write('This file enables VSCode IntelliSense autocomplete for C++ modules.\n')
            f.write('DO NOT EDIT - Auto-generated by IncludeCPP build system.\n')
            f.write('"""\n\n')
            f.write('from typing import Any, List, Dict, Optional, Union, Protocol, overload\n\n')

            # Generate a Protocol/class for each module's wrapper
            for module_name, module_info in modules.items():
                class_name = f"{module_name.capitalize()}ModuleWrapper"

                f.write(f'class {class_name}(Protocol):\n')
                f.write(f'    """Type hints for {module_name} module wrapper (VSCode autocomplete support)."""\n\n')

                # Add getInfo method (from ModuleWrapper base class)
                f.write('    def getInfo(self) -> Dict[str, Any]:\n')
                f.write(f'        """Get {module_name} module information."""\n')
                f.write('        ...\n\n')

                # Generate STRUCT types (v2.0+)
                structs = module_info.get('structs', [])
                for struct in structs:
                    struct_name = struct.get('name', '')
                    is_template = struct.get('is_template', False)
                    template_types = struct.get('template_types', [])
                    fields = struct.get('fields', [])
                    doc = struct.get('doc', '')

                    if is_template:
                        # Generate struct for each template type
                        for ttype in template_types:
                            full_name = f"{struct_name}_{ttype}"
                            self._write_struct_protocol(f, full_name, struct, ttype)
                    else:
                        # Non-template struct
                        self._write_struct_protocol(f, struct_name, struct, None)

                # Generate classes as nested class attributes
                classes = module_info.get('classes', [])
                for cls in classes:
                    class_name_inner = cls.get('name', '')
                    class_doc = cls.get('doc', '')

                    f.write(f'    class {class_name_inner}:\n')
                    if class_doc:
                        f.write(f'        """{class_doc}"""\n\n')
                    else:
                        f.write(f'        """C++ class: {class_name_inner}"""\n\n')

                    constructors = cls.get('constructors', [])
                    if constructors and len(constructors) > 1:
                        # Multiple constructors - use @overload
                        for ctor in constructors:
                            param_types = ctor.get('params', [])
                            f.write('        @overload\n')
                            if param_types:
                                param_list = ['self']
                                for i, ptype in enumerate(param_types):
                                    py_type = self._cpp_to_python_type(ptype)
                                    param_list.append(f'arg{i}: {py_type}')
                                params_str = ', '.join(param_list)
                                f.write(f'        def __init__({params_str}) -> None: ...\n')
                            else:
                                f.write(f'        def __init__(self) -> None: ...\n')
                        f.write('\n')
                        # Actual implementation signature
                        f.write('        def __init__(self, *args: Any, **kwargs: Any) -> None:\n')
                        f.write(f'            """Initialize {class_name_inner} instance"""\n')
                        f.write('            ...\n\n')
                    elif constructors and len(constructors) == 1:
                        # Single constructor
                        param_types = constructors[0].get('params', [])
                        if param_types:
                            param_list = ['self']
                            for i, ptype in enumerate(param_types):
                                py_type = self._cpp_to_python_type(ptype)
                                param_list.append(f'arg{i}: {py_type}')
                            params_str = ', '.join(param_list)
                            f.write(f'        def __init__({params_str}) -> None:\n')
                        else:
                            f.write(f'        def __init__(self) -> None:\n')
                        f.write(f'            """Initialize {class_name_inner} instance"""\n')
                        f.write('            ...\n\n')
                    else:
                        # Fallback - generic constructor
                        f.write('        def __init__(self, *args: Any, **kwargs: Any) -> None:\n')
                        f.write(f'            """Initialize {class_name_inner} instance"""\n')
                        f.write('            ...\n\n')

                    # Generate methods
                    methods = cls.get('methods', [])
                    if isinstance(methods, list):
                        for method in methods:
                            if isinstance(method, dict):
                                method_name = method.get('name', '')
                                method_doc = method.get('doc', '')
                            else:
                                method_name = str(method)
                                method_doc = ''

                            if method_name:
                                f.write(f'        def {method_name}(self, *args: Any, **kwargs: Any) -> Any:\n')
                                if method_doc:
                                    f.write(f'            """{method_doc}"""\n')
                                else:
                                    f.write(f'            """C++ method: {method_name}"""\n')
                                f.write('            ...\n\n')

                    # Generate fields as properties
                    fields_list = cls.get('fields', [])
                    for field in fields_list:
                        if isinstance(field, dict):
                            field_name = field.get('name', '')
                            field_type = self._cpp_to_python_type(field.get('type', 'Any'))
                        else:
                            field_name = str(field)
                            field_type = 'Any'

                        if field_name:
                            f.write(f'        {field_name}: {field_type}\n')

                    if not methods and not fields_list:
                        f.write('        pass\n')

                    f.write('\n')

                # Generate module-level functions as methods
                functions = module_info.get('functions', [])
                for func in functions:
                    if isinstance(func, dict):
                        func_name = func.get('name', '')
                        func_doc = func.get('doc', '')
                    else:
                        func_name = str(func)
                        func_doc = ''

                    if func_name:
                        # Module-level functions are callable directly on the wrapper
                        f.write(f'    def {func_name}(self, *args: Any, **kwargs: Any) -> Any:\n')
                        if func_doc:
                            f.write(f'        """{func_doc}"""\n')
                        else:
                            f.write(f'        """C++ function: {func_name}"""\n')
                        f.write('        ...\n\n')

                if not classes and not functions and not structs:
                    f.write('    pass\n')

                f.write('\n\n')

            f.write('# CppApi with typed include() overloads for each module\n')
            f.write('class CppApi:\n')
            f.write('    """C++ API Manager with typed module loading.\n\n')
            f.write('    The include() method returns a module wrapper with full type hints\n')
            f.write('    for VSCode/PyCharm autocomplete support.\n')
            f.write('    """\n\n')

            f.write('    def __init__(self, project_root: Optional[str] = None, auto_update: bool = True) -> None:\n')
            f.write('        """Initialize CppApi.\n\n')
            f.write('        Args:\n')
            f.write('            project_root: Path to project root (default: auto-detect)\n')
            f.write('            auto_update: Whether to auto-rebuild on source changes\n')
            f.write('        """\n')
            f.write('        ...\n\n')

            # Generate overloaded include() methods for each module
            for module_name, _ in modules.items():
                wrapper_class = f"{module_name.capitalize()}ModuleWrapper"
                f.write('    @overload\n')
                f.write(f'    def include(self, module_name: str = "{module_name}", auto_update: Optional[bool] = None) -> {wrapper_class}: ...\n\n')

            # Fallback overload for unknown modules
            f.write('    @overload\n')
            f.write('    def include(self, module_name: str, auto_update: Optional[bool] = None) -> Any: ...\n\n')

            # Actual implementation signature
            f.write('    def include(self, module_name: str, auto_update: Optional[bool] = None) -> Any:\n')
            f.write('        """Load a C++ module.\n\n')
            f.write('        Args:\n')
            f.write('            module_name: Name of the module to load\n')
            f.write('            auto_update: Override auto-update setting for this module\n\n')
            f.write('        Returns:\n')
            f.write('            ModuleWrapper with access to C++ classes, functions, and structs\n')
            f.write('        """\n')
            f.write('        ...\n\n')

            f.write('    def rebuild(self, verbose: bool = False) -> bool:\n')
            f.write('        """Rebuild all C++ modules."""\n')
            f.write('        ...\n\n')

            f.write('    def list_modules(self) -> List[str]:\n')
            f.write('        """List available modules."""\n')
            f.write('        ...\n')

        if verbose:
            print(f"Generated VSCode IntelliSense stubs: {pyi_file}")

    def _generate_init_pyi_overloads(self, modules: Dict, verbose: bool = False):
        """Generate module declarations in __init__.pyi for dynamic module imports.

        This enables VSCode autocomplete for: from includecpp import fast_list
        By adding explicit module variable declarations.
        """
        package_root = Path(__file__).parent.parent
        init_pyi = package_root / "__init__.pyi"

        if not init_pyi.exists():
            if verbose:
                print(f"__init__.pyi not found at {init_pyi}")
            return

        content = init_pyi.read_text(encoding='utf-8')

        # Markers for the auto-generated section
        start_marker = "# Dynamic module access via: from includecpp import <module_name>"
        auto_gen_marker = "# Auto-generated module declarations"
        end_marker = "def __dir__"

        if start_marker not in content:
            if verbose:
                print("Marker not found in __init__.pyi, skipping module generation")
            return

        # Generate module declarations - these are the KEY for IDE autocomplete!
        declarations = []
        declarations.append(auto_gen_marker)
        declarations.append("# These allow: from includecpp import <module_name>")
        for module_name in modules.keys():
            class_name = f"{module_name.capitalize()}ModuleWrapper"
            declarations.append(f'{module_name}: {class_name}')
        declarations.append("")

        # Parse and rebuild the file content
        lines = content.split('\n')
        new_lines = []
        in_auto_section = False
        found_start_marker = False
        declarations_inserted = False

        for line in lines:
            # Start of auto-generated section (skip old content)
            if auto_gen_marker in line:
                in_auto_section = True
                continue

            # Skip lines in auto-generated section until we hit end marker
            if in_auto_section:
                if end_marker in line:
                    # End of auto section, insert new declarations
                    in_auto_section = False
                    new_lines.extend(declarations)
                    new_lines.append(line)
                    declarations_inserted = True
                    continue
                # Skip old auto-generated lines (module declarations)
                if ':' in line and 'ModuleWrapper' in line:
                    continue
                if line.strip().startswith('#') and 'module' in line.lower():
                    continue
                # Keep other lines
                if line.strip():
                    new_lines.append(line)
                continue

            # Found the section marker
            if start_marker in line:
                new_lines.append(line)
                found_start_marker = True
                continue

            # First run: insert declarations before def __dir__ if not already done
            if found_start_marker and not declarations_inserted and end_marker in line:
                new_lines.extend(declarations)
                declarations_inserted = True

            new_lines.append(line)

        init_pyi.write_text('\n'.join(new_lines), encoding='utf-8')

        if verbose:
            print(f"Updated __init__.pyi with {len(modules)} module declarations")

    def _write_struct_protocol(self, f, struct_name: str, struct: Dict, template_type: Optional[str]):
        """Write struct class to protocol file for VSCode autocomplete."""
        f.write(f'    class {struct_name}:\n')

        doc = struct.get('doc', f'Struct: {struct["name"]}')
        if template_type:
            doc += f'<{template_type}>'
        f.write(f'        """{doc}"""\n\n')

        # Constructor
        f.write('        def __init__(self')
        for field in struct.get('fields', []):
            field_type = field.get('type', 'Any')
            field_name = field.get('name', '')

            # Substitute template parameter
            if template_type and field_type == 'T':
                field_type = self._cpp_to_python_type(template_type)
            else:
                field_type = self._cpp_to_python_type(field_type)

            f.write(f', {field_name}: {field_type} = ...')
        f.write(') -> None:\n')
        f.write(f'            """Initialize {struct_name}"""\n')
        f.write('            ...\n\n')

        # Fields with actual types
        for field in struct.get('fields', []):
            field_type = field.get('type', 'Any')
            field_name = field.get('name', '')
            if template_type and field_type == 'T':
                field_type = self._cpp_to_python_type(template_type)
            else:
                field_type = self._cpp_to_python_type(field_type)
            f.write(f'        {field_name}: {field_type}\n')
        f.write('\n')

        # to_dict method
        f.write('        def to_dict(self) -> Dict[str, Any]:\n')
        f.write('            """Convert struct to dictionary"""\n')
        f.write('            ...\n\n')

        # from_dict static method
        f.write('        @staticmethod\n')
        f.write(f'        def from_dict(d: Dict[str, Any]) -> "{struct_name}":\n')
        f.write('            """Create struct from dictionary"""\n')
        f.write('            ...\n\n')

    def _generate_module_pyi(self, module_name: str, module_info: Dict, verbose: bool = False):
        """Generate individual .pyi stub file for a C++ module.

        This creates {module_name}.pyi in the bindings directory alongside api.pyd.
        VSCode will use this for autocomplete when the module is imported.

        Args:
            module_name: Name of the module (e.g., 'geometry')
            module_info: Module descriptor from registry
            verbose: Print progress
        """
        pyi_file = self.bindings_dir / f"{module_name}.pyi"

        with open(pyi_file, 'w', encoding='utf-8') as f:
            f.write(f'"""Type stubs for {module_name} C++ module.\n\n')
            f.write('Auto-generated by IncludeCPP - DO NOT EDIT.\n')
            f.write('Provides VSCode/PyCharm autocomplete for C++ bindings.\n')
            f.write('"""\n\n')
            f.write('from typing import Any, List, Dict, Optional, Union, overload\n\n')

            # Generate classes
            classes = module_info.get('classes', [])
            for cls in classes:
                class_name = cls.get('name', '')
                class_doc = cls.get('doc', '')

                f.write(f'class {class_name}:\n')
                if class_doc:
                    f.write(f'    """{class_doc}"""\n\n')
                else:
                    f.write(f'    """C++ class: {class_name}"""\n\n')

                constructors = cls.get('constructors', [])
                if constructors and len(constructors) > 1:
                    # Multiple constructors - use @overload
                    for ctor in constructors:
                        param_types = ctor.get('params', [])
                        f.write('    @overload\n')
                        if param_types:
                            param_list = ['self']
                            for i, ptype in enumerate(param_types):
                                py_type = self._cpp_to_python_type(ptype)
                                param_list.append(f'arg{i}: {py_type}')
                            params_str = ', '.join(param_list)
                            f.write(f'    def __init__({params_str}) -> None: ...\n')
                        else:
                            f.write(f'    def __init__(self) -> None: ...\n')
                    f.write('\n')
                    # Actual implementation signature
                    f.write(f'    def __init__(self, *args: Any, **kwargs: Any) -> None:\n')
                    f.write(f'        """Initialize {class_name} instance."""\n')
                    f.write('        ...\n\n')
                elif constructors and len(constructors) == 1:
                    # Single constructor
                    param_types = constructors[0].get('params', [])
                    if param_types:
                        param_list = ['self']
                        for i, ptype in enumerate(param_types):
                            py_type = self._cpp_to_python_type(ptype)
                            param_list.append(f'arg{i}: {py_type}')
                        params_str = ', '.join(param_list)
                        f.write(f'    def __init__({params_str}) -> None:\n')
                    else:
                        f.write(f'    def __init__(self) -> None:\n')
                    f.write(f'        """Initialize {class_name} instance."""\n')
                    f.write('        ...\n\n')
                else:
                    # Fallback: legacy format or no constructor info
                    constructor_params = cls.get('constructor_params', [])
                    if constructor_params:
                        param_list = ['self']
                        for param in constructor_params:
                            param_name = param.get('name', 'arg')
                            param_type = self._cpp_to_python_type(param.get('type', 'Any'))
                            param_default = param.get('default', None)
                            if param_default:
                                py_default = self._convert_cpp_default(param_default, param_type)
                                param_list.append(f'{param_name}: {param_type} = {py_default}')
                            else:
                                param_list.append(f'{param_name}: {param_type}')
                        params_str = ', '.join(param_list)
                        f.write(f'    def __init__({params_str}) -> None:\n')
                    else:
                        f.write(f'    def __init__(self, *args: Any, **kwargs: Any) -> None:\n')
                    f.write(f'        """Initialize {class_name} instance."""\n')
                    f.write('        ...\n\n')

                # Methods
                methods = cls.get('methods', [])
                if isinstance(methods, list):
                    for method in methods:
                        if isinstance(method, dict):
                            method_name = method.get('name', '')
                            method_doc = method.get('doc', '')
                            return_type = method.get('return_type', 'Any')
                            parameters = method.get('parameters', [])
                            is_static = method.get('static', False)
                        else:
                            method_name = str(method)
                            method_doc = ''
                            return_type = 'Any'
                            parameters = []
                            is_static = False

                        if method_name:
                            if is_static:
                                f.write('    @staticmethod\n')

                            if parameters:
                                param_list = [] if is_static else ['self']
                                for param in parameters:
                                    param_name = param.get('name', 'arg')
                                    param_type = self._cpp_to_python_type(param.get('type', 'Any'))
                                    param_default = param.get('default', None)
                                    if param_default:
                                        py_default = self._convert_cpp_default(param_default, param_type)
                                        param_list.append(f'{param_name}: {param_type} = {py_default}')
                                    else:
                                        param_list.append(f'{param_name}: {param_type}')
                                params_str = ', '.join(param_list)
                            else:
                                params_str = 'self' if not is_static else ''

                            py_return_type = self._cpp_to_python_type(return_type)
                            f.write(f'    def {method_name}({params_str}) -> {py_return_type}:\n')
                            if method_doc:
                                f.write(f'        """{method_doc}"""\n')
                            else:
                                f.write(f'        """C++ method: {method_name}"""\n')
                            f.write('        ...\n\n')

                # Fields as class attributes
                fields = cls.get('fields', [])
                for field in fields:
                    if isinstance(field, dict):
                        field_name = field.get('name', '')
                        field_type = self._cpp_to_python_type(field.get('type', 'Any'))
                    else:
                        field_name = str(field)
                        field_type = 'Any'
                    if field_name:
                        f.write(f'    {field_name}: {field_type}\n')

                if not methods and not fields:
                    f.write('    pass\n')
                f.write('\n')

            # Generate structs
            structs = module_info.get('structs', [])
            for struct in structs:
                struct_name = struct.get('name', '')
                is_template = struct.get('is_template', False)
                template_types = struct.get('template_types', [])
                fields = struct.get('fields', [])
                doc = struct.get('doc', '')

                if is_template:
                    for ttype in template_types:
                        full_name = f"{struct_name}_{ttype}"
                        self._write_struct_to_pyi(f, full_name, struct, ttype)
                else:
                    self._write_struct_to_pyi(f, struct_name, struct, None)

            # Generate module-level functions
            functions = module_info.get('functions', [])
            for func in functions:
                if isinstance(func, dict):
                    func_name = func.get('name', '')
                    func_doc = func.get('doc', '')
                    return_type = func.get('return_type', 'Any')
                    parameters = func.get('parameters', [])
                else:
                    func_name = str(func)
                    func_doc = ''
                    return_type = 'Any'
                    parameters = []

                if func_name:
                    if parameters:
                        param_list = []
                        for param in parameters:
                            param_name = param.get('name', 'arg')
                            param_type = self._cpp_to_python_type(param.get('type', 'Any'))
                            param_default = param.get('default', None)
                            if param_default:
                                py_default = self._convert_cpp_default(param_default, param_type)
                                param_list.append(f'{param_name}: {param_type} = {py_default}')
                            else:
                                param_list.append(f'{param_name}: {param_type}')
                        params_str = ', '.join(param_list)
                    else:
                        params_str = '*args: Any, **kwargs: Any'

                    py_return_type = self._cpp_to_python_type(return_type)
                    f.write(f'def {func_name}({params_str}) -> {py_return_type}:\n')
                    if func_doc:
                        f.write(f'    """{func_doc}"""\n')
                    else:
                        f.write(f'    """C++ function: {func_name}"""\n')
                    f.write('    ...\n\n')

        if verbose:
            print(f"  Generated: {pyi_file.name}")

    def _write_struct_to_pyi(self, f, struct_name: str, struct: Dict, template_type: Optional[str]):
        """Write a struct class definition to a .pyi file."""
        doc = struct.get('doc', f'C++ struct: {struct["name"]}')
        if template_type:
            doc += f'<{template_type}>'

        f.write(f'class {struct_name}:\n')
        f.write(f'    """{doc}"""\n\n')

        # Constructor with fields
        fields = struct.get('fields', [])
        f.write('    def __init__(self')
        for field in fields:
            field_type = field.get('type', 'Any')
            field_name = field.get('name', '')
            if template_type and field_type == 'T':
                field_type = self._cpp_to_python_type(template_type)
            else:
                field_type = self._cpp_to_python_type(field_type)
            f.write(f', {field_name}: {field_type} = ...')
        f.write(') -> None:\n')
        f.write(f'        """Initialize {struct_name}."""\n')
        f.write('        ...\n\n')

        # Fields as attributes
        for field in fields:
            field_type = field.get('type', 'Any')
            field_name = field.get('name', '')
            if template_type and field_type == 'T':
                field_type = self._cpp_to_python_type(template_type)
            else:
                field_type = self._cpp_to_python_type(field_type)
            f.write(f'    {field_name}: {field_type}\n')

        f.write('\n')
        f.write('    def to_dict(self) -> Dict[str, Any]:\n')
        f.write('        """Convert struct to dictionary."""\n')
        f.write('        ...\n\n')

        f.write('    @staticmethod\n')
        f.write(f'    def from_dict(d: Dict[str, Any]) -> "{struct_name}":\n')
        f.write('        """Create struct from dictionary."""\n')
        f.write('        ...\n\n')

    def _configure_vscode_autocomplete(self, verbose: bool = False):
        """Auto-configure VSCode for C++ module autocomplete.

        Creates or updates .vscode/settings.json to include the bindings
        directory in python.analysis.extraPaths for Pylance autocomplete.
        """
        vscode_dir = self.project_root / ".vscode"
        settings_file = vscode_dir / "settings.json"

        # Path to bindings directory (use forward slashes for JSON)
        bindings_path = str(self.bindings_dir).replace("\\", "/")

        try:
            # Load existing settings or create new
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    try:
                        settings = json.load(f)
                    except json.JSONDecodeError:
                        settings = {}
            else:
                settings = {}
                vscode_dir.mkdir(parents=True, exist_ok=True)

            # Get or create extraPaths list
            extra_paths = settings.get("python.analysis.extraPaths", [])
            if not isinstance(extra_paths, list):
                extra_paths = []

            # Add bindings path if not already present
            if bindings_path not in extra_paths:
                extra_paths.append(bindings_path)
                settings["python.analysis.extraPaths"] = extra_paths

                # Write updated settings
                with open(settings_file, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4)

                if verbose:
                    print(f"\nVSCode configured for autocomplete:")
                    print(f"  Updated: {settings_file}")
                    print(f"  Added path: {bindings_path}")
            elif verbose:
                print(f"\nVSCode autocomplete already configured")

        except Exception as e:
            if verbose:
                print(f"Warning: Could not configure VSCode: {e}")

    def _generate_all_module_pyi(self, verbose: bool = False):
        """Generate .pyi stub files for all C++ modules in bindings directory.

        This is called after a successful build to create VSCode-compatible
        type stubs for each module.
        """
        if not self.registry_file.exists():
            if verbose:
                print("No registry file found, skipping module .pyi generation")
            return

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        except Exception as e:
            if verbose:
                print(f"Failed to load registry for module .pyi generation: {e}")
            return

        modules = registry.get('modules', registry)

        if verbose:
            print(f"\nGenerating .pyi stubs for {len(modules)} module(s)...")

        for module_name, module_info in modules.items():
            try:
                self._generate_module_pyi(module_name, module_info, verbose=verbose)
            except Exception as e:
                if verbose:
                    print(f"  Warning: Failed to generate {module_name}.pyi: {e}")

    def _generate_pyi_stub(self, verbose: bool = False):
        """Generate .pyi stub file for VSCode IntelliSense with CORRECT module structure.

        This generates TWO types of stubs:
        1. Module wrapper stubs in package directory for VSCode autocomplete
        2. API module stub in bindings directory for runtime type checking
        3. Individual module .pyi files for direct module imports
        """
        if not self.registry_file.exists():
            if verbose:
                print("No registry file found, skipping .pyi generation")
            return

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        except Exception as e:
            if verbose:
                print(f"Failed to load registry for .pyi generation: {e}")
            return

        modules = registry.get('modules', registry)

        # Generate cpp_api_extensions.pyi in package directory for VSCode IntelliSense
        # This is the key to making autocomplete work!
        self._generate_cpp_api_extensions(modules, verbose)

        # Generate __getattr__ overloads in __init__.pyi for dynamic imports
        # This enables: from includecpp import fast_list
        self._generate_init_pyi_overloads(modules, verbose)

        # Also generate api.pyi in bindings for completeness
        pyi_file = self.bindings_dir / "api.pyi"

        with open(pyi_file, 'w', encoding='utf-8') as f:
            f.write('"""Auto-generated type stubs for IncludeCPP C++ bindings\n\n')
            f.write('This file describes the raw C++ module structure.\n')
            f.write('For VSCode autocomplete, see cpp_api_extensions.pyi\n')
            f.write('"""\n')
            f.write('from typing import Any, List, Dict, Optional, Union, overload, Sequence\n\n')

            # Generate stubs for each module
            for module_name, module_info in modules.items():
                f.write(f'class {module_name}:\n')
                f.write(f'    """Module: {module_name}\n\n')

                # Add module docstring with summary
                sources = module_info.get('sources', [])
                if sources:
                    f.write(f'    Sources: {", ".join(sources)}\n')

                deps = module_info.get('dependencies', [])
                if deps:
                    dep_names = [d.get('target', '?') for d in deps]
                    f.write(f'    Dependencies: {", ".join(dep_names)}\n')

                f.write('    """\n\n')

                # Generate STRUCT types (v2.0+)
                structs = module_info.get('structs', [])
                for struct in structs:
                    struct_name = struct.get('name', '')
                    is_template = struct.get('is_template', False)
                    template_types = struct.get('template_types', [])
                    fields = struct.get('fields', [])
                    doc = struct.get('doc', '')

                    if is_template:
                        # Generate struct for each template type
                        for ttype in template_types:
                            full_name = f"{struct_name}_{ttype}"
                            f.write(f'    class {full_name}:\n')
                            if doc:
                                f.write(f'        """{doc}\n\n')
                                f.write(f'        Template instantiation: {struct_name}<{ttype}>\n')
                                f.write('        """\n\n')
                            else:
                                f.write(f'        """POD struct: {struct_name}<{ttype}>"""\n\n')

                            # Constructor
                            f.write(f'        def __init__(self')
                            for field in fields:
                                field_type = field.get('type', 'Any')
                                field_name = field.get('name', '')
                                # Replace template parameter T
                                if field_type == 'T':
                                    field_type = self._cpp_to_python_type(ttype)
                                else:
                                    field_type = self._cpp_to_python_type(field_type)
                                f.write(f', {field_name}: {field_type} = ...')
                            f.write(') -> None:\n')
                            f.write(f'            """Initialize {full_name}"""\n')
                            f.write('            ...\n\n')

                            # Fields with actual types
                            for field in fields:
                                field_type = field.get('type', 'Any')
                                field_name = field.get('name', '')
                                if field_type == 'T':
                                    field_type = self._cpp_to_python_type(ttype)
                                else:
                                    field_type = self._cpp_to_python_type(field_type)
                                f.write(f'        {field_name}: {field_type}\n')
                            f.write('\n')

                            # to_dict method
                            f.write('        def to_dict(self) -> Dict[str, Any]:\n')
                            f.write('            """Convert struct to dictionary"""\n')
                            f.write('            ...\n\n')

                            # from_dict static method
                            f.write('        @staticmethod\n')
                            f.write(f'        def from_dict(d: Dict[str, Any]) -> "{module_name}.{full_name}":\n')
                            f.write('            """Create struct from dictionary"""\n')
                            f.write('            ...\n\n')
                    else:
                        # Non-template struct
                        f.write(f'    class {struct_name}:\n')
                        if doc:
                            f.write(f'        """{doc}"""\n\n')
                        else:
                            f.write(f'        """POD struct: {struct_name}"""\n\n')

                        # Constructor
                        f.write(f'        def __init__(self')
                        for field in fields:
                            field_type = self._cpp_to_python_type(field.get('type', 'Any'))
                            field_name = field.get('name', '')
                            f.write(f', {field_name}: {field_type} = ...')
                        f.write(') -> None:\n')
                        f.write(f'            """Initialize {struct_name}"""\n')
                        f.write('            ...\n\n')

                        # Fields
                        for field in fields:
                            field_type = self._cpp_to_python_type(field.get('type', 'Any'))
                            field_name = field.get('name', '')
                            f.write(f'        {field_name}: {field_type}\n')
                        f.write('\n')

                        # to_dict method
                        f.write('        def to_dict(self) -> Dict[str, Any]:\n')
                        f.write('            """Convert struct to dictionary"""\n')
                        f.write('            ...\n\n')

                        # from_dict static method
                        f.write('        @staticmethod\n')
                        f.write(f'        def from_dict(d: Dict[str, Any]) -> "{module_name}.{struct_name}":\n')
                        f.write('            """Create struct from dictionary"""\n')
                        f.write('            ...\n\n')

                # Generate classes
                classes = module_info.get('classes', [])
                for cls in classes:
                    class_name = cls.get('name', '')
                    class_doc = cls.get('doc', '')

                    f.write(f'    class {class_name}:\n')
                    if class_doc:
                        f.write(f'        """{class_doc}"""\n\n')
                    else:
                        f.write(f'        """C++ class: {class_name}"""\n\n')

                    # Constructor
                    f.write(f'        def __init__(self, *args: Any, **kwargs: Any) -> None:\n')
                    f.write(f'            """Initialize {class_name} instance"""\n')
                    f.write(f'            ...\n\n')

                    # Initialize method (factory method)
                    f.write(f'        @staticmethod\n')
                    f.write(f'        def Initialize(*args: Any, **kwargs: Any) -> "{module_name}.{class_name}":\n')
                    f.write(f'            """Create and initialize a new {class_name} instance"""\n')
                    f.write(f'            ...\n\n')

                    # Generate methods with real signatures (v2.3.5)
                    methods = cls.get('methods', [])
                    if isinstance(methods, list):
                        for method in methods:
                            if isinstance(method, dict):
                                method_name = method.get('name', '')
                                method_doc = method.get('doc', '')
                                return_type = method.get('return_type', 'Any')
                                parameters = method.get('parameters', [])
                                is_const = method.get('const', False)
                                is_static = method.get('static', False)
                            else:
                                method_name = str(method)
                                method_doc = ''
                                return_type = 'Any'
                                parameters = []
                                is_const = False
                                is_static = False

                            if method_name:
                                if is_static:
                                    f.write(f'        @staticmethod\n')

                                if parameters:
                                    param_list = ['self'] if not is_static else []
                                    for param in parameters:
                                        param_name = param.get('name', 'arg')
                                        param_type = self._cpp_to_python_type(param.get('type', 'Any'))
                                        param_default = param.get('default', None)

                                        if param_default:
                                            py_default = self._convert_cpp_default(param_default, param_type)
                                            param_list.append(f'{param_name}: {param_type} = {py_default}')
                                        else:
                                            param_list.append(f'{param_name}: {param_type}')

                                    params_str = ', '.join(param_list)
                                else:
                                    params_str = 'self' if not is_static else ''

                                py_return_type = self._cpp_to_python_type(return_type)

                                f.write(f'        def {method_name}({params_str}) -> {py_return_type}:\n')
                                if method_doc:
                                    f.write(f'            """{method_doc}"""\n')
                                else:
                                    f.write(f'            """C++ method: {method_name}"""\n')
                                f.write(f'            ...\n\n')

                    # Generate fields as properties
                    fields = cls.get('fields', [])
                    for field in fields:
                        if isinstance(field, dict):
                            field_name = field.get('name', '')
                            field_type = self._cpp_to_python_type(field.get('type', 'Any'))
                        else:
                            field_name = str(field)
                            field_type = 'Any'

                        if field_name:
                            f.write(f'        {field_name}: {field_type}\n')

                    if not methods and not fields:
                        f.write(f'        pass\n\n')

                # Generate functions with real signatures (v2.3.5)
                functions = module_info.get('functions', [])
                for func in functions:
                    if isinstance(func, dict):
                        func_name = func.get('name', '')
                        func_doc = func.get('doc', '')
                        return_type = func.get('return_type', 'Any')
                        parameters = func.get('parameters', [])
                        is_static = func.get('static', False)
                    else:
                        func_name = str(func)
                        func_doc = ''
                        return_type = 'Any'
                        parameters = []
                        is_static = False

                    if func_name:
                        f.write(f'    @staticmethod\n')

                        if parameters:
                            param_list = []
                            for param in parameters:
                                param_name = param.get('name', 'arg')
                                param_type = self._cpp_to_python_type(param.get('type', 'Any'))
                                param_default = param.get('default', None)

                                if param_default:
                                    py_default = self._convert_cpp_default(param_default, param_type)
                                    param_list.append(f'{param_name}: {param_type} = {py_default}')
                                else:
                                    param_list.append(f'{param_name}: {param_type}')

                            params_str = ', '.join(param_list)
                        else:
                            params_str = ''

                        py_return_type = self._cpp_to_python_type(return_type)

                        f.write(f'    def {func_name}({params_str}) -> {py_return_type}:\n')

                        if func_doc:
                            f.write(f'        """{func_doc}"""\n')
                        else:
                            f.write(f'        """C++ function: {func_name}"""\n')
                        f.write(f'        ...\n\n')

                if not classes and not functions and not structs:
                    f.write(f'    pass\n')

                f.write('\n')

        if verbose:
            print(f"Generated type stub: {pyi_file}")

    def _update_source_hashes(self, verbose: bool = False):
        """Update source_hashes in registry after successful build (v2.3.5 format)."""
        if not self.registry_file.exists():
            if verbose:
                print("No registry file found, skipping hash update")
            return

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                registry = json.load(f)
        except Exception as e:
            if verbose:
                print(f"Failed to load registry for hash update: {e}")
            return

        modules = registry.get('modules', registry)

        for module_name, module_info in modules.items():
            sources = module_info.get('sources', [])
            source_hashes = {}

            # Hash all source files
            for source in sources:
                source_path = self.project_root / source
                hash_value = self._compute_hash(source_path)
                source_hashes[source] = hash_value

            # Also hash the .cp file
            cp_file = module_info.get('cp_file', '')
            if cp_file:
                cp_path = Path(cp_file)
                if cp_path.exists():
                    cp_hash = self._compute_hash(cp_path)
                    source_hashes[f"{module_name}.cp"] = cp_hash

            # Store in v2.3.5 format (source_hashes field)
            module_info['source_hashes'] = source_hashes

            # Remove old v1.6 'hashes' field if exists
            if 'hashes' in module_info:
                del module_info['hashes']

        if 'modules' in registry:
            registry['modules'] = modules
        else:
            registry = modules

        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2)
            if verbose:
                print(f"Updated source hashes in registry (v2.3.5 format)")
        except Exception as e:
            if verbose:
                print(f"Failed to save registry with hashes: {e}")

    def _cpp_to_python_type(self, cpp_type: str) -> str:
        """Convert C++ type to Python type hint."""
        # Basic type mappings
        type_map = {
            'int': 'int',
            'long': 'int',
            'short': 'int',
            'float': 'float',
            'double': 'float',
            'bool': 'bool',
            'string': 'str',
            'std::string': 'str',
            'void': 'None',
            'char': 'str',
        }

        # Remove const, &, *
        clean_type = cpp_type.strip()
        clean_type = clean_type.replace('const', '').strip()
        clean_type = clean_type.rstrip('&*').strip()

        # Check basic types
        if clean_type in type_map:
            return type_map[clean_type]

        # Handle vector<T>
        if 'vector<' in clean_type or 'std::vector<' in clean_type:
            start = clean_type.find('<') + 1
            end = clean_type.rfind('>')
            if start > 0 and end > start:
                element_type = clean_type[start:end].strip()
                return f'List[{self._cpp_to_python_type(element_type)}]'

        # Handle map<K,V>
        if 'map<' in clean_type or 'std::map<' in clean_type:
            start = clean_type.find('<') + 1
            end = clean_type.rfind('>')
            if start > 0 and end > start:
                inner = clean_type[start:end]
                # Simple split by comma (doesn't handle nested templates perfectly)
                parts = [p.strip() for p in inner.split(',', 1)]
                if len(parts) == 2:
                    key_type = self._cpp_to_python_type(parts[0])
                    val_type = self._cpp_to_python_type(parts[1])
                    return f'Dict[{key_type}, {val_type}]'

        # Unknown type - return as is
        return 'Any'

    def _convert_cpp_default(self, cpp_default: str, param_type: str) -> str:
        """Convert C++ default value to Python equivalent.

        Args:
            cpp_default: C++ default value (e.g., "nullptr", "true", "0")
            param_type: Python type hint for the parameter

        Returns:
            Python default value string
        """
        cpp_default = cpp_default.strip()

        if cpp_default == "nullptr" or cpp_default == "NULL":
            return "None"

        if cpp_default == "true":
            return "True"
        if cpp_default == "false":
            return "False"

        if cpp_default.startswith('"') and cpp_default.endswith('"'):
            return cpp_default
        if cpp_default.startswith("'") and cpp_default.endswith("'"):
            return f'"{cpp_default[1:-1]}"'

        if cpp_default.replace('.', '', 1).replace('-', '', 1).replace('+', '', 1).isdigit():
            return cpp_default

        if cpp_default == '""' or cpp_default == "''":
            return '""'

        if cpp_default.startswith('{') and cpp_default.endswith('}'):
            return cpp_default.replace('{', '[').replace('}', ']')

        return cpp_default

    def _install_module(self, verbose: bool = False, skip_if_exists: bool = False):
        """Copy compiled api.pyd to bindings directory."""
        dest = self.bindings_dir / f"api{self._get_pyd_suffix()}"

        # If module already in bindings_dir (direct compilation), skip
        if skip_if_exists and dest.exists():
            if verbose:
                print(f"Module already in place: {dest}")
            # Still copy MinGW DLLs
            self._copy_mingw_dlls(verbose=verbose)
            return

        pyd_locations = [
            self.cmake_build_dir / "Release" / f"api{self._get_pyd_suffix()}",
            self.cmake_build_dir / f"api{self._get_pyd_suffix()}",
        ]

        api_pyd = None
        for loc in pyd_locations:
            if loc.exists():
                api_pyd = loc
                break

        if not api_pyd:
            raise CppBuildError(
                f"Compiled module not found. Searched:\n" +
                "\n".join(f"  - {loc}" for loc in pyd_locations)
            )

        if dest.exists():
            backup = dest.with_suffix(dest.suffix + ".backup")
            try:
                shutil.move(str(dest), str(backup))
                if verbose:
                    print(f"Backed up old module: {backup}")
            except PermissionError as e:
                raise CppBuildError(
                    f"Cannot move existing module - file is locked!\n\n"
                    f"File: {dest}\n\n"
                    f"This usually means:\n"
                    f"  - A compiled .exe using this module is still running\n"
                    f"  - Another Python process has imported this module\n"
                    f"  - Your IDE/editor has the file open\n\n"
                    f"Fix:\n"
                    f"  1. Close any running .exe that uses this module\n"
                    f"  2. Close Python REPL/scripts using this module\n"
                    f"  3. Restart your IDE if it imported the module\n"
                    f"  4. Then run 'includecpp rebuild' again\n\n"
                    f"Original error: {e}"
                )
            except OSError as e:
                # Linux/Mac: ETXTBSY, EBUSY, etc.
                if e.errno in (16, 26):  # EBUSY, ETXTBSY
                    raise CppBuildError(
                        f"Cannot move module - file is busy!\n\n"
                        f"File: {dest}\n\n"
                        f"A process is currently using this file.\n\n"
                        f"Fix: Close any process using this module, then rebuild."
                    )
                raise

        try:
            shutil.copy2(str(api_pyd), str(dest))
        except PermissionError as e:
            raise CppBuildError(
                f"Cannot write module - permission denied!\n\n"
                f"Destination: {dest}\n\n"
                f"Possible causes:\n"
                f"  - File is locked by another process (close running .exe)\n"
                f"  - Antivirus blocking the write\n"
                f"  - Insufficient permissions\n\n"
                f"Fix: Close any process using '{dest.name}', then rebuild.\n\n"
                f"Original error: {e}"
            )
        except OSError as e:
            if e.errno in (16, 26):  # EBUSY, ETXTBSY (Linux/Mac)
                raise CppBuildError(
                    f"Cannot write module - file is busy!\n\n"
                    f"File: {dest}\n"
                    f"A process is currently using this file.\n\n"
                    f"Fix: Close any process using this module, then rebuild."
                )
            raise

        if verbose:
            print(f"Installed module: {dest}")

        # Copy MinGW DLLs if on Windows
        self._copy_mingw_dlls(verbose=verbose)

    def _get_pyd_suffix(self) -> str:
        """Get platform-specific Python extension suffix."""
        if platform.system() == "Windows":
            return ".pyd"
        else:
            return ".so"

    def _validate_module(self, verbose: bool = False):
        """Validate that api module can be imported."""
        bindings_path = str(self.bindings_dir)

        if bindings_path not in sys.path:
            sys.path.insert(0, bindings_path)

        try:
            if 'api' in sys.modules:
                del sys.modules['api']

            import api

            if verbose:
                print(f"Module validated: {api.__name__}")
                if hasattr(api, '__doc__'):
                    print(f"  Doc: {api.__doc__}")

        except ImportError as e:
            raise CppValidationError(
                f"Module import failed: {e}\n"
                f"Check that api{self._get_pyd_suffix()} exists in {self.bindings_dir}"
            ) from e

    # ========================================================================

    def _load_registry(self) -> Dict[str, Any]:
        """Load module registry (v1.6 or v2.0 format)."""
        if not self.registry_file.exists():
            return {"schema_version": "2.0", "modules": {}}

        try:
            with open(self.registry_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Detect version: v1.6.0 has modules at root, v2.0 has "modules" key
            if "schema_version" not in data:
                # v1.6.0 format - convert to v2.0
                return {"schema_version": "1.6", "modules": data}

            return data

        except json.JSONDecodeError:
            return {"schema_version": "2.0", "modules": {}}

    def _parse_all_modules(self, verbose: bool = False) -> Dict[str, Dict]:
        """Parse all .cp files and return module descriptors.

        Returns:
            Dict mapping module_name -> module_descriptor (from registry JSON)
        """
        # Run plugin_gen to generate registry
        self._generate_bindings(verbose=verbose)

        # Load registry to get module info
        registry = self._load_registry()
        return registry.get("modules", {})

    def _build_dependency_graph(self, modules: Dict[str, Dict]) -> List[List[str]]:
        """Build topological dependency order using Kahn's algorithm.

        Args:
            modules: Dict of module_name -> module_descriptor

        Returns:
            List of dependency levels: [[level0_modules], [level1_modules], ...]
            Each level can be compiled in parallel.

        Raises:
            CppBuildError: If circular dependency detected
        """
        # Build adjacency list
        graph = {}
        in_degree = {}

        for module_name in modules:
            graph[module_name] = []
            in_degree[module_name] = 0

        # Build edges: dependency -> module (reversed for build order)
        for module_name, descriptor in modules.items():
            for dep in descriptor.get('dependencies', []):
                dep_module = dep.get('target')
                if dep_module not in modules:
                    raise CppBuildError(
                        f"Module '{module_name}' depends on unknown module '{dep_module}'"
                    )

                # dep_module must be built before module_name
                graph[dep_module].append(module_name)
                in_degree[module_name] += 1

        # Kahn's algorithm for topological sort with levels
        levels = []
        visited = set()

        while len(visited) < len(modules):
            # Find all nodes with in_degree 0 (no dependencies)
            current_level = []
            for module in modules:
                if module not in visited and in_degree[module] == 0:
                    current_level.append(module)

            if not current_level:
                # Circular dependency detected
                remaining = set(modules.keys()) - visited
                raise CppBuildError(
                    f"Circular dependency detected among: {', '.join(remaining)}\n"
                    f"Cannot determine build order."
                )

            levels.append(current_level)

            # Update in_degrees
            for module in current_level:
                visited.add(module)
                for neighbor in graph.get(module, []):
                    in_degree[neighbor] -= 1

        return levels

    def _get_affected_modules(self, module_name: str, dep_levels: List[List[str]],
                             all_modules: Dict[str, Dict]) -> List[str]:
        """Get list of modules affected by changes to given module.

        This includes the module itself and all modules that depend on it.

        Args:
            module_name: Module that changed
            dep_levels: Dependency levels from _build_dependency_graph
            all_modules: All module descriptors

        Returns:
            List of affected module names in build order
        """
        affected = set()
        affected.add(module_name)

        dependents = {}
        for mod_name in all_modules:
            dependents[mod_name] = []

        for mod_name, mod_info in all_modules.items():
            for dep in mod_info.get('dependencies', []):
                dep_target = dep.get('target')
                if dep_target in dependents:
                    dependents[dep_target].append(mod_name)

        queue = [module_name]
        while queue:
            current = queue.pop(0)
            for dependent in dependents.get(current, []):
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)

        result = []
        for level in dep_levels:
            for mod in level:
                if mod in affected:
                    result.append(mod)

        return result

    def _module_needs_rebuild(self, module_name: str, module_info: Dict, registry: Dict) -> tuple[bool, str]:
        """Check if module needs rebuild using hashes.

        Supports both v2.0 (source_hashes) and v1.6 (hashes) registry formats.

        Returns:
            (needs_rebuild: bool, reason: str)
        """
        pyd_name = f"api_{module_name}"
        pyd_path = self.bindings_dir / f"{pyd_name}{self._get_pyd_suffix()}"

        # Check if .pyd exists
        if not pyd_path.exists():
            return (True, f".pyd not found: {pyd_path.name}")

        # Get stored hashes with v2.0/v1.6 compatibility
        old_registry = registry.get('modules', {}).get(module_name, {})
        stored_hashes = old_registry.get('source_hashes', old_registry.get('hashes', {}))

        # If no hashes stored at all, rebuild needed
        if not stored_hashes:
            return (True, "No hash history found")

        # Check source file hashes
        for source_file in module_info.get('sources', []):
            source_path = self.project_root / source_file
            if not source_path.exists():
                source_path = self.include_dir / source_file

            if source_path.exists():
                current_hash = self._compute_hash(source_path)

                # Try full path first, then filename only (v1.6 compatibility)
                stored_hash = stored_hashes.get(source_file, stored_hashes.get(source_path.name, None))

                if stored_hash is None:
                    return (True, f"No hash for: {source_path.name}")

                # Handle hash length mismatch (v1.6 = 16 chars, v2.0+ = 64 chars)
                if len(stored_hash) != len(current_hash):
                    min_len = min(len(stored_hash), len(current_hash))
                    if current_hash[:min_len] != stored_hash[:min_len]:
                        return (True, f"Source changed: {source_path.name}")
                elif current_hash != stored_hash:
                    return (True, f"Source changed: {source_path.name}")

        # Check .cp file hash
        cp_file = module_info.get('cp_file', '')
        if cp_file:
            cp_path = Path(cp_file)
            if cp_path.exists():
                current_hash = self._compute_hash(cp_path)
                cp_key = f"{module_name}.cp"
                stored_hash = stored_hashes.get(cp_key, None)

                if stored_hash is None:
                    return (True, ".cp file hash missing")

                # Handle hash length mismatch
                if len(stored_hash) != len(current_hash):
                    min_len = min(len(stored_hash), len(current_hash))
                    if current_hash[:min_len] != stored_hash[:min_len]:
                        return (True, ".cp file changed")
                elif current_hash != stored_hash:
                    return (True, ".cp file changed")

        # Check if dependencies were rebuilt more recently
        for dep in module_info.get('dependencies', []):
            dep_module = dep.get('target')
            dep_info = registry.get('modules', {}).get(dep_module, {})

            dep_built = dep_info.get('last_built', '')
            self_built = old_registry.get('last_built', '')

            if dep_built > self_built:
                return (True, f"Dependency rebuilt: {dep_module}")

        return (False, "Up to date")

    def rebuild(self,
                modules: Optional[List[str]] = None,
                incremental: bool = True,
                parallel: bool = False,
                clean: bool = False,
                verbose: bool = False,
                fast: bool = False) -> bool:
        """v2.0: Rebuild modules with incremental and per-module support.

        Args:
            modules: List of specific modules to rebuild (None = all)
            incremental: Use incremental compilation (skip unchanged)
            parallel: Compile independent modules in parallel (not implemented yet)
            clean: Force clean rebuild (ignore incremental)
            verbose: Print detailed output
            fast: Ultra-fast mode - skip unnecessary checks, assume generator is up to date

        Returns:
            True if build succeeded
        """
        # Clear caches on clean build
        if clean:
            self._clear_compiler_cache()

        # Fast mode: skip to essentials only
        if fast and not clean:
            return self._rebuild_fast(modules=modules, verbose=verbose)

        if verbose:
            print("=" * 60)
            print("IncludeCPP v2.0 Build System")
            print("=" * 60)
            print(f"Project: {self.config.config.get('project', 'unnamed')}")
            print(f"Incremental: {incremental and not clean}")
            print("=" * 60)

        # Phase 1: Build generator
        if verbose:
            print("\n[1/5] Building plugin generator...")
        self._build_generator(verbose=verbose)

        # Phase 2: Parse all .cp files (generates registry)
        if verbose:
            print("\n[2/5] Parsing .cp files...")
        all_modules = self._parse_all_modules(verbose=verbose)

        if not all_modules:
            raise CppBuildError("No modules found in plugins directory")

        # Phase 3: Load existing registry for incremental check
        if verbose:
            print("\n[3/5] Determining rebuild targets...")

        registry = self._load_registry()

        # Determine what to rebuild
        if clean:
            to_rebuild = list(all_modules.keys())
            if verbose:
                print(f"  Clean build: rebuilding all {len(to_rebuild)} modules")

        elif modules is not None:
            # User specified modules
            to_rebuild = [m for m in modules if m in all_modules]
            if verbose:
                print(f"  User specified: {', '.join(to_rebuild)}")

        elif incremental:
            # Incremental: only rebuild changed modules
            to_rebuild = []
            for module_name, module_info in all_modules.items():
                needs_rebuild, reason = self._module_needs_rebuild(module_name, module_info, registry)
                if needs_rebuild:
                    to_rebuild.append(module_name)
                    if verbose:
                        print(f"  -> {module_name}: {reason}")

            if not to_rebuild:
                if verbose:
                    print("  All modules up to date!")
                return True

        else:
            # Full rebuild
            to_rebuild = list(all_modules.keys())
            if verbose:
                print(f"  Full rebuild: {len(to_rebuild)} modules")

        # Phase 4: Build dependency order
        if verbose:
            print(f"\n[4/5] Building {len(to_rebuild)} module(s)...")

        try:
            dep_levels = self._build_dependency_graph(all_modules)

            # Filter to only modules we need to rebuild
            filtered_levels = []
            for level in dep_levels:
                filtered = [m for m in level if m in to_rebuild]
                if filtered:
                    filtered_levels.append(filtered)

            if verbose and len(filtered_levels) > 1:
                print(f"  Build order: {len(filtered_levels)} dependency level(s)")

        except CppBuildError as e:
            raise CppBuildError(f"Dependency resolution failed: {e}") from e

        # Phase 5: Build modules (sequential for now, parallel in future)
        # For v2.0, we still use monolithic build but with per-module tracking
        # True per-module builds will come later in implementation
        success = self.rebuild_all(verbose=verbose)

        if verbose:
            print("\n" + "=" * 60)
            print("BUILD COMPLETED")
            print("=" * 60)

        return success

    def _rebuild_fast(self, modules: Optional[List[str]] = None, verbose: bool = False) -> bool:
        """Ultra-fast rebuild - skip unnecessary steps.

        Checks modification times to skip work when nothing changed.
        Typically runs in <3 seconds for no-change rebuilds.
        """
        import time
        start = time.time()

        # Check if generator exists, build only if missing
        if not self.gen_exe.exists():
            if verbose:
                print("Generator missing, building...")
            self._build_generator(verbose=verbose)
        elif verbose:
            print("Generator: cached")

        # Check if bindings need regeneration
        bindings_cpp = self.bindings_dir / "bindings.cpp"
        needs_bindings = not bindings_cpp.exists()

        if not needs_bindings:
            # Check if any .cp file is newer than bindings.cpp
            bindings_mtime = bindings_cpp.stat().st_mtime
            for cp in self.plugins_dir.glob("*.cp"):
                if cp.stat().st_mtime > bindings_mtime:
                    needs_bindings = True
                    if verbose:
                        print(f"  {cp.name} changed")
                    break

        if needs_bindings:
            if verbose:
                print("Regenerating bindings...")
            self._generate_bindings(verbose=verbose)
        elif verbose:
            print("Bindings: cached")

        # Use incremental compilation with object caching
        if verbose:
            print("Compiling (incremental direct)...")
        self._compile_direct_incremental(verbose=verbose)

        # Quick validation
        self._validate_module(verbose=verbose)

        # Generate pyi only if needed
        try:
            self._generate_pyi_stub(verbose=verbose)
        except Exception:
            pass

        elapsed = time.time() - start
        if verbose:
            print(f"Fast rebuild completed in {elapsed:.2f}s")

        return True

    def rebuild_all(self, verbose: bool = False) -> bool:
        """Complete build process with CMake fallback to direct compilation.

        1. Build/update plugin_gen.exe
        2. Generate bindings.cpp
        3. Try CMake build, fallback to direct compilation if CMake fails
        4. Validate module
        """
        use_direct = False

        # Phase 1: Always needed
        basic_steps = [
            ("Building plugin generator", self._build_generator),
            ("Generating bindings", self._generate_bindings),
        ]

        for i, (desc, func) in enumerate(basic_steps):
            if verbose:
                print(f"\n[{i+1}/7] {desc}...")
            try:
                func(verbose=verbose)
            except Exception as e:
                raise CppBuildError(f"{desc} failed: {e}") from e

        # Phase 2: Try CMake, fallback to direct compilation
        step_num = len(basic_steps) + 1

        try:
            # Try CMake build
            if verbose:
                print(f"\n[{step_num}/7] Generating CMake config...")
            self._generate_cmake(verbose=verbose)

            if verbose:
                print(f"\n[{step_num+1}/7] Configuring CMake...")
            self._configure_cmake(verbose=verbose)

            if verbose:
                print(f"\n[{step_num+2}/7] Compiling C++...")
            self._compile_cpp(verbose=verbose)

            if verbose:
                print(f"\n[{step_num+3}/7] Installing module...")
            self._install_module(verbose=verbose)

        except CppBuildError as e:
            if verbose:
                print(f"\nCMake build failed: {e}")
                print("Falling back to direct incremental compilation...")

            # Direct incremental compilation fallback (v2.9.8: with object caching)
            if verbose:
                print(f"\n[{step_num}/7] Compiling with direct g++ (incremental)...")
            try:
                self._compile_direct_incremental(verbose=verbose)
                # Module is already in bindings_dir, skip install
                use_direct = True
            except Exception as e2:
                raise CppBuildError(f"Both CMake and direct compilation failed.\nCMake: {e}\nDirect: {e2}") from e2

        # Phase 3: Validate
        if verbose:
            print(f"\n[7/7] Validating module...")
        try:
            self._validate_module(verbose=verbose)
        except Exception as e:
            raise CppBuildError(f"Module validation failed: {e}") from e

        # Phase 4: Generate .pyi stub for VSCode IntelliSense
        try:
            self._generate_pyi_stub(verbose=verbose)
        except Exception as e:
            if verbose:
                print(f"Warning: .pyi generation failed: {e}")

        # Phase 4b: Generate individual module .pyi files for VSCode autocomplete
        try:
            self._generate_all_module_pyi(verbose=verbose)
        except Exception as e:
            if verbose:
                print(f"Warning: Module .pyi generation failed: {e}")

        # Phase 5: Update registry with source hashes for incremental builds
        self._update_source_hashes(verbose=verbose)

        # Auto-configure VSCode for autocomplete
        self._configure_vscode_autocomplete(verbose=verbose)

        if verbose:
            print(f"\n{'='*60}")
            print("BUILD SUCCESSFUL!")
            if use_direct:
                print("(Used direct compilation fallback)")
            print(f"{'='*60}")
            print(f"Module: {self.bindings_dir / ('api' + self._get_pyd_suffix())}")
            print(f"Registry: {self.registry_file}")
            print(f"Type Stubs: {self.bindings_dir / 'api.pyi'}")

            # Show module stubs info
            pyi_files = list(self.bindings_dir.glob("*.pyi"))
            module_pyis = [f for f in pyi_files if f.name != "api.pyi"]
            if module_pyis:
                print(f"\nModule Stubs ({len(module_pyis)}):")
                for pyi in module_pyis:
                    print(f"  - {pyi.name}")

        return True
