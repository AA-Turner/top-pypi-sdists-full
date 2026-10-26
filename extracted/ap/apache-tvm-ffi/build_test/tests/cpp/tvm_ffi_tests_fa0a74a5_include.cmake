if(EXISTS "/home/runner/work/tvm-ffi/tvm-ffi/build_test/lib/tvm_ffi_tests")
  if(NOT EXISTS "/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_tests.cmake" OR
     NOT "/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_tests.cmake" IS_NEWER_THAN "/home/runner/work/tvm-ffi/tvm-ffi/build_test/lib/tvm_ffi_tests" OR
     NOT "/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_tests.cmake" IS_NEWER_THAN "${CMAKE_CURRENT_LIST_FILE}")
    include("/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_discovery.cmake")
  endif()
endif()
if(EXISTS "/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_tests.cmake")
  include("/home/runner/work/tvm-ffi/tvm-ffi/build_test/tests/cpp/tvm_ffi_tests_fa0a74a5_tests.cmake")
else()
  add_test(tvm_ffi_tests_NOT_BUILT tvm_ffi_tests_NOT_BUILT)
endif()
