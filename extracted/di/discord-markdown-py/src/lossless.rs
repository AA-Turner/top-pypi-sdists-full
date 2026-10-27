//! A lossless syntax tree, as [`crate::parse_lossless`] produces.
//!
//! Every byte of the source belongs to exactly one [`Token`], so writing the tokens out in order
//! reproduces it exactly. Nodes carry what the syntax means; tokens carry how it was written, down
//! to delimiters, escapes, markers, line prefixes and line endings. Nothing is normalized: nested
//! and adjacent modifiers stay as written, and escaped text keeps its backslashes.
//!
//! Every [`Node`] spans exactly its children, which are contiguous and in document order.

use std::{borrow::Cow, iter::once};

use url::Url;

use crate::{
	node::{
		Id,
		block::list::Type,
		inline::{code_block::CodeBlock, emoji::Emoji, mention::Mention, timestamp::Timestamp},
		modifier::ModifierKind,
	},
	span::{Span, TrackedSpan},
	unparse::Unparse,
};

/// A node of the lossless tree: what some region of the source means, and the tokens and nodes
/// it is written with.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize))]
pub struct Node<'data> {
	pub kind: NodeKind<'data>,
	/// Byte offsets into the source, unless [`Self::convert_spans`] counted them otherwise.
	pub span: TrackedSpan,
	pub children: Vec<Child<'data>>,
}

impl<'data> Node<'data> {
	/// Every token in this node, in document order.
	pub fn tokens<'node>(&'node self) -> Box<dyn Iterator<Item = &'node Token<'data>> + 'node> {
		Box::new(self.children.iter().flat_map(|child| match child {
			Child::Token(token) => Box::new(once(token)) as Box<dyn Iterator<Item = _>>,
			Child::Node(node) => node.tokens(),
		}))
	}

	/// Counts every span in this tree in `unit` rather than in bytes. `source` is the text the tree
	/// was parsed from.
	///
	/// A host's text APIs rarely count bytes: JavaScript, `NSString` and Java index by UTF-16 code
	/// unit, Python by code point.
	///
	/// # Panics
	/// If a span lies outside `source`.
	pub fn convert_spans(&mut self, source: &str, unit: Unit) {
		let per_char = match unit {
			Unit::Utf8 => return,
			Unit::Utf16 => char::len_utf16,
			Unit::CodePoint => |_| 1,
		};
		// indexed by byte offset; only char boundaries, the only offsets a span holds, are set
		let mut offsets = vec![0; source.len() + 1];
		let mut count = 0;
		for (at, ch) in source.char_indices() {
			offsets[at] = count;
			count += per_char(ch);
		}
		offsets[source.len()] = count;
		self.map_spans(&|offset| offsets[offset]);
	}

	fn map_spans(&mut self, map: &impl Fn(usize) -> usize) {
		self.span = TrackedSpan::new(map(self.span.start), map(self.span.end));
		for child in &mut self.children {
			match child {
				Child::Node(node) => node.map_spans(map),
				Child::Token(token) => {
					token.span = TrackedSpan::new(map(token.span.start), map(token.span.end));
				}
			}
		}
	}
}

/// What a span counts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Unit {
	/// Bytes of UTF-8, as the tree is parsed.
	Utf8,
	/// UTF-16 code units, as JavaScript, `NSString` and Java count.
	Utf16,
	/// Unicode scalar values, as Python counts.
	CodePoint,
}

impl Unparse for Node<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		self.tokens().try_for_each(|token| f.write_str(token.text))
	}
}

/// A child of a [`Node`].
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(tag = "type", rename_all = "snake_case")
)]
pub enum Child<'data> {
	Node(Node<'data>),
	Token(Token<'data>),
}

impl Child<'_> {
	#[must_use]
	pub fn span(&self) -> &TrackedSpan {
		match self {
			Self::Node(node) => &node.span,
			Self::Token(token) => &token.span,
		}
	}
}

/// What a [`Node`] is.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum NodeKind<'data> {
	/// The whole source.
	Document,

	// blocks
	Paragraph,
	Heading {
		level: u8,
	},
	Small,
	Quote(QuoteKind),
	/// The kind of the list as a whole, as written on its first item.
	List(Type),
	ListItem,
	/// A blank line.
	Empty,

	/// A modifier. One that covers several blocks is a fragment inside each, all sharing an `id`
	/// with each other and with their delimiters.
	Modifier {
		kind: ModifierKind,
		id: Id,
	},

	// inline elements
	/// Text, unescaped.
	Text(Cow<'data, str>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Emoji(Emoji<'data>),
	Mention(Mention),
	Timestamp(Timestamp),
	/// A link. Its text, if it has any, is its child nodes.
	Link {
		kind: LinkKind,
		url: Url,
		title: Option<String>,
	},
}

/// How a quote was written.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(rename_all = "snake_case")
)]
pub enum QuoteKind {
	/// `> ` on every line.
	Line,
	/// `>>> `, quoting everything after it.
	Rest,
}

/// How a link was written.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(rename_all = "snake_case")
)]
pub enum LinkKind {
	/// A bare URL.
	Detected,
	/// `<url>`.
	Auto,
	/// `<+phone>` or `<email>`.
	Contact,
	/// `[text](url)`, optionally with a title.
	Masked,
}

/// A piece of the source, verbatim.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize))]
pub struct Token<'data> {
	pub kind: TokenKind,
	pub text: &'data str,
	/// Byte offsets into the source, unless [`Node::convert_spans`] counted them otherwise.
	pub span: TrackedSpan,
}

/// Which end of a modifier a delimiter is.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(rename_all = "snake_case")
)]
pub enum Side {
	Open,
	Close,
}

/// What a [`Token`] is.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum TokenKind {
	/// Text, as written.
	Text,
	/// The backslash of an escape; the escaped character is the [`Self::Text`] after it.
	Escape,
	/// A modifier delimiter, sharing its `id` with the [`NodeKind::Modifier`] it belongs to.
	Delimiter {
		kind: ModifierKind,
		id: Id,
		side: Side,
	},
	/// The backticks around inline code.
	CodeDelimiter,
	/// The content of inline code or a code block.
	CodeContent,
	/// The backticks around a code block.
	CodeFence,
	/// The language of a code block.
	Language,
	/// An emoji, mention or timestamp, as written.
	Atom,
	/// `[` or `<` before link text or a URL.
	LinkOpen,
	/// `]` or `>` after link text or a URL.
	LinkClose,
	/// `(` before a masked link's destination.
	DestinationOpen,
	/// `)` after a masked link's destination.
	DestinationClose,
	Url,
	/// A masked link's title, quotes included.
	Title,
	/// `\n` or `\r\n`.
	LineEnding,
	/// `>` or `>>>`, with the space or tab after it.
	QuotePrefix,
	/// Spaces or tabs at the start of a line.
	Indent,
	/// `-`, `*` or `1.`.
	ListMarker,
	/// `#`, `##` or `###`.
	HeadingMarker,
	/// `-#`.
	SmallMarker,
	/// Spaces or tabs elsewhere, as after a marker.
	Whitespace,
}

#[cfg(test)]
mod test {
	use pretty_assertions::assert_eq;

	use super::{Child, LinkKind, Node, NodeKind, QuoteKind, Side, Token, TokenKind, Unit};
	use crate::{
		Options, error::Error, node::modifier::ModifierKind, parse_lossless, unparse::unparse,
	};

	fn parsed(s: &str) -> Node<'_> {
		parse_lossless::<Error<'_>>(s, Options::default())
			.unwrap_or_else(|err| panic!("unable to parse {s:?}: {err}"))
	}

	/// Children are contiguous, a node spans exactly its children, and a token is its source.
	fn check(node: &Node<'_>, s: &str) {
		let mut at = node.span.start;
		for child in &node.children {
			let span = child.span();
			assert_eq!(span.start, at, "gap or overlap before {child:?} in {s:?}");
			assert!(span.end > span.start, "empty {child:?} in {s:?}");
			at = span.end;
			match child {
				Child::Node(child) => check(child, s),
				Child::Token(token) => {
					assert_eq!(token.text, &s[span.start..span.end]);
					assert!(fits(token), "{token:?} is mislabelled in {s:?}");
				}
			}
		}
		assert_eq!(at, node.span.end, "{node:?} is not covered in {s:?}");
	}

	/// Whether a syntax token's text is what its kind is written with.
	fn fits(token: &Token<'_>) -> bool {
		let text = token.text;
		let blank = |text: &str| text.chars().all(|ch| ch == ' ' || ch == '\t');
		match token.kind {
			TokenKind::LineEnding => text == "\n" || text == "\r\n",
			TokenKind::QuotePrefix => matches!(text, ">" | "> " | ">\t" | ">>> " | ">>>\t"),
			TokenKind::Indent | TokenKind::Whitespace => blank(text),
			TokenKind::ListMarker => {
				matches!(text, "-" | "*")
					|| text.strip_suffix('.').is_some_and(|digits| {
						!digits.is_empty() && digits.chars().all(|ch| ch.is_ascii_digit())
					})
			}
			TokenKind::HeadingMarker => matches!(text, "#" | "##" | "###"),
			TokenKind::SmallMarker => text == "-#",
			TokenKind::Escape => text == "\\",
			TokenKind::Delimiter { kind, .. } => {
				let chars: &[char] = match kind {
					ModifierKind::Bold => &['*'],
					ModifierKind::Italic => &['*', '_'],
					ModifierKind::Underline => &['_'],
					ModifierKind::Strikethrough => &['~'],
					ModifierKind::Spoiler => &['|'],
				};
				text.len() == kind.delimiter_len() && text.chars().all(|ch| chars.contains(&ch))
			}
			_ => true,
		}
	}

	/// `s` writes back exactly, and its tree holds the invariants.
	fn round_trips(s: &str) {
		let node = parsed(s);
		assert_eq!(unparse(&node), s);
		assert_eq!((node.span.start, node.span.end), (0, s.len()));
		check(&node, s);
	}

	/// Each child of `node`, as `(kind, text)` for a token and its kind for a node.
	fn layout<'data>(node: &Node<'data>) -> Vec<Result<(TokenKind, &'data str), NodeKind<'data>>> {
		node.children
			.iter()
			.map(|child| match child {
				Child::Token(token) => Ok((token.kind, token.text)),
				Child::Node(node) => Err(node.kind.clone()),
			})
			.collect()
	}

	fn child<'node, 'data>(node: &'node Node<'data>, index: usize) -> &'node Node<'data> {
		match &node.children[index] {
			Child::Node(node) => node,
			Child::Token(token) => panic!("expected a node, got {token:?}"),
		}
	}

	const CORPUS: &[&str] = &[
		"",
		"plain text",
		"**bold**",
		"__underline__",
		"~~strikethrough~~",
		"||spoiler||",
		"_italic_ *italic*",
		"`code` ``co`de``",
		"**bold _italic_ and `code`**",
		"_foo __bar__ baz_",
		"**baz****baab**",
		"_*a*_ *_a_*",
		"*a **b _c_ d** e*",
		"**a*",
		"***a***",
		"*a* _b_ *a*_b_",
		"1 * 2 * 3",
		"snake_case_name",
		r"\*x\* \¯\_(ツ)_/¯ \__a\__ \\ \d \",
		"<@873227248453443624> <@!01> <#1> <@&1> <@$1> @everyone @here",
		"</settings:873227248453443624> <id:linked-roles:1> <id:home>",
		"<t:1234567890> <t:+0012:R>",
		"<:pepe:873227248453443624> <a:pepe:007> 🦶 :foot: :foot::skin-tone-2:",
		"https://example.com discord.gg/abc <https://discord.com> dev://branch/main",
		"[text](https://example.com/) [t](<https://a.b> \"x\") [t](https://a.b  \"x\")",
		"[**b** [nested] \\*](https://a.b) [_a_](https://example.com/_x_)",
		"<a@b.c> <+1 555 555 5555>",
		"# heading one\n## heading two\n### heading three",
		"# h\n\n  \n> \nafter",
		"#\theading\r\nnext",
		"-# small\n-#\tsmall",
		"> quoted line\n>\n> > not nested\n>",
		">>> - foo\n  - bar\n- baz",
		"> - foo\n>   - bar\n> - baz",
		"- a\n  - b\n* c",
		"1. a\n2. b\n   continued\n10. c",
		"*1. foo\n2. bar*",
		"||\n- a\n- b\n||",
		"foo ||\n- a\n- b||",
		"- content ||\n# test||",
		"||\n# test\nstuff goes here\n```js\nconst a = '2'\n```\n||",
		"```js\nconst a = 1;\n```",
		"```\nplain\n```",
		"```x```",
		"```js\nno trailing newline```",
		"a\r\nb\r\n\r\n",
		"\n\n\n",
		"   leading and trailing   ",
		"**a\n__a\n~~a\n||a\na||\na~~\na__\na**",
		"__# a",
		"<",
		"](](",
		"[[[[](](",
	];

	#[test]
	fn the_corpus_round_trips() {
		for s in CORPUS {
			round_trips(s);
		}
	}

	#[test]
	fn the_fixtures_round_trip() {
		for entry in std::fs::read_dir("test_content").expect("unable to read test_content") {
			let path = entry.expect("unable to read entry").path();
			let markdown =
				std::fs::read_to_string(path.join("content.md")).expect("unable to read content");
			round_trips(&markdown);
		}
	}

	/// The adversarial inputs of the timeout tests, which reach the depth limits and the rounds.
	#[test]
	fn adversarial_inputs_round_trip() {
		let mut nested = String::new();
		for i in 0..500 {
			nested.push_str(if i % 2 == 0 { "*" } else { "**" });
			nested.push('x');
		}
		for i in (0..500).rev() {
			nested.push_str(if i % 2 == 0 { "*" } else { "**" });
		}

		let mut inputs = vec![
			nested,
			"*".to_owned() + &"**".repeat(300),
			"*x".repeat(200) + &"*".repeat(400),
			"*a **b** ".repeat(100),
			"*a\n_a\n".repeat(100) + "a_\na*",
			"*- a\n".repeat(100) + "*",
			"> *a\n".repeat(100) + "> a*",
			"*_".repeat(200) + "x" + &"_*".repeat(200),
			"[".repeat(200) + &"](".repeat(200),
			"x\\y".repeat(100),
		];
		for c in [
			"*", "_", "|", "~", "`", ">", "#", "-", "<", "[", "\\", " ", "\n",
		] {
			inputs.push(c.repeat(500));
		}
		for s in inputs {
			round_trips(&s);
		}
	}

	#[test]
	fn a_leftover_delimiter_is_text_beside_the_modifier() {
		let node = parsed("**a*");
		let paragraph = child(&node, 0);
		assert_eq!(paragraph.kind, NodeKind::Paragraph);
		assert_eq!(layout(paragraph)[0], Err(NodeKind::Text("*".into())),);
		let italic = child(paragraph, 1);
		let NodeKind::Modifier {
			kind: ModifierKind::Italic,
			id,
		} = italic.kind
		else {
			panic!("expected an italic, got {:?}", italic.kind)
		};
		let delimiter = |side| TokenKind::Delimiter {
			kind: ModifierKind::Italic,
			id,
			side,
		};
		assert_eq!(
			layout(italic),
			[
				Ok((delimiter(Side::Open), "*")),
				Err(NodeKind::Text("a".into())),
				Ok((delimiter(Side::Close), "*")),
			]
		);
		assert_eq!((italic.span.start, italic.span.end), (1, 4));
	}

	/// Nothing is flattened: nested italics stay nested, and each keeps the character it was
	/// written with.
	#[test]
	fn modifiers_stay_as_written() {
		let node = parsed("_*a*_");
		let outer = child(child(&node, 0), 0);
		let inner = child(outer, 1);
		assert!(matches!(
			outer.kind,
			NodeKind::Modifier {
				kind: ModifierKind::Italic,
				..
			}
		));
		assert!(matches!(
			inner.kind,
			NodeKind::Modifier {
				kind: ModifierKind::Italic,
				..
			}
		));
		assert_eq!(unparse(inner), "*a*");
	}

	#[test]
	fn escapes_keep_their_backslash() {
		let node = parsed(r"\*a\*");
		let text = child(child(&node, 0), 0);
		assert_eq!(text.kind, NodeKind::Text("*a*".into()));
		assert_eq!(
			layout(text),
			[
				Ok((TokenKind::Escape, "\\")),
				Ok((TokenKind::Text, "*a")),
				Ok((TokenKind::Escape, "\\")),
				Ok((TokenKind::Text, "*")),
			]
		);
	}

	#[test]
	fn quote_and_list_syntax_are_tokens() {
		let node = parsed("> - a\n>   - b");
		let quote = child(&node, 0);
		assert_eq!(quote.kind, NodeKind::Quote(QuoteKind::Line));
		assert_eq!(layout(quote)[0], Ok((TokenKind::QuotePrefix, "> ")));

		let list = child(quote, 1);
		let item = child(list, 0);
		assert_eq!(item.kind, NodeKind::ListItem);
		assert_eq!(
			layout(item)[..3],
			[
				Ok((TokenKind::ListMarker, "-")),
				Ok((TokenKind::Whitespace, " ")),
				Err(NodeKind::Paragraph),
			]
		);
		// a nested item's indentation is its own
		assert_eq!(layout(item)[3], Ok((TokenKind::QuotePrefix, "> ")));
		let nested = child(child(item, 4), 0);
		assert_eq!(
			layout(nested)[..2],
			[
				Ok((TokenKind::Indent, "  ")),
				Ok((TokenKind::ListMarker, "-")),
			]
		);
	}

	/// A spoiler around blocks is a fragment in each, sharing an id with the delimiters, which stay
	/// among the blocks.
	#[test]
	fn fragments_share_an_id() {
		let node = parsed("||\n- a\n- b\n||");
		let Child::Token(open) = &node.children[0] else {
			panic!("expected a delimiter, got {:?}", node.children[0])
		};
		let TokenKind::Delimiter {
			kind: ModifierKind::Spoiler,
			id,
			side: Side::Open,
		} = open.kind
		else {
			panic!("expected an opening spoiler, got {open:?}")
		};
		assert_eq!(layout(&node)[1], Ok((TokenKind::LineEnding, "\n")));

		let list = child(&node, 2);
		for index in 0..2 {
			let paragraph = child(child(list, index), 2);
			let spoiler = child(paragraph, 0);
			assert_eq!(
				spoiler.kind,
				NodeKind::Modifier {
					kind: ModifierKind::Spoiler,
					id
				}
			);
		}
	}

	#[test]
	fn links_keep_their_syntax() {
		let node = parsed("[t](<https://a.b> \"x\") <https://a.b>");
		let paragraph = child(&node, 0);
		let masked = child(paragraph, 0);
		assert!(matches!(
			masked.kind,
			NodeKind::Link {
				kind: LinkKind::Masked,
				..
			}
		));
		assert_eq!(
			layout(masked),
			[
				Ok((TokenKind::LinkOpen, "[")),
				Err(NodeKind::Text("t".into())),
				Ok((TokenKind::LinkClose, "]")),
				Ok((TokenKind::DestinationOpen, "(")),
				Ok((TokenKind::LinkOpen, "<")),
				Ok((TokenKind::Url, "https://a.b")),
				Ok((TokenKind::LinkClose, ">")),
				Ok((TokenKind::Whitespace, " ")),
				Ok((TokenKind::Title, "\"x\"")),
				Ok((TokenKind::DestinationClose, ")")),
			]
		);
		assert!(matches!(
			child(paragraph, 2).kind,
			NodeKind::Link {
				kind: LinkKind::Auto,
				..
			}
		));
	}

	/// Converted, every span still finds its token's text, counting the way the host does.
	#[test]
	fn spans_convert_to_host_units() {
		let s = "🦶 **é** <@1>\n> 𝕏 `a`";
		let utf16: Vec<u16> = s.encode_utf16().collect();
		let chars: Vec<char> = s.chars().collect();

		let mut node = parsed(s);
		node.convert_spans(s, Unit::Utf16);
		assert_eq!((node.span.start, node.span.end), (0, utf16.len()));
		for token in node.tokens() {
			let text = String::from_utf16(&utf16[token.span.start..token.span.end]).unwrap();
			assert_eq!(text, token.text);
		}

		let mut node = parsed(s);
		node.convert_spans(s, Unit::CodePoint);
		assert_eq!((node.span.start, node.span.end), (0, chars.len()));
		for token in node.tokens() {
			let text: String = chars[token.span.start..token.span.end].iter().collect();
			assert_eq!(text, token.text);
		}

		let mut node = parsed(s);
		node.convert_spans(s, Unit::Utf8);
		assert_eq!(node, parsed(s));
	}

	/// The shape the bindings hand out.
	#[test]
	fn serializes_children_and_kinds_by_tag() {
		let node = parsed("**a**");
		let json = serde_json::to_value(&node).unwrap();
		let paragraph = &json["children"][0];
		let bold = &paragraph["children"][0];
		assert_eq!(json["kind"], serde_json::json!({"type": "document"}));
		assert_eq!(paragraph["type"], "node");
		assert_eq!(
			bold["kind"],
			serde_json::json!({"type": "modifier", "value": {"kind": "bold", "id": 0}})
		);
		assert_eq!(
			bold["children"][0],
			serde_json::json!({
				"type": "token",
				"kind": {
					"type": "delimiter",
					"value": {"kind": "bold", "id": 0, "side": "open"}
				},
				"text": "**",
				"span": {"start": 0, "end": 2}
			})
		);
		assert_eq!(
			bold["children"][1]["kind"],
			serde_json::json!({"type": "text", "value": "a"})
		);
	}
}
