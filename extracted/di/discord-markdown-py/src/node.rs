use std::{borrow::Cow, fmt::Debug, iter::empty, mem::take, ops::DerefMut};

use tracing::Level;

pub use iter::Iter;

use crate::{
	block::{quote, small},
	inline::{bold, code, italic, spoiler, strikethrough, underline},
	unparse::Unparse,
};

use super::{
	block::{Heading, List, Small},
	inline::{
		code_block::CodeBlock,
		emoji::Emoji,
		link::{Link, Normal},
		mention::Mention,
		timestamp::Timestamp,
	},
	rule::{Rule, RuleSet},
	span::{Span, Spanned},
};

mod iter;

/// A node containing markdown content.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case",)
)]
pub enum Node<'data, S: Span> {
	// inline
	Bold(SpannedNodes<'data, S>),
	Italic(SpannedNodes<'data, S>),
	Underline(SpannedNodes<'data, S>),
	Strikethrough(SpannedNodes<'data, S>),
	Spoiler(SpannedNodes<'data, S>),
	Emoji(Emoji<'data>),
	Timestamp(Timestamp),
	Mention(Mention),
	Link(Link<'data, S>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Text(Cow<'data, str>),

	// block
	Heading(Heading<'data, S>),
	List(List<'data, S>),
	/// Plain Node content.
	Paragraph(SpannedNodes<'data, S>),
	Quote(SpannedNodes<'data, S>),
	Small(Small<'data, S>),
	/// New line.
	Empty,
}

/// Node wrapped in a span.
pub type SpannedNode<'data, S> = Spanned<Node<'data, S>, S>;
/// A vec of nodes, all of which are wrapped in a span.
pub type SpannedNodes<'data, S> = Spanned<Vec<SpannedNode<'data, S>>, S>;

impl<'data, S> Node<'data, S>
where
	S: Span,
{
	/// Returns an iterator over all child nodes of this node. Yields no items if this node has no
	/// children.
	pub fn children(&self) -> impl Iterator<Item = &Node<'data, S>> {
		match self {
			Node::Bold(children)
			| Node::Italic(children)
			| Node::Underline(children)
			| Node::Strikethrough(children)
			| Node::Spoiler(children)
			| Node::Paragraph(children)
			| Node::Heading(Heading {
				content: children, ..
			})
			| Node::Small(Small { content: children })
			| Node::Quote(children) => Box::new(children.iter().map(|span| &span.value))
				as Box<dyn Iterator<Item = &Node<S>>>,
			Node::List(List { items, .. }) => Box::new(
				items
					.iter()
					.flat_map(|item| item.content.iter().map(|span| &span.value)),
			),
			_ => Box::new(empty()),
		}
	}

	/// Returns an iterator over this node and all child nodes.
	#[must_use]
	pub fn iter<'node: 'data>(&'node self) -> Iter<'data, 'node, S> {
		Iter {
			node: Some(self),
			// TODO: it's a bit awkward to re-box after this technically returns a pre-boxed iterator
			children: Some(Box::new(self.children())),
		}
	}

	fn flatten_children(&mut self) {
		match self {
			Self::Bold(nodes)
			| Self::Italic(nodes)
			| Self::Underline(nodes)
			| Self::Strikethrough(nodes)
			| Self::Spoiler(nodes) => flatten(nodes),
			_ => {}
		}
	}

	fn is_empty(&self) -> bool {
		match self {
			Self::Bold(nodes)
			| Self::Italic(nodes)
			| Self::Underline(nodes)
			| Self::Strikethrough(nodes)
			| Self::Spoiler(nodes) => nodes.is_empty(),
			// TODO: should we flatten code?
			Self::Text(content) => content.is_empty(),
			_ => false,
		}
	}

	/// The [`Rule`] that this node corresponds to. Returns [`None`] if this is a base rule.
	#[must_use]
	pub fn rule(&self) -> Option<Rule> {
		Some(match self {
			Self::Text(_) | Self::Paragraph(_) | Self::Empty => return None,
			Self::Bold(_) => Rule::Bold,
			Self::Code(_) => Rule::Code,
			Self::CodeBlock(_) => Rule::CodeBlock,
			Self::Emoji(_) => Rule::Emoji,
			Self::Italic(_) => Rule::Italic,
			Self::Link(_) => Rule::Link,
			Self::Mention(_) => Rule::Mention,
			Self::Spoiler(_) => Rule::Spoiler,
			Self::Strikethrough(_) => Rule::Strikethrough,
			Self::Timestamp(_) => Rule::Timestamp,
			Self::Underline(_) => Rule::Underline,
			Self::Heading(_) => Rule::Heading,
			Self::List(_) => Rule::List,
			Self::Quote(_) => Rule::Quote,
			Self::Small(_) => Rule::Small,
		})
	}

	/// All [`Rule`]s that this node contains, including itself.
	#[must_use]
	pub fn rules(&self) -> RuleSet {
		self.iter().filter_map(Node::rule).collect()
	}

	/// Text content of this node (does not include children). Returns [`None`] if this node has no
	/// text content.
	#[must_use]
	pub fn text(&self) -> Option<String> {
		Some(match self {
			Self::Code(code) => code.clone().into_owned(),
			Self::CodeBlock(CodeBlock { content, .. }) => content.clone(),
			Self::Emoji(Emoji::Unicode(code_point)) => code_point.clone().into_owned(),
			Self::Link(Link::Normal(Normal {
				text: None, url, ..
			})) => url.to_string(),
			Self::Link(Link::Mention(mention_link)) => mention_link.to_string(),
			Self::Mention(mention) => mention.to_string(),
			Self::Text(text) => text.clone().into_owned(),
			Self::Bold(_)
			| Self::Italic(_)
			| Self::Underline(_)
			| Self::Strikethrough(_)
			| Self::Spoiler(_)
			| Self::Heading(_)
			| Self::Timestamp(_)
			| Self::List(_)
			| Self::Paragraph(_)
			| Self::Quote(_)
			| Self::Small(_)
			| Self::Empty
			| Self::Emoji(Emoji::Custom(_))
			| Self::Link(Link::Normal(Normal { text: Some(_), .. })) => return None,
		})
	}

	/// Text content of this node _and_ its children.
	#[must_use]
	pub fn content(&self) -> String {
		self.iter().filter_map(Node::text).collect()
	}
}

impl<'data, 'node: 'data, S> IntoIterator for &'node Node<'data, S>
where
	S: Span,
{
	type Item = &'node Node<'data, S>;
	type IntoIter = Iter<'data, 'node, S>;

	fn into_iter(self) -> Self::IntoIter {
		self.iter()
	}
}

impl<S> Unparse for Node<'_, S>
where
	S: Span,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			// Inline nodes
			Self::Bold(children) => bold::unparse(children, f),
			Self::Italic(children) => italic::unparse(children, f),
			Self::Underline(children) => underline::unparse(children, f),
			Self::Strikethrough(children) => strikethrough::unparse(children, f),
			Self::Spoiler(children) => spoiler::unparse(children, f),
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

/// Recursively merges adjacent nodes of the same type in order to produce a more optimized AST.
#[tracing::instrument(level = Level::TRACE)]
pub fn flatten<'data, S>(nodes: &mut Vec<impl DerefMut<Target = Node<'data, S>> + Debug>)
where
	S: Span,
{
	{
		let Some((mut current_node, nodes)) = nodes.split_first_mut() else {
			return;
		};
		current_node.flatten_children();

		for node in nodes {
			node.flatten_children();

			match (&mut **current_node, &mut **node) {
				(Node::Italic(current_children), Node::Italic(children))
				| (Node::Bold(current_children), Node::Bold(children))
				| (Node::Underline(current_children), Node::Underline(children))
				| (Node::Strikethrough(current_children), Node::Strikethrough(children)) => {
					current_children.extend(take(children));
					flatten(&mut current_children.value);
				}
				(Node::Text(current_content), Node::Text(content)) => {
					current_content.to_mut().push_str(&take(content));
				}
				_ => {
					current_node = node;
				}
			}
		}
	}

	nodes.retain(|item| !item.is_empty());
}

/// Same as [`flatten`] but with owned data.
#[must_use]
pub fn flatten_owned<'data, N, S>(mut nodes: Vec<N>) -> Vec<N>
where
	N: DerefMut<Target = Node<'data, S>> + Debug,
	S: Span,
{
	flatten(&mut nodes);
	nodes
}
