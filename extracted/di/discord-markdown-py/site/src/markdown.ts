import type { Block, Rule } from "@discord/markdown-types";
import init, {
	parse as rawParse,
	profile as rawProfile,
	unparse as rawUnparse,
} from "./wasm/discord_markdown_wasm.js";

// Built by `pnpm build:wasm`, which turns on the crate's `profile` feature. The published
// @discord/markdown-wasm package is built without it, so `profile` exists only here -- which is
// why the site loads this module rather than the package.
const wasmUrl = new URL(
	"./wasm/discord_markdown_wasm_bg.wasm",
	import.meta.url,
);

await init({ module_or_path: wasmUrl });

/** Parse markdown into its AST. */
export function parse(content: string, allowedRules?: Rule[] | null): Block[] {
	return rawParse(content, allowedRules);
}

/**
 * Turn an AST back into markdown.
 *
 * Not byte-exact for everything: text is not re-escaped, italics always come back as `_`, and
 * unordered lists always as `* `.
 */
export function unparse(nodes: Block[]): string {
	return rawUnparse(nodes);
}

/**
 * The parser's call tree for one parse, merged and flattened into the "nested set" layout flame
 * graph renderers consume.
 *
 * Rows are a depth-first pre-order walk, so a row's children are the rows that follow it at one
 * level deeper, up to the next row at its own level or shallower.
 */
export interface Profile {
	/** Span name per row, e.g. `inline_parser`. */
	labels: string[];
	/** Depth per row. Row 0 is the root, at level 0. */
	levels: number[];
	/** Span entries in each row's subtree, the row itself included. */
	values: number[];
	/** Span entries attributed to each row directly, excluding its children. */
	selfValues: number[];
	/** Total entries the parse made, i.e. `values[0]`. */
	total: number;
	/** Why the parse failed, or null if it succeeded. The profile still covers the work it did. */
	error: string | null;
}

/**
 * Parse `content` while recording which parsers ran, and how often.
 *
 * The unit is span entries, not time: a parser span is entered once per parser invocation, so a
 * profile is an exact, deterministic account of the work a parse did. Timing each span instead
 * would tell you very little, because spans average tens of nanoseconds and `performance.now` is
 * quantised to 5µs even under cross-origin isolation. Time the parse as a whole for that.
 *
 * Collecting costs under 2x an ordinary {@link parse}.
 */
export function profile(
	content: string,
	allowedRules?: Rule[] | null,
): Profile {
	return rawProfile(content, allowedRules);
}
