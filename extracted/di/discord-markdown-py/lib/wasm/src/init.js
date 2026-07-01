import initWasm from "./lib/discord_markdown_wasm.js";

const wasmUrl = new URL("./lib/discord_markdown_wasm_bg.wasm", import.meta.url);

let _wasmModule;
export async function loadModule() {
	if (!_wasmModule) {
		_wasmModule = await WebAssembly.compileStreaming(fetch(wasmUrl));
	}

	return _wasmModule;
}

export function init(wasmModule) {
	return initWasm({ module_or_path: wasmModule });
}

export async function loadAndInit() {
	const wasmModule = await loadModule();
	return init(wasmModule);
}
