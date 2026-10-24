import { Syntax, init, parse, unparse } from "@discord/markdown-wasm/sync";
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
