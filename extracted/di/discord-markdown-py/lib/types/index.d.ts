export type Node<T, V> = {
	type: T;
	value: V;
};

export type EmptyNode<T> = { type: T; value?: never };

// biome-ignore lint/suspicious/noExplicitAny: this is explicitly any
export type AnyNode<T = any, V = any> = Node<T, V> | EmptyNode<T>;

// base
export type Text = Node<"text", string>;
export type Paragraph = Node<"paragraph", Inline[]>;

export type Code = Node<"code", string>;

// Inline content where the modifier opened mid-line, and block content where it opened at the
// start of a line, e.g. `*1. foo\n2. bar*` is an italic list.
type ModifierContent = (Inline | Block | Paragraph | Text)[];

// A spoiler split across blocks, as `||1. foo\n2. ba||r` splits into one in each list item, is one
// spoiler in fragments that share an id, so that revealing one can reveal them all.
export type Spoiler = Node<"spoiler", { id: number; content: ModifierContent }>;
export type Strikethrough = Node<"strikethrough", ModifierContent>;
export type Underline = Node<"underline", ModifierContent>;
export type Italic = Node<"italic", ModifierContent>;
export type Bold = Node<"bold", ModifierContent>;

export type Modifier = Bold | Italic | Spoiler | Strikethrough | Underline;

export type Link = Node<
	"link",
	{
		text?: Exclude<Inline, Link>[];
		url: string;
		title?: string;
	}
>;

export type UserMention = Node<"user", bigint>;
export type ChannelMention = Node<"channel", bigint>;
export type RoleMention = Node<"role", bigint>;
export type GameMention = Node<"game", bigint>;
export type CommandMention = Node<"command", { name: string; id: bigint }>;
export type EveryoneMention = EmptyNode<"everyone">;
export type HereMention = EmptyNode<"here">;
export type StaticMention = Node<
	"static",
	| EmptyNode<"home">
	| EmptyNode<"browse">
	| EmptyNode<"customize">
	| EmptyNode<"guide">
	| Node<"linked_roles", bigint | undefined>
>;
export type Mention = Node<
	"mention",
	| UserMention
	| ChannelMention
	| RoleMention
	| GameMention
	| CommandMention
	| EveryoneMention
	| HereMention
	| StaticMention
>;

export type Timestamp = Node<"timestamp", { value: bigint; style?: string }>;

export type CustomEmoji = Node<
	"custom",
	{ animated: boolean; name: string; id: bigint }
>;
export type UnicodeEmoji = Node<"unicode", string>;
export type Emoji = Node<"emoji", CustomEmoji | UnicodeEmoji>;

export type CodeBlock = Node<
	"code_block",
	{ language?: string; content: string }
>;

export type Inline =
	| Code
	| CodeBlock
	| Emoji
	| Link
	| Mention
	| Modifier
	| Timestamp;

export type Heading = Node<
	"heading",
	{
		level: number;
		content: Inline[];
	}
>;

export type ListItem = { content: (List | Paragraph)[] };
export type List = Node<
	"list",
	{
		type: "unordered" | "ordered";
		value?: number;
		items: ListItem[];
	}
>;
export type Empty = EmptyNode<"empty">;
export type Quote = Node<"quote", Block[]>;
export type Small = Node<"small", { content: Inline[] }>;

export type Block = Empty | Heading | List | Modifier | Quote | Small;

export type NodeType = Inline["type"] | Block["type"];

// Rules with no matching NodeType: they gate a variant of another rule. `dev_link` allows the
// `dev` URL scheme, e.g. `dev://branch/main`.
export type GateRule = "dev_link";

export type Rule = Exclude<NodeType, "paragraph" | "text" | "empty"> | GateRule;
