use std::{fmt::Debug, marker::PhantomData};

use nom::{combinator::fail, OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	error::ParseError,
	span::{TraceOk, TraceParse},
	util::iter_alt,
	Input,
};

use super::{Grammar, GrammarSet};

pub struct GlobalTerminalSequence<E>(pub Grammar, pub PhantomData<E>);

impl<E> Debug for GlobalTerminalSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("GlobalTerminalSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for GlobalTerminalSequence<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;

	type Error = E;

	#[tracing::instrument(level = Level::TRACE, name = "global_terminal_sequence", fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Grammar::InlineBlock => fail().process::<OM>(input),
			// in most cases we fall back to the regular terminal sequence
			_ => self
				.0
				.terminal_sequence()
				.trace_parse()
				.process::<OM>(input),
		}
		.trace_ok()
	}
}

pub struct GlobalTerminalSequenceSet<E>(pub GrammarSet, pub PhantomData<E>);

impl<E> Debug for GlobalTerminalSequenceSet<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("GlobalTerminalSequenceSet")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for GlobalTerminalSequenceSet<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "global_terminal_sequence_set", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		iter_alt(|| self.0.iter().map(Grammar::global_terminal_sequence))
			.process::<OM>(input)
			.trace_ok()
	}
}
