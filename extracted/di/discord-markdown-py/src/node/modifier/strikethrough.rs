//! Strikethrough.

use crate::node::Inlines;
use crate::span::Span;
use crate::unparse::Unparse;

pub const DELIMITER: &str = "~~";

/// Unparse strikethrough content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(content: &Inlines<S>, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

#[cfg(test)]
mod test {
	use crate::test_utils::inline_content;
	use crate::{spanned_vec, strikethrough};

	#[test]
	fn simple_strikethrough() {
		assert_eq!(
			inline_content("~~foo~~"),
			spanned_vec![strikethrough!("foo")]
		);
	}

	#[test]
	fn escaped_strikethrough() {
		assert_eq!(
			inline_content(r"~~foo\~\~bar\~\~baz~~"),
			spanned_vec![strikethrough!("foo~~bar~~baz")]
		);
	}
}
