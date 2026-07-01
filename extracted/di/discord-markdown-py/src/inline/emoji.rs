use std::borrow::Cow;

use custom::Custom;
use nom::{branch::alt, combinator::map, error::ParseError, IResult, Parser};

use crate::{unparse::Unparse, Input};

pub mod colon_delimited;
/// Custom emoji parsing.
pub mod custom;
/// Unicode emoji parsing.
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

impl Unparse for Emoji<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self::Custom(custom) => Unparse::fmt(custom, f),
			Self::Unicode(value) => f.write_str(value),
		}
	}
}

/// Parse an emoji.
///
/// # Errors
/// If the content does not begin with an emoji.
pub fn parse<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Emoji<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	alt((map(custom::parse, Emoji::Custom), parse_unicode)).parse_complete(data)
}

/// Like [`parse`] but skips the custom emoji path. Used when the `>` byte is known to be
/// absent from the remaining input, making custom emoji impossible.
///
/// # Errors
/// If the content does not start with a unicode or colon-delimited unicode emoji
pub fn parse_unicode<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Emoji<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	map(
		alt((
			#[allow(
				clippy::redundant_closure,
				reason = "This causes compilation errors when removed"
			)]
			colon_delimited::emoji().map(|emoji| Cow::Borrowed(emoji)),
			unicode::emoji().map(|emoji| emoji.content),
		)),
		Emoji::Unicode,
	)
	.parse_complete(data)
}

#[cfg(test)]
mod test {
	use nom::Finish;

	use crate::test_utils::handle_nom_err;

	use super::{parse, Custom, Emoji};

	#[test]
	fn simple_emoji() {
		let s = r"<:abcd:1234>";
		let (rem, res) = parse(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, res) = parse(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		let (rem, res) = parse(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
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
		parse(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("unable to parse");
	}

	#[test]
	fn basic_colon_delimited() {
		let s = ":foot:";
		let (rem, res) = parse(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Emoji::Unicode("🦶".into()));
	}
}
