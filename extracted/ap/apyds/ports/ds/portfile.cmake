vcpkg_from_github(
    OUT_SOURCE_PATH SOURCE_PATH
    REPO USTC-KnowledgeComputingLab/ds
    HEAD_REF main
)

vcpkg_cmake_configure(
    SOURCE_PATH "${SOURCE_PATH}"
)

vcpkg_cmake_build()

vcpkg_cmake_install()

vcpkg_install_copyright(FILE_LIST "${SOURCE_PATH}/LICENSE.md")

vcpkg_cmake_config_fixup(PACKAGE_NAME ds CONFIG_PATH lib/cmake/ds)

file(REMOVE_RECURSE "${CURRENT_PACKAGES_DIR}/debug/include")
