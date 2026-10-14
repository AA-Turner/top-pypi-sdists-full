use std::mem::take;

use derive_where::derive_where;

use crate::{
	range::delim::Delim,
	span::{Span, Spanned},
};

use super::{Element, Sequence};

/// A node of the tree mid-parse. Modifiers are still the [`Delim`] runs that
/// [`crate::range::resolve`] pairs into the [`super::Node`]s of the finished tree.
#[derive_where(Debug, Clone, PartialEq, Eq)]
pub enum ParsedNode<'data, S: Span> {
	Delim(Delim),
	Element(Element<'data, S, ParsedNode<'data, S>>),
}

/// A [`ParsedNode`] wrapped in a span.
pub type SpannedParsedNode<'data, S> = Spanned<ParsedNode<'data, S>, S>;
/// A vec of [`ParsedNode`]s, all of which are wrapped in a span.
pub type ParsedNodes<'data, S> = Sequence<S, ParsedNode<'data, S>>;

impl<S: Span> ParsedNode<'_, S> {
	/// Text content of this node and its children, as [`super::Node::content`] reads it once
	/// resolved, less the delimiters.
	#[must_use]
	pub fn content(&self) -> String {
		let mut content = String::new();
		self.push_content(&mut content);
		content
	}

	fn push_content(&self, out: &mut String) {
		let Self::Element(element) = self else {
			return;
		};

		if let Some(text) = element.text() {
			out.push_str(&text);
		}
		for content in element.sequences() {
			for node in &content.value {
				node.value.push_content(out);
			}
		}
	}
}

/// Merges adjacent text in a parsed sequence, which holds no markup to flatten yet.
pub fn merge_text<S: Span>(nodes: &mut Vec<SpannedParsedNode<'_, S>>) {
	let mut merged: Vec<SpannedParsedNode<'_, S>> = Vec::with_capacity(nodes.len());
	for node in take(nodes) {
		if let (
			Some(Spanned {
				value: ParsedNode::Element(Element::Text(current)),
				span,
			}),
			ParsedNode::Element(Element::Text(text)),
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
