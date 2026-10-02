use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt, bytes::complete::tag, character::char, combinator::recognize, OutputMode, PResult,
	Parser,
};
use tracing::Level;

use crate::{
	error::ParseError,
	inline::italic,
	span::{TraceOk, TraceParse},
	util::single_alphanumeric,
	Input,
};

use super::Grammar;

/// Which grammar's override a [`OverrideTerminalSequence`] runs.
///
/// One variant per grammar that defines a terminal override.
#[derive(Debug, Clone, Copy)]
enum Override {
	UnderscoreItalic,
}

/// A grammar's terminal override. Built only via [`parser`], so it can only exist for a grammar
/// that has one.
pub struct OverrideTerminalSequence<E>(Override, PhantomData<E>);

/// Build the [`Grammar::override_terminal_sequence`] for `grammar`, or [`None`] if it defines no
/// override.
pub fn parser<E>(grammar: Grammar) -> Option<OverrideTerminalSequence<E>> {
	match grammar {
		Grammar::UnderscoreItalic => Some(OverrideTerminalSequence(
			Override::UnderscoreItalic,
			PhantomData,
		)),
		_ => None,
	}
}

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
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "override_terminal_sequence", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Override::UnderscoreItalic => alt((
				recognize((
					single_alphanumeric(),
					tag(italic::UNDERSCORE_DELIMITER),
					single_alphanumeric(),
				)),
				recognize((tag(italic::UNDERSCORE_DELIMITER), char('('))),
			))
			.trace_parse()
			.process::<OM>(input),
		}
		.trace_ok()
	}
}

#[cfg(test)]
mod test {
	use super::parser;
	use crate::grammar::{Grammar, GrammarSet};

	/// Only [`Grammar::UnderscoreItalic`] defines a terminal override. Callers rely on this to skip
	/// the grammars that have none, so pin it down.
	#[test]
	fn only_underscore_italic_has_an_override() {
		let with_override = GrammarSet::all()
			.iter()
			.filter(|grammar| parser::<()>(*grammar).is_some())
			.collect::<GrammarSet>();

		assert_eq!(with_override, Grammar::UnderscoreItalic);
	}
}
