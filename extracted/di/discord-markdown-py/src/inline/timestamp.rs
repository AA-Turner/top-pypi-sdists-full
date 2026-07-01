use nom::{
	bytes::complete::tag,
	character::complete::{char, one_of, u64},
	combinator::{map, opt},
	error::ParseError,
	sequence::{delimited, pair, preceded},
	Parser,
};
use style::{Style, STYLE_CHARS};

pub mod style;

use crate::{unparse::Unparse, Input};

pub const OPEN_DELIMITER: &str = "<t:";
pub const CLOSE_DELIMITER: &str = ">";

/// A timestamp.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Timestamp {
	pub value: u64,
	pub style: Option<Style>,
}

impl Unparse for Timestamp {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self.style {
			Some(style) => write!(
				f,
				"{}{}:{}{}",
				OPEN_DELIMITER, self.value, style, CLOSE_DELIMITER
			),
			None => write!(f, "{}{}{}", OPEN_DELIMITER, self.value, CLOSE_DELIMITER),
		}
	}
}

/// Parse a timestamp.
///
/// # Errors
/// If the content does not begin with a timestamp.
///
/// # Panics
/// If [`STYLE_CHARS`] doesn't match [`Style`]
pub fn timestamp<'data, E>() -> impl Parser<Input<'data>, Output = Timestamp, Error = E>
where
	E: ParseError<Input<'data>>,
{
	map(
		delimited(
			tag(OPEN_DELIMITER),
			pair(
				u64,
				opt(preceded(
					char(':'),
					map(one_of(STYLE_CHARS), |ch| ch.try_into().unwrap()),
				)),
			),
			tag(CLOSE_DELIMITER),
		),
		|(value, style)| Timestamp { value, style },
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{inline::timestamp::Style, test_utils::handle_nom_err};

	use super::{timestamp, Timestamp};

	#[test]
	fn simple_timestamp() {
		let s = r"<t:1234>";
		let (rem, res) = timestamp()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Timestamp {
				value: 1234,
				style: None
			}
		);
	}

	#[test]
	fn styled_timestamp() {
		let s = r"<t:1234:d>";
		let (rem, res) = timestamp()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Timestamp {
				value: 1234,
				style: Some(Style::ShortDate)
			}
		);
	}

	#[test]
	fn not_timestamp() {
		let s = r"<a:12345>";
		timestamp()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("unable to parse");
	}
}
