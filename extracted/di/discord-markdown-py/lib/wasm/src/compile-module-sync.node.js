import { readFileSync } from "node:fs";

const wasmUrl = new URL("./lib/discord_markdown_wasm_bg.wasm", import.meta.url);

export function compileModuleSync() {
	return new WebAssembly.Module(readFileSync(wasmUrl));
}
