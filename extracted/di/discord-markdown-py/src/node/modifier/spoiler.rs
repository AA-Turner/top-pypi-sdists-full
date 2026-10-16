//! Spoiler.

use derive_where::derive_where;

use crate::{
	node::{Id, Inlines},
	span::Span,
	unparse::Unparse,
};

pub const DELIMITER: &str = "||";

/// A spoiler element.
#[derive_where(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound = "")
)]
pub struct Spoiler<'data, S: Span> {
	/// A spoiler split across blocks -- as `||1. foo\n2. ba||r` splits into one in each item -- is
	/// one spoiler in fragments, which share their id so that they can be revealed together.
	pub id: Id,
	pub content: Inlines<'data, S>,
}

/// Unparse spoiler content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(content: &Inlines<S>, f: &mut std::fmt::Formatter) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

#[cfg(test)]
mod test {
	use crate::{spanned_vec, spoiler, test_utils::inline_content};

	#[test]
	fn simple_spoiler() {
		assert_eq!(
			inline_content("||foo bar||"),
			spanned_vec![spoiler!("foo bar")]
		);
	}

	#[test]
	fn escaped_spoiler() {
		assert_eq!(
			inline_content(r"||foo\|\|bar||"),
			spanned_vec![spoiler!("foo||bar")]
		);
	}

	#[test]
	fn allow_unescaped_single_pipes() {
		assert_eq!(
			inline_content("||foo|bar|banana||"),
			spanned_vec![spoiler!("foo|bar|banana")]
		);
	}
}
