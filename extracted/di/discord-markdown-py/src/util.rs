use std::marker::PhantomData;

use memchr::memchr2_iter;
use nom::branch::alt;
use nom::bytes::complete::{take_until, take_while1};
use nom::character::complete::char;
use nom::character::satisfy;
use nom::combinator::{recognize, rest};
use nom::error::{ErrorKind, ParseError};
use nom::{Err, IResult, Mode, OutputMode, PResult, Parser};

use crate::Input;

/// Byte length of the balanced `open`/`close` span at the start of `bytes`, counting both
/// delimiters, whatever the span encloses.
///
/// Returns `None` if `bytes` does not begin with `open` or if nothing closes the span. Depth
/// counting keeps this a single pass with no recursion. `open` and `close` must differ.
#[must_use]
pub fn balanced_span(bytes: &[u8], open: u8, close: u8) -> Option<usize> {
	debug_assert_ne!(
		open, close,
		"a span cannot open and close with the same byte"
	);

	if bytes.first() != Some(&open) {
		return None;
	}

	let mut depth = 0usize;

	for pos in memchr2_iter(open, close, bytes) {
		if bytes[pos] == open {
			depth += 1;
		} else {
			depth -= 1;
			if depth == 0 {
				return Some(pos + 1);
			}
		}
	}

	None
}

/// Parse a single alphanumeric character.
#[must_use]
pub fn single_alphanumeric<'data, E>() -> impl Parser<Input<'data>, Output = char, Error = E>
where
	E: ParseError<Input<'data>>,
{
	satisfy(|c: char| c.is_ascii_alphanumeric())
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

/// A parser that defers to `parser`, or fails outright if there is none.
pub fn maybe<'data, P, O, E>(parser: Option<P>) -> impl Parser<Input<'data>, Output = O, Error = E>
where
	P: Parser<Input<'data>, Output = O, Error = E>,
	E: ParseError<Input<'data>>,
{
	Maybe {
		parser,
		_output: PhantomData,
		_error: PhantomData,
	}
}

struct Maybe<P, O, E> {
	parser: Option<P>,
	_output: PhantomData<O>,
	_error: PhantomData<E>,
}

impl<'data, P, O, E> Parser<Input<'data>> for Maybe<P, O, E>
where
	P: Parser<Input<'data>, Output = O, Error = E>,
	E: ParseError<Input<'data>>,
{
	type Output = O;
	type Error = E;

	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match &mut self.parser {
			Some(parser) => parser.process::<OM>(input),
			None => Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Fail)
			}))),
		}
	}
}

#[cfg(test)]
mod test {
	use super::balanced_span;

	/// Span the brackets at the start of `s`.
	fn brackets(s: &str) -> Option<usize> {
		balanced_span(s.as_bytes(), b'[', b']')
	}

	#[test]
	fn spans_a_pair_and_its_nesting() {
		assert_eq!(brackets("[]"), Some(2));
		assert_eq!(brackets("[a]"), Some(3));
		assert_eq!(brackets("[[a][b]]rest"), Some(8));
	}

	#[test]
	fn needs_an_opener_and_a_close() {
		assert_eq!(brackets("a[]"), None);
		assert_eq!(brackets(""), None);
		assert_eq!(brackets("[a"), None);
		assert_eq!(brackets("[[a]"), None);
	}

	/// A span may run past a close that a deeper level already claimed.
	#[test]
	fn closes_at_matching_depth() {
		assert_eq!(brackets("[a[b]c]d"), Some(7));
	}

	/// Nothing between the delimiters is off limits, newlines included.
	#[test]
	fn crosses_any_content() {
		assert_eq!(brackets("[a b\nc]"), Some(7));
	}
}
