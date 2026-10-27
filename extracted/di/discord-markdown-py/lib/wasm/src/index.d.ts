import type { Block, Inline } from "@discord/markdown-types";

export * from "./parse.js";

export function iter(nodes: Block[] | Inline[]): Iterable<Block | Inline>;
