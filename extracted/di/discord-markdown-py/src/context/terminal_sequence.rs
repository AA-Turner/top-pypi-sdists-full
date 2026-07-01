use std::{fmt::Debug, marker::PhantomData};

use nom::{branch::alt, combinator::not, sequence::preceded, OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	context::matched_pairs,
	error::ParseError,
	grammar::global_terminals,
	span::{TraceOk, TraceParse},
	util::iter_alt,
	Input,
};

use super::{super::grammar::Grammar, Context};

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
			self.context
				.grammar
				.override_terminal_sequence()
				.map(TerminalOutput::Override),
			preceded(
				(
					not(iter_alt(|| {
						// we consider the _start_ sequence a terminal so that the parent can be aware of the matched
						// pairs without blindly consuming the opening token
						(self.context.grammars() & matched_pairs::GRAMMARS)
							.iter()
							.map(Grammar::start_sequence)
					})),
					not(self.context.grammar.terminal_sequence()),
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
