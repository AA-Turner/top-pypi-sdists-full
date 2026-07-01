use std::{
	fmt::Debug,
	marker::PhantomData,
	sync::{atomic::AtomicBool, Arc},
};

use nom::Parser;
use rule_set::ContextualRules;
use start_sequence::StartSequence;
pub use terminal_sequence::TerminalOutput;
use terminal_sequence::TerminalSequence;

use crate::{
	context::matched_pairs::MatchedPairsParser,
	error::ParseError,
	grammar::{ByteHint, Grammar, GrammarStruct},
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

mod matched_pairs;
mod rule;
mod rule_set;
mod start_sequence;
mod terminal_sequence;

/// Per-grammar precheck hints stored in [`Context`]. Each field corresponds to a grammar
/// whose inner parser would do O(N) work before failing on adversarial input. Hints are
/// computed once per top-level [`crate::inline::InlineParser`] call and propagated to all
/// child contexts via [`Context::with_grammar`].
pub type GrammarHints = GrammarStruct<ByteHint>;

impl GrammarHints {
	/// Returns `true` if any tracked hint is still `Unknown` and needs to be computed.
	fn any_unknown(&self) -> bool {
		self.iter().any(|hint| *hint == ByteHint::Unknown)
	}

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

#[derive(Debug)]
pub struct Options {
	pub allowed_rules: RuleSet,
	pub cancelled: Arc<AtomicBool>,
}

impl Default for Options {
	fn default() -> Self {
		Self {
			allowed_rules: RuleSet::all(),
			cancelled: Arc::new(AtomicBool::new(false)),
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
	pub hints: GrammarHints,
	pub cancelled: Arc<AtomicBool>,
	parents: GrammarSet,
}

impl Context {
	/// Create a new context from the specified rule.
	#[must_use]
	pub fn new(options: Options) -> Self {
		Self {
			grammar: Grammar::None,
			allowed_rules: options.allowed_rules,
			hints: GrammarHints::default(),
			cancelled: options.cancelled,
			parents: GrammarSet::new(),
		}
	}

	/// Create a new context by merging this context with another grammar. This will subtract the
	/// [`Grammar::disabled_rules`] from the current allowed rules.
	#[must_use]
	pub fn with_grammar(self, grammar: Grammar) -> Context {
		Context {
			grammar,
			allowed_rules: self.allowed_rules - grammar.disabled_rules(),
			hints: self.hints,
			cancelled: Arc::clone(&self.cancelled),
			parents: self.parents | self.grammar,
		}
	}

	#[must_use]
	pub fn with_hints(&self, input: &Input) -> Self {
		if !self.hints.any_unknown() {
			return self.clone();
		}

		let grammars = self
			.allowed_rules
			.iter()
			.flat_map(|rule| rule.grammar())
			.collect::<GrammarSet>();
		let hints = self.hints.for_grammars(grammars, input);

		Self {
			hints,
			..self.clone()
		}
	}

	/// Create a fresh grammar with the same allowed rules but reset all grammar state.
	pub fn fresh(&self) -> Self {
		Self {
			grammar: Grammar::None,
			allowed_rules: self.allowed_rules,
			hints: GrammarHints::default(),
			cancelled: Arc::clone(&self.cancelled),
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
		StartSequence(
			self.allowed_rules
				.into_iter()
				.map(|rule| rule.grammar())
				.collect(),
			PhantomData,
		)
	}

	/// Check whether we are in a terminal sequence; if not, apply the `normal` parser. Returns the
	/// output of either [`Grammar::override_terminal_sequence`] (if it's matched) or `normal`. Fails
	/// if a terminal sequence is encountered.
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

	#[must_use]
	pub fn grammars(&self) -> GrammarSet {
		self.parents | self.grammar
	}
}

impl Default for Context {
	fn default() -> Self {
		Self::new(Options::default())
	}
}
