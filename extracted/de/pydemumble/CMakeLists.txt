cmake_minimum_required(VERSION 3.15...3.27)
project(pydemumble LANGUAGES CXX)

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

if (UNIX)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
endif()

if (WIN32)
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /Zc:inline")
	add_definitions(-D_CRT_SECURE_NO_WARNINGS)  # The LLVM build sets this.

	# statically link against msvcrt
	string(TOUPPER "${CMAKE_BUILD_TYPE}" build)
	set(flag_var "CMAKE_CXX_FLAGS_${build}")
	if(${flag_var} MATCHES "/MD")
		string(REGEX REPLACE "/MD" "/MT" ${flag_var} "${${flag_var}}")
	endif()
endif()

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.8
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

include_directories(
	src/rust_legacy
	src/third_party/llvm/include
	src/third_party/swift/include
)

add_definitions(
  -DLLVM_DISABLE_ABI_BREAKING_CHECKS_ENFORCING=1
  -DSWIFT_SUPPORT_OLD_MANGLING=1
  -DSWIFT_STDLIB_HAS_TYPE_PRINTING=1
)

# finding nanobind
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/src/nanobind)

nanobind_add_module(
	pydemumble
  STABLE_ABI
  NB_STATIC
	src/pydemumble.cpp
	src/rust_legacy/rust_legacy_demangle.cc
	src/third_party/llvm/lib/Demangle/DLangDemangle.cpp
	src/third_party/llvm/lib/Demangle/ItaniumDemangle.cpp
	src/third_party/llvm/lib/Demangle/MicrosoftDemangle.cpp
	src/third_party/llvm/lib/Demangle/MicrosoftDemangleNodes.cpp
	src/third_party/llvm/lib/Demangle/RustDemangle.cpp
	src/third_party/swift/lib/Demangling/Context.cpp
	src/third_party/swift/lib/Demangling/CrashReporter.cpp
	src/third_party/swift/lib/Demangling/Demangler.cpp
	src/third_party/swift/lib/Demangling/DemanglingErrorHandling.cpp
	src/third_party/swift/lib/Demangling/ManglingUtils.cpp
	src/third_party/swift/lib/Demangling/NodeDumper.cpp
	src/third_party/swift/lib/Demangling/NodePrinter.cpp
	src/third_party/swift/lib/Demangling/OldDemangler.cpp
	src/third_party/swift/lib/Demangling/OldRemangler.cpp
	src/third_party/swift/lib/Demangling/Punycode.cpp
	src/third_party/swift/lib/Demangling/Remangler.cpp
)

install(TARGETS pydemumble LIBRARY DESTINATION pydemumble)
