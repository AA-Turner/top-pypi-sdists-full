//! Inline content: the [`Inline`] nodes of the finished tree, and the parsers for inline markdown
//! content.

use std::{borrow::Cow, fmt::Debug, marker::PhantomData, mem::take};

use derive_where::derive_where;
use nom::Parser;
use nom::branch::alt;
use nom::character::complete::{anychar, line_ending};
use nom::combinator::map;
use nom::multi::many1;
use nom::sequence::preceded;
use tracing::Level;

use crate::{
	Input,
	context::{Context, fuel::ApplyFuel},
	error::ParseError,
	range::delim,
	scope::Scope,
	span::{Span, TraceOk, TraceParse, WithSpan},
	unparse::Unparse,
};

use self::{
	code_block::CodeBlock, emoji::Emoji, link::Link, mention::Mention, timestamp::Timestamp,
};
use super::{
	Element, Elements, Id, Inlines, Iter, SpannedInline, merge_text,
	modifier::{
		ModifierKind, ModifierKinds, bold, italic,
		spoiler::{self, Spoiler},
		strikethrough, underline,
	},
};

pub use {
	code::code, code_block::code_block, link::link, mention::mention, text::text,
	timestamp::timestamp,
};

pub mod code;
pub mod code_block;
pub mod emoji;
pub mod link;
pub mod mention;
pub mod text;
pub mod timestamp;

/// Inline content of the finished tree: a modifier, which holds only more of it, or an inline
/// element.
#[derive_where(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case", bound = "")
)]
pub enum Inline<'data, S: Span> {
	// modifiers
	Bold(Inlines<'data, S>),
	Italic(Inlines<'data, S>),
	Underline(Inlines<'data, S>),
	Strikethrough(Inlines<'data, S>),
	Spoiler(Spoiler<'data, S>),

	// elements
	Emoji(Emoji<'data>),
	Timestamp(Timestamp),
	Mention(Mention),
	Link(Link<S, Inline<'data, S>>),
	Code(Cow<'data, str>),
	CodeBlock(CodeBlock<'data>),
	Text(Cow<'data, str>),
}

impl<'data, S: Span> Inline<'data, S> {
	/// The modifier of `kind` wrapping `content`.
	#[must_use]
	pub fn modifier(kind: ModifierKind, content: Inlines<'data, S>) -> Self {
		match kind {
			ModifierKind::Bold => Self::Bold(content),
			ModifierKind::Italic => Self::Italic(content),
			ModifierKind::Underline => Self::Underline(content),
			ModifierKind::Strikethrough => Self::Strikethrough(content),
			// numbered by `crate::range::resolve`
			ModifierKind::Spoiler => Self::Spoiler(Spoiler {
				id: Id::default(),
				content,
			}),
		}
	}

	/// Which modifier this is, if it is one.
	#[must_use]
	pub fn modifier_kind(&self) -> Option<ModifierKind> {
		Some(match self {
			Self::Bold(_) => ModifierKind::Bold,
			Self::Italic(_) => ModifierKind::Italic,
			Self::Underline(_) => ModifierKind::Underline,
			Self::Strikethrough(_) => ModifierKind::Strikethrough,
			Self::Spoiler(_) => ModifierKind::Spoiler,
			_ => return None,
		})
	}

	/// What this modifier wraps; [`None`] if it is not a modifier.
	#[must_use]
	pub fn modifier_content(&self) -> Option<&Inlines<'data, S>> {
		match self {
			Self::Bold(content)
			| Self::Italic(content)
			| Self::Underline(content)
			| Self::Strikethrough(content)
			| Self::Spoiler(Spoiler { content, .. }) => Some(content),
			_ => None,
		}
	}

	/// As [`Self::modifier_content`], mutably.
	pub fn modifier_content_mut(&mut self) -> Option<&mut Inlines<'data, S>> {
		match self {
			Self::Bold(content)
			| Self::Italic(content)
			| Self::Underline(content)
			| Self::Strikethrough(content)
			| Self::Spoiler(Spoiler { content, .. }) => Some(content),
			_ => None,
		}
	}

	/// Returns an iterator over all child nodes of this node: a modifier's content. Link text is
	/// not among them, being a scope of its own.
	pub fn children(&self) -> impl Iterator<Item = &Inline<'data, S>> {
		self.modifier_content()
			.into_iter()
			.flat_map(|content| content.iter().map(|inline| &inline.value))
	}

	/// Returns an iterator over this node and all child nodes, at every depth.
	///
	/// Depth matters to [`Self::content`]: a modifier's own [`Self::text`] is
	/// [`None`], so stopping at the direct children made `**_text_**` look textless.
	#[must_use]
	pub fn iter<'node>(&'node self) -> Iter<'data, 'node, S> {
		Iter {
			node: Some(self),
			// TODO: it's a bit awkward to re-box after this technically returns a pre-boxed iterator
			children: Some(Box::new(self.children().flat_map(Inline::iter))),
		}
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
			| Self::Timestamp(_)
			| Self::Emoji(Emoji::Custom(_))
			| Self::Link(Link { text: Some(_), .. }) => return None,
		})
	}

	/// Text content of this node _and_ its children.
	#[must_use]
	pub fn content(&self) -> String {
		self.iter().filter_map(Inline::text).collect()
	}
}

impl<'data, 'node, S: Span> IntoIterator for &'node Inline<'data, S> {
	type Item = &'node Inline<'data, S>;
	type IntoIter = Iter<'data, 'node, S>;

	fn into_iter(self) -> Self::IntoIter {
		self.iter()
	}
}

impl<S: Span> Unparse for Inline<'_, S> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self::Bold(content) => bold::unparse(content, f),
			Self::Italic(content) => italic::unparse(content, f),
			Self::Underline(content) => underline::unparse(content, f),
			Self::Strikethrough(content) => strikethrough::unparse(content, f),
			Self::Spoiler(Spoiler { content, .. }) => spoiler::unparse(content, f),
			Self::Emoji(emoji) => Unparse::fmt(emoji, f),
			Self::Timestamp(timestamp) => Unparse::fmt(timestamp, f),
			Self::Mention(mention) => Unparse::fmt(mention, f),
			Self::Link(link) => Unparse::fmt(link, f),
			Self::Code(code) => code::unparse(code, f),
			Self::CodeBlock(code_block) => Unparse::fmt(code_block, f),
			Self::Text(text) => f.write_str(text),
		}
	}
}

impl<'data, S> Inline<'data, S>
where
	S: Span,
{
	/// Recursively flattens this node's children, collapsing any markup made redundant by
	/// `active` -- the markup its ancestors already apply.
	///
	/// A link owns its own inline content, which its own [`flatten`] has already flattened, so
	/// `active` stops there.
	pub fn flatten_children(&mut self, mut active: ModifierKinds) {
		if let Some(kind) = self.modifier_kind() {
			active.insert(kind);
		}
		if let Some(content) = self.modifier_content_mut() {
			flatten_against(&mut content.value, active);
		}
	}

	/// Whether an ancestor already applies this node's markup.
	fn is_nested_in(&self, active: ModifierKinds) -> bool {
		self.modifier_kind()
			.is_some_and(|kind| active.contains(kind))
	}

	/// Takes the children of redundant markup, leaving it empty. [`None`] if it is not redundant.
	fn take_nested_children(
		&mut self,
		active: ModifierKinds,
	) -> Option<Vec<SpannedInline<'data, S>>> {
		if !self.is_nested_in(active) {
			return None;
		}
		self.modifier_content_mut()
			.map(|content| take(&mut content.value))
	}

	fn is_empty(&self) -> bool {
		match self {
			// TODO: should we flatten code?
			Self::Text(content) => content.is_empty(),
			_ => self
				.modifier_content()
				.is_some_and(|content| content.is_empty()),
		}
	}
}

/// Recursively merges adjacent nodes of the same type, and collapses markup nested inside the same
/// markup, in order to produce a more optimized AST.
#[tracing::instrument(level = Level::TRACE)]
pub fn flatten<S>(nodes: &mut Vec<SpannedInline<'_, S>>)
where
	S: Span,
{
	for node in nodes.iter_mut() {
		node.value.flatten_children(ModifierKinds::empty());
	}

	merge_siblings(nodes);
}

/// Same as [`flatten`] but with owned data.
#[must_use]
pub fn flatten_owned<S>(mut nodes: Vec<SpannedInline<'_, S>>) -> Vec<SpannedInline<'_, S>>
where
	S: Span,
{
	flatten(&mut nodes);
	nodes
}

/// Flattens each of `nodes` against `active`, then collapses and merges them.
fn flatten_against<S>(nodes: &mut Vec<SpannedInline<'_, S>>, active: ModifierKinds)
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
fn collapse_nested<S>(nodes: &mut Vec<SpannedInline<'_, S>>, active: ModifierKinds)
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
fn merge_siblings<S>(nodes: &mut Vec<SpannedInline<'_, S>>)
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
fn merge_into<'data, S>(current: &mut Inline<'data, S>, next: &mut Inline<'data, S>) -> bool
where
	S: Span,
{
	if let (Inline::Text(current_content), Inline::Text(content)) = (&mut *current, &mut *next) {
		current_content.to_mut().push_str(&take(content));
		return true;
	}

	let Some(kind) = next.modifier_kind() else {
		return false;
	};
	if current.modifier_kind() != Some(kind) || !kind.merges() {
		return false;
	}
	let (Some(current_children), Some(children)) =
		(current.modifier_content_mut(), next.modifier_content_mut())
	else {
		return false;
	};
	current_children.span.merge(&children.span);
	current_children.extend(take(&mut children.value));
	merge_siblings(&mut current_children.value);
	true
}

struct InlineParser<S, E> {
	context: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Clone for InlineParser<S, E> {
	fn clone(&self) -> Self {
		Self {
			context: self.context.clone(),
			span: PhantomData,
			error: PhantomData,
		}
	}
}

impl<S, E> Debug for InlineParser<S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("InlineParser")
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for InlineParser<S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = Elements<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "inline_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let ctx = self.context.with_hints(&input);

		#[allow(
			clippy::let_and_return,
			reason = "`tracing::instrument` keeps a tail expression's temporaries, which borrow `ctx`, \
			          alive past it"
		)]
		let result = many1(alt((
			ctx.matched_pairs()
				// TODO: this should respect the inner content by outputting a Node (or list of Nodes) rather than Input
				.map(|seq| Element::<S>::Text(seq.content.into()))
				.span(),
			ctx.guard_terminal_sequence(|| {
				alt((
					ctx.allowed_inline_syntax(),
					// resolved into modifiers once the whole message is parsed; see `crate::range`
					delim::delim(ctx.syntaxes).map(Element::Delim),
					preceded((line_ending, ctx.line_prefix()), ctx.allowed_block_syntax()),
					text::text(ctx.clone()).map(|content| Element::Text(Cow::Owned(content))),
					// If we failed to capture the current character after stepping through all rules
					// then we are likely dealing with an unpaired control character, so consume it
					// and allow the rules to continue.
					map(anychar, |ch: char| Element::Text(ch.to_string().into())),
				))
			})
			.span(),
		)))
		.apply_fuel(self.context.remaining_fuel())
		.map(|mut pieces| {
			merge_text(&mut pieces);
			pieces
		})
		.span()
		.trace_parse()
		.process::<OM>(input)
		.trace_ok();
		result
	}
}

/// Parse inline content.
#[must_use]
pub fn inline<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	InlineParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::{
		Inline, Inlines, SpannedInline, flatten, inline, mention::Mention, timestamp::Timestamp,
	};
	use crate::span::{Span, Spanned, TrackedSpan};
	use crate::{
		bold, code, code_block, emoji, italic, link, spanned_vec, spoiler, strikethrough,
		test_utils::{handle_nom_err, resolved_inlines},
		text, underline,
		{context::Context, node::Element},
	};

	/// Wraps untracked nodes, which need no spans, so they can be flattened.
	fn unspanned(nodes: Vec<Inline<'static, ()>>) -> Vec<SpannedInline<'static, ()>> {
		nodes
			.into_iter()
			.map(|value| Spanned { value, span: () })
			.collect()
	}

	/// Flattens a node on its own, expecting a single node back.
	fn flattened(node: Inline<'static, ()>) -> Inline<'static, ()> {
		let mut nodes = unspanned(vec![node]);
		flatten(&mut nodes);
		assert_eq!(nodes.len(), 1, "expected a single node, got {nodes:?}");
		nodes.remove(0).value
	}

	fn spanned(
		value: Inline<'static, TrackedSpan>,
		start: usize,
		end: usize,
	) -> SpannedInline<'static, TrackedSpan> {
		Spanned {
			value,
			span: TrackedSpan::new(start, end),
		}
	}

	fn text_of<'node>(node: &'node SpannedInline<'static, TrackedSpan>) -> &'node str {
		match &node.value {
			Inline::Text(content) => content,
			other => panic!("expected text, got {other:?}"),
		}
	}

	fn children_of<'node>(
		node: &'node SpannedInline<'static, TrackedSpan>,
	) -> &'node Inlines<'static, TrackedSpan> {
		node.value
			.modifier_content()
			.unwrap_or_else(|| panic!("expected markup, got {:?}", node.value))
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
				Inline::Bold(Spanned {
					value: vec![spanned(text!("a"), 2, 3)],
					span: TrackedSpan::new(2, 3),
				}),
				0,
				5,
			),
			spanned(
				Inline::Bold(Spanned {
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
			Inline::Italic(Spanned {
				value: vec![spanned(
					Inline::Italic(Spanned {
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

	#[test]
	fn compound_test() {
		let s = r"_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![italic!(
				text!("foo t_a "),
				bold!("bat"),
				text!(" "),
				emoji!(id = 1234, name = "abcd", animated),
				Inline::Timestamp(Timestamp {
					value: 1234,
					style: None,
				}),
				Inline::Mention(Mention::User(1234)),
				text!(" butt")
			)]
		);
	}

	/// An underscore glued to a word on both sides is part of that word, not a delimiter, so it
	/// must not open an italic -- otherwise the *opening* `_` of a later, real italic gets consumed
	/// as its closer and everything between the two is wrongly emphasised.
	#[test]
	fn intraword_underscore_does_not_open_italic() {
		let s = "the discord_admin codebase and _really_ don't";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![
				text!("the discord_admin codebase and "),
				italic!("really"),
				text!(" don't")
			]
		);
	}

	/// As [`intraword_underscore_does_not_open_italic`], for an underscore followed by `(` rather
	/// than by another alphanumeric.
	#[test]
	fn intraword_underscore_paren_does_not_open_italic() {
		let s = "Endemic_(epidemiology) and _really_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("Endemic_(epidemiology) and "), italic!("really")]
		);
	}

	/// A consequence of the rule above: the underscore that would have opened the italic never
	/// gets the chance, so the trailing one has nothing to close and stays literal.
	#[test]
	fn trailing_underscore_after_word_is_literal() {
		let s = "foo_bar baz_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec![text!("foo_bar baz_")]);
	}

	/// The override is anchored on a *preceding* alphanumeric, so an underscore that starts a word
	/// still opens an italic -- including the `_(` case, which the terminal-side override treats
	/// unconditionally.
	#[test]
	fn leading_underscore_still_opens_italic() {
		let s = "_(foo)_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec![italic!("(foo)")]);
	}

	/// Whether `block`, or any block or inline node at any depth inside it, is a bold.
	fn has_bold(block: &crate::node::Block<'_, ()>) -> bool {
		block
			.inlines()
			.any(|inline| inline.iter().any(|node| matches!(node, Inline::Bold(_))))
			|| block.blocks().any(has_bold)
	}

	/// A bold nested in an asterisk italic survives in every container, because they all descend
	/// through the same terminal guard.
	#[test]
	fn nested_bold_survives_in_any_container() {
		for s in [
			"*foo **bar** baz*",
			"> *foo **bar** baz*",
			"# *foo **bar** baz*",
		] {
			let res = crate::parse::<(), _>(s, crate::context::Options::default())
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert!(
				res.iter().any(|block| has_bold(block)),
				"expected a nested bold for {s:?}, got {res:?}"
			);
		}
	}

	/// Three underscores are an ambiguous run, so the overlapping-rule probe stays out of it and
	/// the rules resolve it in declaration order -- `Italic` precedes `Underline`, so the italic is
	/// the outer node. Both orders render the same, but pin it so the choice is deliberate.
	#[test]
	fn a_triple_underscore_run_nests_italic_outside_underline() {
		let s = "___foo___";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![italic!(underline!("foo"))]
		);
	}

	#[test]
	fn link_detection() {
		let s = "foo https://wnelson.dev bar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), link!("https://wnelson.dev"), text!(" bar"),]
		);
	}

	#[test]
	fn link_in_a_parenthetical() {
		let s = "(see https://wnelson.dev).";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("(see "), link!("https://wnelson.dev"), text!(").")]
		);
	}

	#[test]
	fn masked_links() {
		let s = "foo [bar](https://wnelson.dev) baz";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![
				text!("foo "),
				link!("https://wnelson.dev", [text!("bar")]),
				text!(" baz"),
			]
		);
	}

	#[test]
	fn multi_line_end() {
		let s = "foo\nbar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec![text!("foo\nbar")]);
	}

	#[test]
	fn simple_code() {
		let s = "`foo`";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec![code!("foo")]);
	}

	#[test]
	fn complex_code() {
		let s = "foo `ba**r**`";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), code!("ba**r**")]
		);
	}

	#[test]
	fn simple_codeblock() {
		let s = "```\nfoo```";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec![code_block!("foo")]);
	}

	#[test]
	fn complex_codeblock() {
		let s = "foo **bar**```baz\n_bar_``` _butt_";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![
				text!("foo "),
				bold!("bar"),
				code_block!(language = "baz", "_bar_"),
				text!(" "),
				italic!("butt")
			]
		);
	}

	#[test]
	fn text_with_emoji() {
		let s = "foo 🦶";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), emoji!("🦶"),]
		);
	}

	#[test]
	fn text_with_colon_delimited_emoji() {
		let s = "foo :foot:";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), emoji!("🦶"),]
		);
	}

	#[test]
	fn text_with_spoiler() {
		let s = "foo ||bar|| baz";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), spoiler!("bar"), text!(" baz")]
		);
	}

	// TODO | We need to capture the fact that the <...> was present in the generated AST. Right now we just lose that info.
	// TODO |  It is important for preventing link embedding on the backend.
	#[test]
	fn text_with_autolink() {
		let s = "foo <https://wnelson.dev> bar";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![text!("foo "), link!("https://wnelson.dev"), text!(" bar")]
		);
	}

	#[test]
	fn text_with_nested_rules() {
		let s = "**foo __bar **baz** foo__ bar**";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inlines(res),
			spanned_vec![bold!("foo __bar "), text!("baz"), bold!(" foo__ bar")]
		);
	}

	/// A schemaless host in the middle of a word is not a link.
	///
	/// Without this, `getscammeddiscord.gg/x` hands a scam domain a real invite: the run before the
	/// host becomes its own text node and the tail becomes a coded link, so the client resolves an
	/// invite for a domain the author never wrote. The same shape keeps a scheme we do not support
	/// from being silently dropped -- `ftp://discord.gg/x` must not become an invite either.
	#[test]
	fn schemaless_domain_mid_token_is_text() {
		for s in [
			"getscammeddiscord.gg/invitelink",
			"getscammed_discord.gg/invitelink",
			"getscammed1discord.gg/invitelink",
			// a zero-width space is not whitespace, and reads as one token
			"getscammed\u{200b}discord.gg/invitelink",
			"ftp://discord.gg/code",
			"javascript://discord.gg/code",
			"//discord.gg/code",
			"xdiscord.gg/code",
		] {
			let (rem, res) = inline::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			let res = resolved_inlines(res);

			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert!(
				res.iter().all(|node| matches!(node.value, Inline::Text(_))),
				"expected only text for {s:?}, got {res:?}"
			);
		}
	}

	/// A host inside the run of an existing link does not start a second one.
	#[test]
	fn schemaless_domain_inside_a_link_is_part_of_it() {
		let s = "canary.discord.com/quests/1suffix.discord.com/quests/2";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res.value.len(), 1, "expected one node, got {res:?}");
		assert!(
			matches!(res.value[0].value, Element::Link(_)),
			"expected a link, got {res:?}"
		);
	}

	/// The boundary is whitespace, not "anything non-alphanumeric".
	#[test]
	fn schemaless_domain_after_whitespace_is_a_link() {
		for s in [
			"discord.gg/code",
			"hello discord.gg/code",
			"hello\ndiscord.gg/code",
			"hello\tdiscord.gg/code",
			// the whole host, not `discord.gg` at an offset inside it
			"www.discord.gg/code",
		] {
			let (rem, res) = inline::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");

			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert!(
				res.iter()
					.any(|node| matches!(node.value, Element::Link(_))),
				"expected a link for {s:?}, got {res:?}"
			);
		}
	}

	/// A scheme delimits itself, so it is still detected mid-token.
	#[test]
	fn schemed_url_mid_token_still_detected() {
		let s = "lolhttps://discord.gg/code";
		let (rem, res) = inline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert!(
			res.iter()
				.any(|node| matches!(node.value, Element::Link(_))),
			"expected a link, got {res:?}"
		);
	}
}
