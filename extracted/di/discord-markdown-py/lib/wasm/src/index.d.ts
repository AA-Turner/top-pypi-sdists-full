import type { Block, Inline } from "@discord/markdown-types";

export function iter(nodes: Block[] | Inline[]): Iterable<Block | Inline>;
