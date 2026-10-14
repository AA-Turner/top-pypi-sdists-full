use std::mem::take;

use derive_where::derive_where;
use tracing::Level;

pub use element::Element;
pub use id::{Id, Ids};
pub use iter::Iter;
pub use modifier::Modifier;
pub use parsed::{ParsedNode, ParsedNodes, SpannedParsedNode, merge_text};

use crate::unparse::Unparse;

use super::{
	rule::{Rule, RuleSet},
	span::{Span, Spanned},
};

mod element;
mod id;
mod iter;
pub mod modifier;
mod parsed;
#[cfg(feature = "serde")]
mod repr;

/// A vec of `N`, each wrapped in a span, and wrapped in a span itself.
pub type Sequence<S, N> = Spanned<Vec<Spanned<N, S>>, S>;

/// A node containing markdown content.
///
/// Untagged, so that either half serializes as a node of its own type.
#[derive_where(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(untagged, bound = "", from = "repr::Repr<'data, S>")
)]
pub enum Node<'data, S: Span> {
	Modifier(Modifier<'data, S>),
	Element(Element<'data, S, Node<'data, S>>),
}

/// Node wrapped in a span.
pub type SpannedNode<'data, S> = Spanned<Node<'data, S>, S>;
/// A vec of nodes, all of which are wrapped in a span.
pub type SpannedNodes<'data, S> = Sequence<S, Node<'data, S>>;

impl<'data, S> Node<'data, S>
where
	S: Span,
{
	/// Returns an iterator over all child nodes of this node. Yields no items if this node has no
	/// children.
	pub fn children(&self) -> impl Iterator<Item = &Node<'data, S>> {
		let (content, element) = match self {
			Self::Modifier(modifier) => (Some(modifier.content()), None),
			Self::Element(element) => (None, Some(element)),
		};

		content
			.into_iter()
			.chain(element.into_iter().flat_map(Element::sequences))
			.flat_map(|items| items.iter().map(|span| &span.value))
	}

	/// Returns an iterator over this node and all child nodes, at every depth.
	///
	/// Depth matters to [`Self::content`] and [`Self::rules`]: a markup wrapper's own [`Self::text`]
	/// is [`None`], so stopping at the direct children made `**_text_**` look textless.
	#[must_use]
	pub fn iter<'node>(&'node self) -> Iter<'data, 'node, S> {
		Iter {
			node: Some(self),
			// TODO: it's a bit awkward to re-box after this technically returns a pre-boxed iterator
			children: Some(Box::new(self.children().flat_map(Node::iter))),
		}
	}

	/// The [`Rule`] that this node corresponds to. Returns [`None`] if this is a base rule.
	#[must_use]
	pub fn rule(&self) -> Option<Rule> {
		match self {
			Self::Modifier(modifier) => Some(modifier.kind().rule()),
			Self::Element(element) => element.rule(),
		}
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
		match self {
			Self::Modifier(_) => None,
			Self::Element(element) => element.text(),
		}
	}

	/// Text content of this node _and_ its children.
	#[must_use]
	pub fn content(&self) -> String {
		self.iter().filter_map(Node::text).collect()
	}

	/// Recursively flattens this node's children, collapsing any markup made redundant by
	/// `active` -- the markup its ancestors already apply.
	///
	/// Only markup joins `active`, but it crosses block containers, so a block-level italic
	/// collapses the italics in the paragraphs and lists it wraps. A link owns its own inline
	/// content, which its own [`flatten`] has already flattened, so `active` stops there.
	pub fn flatten_children(&mut self, mut active: RuleSet) {
		match self {
			Self::Modifier(modifier) => {
				active.insert(modifier.kind().rule());
				flatten_against(&mut modifier.content_mut().value, active);
			}
			// with nothing active, a block's content is exactly as its own `flatten` left it
			Self::Element(_) if active.is_empty() => {}
			Self::Element(element) => {
				for content in element.sequences_mut() {
					flatten_against(&mut content.value, active);
				}
			}
		}
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
			Self::Modifier(modifier) => Some(take(&mut modifier.content_mut().value)),
			Self::Element(_) => None,
		}
	}

	fn is_empty(&self) -> bool {
		match self {
			Self::Modifier(modifier) => modifier.content().is_empty(),
			// TODO: should we flatten code?
			Self::Element(Element::Text(content)) => content.is_empty(),
			Self::Element(_) => false,
		}
	}
}

impl<'data, 'node, S> IntoIterator for &'node Node<'data, S>
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
			Self::Modifier(modifier) => Unparse::fmt(modifier, f),
			Self::Element(element) => Unparse::fmt(element, f),
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

/// Flattens each of `nodes` against `active`, then collapses and merges them.
fn flatten_against<S>(nodes: &mut Vec<SpannedNode<'_, S>>, active: RuleSet)
where
	S: Span,
{
	let mut nested = false;
	for node in nodes.iter_mut() {
		node.value.flatten_children(active);
		nested |= node.value.is_nested_in(active);
	}

	// a collapsed child's own children were flattened against this same set, so one round is
	// enough -- nothing spliced in can be redundant again
	if nested {
		collapse_nested(nodes, active);
	}

	merge_siblings(nodes);
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
			if !merge_into(&mut current_node.value, &mut node.value) {
				current_node = node;
				continue;
			}

			current_node.span.merge(&node.span);
		}
	}

	nodes.retain(|item| !item.value.is_empty());
}

/// Moves `next` into `current` if the two are the same kind of node and merge, leaving `next`
/// empty.
fn merge_into<'data, S>(current: &mut Node<'data, S>, next: &mut Node<'data, S>) -> bool
where
	S: Span,
{
	match (current, next) {
		(Node::Modifier(current), Node::Modifier(next)) => {
			let kind = next.kind();
			if current.kind() != kind || !kind.merges() {
				return false;
			}

			let (current_children, children) = (current.content_mut(), next.content_mut());
			current_children.span.merge(&children.span);
			current_children.extend(take(&mut children.value));
			merge_siblings(&mut current_children.value);
			true
		}
		(Node::Element(Element::Text(current_content)), Node::Element(Element::Text(content))) => {
			current_content.to_mut().push_str(&take(content));
			true
		}
		_ => false,
	}
}

#[cfg(test)]
mod test {
	use super::{Element, Modifier, Node, SpannedNode, SpannedNodes, flatten};
	use crate::span::{Span, Spanned, TrackedSpan};
	use crate::{bold, italic, link, spoiler, strikethrough, text, underline};

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
			Node::Element(Element::Text(content)) => content,
			other => panic!("expected text, got {other:?}"),
		}
	}

	fn children_of<'node>(
		node: &'node SpannedNode<'static, TrackedSpan>,
	) -> &'node SpannedNodes<'static, TrackedSpan> {
		match &node.value {
			Node::Modifier(modifier) => modifier.content(),
			other @ Node::Element(_) => panic!("expected markup, got {other:?}"),
		}
	}

	/// The inner wrapper carries no meaning, since the outer one already applies.
	#[test]
	fn nested_markup_collapses() {
		assert_eq!(flattened(italic!(italic!("a"))), italic!("a"));
		assert_eq!(flattened(bold!(bold!("a"))), bold!("a"));
		assert_eq!(flattened(underline!(underline!("a"))), underline!("a"));
		assert_eq!(
			flattened(strikethrough!(strikethrough!("a"))),
			strikethrough!("a")
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
				Node::Modifier(Modifier::Bold(Spanned {
					value: vec![spanned(text!("a"), 2, 3)],
					span: TrackedSpan::new(2, 3),
				})),
				0,
				5,
			),
			spanned(
				Node::Modifier(Modifier::Bold(Spanned {
					value: vec![spanned(text!("b"), 7, 8)],
					span: TrackedSpan::new(7, 8),
				})),
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
			Node::Modifier(Modifier::Italic(Spanned {
				value: vec![spanned(
					Node::Modifier(Modifier::Italic(Spanned {
						value: vec![spanned(text!("a"), 3, 4)],
						span: TrackedSpan::new(3, 4),
					})),
					2,
					5,
				)],
				span: TrackedSpan::new(1, 6),
			})),
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
