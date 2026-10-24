import { Syntax, parse } from "@discord/markdown-wasm/async";
import { expect, test } from "vitest";

test("simple parse", async () => {
	expect(await parse("foo")).toEqual([
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

test("parse with flags", async () => {
	expect(await parse("_foo_ **bar**", Syntax.ITALIC)).toEqual([
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

test("parse mention as bigint", async () => {
	expect(await parse("<@1234>")).toEqual([
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

test("flags remove syntax with a mask", async () => {
	expect(await parse("@everyone", Syntax.ALL & ~Syntax.MENTIONS)).toEqual([
		{ type: "paragraph", value: [{ type: "text", value: "@everyone" }] },
	]);
});

test("every bit set allows everything", async () => {
	expect(await parse("**foo**", ~0)).toEqual(await parse("**foo**"));
});

test("no bit set allows everything", async () => {
	expect(await parse("**foo**", 0)).toEqual(await parse("**foo**"));
});
