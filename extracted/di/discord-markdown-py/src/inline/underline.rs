use nom::bytes::complete::tag;
use nom::sequence::delimited;
use nom::Parser;

use crate::context::Context;
use crate::error::ParseError;
use crate::node::SpannedNodes;
use crate::span::Span;
use crate::unparse::Unparse;
use crate::{inline, Input};

use super::Grammar;

pub const DELIMITER: &str = "__";

/// Unparse underline content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

/// Parse underline.
///
/// # Errors
/// If the content does not begin with an underline.
// foo\_bar -> foo\_bar
#[must_use]
pub fn underline<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	delimited(
		tag(DELIMITER),
		inline::inline(context.with_grammar(Grammar::Underline)),
		tag(DELIMITER),
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::underline;
	use crate::context::Context;
	use crate::test_utils::handle_nom_err;
	use crate::{spanned_vec, text};

	#[test]
	fn simple_underline() {
		let s = r"__foo__";
		let (rem, res) = underline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo")]);
	}

	#[test]
	fn simple_underline_but_double() {
		let s = r"__foo\__bar\__baz__";
		let (rem, res) = underline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo__bar__baz")]);
	}

	#[test]
	fn escaped_underline() {
		let s = r"__foo\_\_bar\_\_baz__";
		let (rem, res) = underline::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo__bar__baz")]);
	}
}
