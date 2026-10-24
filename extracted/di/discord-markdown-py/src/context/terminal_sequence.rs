use std::{fmt::Debug, marker::PhantomData};

use nom::{
	OutputMode, PResult, Parser, character::complete::char, combinator::not, sequence::preceded,
};
use tracing::Level;

use crate::{
	Input,
	context::matched_pairs,
	error::ParseError,
	scope::global_terminals,
	span::{TraceOk, TraceParse},
	util::iter_alt,
};

use super::Context;

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
	type Output = O;
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
		preceded(
			(
				not(iter_alt(|| {
					// we consider the _start_ sequence a terminal so that the parent can be aware of the matched
					// pairs without blindly consuming the opening token
					(self.context.scopes() & matched_pairs::SCOPES)
						.iter()
						.filter_map(|scope| scope.bracket_delimiters())
						.map(|(open, _)| char(open.into()))
				})),
				not(self.context.scope.terminal_sequence()),
				not(global_terminals(self.context.parents)),
			),
			(self.normal)(),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}
