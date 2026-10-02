import assert from "node:assert";
import test from "node:test";

import { parse, unparse } from "./src/index.js";

test("simple parse", () => {
	assert.deepStrictEqual(parse("foo"), [
		{
			type: "paragraph",
			value: [
				{
					type: "text",
					value: "foo",
				},
			],
		},
	]);
});

test("parse with allowed_rules", () => {
	assert.deepStrictEqual(parse("_foo_ **bar**", ["italic"]), [
		{
			type: "paragraph",
			value: [
				{
					type: "italic",
					value: [
						{
							type: "text",
							value: "foo",
						},
					],
				},
				{
					type: "text",
					value: " *",
				},
				{
					type: "italic",
					value: [
						{
							type: "text",
							value: "bar",
						},
					],
				},
				{
					type: "text",
					value: "*",
				},
			],
		},
	]);
});

test("parse mention as bigint", () => {
	assert.deepStrictEqual(parse("<@1234>"), [
		{
			type: "paragraph",
			value: [
				{
					type: "mention",
					value: {
						type: "user",
						value: 1234n,
					},
				},
			],
		},
	]);
});

// A mention link is why unparsing is exposed at all: the AST keeps the parsed resource, not the
// text. A mention covers the bigint path.
const ROUND_TRIPS = [
	"# Hello **world**",
	"> quote with `code` and ||spoilers||",
	"<@873227248453443624>",
	"<t:1234567890:R>",
	"<:pepe:873227248453443624>",
	"https://discord.com/channels/1/2",
	"[text](https://example.com/)",
];

test("unparse round trips", () => {
	for (const content of ROUND_TRIPS) {
		assert.strictEqual(unparse(parse(content)), content, content);
	}
});

test("unparse rejects a malformed ast", () => {
	assert.throws(() => unparse([{ type: "nonsense" }]));
});
