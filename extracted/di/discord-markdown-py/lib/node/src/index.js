import { createRequire } from "node:module";
import { arch, platform } from "node:os";

const require = createRequire(import.meta.url);
const pkg = `@discord/markdown-node-${platform()}-${arch()}`;

export { Syntax } from "@discord/markdown-types";

// `parse(content, flags?, fuel?)`: `flags` is a bitwise OR of `Syntax` members, and defaults to
// `Syntax.ALL`, which `0` also means.
export const { parse, unparse } = require(pkg);
