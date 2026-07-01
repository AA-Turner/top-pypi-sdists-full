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

pub const DELIMITER: &str = "**";

/// Unparse bold content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

/// Parse a bold element.
///
/// # Errors
/// If the content does not begin with bold.
#[must_use]
pub fn bold<'ctx, 'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	delimited(
		tag(DELIMITER),
		inline::inline(context.with_grammar(Grammar::Bold)),
		tag(DELIMITER),
	)
}

#[cfg(test)]
mod test {
	use super::bold;
	use crate::context::Context;
	use crate::test_utils::handle_nom_err;
	use crate::{italic, link, spanned_vec, text};
	use nom::{Finish, Parser};

	#[test]
	fn simple_bold() {
		let s = r"**foo**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo")]);
	}

	#[test]
	fn simple_bold_italic() {
		let s = r"***foo***";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![italic!("foo")]);
	}

	#[test]
	fn escaped_bold() {
		let s = r"**foo\*\*bar\*\*baz**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("foo**bar**baz")]);
	}

	// We allow escaping both underscores (__) at the same time but we do
	// not allow the same for bold's double asterisks.
	#[test]
	fn escape_bold_no_double_bold() {
		let s = r"**\**bar\**baz**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("*"), italic!("bar*"), text!("baz")]);
	}

	#[test]
	fn bold_with_nested_italic_underscore() {
		let s = r"**_bar_baz**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![text!("_bar_baz")]);
	}

	#[test]
	fn bold_with_nested_italic_asterisk() {
		let s = r"***bar*baz**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![italic!("bar"), text!("baz")]);
	}

	#[test]
	fn bold_url() {
		let s = "**https://wnelson.dev**";
		let (rem, res) = bold::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![link!("https://wnelson.dev")]);
	}
}
