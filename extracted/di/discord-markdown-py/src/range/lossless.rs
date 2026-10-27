//! Building the lossless tree of [`crate::lossless`] from a parse, with the same pairing as
//! [`super::resolve`] but none of its normalization.

use crate::{
	lossless::{Child, Node, NodeKind, Side, Token, TokenKind},
	node::{
		Element, Elements, Id, Ids, SpannedElement,
		block::{Heading, List, Small},
	},
	span::{LosslessSpan, Span, Spanned, TrackedSpan},
	syntax::SyntaxSet,
};

use super::{
	Content, PieceInfo, SeqInfo, Unmatched,
	delim::Offset,
	pair::{Matches, RangeId, RangeTree},
	place,
};

/// The text a parse ran over, and where it starts.
#[derive(Debug, Clone, Copy)]
pub struct Source<'data> {
	pub text: &'data str,
	pub start: usize,
}

impl<'data> Source<'data> {
	fn slice(self, start: usize, end: usize) -> &'data str {
		&self.text[start - self.start..end - self.start]
	}

	fn token(self, kind: TokenKind, start: usize, end: usize) -> Child<'data> {
		Child::Token(Token {
			kind,
			text: self.slice(start, end),
			span: TrackedSpan::new(start, end),
		})
	}

	/// The syntax the parser recorded in `span`.
	fn syntax(self, span: &LosslessSpan) -> impl Iterator<Item = Child<'data>> {
		span.syntax
			.iter()
			.map(move |token| self.token(token.kind, token.start, token.end))
	}

	/// A node spanning `span`, of `children` and the syntax recorded alongside them, in any order.
	///
	/// Every byte of `span` should be one of them. Should the parser have consumed something it did
	/// not record, it becomes a text token, so the tree still writes back exactly.
	fn node(
		self,
		kind: NodeKind<'data>,
		span: TrackedSpan,
		mut children: Vec<Child<'data>>,
	) -> Node<'data> {
		children.sort_by_key(|child| child.span().start);

		let mut covered = Vec::with_capacity(children.len());
		let mut at = span.start;
		for child in children {
			let child_span = child.span();
			debug_assert!(
				child_span.start >= at,
				"{child:?} overlaps what precedes it in {kind:?}"
			);
			if child_span.start > at {
				debug_assert!(
					false,
					"unrecorded syntax {:?} in {kind:?}",
					self.slice(at, child_span.start)
				);
				covered.push(self.token(TokenKind::Text, at, child_span.start));
			}
			at = child_span.end;
			covered.push(child);
		}
		if span.end > at {
			debug_assert!(
				false,
				"unrecorded syntax {:?} in {kind:?}",
				self.slice(at, span.end)
			);
			covered.push(self.token(TokenKind::Text, at, span.end));
		}

		Node {
			kind,
			span,
			children: covered,
		}
	}
}

fn tracked(span: &LosslessSpan) -> TrackedSpan {
	TrackedSpan::new(span.start, span.end)
}

/// The span from the first of `children` to the last.
fn cover(children: &[Child<'_>]) -> TrackedSpan {
	let mut span = children[0].span().clone();
	span.merge(children[children.len() - 1].span());
	span
}

/// A piece of content, with the ranges to wrap it in, innermost first.
type Item<'data> = (Child<'data>, Vec<RangeId>);

struct Builder<'a, 'data> {
	matches: &'a Matches,
	ranges: &'a RangeTree,
	allowed: SyntaxSet,
	/// The id of range zero; range `n` has its `n`th.
	base: Id,
	ids: &'a mut Ids,
	source: Source<'data>,
}

impl<'a, 'data> Builder<'a, 'data> {
	fn new(
		matches: &'a Matches,
		ranges: &'a RangeTree,
		allowed: SyntaxSet,
		ids: &'a mut Ids,
		source: Source<'data>,
	) -> Self {
		let base = ids.reserve(ranges.len());
		Self {
			matches,
			ranges,
			allowed,
			base,
			ids,
			source,
		}
	}

	/// As [`super::Rebuild::around`].
	fn around(&self, wrap: Option<RangeId>, applied: usize) -> Vec<RangeId> {
		self.ranges
			.ancestors(wrap)
			.take_while(|&range| self.ranges[range].depth > applied)
			.collect()
	}

	/// Build a sequence of blocks, with the syntax recorded for it.
	fn blocks(
		&mut self,
		seq: Elements<'data, LosslessSpan>,
		info: SeqInfo,
		applied: usize,
	) -> Vec<Child<'data>> {
		let mut blocks: Vec<_> = self.source.syntax(&seq.span).collect();
		for (piece, info) in seq.value.into_iter().zip(info) {
			self.block(piece, info, applied, &mut blocks);
		}
		blocks
	}

	fn block(
		&mut self,
		piece: SpannedElement<'data, LosslessSpan>,
		info: PieceInfo,
		applied: usize,
		out: &mut Vec<Child<'data>>,
	) {
		let source = self.source;
		// in the order of `Element::sequences`
		let mut seqs = info.seqs.into_iter();
		let mut next = move || seqs.next().expect("placed");
		let Spanned { value, span } = piece;
		let mut children: Vec<_> = source.syntax(&span).collect();
		let kind = match value {
			Element::Paragraph(content) => {
				children.extend(self.inlines(content, next(), applied));
				NodeKind::Paragraph
			}
			Element::Heading(Heading { level, content }) => {
				children.extend(self.inlines(content, next(), applied));
				NodeKind::Heading { level }
			}
			Element::Small(Small { content }) => {
				children.extend(self.inlines(content, next(), applied));
				NodeKind::Small
			}
			Element::Quote(kind, content) => {
				children.extend(self.blocks(content, next(), applied));
				NodeKind::Quote(kind)
			}
			Element::List(List { kind, items }) => {
				// the line prefixes before later items
				children.extend(source.syntax(&items.span));
				for item in items.value {
					let content = self.blocks(item.content, next(), applied);
					let span = content.iter().map(Child::span).fold(
						content[0].span().clone(),
						|mut span, child| {
							span.merge(child);
							span
						},
					);
					children.push(Child::Node(source.node(NodeKind::ListItem, span, content)));
				}
				NodeKind::List(kind)
			}
			Element::Empty => NodeKind::Empty,
			// Inline content among blocks: delimiters, spent or not, before a block or alone on
			// their line. The delimiters stay among the blocks, with the line ending after them;
			// leftover characters get a paragraph, with the ranges around them inside.
			value @ (Element::Delim(_)
			| Element::Emoji(_)
			| Element::Timestamp(_)
			| Element::Mention(_)
			| Element::Link(_, _)
			| Element::Code(_)
			| Element::CodeBlock(_)
			| Element::Text(_)) => {
				out.extend(children);
				let mut pending = Vec::new();
				for (child, around) in
					self.inline_items(Spanned { value, span }, info.wrap, applied)
				{
					if matches!(child, Child::Token(_)) {
						self.flush_paragraph(&mut pending, out);
						out.push(child);
					} else {
						pending.push((child, around));
					}
				}
				self.flush_paragraph(&mut pending, out);
				return;
			}
		};
		out.push(Child::Node(source.node(kind, tracked(&span), children)));
	}

	fn flush_paragraph(&self, pending: &mut Vec<Item<'data>>, out: &mut Vec<Child<'data>>) {
		if pending.is_empty() {
			return;
		}
		let children = self.wrap(std::mem::take(pending));
		let span = cover(&children);
		out.push(Child::Node(self.source.node(
			NodeKind::Paragraph,
			span,
			children,
		)));
	}

	/// Build a sequence of inline content, wrapping it in the ranges that cover it, with the
	/// syntax recorded for it.
	fn inlines(
		&mut self,
		seq: Elements<'data, LosslessSpan>,
		info: SeqInfo,
		applied: usize,
	) -> Vec<Child<'data>> {
		let mut items = Vec::with_capacity(seq.value.len());
		for (piece, info) in seq.value.into_iter().zip(info) {
			items.extend(self.inline_items(piece, info.wrap, applied));
		}
		let mut children = self.wrap(items);
		children.extend(self.source.syntax(&seq.span));
		children
	}

	/// One piece of inline content, with the ranges around each part of it. A delimiter run is
	/// split into what it closes, its leftover text and what it opens, each in its own ranges.
	fn inline_items(
		&mut self,
		piece: SpannedElement<'data, LosslessSpan>,
		wrap: Option<RangeId>,
		applied: usize,
	) -> Vec<Item<'data>> {
		let source = self.source;
		let Spanned { value, span } = piece;
		let Element::Delim(delim) = value else {
			return vec![(self.leaf(value, &span), self.around(wrap, applied))];
		};

		let matched = self.matches.of(&delim);
		let mut items = Vec::new();
		let mut at = span.start;
		let delimiter = |range: RangeId, side, at: &mut usize| {
			let end = *at + self.ranges[range].chars;
			let kind = TokenKind::Delimiter {
				kind: self.ranges[range].kind,
				id: self.base.nth(range),
				side,
			};
			let token = source.token(kind, *at, end);
			*at = end;
			(token, self.around(Some(range), applied))
		};
		for &range in &matched.closes {
			items.push(delimiter(range, Side::Close, &mut at));
		}
		if matched.leftover > 0 {
			let end = at + matched.leftover;
			let text = source.slice(at, end);
			let node = Node {
				kind: NodeKind::Text(text.into()),
				span: TrackedSpan::new(at, end),
				children: vec![source.token(TokenKind::Text, at, end)],
			};
			at = end;
			items.push((Child::Node(node), self.around(wrap, applied)));
		}
		for &range in &matched.opens {
			items.push(delimiter(range, Side::Open, &mut at));
		}
		debug_assert_eq!(at, span.start + delim.len, "a run is spent exactly");
		items
	}

	/// An inline element other than a delimiter, of the syntax its parser recorded and, for a link,
	/// its text.
	fn leaf(&mut self, value: Element<'data, LosslessSpan>, span: &LosslessSpan) -> Child<'data> {
		let mut children: Vec<_> = self.source.syntax(span).collect();
		let kind = match value {
			Element::Text(text) => NodeKind::Text(text),
			Element::Code(code) => NodeKind::Code(code),
			Element::CodeBlock(code_block) => NodeKind::CodeBlock(code_block),
			Element::Emoji(emoji) => NodeKind::Emoji(emoji),
			Element::Mention(mention) => NodeKind::Mention(mention),
			Element::Timestamp(timestamp) => NodeKind::Timestamp(timestamp),
			Element::Link(kind, link) => {
				// link text is a scope of its own
				if let Some(text) = link.text {
					children.extend(resolve_inline(text, self.allowed, self.ids, self.source));
				}
				NodeKind::Link {
					kind,
					url: link.url,
					title: link.title,
				}
			}
			Element::Delim(_)
			| Element::Heading(_)
			| Element::List(_)
			| Element::Paragraph(_)
			| Element::Quote(..)
			| Element::Small(_)
			| Element::Empty => {
				unreachable!("inline content is parsed with the inline rules alone")
			}
		};
		Child::Node(self.source.node(kind, tracked(span), children))
	}

	/// Wrap each run of `items` sharing their outermost range in that range's node, as
	/// [`super::wrap`] does. Each node spans exactly its content, its delimiters among it.
	fn wrap(&self, items: Vec<Item<'data>>) -> Vec<Child<'data>> {
		let mut out = Vec::with_capacity(items.len());
		let mut items = items.into_iter().peekable();

		while let Some((child, mut apply)) = items.next() {
			let Some(range) = apply.pop() else {
				out.push(child);
				continue;
			};

			let mut run = vec![(child, apply)];
			while let Some((child, mut apply)) =
				items.next_if(|(_, apply)| apply.last() == Some(&range))
			{
				apply.pop();
				run.push((child, apply));
			}

			let children = self.wrap(run);
			out.push(Child::Node(Node {
				kind: NodeKind::Modifier {
					kind: self.ranges[range].kind,
					id: self.base.nth(range),
				},
				span: cover(&children),
				children,
			}));
		}

		out
	}
}

/// Build the lossless tree of a parsed scope of inline content, like link text.
fn resolve_inline<'data>(
	nodes: Elements<'data, LosslessSpan>,
	allowed: SyntaxSet,
	ids: &mut Ids,
	source: Source<'data>,
) -> Vec<Child<'data>> {
	let (matches, ranges, info) = place(&nodes.value, allowed, Content::Inline, Unmatched::Text)
		.unwrap_or_else(|_| unreachable!("only a rejecting resolve fails"));
	Builder::new(&matches, &ranges, allowed, ids, source).inlines(nodes, info, 0)
}

/// Build the lossless tree of a parsed message from `source`, pairing its delimiters as
/// [`super::resolve`] does.
///
/// # Errors
/// As [`super::resolve`].
pub fn resolve<'data>(
	nodes: Elements<'data, LosslessSpan>,
	source: Source<'data>,
	allowed: SyntaxSet,
	unmatched: Unmatched,
	ids: &mut Ids,
) -> Result<Node<'data>, Vec<Offset>> {
	let (matches, ranges, info) = place(&nodes.value, allowed, Content::Blocks, unmatched)?;
	let children = Builder::new(&matches, &ranges, allowed, ids, source).blocks(nodes, info, 0);
	let span = TrackedSpan::new(source.start, source.start + source.text.len());
	Ok(source.node(NodeKind::Document, span, children))
}
