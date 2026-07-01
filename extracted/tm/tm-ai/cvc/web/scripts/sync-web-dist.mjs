// Distributes the freshly-built `cvc/web_dist/` to every location that
// `cvc gateway` may load it from at runtime.
//
// Why this exists
// ---------------
// CVC's Python package (`tm-ai` per pyproject.toml) gets installed in
// TWO places on a typical Jai dev setup:
//   1. `<repo>/.venv/lib/python3.12/site-packages/cvc/web_dist/`
//      — managed by `uv sync` / pip editable installs.
//   2. `/Users/jkm/.local/share/uv/tools/tm-ai/lib/python3.13/site-packages/cvc/web_dist/`
//      — the `uv tool install` location used by the gateway daemon
//      process (PID 40295 on port 13421).
//
// `npm run build` writes to `cvc/web_dist/` (the source tree) but does
// NOT push to either install location. Without this script the running
// daemon continues serving the OLD compiled bundle + assets, which is
// why a `git pull` + `npm run build` can feel like it "didn't take"
// even though disk has the right files.
//
// Idempotent + safe to re-run. Uses `rsync --delete` so deletions in
// the source tree propagate (e.g. when a font gets dropped). Both
// target directories must exist; we mkdir -p them defensively.

import { execSync } from "node:child_process";
import { existsSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
// scripts/ is at <repo>/cvc/web/scripts/, so .parent.parent is <repo>/cvc/
// and .parent.parent.parent is <repo>/.
const REPO_ROOT = resolve(__dirname, "..", "..", "..");
const SOURCE = resolve(REPO_ROOT, "cvc", "web_dist");

// Best-effort discovery: read the active venv + the uv tool install
// location from environment, fall back to platform defaults.
const candidates = [
  process.env.CVC_VENV_WEB_DIST,                              // explicit override
  resolve(REPO_ROOT, ".venv/lib/python3.12/site-packages/cvc/web_dist"),
  "/Users/jkm/.local/share/uv/tools/tm-ai/lib/python3.13/site-packages/cvc/web_dist",
  "/Users/jkm/.local/share/uv/tools/tm-ai/lib/python3.12/site-packages/cvc/web_dist",
].filter(Boolean);

if (!existsSync(SOURCE)) {
  console.warn(`[sync-web-dist] source not found: ${SOURCE}`);
  console.warn(`[sync-web-dist] run 'npm run build' first.`);
  process.exit(0);
}

let synced = 0;
let skipped = 0;

for (const target of candidates) {
  if (target === SOURCE) continue;
  if (!existsSync(dirname(target))) {
    // No parent — skip silently. The user just hasn't installed
    // CVC at this location.
    skipped++;
    continue;
  }
  try {
    mkdirSync(target, { recursive: true });
    execSync(`rsync -a --delete "${SOURCE}/" "${target}/"`, {
      stdio: ["ignore", "pipe", "pipe"],
    });
    console.log(`[sync-web-dist] → ${target}`);
    synced++;
  } catch (err) {
    console.error(`[sync-web-dist] FAILED → ${target}: ${err.message}`);
  }
}

if (synced === 0) {
  console.log(
    `[sync-web-dist] no install targets found (skipped ${skipped}). ` +
      `If you installed CVC elsewhere, set CVC_VENV_WEB_DIST.`,
  );
} else {
  console.log(`[sync-web-dist] synced ${synced} target(s).`);
}