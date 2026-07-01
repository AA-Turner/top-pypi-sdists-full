import { createRequire } from "node:module";
import { arch, platform } from "node:os";

const require = createRequire(import.meta.url);
const pkg = `@discord/markdown-node-${platform()}-${arch()}`;

export const { parse } = require(pkg);
