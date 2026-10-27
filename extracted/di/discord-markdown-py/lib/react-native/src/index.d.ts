import type { Block, LosslessNode, SyntaxFlags } from "@discord/markdown-types";

export { Syntax, type SyntaxFlags } from "@discord/markdown-types";

/**
 * Parse markdown into an AST.
 *
 * Runs synchronously on the JS thread through a JSI host function backed by the native Rust
 * parser. Throws if the parser rejects the content or if the native module is not linked.
 *
 * `flags` picks the syntax to parse, as a bitwise OR of `Syntax` members, and defaults to
 * `Syntax.ALL`, which `0` also means.
 *
 * `fuel` bounds how much work the parse may do, defaulting to the parser's own budget. Because
 * this runs on the JS thread, a caller handling untrusted content under a frame budget may want
 * a tighter one. Exhausting it throws `parser ran out of fuel` and yields no partial AST, so
 * lowering it too far rejects legitimate content — measure before tightening.
 */
export function parse(
	content: string,
	flags?: SyntaxFlags | null,
	fuel?: number | null,
): Block[];

/**
 * Parse markdown into the lossless tree, for rich text: nodes for what the markdown means, and
 * tokens holding every character of `content` in order, so joining their `text` gives it back
 * exactly. Every span is in UTF-16 code units, so it indexes `content` directly.
 *
 * Runs synchronously on the JS thread, and takes `flags` and `fuel` as {@link parse} does.
 */
export function parseLossless(
	content: string,
	flags?: SyntaxFlags | null,
	fuel?: number | null,
): LosslessNode;

/**
 * Turn an AST back into markdown.
 *
 * Runs synchronously on the JS thread, like {@link parse}, and throws if the AST is malformed or
 * the native module is not linked.
 *
 * Not byte-exact for everything: text is not re-escaped, italics always come back as `_`, and
 * unordered lists always as `* `, and a link written without a scheme comes back with `https://`.
 * Everything else round trips exactly -- including mentions, which are stored as a parsed id and
 * so cannot be rebuilt any other way.
 */
export function unparse(nodes: Block[]): string;
