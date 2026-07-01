import { execSync } from "node:child_process";
import { arch, platform } from "node:os";
import { resolve } from "node:path";

const libPath = resolve("dist", `${platform()}-${arch()}`, "index.node");
const buildCmd =
	"cargo build -p discord-markdown-node --message-format json-render-diagnostics --release";
execSync(
	`pnpm cargo-cp-artifact -a cdylib discord-markdown-node ${libPath} -- ${buildCmd}`,
	{
		stdio: "inherit",
	},
);
