use std::marker::PhantomData;

use enumset::enum_set;
use nom::{
	branch::alt,
	character::complete::{char, line_ending, one_of},
	combinator::{eof, peek, recognize, success, value},
	Parser,
};

use crate::{
	block::quote,
	error::ParseError,
	grammar::{Grammar, GrammarSet},
	Input,
};

pub const LINE_PREFIX_GRAMMARS: GrammarSet = enum_set!(Grammar::Quote);

/// The prefix a container grammar requires at the start of each of its lines.
///
/// Grammars that are not containers match the empty string rather than failing, so that
/// [`crate::context::Context::line_prefix`] can be applied unconditionally at the start of every
/// line.
pub struct LinePrefix<E>(pub Grammar, pub PhantomData<E>);

impl<'data, E> Parser<Input<'data>> for LinePrefix<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			// `>` plus exactly one space on a content line, or a bare `>` on an otherwise empty
			// line. The latter is peeked rather than consumed so that the line ending is left for
			// the block loop to turn into a `Node::Empty`.
			//
			// Only one space belongs to the prefix: the rest is content, and multi-line block rules
			// need it to measure their own indentation. Consuming it greedily would flatten
			// `>   - bar` onto column zero, which would flatten lists.
			Grammar::Quote => recognize((
				char(quote::LINE_PREFIX),
				alt((
					value((), one_of(" \t")),
					peek(value((), alt((line_ending, eof)))),
				)),
			))
			.process::<OM>(input),
			value => {
				debug_assert!(!LINE_PREFIX_GRAMMARS.contains(value));
				recognize(success(())).process::<OM>(input)
			}
		}
	}
}

#[cfg(test)]
mod test {
	use enumset::enum_set;

	use crate::grammar::{line_prefix::LINE_PREFIX_GRAMMARS, Grammar};

	#[test]
	fn set_consistency() {
		assert_eq!(
			enum_set!(Grammar::Quote),
			LINE_PREFIX_GRAMMARS,
			"if this test fails, update either the set or the logic"
		);
	}
}
