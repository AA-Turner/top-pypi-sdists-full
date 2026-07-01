use std::{fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	error::ParseError,
	grammar::{Grammar, GrammarSet},
	span::{TraceOk, TraceParse},
	util::iter_alt,
	Input,
};

pub struct StartSequence<E>(pub GrammarSet, pub PhantomData<E>);

impl<E> Debug for StartSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("StartSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for StartSequence<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(level = Level::TRACE, name = "context_start_sequence", fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		iter_alt(|| self.0.iter().map(Grammar::start_sequence))
			.trace_parse()
			.process::<OM>(input)
			.trace_ok()
	}
}
