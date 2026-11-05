//! Emoji parsing.

use std::borrow::Cow;

use custom::Custom;

use crate::{Input, error::PResult};

pub mod colon_delimited;
/// Custom emoji parsing.
pub mod custom;
pub mod unicode;

/// An emoji element.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum Emoji<'data> {
	// A custom emoji.
	Custom(Custom<'data>),
	/// Probably a Unicode emoji.
	Unicode(Cow<'data, str>),
}

/// Parse an emoji.
///
/// # Errors
/// If the content does not begin with an emoji.
pub fn parse<'data>(input: &mut Input<'data>) -> PResult<Emoji<'data>> {
	match input.attempt(custom::parse)? {
		Some(custom) => Ok(Emoji::Custom(custom)),
		None => parse_unicode(input),
	}
}

/// Like [`parse`] but skips the custom emoji path. Used when the `>` byte is known to be
/// absent from the remaining input, making custom emoji impossible.
///
/// # Errors
/// If the content does not start with a unicode or colon-delimited unicode emoji
pub fn parse_unicode<'data>(input: &mut Input<'data>) -> PResult<Emoji<'data>> {
	let emoji = match input.attempt(colon_delimited::emoji)? {
		Some(emoji) => emoji,
		None => unicode::emoji(input)?,
	};
	Ok(Emoji::Unicode(Cow::Borrowed(emoji)))
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::{Custom, Emoji, parse};

	#[test]
	fn simple_emoji() {
		let s = r"<:abcd:1234>";
		let (rem, res) = run(s, parse).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Emoji::Custom(Custom {
				animated: false,
				name: "abcd".into(),
				id: 1234
			})
		);
	}

	#[test]
	fn emoji_with_more_chars() {
		let s = r"<:abcd_efgh1234:1234>";
		let (rem, res) = run(s, parse).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Emoji::Custom(Custom {
				animated: false,
				name: "abcd_efgh1234".into(),
				id: 1234
			})
		);
	}

	#[test]
	fn animated_emoji() {
		let s = r"<a:abcd:1234>";
		let (rem, res) = run(s, parse).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Emoji::Custom(Custom {
				animated: true,
				name: "abcd".into(),
				id: 1234
			})
		);
	}

	#[test]
	fn not_emoji() {
		let s = r"<t:12345>";
		run(s, parse).expect_err("unable to parse");
	}

	#[test]
	fn basic_colon_delimited() {
		let s = ":foot:";
		let (rem, res) = run(s, parse).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Emoji::Unicode("🦶".into()));
	}
}
