cmake_minimum_required(VERSION 3.30)

set(ORG madler)
set(NAME zlib)
set(VERSION 1.3.1)
set(EXT tar.gz)
set(SHA256 17e88863f3600672ab49182f217281b6fc4d3c762bde361935e436a95214d05c)
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
