use std::{fmt::Display, str::FromStr};

pub const STYLE_CHARS: &str = "tTdDfFR";

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
	serde(into = "String", try_from = "&str")
)]
pub enum Style {
	ShortTime,
	LongTime,
	ShortDate,
	LongDate,
	ShortDateTime,
	LongDateTime,
	Relative,
}

impl Display for Style {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str(match self {
			Self::LongDate => "D",
			Self::LongDateTime => "F",
			Self::LongTime => "T",
			Self::Relative => "R",
			Self::ShortDate => "d",
			Self::ShortDateTime => "f",
			Self::ShortTime => "t",
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
			'T' => Self::LongTime,
			'd' => Self::ShortDate,
			'D' => Self::LongDate,
			'f' => Self::ShortDateTime,
			'F' => Self::LongDateTime,
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
