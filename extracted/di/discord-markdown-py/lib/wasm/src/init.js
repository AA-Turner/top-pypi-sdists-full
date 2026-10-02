import { compileModule } from "#compile-module";
import { compileModuleSync } from "#compile-module-sync";
import initWasm, {
	initSync as initWasmSync,
} from "./lib/discord_markdown_wasm.js";

let _wasmModule;
export async function loadModule() {
	if (!_wasmModule) {
		_wasmModule = await compileModule();
	}

	return _wasmModule;
}

/** The compiled module, or null where it cannot be had without awaiting. */
export function loadModuleSync() {
	if (!_wasmModule) {
		_wasmModule = compileModuleSync();
	}

	return _wasmModule;
}

export function init(wasmModule) {
	return initWasm({ module_or_path: wasmModule });
}

export function initSync(wasmModule) {
	return initWasmSync({ module: wasmModule });
}

export async function loadAndInit() {
	const wasmModule = await loadModule();
	return init(wasmModule);
}
