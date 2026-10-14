use std::borrow::Cow;

use crate::{
	block::{Heading, List, Small},
	inline::{
		code_block::CodeBlock, emoji::Emoji, link::Link, mention::Mention, timestamp::Timestamp,
	},
	span::Span,
};

use super::{Element, Modifier, Node, SpannedNodes, modifier::spoiler::Spoiler};

/// [`Node`] as it deserializes: every variant flat under one tag. Untagged, a [`Node`] would buffer
/// each node to retry it as the other half, and so every subtree once per level above it.
#[derive(serde::Deserialize)]
#[serde(tag = "type", content = "value", rename_all = "snake_case", bound = "")]
pub enum Repr<'data, S: Span> {
	Bold(SpannedNodes<'data, S>),
	Italic(SpannedNodes<'data, S>),
	Underline(SpannedNodes<'data, S>),
	Strikethrough(SpannedNodes<'data, S>),
	Spoiler(Spoiler<'data, S>),

	Emoji(Emoji<'data>),
	Timestamp(Timestamp),
	Mention(Mention),
	Link(Link<S, Node<'data, S>>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Text(Cow<'data, str>),

	Heading(Heading<S, Node<'data, S>>),
	List(List<S, Node<'data, S>>),
	Paragraph(SpannedNodes<'data, S>),
	Quote(SpannedNodes<'data, S>),
	Small(Small<S, Node<'data, S>>),
	Empty,
}

impl<'data, S: Span> From<Repr<'data, S>> for Node<'data, S> {
	fn from(repr: Repr<'data, S>) -> Self {
		match repr {
			Repr::Bold(content) => Self::Modifier(Modifier::Bold(content)),
			Repr::Italic(content) => Self::Modifier(Modifier::Italic(content)),
			Repr::Underline(content) => Self::Modifier(Modifier::Underline(content)),
			Repr::Strikethrough(content) => Self::Modifier(Modifier::Strikethrough(content)),
			Repr::Spoiler(spoiler) => Self::Modifier(Modifier::Spoiler(spoiler)),

			Repr::Emoji(emoji) => Self::Element(Element::Emoji(emoji)),
			Repr::Timestamp(timestamp) => Self::Element(Element::Timestamp(timestamp)),
			Repr::Mention(mention) => Self::Element(Element::Mention(mention)),
			Repr::Link(link) => Self::Element(Element::Link(link)),
			Repr::Code(code) => Self::Element(Element::Code(code)),
			Repr::CodeBlock(code_block) => Self::Element(Element::CodeBlock(code_block)),
			Repr::Text(text) => Self::Element(Element::Text(text)),

			Repr::Heading(heading) => Self::Element(Element::Heading(heading)),
			Repr::List(list) => Self::Element(Element::List(list)),
			Repr::Paragraph(content) => Self::Element(Element::Paragraph(content)),
			Repr::Quote(content) => Self::Element(Element::Quote(content)),
			Repr::Small(small) => Self::Element(Element::Small(small)),
			Repr::Empty => Self::Element(Element::Empty),
		}
	}
}
