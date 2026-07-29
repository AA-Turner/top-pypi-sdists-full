import io
import os
import platform
import subprocess
import sys

from distutils.util import split_quoted
from pathlib import Path
from setuptools.command.build_ext import build_ext
from os import listdir
from os.path import isfile, join

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLICKHOUSE_PATH = os.path.join(ROOT_DIR, 'ClickHouse')
CLICKHOUSE_BUILD_PATH = os.environ.get('CLICKHOUSE_BUILD_PATH', os.path.join(ROOT_DIR, 'ch_build'))

TOOLSET_PATH = os.path.join(ROOT_DIR, 'functions')
TOOLSET_BUILD_PATH = os.environ.get('TOOLSET_BUILD_PATH', os.path.join(ROOT_DIR, 'ts_build'))

COMPILER_CC = os.environ.get('CC', 'clang')
COMPILER_CXX = os.environ.get('CXX', 'clang++')

BUILD_FOR_VALGRIND = bool(os.environ.get('BUILD_FOR_VALGRIND', ''))
DEBUG_SYMBOLS = os.environ.get('DEBUG_SYMBOLS', '1').lower() not in ('', '0', 'false', 'no')
OMIT_PATCHES = bool(os.environ.get('OMIT_PATCHES', ''))
SIMDJSON_DEBUG = bool(os.environ.get('SIMDJSON_DEBUG', ''))

# Sanitizer support
ASAN_ENABLED = bool(os.environ.get('ASAN_ENABLED', ''))  # AddressSanitizer
UBSAN_ENABLED = bool(os.environ.get('UBSAN_ENABLED', ''))  # UndefinedBehaviorSanitizer
MSAN_ENABLED = bool(os.environ.get('MSAN_ENABLED', ''))  # MemorySanitizer
TSAN_ENABLED = bool(os.environ.get('TSAN_ENABLED', ''))  # ThreadSanitizer
THINLTO_FLAG = '-flto=thin'

# Taken from https://github.com/cpp-best-practices/cmake_template/blob/a3971f5b45/cmake/CompilerWarnings.cmake
CLANG_WARNINGS = [
    '-Wall',
    '-Wextra',
    '-Wshadow',
    '-Wnon-virtual-dtor',
    '-Wold-style-cast',
    '-Wcast-align',
    '-Wunused',
    '-Woverloaded-virtual',
    '-Wpedantic',
    '-Wconversion',
    '-Wnull-dereference',
    '-Wdouble-promotion',
    '-Wformat=2',
    '-Wimplicit-fallthrough',
]


def apply_patch(patch_path):
    if OMIT_PATCHES:
        print('PATCH NOT APPLIED:', patch_path)
        return

    # Check if the patch is already applied by doing a reverse dry-run
    with open(patch_path, "r") as patch:
        check = subprocess.Popen(['patch', '-p1', '-R', '--dry-run'],
                                 cwd=ROOT_DIR,
                                 stdin=patch,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 text=True)
        check.communicate()
        if check.returncode == 0:
            print('PATCH ALREADY APPLIED:', patch_path)
            return

    with open(patch_path, "r") as patch:
        stdout_buffer = io.StringIO()
        stderr_buffer = io.StringIO()
        process = subprocess.Popen(['patch', '-p1', '-N'],
                                      cwd=ROOT_DIR,
                                      stdin=patch,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
        stdout, stderr = process.communicate()
        stdout_buffer.write(stdout)
        stderr_buffer.write(stderr)
        returncode = process.returncode
        if returncode != 0:
            raise Exception(f"Failed to apply patch for {patch_path}, returncode={returncode}\n\n\n"
                            f"=== stdout ===\n\n{stdout_buffer.getvalue()}\n\n\n"
                            f"=== stderr ===\n\n{stderr_buffer.getvalue()}")


class ClickHouseBuildExt(build_ext):
    def run(self):

        if not os.path.exists(os.path.join(CLICKHOUSE_PATH, 'CMakeLists.txt')):
            raise RuntimeError('Git submodules are not initialized. Run: `git submodule update --init --recursive`.')

        # One of the libraries, chosen randomly (+ the TTL functions one, added later)
        if os.path.isfile(os.path.join(CLICKHOUSE_BUILD_PATH,
                                       'src/AggregateFunctions/libclickhouse_aggregate_functions.a')) \
                and os.path.isfile(os.path.join(CLICKHOUSE_BUILD_PATH,
                                                'src/Functions/libclickhouse_ttl_functions.a')):
            return

        # Avoid segfault caused by missing global context
        apply_patch("patches/createJSON.patch")

        # Disable analyzer by default
        apply_patch("patches/disable_analyzer.patch")

        # Unwind with external code leads to crashes
        apply_patch("patches/unwind.patch")

        # Sets timezone to UTC manually and avoids reading system files
        apply_patch("patches/timezone.patch")

        # Easier access to ASTIdentifier private data
        apply_patch("patches/ASTIdentifier.patch")

        # Easier access to AggregateFunctionFactory private data
        apply_patch("patches/AggregateFunctionFactory.patch")

        # This patch is used to make it possible to use valgrind with the module
        # see https://jira.mongodb.org/browse/SERVER-25771
        apply_patch("patches/boost_flags.patch")

        # Be able to set our flags in the build (PIC)
        apply_patch("patches/Preload.patch")

        # This is only for performance.
        # Avoids calling getTreeHash() which is slow
        # Might change the output of the query since it won't replace same subqueries with the alias
        # This is ok as long as the subquery isn't super long, but it should be ok since in our case that would
        # mean the query was already super long
        apply_patch("patches/ASTWithAlias_perf.patch")

        # Emit standard SQL TRIM(BOTH/LEADING/TRAILING ... FROM ...) syntax for 2-arg
        # trimBoth/trimLeft/trimRight calls, so the output is compatible with CH < 25.2
        apply_patch("patches/trim_format.patch")

        # Removes TSA warnings (we don't compile with a libc++ with annotations)
        apply_patch("patches/tsa.patch")

        # Builds the functions needed by validate_ttl into libclickhouse_ttl_functions.a,
        # which is linked with --whole-archive/-force_load (see extra_libs).
        # NOTE: after editing this patch (or any other), the early-return above skips the
        # ClickHouse build; delete ch_build/src/Functions/libclickhouse_ttl_functions.a
        # (or the whole ch_build) to force it to run again.
        apply_patch("patches/dbmsfunctions.patch")

        # Range-check narrow-integer Field inserts so JSON/Dynamic paths widen instead of
        # silently wrapping (1944 -> -104). Backport of the ColumnVector::tryInsert fix;
        # remove once the fix lands in the pinned ClickHouse submodule.
        apply_patch("patches/ColumnVectorTryInsert.patch")

        if sys.platform == 'darwin':
            # We disable whole_archive options destined for AppleClang, which is unsupported but keeps being a PITA
            apply_patch("patches/darwin.patch")

            # Problem with offsetof macro definition
            # NOTE: offsetof.patch is no longer needed for ClickHouse 25.3+ as the changes are already upstream
            # apply_patch("patches/offsetof.patch")


        cmake_cmd = os.environ.get('CMAKE_BIN', 'cmake')
        try:
            subprocess.check_output([cmake_cmd, '--version'])
        except OSError:
            raise RuntimeError(
                'CMake must be installed to build the following extensions: ' +
                ', '.join(e.name for e in self.extensions))

        ninja_cmd = os.environ.get('NINJA_BIN', 'ninja')
        try:
            subprocess.check_output([ninja_cmd, '--version'])
        except OSError:
            raise RuntimeError('Ninja must be installed')

        if not os.path.exists(CLICKHOUSE_BUILD_PATH):
            os.makedirs(CLICKHOUSE_BUILD_PATH)

        cmake_args = [
            # Only clang is supported upstream
            f'-DCMAKE_C_COMPILER={COMPILER_CC}',
            f'-DCMAKE_CXX_COMPILER={COMPILER_CXX}',
            '-DENABLE_SIMDJSON=ON',

            # -fPIC: necessary for building a dynamic library
            # -fvisibility=hidden: Reduces the size of the final library by allowing the compiler to not export many
            #                     symbols from CH (in the final library)
            f'-DCMAKE_C_FLAGS=-fPIC -fvisibility=hidden{" -march=x86-64-v3 -mtune=generic" if platform.machine() in ("x86_64", "AMD64") else ""}{" -fsanitize=address" if ASAN_ENABLED else ""}{" -fsanitize=undefined" if UBSAN_ENABLED else ""}{" -fsanitize=memory" if MSAN_ENABLED else ""}{" -fsanitize=thread" if TSAN_ENABLED else ""}',
            f'-DCMAKE_CXX_FLAGS=-fPIC -fvisibility=hidden{" -march=x86-64-v3 -mtune=generic" if platform.machine() in ("x86_64", "AMD64") else ""}{" -fsanitize=address" if ASAN_ENABLED else ""}{" -fsanitize=undefined" if UBSAN_ENABLED else ""}{" -fsanitize=memory" if MSAN_ENABLED else ""}{" -fsanitize=thread" if TSAN_ENABLED else ""}',
            '-DCMAKE_ASM_FLAGS_INIT=-fPIC -fvisibility=hidden',

            '-DENABLE_TESTS=FALSE',
            '-DWERROR=0',
            '-Wno-dev',

            # Lots of issues when building several extensions
            # This means that we go from manylinux1 to manylinux2014 because of aligned_alloc
            # But for now I think it's ok since 2014 can be considered old enough and the fallback exist
            # It should be possible to go back to manylinux1 by providing that symbol, but life is hard enough already
            '-DENABLE_JEMALLOC=FALSE',

            # Build things using system libraries. This is a PITA because it will include refs to them
            # but if we don't then we'll see random crashes depending on the load order or the position of the moon
            # with respect to Saturn
            '-DGLIBC_COMPATIBILITY=FALSE',
            '-DDISABLE_HERMETIC_BUILD=TRUE',

            # Unwind with external code leads to crashes
            '-DUSE_UNWIND=FALSE',

            # x86-specific SIMD: AVX2/BMI2 set the runtime floor to x86-64-v3
            # (Haswell / Zen 1, ~2013+), matching the -march=x86-64-v3 flag above.
            # AVX-512 deliberately not enabled — AMD EPYC Milan in our fleet lacks it.
            *([
                '-DENABLE_SSE42=TRUE',
                '-DENABLE_SSSE3=TRUE',
                '-DENABLE_AVX=TRUE',
                '-DENABLE_AVX2=TRUE',
                '-DENABLE_BMI=TRUE',
                '-DENABLE_BMI2=TRUE',
                '-DNO_SSE3_OR_HIGHER=FALSE',
            ] if platform.machine() in ('x86_64', 'AMD64') else []),
            # ARM: keep the conservative ARMv8.0+crc profile. CI on ARM fails
            # against ClickHouse's modern ARMv8.2-a profile.
            *([
                '-DNO_ARMV81_OR_HIGHER=TRUE',
            ] if platform.machine() == 'aarch64' else []),
            '-DENABLE_EMBEDDED_COMPILER=FALSE',
            '-DENABLE_THINLTO=TRUE',

            # Removing libs that don't offer us anything since we manage function registration ourselves
            '-DENABLE_LIBRARIES=FALSE',
            '-DENABLE_GWP_ASAN=FALSE',
            '-DENABLE_RUST=FALSE',
            '-DENABLE_SSL=FALSE',
            '-DENABLE_SSH=FALSE',
            '-DENABLE_DATASKETCHES=TRUE',  # We need it for some agg validations

            '-DENABLE_CLICKHOUSE_ALL=FALSE',
            '-DENABLE_MULTITARGET_CODE=TRUE',

            # Force Ninja as the generator as we parse its output to build the python module
            '-G',
            'Ninja'
        ]

        # Build libclickhouse_aggregate_functions.a with MinSize to reduce the final size of the library
        # as we don't really care about performance of this part
        subprocess.check_call([cmake_cmd, CLICKHOUSE_PATH] + cmake_args + ['-DCMAKE_BUILD_TYPE=MinSizeRel'],
                              cwd=CLICKHOUSE_BUILD_PATH)
        subprocess.check_call([cmake_cmd, '--build', CLICKHOUSE_BUILD_PATH] +
                              ['--config', 'Release',
                               '--target', 'src/AggregateFunctions/libclickhouse_aggregate_functions.a'])

        # Functions for TTL validation, also with MinSize as performance is not a concern.
        # This library is linked with --whole-archive/-force_load (see extra_libs) so that
        # its REGISTER_FUNCTION static registrars run and DB::registerFunctions() can
        # register all of them without listing them one by one.
        subprocess.check_call([cmake_cmd, '--build', CLICKHOUSE_BUILD_PATH] +
                              ['--config', 'Release',
                               '--target', 'src/Functions/libclickhouse_ttl_functions.a'])

        # Now build with Release just the parser, which is where we want speed
        subprocess.check_call([cmake_cmd, CLICKHOUSE_PATH] + cmake_args + ['-DCMAKE_BUILD_TYPE=Release'],
                              cwd=CLICKHOUSE_BUILD_PATH)
        subprocess.check_call([cmake_cmd, '--build', CLICKHOUSE_BUILD_PATH] +
                              ['--target', 'src/Parsers/libclickhouse_parsers.a'])


# Note that we need to discard not existing paths for libraries
# since we don't build the whole project
def transform_path(lib):
    if lib.startswith(CLICKHOUSE_BUILD_PATH):
        return lib if os.path.exists(lib) else ""

    subdirs = list(filter(lambda f: os.path.isdir(os.path.join(CLICKHOUSE_BUILD_PATH, f)),
                          os.listdir(CLICKHOUSE_BUILD_PATH)))

    # We need to replace things like src/Loggers/libloggers.a with its full path
    for subdir in subdirs:
        if lib.startswith(subdir):
            p = os.path.join(CLICKHOUSE_BUILD_PATH, lib)
            return p if os.path.exists(p) else ""
        if lib.startswith('-I' + subdir):
            return '-I' + os.path.join(CLICKHOUSE_BUILD_PATH, lib[2:])
        if lib.startswith('-L' + subdir):
            p = os.path.join(CLICKHOUSE_BUILD_PATH, lib[2:])
            return '-L' + p if os.path.exists(p) else ""
    return lib


class CustomBuildWithFromCH(build_ext):
    @staticmethod
    def ninja_extractor_ldflags(what):
        ninja_path = os.path.join(CLICKHOUSE_BUILD_PATH, "build.ninja")
        task = subprocess.Popen(
            [f'grep "build programs/clickhouse:" {ninja_path} -A 13'
             f' | grep {what}'], shell=True, stdout=subprocess.PIPE)
        return list(task.stdout.read().decode('utf-8').split())[2:]

    @staticmethod
    def ninja_extractor_other(which):
        ninja_path = os.path.join(CLICKHOUSE_BUILD_PATH, "build.ninja")
        task = subprocess.Popen(
            ['grep "build src/CMakeFiles/dbms.dir/AggregateFunctions/AggregateFunctionCount.cpp.o" '
             f'{ninja_path} -A 9 | grep {which}'], shell=True,
            stdout=subprocess.PIPE)
        return list(task.stdout.read().decode('utf-8').split())[2:]

    @staticmethod
    def cflags():
        cflags_list = CustomBuildWithFromCH.ninja_extractor_other('FLAGS')
        include_list = list(map(transform_path, CustomBuildWithFromCH.ninja_extractor_other('INCLUDES')))
        # Replace -I with -isystem: these are external headers and we don't want to see warnings from them
        include_list = [flag.replace('-I', '-isystem', 1) if flag.startswith('-I') else flag for flag in include_list]
        # Remove -W flags, set our own warnings
        cflags_list = [flag for flag in cflags_list if not flag.startswith('-W')]
        other_list = CLANG_WARNINGS.copy()
        other_list += ['-Werror']  # Treat warnings as errors

        if BUILD_FOR_VALGRIND:
            other_list += ['-g', '-gdwarf-4']
        elif DEBUG_SYMBOLS:
            other_list += ['-g']

        # Sanitizer flags
        if ASAN_ENABLED:
            other_list += ['-fsanitize=address', '-fno-omit-frame-pointer', '-g']
        if UBSAN_ENABLED:
            other_list += ['-fsanitize=undefined', '-fno-omit-frame-pointer', '-g']
        if MSAN_ENABLED:
            other_list += ['-fsanitize=memory', '-fno-omit-frame-pointer', '-g']
        if TSAN_ENABLED:
            other_list += ['-fsanitize=thread', '-fno-omit-frame-pointer', '-g']

        if THINLTO_FLAG not in cflags_list:
            other_list += [THINLTO_FLAG]

        other_list += ['-DUSE_SIMDJSON=1']
        other_list += ['-DSIMDJSON_THREADS_ENABLED=1']
        
        if SIMDJSON_DEBUG:
            other_list += ['-DSIMDJSON_DEVELOPMENT_CHECKS=1']

        flags = cflags_list + include_list + other_list
        return " ".join(flags)

    @staticmethod
    def ldflags():
        link_flags = CustomBuildWithFromCH.ninja_extractor_ldflags('LINK_FLAGS')
        if sys.platform == 'linux':
            link_flags.append('-g' if BUILD_FOR_VALGRIND or DEBUG_SYMBOLS else '-s')
            link_flags.append('-Wl,--whole-archive')

        if THINLTO_FLAG not in link_flags:
            link_flags.append(THINLTO_FLAG)

        # Remove some noise from CH link flags:
        link_flags += ['-Wno-unused-command-line-argument']

        # Sanitizer linking flags
        if ASAN_ENABLED:
            link_flags += ['-fsanitize=address']
        if UBSAN_ENABLED:
            link_flags += ['-fsanitize=undefined']
        if MSAN_ENABLED:
            link_flags += ['-fsanitize=memory']
        if TSAN_ENABLED:
            link_flags += ['-fsanitize=thread']

        # Remove -Wl,--no-undefined since Python symbols will undefined
        link_flags = filter(lambda flag: flag.find('--no-undefined') == -1, link_flags)
        if sys.platform == 'darwin':
            # -undefined dynamic_lookup (added in extra_libs) already permits all undefined
            # symbols, so an explicit -Wl,-U,<symbol> is redundant and makes ld emit a warning.
            link_flags = filter(lambda flag: not flag.startswith('-Wl,-U,'), link_flags)
        return " ".join(link_flags)

    @staticmethod
    def extra_libs():
        ch_libs = [f"{TOOLSET_BUILD_PATH}/{f}"
                   for f in listdir(TOOLSET_BUILD_PATH)
                   if isfile(join(TOOLSET_BUILD_PATH, f)) and f.endswith(".a")]
        ch_libs += CustomBuildWithFromCH.ninja_extractor_ldflags('LINK_LIBRARIES')
        ch_libs = map(transform_path, ch_libs)
        # Several changes:
        # - Remove whole-archive directives as we want our own (more restrictive for less data)
        # - Remove libmath to remove deps on GLIBC
        # - Remove
        # No longer needed:
        # - Don't add src/libclickhouse_new_delete.a since it ends up crashing things
        # - Remove .o. These files only contain function declaration and we don't need them
        ch_libs = list(filter(lambda lib: lib and lib.find('whole-archive') == -1 and lib.find('-lm') == -1, ch_libs))

        # Force-load the TTL validation functions so their REGISTER_FUNCTION static
        # registrars run even though nothing references their symbols directly.
        # DB::registerFunctions() (called from ValidateTTL.cpp) registers all of them.
        ttl_functions_lib = os.path.join(CLICKHOUSE_BUILD_PATH, 'src/Functions/libclickhouse_ttl_functions.a')
        if sys.platform == 'darwin':
            ch_libs = [f'-Wl,-force_load,{ttl_functions_lib}'] + ch_libs
        else:
            ch_libs = ['-Wl,--whole-archive', ttl_functions_lib, '-Wl,--no-whole-archive'] + ch_libs

        if sys.platform == 'linux':
            ch_libs = ['-Wl,--no-whole-archive'] + ch_libs

        if sys.platform == 'darwin':
            # Needed so it doesn't complain about the missing Python functions (which is expected)
            ch_libs = ch_libs + ['-Wl,-undefined,dynamic_lookup']
        return ch_libs

    def build_extensions(self):
        self.run_command('clickhouse')
        self.run_command('toolset')

        compiler = getattr(self.compiler, "compiler_so")
        if sys.platform == 'darwin':
            # Fix for problem in Apple Silicon Mac with Python 3.11
            # both -arch arm64 and -arch x86_64 are included and this collides with
            # other -march option from cflags() (generated by Ninja)
            if 'x86_64' in compiler and 'arm64' in compiler:
                intel_pos = compiler.index('x86_64')
                if compiler[intel_pos - 1] == '-arch':
                    compiler.pop(intel_pos - 1)  # remove '-arch'
                    compiler.pop(intel_pos - 1)  # remove 'x86_64'

            compiler[0] = COMPILER_CC
            compiler += split_quoted(self.cflags())
            if DEBUG_SYMBOLS:
                compiler += ['-g']
        else:
            # Remove all external flags
            compiler = [COMPILER_CC] + split_quoted(self.cflags())

        linker = getattr(self.compiler, "linker_so_cxx")
        linker = [COMPILER_CC] + split_quoted(self.ldflags()) + linker[1:]

        compiler += ['-I', TOOLSET_PATH]
        # Make include_dirs (Python headers; set by setuptools) to -isystem: prevents warnings from Python headers
        for d in self.include_dirs or []:
            compiler += ['-isystem', d]
        self.include_dirs = []

        self.compiler.set_executable("compiler_so", compiler)
        self.compiler.set_executable("compiler_so_cxx", compiler)
        self.compiler.set_executable("compiler", compiler)
        self.compiler.set_executable("compiler_cxx", compiler)
        self.compiler.set_executable("linker_so_cxx", linker)

        build_ext.build_extensions(self)

    def build_extension(self, ext):
        ext.extra_link_args += self.extra_libs()
        build_ext.build_extension(self, ext)


class ToolsetBuildWithFromCH(CustomBuildWithFromCH):
    def run(self):

        cmake_cmd = os.environ.get('CMAKE_BIN', 'cmake')
        try:
            subprocess.check_output([cmake_cmd, '--version'])
        except OSError:
            raise RuntimeError(
                'CMake must be installed to build the following extensions: ' +
                ', '.join(e.name for e in self.extensions))

        if not os.path.exists(TOOLSET_BUILD_PATH):
            os.makedirs(TOOLSET_BUILD_PATH)

        cmake_args = [
            f'-DCMAKE_C_COMPILER={COMPILER_CC}',
            f'-DCMAKE_CXX_COMPILER={COMPILER_CXX}',
            f'-DCMAKE_CXX_FLAGS={self.cflags()}',
            '-G',
            'Ninja']

        subprocess.check_call([cmake_cmd, TOOLSET_PATH] + cmake_args,
                              cwd=TOOLSET_BUILD_PATH)

        build_args = ['--config', 'Release']
        subprocess.check_call([cmake_cmd, '--build', TOOLSET_BUILD_PATH] + build_args)


def requirements_from_file(path):
    return [
        line.strip()
        for line in Path(path).read_text().split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]
