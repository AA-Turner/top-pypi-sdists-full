//! Inline code parsing.

use crate::{
	Input,
	error::PResult,
	lossless::TokenKind,
	span::{Span, Syntax},
};

pub const SINGLE_DELIMITER: &str = "`";
pub const DOUBLE_DELIMITER: &str = "``";

/// Parse inline code in either syntax.
///
/// # Errors
/// If the content does not begin with inline code.
pub fn code<'data, S: Span>(input: &mut Input<'data>) -> PResult<(&'data str, S::Syntax)> {
	match input.attempt(single::<S>)? {
		Some(code) => Ok(code),
		None => double::<S>(input),
	}
}

/// Parse inline code delimited by [`SINGLE_DELIMITER`].
///
/// # Errors
/// If the content does not begin with such code.
pub fn single<'data, S: Span>(input: &mut Input<'data>) -> PResult<(&'data str, S::Syntax)> {
	delimited_by::<S>(input, SINGLE_DELIMITER)
}

/// Parse inline code delimited by [`DOUBLE_DELIMITER`], which can hold a single backtick.
///
/// # Errors
/// If the content does not begin with such code.
pub fn double<'data, S: Span>(input: &mut Input<'data>) -> PResult<(&'data str, S::Syntax)> {
	delimited_by::<S>(input, DOUBLE_DELIMITER)
}

fn delimited_by<'data, S: Span>(
	input: &mut Input<'data>,
	delimiter: &str,
) -> PResult<(&'data str, S::Syntax)> {
	let open = input.token::<S, _>(TokenKind::CodeDelimiter, |input| input.tag(delimiter))?;
	let (content, syntax) =
		input.with_token::<S, _>(TokenKind::CodeContent, |input| input.take_until1(delimiter))?;
	let close = input.token::<S, _>(TokenKind::CodeDelimiter, |input| input.tag(delimiter))?;
	Ok((content, open.join(syntax).join(close)))
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::code;

	#[test]
	fn simple_code() {
		let s = "`foo`";
		let (rem, (res, ())) = run(s, code::<()>).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo");
	}

	#[test]
	fn empty_code() {
		let s = "``";
		run(s, code::<()>).expect_err("able to parse");
	}

	#[test]
	fn escaped_code() {
		let s = r"`foo\`bar`";
		let (rem, (res, ())) = run(s, code::<()>).expect("unable to parse");
		assert_eq!(rem, "bar`");
		assert_eq!(res, "foo\\");
	}

	#[test]
	fn code_with_italic() {
		let s = r"`_foobar_`";
		let (rem, (res, ())) = run(s, code::<()>).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "_foobar_");
	}

	#[test]
	fn code_with_link() {
		let s = r"`foo\nbar`";
		let (rem, (res, ())) = run(s, code::<()>).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo\\nbar");
	}

	#[test]
	fn double_delimiter_contains_single_delimiter() {
		let s = r"``foo`bar``";
		let (rem, (res, ())) = run(s, code::<()>).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo`bar");
	}
}
