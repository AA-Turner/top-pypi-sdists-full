use std::marker::PhantomData;

use enumset::enum_set;
use nom::{
	Input as _, Mode, Parser,
	error::{ErrorKind, ParseError},
};

use crate::{
	Input,
	scope::{Scope, ScopeSet},
	util::balanced_span,
};

pub const SCOPES: ScopeSet = enum_set!(Scope::MaskedLinkText);

pub struct MatchedPairsParser<E> {
	pub scopes: ScopeSet,
	pub error: PhantomData<E>,
}

impl<'data, E> Parser<Input<'data>> for MatchedPairsParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = Input<'data>;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		for scope in (self.scopes & SCOPES).iter() {
			let Some((open, close)) = scope.bracket_delimiters() else {
				continue;
			};
			if let Some(span_len) = balanced_span(input.as_bytes(), open, close) {
				let (remaining, span) = input.take_split(span_len);
				return Ok((remaining, OM::Output::bind(|| span)));
			}
		}
		Err(nom::Err::Error(OM::Error::bind(|| {
			E::from_error_kind(input, ErrorKind::Alt)
		})))
	}
}
