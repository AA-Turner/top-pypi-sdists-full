use std::marker::PhantomData;

use nom::Parser;

use crate::{
	Input,
	error::ParseError,
	scope::{Scope, ScopeSet},
};

/// The line prefix required by the innermost enclosing container scope, or the empty string if
/// there is no container.
///
/// Container prefixes are conjunctive rather than alternative, so this selects the one container in
/// scope rather than alternating over the whole set. [`Scope::Quote`] is the only container today
/// and it cannot nest -- it disables [`crate::syntax::Syntax::QUOTES`] for its own content -- so at
/// most one scope in the set imposes a prefix.
pub struct LinePrefix<E> {
	pub scopes: ScopeSet,
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
		self.scopes
			.iter()
			.find(|scope| scope.has_line_prefix())
			.unwrap_or(Scope::None)
			.line_prefix()
			.process::<OM>(input)
	}
}
