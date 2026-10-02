import { playwright } from "@vitest/browser-playwright";
import { defineConfig } from "vitest/config";

export default defineConfig({
	test: {
		projects: [
			{
				test: {
					name: "browser",
					include: ["src/**/*.test.js"],
					exclude: ["src/**/*.node.test.js"],
					browser: {
						enabled: true,
						provider: playwright(),
						instances: [{ browser: "chromium" }],
					},
				},
			},
			{
				test: {
					name: "node",
					include: ["src/**/*.test.js"],
				},
			},
		],
	},
});
