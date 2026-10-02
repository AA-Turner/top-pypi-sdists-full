use std::marker::PhantomData;

use nom::Parser;

use crate::{
	error::ParseError,
	grammar::{Grammar, GrammarSet},
	Input,
};

/// The line prefix required by the innermost enclosing container grammar, or the empty string if
/// there is no container.
///
/// Container prefixes are conjunctive rather than alternative, so this selects the one container in
/// scope rather than alternating over the whole set. [`Grammar::Quote`] is the only container today
/// and it cannot nest -- it disables [`crate::rule::Rule::Quote`] for its own content -- so at most
/// one grammar in the set imposes a prefix.
pub struct LinePrefix<E> {
	pub grammars: GrammarSet,
	pub error: PhantomData<E>,
}

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
		self.grammars
			.iter()
			.find(|grammar| grammar.has_line_prefix())
			.unwrap_or(Grammar::None)
			.line_prefix()
			.process::<OM>(input)
	}
}
