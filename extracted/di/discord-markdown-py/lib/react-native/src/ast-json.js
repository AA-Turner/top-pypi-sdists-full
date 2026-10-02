/**
 * Decodes the JSON AST emitted by the native parser.
 *
 * 64-bit integers (snowflake IDs, timestamp values) cross the JSI boundary as
 * `{"$bigint": "…"}` wrapper objects, because `JSON.parse` would otherwise read them as lossy
 * float64 numbers. This revives them into `BigInt`s, so the decoded AST matches
 * `@discord/markdown-types` exactly like the wasm binding's output does.
 */
export function decodeAstJson(json) {
	return JSON.parse(json, reviveBigInts);
}

function reviveBigInts(_key, value) {
	if (typeof value === "object" && value !== null && "$bigint" in value) {
		return BigInt(value.$bigint);
	}
	return value;
}

/**
 * Encodes an AST for the native unparser, the inverse of {@link decodeAstJson}.
 *
 * `JSON.stringify` throws outright on a `BigInt`, so the values `decodeAstJson` revived have to
 * go back into their `{"$bigint": "…"}` wrappers.
 */
export function encodeAstJson(nodes) {
	return JSON.stringify(nodes, replaceBigInts);
}

function replaceBigInts(_key, value) {
	if (typeof value === "bigint") {
		return { $bigint: value.toString() };
	}
	return value;
}
