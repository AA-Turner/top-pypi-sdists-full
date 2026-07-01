use nom::branch::alt;
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

pub const UNDERSCORE_DELIMITER: &str = "_";
pub const ASTERISK_DELIMITER: &str = "*";

/// Unparse italic content back to markdown.
///
/// # Errors
/// If formatting fails
// TODO: Retain which delimiter was used in the AST (underscore vs asterisk) and use it here.
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(
		f,
		"{}{}{}",
		UNDERSCORE_DELIMITER,
		content.unparse(),
		UNDERSCORE_DELIMITER
	)
}

/// Parse italic.
///
/// # Errors
/// If the content does not begin with italics.
#[must_use]
pub fn italic<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	nom::error::context(
		"italic",
		alt((
			delimited(
				tag(UNDERSCORE_DELIMITER),
				inline::inline(context.clone().with_grammar(Grammar::UnderscoreItalic)),
				tag(UNDERSCORE_DELIMITER),
			),
			delimited(
				tag(ASTERISK_DELIMITER),
				inline::inline(context.with_grammar(Grammar::AsteriskItalic)),
				tag(ASTERISK_DELIMITER),
			),
		)),
	)
}

// _bar_baz_ -> <i>bar_baz</i>
// _bar_ -> <i>bar</i>
// _foo_bar_baz_cat_ -> <i>foo_bar_baz_cat</i>
// _foo\_bar_ -> <i>foo_bar</i>
//
// _foo t_a **bat** butt_

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::italic;
	use crate::context::Context;
	use crate::test_utils::handle_nom_err;
	use crate::{link, spanned_vec, text};

	#[test]
	fn simple_italic() {
		let s = r"_foo_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo")]);
	}

	#[test]
	fn simple_italic_asterisk() {
		let s = r"*foo*";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo")]);
	}

	#[test]
	fn complex_italic() {
		let s = r"_foo_bar_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo_bar")]);
	}

	#[test]
	fn complexer_italic() {
		let s = r"_foo_bar_baz_cat_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo_bar_baz_cat")]);
	}

	#[test]
	fn complexest_italic() {
		let s = r"_foo_ba\\r_baz_cat_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!(r"foo_ba\r_baz_cat")]);
	}

	#[test]
	fn italic_paren() {
		let s = r"_https://en.wikipedia.org/wiki/Endemic_(epidemiology)_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(
			res,
			spanned_vec![link!(
				"https://en.wikipedia.org/wiki/Endemic_(epidemiology)"
			)]
		);
	}

	#[test]
	fn escaped_italic() {
		let s = r"_foo\_bar_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo_bar")]);
	}

	#[test]
	fn italic_with_new_line() {
		let s = "_foo\nbar_";
		let (rem, res) = italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo\nbar")]);
	}
}
