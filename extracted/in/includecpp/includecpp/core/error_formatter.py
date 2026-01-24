"""Enhanced error formatting for IncludeCPP build system.

Provides user-friendly error messages with context and suggestions.
Error messages are always printed LAST so users who only read the end still see the fix.
"""

from typing import List, Optional, Dict
import re
import sys

from .error_catalog import ERROR_CATALOG, get_error_message, format_error_box, format_unknown_error


def _supports_unicode():
    """Check if terminal supports Unicode output."""
    if sys.platform == 'win32':
        try:
            '✓✗❌→←'.encode(sys.stdout.encoding or 'utf-8')
            return True
        except (UnicodeEncodeError, LookupError, AttributeError):
            return False
    return True


_UNICODE_OK = _supports_unicode()

# Box drawing characters with ASCII fallbacks
BOX_TL = '╔' if _UNICODE_OK else '+'
BOX_TR = '╗' if _UNICODE_OK else '+'
BOX_BL = '╚' if _UNICODE_OK else '+'
BOX_BR = '╝' if _UNICODE_OK else '+'
BOX_H = '═' if _UNICODE_OK else '='
BOX_V = '║' if _UNICODE_OK else '|'
BULLET = '•' if _UNICODE_OK else '*'
ARROW = '→' if _UNICODE_OK else '->'
DBLARROW = '↔' if _UNICODE_OK else '<->'
CHECK = '✓' if _UNICODE_OK else '[OK]'
CROSS = '✗' if _UNICODE_OK else '[X]'
ERR_CROSS = '❌' if _UNICODE_OK else '[X]'


class BuildErrorFormatter:
    """Format C++ compilation errors with context and suggestions."""

    @staticmethod
    def format_type_mismatch(expected: str, got: str, location: str) -> str:
        """Format type mismatch error with suggestions.

        Args:
            expected: Expected type string
            got: Actual type string
            location: Location of error (file:line)

        Returns:
            Formatted error message with suggestions
        """
        h_line = BOX_H * 62
        return f"""
{BOX_TL}{h_line}{BOX_TR}
{BOX_V} TYPE MISMATCH ERROR                                          {BOX_V}
{BOX_BL}{h_line}{BOX_BR}

Location: {location}

Expected: {expected}
Got:      {got}

Suggestions:
  {BULLET} Check if you're passing the correct type
  {BULLET} For struct {ARROW} dict: use struct_instance.to_dict()
  {BULLET} For dict {ARROW} struct: use StructName.from_dict(dict_instance)
  {BULLET} For vector conversions: Python list {DBLARROW} std::vector is automatic

Type Conversion Examples:
  # Struct to dict
  point_dict = point.to_dict()

  # Dict to struct
  point = Point.from_dict({{"x": 10, "y": 20}})

  # Vector of structs
  points: List[Point] = [...]  # Automatically converts
"""

    @staticmethod
    def format_dependency_error(module: str, missing_dep: str) -> str:
        """Format missing dependency error.

        Args:
            module: Module name that has missing dependency
            missing_dep: Name of missing dependency module

        Returns:
            Formatted error message with fix instructions
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ DEPENDENCY ERROR                                             ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
Missing Dependency: {missing_dep}

To Fix:
  1. Add dependency to {module}.cp:

     SOURCE(path/to/{module}.cpp) {module}
     DEPENDS({missing_dep})
     PUBLIC(
         ...
     )

  2. Ensure {missing_dep} module exists in plugins/ directory

  3. Rebuild:
     python -m includecpp rebuild --verbose

Dependency Chain:
  {{module}} {ARROW} {{missing_dep}}
"""

    @staticmethod
    def format_circular_dependency(cycle: List[str]) -> str:
        """Format circular dependency error.

        Args:
            cycle: List of module names forming the cycle

        Returns:
            Formatted error message with refactoring suggestions
        """
        cycle_display = f" {ARROW} ".join(cycle + [cycle[0]])
        h_line = BOX_H * 62
        return f"""
{BOX_TL}{h_line}{BOX_TR}
{BOX_V} CIRCULAR DEPENDENCY DETECTED                                 {BOX_V}
{BOX_BL}{h_line}{BOX_BR}

Dependency Cycle:
  {cycle_display}

To Fix:
  {BULLET} Refactor modules to remove circular dependency
  {BULLET} Use forward declarations where possible
  {BULLET} Consider merging modules if they're tightly coupled
  {BULLET} Create a third module for shared types

Example Refactoring:
  Before:
    module_a {ARROW} module_b {ARROW} module_a  {ERR_CROSS}

  After:
    module_a {ARROW} shared_types
    module_b {ARROW} shared_types         {CHECK}
"""

    @staticmethod
    def format_module_not_found(module: str, available: List[str]) -> str:
        """Format module not found error.

        Args:
            module: Requested module name
            available: List of available module names

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ MODULE NOT FOUND                                             ║
╚══════════════════════════════════════════════════════════════╝

Requested: {module}

Available modules:
  {', '.join(available) if available else '(none)'}

To Fix:
  • Check spelling of module name
  • Ensure {module}.cp exists in plugins/ directory
  • Run 'python -m includecpp rebuild' to build all modules
  • Run 'python -m includecpp list' to see available modules
"""

    @staticmethod
    def format_build_failed(module: str, reason: str) -> str:
        """Format general build failure error.

        Args:
            module: Module name that failed to build
            reason: Reason for failure

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ BUILD FAILED                                                 ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}

Reason:
  {reason}

To Debug:
  • Run with --verbose flag for detailed output
  • Check {module}.cpp for syntax errors
  • Verify all includes are available
  • Check build log in AppData/IncludeCPP/
"""

    @staticmethod
    def parse_compiler_error(stderr: str, module_name: str) -> str:
        """Parse C++ compiler errors and add helpful context.

        Args:
            stderr: Standard error output from compiler
            module_name: Name of module being compiled

        Returns:
            Formatted error messages with context
        """
        lines = stderr.split('\n')
        formatted = []
        error_count = 0

        for line in lines:
            # GCC/Clang format: file:line:col: error: message
            if ': error:' in line:
                error_count += 1
                parts = line.split(':')

                if len(parts) >= 4:
                    file_path = parts[0].strip()
                    line_num = parts[1].strip() if parts[1].strip().isdigit() else "?"
                    error_msg = ':'.join(parts[3:]).strip()

                    formatted.append("")
                    formatted.append("╔══════════════════════════════════════════╗")
                    formatted.append("║ COMPILATION ERROR                        ║")
                    formatted.append("╚══════════════════════════════════════════╝")
                    formatted.append("")
                    formatted.append(f"Module: {module_name}")
                    formatted.append(f"File: {file_path}")
                    formatted.append(f"Line: {line_num}")
                    formatted.append(f"Error: {error_msg}")
                    formatted.append("")

                    # Add context based on error type
                    if "undefined reference" in error_msg.lower() or "unresolved external" in error_msg.lower():
                        formatted.append("Suggestion:")
                        formatted.append("  • Check if function/class is declared in header")
                        formatted.append("  • Verify all source files are listed in .cp file")
                        formatted.append("  • Check for missing DEPENDS() if using types from other modules")
                        formatted.append("  • Ensure function is in 'includecpp' namespace")

                    elif "no matching function" in error_msg.lower() or "no member named" in error_msg.lower():
                        formatted.append("Suggestion:")
                        formatted.append("  • Check parameter types match function signature")
                        formatted.append("  • Verify template instantiations are correct")
                        formatted.append("  • Check for const/reference qualifiers")
                        formatted.append("  • Ensure all required headers are included")

                    elif "expected" in error_msg.lower() and "before" in error_msg.lower():
                        formatted.append("Suggestion:")
                        formatted.append("  • Check for missing semicolons")
                        formatted.append("  • Verify bracket/parenthesis matching")
                        formatted.append("  • Check for typos in type names")

                    elif "does not name a type" in error_msg.lower():
                        formatted.append("Suggestion:")
                        formatted.append("  • Check if type is defined before use")
                        formatted.append("  • Verify #include statements are correct")
                        formatted.append("  • Check namespace qualifications (std::, includecpp::)")

                    elif "incomplete type" in error_msg.lower():
                        formatted.append("Suggestion:")
                        formatted.append("  • Add forward declaration or full type definition")
                        formatted.append("  • Check if header file is included")
                        formatted.append("  • Verify struct/class definition is complete")

            # MSVC format: file(line): error C####: message
            elif re.match(r'.*\(\d+\):\s*error\s+C\d+:', line):
                error_count += 1
                match = re.match(r'(.*)\((\d+)\):\s*error\s+C\d+:\s*(.*)', line)
                if match:
                    file_path = match.group(1).strip()
                    line_num = match.group(2)
                    error_msg = match.group(3).strip()

                    formatted.append("")
                    formatted.append("╔══════════════════════════════════════════╗")
                    formatted.append("║ COMPILATION ERROR                        ║")
                    formatted.append("╚══════════════════════════════════════════╝")
                    formatted.append("")
                    formatted.append(f"Module: {module_name}")
                    formatted.append(f"File: {file_path}")
                    formatted.append(f"Line: {line_num}")
                    formatted.append(f"Error: {error_msg}")
                    formatted.append("")

            # Warning lines - pass through but mark them
            elif ': warning:' in line or 'warning C' in line:
                if not formatted or formatted[-1] != "":
                    formatted.append("")
                formatted.append(f"⚠️  {line}")

            # Note lines
            elif ': note:' in line:
                formatted.append(f"ℹ️  {line}")

            # Empty lines
            elif not line.strip():
                if formatted and formatted[-1] != "":
                    formatted.append("")

        if error_count > 0:
            header = [
                "",
                "═" * 60,
                f"COMPILATION FAILED: {error_count} error(s) in {module_name}",
                "═" * 60,
                ""
            ]
            formatted = header + formatted

        return '\n'.join(formatted) if formatted else stderr

    @staticmethod
    def format_cmake_error(stderr: str, module_name: str) -> str:
        """Format CMake configuration errors.

        Args:
            stderr: CMake error output
            module_name: Name of module being configured

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ CMAKE CONFIGURATION ERROR                                    ║
╚══════════════════════════════════════════════════════════════╝

Module: {module_name}

CMake Output:
{stderr}

Common Issues:
  • CMake not installed or not in PATH
  • C++ compiler not found (install g++, clang++, or MSVC)
  • pybind11 not found (auto-installed, check network)
  • Python development headers missing

To Fix:
  • Install CMake 3.15+ from cmake.org
  • Install C++ compiler:
    - Windows: Visual Studio or MinGW
    - Linux: apt-get install g++ cmake python3-dev
    - macOS: xcode-select --install
  • Run with --verbose for detailed CMake output
"""

    @staticmethod
    def format_import_error(module: str, error_msg: str, pyd_path: str) -> str:
        """Format Python import errors for .pyd modules.

        Args:
            module: Module name
            error_msg: Import error message
            pyd_path: Path to .pyd file

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ MODULE IMPORT ERROR                                          ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
Path: {pyd_path}

Error:
  {error_msg}

Common Causes:
  • Missing dependencies (DLLs on Windows, .so on Linux)
  • Python version mismatch (rebuild for current Python)
  • Corrupted .pyd file (rebuild module)
  • Missing Visual C++ Redistributable (Windows)

To Fix:
  1. Rebuild module:
     python -m includecpp rebuild {module} --clean

  2. Check Python version matches build:
     python --version

  3. Windows: Install Visual C++ Redistributable
     https://aka.ms/vs/17/release/vc_redist.x64.exe

  4. Run with --verbose for detailed output
"""

    @staticmethod
    def format_namespace_error(module: str, source_file: str) -> str:
        """Format namespace error when includecpp namespace is missing.

        Args:
            module: Module name
            source_file: Path to source file

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ NAMESPACE ERROR                                              ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
Source: {source_file}

Problem:
  Your C++ code is not wrapped in the 'includecpp' namespace.
  IncludeCPP requires all exported code to be in this namespace.

Why this matters:
  The generated Python bindings expect functions/classes in the
  'includecpp' namespace. Without it, the compiler cannot find
  your code and you'll get "undefined reference" errors.

To Fix:
  Wrap your code in the namespace:

  // {source_file}
  #include <...>

  namespace includecpp {{

      // Your functions and classes here
      int my_function(int x) {{
          return x * 2;
      }}

      class MyClass {{
      public:
          void method() {{ ... }}
      }};

  }} // namespace includecpp

After fixing:
  python -m includecpp rebuild
"""

    @staticmethod
    def format_syntax_error(module: str, file: str, line: int, error: str) -> str:
        """Format C++ syntax error.

        Args:
            module: Module name
            file: Source file path
            line: Line number
            error: Error message

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ C++ SYNTAX ERROR                                             ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
File:   {file}
Line:   {line}

Error:
  {error}

Common Causes:
  • Missing semicolon (;) at end of statement
  • Unbalanced braces {{ }} or parentheses ( )
  • Missing #include directive
  • Typo in keyword or identifier
  • Wrong order of template/class declaration

How to Debug:
  1. Open {file} at line {line}
  2. Check the line and lines immediately before it
  3. Look for missing ; or }}
  4. Verify all includes are correct

After fixing:
  python -m includecpp rebuild --verbose
"""

    @staticmethod
    def format_linker_error(module: str, undefined_symbol: str, hint: str = "") -> str:
        """Format linker error for undefined references.

        Args:
            module: Module name
            undefined_symbol: The undefined symbol
            hint: Optional hint about cause

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ LINKER ERROR - UNDEFINED REFERENCE                           ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
Missing Symbol: {undefined_symbol}
{f"Hint: {hint}" if hint else ""}

What this means:
  The linker cannot find the implementation of '{undefined_symbol}'.
  The symbol is declared (perhaps in a header) but not defined.

Common Causes:
  • Function declared but not implemented
  • Typo in function/class name
  • Missing namespace qualifier (forgot 'includecpp::')
  • Missing source file in .cp configuration
  • Template function defined in .cpp instead of header

To Fix:
  1. Check if '{undefined_symbol}' is fully implemented
  2. Verify the function is in 'namespace includecpp'
  3. For templates: move implementation to header file
  4. Check your .cp file includes all necessary sources:

     SOURCE(path/to/all_sources.cpp) {module}

  5. If using multiple files:

     SOURCES(file1.cpp, file2.cpp)
     HEADER(headers.h) {module}

After fixing:
  python -m includecpp rebuild --clean
"""

    @staticmethod
    def format_missing_include_error(module: str, missing_header: str, file: str) -> str:
        """Format missing include error.

        Args:
            module: Module name
            missing_header: The missing header file
            file: Source file that needs the include

        Returns:
            Formatted error message
        """
        common_headers = {
            'string': '#include <string>',
            'vector': '#include <vector>',
            'map': '#include <map>',
            'iostream': '#include <iostream>',
            'cmath': '#include <cmath>',
            'memory': '#include <memory>',
            'algorithm': '#include <algorithm>',
            'functional': '#include <functional>',
        }

        suggestion = common_headers.get(missing_header.lower(), f'#include <{missing_header}>')

        return f"""
╔══════════════════════════════════════════════════════════════╗
║ MISSING INCLUDE ERROR                                        ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
File:   {file}
Missing: {missing_header}

To Fix:
  Add at the top of {file}:

    {suggestion}

Common Standard Library Headers:
  #include <string>     // std::string
  #include <vector>     // std::vector
  #include <map>        // std::map, std::unordered_map
  #include <memory>     // std::unique_ptr, std::shared_ptr
  #include <algorithm>  // std::sort, std::find, etc.
  #include <cmath>      // Mathematical functions
  #include <iostream>   // std::cout, std::cin

After fixing:
  python -m includecpp rebuild
"""

    @staticmethod
    def format_generic_build_error(module: str, stage: str, error: str) -> str:
        """Format a generic build error with helpful context.

        Args:
            module: Module name
            stage: Build stage (compile, link, etc.)
            error: Error message

        Returns:
            Formatted error message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ BUILD ERROR                                                  ║
╚══════════════════════════════════════════════════════════════╝

Module: {module}
Stage:  {stage}

Error Details:
{error}

Troubleshooting Steps:
  1. Run with verbose output:
     python -m includecpp rebuild --verbose

  2. Check your C++ code for errors:
     - Syntax errors (missing ; or }})
     - Missing namespace includecpp {{ }}
     - Undefined functions or classes

  3. Verify your .cp configuration:
     - All source files listed
     - Correct module name
     - Valid DEPENDS() if using other modules

  4. Try a clean rebuild:
     python -m includecpp rebuild --clean

  5. Check compiler is installed:
     g++ --version   (Linux/macOS)
     cl              (Windows MSVC)

If the error persists:
  - Check the full error output above
  - Verify all #include statements are correct
  - Ensure no circular dependencies between modules
"""

    @staticmethod
    def format_bindings_error(module: str, bad_method: str, bad_class: str) -> str:
        """Format error in auto-generated bindings.cpp file.

        Args:
            module: Module name
            bad_method: The method/member that doesn't exist
            bad_class: The class that should have the method

        Returns:
            Formatted error message
        """
        specific_hint = ""
        if bad_method and bad_class:
            specific_hint = f"""
The generated bindings tried to bind '{bad_method}' as a method of '{bad_class}',
but '{bad_class}' doesn't have a member called '{bad_method}'.
"""

        return f"""
+======================================================================+
|  BUILD ERROR                                                         |
+======================================================================+
{specific_hint}
Try regenerating your .cp file:

  includecpp plugin {module if module else '<name>'}

This re-scans your C++ source files and updates the plugin definition.
Then run:

  includecpp rebuild
"""

    @staticmethod
    def format_redefinition_error(module: str, type_name: str, file1: str, file2: str) -> str:
        """Format redefinition/duplicate declaration error.

        Args:
            module: Module name
            type_name: Name of redefined type (class, struct, function)
            file1: First file where type is defined
            file2: Second file where type is redefined

        Returns:
            Formatted error message
        """
        return f"""
+======================================================================+
|  REDEFINITION ERROR - YOUR CODE HAS DUPLICATE DECLARATIONS          |
+======================================================================+

Module: {module}
Conflict: '{type_name}' is defined in multiple files

  File 1: {file1}
  File 2: {file2}

PROBLEM:
  You have the same class/struct/function defined twice.
  C++ does not allow multiple definitions of the same type.

THIS IS A USER CODE ERROR, NOT AN IncludeCPP BUG.

HOW TO FIX:
  Option 1: Remove the duplicate
    - Delete '{type_name}' from one of the files

  Option 2: Use different names
    - Rename one to '{type_name}2' or a more descriptive name

  Option 3: Share the type
    - Put '{type_name}' in a common header file
    - Include that header in both modules
    - Use DEPENDS() in .cp files to share types

  Option 4: Use namespaces
    - Put each in a different sub-namespace:
      namespace includecpp::module1 {{ class {type_name} {{ }}; }}
      namespace includecpp::module2 {{ class {type_name} {{ }}; }}

After fixing:
  python -m includecpp rebuild --clean
"""

    @staticmethod
    def get_final_message(stderr: str, module_name: str = "") -> str:
        """Get the final helpful message to print LAST.

        This is the short, actionable message that lazy users will see.
        Always call this and print it as the last line of output.

        Args:
            stderr: Standard error output
            module_name: Name of module

        Returns:
            Short, helpful message for the end of output
        """
        context = {"module": module_name} if module_name else None
        msg = get_error_message(stderr, context)
        if msg:
            return msg
        return format_unknown_error(stderr)

    @staticmethod
    def analyze_error(stderr: str, module_name: str = "") -> str:
        """Analyze stderr and return appropriate formatted error.

        Args:
            stderr: Standard error output from build
            module_name: Name of module being built

        Returns:
            Formatted error message with hints
        """
        # First try the error catalog for quick matching
        context = {"module": module_name} if module_name else None
        catalog_msg = get_error_message(stderr, context)
        if catalog_msg:
            return format_error_box(catalog_msg, "BUILD ERROR")

        stderr_lower = stderr.lower()

        redef_match = re.search(r"redefinition of ['\"]?(?:class |struct |)?([^'\"]+)['\"]?", stderr)
        if redef_match:
            type_name = redef_match.group(1).strip()
            # Try to find the two file locations
            file_matches = re.findall(r"([^\s:]+\.[ch](?:pp)?):(\d+)", stderr)
            file1 = file_matches[0][0] if len(file_matches) > 0 else "unknown"
            file2 = file_matches[1][0] if len(file_matches) > 1 else "unknown"
            return BuildErrorFormatter.format_redefinition_error(module_name, type_name, file1, file2)

        # Check for namespace error
        if 'namespace includecpp' in stderr or 'using namespace includecpp' in stderr:
            if 'undefined' in stderr_lower or 'not found' in stderr_lower:
                return BuildErrorFormatter.format_namespace_error(module_name, "your source file")

        # Check for undefined reference (linker error)
        undefined_match = re.search(r"undefined reference to ['\"]?([^'\"]+)['\"]?", stderr)
        if undefined_match:
            symbol = undefined_match.group(1)
            hint = ""
            if '::' in symbol and 'includecpp' not in symbol:
                hint = "Symbol is not in 'includecpp' namespace"
            return BuildErrorFormatter.format_linker_error(module_name, symbol, hint)

        # Check for missing include
        include_match = re.search(r"fatal error: ([^:]+): No such file", stderr)
        if not include_match:
            include_match = re.search(r"cannot open include file[:\s]+['\"]?([^'\"]+)['\"]?", stderr, re.IGNORECASE)
        if include_match:
            missing = include_match.group(1).strip()
            return BuildErrorFormatter.format_missing_include_error(module_name, missing, "your source file")

        if 'bindings.cpp' in stderr or 'bindings\\bindings.cpp' in stderr:
            # Extract what's wrong (e.g., "'Vector2D' is not a member of 'Circle'")
            member_error = re.search(r"'(\w+)' is not a member of '([^']+)'", stderr)
            if member_error:
                bad_method = member_error.group(1)
                bad_class = member_error.group(2).split('::')[-1]
                return BuildErrorFormatter.format_bindings_error(module_name, bad_method, bad_class)

        # Check for syntax error with line number
        syntax_match = re.search(r"([^:]+):(\d+):\d*:?\s*error:\s*(.+)", stderr)
        if syntax_match:
            file = syntax_match.group(1)
            line = int(syntax_match.group(2))
            error = syntax_match.group(3)
            # Skip if it's bindings.cpp - already handled above
            if 'bindings.cpp' in file:
                return BuildErrorFormatter.format_bindings_error(module_name, "", "")
            return BuildErrorFormatter.format_syntax_error(module_name, file, line, error)

        # Check for circular dependency
        if 'circular' in stderr_lower and 'dependency' in stderr_lower:
            cycle_match = re.findall(r'\b([a-zA-Z_]\w*)\b', stderr)
            if cycle_match:
                return BuildErrorFormatter.format_circular_dependency(list(set(cycle_match[:5])))

        # Check for missing dependency
        dep_match = re.search(r"depends on unknown module[:\s]+['\"]?(\w+)['\"]?", stderr, re.IGNORECASE)
        if dep_match:
            missing_dep = dep_match.group(1)
            return BuildErrorFormatter.format_dependency_error(module_name, missing_dep)

        # Default: generic build error
        return BuildErrorFormatter.format_generic_build_error(module_name, "build", stderr)


class BuildSuccessFormatter:
    """Format build success messages with professional styling."""

    @staticmethod
    def format_build_success(modules: List[str], build_time: float, stats: dict = None) -> str:
        """Format successful build completion message.

        Args:
            modules: List of successfully built modules
            build_time: Total build time in seconds
            stats: Optional build statistics dict

        Returns:
            Formatted success message
        """
        module_count = len(modules)
        module_list = "\n  ".join(f"{m}" for m in modules) if modules else "  (no modules)"

        stats_section = ""
        if stats:
            stats_lines = []
            if 'total_functions' in stats:
                stats_lines.append(f"  Functions exported: {stats['total_functions']}")
            if 'total_classes' in stats:
                stats_lines.append(f"  Classes exported:   {stats['total_classes']}")
            if 'total_structs' in stats:
                stats_lines.append(f"  Structs exported:   {stats['total_structs']}")
            if stats_lines:
                stats_section = "\n" + "\n".join(stats_lines)

        return f"""
╔══════════════════════════════════════════════════════════════╗
║ BUILD SUCCESSFUL                                              ║
╚══════════════════════════════════════════════════════════════╝

Modules built ({module_count}):
  {module_list}

Build time: {build_time:.2f}s{stats_section}

Usage:
  from includecpp import CppApi
  api = CppApi()
  module = api.include("<module_name>")
"""

    @staticmethod
    def format_module_compile_start(module: str) -> str:
        """Format module compilation start message.

        Args:
            module: Module name

        Returns:
            Formatted start message
        """
        return f"┌─ Building: {module}"

    @staticmethod
    def format_module_compile_success(module: str, time_seconds: float) -> str:
        """Format module compilation success message.

        Args:
            module: Module name
            time_seconds: Compilation time

        Returns:
            Formatted success message
        """
        return f"└─ {module} ({time_seconds:.2f}s)"

    @staticmethod
    def format_module_compile_failed(module: str, error_summary: str) -> str:
        """Format module compilation failure message.

        Args:
            module: Module name
            error_summary: Brief error summary

        Returns:
            Formatted failure message
        """
        return f"└─ ✗ {module}: {error_summary}"

    @staticmethod
    def format_build_start(modules: List[str], incremental: bool = False) -> str:
        """Format build start message.

        Args:
            modules: List of modules to build
            incremental: Whether this is an incremental build

        Returns:
            Formatted start message
        """
        build_type = "Incremental" if incremental else "Full"
        module_count = len(modules) if modules else "all"

        return f"""
╔══════════════════════════════════════════════════════════════╗
║ IncludeCPP {build_type} Build
╚══════════════════════════════════════════════════════════════╝
Modules: {module_count}
"""

    @staticmethod
    def format_build_failed(failed_modules: List[str], succeeded_modules: List[str]) -> str:
        """Format build failure summary.

        Args:
            failed_modules: List of modules that failed
            succeeded_modules: List of modules that succeeded

        Returns:
            Formatted failure message
        """
        failed_list = "\n  ".join(f"✗ {m}" for m in failed_modules)
        succeeded_list = "\n  ".join(f"{m}" for m in succeeded_modules) if succeeded_modules else "  (none)"

        return f"""
╔══════════════════════════════════════════════════════════════╗
║ ✗ BUILD FAILED                                               ║
╚══════════════════════════════════════════════════════════════╝

Failed ({len(failed_modules)}):
  {failed_list}

Succeeded ({len(succeeded_modules)}):
  {succeeded_list}

To fix:
  • Check the error messages above
  • Run with --verbose for more details
  • Fix errors and run: python -m includecpp rebuild
"""

    @staticmethod
    def format_up_to_date(modules: List[str]) -> str:
        """Format message when all modules are up to date.

        Args:
            modules: List of up-to-date modules

        Returns:
            Formatted message
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ ALL MODULES UP TO DATE                                        ║
╚══════════════════════════════════════════════════════════════╝

{len(modules)} module(s) already built and unchanged.
Use --clean to force a full rebuild.
"""

    @staticmethod
    def format_clean_success(cleaned_items: List[str]) -> str:
        """Format successful clean operation message.

        Args:
            cleaned_items: List of cleaned items/modules

        Returns:
            Formatted message
        """
        items = "\n  ".join(f"• {item}" for item in cleaned_items) if cleaned_items else "  (nothing to clean)"
        return f"""
╔══════════════════════════════════════════════════════════════╗
║ CLEAN COMPLETE                                                ║
╚══════════════════════════════════════════════════════════════╝

Cleaned:
  {items}
"""
