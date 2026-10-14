//! Pairing delimiter runs into ranges.

use super::delim::{Delim, DelimCharStruct, Flanking, Neighbor, Offset, SpoilerState};
use crate::{node::modifier::ModifierKind, rule::RuleSet};
use tracing::Level;

pub type RangeId = usize;

#[derive(Debug, Clone, Copy)]
pub struct RangeInfo {
	pub kind: ModifierKind,
	/// The tokens it opens and closes at.
	pub tokens: (usize, usize),
	/// How many characters it spends at each end.
	pub chars: usize,
	/// The innermost range around it; set by [`nest`].
	pub parent: Option<RangeId>,
	/// How many ranges it is inside, itself included; set by [`nest`].
	pub depth: usize,
}

/// Every range of a scope, which nest as a tree.
#[derive(Debug, Default)]
pub struct RangeTree(Vec<RangeInfo>);

impl RangeTree {
	#[must_use]
	pub fn len(&self) -> usize {
		self.0.len()
	}

	#[must_use]
	pub fn is_empty(&self) -> bool {
		self.0.is_empty()
	}

	/// How many ranges `range` is inside, itself included; zero for none.
	#[must_use]
	pub fn depth(&self, range: Option<RangeId>) -> usize {
		range.map_or(0, |range| self[range].depth)
	}

	#[must_use]
	pub fn parent(&self, range: Option<RangeId>) -> Option<RangeId> {
		range.and_then(|range| self[range].parent)
	}

	/// `range` and the ranges around it, innermost first.
	pub fn ancestors(&self, range: Option<RangeId>) -> impl Iterator<Item = RangeId> {
		std::iter::successors(range, |&range| self[range].parent)
	}

	/// The innermost range around both `a` and `b`.
	#[must_use]
	pub fn common(&self, mut a: Option<RangeId>, mut b: Option<RangeId>) -> Option<RangeId> {
		while a != b {
			if self.depth(a) >= self.depth(b) {
				a = self.parent(a);
			} else {
				b = self.parent(b);
			}
		}
		a
	}
}

impl std::ops::Index<RangeId> for RangeTree {
	type Output = RangeInfo;

	fn index(&self, range: RangeId) -> &RangeInfo {
		&self.0[range]
	}
}

/// What became of one [`Delim`] once matched: the ranges it closes and opens, in document order,
/// and the characters left over, which sit between the two and are text.
#[derive(Debug, Default)]
pub struct Matched {
	pub closes: Vec<RangeId>,
	pub opens: Vec<RangeId>,
	pub leftover: usize,
}

/// What became of each delimiter of a scope.
#[derive(Debug)]
pub struct Matches {
	/// Where each delimiter starts, in document order.
	starts: Vec<Offset>,
	matched: Vec<Matched>,
}

impl Matches {
	/// What became of `delim`.
	///
	/// # Panics
	/// If `delim` is not one of those paired.
	#[must_use]
	pub fn of(&self, delim: &Delim) -> &Matched {
		let index = self
			.starts
			.binary_search(&delim.start)
			.expect("a delimiter of this scope");
		&self.matched[index]
	}

	/// What became of each delimiter, in document order.
	pub fn iter(&self) -> impl Iterator<Item = &Matched> {
		self.matched.iter()
	}
}

/// How deeply ranges can nest. Deeper ones are left as text: every pass over the rebuilt tree
/// recurses through them, and nothing written by hand nests anywhere near this far.
pub const MAX_RANGE_DEPTH: usize = 32;

/// A delimiter with the characters around it, which decide whether it can open or close.
#[derive(Debug)]
pub struct Token {
	pub delim: Delim,
	pub prev: Neighbor,
	pub next: Neighbor,
	/// How many leaves come before it, so that a pair with nothing between them can be refused.
	pub leaves: usize,
}

impl Token {
	fn flanking(&self, spoiler: SpoilerState) -> Flanking {
		self.delim
			.ch
			.flanking(self.delim.len, self.prev, self.next, spoiler)
	}
}

/// The second pass: pair delimiters with a stack, as the `CommonMark` emphasis algorithm does.
#[must_use]
#[tracing::instrument(level = Level::TRACE, skip_all, fields(tokens = tokens.len(), ranges))]
pub fn pair(tokens: &[Token], allowed: RuleSet) -> (Matches, RangeTree) {
	#[derive(Clone, Copy)]
	struct Opener {
		token: usize,
		remaining: usize,
	}

	let mut matched: Vec<Matched> = tokens.iter().map(|_| Matched::default()).collect();
	let mut ranges: Vec<RangeInfo> = Vec::new();
	// each character's openers, latest last, so a closer finds its opener without a search. A
	// search that refused a pair and left the openers alone would repeat for every closer.
	let mut openers = DelimCharStruct::<Vec<Opener>>::default();

	// the longest run of the same character after each token that could close, for the rules below
	let mut closer_after = vec![0; tokens.len()];
	let mut longest = DelimCharStruct::<usize>::default();
	for (index, token) in tokens.iter().enumerate().rev() {
		let ch = token.delim.ch;
		closer_after[index] = *longest.get(&ch);
		if token.flanking(SpoilerState::Closed).closes {
			let longest = longest.get_mut(&ch);
			*longest = (*longest).max(token.delim.len);
		}
	}

	for (index, token) in tokens.iter().enumerate() {
		let Delim { ch, len, .. } = token.delim;
		let spoiler = if openers.pipe.is_empty() {
			SpoilerState::Closed
		} else {
			SpoilerState::Open
		};
		let flanking = token.flanking(spoiler);
		let mut remaining = len;

		while flanking.closes && remaining > 0 {
			let Some(&opener) = openers.get(&ch).last() else {
				break;
			};
			// A range must hold something -- some text, or a delimiter that will be -- or its
			// delimiters would vanish.
			if index == opener.token + 1 && tokens[opener.token].leaves == token.leaves {
				break;
			}
			if flanking.opens && ch.opens_instead(remaining, opener.remaining, closer_after[index])
			{
				break;
			}
			let Some(kind) = ch.spend(remaining, opener.remaining, allowed) else {
				break;
			};
			let used = kind.delimiter_len();
			// whatever opened since can no longer close here, and stays text
			for (_, stack) in openers.iter_variants_mut() {
				while stack.last().is_some_and(|other| other.token > opener.token) {
					stack.pop();
				}
			}

			// Another pair between the same two runs, like the outer bold of `****x****`, would
			// only nest a node inside one of its own kind. Leave the rest of the runs as text.
			let previous = matched[index].closes.last().copied();
			if previous.is_some_and(|id| {
				ranges[id].tokens == (opener.token, index) && ranges[id].kind == kind
			}) {
				break;
			}
			let id = ranges.len();
			ranges.push(RangeInfo {
				kind,
				tokens: (opener.token, index),
				chars: used,
				parent: None,
				depth: 0,
			});
			// an opener's innermost range is matched first and sits nearest its content
			matched[opener.token].opens.insert(0, id);
			matched[index].closes.push(id);

			let stack = openers.get_mut(&ch);
			stack.pop();
			if opener.remaining > used {
				stack.push(Opener {
					remaining: opener.remaining - used,
					..opener
				});
			}
			remaining -= used;
		}

		if flanking.opens && remaining > 0 {
			openers.get_mut(&ch).push(Opener {
				token: index,
				remaining,
			});
		}
	}

	nest(&mut matched, &mut ranges);

	for (token, matched) in tokens.iter().zip(&mut matched) {
		let used: usize = matched
			.closes
			.iter()
			.chain(&matched.opens)
			.map(|&id| ranges[id].chars)
			.sum();
		matched.leftover = token.delim.len - used;
	}

	tracing::Span::current().record("ranges", ranges.len());
	let starts: Vec<Offset> = tokens.iter().map(|token| token.delim.start).collect();
	debug_assert!(
		starts.is_sorted_by(|a, b| a < b),
		"tokens are in document order"
	);
	(Matches { starts, matched }, RangeTree(ranges))
}

/// Record how the ranges nest, and leave every range nested deeper than [`MAX_RANGE_DEPTH`] as
/// text. Ranges are well nested, so whatever such a range encloses is deeper still, and goes with
/// it.
fn nest(matched: &mut [Matched], ranges: &mut [RangeInfo]) {
	let mut open: Option<RangeId> = None;
	for matched in matched.iter() {
		for &id in &matched.closes {
			debug_assert_eq!(open, Some(id), "ranges are well nested");
			open = ranges[id].parent;
		}
		for &id in &matched.opens {
			ranges[id].parent = open;
			ranges[id].depth = open.map_or(0, |parent| ranges[parent].depth) + 1;
			open = Some(id);
		}
	}

	if ranges.iter().any(|range| range.depth > MAX_RANGE_DEPTH) {
		let kept = |id: &RangeId| ranges[*id].depth <= MAX_RANGE_DEPTH;
		for matched in matched {
			matched.closes.retain(kept);
			matched.opens.retain(kept);
		}
	}
}
