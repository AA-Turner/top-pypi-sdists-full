use std::marker::PhantomData;

use enumset::enum_set;
use nom::{
	Parser,
	branch::alt,
	character::complete::{char, line_ending, one_of},
	combinator::{eof, peek, recognize, success, value},
};

use crate::{
	Input,
	error::ParseError,
	node::block::quote,
	scope::{Scope, ScopeSet},
};

pub const LINE_PREFIX_SCOPES: ScopeSet = enum_set!(Scope::Quote);

/// The prefix a container grammar requires at the start of each of its lines.
///
/// Grammars that are not containers match the empty string rather than failing, so that
/// [`crate::context::Context::line_prefix`] can be applied unconditionally at the start of every
/// line.
pub struct LinePrefix<E>(pub Scope, pub PhantomData<E>);

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
			// the block loop to turn into an `Element::Empty`.
			//
			// Only one space belongs to the prefix: the rest is content, and multi-line block rules
			// need it to measure their own indentation. Consuming it greedily would flatten
			// `>   - bar` onto column zero, which would flatten lists.
			Scope::Quote => recognize((
				char(quote::LINE_PREFIX),
				alt((
					value((), one_of(" \t")),
					peek(value((), alt((line_ending, eof)))),
				)),
			))
			.process::<OM>(input),
			value => {
				debug_assert!(!LINE_PREFIX_SCOPES.contains(value));
				recognize(success(())).process::<OM>(input)
			}
		}
	}
}

#[cfg(test)]
mod test {
	use enumset::enum_set;

	use crate::scope::{Scope, line_prefix::LINE_PREFIX_SCOPES};

	#[test]
	fn set_consistency() {
		assert_eq!(
			enum_set!(Scope::Quote),
			LINE_PREFIX_SCOPES,
			"if this test fails, update either the set or the logic"
		);
	}
}
