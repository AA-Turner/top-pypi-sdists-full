import NativeDiscordMarkdown from "./NativeDiscordMarkdown";
import { decodeAstJson, encodeAstJson } from "./ast-json.js";

export function parse(content, allowedRules, fuel) {
	return decodeAstJson(
		NativeDiscordMarkdown.parseToAstString(
			content,
			allowedRules == null ? undefined : JSON.stringify(allowedRules),
			// Codegen maps only `undefined` to an absent argument; a `null` would reach
			// `asNumber()` and throw from JSI.
			fuel ?? undefined,
		),
	);
}

export function unparse(nodes) {
	return NativeDiscordMarkdown.unparseFromAstString(encodeAstJson(nodes));
}
