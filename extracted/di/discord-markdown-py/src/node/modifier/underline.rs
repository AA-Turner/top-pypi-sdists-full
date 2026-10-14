//! Underline.

use crate::node::SpannedNodes;
use crate::span::Span;
use crate::unparse::Unparse;

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

#[cfg(test)]
mod test {
	use crate::test_utils::inline_content;
	use crate::{spanned_vec, underline};

	#[test]
	fn simple_underline() {
		assert_eq!(inline_content("__foo__"), spanned_vec![underline!("foo")]);
	}

	#[test]
	fn simple_underline_but_double() {
		assert_eq!(
			inline_content(r"__foo\__bar\__baz__"),
			spanned_vec![underline!("foo__bar__baz")]
		);
	}

	#[test]
	fn escaped_underline() {
		assert_eq!(
			inline_content(r"__foo\_\_bar\_\_baz__"),
			spanned_vec![underline!("foo__bar__baz")]
		);
	}
}
