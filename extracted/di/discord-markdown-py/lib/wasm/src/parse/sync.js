import { loadAndInit } from "../init.js";
import { parse as rawParse } from "../lib/discord_markdown_wasm.js";

await loadAndInit();

export function parse(content, allowedRules) {
	return rawParse(content, allowedRules);
}
