use std::{collections::HashSet, fmt::Debug, marker::PhantomData, rc::Rc};

use nom::Parser;
use rule_set::ContextualRules;
use start_sequence::StartSequence;
use terminal_sequence::TerminalSequence;

use crate::{
	context::{fuel::Fuel, line_prefix::LinePrefix, matched_pairs::MatchedPairsParser},
	error::ParseError,
	grammar::{ByteHint, Grammar, GrammarStruct},
	range::delim::Offset,
};

use super::{
	Input,
	grammar::GrammarSet,
	node::Element,
	rule::{ParsedRule, ParsedRuleSet, RuleSet},
	span::Span,
};

#[cfg(doc)]
use super::rule::Rule;

pub mod fuel;
mod line_prefix;
mod matched_pairs;
mod rule;
mod rule_set;
mod start_sequence;
mod terminal_sequence;

/// Per-grammar precheck hints stored in [`Context`].
///
/// Each field corresponds to a grammar whose inner parser would do O(N) work before
/// failing on adversarial input. Hints are computed once per top-level
/// [`crate::node::inline::inline`] call and propagated to all child contexts via
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
/// - Real messages are nowhere near it. The announcement posts in `test_content` need 12–66 fuel;
///   ordinary prose costs about 1 fuel per line plus well under 1 per 100 bytes, because a run of
///   plain text is a single inline parse no matter how long it is.
/// - Adversarial input is what costs. The most expensive 4000-character inputs the timeout tests
///   know about -- short lines that each open a delimiter, some before block syntax -- burn about
///   2.6k, under 1 fuel per byte, in about 3ms. That is the realistic worst case for a Discord
///   message, whose limit is 4000 characters, and this default is far above it.
///
/// Modifiers no longer backtrack at all, so the default leaves room for rules that might. The
/// effect is to cap a pathological parse rather than letting it run unbounded. A caller parsing
/// only message-length content can safely tighten this a long way; see [`Options::fuel`] for what
/// moving it in either direction costs.
pub const DEFAULT_FUEL: u32 = 500_000;

#[derive(Debug, Clone, Copy)]
pub struct Options {
	pub allowed_rules: RuleSet,
	/// How much work the parse is allowed to do before it gives up with
	/// [`fuel::OutOfFuel`].
	///
	/// One unit of fuel buys one invocation of the inline parser, or one line of block content.
	/// Those are the parser's units of backtracking, so the count includes every attempt that a
	/// rule later abandons — which is exactly where pathological input spends its time. Fuel is a
	/// single tank shared by the whole parse, not a per-rule or per-nesting-level allowance, so it
	/// bounds total work rather than depth.
	///
	/// Fuel consumption tracks the parser's running time, but it is not a wall-clock budget. A unit
	/// costs on the order of a quarter of a microsecond in a release build, but a single unit's cost
	/// varies with the input, resolving modifiers is not metered at all (it is linear), and rule
	/// changes move it. Treat a fuel figure as a bound on work, and re-measure after changing the
	/// parser rather than assuming it still buys the same number of milliseconds.
	///
	/// Raising this lets more (or more adversarial) content parse, at the cost of a higher
	/// worst-case time and allocation count per parse. Lowering it caps that worst case more
	/// tightly, at the risk of rejecting legitimate content — a parse that runs dry fails outright
	/// with [`fuel::OutOfFuel`] and returns no partial AST, so a limit set too low is a
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
	/// The members of [`Self::allowed_rules`] with a parser, cached because they are derived once
	/// per context but tried at every position.
	parsed_rules: ParsedRuleSet,
	/// The grammars [`Self::allowed_rules`] can reach, cached because it is derived once per
	/// context but consulted once per character. See [`Self::allowed_grammars`].
	allowed_grammars: GrammarSet,
	// This struct is huge so we reference count it to keep it off the stack and reduce allocations
	pub hints: Rc<GrammarHints>,
	/// The depth of the innermost enclosing list, used to implement a cap to list depth. This is
	/// 1-indexed for lists — an unnested list is at depth 1 — and is 0 when not inside a list at
	/// all.
	///
	/// This is a `u8` because the maximum is [`crate::node::block::list::MAX_DEPTH`].
	pub list_depth: u8,
	parents: GrammarSet,
	/// Shared by every context of a parse, including the ones [`Context::fresh`] hands out, so that
	/// the budget covers the parse as a whole rather than resetting per rule. See
	/// [`Context::remaining_fuel`].
	fuel: Fuel,
	/// See [`Context::is_disabled_opener`].
	disabled_openers: Rc<HashSet<Offset>>,
}

/// The grammars `rules` can reach. Derived once per [`Context`] rather than per call; see
/// [`Context::allowed_grammars`].
fn grammars_for(rules: ParsedRuleSet) -> GrammarSet {
	rules.iter().flat_map(ParsedRule::grammar).collect()
}

impl Context {
	/// Create a new context from the specified rule.
	#[must_use]
	pub fn new(options: Options) -> Self {
		let parsed_rules = ParsedRule::allowed(options.allowed_rules);
		Self {
			grammar: Grammar::None,
			allowed_rules: options.allowed_rules,
			parsed_rules,
			allowed_grammars: grammars_for(parsed_rules),
			hints: Rc::new(GrammarHints::default()),
			list_depth: 0,
			parents: GrammarSet::new(),
			fuel: Fuel::new(options.fuel),
			disabled_openers: Rc::new(HashSet::new()),
		}
	}

	#[must_use]
	pub fn with_disabled_openers(self, disabled: &HashSet<Offset>) -> Self {
		let disabled_openers = Rc::new(self.disabled_openers.union(disabled).copied().collect());

		Self {
			disabled_openers,
			..self
		}
	}

	/// Whether the delimiter run at `offset` is one that an earlier parse read before block syntax,
	/// as in `*1. foo`, but that matched nothing. Its line is a paragraph; see
	/// [`crate::range::delim::opener`].
	#[must_use]
	pub fn is_disabled_opener(&self, offset: Offset) -> bool {
		self.disabled_openers.contains(&offset)
	}

	/// This parse's fuel tank, started at [`Options::fuel`]. The inline parser spends a unit per
	/// invocation and the block parser a unit per line.
	///
	/// This is how a caller measures what its own corpus costs, which is what picking a value for
	/// [`Options::fuel`] rests on. [`crate::parse`] builds its context internally, so measuring
	/// means driving the parser directly and keeping a handle on the context — every context
	/// derived from it draws down the same tank, so the one here still reflects the whole parse
	/// when it finishes:
	///
	/// ```
	/// # use discord_markdown::{context::{Context, Options}, node::block};
	/// # use nom::{combinator::all_consuming, Finish, Parser};
	/// let options = Options::default();
	/// let context = Context::new(options);
	///
	/// let result = all_consuming(block::block::<(), nom::error::Error<_>>(context.clone()))
	///     .parse_complete("**hello** world".into())
	///     .finish();
	///
	/// assert!(result.is_ok());
	/// println!("used {} fuel", options.fuel - context.remaining_fuel().get());
	/// ```
	#[must_use]
	pub fn remaining_fuel(&self) -> &Fuel {
		&self.fuel
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
		let parsed_rules = ParsedRule::allowed(allowed_rules);

		Context {
			grammar,
			allowed_rules,
			parsed_rules,
			allowed_grammars: grammars_for(parsed_rules),
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

	/// Create a fresh grammar with the same allowed rules but reset all grammar state. It still
	/// draws from this parse's fuel tank.
	#[must_use]
	pub fn fresh(&self) -> Self {
		Self {
			grammar: Grammar::None,
			allowed_rules: self.allowed_rules,
			parsed_rules: self.parsed_rules,
			allowed_grammars: self.allowed_grammars,
			hints: Rc::new(GrammarHints::default()),
			list_depth: 0,
			parents: GrammarSet::new(),
			fuel: self.fuel.clone(),
			disabled_openers: Rc::clone(&self.disabled_openers),
		}
	}

	/// Get allowed inline rules in the current context. Modifiers are not among them: they are
	/// recorded as delimiters and resolved afterwards; see [`crate::range`].
	#[must_use]
	pub fn allowed_inline_rules<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Element<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualRules::<S, E>::from_context(self, self.parsed_rules & ParsedRule::INLINE)
	}

	/// Get allowed block rules in the current context.
	#[must_use]
	pub fn allowed_block_rules<'data, 'ctx, S, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Element<'data, S>, Error = E> + 'ctx
	where
		S: Span,
		E: ParseError<'data> + 'ctx,
	{
		ContextualRules::from_context(self, self.parsed_rules & ParsedRule::BLOCK)
	}

	/// Get allowed start sequences for the current context. This is based on [`Self::allowed_rules`]:
	/// for example, if [`Rule::Code`] is in this set, then this will match its start sequence (`` ` ``).
	#[must_use]
	pub fn allowed_start_sequences<'ctx, 'data, E>(
		&'ctx self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data> + 'ctx,
	{
		StartSequence(self.allowed_grammars, PhantomData)
	}

	/// Check whether we are in a terminal sequence; if not, apply the `normal` parser. Fails if a
	/// terminal sequence is encountered.
	pub fn guard_terminal_sequence<'ctx, 'data, O, E, P>(
		&'ctx self,
		normal: impl Fn() -> P + 'ctx,
	) -> impl Parser<Input<'data>, Output = O, Error = E> + 'ctx
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
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E> + use<'data, E>
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
	use super::{Context, Options};
	use crate::grammar::Grammar;

	/// Fuel is one tank for the whole parse: every context derived from the same [`Context::new`]
	/// draws from it, so nesting cannot mint more.
	#[test]
	fn derived_contexts_share_one_tank() {
		let context = Context::new(Options {
			fuel: 4,
			..Default::default()
		});

		let child = context.clone().with_grammar(Grammar::Quote);
		let grandchild = child.clone().with_deeper_list();
		// `fresh` resets grammar state, but deliberately not the budget.
		let unrelated = grandchild.fresh();

		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(ctx.remaining_fuel().consume());
			assert_eq!(context.remaining_fuel(), ctx.remaining_fuel());
		}

		assert_eq!(*context.remaining_fuel(), 0);
		// The fourth draw emptied the tank; every context now reports empty rather than one of
		// them still holding a reserve.
		for ctx in [&context, &child, &grandchild, &unrelated] {
			assert!(!ctx.remaining_fuel().consume());
		}
	}
}
