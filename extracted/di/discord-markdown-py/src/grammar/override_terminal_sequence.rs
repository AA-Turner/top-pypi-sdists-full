use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	bytes::complete::tag,
	character::char,
	combinator::{fail, recognize},
	error::ParseError,
	OutputMode, PResult, Parser,
};
use tracing::Level;

use crate::{
	inline::italic,
	span::{TraceOk, TraceParse},
	util::single_alphanumeric,
	Input,
};

use super::Grammar;

pub struct OverrideTerminalSequence<E>(pub Grammar, pub PhantomData<E>);

impl<E> Debug for OverrideTerminalSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("OverrideTerminalSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for OverrideTerminalSequence<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "override_terminal_sequence", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Grammar::UnderscoreItalic => alt((
				recognize((
					single_alphanumeric,
					tag(italic::UNDERSCORE_DELIMITER),
					single_alphanumeric,
				)),
				recognize((tag(italic::UNDERSCORE_DELIMITER), char('('))),
			))
			.trace_parse()
			.process::<OM>(input),
			// in most cases there is no overridden terminal sequence
			_ => fail().process::<OM>(input),
		}
		.trace_ok()
	}
}
