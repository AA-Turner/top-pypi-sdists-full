import NativeDiscordMarkdown from "./NativeDiscordMarkdown";
import { decodeAstJson, encodeAstJson } from "./ast-json.js";

export { Syntax } from "@discord/markdown-types";

export function parse(content, flags, fuel) {
	return decodeAstJson(
		NativeDiscordMarkdown.parseToAstString(
			content,
			// Codegen maps only `undefined` to an absent argument; a `null` would reach
			// `asNumber()` and throw from JSI.
			flags ?? undefined,
			fuel ?? undefined,
		),
	);
}

export function parseLossless(content, flags, fuel) {
	return decodeAstJson(
		NativeDiscordMarkdown.parseLosslessToAstString(
			content,
			flags ?? undefined,
			fuel ?? undefined,
		),
	);
}

export function unparse(nodes) {
	return NativeDiscordMarkdown.unparseFromAstString(encodeAstJson(nodes));
}
