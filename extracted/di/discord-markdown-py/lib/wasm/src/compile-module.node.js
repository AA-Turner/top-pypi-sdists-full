import { readFile } from "node:fs/promises";

const wasmUrl = new URL("./lib/discord_markdown_wasm_bg.wasm", import.meta.url);

export async function compileModule() {
	return WebAssembly.compile(await readFile(wasmUrl));
}
