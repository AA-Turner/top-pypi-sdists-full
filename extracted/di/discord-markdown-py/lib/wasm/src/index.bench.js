import { readFile } from "node:fs/promises";
import { bench } from "vitest";

import { parse } from ".";

for (const name of [
	"ddevs_announcement",
	"helldivers_announcement",
	"discordjs_announcement",
]) {
	const content = await readFile(
		`../../test_content/${name}/content.md`,
		"utf-8",
	);
	bench(name, () => {
		parse(content);
	});
}
