//! Italic.

use crate::node::SpannedNodes;
use crate::span::Span;
use crate::unparse::Unparse;

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

#[cfg(test)]
mod test {
	use crate::node::{Element, Node};
	use crate::test_utils::{inline_content, parsed};
	use crate::{bold, italic, link, paragraph, spanned_vec, text, underline};

	#[test]
	fn simple_italic() {
		assert_eq!(inline_content("_foo_"), spanned_vec![italic!("foo")]);
		assert_eq!(inline_content("*foo*"), spanned_vec![italic!("foo")]);
	}

	/// `* foo` would be a list item, so check the asterisk mid-line.
	#[test]
	fn asterisk_italic_cannot_start_with_whitespace() {
		assert_eq!(inline_content("a * foo*"), spanned_vec![text!("a * foo*")]);
	}

	#[test]
	fn underscores_inside_a_word_are_text() {
		for (s, content) in [
			("_foo_bar_", "foo_bar"),
			("_foo_bar_baz_cat_", "foo_bar_baz_cat"),
			(r"_foo_ba\\r_baz_cat_", r"foo_ba\r_baz_cat"),
		] {
			assert_eq!(
				inline_content(s),
				spanned_vec![italic!(Node::Element(Element::Text(content.into())))],
				"unexpected output for {s:?}"
			);
		}
	}

	#[test]
	fn italic_paren() {
		assert_eq!(
			inline_content("_https://en.wikipedia.org/wiki/Endemic_(epidemiology)_"),
			spanned_vec![italic!(link!(
				"https://en.wikipedia.org/wiki/Endemic_(epidemiology)"
			))]
		);
	}

	#[test]
	fn escaped_italic() {
		assert_eq!(
			inline_content(r"_foo\_bar_"),
			spanned_vec![italic!("foo_bar")]
		);
	}

	/// An italic's delimiter is the first half of the one that opens a bold or an underline. The
	/// longer delimiter must open its own rule rather than close the italic, or the nested node is
	/// destroyed.
	#[test]
	fn italic_keeps_a_nested_rule_that_shares_its_delimiter() {
		for (s, expected) in [
			(
				r"*foo **bar** baz*",
				spanned_vec![italic!(text!("foo "), bold!("bar"), text!(" baz"))],
			),
			(
				r"_foo __bar__ baz_",
				spanned_vec![italic!(text!("foo "), underline!("bar"), text!(" baz"))],
			),
			// two of them, so the italic has to survive re-entering the rule
			(
				r"*foo **bar** baz **qux** end*",
				spanned_vec![italic!(
					text!("foo "),
					bold!("bar"),
					text!(" baz "),
					bold!("qux"),
					text!(" end")
				)],
			),
			// the bold closes against the italic's own closer, sharing the delimiter run
			(
				r"*foo **bar***",
				spanned_vec![italic!(text!("foo "), bold!("bar"))],
			),
		] {
			assert_eq!(inline_content(s), expected, "unexpected output for {s:?}");
		}
	}

	/// Where the longer delimiter cannot open anything, it closes the italic instead.
	#[test]
	fn the_longer_delimiter_closes_when_it_cannot_open() {
		for (s, expected) in [
			(r"*a**b*", spanned_vec![italic!("ab")]),
			(r"*foo**", spanned_vec![italic!("foo"), text!("*")]),
			(r"_a__", spanned_vec![italic!("a"), text!("_")]),
		] {
			assert_eq!(inline_content(s), expected, "unexpected output for {s:?}");
		}
	}

	/// Where nothing later could close it, the shorter delimiter closes the italic half of the
	/// longer one.
	#[test]
	fn the_shorter_delimiter_closes_when_nothing_later_can() {
		for (s, expected) in [
			(r"__a_", spanned_vec![text!("_"), italic!("a")]),
			(
				r"x __a_ y",
				spanned_vec![text!("x _"), italic!("a"), text!(" y")],
			),
			(r"**a*", spanned_vec![text!("*"), italic!("a")]),
		] {
			assert_eq!(inline_content(s), expected, "unexpected output for {s:?}");
		}
	}

	/// Each line is its own paragraph, and an italic spanning two of them wraps both.
	#[test]
	fn italic_with_new_line() {
		assert_eq!(
			parsed("_foo\nbar_"),
			spanned_vec![italic!(paragraph!("foo"), paragraph!("bar"))]
		);
	}
}
