use std::{cell::Cell, fmt::Debug, marker::PhantomData, rc::Rc};

use nom::Parser;
use rule_set::ContextualRules;
use start_sequence::StartSequence;
pub use terminal_sequence::TerminalOutput;
use terminal_sequence::TerminalSequence;

use crate::{
	context::overrides::Overrides,
	context::{line_prefix::LinePrefix, matched_pairs::MatchedPairsParser},
	error::ParseError,
	grammar::{ByteHint, Grammar, GrammarStruct, OVERRIDE_START_GRAMMARS},
};

use super::{
	grammar::GrammarSet,
	node::Node,
	rule::{RuleSet, BLOCK_RULES, INLINE_RULES},
	span::Span,
	Input,
};

#[cfg(doc)]
use super::rule::Rule;

mod line_prefix;
mod matched_pairs;
mod overrides;
mod rule;
mod rule_set;
mod start_sequence;
mod terminal_sequence;

/// Per-grammar precheck hints stored in [`Context`].
///
/// Each field corresponds to a grammar whose inner parser would do O(N) work before
/// failing on adversarial input. Hints are computed once per top-level
/// [`crate::inline::inline`] call and propagated to all child contexts via
/// [`Context::with_grammar`].
///
/// NOTE: as this struct has a field for each grammar, it is very large.
// TODO: we can probably optimize the size of this struct by only building it for grammars that need byte hints.
pub type GrammarHints = GrammarStruct<ByteHint>;

impl GrammarHints {
	/// Returns `true` if any tracked hint is still `Unknown` and needs to be computed.
	fn any_unknown(&self) -> bool {
		self.iter().any(|hint| *hint == ByteHint::Unknown)
	}

	/// Clone self with hints derived from the given `grammars`.
	///
	/// Calculated by running `input` through [`Grammar::precheck_hint`] for each grammar in the set.
	#[must_use]
	pub fn for_grammars(&self, grammars: GrammarSet, input: &Input) -> Self {
		let mut new = self.clone();

		for (grammar, hint) in new.iter_variants_mut() {
			if *hint == ByteHint::Unknown {
				*hint = if grammars.contains(grammar) {
					grammar.precheck_hint(input)
				} else {
					ByteHint::NotApplicable
				};
			}
		}

		new
	}
}

/// The amount of fuel [`Options::default`] gives a parse.
///
/// Sized so that content a user can plausibly send finishes with a wide margin, while a
/// pathological input still terminates. Two measurements set it, taken against a release build:
///
/// - Real messages are nowhere near it. The announcement posts in `test_content` need 5–51 fuel;
///   ordinary prose costs well under 1 fuel per 100 bytes, because a run of plain text is a single
///   inline parse no matter how long it is.
/// - Adversarial input is what costs. The most expensive 4000-character inputs the timeout tests
///   know about — long runs of `__`/`**` delimiters that each open a rule the parser must abandon
///   — burn about 32k, or 2 fuel per byte. That is the realistic worst case for a Discord message,
///   whose limit is 4000 characters, and this default is ~15x above it.
///
/// The effect is to cap a pathological parse at roughly 100ms rather than letting it run
/// unbounded. A caller parsing only message-length content can safely tighten this a long way; see
/// [`Options::fuel`] for what moving it in either direction costs.
pub const DEFAULT_FUEL: u32 = 500_000;

#[derive(Debug, Clone, Copy)]
pub struct Options {
	pub allowed_rules: RuleSet,
	/// How much work the parse is allowed to do before it gives up with
	/// [`crate::error::OutOfFuel`].
	///
	/// One unit of fuel buys one invocation of the inline parser. That is the parser's unit of
	/// backtracking, so the count includes every attempt that a rule later abandons — which is
	/// exactly where pathological input spends its time. Fuel is a single tank shared by the whole
	/// parse, not a per-rule or per-nesting-level allowance, so it bounds total work rather than
	/// depth.
	///
	/// Fuel consumption tracks the parser's running time, but it is not a wall-clock budget. A unit
	/// costs on the order of a quarter of a microsecond on inline-heavy input in a release build,
	/// but a single invocation's cost varies with the input, block-level work is not metered at
	/// all, and rule changes move both. Treat a fuel figure as a bound on work, and re-measure
	/// after changing the parser rather than assuming it still buys the same number of
	/// milliseconds.
	///
	/// Raising this lets more (or more adversarial) content parse, at the cost of a higher
	/// worst-case time and allocation count per parse. Lowering it caps that worst case more
	/// tightly, at the risk of rejecting legitimate content — a parse that runs dry fails outright
	/// with [`crate::error::OutOfFuel`] and returns no partial AST, so a limit set too low is a
	/// correctness bug, not a graceful degradation. Callers running untrusted content under a
	/// latency budget should pick a value by measuring their own corpus and leaving generous
	/// headroom; [`DEFAULT_FUEL`] is that measurement done against Discord's 4000-character
	/// message limit.
	pub fuel: u32,
}

impl Default for Options {
	fn default() -> Self {
		Self {
			allowed_rules: RuleSet::all(),
			fuel: DEFAULT_FUEL,
		}
	}
}

/// An inline parse context which controls how child rules handle child and terminal content.
///
/// As we descend the parse tree, context accumulates allowed and disabled rules and global
/// terminals based on the each [`Grammar`]. This is essential for 2 purposes:
///
/// 1. Parent rules can control what rules are enabled as their children.
/// 2. Parent grammars can get terminated rather than beginning a new node.
///
/// As context descends, each [`Grammar::disabled_rules`] is subtracted from the parent
/// [`Context::allowed_rules`]. This ensures that allowed rules only becomes more restrictive.
///
/// Each grammar is accumulated in a [`GrammarSet`] which parses the
/// [`Grammar::terminal_sequence`] and [`Grammar::global_terminal_sequence`] in
/// [`Context::guard_terminal_sequence`].
#[derive(Debug, Clone)]
pub struct Context {
	/// The current grammar being parsed.
	pub grammar: Grammar,
	/// Rules allowed in this grammar, derived from all higher contexts.
	pub allowed_rules: RuleSet,
	/// The grammars [`Self::allowed_rules`] can reach, cached because it is derived once per
	/// context but consulted once per character. See [`Self::allowed_grammars`].
	allowed_grammars: GrammarSet,
	// This struct is huge so we reference count it to keep it off the stack and reduce allocations
	pub hints: Rc<GrammarHints>,
	/// Fuel remaining in this parse, drawn down by [`Context::consume_fuel`]. Shared by every
	/// context descended from the same [`Context::new`] call — including the ones
	/// [`Context::fresh`] hands out — so that the budget covers the parse as a whole rather than
	/// resetting per rule. A parse is single-threaded, so a `Cell` is sufficient.
	fuel: Rc<Cell<u32>>,
	/// The depth of the innermost enclosing list, used to implement a cap to list depth. This is
	/// 1-indexed for lists — an unnested list is at depth 1 — and is 0 when not inside a list at
	/// all.
	///
	/// This is a `u8` because the maximum is [`crate::block::list::MAX_DEPTH`].
	pub list_depth: u8,
	parents: GrammarSet,
}

/// The grammars `rules` can reach. Derived once per [`Context`] rather than per call; see
/// [`Context::allowed_grammars`].
fn grammars_for(rules: RuleSet) -> GrammarSet {
	rules.iter().flat_map(|rule| rule.grammar()).collect()
}

impl Context {
	/// Create a new context from the specified rule.
	#[must_use]
	pub fn new(options: Options) -> Self {
		Self {
			grammar: Grammar::None,
			allowed_rules: options.allowed_rules,
			allowed_grammars: grammars_for(options.allowed_rules),
			hints: Rc::new(GrammarHints::default()),
			fuel: Rc::new(Cell::new(options.fuel)),
			list_depth: 0,
			parents: GrammarSet::new(),
		}
	}

	/// Spend a unit of fuel, returning `false` if the tank is empty.
	///
	/// Called once per inline parse; see [`Options::fuel`].
	#[must_use]
	pub fn consume_fuel(&self) -> bool {
		match self.fuel.get() {
			0 => false,
			remaining => {
				self.fuel.set(remaining - 1);
				true
			}
		}
	}

	/// Fuel left in this parse.
	///
	/// This is how a caller measures what its own corpus costs, which is what picking a value for
	/// [`Options::fuel`] rests on. [`crate::parse`] builds its context internally, so measuring
	/// means driving the parser directly and keeping a handle on the context — every context
	/// derived from it draws down the same tank, so the one here still reflects the whole parse
	/// when it finishes:
	///
	/// ```
	/// # use discord_markdown::{block, context::{Context, Options}, node::SpannedNodes};
	/// # use nom::{combinator::all_consuming, Finish, Parser};
	/// let options = Options::default();
	/// let context = Context::new(options);
	///
	/// let result = all_consuming(block::block::<(), nom::error::Error<_>>(context.clone()))
	///     .parse_complete("**hello** world".into())
	///     .finish();
	///
	/// assert!(result.is_ok());
	/// println!("used {} fuel", options.fuel - context.remaining_fuel());
	/// ```
	#[must_use]
	pub fn remaining_fuel(&self) -> u32 {
		self.fuel.get()
	}

	/// Create a new context with a deeper list level.
	#[must_use]
	pub fn with_deeper_list(&self) -> Context {
		Context {
			list_depth: self.list_depth + 1,
			..self.clone()
		}
	}

	/// Create a new context by merging this context with another grammar. This will subtract the
	/// [`Grammar::disabled_rules`] from the current allowed rules.
	#[must_use]
	pub fn with_grammar(self, grammar: Grammar) -> Context {
		let disabled = grammar.disabled_rules();

		// Only a handful of grammars disable anything, and this is on the hot path for every rule
		// descent -- so keep the cached grammar set as-is unless the rules actually changed.
		if disabled.is_empty() {
			return Context {
				grammar,
				parents: self.parents | self.grammar,
				..self
			};
		}

		let allowed_rules = self.allowed_rules - disabled;

		Context {
			grammar,
			allowed_rules,
			allowed_grammars: grammars_for(allowed_rules),
			parents: self.parents | self.grammar,
			..self
		}
	}

	#[must_use]
	pub fn with_hints(&self, input: &Input) -> Self {
		if !self.hints.any_unknown() {
			return self.clone();
		}

		let hints = self.hints.for_grammars(self.allowed_grammars, input);

		Self {
			hints: Rc::new(hints),
			..self.clone()
		}
	}

	/// Create a fresh grammar with the same allowed rules but reset all grammar state.
	#[must_use]
	pub fn fresh(&self) -> Self {
		Self {
			grammar: Grammar::None,
			allowed_rules: self.allowed_rules,
			allowed_grammars: self.allowed_grammars,
			hints: Rc::new(GrammarHints::default()),
			fuel: Rc::clone(&self.fuel),
			list_depth: 0,
			parents: GrammarSet::new(),
		}
	}

	/// Get allowed inline rules in the current context.
	#[must_use]
	pub fn allowed_inline_rules<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Node<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualRules::<S, E>::from_context(self, self.allowed_rules & INLINE_RULES)
	}

	/// Get allowed block rules in the current context.
	#[must_use]
	pub fn allowed_block_rules<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Node<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualRules::from_context(self, self.allowed_rules & BLOCK_RULES)
	}

	/// Get allowed start sequences for the current context. This is based on [`Self::allowed_rules`]:
	/// for example, if [`Rule::Bold`] is in this set, then this will match its start sequence (`**`).
	#[must_use]
	pub fn allowed_start_sequences<'ctx, 'data, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data> + 'ctx,
	{
		StartSequence(self.allowed_grammars, PhantomData)
	}

	/// Sequences that contain what would otherwise be a delimiter -- a start sequence or this
	/// grammar's terminal -- but which should be consumed as literal text instead.
	///
	/// Both kinds share a branch because the caller treats them identically: whichever matched, the
	/// result is text.
	#[must_use]
	pub fn overrides<'ctx, 'data, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E> + 'ctx
	where
		E: ParseError<'data> + 'ctx,
	{
		let allowed = self.allowed_grammars & OVERRIDE_START_GRAMMARS;

		Overrides {
			grammar: self.grammar,
			start: allowed,
			error: PhantomData,
		}
	}

	/// Check whether we are in a terminal sequence; if not, apply the `normal` parser. Returns the
	/// output of whichever override matched -- [`Grammar::override_terminal_sequence`] or
	/// [`Self::override_start_sequences`] -- or of `normal`. Fails if a terminal sequence is
	/// encountered.
	pub fn guard_terminal_sequence<'ctx, 'data, O, E, P>(
		&'ctx self,
		normal: impl Fn() -> P + 'ctx,
	) -> impl Parser<Input<'data>, Output = TerminalOutput<'data, O>, Error = E> + 'ctx
	where
		E: ParseError<'data> + 'ctx,
		P: Parser<Input<'data>, Output = O, Error = E> + 'ctx,
		O: Debug,
	{
		TerminalSequence {
			context: self,
			normal,
			error: PhantomData,
		}
	}

	#[must_use]
	pub fn matched_pairs<'data, E>(
		&self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		MatchedPairsParser {
			grammars: self.grammars(),
			error: PhantomData,
		}
	}

	/// The line prefix required at the start of each line in this context, e.g. `> ` inside a
	/// quote. Matches the empty string when there is no enclosing container, so it can be applied
	/// unconditionally at the start of every line.
	#[must_use]
	pub fn line_prefix<'data, E>(
		&self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		LinePrefix {
			grammars: self.grammars(),
			error: PhantomData,
		}
	}

	#[must_use]
	pub fn grammars(&self) -> GrammarSet {
		self.parents | self.grammar
	}

	/// The grammars [`Self::allowed_rules`] can reach — the ones whose start sequences
	/// [`Self::allowed_start_sequences`] will match here.
	#[must_use]
	pub fn allowed_grammars(&self) -> GrammarSet {
		self.allowed_grammars
	}
}

impl Default for Context {
	fn default() -> Self {
		Self::new(Options::default())
	}
}

#[cfg(test)]
mod test {
	use super::{Context, Options, DEFAULT_FUEL};
	use crate::error::Error;
	use crate::grammar::Grammar;
	use crate::parse;

	/// Fuel is one tank for the whole parse: every context derived from the same [`Context::new`]
	/// draws from it, so nesting cannot mint more.
	#[test]
	fn derived_contexts_share_one_tank() {
		let context = Context::new(Options {
			fuel: 4,
			..Default::default()
		});

		let child = context.clone().with_grammar(Grammar::Bold);
		let grandchild = child.clone().with_deeper_list();
		// `fresh` resets grammar state, but deliberately not the budget.
		let unrelated = grandchild.fresh();

		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(ctx.consume_fuel());
			assert_eq!(context.remaining_fuel(), ctx.remaining_fuel());
		}

		assert_eq!(context.remaining_fuel(), 0);
		// The fourth draw emptied the tank; every context now reports empty rather than one of
		// them still holding a reserve.
		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(!ctx.consume_fuel());
		}
	}

	/// Exhausting the tank fails the parse outright — the caller gets an error, not a truncated
	/// AST — and an error type that keeps the external error says so. This is the cost of setting
	/// [`Options::fuel`] too low.
	#[test]
	fn exhaustion_fails_the_parse() {
		let s = "**bold** and _italic_";

		let err = parse::<(), Error<'_>>(
			s,
			Options {
				fuel: 1,
				..Default::default()
			},
		)
		.expect_err("one unit cannot cover a nested rule");
		assert_eq!(err, Error::OutOfFuel);

		parse::<(), Error<'_>>(s, Options::default())
			.expect("the same input parses with the default budget");
	}

	/// The worst 4000-character input the timeout tests know about stays far inside
	/// [`DEFAULT_FUEL`], which is what makes that default safe to ship. If this starts failing,
	/// a rule change has made backtracking much more expensive.
	#[test]
	fn default_fuel_covers_worst_case_message_content() {
		// Discord's message limit is 4000 characters. Both emphasis families are here because
		// `Grammar::overlapping_rules` makes an italic spend a whole bold (or underline) parse at
		// the position where it would otherwise have closed, and the two run different parsers.
		for s in [
			"__".repeat(1_000) + "x" + &"_".repeat(1_998),
			"**".repeat(1_000) + "x" + &"*".repeat(1_998),
		] {
			assert_eq!(s.chars().count(), 4_000 - 1);

			let used = (1..=5)
				.map(|n| DEFAULT_FUEL / 10 * n)
				.find(|&fuel| {
					parse::<(), Error<'_>>(
						&*s,
						Options {
							fuel,
							..Default::default()
						},
					)
					.is_ok()
				})
				.expect("worst-case message content should fit in half the default budget");

			assert!(
				used <= DEFAULT_FUEL / 2,
				"worst-case message content used {used} of {DEFAULT_FUEL} fuel, leaving too little headroom"
			);
		}
	}
}
