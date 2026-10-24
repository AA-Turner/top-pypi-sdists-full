//! Inline code parsing.

use nom::{
	Parser,
	branch::alt,
	bytes::complete::{tag, take_until1},
	error::ParseError,
	sequence::delimited,
};

use crate::Input;

pub const SINGLE_DELIMITER: &str = "`";
pub const DOUBLE_DELIMITER: &str = "``";

/// Unparse inline code back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse(code: &str, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	if code.contains('`') {
		write!(f, "{DOUBLE_DELIMITER}{code}{DOUBLE_DELIMITER}")
	} else {
		write!(f, "{SINGLE_DELIMITER}{code}{SINGLE_DELIMITER}")
	}
}

/// Parse inline code in either syntax.
///
/// # Errors
/// If the content does not begin with inline code.
#[must_use]
pub fn code<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	alt((single(), double()))
}

/// Parse inline code delimited by [`SINGLE_DELIMITER`].
///
/// # Errors
/// If the content does not begin with such code.
#[must_use]
pub fn single<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		tag(SINGLE_DELIMITER),
		take_until1(SINGLE_DELIMITER),
		tag(SINGLE_DELIMITER),
	)
}

/// Parse inline code delimited by [`DOUBLE_DELIMITER`], which can hold a single backtick.
///
/// # Errors
/// If the content does not begin with such code.
#[must_use]
pub fn double<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		tag(DOUBLE_DELIMITER),
		take_until1(DOUBLE_DELIMITER),
		tag(DOUBLE_DELIMITER),
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

	use super::code;

	#[test]
	fn simple_code() {
		let s = "`foo`";
		let (rem, res) = code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo");
	}

	#[test]
	fn empty_code() {
		let s = "``";
		code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn escaped_code() {
		let s = r"`foo\`bar`";
		let (rem, res) = code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "bar`");
		assert_eq!(res, "foo\\");
	}

	#[test]
	fn code_with_italic() {
		let s = r"`_foobar_`";
		let (rem, res) = code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "_foobar_");
	}

	#[test]
	fn code_with_link() {
		let s = r"`foo\nbar`";
		let (rem, res) = code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo\\nbar");
	}

	#[test]
	fn double_delimiter_contains_single_delimiter() {
		let s = r"``foo`bar``";
		let (rem, res) = code()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo`bar");
	}
}
