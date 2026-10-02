import { createRequire } from "node:module";
import { expect, test } from "vitest";

// What the sync entry point gives up top-level await for: a top-level await anywhere in the graph
// makes require() throw ERR_REQUIRE_ASYNC_MODULE. This also covers Node initialising on first use,
// since a fresh require() has never seen init().
test("require() works and parses without an explicit init", () => {
	const require = createRequire(import.meta.url);
	const { parse } = require("./sync.js");

	expect(parse("foo")).toEqual([
		{ type: "paragraph", value: [{ type: "text", value: "foo" }] },
	]);
});
