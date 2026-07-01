import { init } from "../../init.js";
import { parse as rawParse } from "../../lib/discord_markdown_wasm.js";
import { INIT, PARSE } from "./messages.js";

async function handleInit(wasmModule) {
	await init(wasmModule);
	self.postMessage({ type: INIT });
}

function handleParse(content, allowedRules) {
	const result = rawParse(content, allowedRules);
	self.postMessage({ type: PARSE, result });
}

self.onmessage = (event) => {
	switch (event.data.type) {
		case INIT:
			void handleInit(event.data.module);
			break;
		case PARSE:
			handleParse(event.data.content, event.data.allowedRules);
			break;
	}
};
