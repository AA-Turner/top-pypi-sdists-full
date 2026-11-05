//! Strikethrough.

pub const DELIMITER: &str = "~~";

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
