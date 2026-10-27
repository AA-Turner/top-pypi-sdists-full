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

// Only ever inline content: a modifier covering several blocks splits into a fragment inside each,
// e.g. `*1. foo\n2. bar*` is a list of two italics.
type ModifierContent = (Inline | Text)[];

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

export type Block = Empty | Heading | List | Quote | Small;

export type NodeType = Inline["type"] | Block["type"];

// The lossless tree, as `parseLossless` returns it: nodes for what the markdown means, and tokens
// holding every character of the source in order, so joining their text gives it back exactly.

/** A region of the source, from `start` up to `end`, in UTF-16 code units: string indices. */
export type Span = { start: number; end: number };

export type ModifierKind =
	| "bold"
	| "italic"
	| "underline"
	| "strikethrough"
	| "spoiler";

/** How a link was written: bare, `<url>`, `<email>` or `<+phone>`, or `[text](url)`. */
export type LinkKind = "detected" | "auto" | "contact" | "masked";

export type LosslessNodeKind =
	| EmptyNode<"document">
	| EmptyNode<"paragraph">
	| Node<"heading", { level: number }>
	| EmptyNode<"small">
	// `> ` on every line, or `>>> ` quoting the rest
	| Node<"quote", "line" | "rest">
	// the list's kind as written on its first item
	| Node<"list", Node<"ordered", number> | EmptyNode<"unordered">>
	| EmptyNode<"list_item">
	| EmptyNode<"empty">
	// A modifier covering several blocks is a fragment inside each, sharing an `id` with the
	// others and with its delimiter tokens.
	| Node<"modifier", { kind: ModifierKind; id: number }>
	// unescaped
	| Text
	| Code
	| CodeBlock
	| Emoji
	| Mention
	| Timestamp
	// a link's text, if it has any, is its child nodes
	| Node<"link", { kind: LinkKind; url: string; title: string | null }>;

export type TokenKind =
	| EmptyNode<"text">
	// the backslash of an escape; the escaped character is the text after it
	| EmptyNode<"escape">
	| Node<
			"delimiter",
			{ kind: ModifierKind; id: number; side: "open" | "close" }
	  >
	| EmptyNode<"code_delimiter">
	| EmptyNode<"code_content">
	| EmptyNode<"code_fence">
	| EmptyNode<"language">
	// an emoji, mention or timestamp, as written
	| EmptyNode<"atom">
	// `[` or `<`, and `]` or `>`
	| EmptyNode<"link_open">
	| EmptyNode<"link_close">
	// `(` and `)` around a masked link's destination
	| EmptyNode<"destination_open">
	| EmptyNode<"destination_close">
	| EmptyNode<"url">
	| EmptyNode<"title">
	| EmptyNode<"line_ending">
	| EmptyNode<"quote_prefix">
	| EmptyNode<"indent">
	| EmptyNode<"list_marker">
	| EmptyNode<"heading_marker">
	| EmptyNode<"small_marker">
	| EmptyNode<"whitespace">;

export type Token = { kind: TokenKind; text: string; span: Span };

export type LosslessNode = {
	kind: LosslessNodeKind;
	span: Span;
	children: LosslessChild[];
};

export type LosslessChild =
	| ({ type: "node" } & LosslessNode)
	| ({ type: "token" } & Token);

export { Syntax, type SyntaxFlags } from "./syntax.js";
