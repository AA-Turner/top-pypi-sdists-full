# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

get_target_property(_tango_include_dirs Tango::Tango INTERFACE_INCLUDE_DIRECTORIES)
set(Tango_VERSION_STRING "unknown")

if(NOT CMAKE_CROSSCOMPILING)
  set(_tango_git_revision_probe "${CMAKE_CURRENT_BINARY_DIR}/get_tango_git_revision.cpp")
  string(JOIN ";" _tango_try_run_include_dirs ${_tango_include_dirs})
  file(WRITE "${_tango_git_revision_probe}" [=[
#include <iostream>
#include <tango/common/versions.h>

int main()
{
    std::cout
        << TANGO_VERSION_MAJOR << '.'
        << TANGO_VERSION_MINOR << '.'
        << TANGO_VERSION_PATCH
        << " (git_version: " << Tango::git_revision() << ')';
    return 0;
}
]=])
  try_run(
    Tango_GIT_VERSION_RUN_RESULT
    Tango_GIT_VERSION_COMPILE_RESULT
    "${CMAKE_CURRENT_BINARY_DIR}"
    "${_tango_git_revision_probe}"
    CMAKE_FLAGS "-DINCLUDE_DIRECTORIES:STRING=${_tango_try_run_include_dirs}"
    LINK_LIBRARIES Tango::Tango
    RUN_OUTPUT_VARIABLE Tango_VERSION_STRING
  )
  if(
    NOT Tango_GIT_VERSION_COMPILE_RESULT
    OR NOT "${Tango_GIT_VERSION_RUN_RESULT}" STREQUAL "0"
  )
    set(Tango_VERSION_STRING "unknown")
  endif()
  string(STRIP "${Tango_VERSION_STRING}" Tango_VERSION_STRING)
endif()

message(STATUS "  cppTango version:  ${Tango_VERSION_STRING}")
