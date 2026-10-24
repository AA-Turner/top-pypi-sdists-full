import type { Block, SyntaxFlags } from "@discord/markdown-types";

export { Syntax, type SyntaxFlags } from "@discord/markdown-types";

/**
 * Parse markdown into an AST on a worker. `flags` picks the syntax to parse, as a bitwise OR of
 * `Syntax` members, and defaults to `Syntax.ALL`, which `0` also means.
 */
export function parse(
	content: string,
	flags?: SyntaxFlags | null,
	options?: { signal?: AbortSignal },
): Promise<Block[]>;
