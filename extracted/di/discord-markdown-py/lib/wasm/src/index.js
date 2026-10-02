export function* iter(nodes) {
	for (const node of nodes) {
		yield node;

		switch (node.type) {
			case "paragraph":
			case "spoiler":
			case "strikethrough":
			case "underline":
			case "italic":
			case "bold":
			case "quote":
				yield* iter(node.value);
				break;
			case "heading":
			case "small":
				yield* iter(node.value.content);
				break;
			case "list":
				for (const item of node.value.items) {
					yield* iter(item.content);
				}

				break;
			case "link":
				if (node.text) yield* iter(node.text);
		}
	}
}
