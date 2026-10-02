//! Italic parsing.

use nom::branch::alt;
use nom::bytes::complete::tag;
use nom::character::complete::satisfy;
use nom::combinator::peek;
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
				(
					tag(ASTERISK_DELIMITER),
					// prevents things like `1 * 2 * 3` parsing as italic
					peek(satisfy(|ch| !ch.is_whitespace())),
				),
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
	use crate::{bold, link, spanned_vec, text, underline};

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
	fn asterisk_italic_cannot_start_with_whitespace() {
		let s = r"* foo*";
		italic::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse asterisk italic starting with whitespace");
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

	/// An italic's terminal is one delimiter long, and it is the first half of the two-delimiter
	/// sequence that opens a bold or an underline. It must not close on that -- otherwise it ends
	/// on the opener, the leftover delimiter opens a *second* italic, the two get flattened
	/// together, and the nested node is destroyed outright.
	#[test]
	fn italic_keeps_a_nested_rule_that_shares_its_delimiter() {
		for (s, expected) in [
			(
				r"*foo **bar** baz*",
				spanned_vec![text!("foo "), bold!("bar"), text!(" baz")],
			),
			(
				r"_foo __bar__ baz_",
				spanned_vec![text!("foo "), underline!("bar"), text!(" baz")],
			),
			// two of them, so the italic has to survive re-entering the rule
			(
				r"*foo **bar** baz **qux** end*",
				spanned_vec![
					text!("foo "),
					bold!("bar"),
					text!(" baz "),
					bold!("qux"),
					text!(" end")
				],
			),
			// the bold closes against the italic's own closer, sharing the delimiter run
			(r"*foo **bar***", spanned_vec![text!("foo "), bold!("bar")]),
		] {
			let (rem, res) = italic::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
	}

	/// The terminal only yields to a nested rule that *parses*. Where the longer delimiter cannot
	/// open anything -- nothing closes it, or the run is too long to be an unambiguous opener --
	/// the italic still closes on its own delimiter.
	#[test]
	fn italic_terminal_wins_when_the_nested_rule_cannot_parse() {
		for (s, rest, expected) in [
			// no `**` closes, so the first asterisk is just this italic's closer
			(r"*a**b*", "*b*", spanned_vec![text!("a")]),
			(r"*foo**", "*", spanned_vec![text!("foo")]),
			// a bold cannot open on whitespace either
			(r"*foo ** bar*", "* bar*", spanned_vec![text!("foo ")]),
			(r"_a__", "_", spanned_vec![text!("a")]),
			// three delimiters are ambiguous, and are left to the rules as they always were
			(r"_foo ___", "__", spanned_vec![text!("foo ")]),
		] {
			let (rem, res) = italic::<(), _>(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(rem, rest, "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
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
