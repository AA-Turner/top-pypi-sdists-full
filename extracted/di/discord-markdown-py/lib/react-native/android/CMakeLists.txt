# Added to the consuming app's native build by React Native autolinking (see
# react-native.config.cjs); the `discordmarkdown_cxxmodule` target is linked into the app's
# `appmodules` library alongside the codegen'd `react_codegen_RNDiscordMarkdownSpec` target.
cmake_minimum_required(VERSION 3.13)

add_library(discordmarkdown_cxxmodule
	STATIC
	${CMAKE_CURRENT_SOURCE_DIR}/../cpp/NativeDiscordMarkdown.cpp)

set_target_properties(discordmarkdown_cxxmodule PROPERTIES POSITION_INDEPENDENT_CODE ON)

target_include_directories(discordmarkdown_cxxmodule PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../cpp)

# The Rust parser, cross-compiled by the cargoBuildRust Gradle task when building inside the
# discord/markdown repo, or shipped prebuilt in the npm package.
add_library(discord_markdown_c STATIC IMPORTED)
set_target_properties(discord_markdown_c PROPERTIES
	IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/prebuilt/${ANDROID_ABI}/libdiscord_markdown_c.a)

# Plain (non-keyword) signature: React Native's ReactNative-application.cmake links
# `common_flags` into every autolinked target with the plain signature, and CMake forbids
# mixing the two forms on one target.
target_link_libraries(discordmarkdown_cxxmodule
	discord_markdown_c
	jsi
	reactnative
	react_codegen_RNDiscordMarkdownSpec)

# React Native's compile flags (folly options and friends), defined by the app-level React
# Native CMake setup that includes this file.
if(COMMAND target_compile_reactnative_options)
	target_compile_reactnative_options(discordmarkdown_cxxmodule PRIVATE)
endif()
