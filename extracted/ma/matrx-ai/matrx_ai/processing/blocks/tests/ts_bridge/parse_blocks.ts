/**
 * parse_blocks.ts — TypeScript bridge for block parsing comparison.
 *
 * Reads markdown content from stdin (or a file path passed as the first CLI
 * argument), runs it through splitContentIntoBlocksV2 (the production frontend
 * parser), and writes the resulting MessageBlock[] as JSON to stdout.
 *
 * Usage:
 *   echo "content" | npx tsx --tsconfig /path/to/matrx-frontend/tsconfig.json parse_blocks.ts
 *   npx tsx --tsconfig /path/to/matrx-frontend/tsconfig.json parse_blocks.ts /path/to/file.md
 *   ... parse_blocks.ts /path/to/file.md --out /path/to/blocks.json
 *
 * The script is invoked by tests/parity/harness.py (the CI parity gate) and by
 * block_tester.py via subprocess.
 *
 * --out is REQUIRED for machine consumption: imported FE modules log to stdout
 * (kind parsers print diagnostics), so stdout is NOT a reliable JSON channel.
 * With --out the JSON is written to that file and stdout may contain anything.
 *
 * NOTE: This script MUST be run from within the matrx-frontend repo root
 * (or with --tsconfig pointing to it) so that the @/ path alias resolves.
 */

import * as fs from "fs";
import * as path from "path";
import * as readline from "readline";

// The import uses the @/ alias — tsx resolves it via the tsconfig paths mapping.
import { splitContentIntoBlocksV2 } from "@/components/mardown-display/markdown-classification/processors/utils/content-splitter-v2";

async function readStdin(): Promise<string> {
  return new Promise((resolve, reject) => {
    let data = "";
    const rl = readline.createInterface({ input: process.stdin });
    rl.on("line", (line) => {
      data += line + "\n";
    });
    rl.on("close", () => resolve(data));
    rl.on("error", reject);
  });
}

async function main(): Promise<void> {
  let content: string;

  const argv = process.argv.slice(2);
  const outIdx = argv.indexOf("--out");
  const outPath = outIdx !== -1 ? argv[outIdx + 1] : undefined;
  if (outIdx !== -1 && !outPath) {
    process.stderr.write("[parse_blocks.ts] ERROR: --out requires a path\n");
    process.exit(1);
  }
  const filePaths = argv.filter((a, n) => n !== outIdx && n !== outIdx + 1);

  // Batch mode: 2+ file paths -> { [absolutePath]: SplitterBlock[] }. One tsx
  // startup for a whole fixture corpus (the parity gate's hot path).
  if (filePaths.length > 1) {
    const batch: Record<string, unknown> = {};
    for (const fp of filePaths) {
      const resolved = path.resolve(fp);
      if (!fs.existsSync(resolved)) {
        process.stderr.write(`[parse_blocks.ts] ERROR: File not found: ${resolved}\n`);
        process.exit(1);
      }
      batch[resolved] = splitContentIntoBlocksV2(
        fs.readFileSync(resolved, "utf-8"),
      );
    }
    const batchJson = JSON.stringify(batch, null, 2) + "\n";
    if (outPath) fs.writeFileSync(path.resolve(outPath), batchJson, "utf-8");
    else process.stdout.write(batchJson);
    return;
  }

  const filePath = filePaths[0];
  if (filePath) {
    const resolved = path.resolve(filePath);
    if (!fs.existsSync(resolved)) {
      process.stderr.write(
        `[parse_blocks.ts] ERROR: File not found: ${resolved}\n`,
      );
      process.exit(1);
    }
    content = fs.readFileSync(resolved, "utf-8");
    process.stderr.write(
      `[parse_blocks.ts] Parsing file: ${resolved} (${content.length} chars)\n`,
    );
  } else {
    if (process.stdin.isTTY) {
      process.stderr.write(
        "[parse_blocks.ts] ERROR: No file argument and stdin is a TTY — pipe content or pass a file path.\n",
      );
      process.exit(1);
    }
    content = await readStdin();
    process.stderr.write(
      `[parse_blocks.ts] Parsing stdin (${content.length} chars)\n`,
    );
  }

  try {
    const blocks = splitContentIntoBlocksV2(content);
    process.stderr.write(
      `[parse_blocks.ts] Produced ${blocks.length} block(s)\n`,
    );
    const json = JSON.stringify(blocks, null, 2) + "\n";
    if (outPath) {
      fs.writeFileSync(path.resolve(outPath), json, "utf-8");
    } else {
      process.stdout.write(json);
    }
  } catch (err) {
    process.stderr.write(`[parse_blocks.ts] PARSE ERROR: ${err}\n`);
    process.exit(2);
  }
}

main().catch((err) => {
  process.stderr.write(`[parse_blocks.ts] FATAL: ${err}\n`);
  process.exit(3);
});
