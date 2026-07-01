import assert from "node:assert";
import test from "node:test";

import { parse } from "./src/index.js";

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
