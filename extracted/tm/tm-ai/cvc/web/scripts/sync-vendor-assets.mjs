// Copies vendored Nous UI fonts/assets into public/ so they're served by Vite
// at /fonts/* and /ds-assets/*, mirroring the upstream `sync-assets` script.
import { cp, rm, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, "..");
const VENDOR = resolve(ROOT, "src/vendor/nous-ui");
const PUBLIC = resolve(ROOT, "public");

const PAIRS = [
  ["fonts", "fonts"],
  ["assets", "ds-assets"],
];

await mkdir(PUBLIC, { recursive: true });

for (const [from, to] of PAIRS) {
  const src = resolve(VENDOR, from);
  const dst = resolve(PUBLIC, to);
  if (!existsSync(src)) {
    console.warn(`[sync-vendor-assets] missing ${src} — skipping`);
    continue;
  }
  await rm(dst, { recursive: true, force: true });
  await cp(src, dst, { recursive: true });
  console.log(`[sync-vendor-assets] ${from} → public/${to}`);
}
