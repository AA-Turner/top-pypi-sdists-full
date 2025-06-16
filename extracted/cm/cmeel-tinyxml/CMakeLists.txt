cmake_minimum_required(VERSION 3.1)

set(PROJECT_NAME tinyxml)
set(PROJECT_VERSION 2.6.2)

project(${PROJECT_NAME} VERSION ${PROJECT_VERSION})

set(${PROJECT_NAME}_SOURCES
    ${PROJECT_NAME}/tinyxml.cpp ${PROJECT_NAME}/tinyxmlerror.cpp
    ${PROJECT_NAME}/tinyxmlparser.cpp)

set(${PROJECT_NAME}_HEADERS ${PROJECT_NAME}/tinyxml.h ${PROJECT_NAME}/tinystr.h)

add_library(${PROJECT_NAME} SHARED ${${PROJECT_NAME}_SOURCES}
                                   ${${PROJECT_NAME}_HEADERS})
target_include_directories(${PROJECT_NAME} PUBLIC $<INSTALL_INTERFACE:include>)
target_compile_definitions(${PROJECT_NAME} PUBLIC -DTIXML_USE_STL)

install(
  TARGETS ${PROJECT_NAME}
  EXPORT ${PROJECT_NAME}Targets
  DESTINATION lib)
install(FILES ${${PROJECT_NAME}_HEADERS} DESTINATION include)

include(CMakePackageConfigHelpers)

configure_package_config_file(
  "${PROJECT_NAME}Config.cmake.in"
  "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
  INSTALL_DESTINATION "lib/cmake/${PROJECT_NAME}")
write_basic_package_version_file(
  "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
  VERSION ${PROJECT_VERSION}
  COMPATIBILITY SameMajorVersion)

install(FILES "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
              "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        DESTINATION "lib/cmake/${PROJECT_NAME}")

install(
  EXPORT ${PROJECT_NAME}Targets
  NAMESPACE cmeel::
  DESTINATION "lib/cmake/${PROJECT_NAME}")
