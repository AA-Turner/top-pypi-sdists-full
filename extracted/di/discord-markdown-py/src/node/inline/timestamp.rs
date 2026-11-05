//! Timestamp parsing.

use style::{STYLE_CHARS, Style};

pub mod style;

use crate::{Input, error::PResult};

pub const OPEN_DELIMITER: &str = "<t:";
pub const CLOSE_DELIMITER: &str = ">";

/// A timestamp.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Timestamp {
	pub value: i64,
	pub style: Option<Style>,
}

/// Parse a timestamp.
///
/// # Errors
/// If the content does not begin with a timestamp.
///
/// # Panics
/// If [`STYLE_CHARS`] doesn't match [`Style`]
pub fn timestamp(input: &mut Input) -> PResult<Timestamp> {
	input.tag(OPEN_DELIMITER)?;
	let value = input.i64()?;
	let style = input.attempt(|input| {
		input.char(':')?;
		let style = input.satisfy(|ch| STYLE_CHARS.contains(ch))?;
		Ok(style.try_into().unwrap())
	})?;
	input.tag(CLOSE_DELIMITER)?;
	Ok(Timestamp { value, style })
}

#[cfg(test)]
mod test {
	use crate::{node::inline::timestamp::Style, test_utils::run};

	use super::{Timestamp, timestamp};

	#[test]
	fn simple_timestamp() {
		let s = r"<t:1234>";
		let (rem, res) = run(s, timestamp).expect("unable to parse");
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
		let (rem, res) = run(s, timestamp).expect("unable to parse");
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
		run(s, timestamp).expect_err("unable to parse");
	}
}
