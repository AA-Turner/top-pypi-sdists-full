use std::{borrow::Cow, mem::take};

use derive_where::derive_where;

use crate::{
	range::{Content, delim::Delim},
	span::{Span, Spanned},
};

use super::{
	Sequence,
	block::{Heading, List, Small},
	inline::{
		code_block::CodeBlock, emoji::Emoji, link::Link, mention::Mention, timestamp::Timestamp,
	},
};

/// A node of the tree mid-parse. Modifiers are still the [`Delim`] runs that
/// [`crate::range::resolve`] pairs into the modifiers of the finished tree, turning the rest into
/// [`super::Block`]s and [`super::Inline`]s.
#[derive_where(Debug, Clone, PartialEq, Eq)]
pub enum Element<'data, S: Span> {
	Delim(Delim),

	// inline
	Emoji(Emoji<'data>),
	Timestamp(Timestamp),
	Mention(Mention),
	Link(Link<S, Element<'data, S>>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Text(Cow<'data, str>),

	// block
	Heading(Heading<S, Element<'data, S>>),
	List(List<S, Element<'data, S>>),
	/// Plain Node content.
	Paragraph(Elements<'data, S>),
	Quote(Elements<'data, S>),
	Small(Small<S, Element<'data, S>>),
	/// New line.
	Empty,
}

/// An [`Element`] wrapped in a span.
pub type SpannedElement<'data, S> = Spanned<Element<'data, S>, S>;
/// A vec of [`Element`]s, all of which are wrapped in a span.
pub type Elements<'data, S> = Sequence<S, Element<'data, S>>;

impl<S: Span> Element<'_, S> {
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
			Self::Delim(_)
			| Self::Heading(_)
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

	/// Text content of this element and its children, as [`super::Inline::content`] reads it once
	/// resolved, less the delimiters.
	#[must_use]
	pub fn content(&self) -> String {
		let mut content = String::new();
		self.push_content(&mut content);
		content
	}

	fn push_content(&self, out: &mut String) {
		if let Some(text) = self.text() {
			out.push_str(&text);
		}
		for (_, content) in self.sequences() {
			for node in &content.value {
				node.value.push_content(out);
			}
		}
	}

	/// Whether this is a block container, which holds [`Self::sequences`].
	#[must_use]
	pub fn is_container(&self) -> bool {
		matches!(
			self,
			Self::Paragraph(_) | Self::Quote(_) | Self::Heading(_) | Self::Small(_) | Self::List(_)
		)
	}

	/// Whether this is a block: a container, or a blank line.
	#[must_use]
	pub fn is_block(&self) -> bool {
		self.is_container() || matches!(self, Self::Empty)
	}

	/// The sequences a container holds directly, with what each holds: one per list item,
	/// otherwise its content. Link text is not among them, being a scope of its own.
	pub fn sequences(&self) -> impl Iterator<Item = (Content, &Elements<'_, S>)> {
		let (content, items) = match self {
			Self::Paragraph(content)
			| Self::Heading(Heading { content, .. })
			| Self::Small(Small { content }) => (Some((Content::Inline, content)), &[][..]),
			Self::Quote(content) => (Some((Content::Blocks, content)), &[][..]),
			Self::List(List { items, .. }) => (None, items.value.as_slice()),
			_ => (None, &[][..]),
		};
		content
			.into_iter()
			.chain(items.iter().map(|item| (Content::Blocks, &item.content)))
	}
}

/// Merges adjacent text in a parsed sequence, which holds no markup to flatten yet.
pub fn merge_text<S: Span>(nodes: &mut Vec<SpannedElement<'_, S>>) {
	let mut merged: Vec<SpannedElement<'_, S>> = Vec::with_capacity(nodes.len());
	for node in take(nodes) {
		if let (
			Some(Spanned {
				value: Element::Text(current),
				span,
			}),
			Element::Text(text),
		) = (merged.last_mut(), &node.value)
		{
			current.to_mut().push_str(text);
			span.merge(&node.span);
			continue;
		}
		merged.push(node);
	}
	*nodes = merged;
}
