import type { Block, Rule } from "@discord/markdown-types";

/**
 * Compile and instantiate the wasm.
 *
 * Only needed outside Node, where the bytes cannot be read without awaiting: Node initialises
 * itself on the first {@link parse} or {@link unparse}. Repeat calls are a no-op.
 *
 * This module has no top-level await, so importing it never makes the graph async.
 */
export function init(): Promise<void>;

/**
 * Instantiate from wasm you already hold, e.g. a module your bundler or host handed you.
 *
 * Prefer a `WebAssembly.Module`. Browsers refuse to compile buffers over 4KB synchronously on
 * the main thread, so passing bytes there throws.
 */
export function initSync(wasmModule: WebAssembly.Module | BufferSource): void;

/** Throws if the wasm is not initialised. See {@link init}. */
export function parse(content: string, allowedRules?: Rule[] | null): Block[];

/**
 * Turn an AST back into markdown. Throws if the AST is malformed.
 *
 * Not byte-exact for everything: text is not re-escaped, italics always come back as `_`, and
 * unordered lists always as `* `, and a link written without a scheme comes back with `https://`.
 * Everything else round trips exactly -- including mentions, which are stored as a parsed id and
 * so cannot be rebuilt any other way.
 *
 * Throws if the wasm is not initialised. See {@link init}.
 */
export function unparse(nodes: Block[]): string;
