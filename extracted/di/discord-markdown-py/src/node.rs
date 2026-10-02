use std::{borrow::Cow, iter::empty, mem::take};

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
		code_block::CodeBlock, emoji::Emoji, link::Link, mention::Mention, timestamp::Timestamp,
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

	/// Returns an iterator over this node and all child nodes, at every depth.
	///
	/// Depth matters to [`Self::content`] and [`Self::rules`]: a markup wrapper's own [`Self::text`]
	/// is [`None`], so stopping at the direct children made `**_text_**` look textless.
	#[must_use]
	pub fn iter<'node: 'data>(&'node self) -> Iter<'data, 'node, S> {
		Iter {
			node: Some(self),
			// TODO: it's a bit awkward to re-box after this technically returns a pre-boxed iterator
			children: Some(Box::new(self.children().flat_map(Node::iter))),
		}
	}

	/// Recursively flattens this node's children, collapsing any markup made redundant by
	/// `active` -- the markup its ancestors already apply.
	///
	/// Markup is the only thing `active` crosses. A block container or a link owns its own inline
	/// content, which its own [`flatten`] has already flattened, so an italic inside a heading
	/// inside an italic keeps both.
	fn flatten_children(&mut self, mut active: RuleSet) {
		let rule = self.rule();

		let (Self::Bold(nodes)
		| Self::Italic(nodes)
		| Self::Underline(nodes)
		| Self::Strikethrough(nodes)
		| Self::Spoiler(nodes)) = self
		else {
			return;
		};

		// only markup descends, so only markup joins the set
		active.extend(rule);

		let mut nested = false;
		for node in &mut nodes.value {
			node.flatten_children(active);
			nested |= node.is_nested_in(active);
		}

		// a collapsed child's own children were flattened against this same set, so one round is
		// enough -- nothing spliced in can be redundant again
		if nested {
			collapse_nested(&mut nodes.value, active);
		}

		merge_siblings(&mut nodes.value);
	}

	/// Whether an ancestor already applies this node's markup.
	fn is_nested_in(&self, active: RuleSet) -> bool {
		self.rule().is_some_and(|rule| active.contains(rule))
	}

	/// Takes the children of redundant markup, leaving it empty. [`None`] if it is not redundant.
	fn take_nested_children(&mut self, active: RuleSet) -> Option<Vec<SpannedNode<'data, S>>> {
		if !self.is_nested_in(active) {
			return None;
		}

		match self {
			Self::Bold(nodes)
			| Self::Italic(nodes)
			| Self::Underline(nodes)
			| Self::Strikethrough(nodes)
			| Self::Spoiler(nodes) => Some(take(&mut nodes.value)),
			_ => None,
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
			Self::Emoji(Emoji::Unicode(code_point)) => code_point.to_string(),
			Self::Link(Link {
				text: None, url, ..
			}) => url.to_string(),
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
			| Self::Link(Link { text: Some(_), .. }) => return None,
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

/// Recursively merges adjacent nodes of the same type, and collapses markup nested inside the same
/// markup, in order to produce a more optimized AST.
#[tracing::instrument(level = Level::TRACE)]
pub fn flatten<S>(nodes: &mut Vec<SpannedNode<'_, S>>)
where
	S: Span,
{
	for node in nodes.iter_mut() {
		node.value.flatten_children(RuleSet::empty());
	}

	merge_siblings(nodes);
}

/// Same as [`flatten`] but with owned data.
#[must_use]
pub fn flatten_owned<S>(mut nodes: Vec<SpannedNode<'_, S>>) -> Vec<SpannedNode<'_, S>>
where
	S: Span,
{
	flatten(&mut nodes);
	nodes
}

/// Splices the children of every redundant node into `nodes`. Rebuilt in one pass rather than
/// spliced per node, so a run of them does not reshuffle the tail repeatedly.
///
/// Spans need no adjustment: a promoted child keeps its own, and `nodes` is still parsed from the
/// same region of source it was before.
fn collapse_nested<S>(nodes: &mut Vec<SpannedNode<'_, S>>, active: RuleSet)
where
	S: Span,
{
	let mut collapsed = Vec::with_capacity(nodes.len());

	for mut node in take(nodes) {
		match node.value.take_nested_children(active) {
			Some(children) => collapsed.extend(children),
			None => collapsed.push(node),
		}
	}

	*nodes = collapsed;
}

/// Merges adjacent nodes of the same type and drops the empty ones.
///
/// Every child is already flattened, so this does not descend into them -- only into a merged node,
/// whose two halves have to merge across the seam.
fn merge_siblings<S>(nodes: &mut Vec<SpannedNode<'_, S>>)
where
	S: Span,
{
	{
		let Some((mut current_node, nodes)) = nodes.split_first_mut() else {
			return;
		};

		for node in nodes {
			match (&mut current_node.value, &mut node.value) {
				(Node::Italic(current_children), Node::Italic(children))
				| (Node::Bold(current_children), Node::Bold(children))
				| (Node::Underline(current_children), Node::Underline(children))
				| (Node::Strikethrough(current_children), Node::Strikethrough(children)) => {
					current_children.span.merge(&children.span);
					current_children.extend(take(&mut children.value));
					merge_siblings(&mut current_children.value);
				}
				(Node::Text(current_content), Node::Text(content)) => {
					current_content.to_mut().push_str(&take(content));
				}
				_ => {
					current_node = node;
					continue;
				}
			}

			current_node.span.merge(&node.span);
		}
	}

	nodes.retain(|item| !item.value.is_empty());
}

#[cfg(test)]
mod test {
	use super::{flatten, Node, SpannedNode, SpannedNodes};
	use crate::span::{Span, Spanned, TrackedSpan};
	use crate::{bold, italic, link, spanned_vec, spoiler, text, underline};

	/// Wraps untracked nodes, which need no spans, so they can be flattened.
	fn unspanned(nodes: Vec<Node<'static, ()>>) -> Vec<SpannedNode<'static, ()>> {
		nodes
			.into_iter()
			.map(|value| Spanned { value, span: () })
			.collect()
	}

	/// Flattens a node on its own, expecting a single node back.
	fn flattened(node: Node<'static, ()>) -> Node<'static, ()> {
		let mut nodes = unspanned(vec![node]);
		flatten(&mut nodes);
		assert_eq!(nodes.len(), 1, "expected a single node, got {nodes:?}");
		nodes.remove(0).value
	}

	fn spanned(
		value: Node<'static, TrackedSpan>,
		start: usize,
		end: usize,
	) -> SpannedNode<'static, TrackedSpan> {
		Spanned {
			value,
			span: TrackedSpan::new(start, end),
		}
	}

	fn text_of<'node>(node: &'node SpannedNode<'static, TrackedSpan>) -> &'node str {
		match &node.value {
			Node::Text(content) => content,
			other => panic!("expected text, got {other:?}"),
		}
	}

	fn children_of<'node>(
		node: &'node SpannedNode<'static, TrackedSpan>,
	) -> &'node SpannedNodes<'static, TrackedSpan> {
		match &node.value {
			Node::Bold(children) | Node::Italic(children) => children,
			other => panic!("expected markup, got {other:?}"),
		}
	}

	/// The inner wrapper carries no meaning, since the outer one already applies.
	#[test]
	fn nested_markup_collapses() {
		assert_eq!(flattened(italic!(italic!("a"))), italic!("a"));
		assert_eq!(flattened(bold!(bold!("a"))), bold!("a"));
		assert_eq!(flattened(underline!(underline!("a"))), underline!("a"));
		assert_eq!(
			flattened(Node::Strikethrough(spanned_vec![Node::Strikethrough(
				spanned_vec![text!("a")]
			)])),
			Node::Strikethrough(spanned_vec![text!("a")])
		);
		assert_eq!(flattened(spoiler!(spoiler!("a"))), spoiler!("a"));
	}

	/// The collapse reaches through markup of a different type, which loses the inner markup
	/// relative to what was written.
	#[test]
	fn nested_markup_collapses_through_other_markup() {
		assert_eq!(flattened(italic!(bold!(italic!("a")))), italic!(bold!("a")));
	}

	#[test]
	fn a_chain_of_nested_markup_collapses_completely() {
		assert_eq!(
			flattened(italic!(italic!(italic!(italic!("a"))))),
			italic!("a")
		);
	}

	#[test]
	fn collapsing_merges_the_text_it_exposes() {
		assert_eq!(
			flattened(italic!(text!("a "), italic!("b"), text!(" c"))),
			italic!("a b c")
		);
	}

	#[test]
	fn collapsing_merges_the_markup_it_exposes() {
		assert_eq!(
			flattened(italic!(bold!("a"), italic!(bold!("b")))),
			italic!(bold!("ab"))
		);
	}

	/// A link owns its own inline content, which its own [`flatten`] already flattened, so the
	/// markup around it is not in scope for the markup inside it.
	#[test]
	fn markup_does_not_collapse_through_a_link() {
		let node = italic!(link!("https://example.com/", [italic!("a")]));
		assert_eq!(flattened(node.clone()), node);
	}

	#[test]
	fn adjacent_markup_merges() {
		let mut nodes = unspanned(vec![italic!("a"), italic!("b")]);
		flatten(&mut nodes);
		assert_eq!(nodes, unspanned(vec![italic!("ab")]));

		// spoiler stays out of the merge on purpose: two of them are two independently revealable
		// regions, so merging them would change what the reader gets, not just the AST
		let mut nodes = unspanned(vec![spoiler!("a"), spoiler!("b")]);
		flatten(&mut nodes);
		assert_eq!(nodes, unspanned(vec![spoiler!("a"), spoiler!("b")]));
	}

	/// A merged span covers both halves. It therefore also covers the delimiters between them,
	/// which a start/end pair cannot exclude.
	#[test]
	fn merging_text_widens_the_span() {
		let mut nodes = vec![spanned(text!("abc"), 0, 3), spanned(text!("def"), 3, 6)];
		flatten(&mut nodes);

		assert_eq!(nodes.len(), 1);
		assert_eq!(text_of(&nodes[0]), "abcdef");
		assert_eq!((nodes[0].span.start, nodes[0].span.end), (0, 6));
	}

	/// Both the node and its children collection grew, so both spans widen.
	#[test]
	fn merging_markup_widens_the_node_and_its_children() {
		let mut nodes = vec![
			spanned(
				Node::Bold(Spanned {
					value: vec![spanned(text!("a"), 2, 3)],
					span: TrackedSpan::new(2, 3),
				}),
				0,
				5,
			),
			spanned(
				Node::Bold(Spanned {
					value: vec![spanned(text!("b"), 7, 8)],
					span: TrackedSpan::new(7, 8),
				}),
				5,
				10,
			),
		];
		flatten(&mut nodes);

		assert_eq!(nodes.len(), 1);
		assert_eq!((nodes[0].span.start, nodes[0].span.end), (0, 10));

		let children = children_of(&nodes[0]);
		assert_eq!((children.span.start, children.span.end), (2, 8));
		assert_eq!(children.value.len(), 1);
		assert_eq!(text_of(&children.value[0]), "ab");
		assert_eq!(
			(children.value[0].span.start, children.value[0].span.end),
			(2, 8)
		);
	}

	/// Collapsing needs no span arithmetic: the promoted child keeps its own span, and the
	/// children collection still covers the region it was parsed from.
	#[test]
	fn collapsing_keeps_the_promoted_child_span() {
		let mut nodes = vec![spanned(
			Node::Italic(Spanned {
				value: vec![spanned(
					Node::Italic(Spanned {
						value: vec![spanned(text!("a"), 3, 4)],
						span: TrackedSpan::new(3, 4),
					}),
					2,
					5,
				)],
				span: TrackedSpan::new(1, 6),
			}),
			0,
			7,
		)];
		flatten(&mut nodes);

		assert_eq!(nodes.len(), 1);
		let children = children_of(&nodes[0]);
		assert_eq!((children.span.start, children.span.end), (1, 6));
		assert_eq!(children.value.len(), 1);
		assert_eq!(text_of(&children.value[0]), "a");
		assert_eq!(
			(children.value[0].span.start, children.value[0].span.end),
			(3, 4)
		);
	}
}
