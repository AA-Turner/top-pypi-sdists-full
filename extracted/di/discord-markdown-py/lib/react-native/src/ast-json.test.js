import { expect, test } from "vitest";
import { decodeAstJson, encodeAstJson } from "./ast-json.js";

test("revives $bigint wrappers as BigInts", () => {
	const json =
		'[{"type":"paragraph","value":[{"type":"mention","value":{"type":"user","value":{"$bigint":"873227248453443624"}}}]}]';
	expect(decodeAstJson(json)).toStrictEqual([
		{
			type: "paragraph",
			value: [
				{
					type: "mention",
					value: { type: "user", value: 873227248453443624n },
				},
			],
		},
	]);
});

test("revives nested $bigint wrappers", () => {
	const json =
		'[{"type":"timestamp","value":{"value":{"$bigint":"1234567890"},"style":"R"}}]';
	expect(decodeAstJson(json)).toStrictEqual([
		{ type: "timestamp", value: { value: 1234567890n, style: "R" } },
	]);
});

test("leaves plain numbers untouched", () => {
	const json = '[{"type":"heading","value":{"level":1,"content":[]}}]';
	expect(decodeAstJson(json)).toStrictEqual([
		{ type: "heading", value: { level: 1, content: [] } },
	]);
});

test("leaves text content containing $bigint syntax untouched", () => {
	// A message whose literal text mentions the wrapper syntax is still just a string.
	const json =
		'[{"type":"paragraph","value":[{"type":"text","value":"{\\"$bigint\\":\\"1\\"}"}]}]';
	expect(decodeAstJson(json)).toStrictEqual([
		{ type: "paragraph", value: [{ type: "text", value: '{"$bigint":"1"}' }] },
	]);
});

test("values above Number.MAX_SAFE_INTEGER keep full precision", () => {
	const json = '{"$bigint":"18446744073709551615"}';
	expect(decodeAstJson(json)).toBe(18446744073709551615n);
});

test("re-wraps BigInts on the way out", () => {
	expect(
		encodeAstJson([
			{
				type: "paragraph",
				value: [
					{
						type: "mention",
						value: { type: "user", value: 873227248453443624n },
					},
				],
			},
		]),
	).toBe(
		'[{"type":"paragraph","value":[{"type":"mention","value":{"type":"user","value":{"$bigint":"873227248453443624"}}}]}]',
	);
});

test("encode and decode are inverses", () => {
	for (const nodes of [
		[{ type: "heading", value: { level: 1, content: [] } }],
		[{ type: "timestamp", value: { value: 1234567890n, style: "R" } }],
		[
			{
				type: "paragraph",
				value: [{ type: "text", value: '{"$bigint":"1"}' }],
			},
		],
		[
			{
				type: "mention",
				value: { type: "user", value: 18446744073709551615n },
			},
		],
	]) {
		expect(decodeAstJson(encodeAstJson(nodes))).toStrictEqual(nodes);
	}
});
