import { expect, test } from "vitest";
import { iter } from ".";

test("is iterable", () => {
	expect(iter([])[Symbol.iterator]).toBeTypeOf("function");
});

test("basic bold", () => {
	const text = {
		type: "text",
		value: "foo",
	};

	const bold = {
		type: "bold",
		value: [text],
	};

	const paragraph = {
		type: "paragraph",
		value: [bold],
	};

	const nodes = iter([paragraph]);
	const allNodes = Array.from(nodes);

	expect(allNodes).toStrictEqual([paragraph, bold, text]);
});

test("list with content", () => {
	const content1Content = {
		type: "text",
		value: "foo",
	};

	const content1 = {
		type: "paragraph",
		value: [content1Content],
	};

	const content2Content = {
		type: "text",
		value: "bar",
	};

	const content2 = {
		type: "paragraph",
		value: [content2Content],
	};

	const list = {
		type: "list",
		value: {
			type: "unordered",
			items: [
				{
					content: [content1, content2],
				},
			],
		},
	};

	const nodes = iter([list]);
	const allNodes = Array.from(nodes);

	expect(allNodes).toStrictEqual([
		list,
		content1,
		content1Content,
		content2,
		content2Content,
	]);
});

test("basic subtext", () => {
	const content = {
		type: "text",
		value: "foo",
	};

	const subtext = {
		type: "subtext",
		value: {
			content: [content],
		},
	};

	const nodes = iter([subtext]);
	const allNodes = Array.from(nodes);

	expect(allNodes).toStrictEqual([subtext, content]);
});
