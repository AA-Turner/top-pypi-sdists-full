import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";
import fs from "node:fs";

const BACKEND = process.env.CVC_GATEWAY_URL ?? "http://127.0.0.1:9119";

// Vendored Nous Research UI: alias `@nous-research/ui/...` imports to
// `cvc/web/src/vendor/nous-ui/...`. No npm dep at install time.
const NOUS_UI_DIR = path.resolve(__dirname, "./src/vendor/nous-ui");

// ── v2.86.0: dynamic version injection ──────────────────────────────────────
// Read the canonical CVC version from the repo's pyproject.toml at build time
// so every `npm run build` after a Python version bump automatically ships the
// new version in the UI. No manual sync of cvc/web/package.json required.
// Falls back to package.json then "0.0.0-dev" if pyproject can't be parsed.
function readCvcVersion(): string {
  const pyproject = path.resolve(__dirname, "../../pyproject.toml");
  try {
    const txt = fs.readFileSync(pyproject, "utf8");
    const m = txt.match(/^\s*version\s*=\s*["']([^"']+)["']/m);
    if (m && m[1]) return m[1];
  } catch {
    /* fallthrough */
  }
  try {
    const pkg = JSON.parse(
      fs.readFileSync(path.resolve(__dirname, "package.json"), "utf8"),
    );
    if (pkg.version) return pkg.version as string;
  } catch {
    /* fallthrough */
  }
  return "0.0.0-dev";
}

const CVC_VERSION = readCvcVersion();

export default defineConfig({
  plugins: [react(), tailwindcss()],
  define: {
    __CVC_VERSION__: JSON.stringify(CVC_VERSION),
  },
  resolve: {
    alias: [
      { find: "@/", replacement: path.resolve(__dirname, "./src") + "/" },
      // Match `@nous-research/ui/...` deep imports (utils, hooks, components)
      {
        find: /^@nous-research\/ui$/,
        replacement: path.resolve(NOUS_UI_DIR, "index.js"),
      },
      {
        find: /^@nous-research\/ui\/(.+)$/,
        replacement: path.resolve(NOUS_UI_DIR, "$1") + ".js",
      },
    ],
    dedupe: ["react", "react-dom", "three"],
  },
  build: {
    outDir: path.resolve(__dirname, "../web_dist"),
    emptyOutDir: true,
  },
  server: {
    port: 9120,
    proxy: {
      "/api": { target: BACKEND, ws: true, changeOrigin: true },
    },
  },
});
