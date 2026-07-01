use nom::{
	bytes::complete::{tag, take_until1},
	error::ParseError,
	sequence::delimited,
	Parser,
};

use crate::Input;

pub const DELIMITER: &str = "`";

/// Unparse inline code back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse(code: &str, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	write!(f, "{DELIMITER}{code}{DELIMITER}")
}

/// Parse inline code.
///
/// # Errors
/// If the content does not begin with inline code.
#[must_use]
pub fn code<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	// TODO: allow escaping code
	delimited(tag(DELIMITER), take_until1(DELIMITER), tag(DELIMITER))
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
}
