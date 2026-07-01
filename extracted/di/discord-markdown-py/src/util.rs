use std::marker::PhantomData;

use nom::branch::alt;
use nom::bytes::complete::{take_until, take_while1};
use nom::character::complete::{char, satisfy};
use nom::combinator::{recognize, rest};
use nom::error::{ErrorKind, ParseError};
use nom::{Err, IResult, Mode, OutputMode, PResult, Parser};

use crate::Input;

/// Parse a single alphanumeric character.
///
/// # Errors
/// If the character is not alphanumeric.
pub fn single_alphanumeric<'data, E>(data: Input<'data>) -> IResult<Input<'data>, char, E>
where
	E: ParseError<Input<'data>>,
{
	satisfy::<_, _, E>(|c| c.is_ascii_alphanumeric())(data)
}

#[must_use]
pub fn alphanumeric_with_extra<'data, E>(
	extra: &'static str,
) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	take_while1::<_, _, E>(|ch| ch.is_ascii_alphanumeric() || extra.contains(ch))
}

pub fn iter_alt<'data, F, Iter, O, E>(items: F) -> impl Parser<Input<'data>, Output = O, Error = E>
where
	F: Fn() -> Iter,
	Iter: IntoIterator<Item: Parser<Input<'data>, Output = O, Error = E>>,
	E: ParseError<Input<'data>>,
{
	IterAlt {
		items,
		_output: PhantomData,
		_error: PhantomData,
	}
}

struct IterAlt<F, O, E> {
	items: F,
	_output: PhantomData<O>,
	_error: PhantomData<E>,
}

impl<'data, F, Iter, O, E> Parser<Input<'data>> for IterAlt<F, O, E>
where
	F: Fn() -> Iter,
	Iter: IntoIterator<Item: Parser<Input<'data>, Output = O, Error = E>>,
	E: ParseError<Input<'data>>,
{
	type Output = O;
	type Error = E;

	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let mut acc_err = None;

		for mut item in (self.items)() {
			match item.process::<OM>(input.clone()) {
				Err(Err::Error(e)) => match acc_err {
					Some(err) => {
						acc_err = Some(OM::Error::combine(err, e, |e1: E, e2| e1.or(e2)));
					}
					None => {
						acc_err = Some(e);
					}
				},
				res => return res,
			}
		}

		Err(nom::Err::Error(match acc_err {
			Some(err) => OM::Error::map(err, move |err| E::append(input, ErrorKind::Alt, err)),
			None => OM::Error::bind(|| E::from_error_kind(input, ErrorKind::Alt)),
		}))
	}
}

/// Take a line of content from the input.
///
/// # Errors
/// If the content does not begin with new-line terminated content
pub fn take_line<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	alt((recognize((take_until("\n"), char('\n'))), rest)).parse_complete(data)
}
