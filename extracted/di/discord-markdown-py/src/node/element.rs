use std::borrow::Cow;

use derive_where::derive_where;

use crate::{
	block::{Heading, List, Small, list::item::Item, quote, small},
	inline::{
		code, code_block::CodeBlock, emoji::Emoji, link::Link, mention::Mention,
		timestamp::Timestamp,
	},
	range::Content,
	rule::Rule,
	span::{Span, Spanned},
	unparse::Unparse,
};

use super::{Node, Sequence};

/// What the parser builds directly, as opposed to the modifiers resolved over it: the nodes both
/// a [`Node`] and a [`super::ParsedNode`] can be, holding children of type `N`.
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(
		tag = "type",
		content = "value",
		rename_all = "snake_case",
		bound(
			serialize = "N: serde::Serialize",
			deserialize = "N: serde::Deserialize<'de>"
		)
	)
)]
pub enum Element<'data, S: Span, N> {
	// inline
	Emoji(Emoji<'data>),
	Timestamp(Timestamp),
	Mention(Mention),
	Link(Link<S, N>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Text(Cow<'data, str>),

	// block
	Heading(Heading<S, N>),
	List(List<S, N>),
	/// Plain Node content.
	Paragraph(Sequence<S, N>),
	Quote(Sequence<S, N>),
	Small(Small<S, N>),
	/// New line.
	Empty,
}

impl<S: Span, N> Element<'_, S, N> {
	/// The [`Rule`] that this element corresponds to. Returns [`None`] if this is a base rule.
	#[must_use]
	pub fn rule(&self) -> Option<Rule> {
		Some(match self {
			Self::Text(_) | Self::Paragraph(_) | Self::Empty => return None,
			Self::Code(_) => Rule::Code,
			Self::CodeBlock(_) => Rule::CodeBlock,
			Self::Emoji(_) => Rule::Emoji,
			Self::Link(_) => Rule::Link,
			Self::Mention(_) => Rule::Mention,
			Self::Timestamp(_) => Rule::Timestamp,
			Self::Heading(_) => Rule::Heading,
			Self::List(_) => Rule::List,
			Self::Quote(_) => Rule::Quote,
			Self::Small(_) => Rule::Small,
		})
	}

	/// Text content of this element (does not include children). Returns [`None`] if it has no
	/// text content.
	#[must_use]
	pub fn text(&self) -> Option<String> {
		Some(match self {
			Self::Code(code) => code.clone().into_owned(),
			Self::CodeBlock(CodeBlock { content, .. }) => content.clone(),
			Self::Emoji(Emoji::Unicode(code_point)) => code_point.to_string(),
			Self::Link(Link {
				text: None, url, ..
			}) => url.to_string(),
			Self::Mention(mention) => mention.to_string(),
			Self::Text(text) => text.clone().into_owned(),
			Self::Heading(_)
			| Self::Timestamp(_)
			| Self::List(_)
			| Self::Paragraph(_)
			| Self::Quote(_)
			| Self::Small(_)
			| Self::Empty
			| Self::Emoji(Emoji::Custom(_))
			| Self::Link(Link { text: Some(_), .. }) => return None,
		})
	}

	/// Whether this is a block container, which holds [`Self::sequences`].
	#[must_use]
	pub fn is_container(&self) -> bool {
		matches!(
			self,
			Self::Paragraph(_) | Self::Quote(_) | Self::Heading(_) | Self::Small(_) | Self::List(_)
		)
	}

	/// The sequences a container holds directly: one per list item, otherwise its content. Link
	/// text is not among them, being a scope of its own.
	pub fn sequences(&self) -> impl Iterator<Item = &Sequence<S, N>> {
		let (content, items) = match self {
			Self::Paragraph(content)
			| Self::Quote(content)
			| Self::Heading(Heading { content, .. })
			| Self::Small(Small { content }) => (Some(content), &[][..]),
			Self::List(List { items, .. }) => (None, items.value.as_slice()),
			_ => (None, &[][..]),
		};
		content
			.into_iter()
			.chain(items.iter().map(|item| &item.content))
	}

	/// As [`Self::sequences`], mutably.
	pub fn sequences_mut(&mut self) -> impl Iterator<Item = &mut Sequence<S, N>> {
		let (content, items) = match self {
			Self::Paragraph(content)
			| Self::Quote(content)
			| Self::Heading(Heading { content, .. })
			| Self::Small(Small { content }) => (Some(content), &mut [][..]),
			Self::List(List { items, .. }) => (None, items.value.as_mut_slice()),
			_ => (None, &mut [][..]),
		};
		content
			.into_iter()
			.chain(items.iter_mut().map(|item| &mut item.content))
	}
}

impl<'data, S: Span, N> Element<'data, S, N> {
	/// This element with children of type `M`: every sequence it holds, link text included, mapped
	/// through `f` along with what it holds.
	pub fn map_children<M>(
		self,
		mut f: impl FnMut(Sequence<S, N>, Content) -> Sequence<S, M>,
	) -> Element<'data, S, M> {
		match self {
			Self::Paragraph(content) => Element::Paragraph(f(content, Content::Inline)),
			Self::Heading(Heading { level, content }) => Element::Heading(Heading {
				level,
				content: f(content, Content::Inline),
			}),
			Self::Small(Small { content }) => Element::Small(Small {
				content: f(content, Content::Inline),
			}),
			Self::Quote(content) => Element::Quote(f(content, Content::Blocks)),
			Self::List(List { kind, items }) => Element::List(List {
				kind,
				items: Spanned {
					value: items
						.value
						.into_iter()
						.map(|item| Item {
							content: f(item.content, Content::Blocks),
						})
						.collect(),
					span: items.span,
				},
			}),
			Self::Link(Link { text, url, title }) => Element::Link(Link {
				text: text.map(|text| f(text, Content::Inline)),
				url,
				title,
			}),
			Self::Emoji(emoji) => Element::Emoji(emoji),
			Self::Timestamp(timestamp) => Element::Timestamp(timestamp),
			Self::Mention(mention) => Element::Mention(mention),
			Self::Code(code) => Element::Code(code),
			Self::CodeBlock(code_block) => Element::CodeBlock(code_block),
			Self::Text(text) => Element::Text(text),
			Self::Empty => Element::Empty,
		}
	}
}

impl<'data, S: Span> Unparse for Element<'data, S, Node<'data, S>> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			// Inline nodes
			Self::Emoji(emoji) => Unparse::fmt(emoji, f),
			Self::Timestamp(timestamp) => Unparse::fmt(timestamp, f),
			Self::Mention(mention) => Unparse::fmt(mention, f),
			Self::Link(link) => Unparse::fmt(link, f),
			Self::Code(code) => code::unparse(code, f),
			Self::CodeBlock(code_block) => Unparse::fmt(code_block, f),
			Self::Text(text) => f.write_str(text),

			// Block nodes
			Self::Heading(heading) => Unparse::fmt(heading, f),
			Self::List(list) => Unparse::fmt(list, f),
			Self::Paragraph(children) => Unparse::fmt(children, f),
			Self::Quote(children) => quote::unparse(children, f),
			Self::Small(small) => small::unparse(&small.content, f),
			Self::Empty => f.write_str("\n"),
		}
	}
}
