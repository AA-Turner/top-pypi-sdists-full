import {
	initSync as initWasmSync,
	loadAndInit,
	loadModuleSync,
} from "../init.js";
import {
	parse as rawParse,
	unparse as rawUnparse,
} from "../lib/discord_markdown_wasm.js";

let ready = false;
let initPromise = null;

export function init() {
	if (ready) return Promise.resolve();

	initPromise ??= loadAndInit().then(
		() => {
			ready = true;
		},
		(e) => {
			initPromise = null;
			throw e;
		},
	);

	return initPromise;
}

export function initSync(wasmModule) {
	initWasmSync(wasmModule);
	ready = true;
}

// Node reads and compiles the wasm synchronously, so the first call can initialise itself.
// Nowhere else can, so those callers have to init ahead of time.
function ensureReady() {
	if (ready) return;

	const wasmModule = loadModuleSync();
	if (!wasmModule) {
		throw new Error(
			"@discord/markdown-wasm/sync is not initialised. Await init() once before parsing, or hand already-compiled wasm to initSync().",
		);
	}

	initWasmSync(wasmModule);
	ready = true;
}

export function parse(content, allowedRules) {
	ensureReady();
	return rawParse(content, allowedRules);
}

export function unparse(nodes) {
	ensureReady();
	return rawUnparse(nodes);
}
