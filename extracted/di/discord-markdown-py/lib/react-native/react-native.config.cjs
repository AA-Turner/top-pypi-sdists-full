/**
 * Registers the pure C++ TurboModule with Android autolinking: the generated
 * `autolinking.cpp` includes `<NativeDiscordMarkdown.h>` and instantiates the module when JS
 * requests it, and the generated autolinking CMake adds `android/CMakeLists.txt` to the
 * app's native build. iOS registration goes through `codegenConfig.ios.modulesProvider` in
 * package.json instead.
 */
module.exports = {
	dependency: {
		platforms: {
			android: {
				cxxModuleCMakeListsPath: "CMakeLists.txt",
				cxxModuleCMakeListsModuleName: "discordmarkdown_cxxmodule",
				cxxModuleHeaderName: "NativeDiscordMarkdown",
			},
		},
	},
};
