import {
	Syntax,
	init,
	parse,
	parseLossless,
	unparse,
} from "@discord/markdown-wasm";
import { beforeAll, expect, test } from "vitest";

// Node initialises itself on first use; the browser cannot.
beforeAll(() => init());

test("simple parse", () => {
	expect(parse("foo")).toEqual([
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
	expect(parse("_foo_ **bar**", Syntax.ITALIC)).toEqual([
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
	expect(parse("<@1234>")).toEqual([
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

// Unparsing is exposed because the AST keeps parsed values, not the text a node came from. A
// mention covers the bigint path.
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
		expect(unparse(parse(content))).toBe(content);
	}
});

test("unparse rejects a malformed ast", () => {
	expect(() => unparse([{ type: "nonsense" }])).toThrow();
});

test("flags remove syntax with a mask", () => {
	expect(parse("@everyone", Syntax.ALL & ~Syntax.MENTIONS)).toEqual([
		{ type: "paragraph", value: [{ type: "text", value: "@everyone" }] },
	]);
});

test("every bit set allows everything", () => {
	expect(parse("**foo**", ~0)).toEqual(parse("**foo**"));
});

test("no bit set allows everything", () => {
	expect(parse("**foo**", 0)).toEqual(parse("**foo**"));
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
	expect(node.span).toEqual({ start: 0, end: LOSSLESS.length });

	let joined = "";
	for (const token of tokens(node)) {
		expect(LOSSLESS.slice(token.span.start, token.span.end)).toBe(token.text);
		joined += token.text;
	}
	expect(joined).toBe(LOSSLESS);
});

test("lossless keeps the syntax as written", () => {
	const paragraph = parseLossless("*a* \\_").children[0];
	const [italic, text] = paragraph.children;
	expect(italic.kind).toEqual({
		type: "modifier",
		value: { kind: "italic", id: 0 },
	});
	expect(italic.children[0]).toEqual({
		type: "token",
		kind: { type: "delimiter", value: { kind: "italic", id: 0, side: "open" } },
		text: "*",
		span: { start: 0, end: 1 },
	});
	expect(text.kind).toEqual({ type: "text", value: " _" });
	expect(text.children.map((token) => [token.kind.type, token.text])).toEqual([
		["text", " "],
		["escape", "\\"],
		["text", "_"],
	]);
});

test("lossless mentions are bigints", () => {
	const mention = parseLossless("<@1234>").children[0].children[0];
	expect(mention.kind).toEqual({
		type: "mention",
		value: { type: "user", value: 1234n },
	});
});
