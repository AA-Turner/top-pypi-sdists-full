import type { Block, Rule } from "@discord/markdown-types";

export function parse(
	content: string,
	allowedRules?: Rule[] | null,
	options?: { signal?: AbortSignal },
): Promise<Block[]>;
