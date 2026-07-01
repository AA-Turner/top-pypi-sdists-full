import { playwright } from "@vitest/browser-playwright";
import { defineConfig } from "vite";

export default defineConfig({
	test: {
		setupFiles: ["vitest.setup.js"],
		browser: {
			enabled: true,
			provider: playwright(),
			instances: [{ browser: "chromium" }],
		},
	},
});
