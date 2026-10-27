import assert from "node:assert";
import test from "node:test";

import { Syntax, parse, parseLossless, unparse } from "./src/index.js";

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

test("parse with flags", () => {
	assert.deepStrictEqual(parse("_foo_ **bar**", Syntax.ITALIC), [
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

test("flags remove syntax with a mask", () => {
	assert.deepStrictEqual(parse("@everyone", Syntax.ALL & ~Syntax.MENTIONS), [
		{ type: "paragraph", value: [{ type: "text", value: "@everyone" }] },
	]);
});

test("every bit set allows everything", () => {
	assert.deepStrictEqual(parse("**foo**", ~0), parse("**foo**"));
	// as does no bit set, since no syntax at all would be plain text
	assert.deepStrictEqual(parse("**foo**", 0), parse("**foo**"));
	assert.deepStrictEqual(parse("**foo**", null, 1000), parse("**foo**"));
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

function* tokens(node) {
	for (const child of node.children) {
		if (child.type === "token") yield child;
		else yield* tokens(child);
	}
}

// Characters outside the BMP take two UTF-16 code units, which is where a byte or code point
// offset would drift from a string index.
const LOSSLESS = "🦶 **é** <@873227248453443624>\n> 𝕏 \\*`a`";

test("lossless tokens join into the content, at their spans", () => {
	const node = parseLossless(LOSSLESS);
	assert.deepStrictEqual(node.span, { start: 0, end: LOSSLESS.length });

	let joined = "";
	for (const token of tokens(node)) {
		assert.strictEqual(
			LOSSLESS.slice(token.span.start, token.span.end),
			token.text,
		);
		joined += token.text;
	}
	assert.strictEqual(joined, LOSSLESS);
});

test("lossless takes flags and fuel as parse does", () => {
	// with no asterisk syntax, the asterisks are text
	const text = parseLossless("**a**", Syntax.UNDERLINE).children[0].children[0];
	assert.deepStrictEqual(text.kind, { type: "text", value: "**a**" });
	assert.throws(() => parseLossless("**a**", null, 1), /out of fuel/);
});

test("lossless mentions are bigints", () => {
	const mention = parseLossless("<@1234>").children[0].children[0];
	assert.deepStrictEqual(mention.kind, {
		type: "mention",
		value: { type: "user", value: 1234n },
	});
});
