//! Modifiers as style ranges.
//!
//! Instead of parsing a modifier's content recursively, parsing records each run of modifier
//! delimiters as a [`Delim`] token and carries on. [`resolve`] then pairs the tokens across the whole
//! message with a delimiter stack, and applies each pair to the finished tree as a range: wrapping
//! whole nodes where the range covers them, and splitting at block boundaries where it does not.
//! Nothing about a modifier depends on where it sits relative to other rules.

pub mod delim;
pub mod pair;

use std::collections::HashMap;

use crate::{
	block::List,
	inline::link::Link,
	node::{
		Element, Id, Ids, Modifier, Node, ParsedNode, ParsedNodes, SpannedNode, SpannedNodes,
		SpannedParsedNode, flatten,
	},
	rule::RuleSet,
	span::{Span, Spanned},
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
	fn seq<S: Span>(&mut self, seq: &[SpannedParsedNode<'_, S>]) {
		for node in seq {
			match &node.value {
				ParsedNode::Delim(delim) => self.delim(*delim),
				ParsedNode::Element(element) => self.element(element),
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

	/// Move past `element`: through the sequences of a container, or over a leaf, which counts as
	/// one and reads as its first and last characters.
	fn element<S: Span>(&mut self, element: &Element<'_, S, ParsedNode<'_, S>>) {
		// A delimiter just before a block reads its first character, as `*` does in `*1. foo`;
		// one ending a block reads the line ending.
		if element.is_container() {
			for content in element.sequences() {
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
}

/// Where a range covering `piece` is wrapped, given whether it covers `siblings` of it too and
/// whether it `opens_here`, among them.
fn placement<S: Span>(piece: &ParsedNode<'_, S>, siblings: bool, opens_here: bool) -> Placement {
	match piece {
		_ if siblings || opens_here => Placement::Here,
		// split across several items, a spoiler around a whole list would be one spoiler per item
		ParsedNode::Element(Element::List(List { items, .. })) if items.len() != 1 => {
			Placement::Here
		}
		// so `# **foo**` stays a bold inside a heading
		ParsedNode::Element(element) if element.is_container() => Placement::Inside,
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
	/// Decide where every range covering a piece of `seq` is wrapped, and find how far into the
	/// ranges `seq` as a whole reaches.
	#[tracing::instrument(name = "place", level = Level::TRACE, skip_all)]
	fn seq<S: Span>(&mut self, seq: &[SpannedParsedNode<'_, S>]) -> (Option<Reach>, SeqInfo) {
		// the ranges whose opening delimiter the sequence holds
		let mut opens = Vec::new();
		let mut reach = None;
		let mut pieces = Vec::with_capacity(seq.len());
		for piece in seq {
			let (piece_reach, seqs) = self.piece(&piece.value, &mut opens);
			pieces.push((piece_reach.and_then(|reach| reach.cover(self.ranges)), seqs));
			reach = Reach::join(reach, piece_reach);
		}

		// how many pieces each range covers whole
		let mut covered: HashMap<RangeId, usize> = HashMap::new();
		for range in pieces
			.iter()
			.flat_map(|&(cover, _)| self.ranges.ancestors(cover))
		{
			*covered.entry(range).or_default() += 1;
		}

		let info = seq
			.iter()
			.zip(pieces)
			.map(|(piece, (cover, seqs))| PieceInfo {
				// once a range goes inside a piece, every range within it does too, so the ranges
				// wrapped around a piece are the outermost of those covering it
				wrap: self.ranges.ancestors(cover).find(|&range| {
					placement(&piece.value, covered[&range] >= 2, opens.contains(&range))
						== Placement::Here
				}),
				seqs,
			})
			.collect();
		(reach, info)
	}

	/// Walk past `node`, tracking which range is open: the reach of its leaves, and what is decided
	/// for the sequences inside it. A delimiter adds the ranges it opens to `opens`.
	fn piece<S: Span>(
		&mut self,
		node: &ParsedNode<'_, S>,
		opens: &mut Vec<RangeId>,
	) -> (Option<Reach>, Vec<SeqInfo>) {
		match node {
			ParsedNode::Delim(delim) => {
				let matched = self.matches.of(delim);
				if let Some(&outer) = matched.closes.last() {
					self.open = self.ranges[outer].parent;
				}
				// leftover characters are a leaf, between what it closes and what it opens
				let reach = (matched.leftover > 0).then_some(Reach::leaf(self.open));
				if let Some(&inner) = matched.opens.last() {
					self.open = Some(inner);
				}
				opens.extend(&matched.opens);
				(reach, Vec::new())
			}
			ParsedNode::Element(element) if element.is_container() => {
				let mut reach = None;
				let mut seqs = Vec::new();
				for content in element.sequences() {
					let (content_reach, info) = self.seq(content);
					reach = Reach::join(reach, content_reach);
					seqs.push(info);
				}
				(reach, seqs)
			}
			ParsedNode::Element(_) => (Some(Reach::leaf(self.open)), Vec::new()),
		}
	}
}

/// The last pass: rebuild the tree with every range applied.
struct Rebuild<'a> {
	matches: &'a Matches,
	ranges: &'a RangeTree,
	allowed: RuleSet,
	/// The id of range zero; range `n` has its `n`th.
	base: Id,
	/// The ids of the parse, for the link text resolved inside this scope.
	ids: &'a mut Ids,
}

impl Rebuild<'_> {
	/// Rebuild `seq`, whose ancestors already apply the outermost `applied` ranges covering it.
	#[tracing::instrument(name = "rebuild", level = Level::TRACE, skip(self, seq, info))]
	fn seq<'data, S: Span>(
		&mut self,
		seq: Vec<SpannedParsedNode<'data, S>>,
		info: SeqInfo,
		applied: usize,
		content: Content,
	) -> Vec<SpannedNode<'data, S>> {
		let mut items = Vec::with_capacity(seq.len());
		// the delimiters directly in this sequence, whose spans a node wrapped here takes in
		let mut delimiters: HashMap<RangeId, Vec<S>> = HashMap::new();
		for (piece, info) in seq.into_iter().zip(info) {
			if let ParsedNode::Delim(delim) = &piece.value {
				let matched = self.matches.of(delim);
				for &range in matched.opens.iter().chain(&matched.closes) {
					delimiters
						.entry(range)
						.or_default()
						.push(piece.span.clone());
				}
			}

			// wrapped around it here, innermost first, less what an ancestor already applies
			let wrap: Vec<RangeId> = self
				.ranges
				.ancestors(info.wrap)
				.take_while(|&range| self.ranges[range].depth > applied)
				.collect();
			if let Some(node) = self.piece(piece, info.seqs, applied + wrap.len(), content) {
				items.push((node, wrap));
			}
		}

		wrap(items, self.ranges, self.base, &delimiters)
	}

	/// [`Self::seq`] for the content of a container.
	fn content<'data, S: Span>(
		&mut self,
		nodes: ParsedNodes<'data, S>,
		info: SeqInfo,
		applied: usize,
		content: Content,
	) -> SpannedNodes<'data, S> {
		Spanned {
			value: self.seq(nodes.value, info, applied, content),
			span: nodes.span,
		}
	}

	/// Rebuild `piece`, given what [`Place`] decided for its sequences.
	fn piece<'data, S: Span>(
		&mut self,
		piece: SpannedParsedNode<'data, S>,
		seqs: Vec<SeqInfo>,
		applied: usize,
		content: Content,
	) -> Option<SpannedNode<'data, S>> {
		let Spanned { value, span } = piece;
		let value = match value {
			ParsedNode::Delim(delim) => {
				let leftover = self.matches.of(&delim).leftover;
				if leftover == 0 {
					return None;
				}
				let text = Node::Element(Element::Text(
					delim.ch.char().to_string().repeat(leftover).into(),
				));
				// leftover delimiters are text, and text cannot sit among blocks
				if content == Content::Blocks {
					Node::Element(Element::Paragraph(Spanned {
						value: vec![Spanned {
							value: text,
							span: span.clone(),
						}],
						span: span.clone(),
					}))
				} else {
					text
				}
			}
			ParsedNode::Element(element) => Node::Element(self.element(element, seqs, applied)?),
		};
		Some(Spanned { value, span })
	}

	/// Rebuild the sequences of `element`, given what [`Place`] decided for each. [`None`] for a
	/// paragraph left with nothing in it.
	fn element<'data, S: Span>(
		&mut self,
		element: Element<'data, S, ParsedNode<'data, S>>,
		seqs: Vec<SeqInfo>,
		applied: usize,
	) -> Option<Element<'data, S, Node<'data, S>>> {
		let mut seqs = seqs.into_iter();
		let element = match element {
			// link text is a scope of its own
			Element::Link(link) => Element::Link(resolve_link(link, self.allowed, self.ids)),
			// `map_children` visits the same sequences as `sequences`, in the same order
			element => element.map_children(|nodes, content| {
				let info = seqs.next().expect("placed");
				self.content(nodes, info, applied, content)
			}),
		};
		// nothing but delimiters, all of which were spent
		if let Element::Paragraph(content) = &element
			&& content.value.is_empty()
		{
			return None;
		}
		Some(element)
	}
}

/// Wrap each run of `items` sharing their outermost range in that range's node. Each item lists
/// the ranges to wrap it in, innermost first.
///
/// A wrapping node spans its content and, of `delimiters` -- the spans of the delimiters beside
/// `items` -- its own. A spoiler's id is the one of `base`'s block for its range.
fn wrap<'data, S: Span>(
	items: Vec<(SpannedNode<'data, S>, Vec<RangeId>)>,
	ranges: &RangeTree,
	base: Id,
	delimiters: &HashMap<RangeId, Vec<S>>,
) -> Vec<SpannedNode<'data, S>> {
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
		let mut modifier = Modifier::new(
			ranges[range].kind,
			Spanned {
				value: content,
				span: content_span,
			},
		);
		// every fragment of one range is one spoiler
		if let Modifier::Spoiler(spoiler) = &mut modifier {
			spoiler.id = base.nth(range);
		}
		out.push(Spanned {
			value: Node::Modifier(modifier),
			span,
		});
	}

	out
}

/// Resolve link text on its own: the scope around it reads the link as one atom.
fn resolve_link<'data, S: Span>(
	link: Link<S, ParsedNode<'data, S>>,
	allowed: RuleSet,
	ids: &mut Ids,
) -> Link<S, Node<'data, S>> {
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
fn flatten_all<S: Span>(nodes: &mut Vec<SpannedNode<'_, S>>) {
	for node in nodes.iter_mut() {
		match &mut node.value {
			Node::Modifier(modifier) => flatten_all(&mut modifier.content_mut().value),
			Node::Element(element) => {
				for content in element.sequences_mut() {
					flatten_all(&mut content.value);
				}
			}
		}
	}
	flatten(nodes);
}

/// Pair every [`ParsedNode::Delim`] in a parsed tree and apply the resulting ranges, producing the
/// finished tree.
///
/// # Errors
/// With [`Unmatched::Reject`], the offsets of any openers that block syntax was recognized after
/// but that matched nothing. Their lines are paragraphs -- `__# a` is not a heading -- so the
/// caller must parse again with them disabled, as [`crate::parse`] does.
///
/// Spoilers take their ids from `ids`.
#[tracing::instrument(level = Level::TRACE, skip(nodes, ids), err(level = Level::TRACE, Debug))]
pub fn resolve<'data, S: Span>(
	nodes: Vec<SpannedParsedNode<'data, S>>,
	allowed: RuleSet,
	content: Content,
	unmatched: Unmatched,
	ids: &mut Ids,
) -> Result<Vec<SpannedNode<'data, S>>, Vec<Offset>> {
	// a token still pending at the end keeps the line ending it was created with
	let mut collect = Collect {
		tokens: Vec::new(),
		pending: 0,
		prev: Neighbor::LINE_END,
		leaves: 0,
	};
	collect.seq(&nodes);
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
	let (_, info) = place.seq(&nodes);

	// claimed before rebuilding, so link text resolved along the way takes ids after these
	let base = ids.reserve(ranges.len());
	let mut rebuild = Rebuild {
		matches: &matches,
		ranges: &ranges,
		allowed,
		base,
		ids,
	};
	let mut nodes = rebuild.seq(nodes, info, 0, content);

	flatten_all(&mut nodes);
	Ok(nodes)
}

/// Resolve a scope of inline content, like link text. It holds no block syntax, so no opener in
/// it goes unmatched, and this cannot fail.
#[must_use]
pub fn resolve_inline<'data, S: Span>(
	nodes: Vec<SpannedParsedNode<'data, S>>,
	allowed: RuleSet,
	ids: &mut Ids,
) -> Vec<SpannedNode<'data, S>> {
	resolve(nodes, allowed, Content::Inline, Unmatched::Text, ids)
		.unwrap_or_else(|_| unreachable!("only a rejecting resolve fails"))
}

#[cfg(test)]
mod test {
	use pretty_assertions::assert_eq;

	use crate::{
		bold, code_block, heading, italic, link, list, list_item,
		node::{Element, Node},
		paragraph, spanned_vec, spoiler,
		test_utils::parsed,
		text,
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
			spanned_vec![italic!(list!(1: [list_item!("a")])), paragraph!("b")]
		);
	}

	#[test]
	fn a_modifier_wraps_the_blocks_it_covers() {
		assert_eq!(
			parsed("*1. foo\n2. bar*"),
			spanned_vec![italic!(list!(1: [list_item!("foo"), list_item!("bar")]))]
		);
		assert_eq!(
			parsed("||1. foo\n2. bar||"),
			spanned_vec![spoiler!(id = 0; list!(1: [list_item!("foo"), list_item!("bar")]))]
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

	/// A range wraps whatever blocks lie between its delimiters, whichever container they sit in.
	#[test]
	fn a_modifier_crosses_containers() {
		assert_eq!(
			parsed("||\n- a\n- b||"),
			spanned_vec![spoiler!(list!(-[list_item!("a"), list_item!("b")]))]
		);
		assert_eq!(
			parsed("*a\n> b\n> c*"),
			spanned_vec![italic!(
				paragraph!("a"),
				Node::Element(Element::Quote(spanned_vec![
					paragraph!("b"),
					paragraph!("c")
				]))
			)]
		);
		assert_eq!(
			parsed("> *- a\n> - b*"),
			spanned_vec![Node::Element(Element::Quote(spanned_vec![italic!(list!(
				-[list_item!("a"), list_item!("b")]
			))]))]
		);
		assert_eq!(
			parsed("*>>> a\nb*"),
			spanned_vec![italic!(Node::Element(Element::Quote(spanned_vec![
				paragraph!("a"),
				paragraph!("b")
			])))]
		);
		assert_eq!(
			parsed("**# h\nb**"),
			spanned_vec![bold!(heading!(1, "h"), paragraph!("b"))]
		);
		assert_eq!(
			parsed("- *a\n- b*"),
			spanned_vec![italic!(list!(-[list_item!("a"), list_item!("b")]))]
		);
	}

	/// A range ending partway through a block covers what it can whole, and the rest in place.
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
			spanned_vec![italic!(
				paragraph!(text!("foo "), bold!("bar")),
				list!(-[list_item!("x")])
			)]
		);
		assert_eq!(
			parsed("_foo_bar\n- x_"),
			spanned_vec![italic!(paragraph!("foo_bar"), list!(-[list_item!("x")]))]
		);
	}
}
