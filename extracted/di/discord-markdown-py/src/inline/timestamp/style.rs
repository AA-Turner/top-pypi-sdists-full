//! Styles for timestamps.

use std::{fmt::Display, str::FromStr};

/// All characters that can represent a timestamp style.
pub const STYLE_CHARS: &str = "tTdDfFsSR";

#[derive(Debug)]
pub struct StyleError(String);

impl StyleError {
	fn new(found: impl Display) -> Self {
		Self(format!("expected one of \"{STYLE_CHARS}\", found {found}"))
	}
}

impl Display for StyleError {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str(&self.0)
	}
}

impl std::error::Error for StyleError {}

/// The style of a timestamp.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	// `String` rather than `&str`: the bindings read an AST back without borrowing.
	serde(into = "String", try_from = "String")
)]
pub enum Style {
	/// "t": 16:20
	ShortTime,
	/// "T": 16:20:30
	MediumTime,
	/// "d": 20/04/2021
	ShortDate,
	/// "D": April 20, 2021
	LongDate,
	/// "f": April 20, 2021 at 16:20
	LongDateShortTime,
	/// "F": Tuesday, April 20, 2021 at 16:20
	FullDateShortTime,
	/// "s": 20/04/2021, 16:20
	ShortDateShortTime,
	/// "S": 20/04/2021, 16:20:30
	ShortDateMediumTime,
	/// "R": 4 years ago
	Relative,
}

impl Display for Style {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str(match self {
			Self::LongDate => "D",
			Self::FullDateShortTime => "F",
			Self::MediumTime => "T",
			Self::Relative => "R",
			Self::ShortDate => "d",
			Self::LongDateShortTime => "f",
			Self::ShortTime => "t",
			Self::ShortDateShortTime => "s",
			Self::ShortDateMediumTime => "S",
		})
	}
}

impl From<Style> for String {
	fn from(value: Style) -> Self {
		value.to_string()
	}
}

impl TryFrom<char> for Style {
	type Error = StyleError;

	fn try_from(value: char) -> Result<Self, Self::Error> {
		Ok(match value {
			't' => Self::ShortTime,
			'T' => Self::MediumTime,
			'd' => Self::ShortDate,
			'D' => Self::LongDate,
			'f' => Self::LongDateShortTime,
			'F' => Self::FullDateShortTime,
			's' => Self::ShortDateShortTime,
			'S' => Self::ShortDateMediumTime,
			'R' => Self::Relative,
			other => return Err(StyleError::new(other)),
		})
	}
}

impl FromStr for Style {
	type Err = StyleError;

	fn from_str(s: &str) -> Result<Self, Self::Err> {
		let mut chars = s.chars();

		let result = match chars.next() {
			Some(ch) => ch.try_into(),
			None => Err(StyleError::new("empty string")),
		}?;

		if chars.next().is_some() {
			return Err(StyleError::new(s));
		}

		Ok(result)
	}
}

impl TryFrom<&str> for Style {
	type Error = StyleError;

	fn try_from(value: &str) -> Result<Self, Self::Error> {
		value.parse()
	}
}

impl TryFrom<String> for Style {
	type Error = StyleError;

	fn try_from(value: String) -> Result<Self, Self::Error> {
		value.parse()
	}
}
