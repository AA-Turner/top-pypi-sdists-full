use std::fmt::Display;

use crate::context::fuel::OutOfFuel;

/// Why a parser did not produce anything.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Fail {
	/// The input is not what this parser reads. Another alternative may be tried in its place.
	NoMatch,
	/// The parse exhausted its fuel. This ends the whole parse: no alternative may be tried, or the
	/// budget would not bound anything.
	OutOfFuel,
}

impl From<OutOfFuel> for Fail {
	fn from(OutOfFuel: OutOfFuel) -> Self {
		Self::OutOfFuel
	}
}

/// The result of a parser.
pub type PResult<T> = Result<T, Fail>;

/// A failed parse.
///
/// Running out of fuel is the one failure a caller can act on — by raising the budget, or by
/// rejecting the content as adversarial — so it is kept apart from the rest.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
	/// The parse exhausted its fuel. See [`crate::context::Options::fuel`].
	///
	/// This carries no position: the parser stops wherever the budget happens to run dry, which
	/// says nothing about the input.
	OutOfFuel,
	/// The parser stopped short of the end of the input, at this byte offset. Every input is
	/// markdown, so this is a bug in the parser.
	Parse { offset: usize },
}

impl Error {
	/// Whether this failure is the fuel limit rather than a problem with the content.
	#[must_use]
	pub fn is_out_of_fuel(&self) -> bool {
		matches!(self, Self::OutOfFuel)
	}
}

impl Display for Error {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		match self {
			Self::OutOfFuel => Display::fmt(&OutOfFuel, f),
			Self::Parse { offset } => write!(f, "parser stopped at byte {offset}"),
		}
	}
}

impl std::error::Error for Error {}
