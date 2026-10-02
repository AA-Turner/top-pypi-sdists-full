use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	combinator::{fail, not},
	sequence::preceded,
	Check, Mode, OutputM, OutputMode, PResult, Parser,
};
use tracing::Level;

use crate::{
	context::matched_pairs,
	error::ParseError,
	grammar::{global_terminals, GrammarSet},
	span::{TraceOk, TraceParse},
	util::iter_alt,
	Input,
};

use super::{super::grammar::Grammar, rule_set::ContextualRules, Context};

pub(super) struct TerminalSequence<'ctx, F, E> {
	pub context: &'ctx Context,
	pub normal: F,
	pub error: PhantomData<E>,
}

impl<'ctx, 'data, F, P, O, E> Parser<Input<'data>> for TerminalSequence<'ctx, F, E>
where
	E: ParseError<'data> + 'ctx,
	F: Fn() -> P,
	P: Parser<Input<'data>, Output = O, Error = E> + 'ctx,
	O: Debug,
{
	type Output = TerminalOutput<'data, O>;
	type Error = E;

	#[tracing::instrument(
	    skip(self),
		fields(context = ?self.context, ok, output),
		name = "context_terminal_sequence",
		level = Level::TRACE
	)]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		alt((
			// overrides consume text that would otherwise read as a delimiter -- an intraword `_`
			// is part of the word, not an italic marker -- so they come before any terminal check
			self.context.overrides().map(TerminalOutput::Override),
			preceded(
				(
					not(iter_alt(|| {
						// we consider the _start_ sequence a terminal so that the parent can be aware of the matched
						// pairs without blindly consuming the opening token
						(self.context.grammars() & matched_pairs::GRAMMARS)
							.iter()
							.map(Grammar::start_sequence)
					})),
					// the terminal loses to a longer delimiter that actually opens a rule here
					alt((
						not(self.context.grammar.terminal_sequence()),
						OverlappingRule {
							context: self.context,
							error: PhantomData,
						},
					)),
					not(global_terminals(self.context.parents)),
				),
				(self.normal)().map(TerminalOutput::Normal),
			),
		))
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Succeeds, consuming nothing, when this grammar's terminal sequence should stand down because a
/// longer delimiter opens a rule right here -- see [`Grammar::overlapping_rules`].
///
/// The rule has to *parse*, not merely start: in `*a**b*` no bold can close, so the terminal still
/// wins and the italic ends where it always did.
struct OverlappingRule<'ctx, E> {
	context: &'ctx Context,
	error: PhantomData<E>,
}

impl<E> Debug for OverlappingRule<'_, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("OverlappingRule")
			.field("context", &self.context)
			.finish_non_exhaustive()
	}
}

impl<'data, E> Parser<Input<'data>> for OverlappingRule<'_, E>
where
	E: ParseError<'data>,
{
	type Output = ();
	type Error = E;

	#[tracing::instrument(name = "overlapping_rule", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let rules = self.context.grammar.overlapping_rules() & self.context.allowed_rules;

		// Immediately bail in the common case where there are no overlapping rules.
		if rules.is_empty() {
			return fail().process::<OM>(input);
		}

		// Past the opener, a longer run leaves this grammar's own terminal -- and the probed rule
		// inherits that as a global terminal, so it would open on an empty body and fail. The probe
		// below would reach the same answer; this just gets there without running it.
		let openers = rules
			.iter()
			.flat_map(|rule| rule.grammar())
			.collect::<GrammarSet>();
		let run_is_exact = (
			iter_alt(|| openers.iter().map(Grammar::start_sequence::<E>)),
			not(self.context.grammar.terminal_sequence()),
		)
			.process::<OutputM<Check, Check, OM::Incomplete>>(input.clone())
			.is_err();
		if run_is_exact {
			return fail().process::<OM>(input);
		}

		let mut probe = ContextualRules::<(), E>::from_context(self.context, rules);

		match probe.process::<OutputM<Check, Check, OM::Incomplete>>(input.clone()) {
			Ok(_) => Ok((input, OM::Output::bind(|| ()))),
			Err(nom::Err::Error(())) => fail().process::<OM>(input),
			Err(nom::Err::Failure(error)) => Err(nom::Err::Failure(error)),
			Err(nom::Err::Incomplete(needed)) => Err(nom::Err::Incomplete(needed)),
		}
	}
}

/// Output of [`Context::guard_terminal_sequence`].
#[derive(Debug, Clone)]
pub enum TerminalOutput<'data, N> {
	/// An override sequence was matched.
	Override(Input<'data>),
	/// The normal parser was matched.
	Normal(N),
}

#[allow(clippy::mismatching_type_param_order)]
impl<'data> TerminalOutput<'data, Input<'data>> {
	#[must_use]
	pub fn inner(self) -> Input<'data> {
		match self {
			Self::Override(input) | Self::Normal(input) => input,
		}
	}
}
