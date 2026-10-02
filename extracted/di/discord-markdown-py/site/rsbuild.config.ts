import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { defineConfig } from "@rsbuild/core";
import { pluginReact } from "@rsbuild/plugin-react";

// @grafana/ui fetches icons as individual SVGs at render time rather than bundling them. They
// ship inside the package, so serve them ourselves; see GRAFANA_PUBLIC_PATH in src/index.tsx for
// the other half of this.
const grafanaIcons = join(
	dirname(createRequire(import.meta.url).resolve("@grafana/ui/package.json")),
	"dist/public/img/icons",
);

export default defineConfig({
	plugins: [pluginReact()],
	html: {
		title: "Discord Markdown",
	},
	server: {
		headers: {
			"Cross-Origin-Opener-Policy": "same-origin",
			"Cross-Origin-Embedder-Policy": "require-corp",
		},
	},
	output: {
		copy: [{ from: grafanaIcons, to: "grafana/img/icons" }],
	},
	tools: {
		rspack: {
			module: {
				rules: [
					{
						// @grafana/ui and @grafana/flamegraph ship .mjs, but were built assuming
						// Babel-style CommonJS interop: they default-import packages that set
						// `exports.default`. rspack reads .mjs as real ESM, where that instead
						// yields the whole `module.exports` object, and React refuses to render
						// the object it gets handed. Parsing them as javascript/auto restores the
						// interop they were built against.
						test: /\.mjs$/,
						include: /node_modules[\\/]@grafana[\\/]/,
						type: "javascript/auto",
					},
				],
			},
		},
	},
	resolve: {
		alias: {
			"react-dom$": "react-dom/profiling",
		},
	},
});
