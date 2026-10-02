use std::{fmt::Debug, marker::PhantomData};

use nom::{branch::alt, error::ErrorKind, Check, Mode, OutputM, OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	error::ParseError,
	grammar::{Grammar, GrammarSet},
	span::{TraceOk, TraceParse},
	util::{iter_alt, maybe},
	Input,
};

/// Runs every override that applies here -- see [`crate::Context::overrides`].
pub struct Overrides<E> {
	/// The grammar being parsed, whose terminal override (if any) applies.
	pub grammar: Grammar,
	/// The grammars whose start overrides apply, already restricted to the allowed rules.
	pub start: GrammarSet,
	pub error: PhantomData<E>,
}

impl<E> Debug for Overrides<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("Overrides")
			.field("grammar", &self.grammar)
			.field("start", &self.start)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for Overrides<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "overrides", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let mut overrides = alt((
			maybe(self.grammar.override_terminal_sequence()),
			iter_alt(|| {
				self.start
					.iter()
					.filter_map(Grammar::override_start_sequence)
			}),
		))
		.trace_parse();

		// Run with the error mode switched to [`Check`], which makes `OM::Error::bind` a no-op, and
		// synthesise an error only if we actually need one. Nothing reads the error this branch
		// produces: the enclosing `alt` folds branch errors with `ParseError::or`, and
		// [`crate::error::Error::or`] keeps the later one -- so this branch's error is discarded
		// whenever anything else runs. Building it in `Emit` mode is pure waste, and this branch is
		// attempted once per character of every text run.
		match overrides.process::<OutputM<OM::Output, Check, OM::Incomplete>>(input.clone()) {
			Ok((remaining, matched)) => Ok((remaining, matched)),
			Err(nom::Err::Error(())) => Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Alt)
			}))),
			// `PResult` only mode-wraps the recoverable error; a `Failure` carries the real `E`
			// whatever the mode, so an aborting error still travels intact.
			Err(nom::Err::Failure(error)) => Err(nom::Err::Failure(error)),
			Err(nom::Err::Incomplete(needed)) => Err(nom::Err::Incomplete(needed)),
		}
		.trace_ok()
	}
}
