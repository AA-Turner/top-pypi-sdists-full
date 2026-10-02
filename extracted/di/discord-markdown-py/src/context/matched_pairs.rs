use std::marker::PhantomData;

use enumset::enum_set;
use nom::{
	error::{ErrorKind, ParseError},
	Input as _, Mode, Parser,
};

use crate::{
	grammar::{Grammar, GrammarSet},
	util::balanced_span,
	Input,
};

pub const GRAMMARS: GrammarSet = enum_set!(Grammar::MaskedLinkText);

pub struct MatchedPairsParser<E> {
	pub grammars: GrammarSet,
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
		for grammar in (self.grammars & GRAMMARS).iter() {
			let Some((open, close)) = grammar.bracket_delimiters() else {
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
