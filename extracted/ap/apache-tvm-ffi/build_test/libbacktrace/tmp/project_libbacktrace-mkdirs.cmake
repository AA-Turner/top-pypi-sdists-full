# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION ${CMAKE_VERSION}) # this file comes with cmake

# If CMAKE_DISABLE_SOURCE_CHANGES is set to true and the source directory is an
# existing directory in our source tree, calling file(MAKE_DIRECTORY) on it
# would cause a fatal error, even though it would be a no-op.
if(NOT EXISTS "/home/runner/work/tvm-ffi/tvm-ffi/cmake/Utils/../../3rdparty/libbacktrace")
  file(MAKE_DIRECTORY "/home/runner/work/tvm-ffi/tvm-ffi/cmake/Utils/../../3rdparty/libbacktrace")
endif()
file(MAKE_DIRECTORY
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace"
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace"
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/tmp"
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/src/project_libbacktrace-stamp"
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/src"
  "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/logs"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/src/project_libbacktrace-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/runner/work/tvm-ffi/tvm-ffi/build_test/libbacktrace/src/project_libbacktrace-stamp${cfgdir}") # cfgdir has leading slash
endif()
