import { beforeEach, expect, test, vi } from "vitest";

// The real module reaches for the native TurboModule at import time, which only exists inside a
// React Native runtime. Stubbing it lets us test the wrapper's own job: what it forwards across
// the JSI boundary. The parser itself is tested in `cargo test -p discord-markdown-c`.
const parseToAstString = vi.fn(() => "[]");
const unparseFromAstString = vi.fn(() => "");
vi.mock("./NativeDiscordMarkdown", () => ({
	default: {
		parseToAstString: (...args) => parseToAstString(...args),
		unparseFromAstString: (...args) => unparseFromAstString(...args),
	},
}));

const { parse, unparse } = await import("./index.js");

beforeEach(() => {
	parseToAstString.mockClear();
	unparseFromAstString.mockClear();
});

test("forwards content alone when nothing else is given", () => {
	parse("**foo**");
	expect(parseToAstString).toHaveBeenCalledWith(
		"**foo**",
		undefined,
		undefined,
	);
});

test("serialises allowed rules and forwards fuel", () => {
	parse("**foo**", ["bold"], 1000);
	expect(parseToAstString).toHaveBeenCalledWith("**foo**", '["bold"]', 1000);
});

// Codegen turns an argument into `std::nullopt` only for `undefined`; a `null` would reach
// `asNumber()`/`asString()` and throw from JSI. Both have to be normalised here.
test("normalises null to undefined", () => {
	parse("**foo**", null, null);
	expect(parseToAstString).toHaveBeenCalledWith(
		"**foo**",
		undefined,
		undefined,
	);
});

test("forwards fuel without allowed rules", () => {
	parse("**foo**", null, 1);
	expect(parseToAstString).toHaveBeenCalledWith("**foo**", undefined, 1);
});

test("forwards an explicit zero rather than dropping it", () => {
	// `0` is falsy, so a `||` in the wrapper would silently turn it into the default budget.
	parse("**foo**", null, 0);
	expect(parseToAstString).toHaveBeenCalledWith("**foo**", undefined, 0);
});

test("decodes the AST the native module returns", () => {
	parseToAstString.mockReturnValueOnce(
		'[{"type":"mention","value":{"type":"user","value":{"$bigint":"873227248453443624"}}}]',
	);
	expect(parse("<@873227248453443624>")).toStrictEqual([
		{ type: "mention", value: { type: "user", value: 873227248453443624n } },
	]);
});

test("encodes the AST it hands to the native module", () => {
	unparse([
		{ type: "mention", value: { type: "user", value: 873227248453443624n } },
	]);
	expect(unparseFromAstString).toHaveBeenCalledWith(
		'[{"type":"mention","value":{"type":"user","value":{"$bigint":"873227248453443624"}}}]',
	);
});

test("returns the markdown the native module produced", () => {
	unparseFromAstString.mockReturnValueOnce("**foo**");
	expect(
		unparse([{ type: "bold", value: [{ type: "text", value: "foo" }] }]),
	).toBe("**foo**");
});
