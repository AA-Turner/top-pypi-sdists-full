import { readFileSync } from "node:fs";
import { Bench, hrtimeNow } from "tinybench";

import { parse } from "./src/index.js";

const bench = new Bench({
	name: "parse",
	now: hrtimeNow,
	warmupTime: 3_000,
});

for (const name of [
	"ddevs_announcement",
	"discordjs_announcement",
	"helldivers_announcement",
]) {
	const content = readFileSync(
		`../../test_content/${name}/content.md`,
		"utf-8",
	);

	bench.add(name, () => parse(content));
}

await bench.run();

console.log(bench.name);
console.table(bench.table());
