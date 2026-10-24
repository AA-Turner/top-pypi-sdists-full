//! Modifiers as style ranges.
//!
//! Instead of parsing a modifier's content recursively, parsing records each run of modifier
//! delimiters as a [`Delim`] token and carries on. [`resolve`] then pairs the tokens across the whole
//! message with a delimiter stack, and applies each pair to the finished tree as a range: wrapping
//! the inline content it covers, and splitting at every block, so no modifier holds a block.
//! Nothing about a modifier depends on where it sits relative to other rules.

pub mod delim;
pub mod pair;

use std::collections::HashMap;

use crate::{
	node::{
		Block, Blocks, Element, Elements, Id, Ids, Inline, Inlines, SpannedBlock, SpannedElement,
		SpannedInline,
		block::{Heading, List, Small, list::item::Item},
		flatten,
		inline::link::Link,
	},
	span::{Span, Spanned},
	syntax::SyntaxSet,
};
use delim::{Delim, Neighbor, Offset};
use pair::{Matches, RangeId, RangeTree, Token, pair};
use tracing::Level;

/// What the top level of a scope holds.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Content {
	/// Blocks, as a message or a quote does: leftover delimiters are wrapped in paragraphs.
	Blocks,
	/// Inline content, as link text is.
	Inline,
}

/// What [`resolve`] does with an opener that block syntax was recognized after but that matched
/// nothing.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Unmatched {
	/// Fail with its offset, so the caller can parse again with it disabled.
	Reject,
	/// Leave it as text where it stands.
	Text,
}

/// The first pass: every delimiter in document order, with the characters around it.
struct Collect {
	tokens: Vec<Token>,
	/// Where the tokens still waiting for the character after them begin.
	pending: usize,
	/// The last character before the current position; a line ending at the start of a block.
	prev: Neighbor,
	/// How many leaves the walk has passed.
	leaves: usize,
}

impl Collect {
	/// Move past something beginning with `first` and ending with `last`.
	fn chars(&mut self, first: Neighbor, last: Neighbor) {
		for token in &mut self.tokens[self.pending..] {
			token.next = first;
		}
		self.pending = self.tokens.len();
		self.prev = last;
	}

	/// Walk `seq` in document order, recording every delimiter in it and in its containers.
	#[tracing::instrument(name = "collect", level = Level::TRACE, skip_all)]
	fn seq<S: Span>(&mut self, seq: &[SpannedElement<'_, S>]) {
		for node in seq {
			match &node.value {
				Element::Delim(delim) => self.delim(*delim),
				element => self.element(element),
			}
		}
	}

	/// Record `delim` as a token, with the character before it; the one after it is filled in by
	/// whatever comes next.
	fn delim(&mut self, delim: Delim) {
		let prev = self.prev;
		let ch = Neighbor::Char(delim.ch.char());
		self.chars(ch, ch);
		self.tokens.push(Token {
			delim,
			prev,
			next: Neighbor::LINE_END,
			leaves: self.leaves,
		});
		// a delimiter alone on its line has a line ending after it, which the line consumed
		if delim.alone {
			self.chars(Neighbor::LINE_END, Neighbor::LINE_END);
		}
	}

	/// Move past `element`, which is not a delimiter: through the sequences of a container, or over
	/// a leaf, which counts as one and reads as its first and last characters.
	fn element<S: Span>(&mut self, element: &Element<'_, S>) {
		// A delimiter just before a block reads its first character, as `*` does in `*1. foo`;
		// one ending a block reads the line ending.
		if element.is_container() {
			for (_, content) in element.sequences() {
				self.prev = Neighbor::LINE_END;
				self.seq(content);
				self.chars(Neighbor::LINE_END, Neighbor::LINE_END);
			}
			return;
		}

		self.leaves += 1;
		match element {
			Element::Text(text) => {
				if let (Some(first), Some(last)) = (text.chars().next(), text.chars().last()) {
					self.chars(Neighbor::Char(first), Neighbor::Char(last));
				}
			}
			Element::Empty => self.chars(Neighbor::LINE_END, Neighbor::LINE_END),
			_ => self.chars(Neighbor::Atom, Neighbor::Atom),
		}
	}
}

/// The innermost ranges open at the first and at the last leaf of some content.
#[derive(Debug, Clone, Copy)]
struct Reach {
	first: Option<RangeId>,
	last: Option<RangeId>,
}

impl Reach {
	/// A single leaf, inside `open`.
	fn leaf(open: Option<RangeId>) -> Self {
		Self {
			first: open,
			last: open,
		}
	}

	/// The innermost range open across all of it.
	fn cover(self, ranges: &RangeTree) -> Option<RangeId> {
		ranges.common(self.first, self.last)
	}

	/// Two pieces of content, one after the other, either of which may hold no leaf.
	fn join(a: Option<Self>, b: Option<Self>) -> Option<Self> {
		match (a, b) {
			(Some(a), Some(b)) => Some(Self {
				first: a.first,
				last: b.last,
			}),
			_ => a.or(b),
		}
	}
}

/// Where a range covering a piece is wrapped.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum Placement {
	/// Around the piece.
	Here,
	/// Inside the piece, which is a container.
	Inside,
	/// Not at all, as a blank line between blocks is left uncovered.
	Nowhere,
}

/// Where a range covering `piece`, in a sequence holding `content`, is wrapped. Among blocks it
/// never wraps the block itself, so no modifier holds one.
fn placement<S: Span>(piece: &Element<'_, S>, content: Content) -> Placement {
	match (content, piece) {
		(Content::Blocks, Element::Empty) => Placement::Nowhere,
		(Content::Blocks, element) if element.is_container() => Placement::Inside,
		// leftover delimiters among blocks are wrapped inside the paragraph made for them
		_ => Placement::Here,
	}
}

/// What [`Place`] decides for one piece of a sequence.
struct PieceInfo {
	/// The innermost range wrapped around it in its sequence. The ranges around that one are too,
	/// less any an ancestor already applies.
	wrap: Option<RangeId>,
	/// Its [`Element::sequences`], in order; empty unless it is a container.
	seqs: Vec<SeqInfo>,
}

/// What [`Place`] decides for each piece of a sequence, in order.
type SeqInfo = Vec<PieceInfo>;

/// The third pass: where each range is wrapped.
struct Place<'a> {
	matches: &'a Matches,
	ranges: &'a RangeTree,
	/// The innermost range open where the walk is.
	open: Option<RangeId>,
}

impl Place<'_> {
	/// Decide where every range covering a piece of `seq`, which holds `content`, is wrapped, and
	/// find how far into the ranges `seq` as a whole reaches.
	#[tracing::instrument(name = "place", level = Level::TRACE, skip_all)]
	fn seq<S: Span>(
		&mut self,
		seq: &[SpannedElement<'_, S>],
		content: Content,
	) -> (Option<Reach>, SeqInfo) {
		let mut reach = None;
		let mut info = Vec::with_capacity(seq.len());
		for piece in seq {
			let (piece_reach, seqs) = self.piece(&piece.value);
			let cover = piece_reach.and_then(|reach| reach.cover(self.ranges));
			reach = Reach::join(reach, piece_reach);
			// a piece's placement is the same for every range, so the ranges wrapped around it are
			// all of those covering it, or none
			let wrap = (placement(&piece.value, content) == Placement::Here)
				.then_some(cover)
				.flatten();
			info.push(PieceInfo { wrap, seqs });
		}
		(reach, info)
	}

	/// Walk past `node`, tracking which range is open: the reach of its leaves, and what is decided
	/// for the sequences inside it.
	fn piece<S: Span>(&mut self, node: &Element<'_, S>) -> (Option<Reach>, Vec<SeqInfo>) {
		match node {
			Element::Delim(delim) => {
				let matched = self.matches.of(delim);
				if let Some(&outer) = matched.closes.last() {
					self.open = self.ranges[outer].parent;
				}
				// leftover characters are a leaf, between what it closes and what it opens
				let reach = (matched.leftover > 0).then_some(Reach::leaf(self.open));
				if let Some(&inner) = matched.opens.last() {
					self.open = Some(inner);
				}
				(reach, Vec::new())
			}
			element if element.is_container() => {
				let mut reach = None;
				let mut seqs = Vec::new();
				for (content, nodes) in element.sequences() {
					let (content_reach, info) = self.seq(nodes, content);
					reach = Reach::join(reach, content_reach);
					seqs.push(info);
				}
				(reach, seqs)
			}
			_ => (Some(Reach::leaf(self.open)), Vec::new()),
		}
	}
}

/// The last pass: rebuild the tree with every range applied.
struct Rebuild<'a> {
	matches: &'a Matches,
	ranges: &'a RangeTree,
	allowed: SyntaxSet,
	/// The id of range zero; range `n` has its `n`th.
	base: Id,
	/// The ids of the parse, for the link text resolved inside this scope.
	ids: &'a mut Ids,
}

impl<'a> Rebuild<'a> {
	/// A rebuild of `ranges`, claiming their spoiler ids from `ids`.
	fn new(
		matches: &'a Matches,
		ranges: &'a RangeTree,
		allowed: SyntaxSet,
		ids: &'a mut Ids,
	) -> Self {
		// claimed before rebuilding, so link text resolved along the way takes ids after these
		let base = ids.reserve(ranges.len());
		Self {
			matches,
			ranges,
			allowed,
			base,
			ids,
		}
	}

	/// The ranges wrapped around a piece whose innermost is `wrap`, innermost first, less what the
	/// `applied` outermost of them an ancestor already applies.
	fn around(&self, wrap: Option<RangeId>, applied: usize) -> Vec<RangeId> {
		self.ranges
			.ancestors(wrap)
			.take_while(|&range| self.ranges[range].depth > applied)
			.collect()
	}

	/// Rebuild a sequence of blocks, whose ancestors already apply the outermost `applied` ranges
	/// covering it. No range is wrapped around a block, only inside it.
	#[tracing::instrument(name = "rebuild_blocks", level = Level::TRACE, skip(self, seq, info))]
	fn blocks<'data, S: Span>(
		&mut self,
		seq: Vec<SpannedElement<'data, S>>,
		info: SeqInfo,
		applied: usize,
	) -> Vec<SpannedBlock<'data, S>> {
		let mut blocks = Vec::with_capacity(seq.len());
		for (piece, info) in seq.into_iter().zip(info) {
			let span = piece.span.clone();
			if let Some(value) = self.block(piece, info, applied) {
				blocks.push(Spanned { value, span });
			}
		}
		blocks
	}

	/// Rebuild one piece of a sequence of blocks, given what [`Place`] decided for it. [`None`] for
	/// a paragraph left with nothing in it.
	fn block<'data, S: Span>(
		&mut self,
		piece: SpannedElement<'data, S>,
		info: PieceInfo,
		applied: usize,
	) -> Option<Block<'data, S>> {
		// in the order of `Element::sequences`
		let mut seqs = info.seqs.into_iter();
		let mut next = move || seqs.next().expect("placed");
		let Spanned { value, span } = piece;
		Some(match value {
			Element::Paragraph(content) => {
				let content = self.inline_content(content, next(), applied);
				// nothing but delimiters, all of which were spent
				if content.value.is_empty() {
					return None;
				}
				Block::Paragraph(content)
			}
			Element::Heading(Heading { level, content }) => Block::Heading(Heading {
				level,
				content: self.inline_content(content, next(), applied),
			}),
			Element::Small(Small { content }) => Block::Small(Small {
				content: self.inline_content(content, next(), applied),
			}),
			Element::Quote(content) => Block::Quote(self.block_content(content, next(), applied)),
			Element::List(List { kind, items }) => Block::List(List {
				kind,
				items: Spanned {
					value: items
						.value
						.into_iter()
						.map(|item| Item {
							content: self.block_content(item.content, next(), applied),
						})
						.collect(),
					span: items.span,
				},
			}),
			Element::Empty => Block::Empty,
			// Inline content among blocks -- leftover delimiters, the only kind the grammar puts
			// here -- gets a paragraph, with the ranges around it inside.
			value => {
				let around = self.around(info.wrap, applied);
				let inline = self.inline(Spanned {
					value,
					span: span.clone(),
				})?;
				Block::Paragraph(Spanned {
					value: wrap(
						vec![(inline, around)],
						self.ranges,
						self.base,
						&HashMap::new(),
					),
					span,
				})
			}
		})
	}

	/// [`Self::blocks`] for the content of a container.
	fn block_content<'data, S: Span>(
		&mut self,
		nodes: Elements<'data, S>,
		info: SeqInfo,
		applied: usize,
	) -> Blocks<'data, S> {
		Spanned {
			value: self.blocks(nodes.value, info, applied),
			span: nodes.span,
		}
	}

	/// Rebuild a sequence of inline content, whose ancestors already apply the outermost `applied`
	/// ranges covering it, wrapping it in the rest.
	#[tracing::instrument(name = "rebuild_inlines", level = Level::TRACE, skip(self, seq, info))]
	fn inlines<'data, S: Span>(
		&mut self,
		seq: Vec<SpannedElement<'data, S>>,
		info: SeqInfo,
		applied: usize,
	) -> Vec<SpannedInline<'data, S>> {
		let mut items = Vec::with_capacity(seq.len());
		// the delimiters directly in this sequence, whose spans a node wrapped here takes in
		let mut delimiters: HashMap<RangeId, Vec<S>> = HashMap::new();
		for (piece, info) in seq.into_iter().zip(info) {
			if let Element::Delim(delim) = &piece.value {
				let matched = self.matches.of(delim);
				for &range in matched.opens.iter().chain(&matched.closes) {
					delimiters
						.entry(range)
						.or_default()
						.push(piece.span.clone());
				}
			}

			let around = self.around(info.wrap, applied);
			if let Some(inline) = self.inline(piece) {
				items.push((inline, around));
			}
		}

		wrap(items, self.ranges, self.base, &delimiters)
	}

	/// [`Self::inlines`] for the content of a container.
	fn inline_content<'data, S: Span>(
		&mut self,
		nodes: Elements<'data, S>,
		info: SeqInfo,
		applied: usize,
	) -> Inlines<'data, S> {
		Spanned {
			value: self.inlines(nodes.value, info, applied),
			span: nodes.span,
		}
	}

	/// Rebuild one piece of inline content. Leftover delimiters come back as text; [`None`] if a
	/// delimiter was spent entirely.
	fn inline<'data, S: Span>(
		&mut self,
		piece: SpannedElement<'data, S>,
	) -> Option<SpannedInline<'data, S>> {
		let Spanned { value, span } = piece;
		let value = match value {
			Element::Delim(delim) => {
				let leftover = self.matches.of(&delim).leftover;
				if leftover == 0 {
					return None;
				}
				Inline::Text(delim.ch.char().to_string().repeat(leftover).into())
			}
			Element::Emoji(emoji) => Inline::Emoji(emoji),
			Element::Timestamp(timestamp) => Inline::Timestamp(timestamp),
			Element::Mention(mention) => Inline::Mention(mention),
			// link text is a scope of its own
			Element::Link(link) => Inline::Link(resolve_link(link, self.allowed, self.ids)),
			Element::Code(code) => Inline::Code(code),
			Element::CodeBlock(code_block) => Inline::CodeBlock(code_block),
			Element::Text(text) => Inline::Text(text),
			Element::Heading(_)
			| Element::List(_)
			| Element::Paragraph(_)
			| Element::Quote(_)
			| Element::Small(_)
			| Element::Empty => {
				unreachable!("inline content is parsed with the inline rules alone")
			}
		};
		Some(Spanned { value, span })
	}
}

/// Wrap each run of `items` sharing their outermost range in that range's node. Each item lists
/// the ranges to wrap it in, innermost first.
///
/// A wrapping node spans its content and, of `delimiters` -- the spans of the delimiters beside
/// `items` -- its own. A spoiler's id is the one of `base`'s block for its range.
fn wrap<'data, S: Span>(
	items: Vec<(SpannedInline<'data, S>, Vec<RangeId>)>,
	ranges: &RangeTree,
	base: Id,
	delimiters: &HashMap<RangeId, Vec<S>>,
) -> Vec<SpannedInline<'data, S>> {
	let mut out = Vec::with_capacity(items.len());
	let mut items = items.into_iter().peekable();

	while let Some((node, mut apply)) = items.next() {
		let Some(range) = apply.pop() else {
			out.push(node);
			continue;
		};

		let mut run = vec![(node, apply)];
		while let Some((node, mut apply)) = items.next_if(|(_, apply)| apply.last() == Some(&range))
		{
			apply.pop();
			run.push((node, apply));
		}

		let content = wrap(run, ranges, base, delimiters);
		let mut content_span = content[0].span.clone();
		content_span.merge(&content[content.len() - 1].span);
		let mut span = content_span.clone();
		for delimiter in delimiters.get(&range).into_iter().flatten() {
			span.merge(delimiter);
		}
		let mut modifier = Inline::modifier(
			ranges[range].kind,
			Spanned {
				value: content,
				span: content_span,
			},
		);
		// every fragment of one range is one spoiler
		if let Inline::Spoiler(spoiler) = &mut modifier {
			spoiler.id = base.nth(range);
		}
		out.push(Spanned {
			value: modifier,
			span,
		});
	}

	out
}

/// Resolve link text on its own: the scope around it reads the link as one atom.
fn resolve_link<'data, S: Span>(
	link: Link<S, Element<'data, S>>,
	allowed: SyntaxSet,
	ids: &mut Ids,
) -> Link<S, Inline<'data, S>> {
	Link {
		text: link.text.map(|text| Spanned {
			value: resolve_inline(text.value, allowed, ids),
			span: text.span,
		}),
		url: link.url,
		title: link.title,
	}
}

/// Flatten every sequence, bottom up, merging the text that leftover delimiters split.
#[tracing::instrument(level = Level::TRACE, skip_all)]
fn flatten_blocks<S: Span>(blocks: &mut [SpannedBlock<'_, S>]) {
	for block in blocks {
		match &mut block.value {
			Block::Paragraph(content)
			| Block::Heading(Heading { content, .. })
			| Block::Small(Small { content }) => flatten(&mut content.value),
			Block::Quote(content) => flatten_blocks(&mut content.value),
			Block::List(list) => {
				for item in &mut list.items.value {
					flatten_blocks(&mut item.content.value);
				}
			}
			Block::Empty => {}
		}
	}
}

/// The passes before the rebuild: pair the delimiters in `nodes`, a scope holding `content`, and
/// decide where each range is wrapped.
///
/// # Errors
/// As [`resolve`].
fn place<S: Span>(
	nodes: &[SpannedElement<'_, S>],
	allowed: SyntaxSet,
	content: Content,
	unmatched: Unmatched,
) -> Result<(Matches, RangeTree, SeqInfo), Vec<Offset>> {
	// a token still pending at the end keeps the line ending it was created with
	let mut collect = Collect {
		tokens: Vec::new(),
		pending: 0,
		prev: Neighbor::LINE_END,
		leaves: 0,
	};
	collect.seq(nodes);
	let tokens = collect.tokens;
	let (matches, ranges) = pair(&tokens, allowed);

	if unmatched == Unmatched::Reject {
		let unmatched: Vec<Offset> = tokens
			.iter()
			.zip(matches.iter())
			.filter(|(token, matched)| {
				token.delim.before_block && matched.leftover == token.delim.len
			})
			.map(|(token, _)| token.delim.start)
			.collect();
		if !unmatched.is_empty() {
			return Err(unmatched);
		}
	}

	let mut place = Place {
		matches: &matches,
		ranges: &ranges,
		open: None,
	};
	let (_, info) = place.seq(nodes, content);
	Ok((matches, ranges, info))
}

/// Pair every [`Element::Delim`] in a parsed scope of blocks, like a message, and apply the
/// resulting ranges, producing the finished tree.
///
/// # Errors
/// With [`Unmatched::Reject`], the offsets of any openers that block syntax was recognized after
/// but that matched nothing. Their lines are paragraphs -- `__# a` is not a heading -- so the
/// caller must parse again with them disabled, as [`crate::parse`] does.
///
/// Spoilers take their ids from `ids`.
#[tracing::instrument(level = Level::TRACE, skip(nodes, ids), err(level = Level::TRACE, Debug))]
pub fn resolve<'data, S: Span>(
	nodes: Vec<SpannedElement<'data, S>>,
	allowed: SyntaxSet,
	unmatched: Unmatched,
	ids: &mut Ids,
) -> Result<Vec<SpannedBlock<'data, S>>, Vec<Offset>> {
	let (matches, ranges, info) = place(&nodes, allowed, Content::Blocks, unmatched)?;
	let mut blocks = Rebuild::new(&matches, &ranges, allowed, ids).blocks(nodes, info, 0);
	flatten_blocks(&mut blocks);
	Ok(blocks)
}

/// [`resolve`] for a scope of inline content, like link text. It holds no block syntax, so no
/// opener in it goes unmatched, and this cannot fail.
#[must_use]
pub fn resolve_inline<'data, S: Span>(
	nodes: Vec<SpannedElement<'data, S>>,
	allowed: SyntaxSet,
	ids: &mut Ids,
) -> Vec<SpannedInline<'data, S>> {
	let (matches, ranges, info) = place(&nodes, allowed, Content::Inline, Unmatched::Text)
		.unwrap_or_else(|_| unreachable!("only a rejecting resolve fails"));
	let mut inlines = Rebuild::new(&matches, &ranges, allowed, ids).inlines(nodes, info, 0);
	flatten(&mut inlines);
	inlines
}

#[cfg(test)]
mod test {
	use pretty_assertions::assert_eq;

	use crate::{
		bold, code_block, heading, italic, link, list, list_item, node::Block, paragraph,
		spanned_vec, spoiler, test_utils::parsed, text,
	};

	#[test]
	fn asterisks_close_after_whitespace() {
		assert_eq!(parsed("**foo **"), spanned_vec![paragraph!(bold!("foo "))]);
		assert_eq!(parsed("*foo *"), spanned_vec![paragraph!(italic!("foo "))]);
		assert_eq!(parsed("** foo**"), spanned_vec![paragraph!(bold!(" foo"))]);
		assert_eq!(parsed("1 * 2 * 3"), spanned_vec![paragraph!("1 * 2 * 3")]);
	}

	/// The `**` before `bar` could close the italic, but a bold that can close later wins.
	#[test]
	fn an_italic_yields_to_a_bold() {
		assert_eq!(
			parsed("*foo **bar** baz*"),
			spanned_vec![paragraph!(italic!(
				text!("foo "),
				bold!("bar"),
				text!(" baz")
			))]
		);
		assert_eq!(
			parsed("***foo***"),
			spanned_vec![paragraph!(bold!(italic!("foo")))]
		);
	}

	#[test]
	fn delimiters_can_be_the_content() {
		assert_eq!(parsed("*_*"), spanned_vec![paragraph!(italic!("_"))]);
		assert_eq!(parsed("*__*"), spanned_vec![paragraph!(italic!("__"))]);
		assert_eq!(parsed("**"), spanned_vec![paragraph!("**")]);
	}

	#[test]
	fn underscores_between_word_characters_are_text() {
		assert_eq!(
			parsed("snake_case_name"),
			spanned_vec![paragraph!("snake_case_name")]
		);
		assert_eq!(
			parsed("_foo_bar_"),
			spanned_vec![paragraph!(italic!("foo_bar"))]
		);
		assert_eq!(
			parsed("foo_bar baz_"),
			spanned_vec![paragraph!("foo_bar baz_")]
		);
		assert_eq!(
			parsed("Endemic_(epidemiology) and _really_"),
			spanned_vec![paragraph!(
				text!("Endemic_(epidemiology) and "),
				italic!("really")
			)]
		);
		// punctuation after an underscore lets it close
		assert_eq!(
			parsed("_foo_(bar)"),
			spanned_vec![paragraph!(italic!("foo"), text!("(bar)"))]
		);
	}

	#[test]
	fn spoilers_cannot_hold_spoilers() {
		assert_eq!(
			parsed("||a ||b|| c||"),
			spanned_vec![paragraph!(
				spoiler!(id = 0; "a "),
				text!("b"),
				spoiler!(id = 1; " c")
			)]
		);
	}

	/// Only link text bounds a range: code is crossed, and its delimiters are its own.
	#[test]
	fn ranges_cross_code_but_not_link_text() {
		assert_eq!(
			parsed("*a ```x*y``` b*"),
			spanned_vec![paragraph!(italic!(
				text!("a "),
				code_block!("x*y"),
				text!(" b")
			))]
		);
		assert_eq!(
			parsed("*a [b*](https://example.com/)"),
			spanned_vec![paragraph!(
				text!("*a "),
				link!("https://example.com/", [text!("b*")])
			)]
		);
	}

	/// An opener with nothing to close it does not get to start block syntax.
	#[test]
	fn an_unmatched_opener_leaves_block_syntax_alone() {
		assert_eq!(parsed("__# a"), spanned_vec![paragraph!("__# a")]);
		assert_eq!(
			parsed("*1. a\nb"),
			spanned_vec![paragraph!("*1. a"), paragraph!("b")]
		);
		// a closer after a line ending still closes, so this one is matched
		assert_eq!(
			parsed("*1. a\n*b"),
			spanned_vec![
				list!(1: [list_item!(paragraph!(italic!("a")))]),
				paragraph!("b")
			]
		);
	}

	/// A modifier never holds a block: it goes inside each block it covers.
	#[test]
	fn a_modifier_splits_into_the_blocks_it_covers() {
		assert_eq!(
			parsed("*1. foo\n2. bar*"),
			spanned_vec![list!(1: [
				list_item!(paragraph!(italic!("foo"))),
				list_item!(paragraph!(italic!("bar")))
			])]
		);
		assert_eq!(
			parsed("||1. foo\n2. bar||"),
			spanned_vec![list!(1: [
				list_item!(paragraph!(spoiler!(id = 0; "foo"))),
				list_item!(paragraph!(spoiler!(id = 0; "bar")))
			])]
		);
		// the blank line between paragraphs stays uncovered
		assert_eq!(
			parsed("||a\n\nb||"),
			spanned_vec![
				paragraph!(spoiler!(id = 0; "a")),
				Block::Empty,
				paragraph!(spoiler!(id = 0; "b"))
			]
		);
	}

	/// Split into blocks, nested modifiers keep their order.
	#[test]
	fn a_split_modifier_keeps_its_nesting() {
		assert_eq!(
			parsed("||**a\n- b**||"),
			spanned_vec![
				paragraph!(spoiler!(id = 1; bold!("a"))),
				list!(-[list_item!(paragraph!(spoiler!(id = 1; bold!("b"))))])
			]
		);
	}

	/// Leftover delimiters between blocks get a paragraph, with the modifier inside it.
	#[test]
	fn leftover_delimiters_among_blocks_are_wrapped_inside_their_paragraph() {
		assert_eq!(
			parsed("*a\n___\nb*"),
			spanned_vec![
				paragraph!(italic!("a")),
				paragraph!(italic!("___")),
				paragraph!(italic!("b"))
			]
		);
	}

	/// A spoiler ending partway through a list is split into its items, as fragments of one
	/// spoiler that share an id.
	#[test]
	fn a_split_spoiler_shares_its_id() {
		assert_eq!(
			parsed("||1. foo\n2. ba||r\n||c||"),
			spanned_vec![
				list!(1: [
					list_item!(paragraph!(spoiler!(id = 0; "foo"))),
					list_item![paragraph!(spoiler!(id = 0; "ba"), text!("r"))]
				]),
				paragraph!(spoiler!(id = 1; "c"))
			]
		);
	}

	/// A range covers whatever lies between its delimiters, whichever container it sits in.
	#[test]
	fn a_modifier_crosses_containers() {
		assert_eq!(
			parsed("||\n- a\n- b||"),
			spanned_vec![list!(-[
				list_item!(paragraph!(spoiler!("a"))),
				list_item!(paragraph!(spoiler!("b")))
			])]
		);
		assert_eq!(
			parsed("*a\n> b\n> c*"),
			spanned_vec![
				paragraph!(italic!("a")),
				Block::Quote(spanned_vec![
					paragraph!(italic!("b")),
					paragraph!(italic!("c"))
				])
			]
		);
		assert_eq!(
			parsed("> *- a\n> - b*"),
			spanned_vec![Block::Quote(spanned_vec![list!(-[
				list_item!(paragraph!(italic!("a"))),
				list_item!(paragraph!(italic!("b")))
			])])]
		);
		assert_eq!(
			parsed("*>>> a\nb*"),
			spanned_vec![Block::Quote(spanned_vec![
				paragraph!(italic!("a")),
				paragraph!(italic!("b"))
			])]
		);
		assert_eq!(
			parsed("**# h\nb**"),
			spanned_vec![heading!(1, [bold!("h")]), paragraph!(bold!("b"))]
		);
		assert_eq!(
			parsed("- *a\n- b*"),
			spanned_vec![list!(-[
				list_item!(paragraph!(italic!("a"))),
				list_item!(paragraph!(italic!("b")))
			])]
		);
	}

	/// A range ending partway through a block wraps only the part it covers.
	#[test]
	fn a_modifier_ending_mid_block_splits() {
		assert_eq!(
			parsed("*a\nb* c"),
			spanned_vec![
				paragraph!(italic!("a")),
				paragraph!(italic!("b"), text!(" c"))
			]
		);
	}

	/// The inline rules for a modifier's content hold when it spans blocks too.
	#[test]
	fn a_block_spanning_modifier_keeps_its_inline_rules() {
		assert_eq!(
			parsed("*foo **bar**\n- x*"),
			spanned_vec![
				paragraph!(italic!(text!("foo "), bold!("bar"))),
				list!(-[list_item!(paragraph!(italic!("x")))])
			]
		);
		assert_eq!(
			parsed("_foo_bar\n- x_"),
			spanned_vec![
				paragraph!(italic!("foo_bar")),
				list!(-[list_item!(paragraph!(italic!("x")))])
			]
		);
	}
}
