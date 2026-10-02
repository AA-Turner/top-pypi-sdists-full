const wasmUrl = new URL("./lib/discord_markdown_wasm_bg.wasm", import.meta.url);

export function compileModule() {
	return WebAssembly.compileStreaming(fetch(wasmUrl));
}
