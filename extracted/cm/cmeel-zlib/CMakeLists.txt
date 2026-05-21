cmake_minimum_required(VERSION 4.0)

set(ORG madler)
set(NAME zlib)
set(VERSION 1.3.2)
set(EXT tar.gz)
set(SHA256 b99a0b86c0ba9360ec7e78c4f1e43b1cbdf1e6936c8fa0f6835c0cd694a495a1)
set(TAG_PREFIX "refs/tags/v")

project("cmeel-${NAME}" VERSION "${VERSION}")

include(ExternalProject)
ExternalProject_Add(
  ${NAME}
  URL "https://github.com/${ORG}/${NAME}/archive/${TAG_PREFIX}${VERSION}.${EXT}"
  URL_HASH "SHA256=${SHA256}"
  DOWNLOAD_EXTRACT_TIMESTAMP OFF
  CMAKE_ARGS "-DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}")

# dummy file for install target
install(FILES "README.md" DESTINATION "share/cmeel-${NAME}/")
