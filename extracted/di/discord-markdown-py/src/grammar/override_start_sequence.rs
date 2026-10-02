use std::{fmt::Debug, marker::PhantomData};

use enumset::enum_set;
use nom::{
	branch::alt,
	bytes::complete::tag,
	character::char,
	combinator::{peek, recognize},
	OutputMode, PResult, Parser,
};
use tracing::Level;

use crate::{
	error::ParseError,
	inline::italic,
	span::{TraceOk, TraceParse},
	util::single_alphanumeric,
	Input,
};

use super::{Grammar, GrammarSet};

/// The grammars for which [`parser`] returns [`Some`].
///
/// Callers intersect with this so the search is proportional to the number of overrides that exist
/// rather than to the number of grammars in play.
// Keep this in sync with the `grammars_is_exhaustive` test below.
pub const GRAMMARS: GrammarSet = enum_set!(Grammar::UnderscoreItalic);

/// Which grammar's override a [`OverrideStartSequence`] runs.
#[derive(Debug, Clone, Copy)]
enum Override {
	UnderscoreItalic,
}

/// A grammar's start override.
pub struct OverrideStartSequence<E>(Override, PhantomData<E>);

/// Build the [`Grammar::override_start_sequence`] for `grammar`, or [`None`] if it defines no
/// override.
pub fn parser<E>(grammar: Grammar) -> Option<OverrideStartSequence<E>> {
	match grammar {
		Grammar::UnderscoreItalic => Some(OverrideStartSequence(
			Override::UnderscoreItalic,
			PhantomData,
		)),
		_ => None,
	}
}

impl<E> Debug for OverrideStartSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("OverrideStartSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for OverrideStartSequence<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "override_start_sequence", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			// Anchored on the preceding alphanumeric: an underscore glued to the end of a word is
			// part of that word, not an opening delimiter. Unlike the terminal override the leading
			// alphanumeric is required -- without it a bare `_(` would stop `_(foo)_` from opening
			// an italic at all.
			//
			// The character that closes the sequence is only peeked, never consumed: `(` has to
			// stay in the input so that the balanced-paren branch of
			// [`crate::inline::link::LinkCharsParser`] can still open a group on it.
			Override::UnderscoreItalic => recognize((
				single_alphanumeric(),
				tag(italic::UNDERSCORE_DELIMITER),
				peek(alt((
					recognize(single_alphanumeric()),
					recognize(char('(')),
				))),
			))
			.trace_parse()
			.process::<OM>(input),
		}
		.trace_ok()
	}
}

#[cfg(test)]
mod test {
	use super::{parser, GRAMMARS};
	use crate::grammar::GrammarSet;

	/// [`GRAMMARS`] short-circuits the search for overrides, so it must list exactly the grammars
	/// [`parser`] builds one for -- omitting one would silently disable it.
	#[test]
	fn grammars_is_exhaustive() {
		let with_override = GrammarSet::all()
			.iter()
			.filter(|grammar| parser::<()>(*grammar).is_some())
			.collect::<GrammarSet>();

		assert_eq!(with_override, GRAMMARS);
	}
}
