"""Error catalog for IncludeCPP - 130 error patterns with direct, helpful messages.

Messages are written like a dev explaining to another dev. No corporate fluff.
Always printed LAST so users who only read the end still get the fix.
"""

import re
from typing import Optional, Dict, Tuple

# Error catalog: pattern -> (message, category)
# Categories: beginner, compiler, linker, cmake, pybind11, runtime, plugin, import
ERROR_CATALOG = {
    # ========== PRIORITY: FILE LOCK ERRORS (checked FIRST) ==========
    # These must be at the top to catch file-locked errors before other patterns match
    "FILE_LOCKED_WIN32": {
        "pattern": r"WinError 32|being used by another process|cannot access.*because.*used|process cannot access|PermissionError.*api\.pyd|Permission denied.*\.pyd",
        "message": "Module file is locked by another process!\n\nThis usually means:\n  - A compiled .exe using this module is still running\n  - Another Python script has imported this module\n  - Your IDE has the file open\n\nFix:\n  1. Close any running .exe that uses this module\n  2. Close Python REPL/scripts using this module\n  3. Restart your IDE if it imported the module\n  4. Then run 'includecpp rebuild' again",
        "category": "import"
    },
    "FILE_LOCKED_COPY": {
        "pattern": r"copy.*failed.*permission|cannot (copy|overwrite|write).*\.pyd|failed.*copy.*bindings",
        "message": "Cannot overwrite module file - it's locked!\n\nThe compiled .pyd/.so file is in use by another process.\n\nFix:\n  1. Close any running .exe that uses this module\n  2. Close all Python processes that imported this module\n  3. Run 'includecpp rebuild' again",
        "category": "import"
    },
    "FILE_LOCKED_LINKER": {
        "pattern": r"cannot open output file.*\.pyd|cannot open.*api\.pyd|ld\.exe:.*cannot open|ld\.exe:.*Permission denied|ld:.*cannot open output|error: unable to open output file|collect2.*ld.*Permission denied|LINK :.*cannot open.*\.pyd",
        "message": "Linker cannot write output file - it's locked!\n\nThe .pyd/.so file is being used by another process.\n\nFix:\n  1. Close any running .exe using this module\n  2. Close Python/IDE that imported this module\n  3. Run 'includecpp rebuild --clean'",
        "category": "linker"
    },
    "PERMISSION_DENIED_PYD": {
        "pattern": r"Permission denied.*\.pyd|Permission denied.*\.so|PermissionError.*bindings",
        "message": "Permission denied writing module file!\n\nThe .pyd/.so file is locked (probably by a running process).\n\nFix: Close any .exe or Python script using this module, then rebuild.",
        "category": "import"
    },
    # ========== A. BEGINNER MISTAKES (1-20) ==========
    "MODULE_NOT_BUILT": {
        "pattern": r"Module '(\w+)'.*not found|No module named '(\w+)'",
        "message": "Module '{name}' not built yet.\n\nFix: includecpp rebuild",
        "category": "beginner"
    },
    "MODULE_OUTDATED": {
        "pattern": r"Module '(\w+)'.*outdated|source.*changed",
        "message": "Module '{name}' outdated. Source changed since last build.\n\nFix: includecpp rebuild",
        "category": "beginner"
    },
    "NO_CPP_PROJ": {
        "pattern": r"cpp\.proj.*not found|No cpp\.proj",
        "message": "No cpp.proj found. Not an IncludeCPP project.\n\nFix: includecpp init",
        "category": "beginner"
    },
    "NO_PLUGINS_DIR": {
        "pattern": r"plugins.*directory.*not found|plugins/.*missing",
        "message": "plugins/ folder missing.\n\nFix: includecpp init",
        "category": "beginner"
    },
    "NO_INCLUDE_DIR": {
        "pattern": r"include.*directory.*not found|include/.*missing",
        "message": "include/ folder missing. Create it or check cpp.proj paths.",
        "category": "beginner"
    },
    "EMPTY_CP_FILE": {
        "pattern": r"\.cp.*is empty|empty plugin",
        "message": "Plugin file is empty. Add SOURCE() and PUBLIC() blocks.",
        "category": "beginner"
    },
    "NO_SOURCE_IN_CP": {
        "pattern": r"no SOURCE|SOURCE\(\).*missing|Missing SOURCE",
        "message": "No SOURCE() in .cp file.\n\nFix: Add SOURCE(file.cpp) module_name",
        "category": "beginner"
    },
    "NO_PUBLIC_IN_CP": {
        "pattern": r"no PUBLIC|PUBLIC\(\).*missing|nothing.*export",
        "message": "No PUBLIC() block. Nothing gets exported to Python.",
        "category": "beginner"
    },
    "NOT_IN_NAMESPACE": {
        "pattern": r"namespace includecpp|using namespace includecpp",
        "message": "Code not in 'namespace includecpp'.\n\nFix: Wrap your code:\nnamespace includecpp {\n    // your code here\n}",
        "category": "beginner"
    },
    "WRONG_INCLUDE_PATH": {
        "pattern": r"No such file.*['\"]([^'\"]+)['\"]|cannot find.*['\"]([^'\"]+)['\"]",
        "message": "Can't find '{file}'. Check path in SOURCE() matches actual file location.",
        "category": "beginner"
    },
    "FORGOT_HEADER": {
        "pattern": r"'(\w+)'.*was not declared|unknown type.*'(\w+)'|error:.*'(\w+)'.*undeclared",
        "message": "'{name}' not declared. Include header or check if it's a private/nested type.",
        "category": "beginner"
    },
    "PYTHON_SHADOWS_MODULE": {
        "pattern": r"shadows|already.*defined.*\.py",
        "message": "Python file shadows C++ module. Rename your .py script.",
        "category": "beginner"
    },
    "OLD_PYD_LOADED": {
        "pattern": r"old.*location|cached.*module|already loaded",
        "message": "Module loaded from old location. Restart Python.",
        "category": "beginner"
    },
    "EDITING_WRONG_FILE": {
        "pattern": r"source.*mismatch|wrong.*file",
        "message": "SOURCE() points to different file. Check your .cp configuration.",
        "category": "beginner"
    },
    "NO_COMPILER": {
        "pattern": r"No C\+\+ compiler|compiler.*not found|g\+\+.*not found|cl\.exe.*not found",
        "message": "No C++ compiler found.\n\nFix: Install g++ (MinGW/MSYS2) or Visual Studio",
        "category": "beginner"
    },
    "WRONG_PYTHON_VERSION": {
        "pattern": r"Python.*version.*mismatch|built.*Python\s*(\d+\.\d+).*running.*(\d+\.\d+)",
        "message": "Built with different Python version.\n\nFix: includecpp rebuild",
        "category": "beginner"
    },
    "MISSING_PYBIND11": {
        "pattern": r"pybind11.*not found|No module.*pybind11",
        "message": "pybind11 not found.\n\nFix: pip install pybind11",
        "category": "beginner"
    },
    "CIRCULAR_IMPORT": {
        "pattern": r"circular.*import|circular.*dependency|import cycle",
        "message": "Circular import detected.\n\nFix: Use DEPENDS() in one .cp file, not both",
        "category": "beginner"
    },
    "CLASS_NOT_IN_PUBLIC": {
        "pattern": r"class '(\w+)'.*not.*PUBLIC|'(\w+)'.*not exported",
        "message": "Class '{name}' exists but not in PUBLIC() block.\n\nFix: Add CLASS({name}) to PUBLIC()",
        "category": "beginner"
    },
    "METHOD_NOT_IN_CLASS": {
        "pattern": r"method '(\w+)'.*not.*listed|'(\w+)'.*not.*CLASS",
        "message": "Method not listed in CLASS block.\n\nFix: Add METHOD({name}) inside CLASS(){{ }}",
        "category": "beginner"
    },

    # ========== B. COMPILER ERRORS (21-45) ==========
    "UNDEFINED_REFERENCE": {
        "pattern": r"undefined reference to ['\"`]([^'\"`]+)['\"`]",
        "message": "'{symbol}' declared but not defined.\n\nFix: Add implementation or check spelling",
        "category": "compiler"
    },
    "NO_MATCHING_FUNCTION": {
        "pattern": r"no matching function.*call to ['\"`]([^'\"`]+)['\"`]",
        "message": "No matching function for '{func}'.\n\nFix: Check parameter types match declaration",
        "category": "compiler"
    },
    "EXPECTED_SEMICOLON": {
        "pattern": r"expected ['\"`];['\"`]|expected.*semicolon",
        "message": "Missing semicolon.\n\nFix: Add ';' at indicated line",
        "category": "compiler"
    },
    "EXPECTED_BRACE": {
        "pattern": r"expected ['\"`][{}]['\"`]|unmatched.*brace",
        "message": "Unmatched brace.\n\nFix: Check your { } pairs match",
        "category": "compiler"
    },
    "UNDECLARED_IDENTIFIER": {
        "pattern": r"['\"`](\w+)['\"`].*undeclared|undeclared identifier ['\"`](\w+)['\"`]",
        "message": "'{id}' not declared.\n\nFix: Include header or check spelling",
        "category": "compiler"
    },
    "NOT_A_MEMBER": {
        "pattern": r"['\"`](\w+)['\"`] is not a member of ['\"`]([^'\"`]+)['\"`]",
        "message": "'{member}' is not in class '{cls}'.\n\nFix: Check method name or add it to class",
        "category": "compiler"
    },
    "INCOMPLETE_TYPE": {
        "pattern": r"incomplete type ['\"`]([^'\"`]+)['\"`]",
        "message": "Incomplete type '{type}'.\n\nFix: Include full definition or forward declare",
        "category": "compiler"
    },
    "CANNOT_CONVERT": {
        "pattern": r"cannot convert ['\"`]([^'\"`]+)['\"`].*to ['\"`]([^'\"`]+)['\"`]",
        "message": "Can't convert '{from}' to '{to}'.\n\nFix: Use explicit cast or fix types",
        "category": "compiler"
    },
    "AMBIGUOUS_CALL": {
        "pattern": r"ambiguous.*call|call.*ambiguous",
        "message": "Ambiguous function call. Multiple overloads match.\n\nFix: Be more specific with argument types",
        "category": "compiler"
    },
    "PRIVATE_MEMBER": {
        "pattern": r"['\"`](\w+)['\"`].*private.*['\"`]([^'\"`]+)['\"`]|private member",
        "message": "'{member}' is private.\n\nFix: Make it public or add getter method",
        "category": "compiler"
    },
    "PURE_VIRTUAL_COMPILE": {
        "pattern": r"cannot.*instantiate.*pure virtual|pure virtual.*function",
        "message": "Can't instantiate class with pure virtual methods.\n\nFix: Implement all virtual methods",
        "category": "compiler"
    },
    "DELETED_FUNCTION": {
        "pattern": r"use of deleted function|deleted.*constructor",
        "message": "Using deleted function (copy/move).\n\nFix: Use pointers or implement copy/move",
        "category": "compiler"
    },
    "NARROWING_CONVERSION": {
        "pattern": r"narrowing conversion",
        "message": "Narrowing conversion (losing precision).\n\nFix: Use explicit cast like static_cast<int>()",
        "category": "compiler"
    },
    "TEMPLATE_ARGUMENT": {
        "pattern": r"template argument|invalid.*template",
        "message": "Template type mismatch.\n\nFix: Check template parameters match expected types",
        "category": "compiler"
    },
    "DISCARDS_QUALIFIERS": {
        "pattern": r"discards qualifiers|const.*correctness",
        "message": "Const correctness issue.\n\nFix: Add 'const' or use non-const object",
        "category": "compiler"
    },
    "NO_RETURN": {
        "pattern": r"no return statement|control reaches end",
        "message": "Function missing return statement.\n\nFix: Add return at end of function",
        "category": "compiler"
    },
    "UNREACHABLE_CODE": {
        "pattern": r"unreachable code|code.*never.*executed",
        "message": "Code after return never runs.\n\nFix: Remove dead code",
        "category": "compiler"
    },
    "UNINITIALIZED": {
        "pattern": r"uninitialized|used.*before.*init",
        "message": "Variable used before initialization.\n\nFix: Initialize variable before use",
        "category": "compiler"
    },
    "ARRAY_BOUNDS": {
        "pattern": r"array subscript|out of bounds|index.*range",
        "message": "Array index possibly out of bounds.\n\nFix: Check array indices",
        "category": "compiler"
    },
    # SIGNED_UNSIGNED removed in v4.6.6 - this is a warning, not an error
    # pybind11 generates code that triggers this warning, we suppress it with -Wno-sign-compare
    "REDEFINITION": {
        "pattern": r"redefinition of ['\"`]([^'\"`]+)['\"`]",
        "message": "'{name}' defined twice.\n\nFix: Remove duplicate or use different names",
        "category": "compiler"
    },
    "MULTIPLE_DEFINITION": {
        "pattern": r"multiple definition of ['\"`]([^'\"`]+)['\"`]",
        "message": "'{name}' defined in multiple files.\n\nFix: Move to header or make 'static'",
        "category": "compiler"
    },
    "CONFLICTING_TYPES": {
        "pattern": r"conflicting.*types|conflicting.*declaration",
        "message": "Conflicting declarations.\n\nFix: Make declarations match",
        "category": "compiler"
    },
    "UNKNOWN_TYPE": {
        "pattern": r"unknown type name ['\"`](\w+)['\"`]",
        "message": "Unknown type '{type}'.\n\nFix: Include its header",
        "category": "compiler"
    },
    "STATIC_ASSERT": {
        "pattern": r"static_assert|static assertion",
        "message": "Compile-time assertion failed.\n\nFix: Read the assertion message for details",
        "category": "compiler"
    },

    # ========== C. LINKER ERRORS (46-60) ==========
    "UNDEFINED_SYMBOL": {
        "pattern": r"undefined symbol ['\"`]([^'\"`]+)['\"`]",
        "message": "Linker can't find '{symbol}'.\n\nFix: Implementation missing or file not compiled",
        "category": "linker"
    },
    "UNRESOLVED_EXTERNAL": {
        "pattern": r"unresolved external symbol ['\"`]([^'\"`]+)['\"`]",
        "message": "MSVC: Unresolved symbol '{symbol}'.\n\nFix: Check lib paths and add missing library",
        "category": "linker"
    },
    "CANNOT_FIND_LIB": {
        "pattern": r"cannot find -l(\w+)",
        "message": "Library '{lib}' not found.\n\nFix: Install it or fix -L path",
        "category": "linker"
    },
    "MULTIPLE_SYMBOLS": {
        "pattern": r"multiple.*symbols|symbol.*multiply defined",
        "message": "Symbol defined in multiple files.\n\nFix: Make one 'static' or rename",
        "category": "linker"
    },
    "UNDEFINED_VTABLE": {
        "pattern": r"undefined.*vtable|vtable.*undefined",
        "message": "Virtual function not implemented.\n\nFix: Add missing virtual method bodies",
        "category": "linker"
    },
    "UNDEFINED_TYPEINFO": {
        "pattern": r"undefined.*typeinfo|typeinfo.*undefined",
        "message": "RTTI issue with virtual class.\n\nFix: Check virtual destructors, compile with -frtti",
        "category": "linker"
    },
    "UNDEFINED_MAIN": {
        "pattern": r"undefined.*main|main.*undefined",
        "message": "This is a module, not a program.\n\nFix: Build as shared library, not executable",
        "category": "linker"
    },
    "MISSING_LIBSTDCPP": {
        "pattern": r"cannot find -lstdc\+\+|ld:.*cannot find.*libstdc\+\+|error:.*libstdc\+\+\.so.*not found|/usr/lib.*libstdc\+\+.*not found",
        "message": "C++ runtime missing.\n\nFix: Install gcc-libs/libstdc++ package",
        "category": "linker"
    },
    "MISSING_LIBPYTHON": {
        "pattern": r"cannot find -lpython|cannot find.*libpython|error:.*libpython.*not found|ld:.*-lpython.*not found",
        "message": "Python dev libs missing.\n\nFix: Install python3-dev/python3-devel",
        "category": "linker"
    },
    "ABI_MISMATCH": {
        "pattern": r"ABI.*mismatch|incompatible.*ABI",
        "message": "Compiled with different compiler version.\n\nFix: Rebuild everything with same compiler",
        "category": "linker"
    },
    "SYMBOL_VERSION": {
        "pattern": r"symbol.*version|version.*mismatch",
        "message": "Library version mismatch.\n\nFix: Update or downgrade the library",
        "category": "linker"
    },
    "RELOCATION": {
        "pattern": r"relocation.*truncated|relocation.*error",
        "message": "Position-independent code issue.\n\nFix: Add -fPIC flag to compilation",
        "category": "linker"
    },
    "ENTRY_POINT": {
        "pattern": r"entry point|cannot find entry",
        "message": "Wrong entry point for shared library.\n\nFix: Don't link as executable",
        "category": "linker"
    },
    "IMPORT_LIB_MISSING": {
        "pattern": r"\.lib.*not found|cannot open.*\.lib",
        "message": "MSVC: Import library missing.\n\nFix: Check library path or install library",
        "category": "linker"
    },
    "DLL_NOT_FOUND": {
        "pattern": r"DLL.*not found|cannot find.*\.dll",
        "message": "Required DLL missing at runtime.\n\nFix: Add DLL location to PATH",
        "category": "linker"
    },

    # ========== D. CMAKE ERRORS (61-75) ==========
    "CMAKE_NOT_FOUND": {
        "pattern": r"cmake.*not found|'cmake'.*not recognized",
        "message": "CMake not installed.\n\nFix: Install CMake 3.15+",
        "category": "cmake"
    },
    "CMAKE_GENERATOR_FAILED": {
        "pattern": r"Generator.*failed|could not find.*generator",
        "message": "CMake generator not available.\n\nFix: Install or try different generator",
        "category": "cmake"
    },
    "CMAKE_NO_COMPILER": {
        "pattern": r"No CMAKE_CXX_COMPILER|CMAKE_CXX_COMPILER.*NOTFOUND",
        "message": "CMake can't find C++ compiler.\n\nFix: Install g++ or set CC/CXX env vars",
        "category": "cmake"
    },
    "CMAKE_PYBIND11": {
        "pattern": r"pybind11.*not found|Could not find.*pybind11",
        "message": "CMake can't find pybind11.\n\nFix: pip install pybind11",
        "category": "cmake"
    },
    "CMAKE_PYTHON": {
        "pattern": r"Python.*not found|Could not find.*Python",
        "message": "CMake can't find Python.\n\nFix: Set Python3_ROOT_DIR or add Python to PATH",
        "category": "cmake"
    },
    "CMAKE_VERSION": {
        "pattern": r"CMake.*version.*required|version.*too old",
        "message": "CMake version too old.\n\nFix: Update CMake",
        "category": "cmake"
    },
    "CMAKE_CONFIG_FAILED": {
        "pattern": r"Configuring incomplete|configuration.*failed",
        "message": "CMake configure failed.\n\nFix: Check CMakeError.log for details",
        "category": "cmake"
    },
    "CMAKE_BUILD_FAILED": {
        "pattern": r"Build.*failed|cmake --build.*failed",
        "message": "CMake build failed.\n\nFix: See compiler error above",
        "category": "cmake"
    },
    "NINJA_NOT_FOUND": {
        "pattern": r"Ninja.*not found|'ninja'.*not recognized",
        "message": "Ninja not installed.\n\nFix: Install Ninja or use different generator",
        "category": "cmake"
    },
    "MAKE_NOT_FOUND": {
        "pattern": r"make.*not found|'make'.*not recognized",
        "message": "Make not found.\n\nFix: Install build-essential (Linux) or MinGW (Windows)",
        "category": "cmake"
    },
    "VS_NOT_FOUND": {
        "pattern": r"Visual Studio.*not found|could not find.*Visual Studio",
        "message": "Visual Studio not installed.\n\nFix: Install VS Build Tools or use MinGW",
        "category": "cmake"
    },
    "ARCHITECTURE_MISMATCH": {
        "pattern": r"architecture.*mismatch|32.*64|x86.*x64",
        "message": "32/64 bit mismatch.\n\nFix: Use matching compiler architecture",
        "category": "cmake"
    },
    "CMAKE_POLICY": {
        "pattern": r"CMP\d{4}|cmake.*policy",
        "message": "CMake policy warning.\n\nFix: Usually safe to ignore",
        "category": "cmake"
    },
    "TARGET_EXISTS": {
        "pattern": r"target.*already exists|duplicate.*target",
        "message": "Duplicate CMake target name.\n\nFix: Rename one of the modules",
        "category": "cmake"
    },
    "CMAKE_FILE_NOT_FOUND": {
        "pattern": r"include.*could not find|CMake.*file.*not found",
        "message": "CMake can't find required file.\n\nFix: Check paths in CMakeLists.txt",
        "category": "cmake"
    },

    # ========== E. PYBIND11 ERRORS (76-90) ==========
    "NOT_COPYABLE": {
        "pattern": r"is not copyable|cannot be copied",
        "message": "Class can't be copied for Python.\n\nFix: Use py::return_value_policy::reference",
        "category": "pybind11"
    },
    "HOLDER_TYPE": {
        "pattern": r"holder type|incompatible.*holder",
        "message": "Wrong smart pointer type.\n\nFix: Use std::shared_ptr consistently",
        "category": "pybind11"
    },
    "ALREADY_REGISTERED": {
        "pattern": r"already registered|type.*registered.*twice",
        "message": "Type registered twice.\n\nFix: Check DEPENDS() or module structure",
        "category": "pybind11"
    },
    "NO_CONSTRUCTOR": {
        "pattern": r"no.*constructor.*match|constructor.*not found",
        "message": "No matching constructor for binding.\n\nFix: Add CONSTRUCTOR() to .cp file",
        "category": "pybind11"
    },
    "TYPE_NOT_REGISTERED": {
        "pattern": r"type.*not.*registered|unknown.*type",
        "message": "Type not bound to Python.\n\nFix: Add it to PUBLIC() block",
        "category": "pybind11"
    },
    "RETURN_POLICY": {
        "pattern": r"return_value_policy|lifetime.*unclear",
        "message": "Can't determine object lifetime.\n\nFix: Specify return_value_policy explicitly",
        "category": "pybind11"
    },
    "BUFFER_PROTOCOL": {
        "pattern": r"buffer.*protocol|buffer.*interface",
        "message": "Type doesn't support buffer protocol.\n\nFix: Implement buffer interface or use vector",
        "category": "pybind11"
    },
    "OPAQUE_TYPE": {
        "pattern": r"opaque.*type|PYBIND11_MAKE_OPAQUE",
        "message": "Type needs PYBIND11_MAKE_OPAQUE.\n\nFix: Add macro before module definition",
        "category": "pybind11"
    },
    "GIL_ISSUE": {
        "pattern": r"GIL|Global Interpreter Lock",
        "message": "Python GIL issue.\n\nFix: Use py::gil_scoped_release for long operations",
        "category": "pybind11"
    },
    "OVERLOAD_CAST_AMBIG": {
        "pattern": r"overload_cast.*ambiguous|ambiguous.*overload",
        "message": "Ambiguous method overload.\n\nFix: Use METHOD(name, type1, type2) in .cp",
        "category": "pybind11"
    },
    "TRAMPOLINE_NEEDED": {
        "pattern": r"trampoline|virtual.*class.*binding",
        "message": "Virtual class needs trampoline.\n\nFix: Complex - see pybind11 docs for virtual classes",
        "category": "pybind11"
    },
    "KEEP_ALIVE": {
        "pattern": r"prevent.*finalizer|prevent finalizer|reference.*invalid",
        "message": "Object destroyed while Python holds reference.\n\nFix: Use py::keep_alive policy",
        "category": "pybind11"
    },
    "TYPE_CASTER": {
        "pattern": r"type_caster|no.*conversion",
        "message": "No type conversion available.\n\nFix: Register custom type_caster or use different type",
        "category": "pybind11"
    },
    "MODULE_NAME_MISMATCH": {
        "pattern": r"module.*name.*mismatch|PYBIND11_MODULE.*mismatch",
        "message": "Module name mismatch.\n\nFix: Check module name in .cp matches binding",
        "category": "pybind11"
    },
    "INIT_ORDER": {
        "pattern": r"init.*order|initialization.*order",
        "message": "Modules initialized in wrong order.\n\nFix: Check DEPENDS() declarations",
        "category": "pybind11"
    },

    # ========== F. RUNTIME ERRORS (91-105) ==========
    "SEGFAULT": {
        "pattern": r"Segmentation fault|SIGSEGV|segfault",
        "message": "Code crashed (segfault).\n\nFix: Check null pointers and array bounds",
        "category": "runtime"
    },
    "STACK_OVERFLOW": {
        "pattern": r"stack overflow|stack.*exhausted",
        "message": "Stack overflow.\n\nFix: Check recursion depth or reduce stack allocation",
        "category": "runtime"
    },
    "BAD_ALLOC": {
        "pattern": r"bad_alloc|std::bad_alloc|out of memory",
        "message": "Out of memory.\n\nFix: Reduce data size or check for memory leaks",
        "category": "runtime"
    },
    "PURE_VIRTUAL_CALL": {
        "pattern": r"pure virtual.*call|call.*pure virtual",
        "message": "Called pure virtual function.\n\nFix: Object was partially constructed or already destroyed",
        "category": "runtime"
    },
    "INVALID_POINTER": {
        "pattern": r"invalid pointer|dangling.*pointer",
        "message": "Dangling pointer access.\n\nFix: Object was already deleted",
        "category": "runtime"
    },
    "DOUBLE_FREE": {
        "pattern": r"double free|free.*twice",
        "message": "Memory freed twice.\n\nFix: Check ownership - use smart pointers",
        "category": "runtime"
    },
    "HEAP_CORRUPT": {
        "pattern": r"heap.*corrupt|memory.*corrupt",
        "message": "Heap corruption.\n\nFix: Check array bounds and pointer arithmetic",
        "category": "runtime"
    },
    "ACCESS_VIOLATION": {
        "pattern": r"Access violation|0xC0000005",
        "message": "Windows: Invalid memory access.\n\nFix: Same as segfault - check pointers",
        "category": "runtime"
    },
    "DIVISION_ZERO": {
        "pattern": r"division by zero|divide.*zero",
        "message": "Division by zero.\n\nFix: Check divisor before dividing",
        "category": "runtime"
    },
    "OUT_OF_RANGE": {
        "pattern": r"out_of_range|std::out_of_range|index.*out.*range",
        "message": "Index out of bounds.\n\nFix: Check vector/array indices",
        "category": "runtime"
    },
    "BAD_CAST": {
        "pattern": r"bad_cast|std::bad_cast|dynamic_cast.*failed",
        "message": "Dynamic cast failed.\n\nFix: Object is not the expected type",
        "category": "runtime"
    },
    "LOGIC_ERROR": {
        "pattern": r"logic_error|std::logic_error",
        "message": "Logic error - precondition violated.\n\nFix: Check your assumptions",
        "category": "runtime"
    },
    "RUNTIME_ERROR": {
        "pattern": r"runtime_error|std::runtime_error",
        "message": "Runtime error.\n\nFix: Read the error message for details",
        "category": "runtime"
    },
    "BAD_FUNCTION": {
        "pattern": r"bad_function_call|std::bad_function_call",
        "message": "Called empty std::function.\n\nFix: Check function is set before calling",
        "category": "runtime"
    },
    "SYSTEM_ERROR": {
        "pattern": r"system_error|std::system_error",
        "message": "OS-level error.\n\nFix: Check errno (Linux) or GetLastError (Windows)",
        "category": "runtime"
    },

    # ========== G. PLUGIN PARSING ERRORS (106-120) ==========
    "CP_MISSING_PAREN": {
        "pattern": r"\.cp.*missing.*\(|expected.*\(",
        "message": "Missing parenthesis in .cp file.\n\nFix: Check FUNC(), CLASS() syntax",
        "category": "plugin"
    },
    "CP_UNCLOSED_BRACE": {
        "pattern": r"\.cp.*unclosed.*\{|expected.*\}",
        "message": "Unclosed brace in .cp file.\n\nFix: Check CLASS(){} blocks",
        "category": "plugin"
    },
    "CP_INVALID_KEYWORD": {
        "pattern": r"unknown.*keyword|invalid.*keyword",
        "message": "Unknown keyword in .cp.\n\nFix: Valid keywords: SOURCE, HEADER, PUBLIC, DEPENDS, CLASS, FUNC, METHOD",
        "category": "plugin"
    },
    "CP_EMPTY_FUNC": {
        "pattern": r"FUNC\(\s*\)|empty.*FUNC",
        "message": "Empty FUNC().\n\nFix: Add function name: FUNC(my_function)",
        "category": "plugin"
    },
    "CP_EMPTY_CLASS": {
        "pattern": r"CLASS\(\s*\)|empty.*CLASS",
        "message": "Empty CLASS().\n\nFix: Add class name: CLASS(MyClass)",
        "category": "plugin"
    },
    "CP_INVALID_CHARS": {
        "pattern": r"invalid.*character|illegal.*character",
        "message": "Invalid character in .cp file.\n\nFix: Use ASCII only",
        "category": "plugin"
    },
    "CP_DUPLICATE": {
        "pattern": r"duplicate.*name|name.*already.*used",
        "message": "Duplicate name in .cp.\n\nFix: Use unique names",
        "category": "plugin"
    },
    "CP_RESERVED": {
        "pattern": r"reserved.*word|reserved.*keyword",
        "message": "Using reserved word.\n\nFix: Choose different name",
        "category": "plugin"
    },
    "CP_BAD_SOURCE_PATH": {
        "pattern": r"SOURCE.*invalid.*path|bad.*path.*SOURCE",
        "message": "Invalid SOURCE() path.\n\nFix: Use forward slashes: SOURCE(include/file.cpp)",
        "category": "plugin"
    },
    "CP_MISSING_MODULE_NAME": {
        "pattern": r"missing.*module.*name|SOURCE.*no.*name",
        "message": "SOURCE() missing module name.\n\nFix: SOURCE(file.cpp) module_name",
        "category": "plugin"
    },
    "CP_BAD_DEPENDS": {
        "pattern": r"DEPENDS.*invalid|bad.*DEPENDS",
        "message": "Invalid DEPENDS() syntax.\n\nFix: DEPENDS(module1, module2)",
        "category": "plugin"
    },
    "CP_SELF_DEPEND": {
        "pattern": r"depends.*itself|self.*dependency",
        "message": "Module depends on itself.\n\nFix: Remove circular DEPENDS()",
        "category": "plugin"
    },
    "CP_NO_IMPL": {
        "pattern": r"no.*implementation|function.*not.*found.*source",
        "message": "Function declared in .cp but not in source.\n\nFix: Add implementation or remove from .cp",
        "category": "plugin"
    },
    "CP_SIGNATURE_MISMATCH": {
        "pattern": r"signature.*mismatch|parameter.*mismatch",
        "message": "Method signature doesn't match C++ code.\n\nFix: Regenerate .cp with: includecpp plugin <name>",
        "category": "plugin"
    },
    "CP_TEMPLATE_SYNTAX": {
        "pattern": r"TEMPLATE.*syntax|TYPES.*invalid|bad.*TYPES",
        "message": "Invalid template syntax.\n\nFix: TEMPLATE_FUNC(name) TYPES(int, float, double)",
        "category": "plugin"
    },

    # ========== H. IMPORT/LOAD ERRORS (121-130) ==========
    "DLL_LOAD_FAILED": {
        "pattern": r"DLL load failed|ImportError.*DLL",
        "message": "Can't load .pyd module.\n\nFix: Install VC++ Redistributable or check Python version",
        "category": "import"
    },
    "IMPORT_ERROR": {
        "pattern": r"ImportError|ModuleNotFoundError",
        "message": "Can't import module.\n\nFix: includecpp rebuild",
        "category": "import"
    },
    "MODULE_CORRUPT": {
        "pattern": r"corrupt.*module|module.*corrupt|invalid.*module",
        "message": "Module file corrupted.\n\nFix: includecpp rebuild --clean",
        "category": "import"
    },
    "VERSION_MISMATCH": {
        "pattern": r"version mismatch|wrong.*version",
        "message": "Python version changed since build.\n\nFix: includecpp rebuild",
        "category": "import"
    },
    "MISSING_DEP_MODULE": {
        "pattern": r"depends.*on.*'(\w+)'|missing.*dependency.*'(\w+)'",
        "message": "Module needs '{dep}'.\n\nFix: Build '{dep}' first or add DEPENDS({dep})",
        "category": "import"
    },
    "PATH_ISSUE": {
        "pattern": r"module.*not.*path|cannot.*find.*module.*path",
        "message": "Module not in Python path.\n\nFix: Check PYTHONPATH or install location",
        "category": "import"
    },
    "FILE_LOCKED_WINDOWS": {
        "pattern": r"WinError 32|being used by another process|cannot access.*because.*used|process cannot access",
        "message": "File is locked by another process!\n\nThis usually means:\n  - A compiled .exe is still running\n  - Another Python script is using this module\n  - An IDE has the file open\n\nFix: Close any running .exe or Python process that uses this module,\n     then run 'includecpp rebuild' again.",
        "category": "import"
    },
    "FILE_LOCKED_LINUX": {
        "pattern": r"ETXTBSY|EBUSY|Text file busy|Device or resource busy|\[Errno 16\]|\[Errno 26\]",
        "message": "File is busy (in use by another process)!\n\nThis usually means:\n  - A running process is using this shared library\n  - Another Python script has imported this module\n\nFix: Close any process using this module, then run 'includecpp rebuild' again.",
        "category": "import"
    },
    "MODULE_FILE_LOCKED": {
        "pattern": r"(api\.pyd|\.pyd|\.so|\.dll).*(?:Permission|WinError|denied|locked|in use|busy)",
        "message": "Module file (.pyd/.so/.dll) is locked!\n\nThe compiled module cannot be overwritten because it's in use.\n\nFix:\n  1. Close any running executable that uses this module\n  2. Close Python scripts/REPL using this module\n  3. Restart your IDE if it imported the module\n  4. Then run 'includecpp rebuild'",
        "category": "import"
    },
    "PERMISSION_ERROR_WINDOWS": {
        "pattern": r"WinError 5|WinError 13|Access is denied",
        "message": "Permission denied (Windows).\n\nPossible causes:\n  - File is locked by another process (close running .exe)\n  - Antivirus blocking write access\n  - Need administrator rights\n\nFix: Close any process using this file, or run as administrator.",
        "category": "import"
    },
    "PERMISSION_ERROR_LINUX": {
        "pattern": r"\[Errno 13\]|EACCES|Operation not permitted|\[Errno 1\]",
        "message": "Permission denied (Linux/Mac).\n\nPossible causes:\n  - File is locked by another process\n  - Insufficient permissions\n  - File owned by different user\n\nFix: Close any process using this file, check ownership, or use sudo.",
        "category": "import"
    },
    "PERMISSION_ERROR": {
        "pattern": r"permission denied|PermissionError|access.*denied",
        "message": "Permission denied.\n\nFix: Check file permissions or close processes using the file",
        "category": "import"
    },
    "FILE_LOCKED": {
        "pattern": r"file.*locked|file.*in use|being used.*another|file is busy",
        "message": "File in use by another process.\n\nFix: Close Python processes or executables using this module",
        "category": "import"
    },
    "REGISTRY_MISSING": {
        "pattern": r"registry.*not found|\.module_registry\.json.*missing",
        "message": ".module_registry.json missing.\n\nFix: includecpp rebuild",
        "category": "import"
    },
    "HASH_MISMATCH": {
        "pattern": r"hash.*mismatch|checksum.*mismatch|source.*changed",
        "message": "Source changed since build.\n\nFix: includecpp rebuild",
        "category": "import"
    },
}


def _extract_error_location(stderr: str) -> Tuple[Optional[str], Optional[int]]:
    """Extract file and line number from compiler error output.

    Supports GCC/Clang format: file.cpp:42:10: error: ...
    Supports MSVC format: file.cpp(42): error C1234: ...

    Returns:
        Tuple of (filename, line_number) or (None, None) if not found
    """
    # GCC/Clang format: file:line:col: error:
    gcc_match = re.search(r'([^\s:]+\.[ch](?:pp)?):(\d+):\d*:?\s*error:', stderr)
    if gcc_match:
        return gcc_match.group(1), int(gcc_match.group(2))

    # MSVC format: file(line): error
    msvc_match = re.search(r'([^\s(]+\.[ch](?:pp)?)\((\d+)\):\s*error', stderr)
    if msvc_match:
        return msvc_match.group(1), int(msvc_match.group(2))

    # Try to find any line number mention
    line_match = re.search(r':(\d+):', stderr)
    if line_match:
        return None, int(line_match.group(1))

    return None, None


def get_error_message(stderr: str, context: Optional[Dict] = None) -> Optional[str]:
    """Match error text against catalog and return helpful message.

    Args:
        stderr: Error text (stderr, exception message, etc.)
        context: Optional dict with extra info (module_name, file, line, etc.)

    Returns:
        Formatted error message or None if no match
    """
    if not stderr:
        return None

    context = context or {}

    # Extract location info from stderr
    error_file, error_line = _extract_error_location(stderr)

    for key, entry in ERROR_CATALOG.items():
        match = re.search(entry["pattern"], stderr, re.IGNORECASE)
        if match:
            msg = entry["message"]

            # Extract captured groups (filter None values)
            groups = [g for g in match.groups() if g]

            # Find all placeholders in message and replace with first captured value
            if groups:
                # Replace any placeholder with the first captured group
                placeholder_pattern = re.compile(r'\{(\w+)\}')
                for placeholder in placeholder_pattern.findall(msg):
                    msg = msg.replace(f'{{{placeholder}}}', groups[0])

            # Add location info if found
            location_info = []
            if error_file:
                location_info.append(f"File: {error_file}")
            if error_line:
                location_info.append(f"Line: {error_line}")

            if location_info:
                msg = f"{' | '.join(location_info)}\n\n{msg}"

            # Add context info
            if context.get("module"):
                msg = f"[{context['module']}] {msg}"

            return msg

    return None


def format_error_box(message: str, title: str = "ERROR") -> str:
    """Format error in a visible box."""
    width = 60
    lines = message.split('\n')

    box = []
    box.append(f"+{'-' * (width - 2)}+")
    box.append(f"| {title:<{width - 4}} |")
    box.append(f"+{'-' * (width - 2)}+")
    box.append("")

    for line in lines:
        box.append(line)

    return '\n'.join(box)


def format_unknown_error(stderr: str) -> str:
    """Format unknown error with basic troubleshooting."""
    # Extract first meaningful error line
    lines = stderr.strip().split('\n')
    first_error = next((l for l in lines if 'error' in l.lower()), lines[0] if lines else "Unknown error")

    # Try to extract location info
    error_file, error_line = _extract_error_location(stderr)
    location_str = ""
    if error_file or error_line:
        parts = []
        if error_file:
            parts.append(f"File: {error_file}")
        if error_line:
            parts.append(f"Line: {error_line}")
        location_str = f"{' | '.join(parts)}\n\n"

    return f"""Unknown error occurred.

{location_str}{first_error[:200]}

Troubleshooting:
  1. Run with --verbose for full output
  2. Check C++ syntax in your source files
  3. Try: includecpp rebuild --clean
  4. Report bug: includecpp bug"""
