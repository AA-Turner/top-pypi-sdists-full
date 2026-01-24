# cmake_minimum_required(VERSION 3.16)  # Ubuntu 20.04 ships with cmake 3.16.3
# cmake_minimum_required(VERSION 3.17)  # cmake 3.17 added support for conda environments FindPython
cmake_minimum_required(VERSION 3.18)  # cmake 3.18 supported in debian bullseye and cppTango
# cmake_minimum_required(VERSION 3.25)  # latest release. Available as pip install cmake

include(cmake/prelude.cmake)

project(
    pytango
    VERSION 10.1.2
    DESCRIPTION "Python bindings for the Tango distributed control system"
    HOMEPAGE_URL "https://pytango.readthedocs.io/"
    LANGUAGES CXX
)

include(cmake/project-is-top-level.cmake)

# ---- Dependencies -------

# A temporary method for finding Tango and its dependencies is
# to use the cmake/Find*.cmake files. Longer term solution would be for
# cppTango to export/install a tango-config.cmake file and use find_package
# in CONFIG mode: find_package(tango REQUIRED CONFIG)
# See: https://gitlab.com/tango-controls/TangoTickets/-/issues/81
# The FindTango.cmake will attempt to find tango first using pkg-config
# but gracefully try using cmake ways if pkg-config is not available (i.e. Windows)
# or tango is not found.
# Use the environment/cache variable Tango_ROOT to set the tango installation prefix.
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/TangoCMakeModules)
find_package(Tango REQUIRED)

if(NOT DEFINED CMAKE_CXX_STANDARD)
    set(CMAKE_CXX_STANDARD 17)
endif()

# Find Python and NumPy
# https://cmake.org/cmake/help/latest/module/FindPython.html
if (DEFINED ENV{PYTHON_ROOT})
    set(Python_ROOT_DIR "$ENV{PYTHON_ROOT}" CACHE STRING "Python root installation path")
    set(Python_FIND_STRATEGY LOCATION)
endif()
find_package (Python 3.10 COMPONENTS Interpreter Development NumPy)
message(STATUS "    Python version:  ${Python_VERSION}")
message(STATUS "      - intepreter:  ${Python_EXECUTABLE}")
message(STATUS "       - libraries:  ${Python_LIBRARIES}")
message(STATUS "       - libraries:  ${Python_LIBRARY_DIRS}")
message(STATUS "     NumPy version:  ${Python_NumPy_VERSION}")
message(STATUS "     - include dir:  ${Python_NumPy_INCLUDE_DIRS}")

set(PYBIND11_FINDPYTHON ON)
find_package(pybind11 3.0.1
  HINTS ${Python_SITELIB}
  version
  CONFIG REQUIRED)
message(STATUS "     - pybind11 version:  ${pybind11_VERSION}")

# ---- Declare library ----
pybind11_add_module(
    pytango_tango MODULE

    ext/base_types_structures/attr_conf_event_data.cpp
    ext/base_types_structures/attribute_alarm_info.cpp
    ext/base_types_structures/attribute_config.cpp
    ext/base_types_structures/attribute_config_and_info.cpp
    ext/base_types_structures/attribute_dimension.cpp
    ext/base_types_structures/base_structures.cpp
    ext/base_types_structures/base_types.cpp
    ext/base_types_structures/command_info.cpp
    ext/base_types_structures/data_ready_event_data.cpp
    ext/base_types_structures/dev_command_info.cpp
    ext/base_types_structures/device_attribute_history.cpp
    ext/base_types_structures/device_data_history.cpp
    ext/base_types_structures/device_info.cpp
    ext/base_types_structures/devintr_change_event_data.cpp
    ext/base_types_structures/enums.cpp
    ext/base_types_structures/event_data.cpp
    ext/base_types_structures/events_info.cpp
    ext/base_types_structures/exception.cpp
    ext/base_types_structures/fwdAttr.cpp
    ext/base_types_structures/locker_info.cpp
    ext/base_types_structures/locking_thread.cpp
    ext/base_types_structures/poll_device.cpp
    ext/base_types_structures/time_val.cpp
    ext/base_types_structures/user_default_attr_prop.cpp
    ext/base_types_structures/client_addr.cpp

    ext/convertors/generic_from_py.cpp
    ext/convertors/object_casters.cpp
    ext/convertors/vector_wrappers.cpp

    ext/client/attribute_proxy.cpp
    ext/client/callback.cpp
    ext/client/connection.cpp
    ext/client/device_attribute.cpp
    ext/client/device_data.cpp
    ext/client/device_proxy.cpp
    ext/client/group.cpp
    ext/client/group_reply.cpp
    ext/client/group_reply_list.cpp

    ext/database/database.cpp
    ext/database/db.cpp

    ext/server/attr.cpp
    ext/server/attribute.cpp
    ext/server/auto_monitor.cpp
    ext/server/command.cpp
    ext/server/device_class.cpp
    ext/server/device_impl.cpp
    ext/server/dserver.cpp
    ext/server/encoded_attribute.cpp
    ext/server/log4tango.cpp
    ext/server/multi_attribute.cpp
    ext/server/multi_class_attribute.cpp
    ext/server/subdev.cpp
    ext/server/wattribute.cpp

    ext/api_util.cpp
    ext/constants.cpp
    ext/coverage.cpp
    ext/ensure_omni_thread.cpp
    ext/pytango.cpp
    ext/pyutils.cpp
    ext/tango_util.cpp
    ext/telemetry.cpp
    ext/version.cpp
)

set_source_files_properties(
    ext/client/device_attribute.cpp
    PROPERTIES
    COMPILE_OPTIONS $<$<CXX_COMPILER_ID:GNU,Clang>:-Wno-nonnull>
)

target_precompile_headers(pytango_tango PRIVATE ext/precompiled_header.hpp)

set_target_properties(
    pytango_tango PROPERTIES
    VISIBILITY_INLINES_HIDDEN YES
    OUTPUT_NAME _tango
    COMPILE_OPTIONS "-DPYTANGO_NUMPY_VERSION=${Python_NumPy_VERSION};-DNPY_NO_DEPRECATED_API=0"
)
if (WIN32)
    set_target_properties(
        pytango_tango PROPERTIES
        COMPILE_OPTIONS "/bigobj;-DPYTANGO_NUMPY_VERSION=${Python_NumPy_VERSION};-DNPY_NO_DEPRECATED_API=0"
    )
endif()

target_include_directories(
    pytango_tango
    PUBLIC
    "$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/ext>"
)

target_link_libraries(pytango_tango PRIVATE Python::Module Python::NumPy pybind11::module Tango::Tango)

install(TARGETS pytango_tango
	LIBRARY DESTINATION tango
	RUNTIME DESTINATION tango)

if(NOT CMAKE_CROSSCOMPILING)
  include(cmake/generate_stubs.cmake)
endif()

option(PYTANGO_ENABLE_COVERAGE "Instrument code for coverage analysis" OFF)
if(PYTANGO_ENABLE_COVERAGE AND NOT (CMAKE_CXX_COMPILER_ID MATCHES "GNU"))
  message(FATAL_ERROR "Code coverage is not supported for selected compiler.")
endif()

if(PYTANGO_ENABLE_COVERAGE)
  target_compile_definitions(pytango_tango PRIVATE PYTANGO_ENABLE_COVERAGE=1)
  target_compile_options(pytango_tango PRIVATE --coverage -Wl,--dynamic-list-data)
  target_link_options(pytango_tango PRIVATE --coverage -Wl,--dynamic-list-data)
endif()

# ---- Developer mode ----

if(NOT pytango_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of pytango"
  )
endif()
