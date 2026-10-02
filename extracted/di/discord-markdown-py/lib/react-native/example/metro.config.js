const path = require("node:path");
const { getDefaultConfig, mergeConfig } = require("@react-native/metro-config");

const workspaceRoot = path.resolve(__dirname, "../../..");

/**
 * Metro configuration
 * https://reactnative.dev/docs/metro
 *
 * Watches the whole pnpm workspace so Metro resolves @discord/markdown-react-native (and its
 * dependencies in the root node_modules) through the workspace symlinks.
 *
 * @type {import('@react-native/metro-config').MetroConfig}
 */
const config = {
	watchFolders: [workspaceRoot],
	resolver: {
		nodeModulesPaths: [
			path.resolve(__dirname, "node_modules"),
			path.resolve(workspaceRoot, "node_modules"),
		],
	},
};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);
