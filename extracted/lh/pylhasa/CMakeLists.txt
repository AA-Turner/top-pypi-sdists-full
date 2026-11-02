cmake_minimum_required(VERSION 3.20)
project(pylhasa LANGUAGES C)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)

add_library(lhasa STATIC
  native/vendor/lhasa/crc16.c
  native/vendor/lhasa/ext_header.c
  native/vendor/lhasa/lh1_decoder.c
  native/vendor/lhasa/lh2_decoder.c
  native/vendor/lhasa/lh3_decoder.c
  native/vendor/lhasa/lh5_decoder.c
  native/vendor/lhasa/lh6_decoder.c
  native/vendor/lhasa/lh7_decoder.c
  native/vendor/lhasa/lha_arch_unix.c
  native/vendor/lhasa/lha_arch_win32.c
  native/vendor/lhasa/lha_basic_reader.c
  native/vendor/lhasa/lha_decoder.c
  native/vendor/lhasa/lha_endian.c
  native/vendor/lhasa/lha_file_header.c
  native/vendor/lhasa/lha_input_stream.c
  native/vendor/lhasa/lha_reader.c
  native/vendor/lhasa/lhx_decoder.c
  native/vendor/lhasa/lk7_decoder.c
  native/vendor/lhasa/lz5_decoder.c
  native/vendor/lhasa/lzs_decoder.c
  native/vendor/lhasa/macbinary.c
  native/vendor/lhasa/null_decoder.c
  native/vendor/lhasa/pm1_decoder.c
  native/vendor/lhasa/pm2_decoder.c
)

target_include_directories(lhasa PUBLIC
  native/vendor/lhasa
)

target_compile_features(lhasa PRIVATE c_std_99)
set_target_properties(lhasa PROPERTIES POSITION_INDEPENDENT_CODE ON)

add_library(_pylhasa MODULE
  native/pylhasa_module.c
)

target_include_directories(_pylhasa PRIVATE
  native/vendor/lhasa
)

target_link_libraries(_pylhasa PRIVATE
  lhasa
  Python::Module
)

target_compile_features(_pylhasa PRIVATE c_std_99)

set_target_properties(_pylhasa PROPERTIES
  PREFIX ""
  OUTPUT_NAME "_pylhasa"
)

if (Python_EXTENSION_MODULE_SUFFIX)
  set_target_properties(_pylhasa PROPERTIES
    SUFFIX "${Python_EXTENSION_MODULE_SUFFIX}"
  )
endif()

if (WIN32)
  # Ensure the extension uses .pyd on Windows even if suffix vars are empty.
  set_target_properties(_pylhasa PROPERTIES SUFFIX ".pyd")
endif()

if (MSVC)
  target_compile_definitions(_pylhasa PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()

install(TARGETS _pylhasa
  LIBRARY DESTINATION pylhasa
  ARCHIVE DESTINATION pylhasa
  RUNTIME DESTINATION pylhasa
)

# Install the pure-Python package alongside the extension.
install(
  DIRECTORY src/pylhasa
  DESTINATION .
  PATTERN "__pycache__" EXCLUDE
  PATTERN "*.pyc" EXCLUDE
)
