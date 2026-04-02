cmake_minimum_required(VERSION 3.30)
project(ds LANGUAGES CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

include(GNUInstallDirs)
file(GLOB_RECURSE SOURCES CONFIGURE_DEPENDS "${CMAKE_CURRENT_SOURCE_DIR}/src/*.cc")
add_library(${PROJECT_NAME} STATIC)
target_sources(${PROJECT_NAME} PRIVATE ${SOURCES})
target_include_directories(${PROJECT_NAME} PUBLIC $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)
target_compile_features(${PROJECT_NAME} PUBLIC cxx_std_20)
set_property(TARGET ${PROJECT_NAME} PROPERTY INTERPROCEDURAL_OPTIMIZATION True)

install(TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}-targets
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/include/
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(EXPORT ${PROJECT_NAME}-targets
  FILE ${PROJECT_NAME}-config.cmake
  NAMESPACE ${PROJECT_NAME}::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME})

file(GLOB EXECUTABLE_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/examples/*.cc")
foreach(EXEC_FILE ${EXECUTABLE_SOURCES})
  get_filename_component(EXEC_NAME ${EXEC_FILE} NAME_WE)
  add_executable(${EXEC_NAME} ${EXEC_FILE})
  target_link_libraries(${EXEC_NAME} PRIVATE ${PROJECT_NAME})
  set_property(TARGET ${EXEC_NAME} PROPERTY INTERPROCEDURAL_OPTIMIZATION True)
endforeach()

find_package(pybind11)
if(pybind11_FOUND)
  pybind11_add_module(apyds ${CMAKE_CURRENT_SOURCE_DIR}/apyds/ds.cc)
  target_link_libraries(apyds PRIVATE ${PROJECT_NAME})
  set_property(TARGET apyds PROPERTY INTERPROCEDURAL_OPTIMIZATION True)
  set_target_properties(apyds PROPERTIES OUTPUT_NAME _ds)
  install(TARGETS apyds DESTINATION apyds COMPONENT python)
else()
  message(STATUS "pybind11 not found, Python bindings will not be built.")
endif()

find_package(GTest)
if(GTest_FOUND)
  enable_testing()
  add_custom_target(test_executables)
  file(GLOB TEST_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/tests/*.cc")
  foreach(TEST_FILE ${TEST_SOURCES})
    get_filename_component(TEST_NAME ${TEST_FILE} NAME_WE)
    add_executable(${TEST_NAME} ${TEST_FILE})
    target_link_libraries(${TEST_NAME} PRIVATE ${PROJECT_NAME} GTest::gtest_main)
    set_property(TARGET ${TEST_NAME} PROPERTY INTERPROCEDURAL_OPTIMIZATION True)
    gtest_discover_tests(${TEST_NAME})
    add_dependencies(test_executables ${TEST_NAME})
  endforeach()
else()
  message(STATUS "GTest not found, tests will not be built.")
endif()
