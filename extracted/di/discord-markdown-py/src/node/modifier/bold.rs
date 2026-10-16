//! Bold.

use crate::node::Inlines;
use crate::span::Span;
use crate::unparse::Unparse;

pub const DELIMITER: &str = "**";

/// Unparse bold content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(content: &Inlines<S>, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

#[cfg(test)]
mod test {
	use crate::test_utils::inline_content;
	use crate::{bold, italic, link, spanned_vec, text};

	#[test]
	fn simple_bold() {
		assert_eq!(inline_content("**foo**"), spanned_vec![bold!("foo")]);
	}

	#[test]
	fn simple_bold_italic() {
		assert_eq!(
			inline_content("***foo***"),
			spanned_vec![bold!(italic!("foo"))]
		);
	}

	#[test]
	fn escaped_bold() {
		assert_eq!(
			inline_content(r"**foo\*\*bar\*\*baz**"),
			spanned_vec![bold!("foo**bar**baz")]
		);
	}

	// We allow escaping both underscores (__) at the same time but we do
	// not allow the same for bold's double asterisks.
	#[test]
	fn escape_bold_no_double_bold() {
		assert_eq!(
			inline_content(r"**\**bar\**baz**"),
			spanned_vec![bold!(text!("*"), italic!("bar*"), text!("baz"))]
		);
	}

	#[test]
	fn bold_with_nested_italic_underscore() {
		assert_eq!(
			inline_content("**_bar_baz**"),
			spanned_vec![bold!("_bar_baz")]
		);
	}

	#[test]
	fn bold_with_nested_italic_asterisk() {
		assert_eq!(
			inline_content("***bar*baz**"),
			spanned_vec![bold!(italic!("bar"), text!("baz"))]
		);
	}

	#[test]
	fn bold_url() {
		assert_eq!(
			inline_content("**https://wnelson.dev**"),
			spanned_vec![bold!(link!("https://wnelson.dev"))]
		);
	}
}
