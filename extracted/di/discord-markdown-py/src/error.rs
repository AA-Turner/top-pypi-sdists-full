use std::{fmt::Display, num::TryFromIntError};

use crate::Input;

/// Any error used in the parser must implement this trait.
///
/// This is simply an extension of several `nom` error traits, combined for convenience.
///
/// The [`FromExternalError`] bounds are how the parser hands an implementor information `nom`'s
/// own combinators cannot carry — most importantly [`OutOfFuel`]. An implementor is free to
/// discard any of it, as [`nom::error::Error`] does, but then it cannot report it either: pick
/// [`Error`] if the caller needs to tell running out of fuel apart from an ordinary parse failure.
///
/// [`FromExternalError`]: nom::error::FromExternalError
pub trait ParseError<'data>:
	nom::error::ParseError<Input<'data>>
	+ nom::error::ContextError<Input<'data>>
	+ nom::error::FromExternalError<Input<'data>, url::ParseError>
	+ nom::error::FromExternalError<Input<'data>, OutOfFuel>
	+ nom::error::FromExternalError<Input<'data>, TryFromIntError>
{
}

impl ParseError<'_> for () {}

#[cfg(test)]
impl<'data> ParseError<'data> for nom_language::error::VerboseError<Input<'data>> {}

/// Keeps only an [`ErrorKind`](nom::error::ErrorKind), so every external error the parser reports
/// — including [`OutOfFuel`] — collapses into an indistinguishable failure. Cheap, and fine when
/// the caller only needs to know that parsing did not succeed.
impl<'data> ParseError<'data> for nom::error::Error<Input<'data>> {}

/// Indicates that a parse exhausted the fuel it was given.
///
/// This is the external error the parser reports through
/// [`FromExternalError`](nom::error::FromExternalError) when the tank runs dry. It is what an
/// error type receives, not what a caller gets back: [`Error::OutOfFuel`] is the variant that
/// survives to [`crate::parse`]'s return value.
///
/// See [`crate::context::Options::fuel`] for what fuel is and how to budget it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutOfFuel;

impl Display for OutOfFuel {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str("parser ran out of fuel")
	}
}

impl std::error::Error for OutOfFuel {}

/// A parse failure that remembers whether the parse ran out of fuel.
///
/// [`crate::parse`] is generic over its error type, and the cheapest choices throw away everything
/// but the position a parser gave up at. Running out of fuel is the one failure a caller can
/// actually act on — by raising the budget, or by rejecting the content as adversarial — so it
/// needs an error type that keeps it. This is that type, and it is what the language bindings use.
///
/// It records nothing beyond what [`nom::error::Error`] does otherwise, so it costs a discriminant
/// over the cheap choice.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error<'data> {
	/// The parse exhausted its fuel. See [`crate::context::Options::fuel`].
	///
	/// This carries no position: the parser stops wherever the budget happens to run dry, which
	/// says nothing about the input.
	OutOfFuel,
	/// An ordinary parse failure.
	Parse(nom::error::Error<Input<'data>>),
}

impl Error<'_> {
	/// Whether this failure is the fuel limit rather than a problem with the content.
	#[must_use]
	pub fn is_out_of_fuel(&self) -> bool {
		matches!(self, Self::OutOfFuel)
	}
}

impl<'data> nom::error::ParseError<Input<'data>> for Error<'data> {
	fn from_error_kind(input: Input<'data>, kind: nom::error::ErrorKind) -> Self {
		Self::Parse(nom::error::Error::from_error_kind(input, kind))
	}

	fn append(input: Input<'data>, kind: nom::error::ErrorKind, other: Self) -> Self {
		match other {
			// Running out of fuel ends the parse, so there is no surrounding context that could
			// explain it better. Anything layered on top would only bury it.
			Self::OutOfFuel => Self::OutOfFuel,
			Self::Parse(error) => Self::Parse(nom::error::Error::append(input, kind, error)),
		}
	}

	fn or(self, other: Self) -> Self {
		// `nom` short-circuits on the `Failure` that carries an empty tank, so this is belt and
		// braces — but a branch that ran out of fuel must not be discarded in favour of one that
		// merely failed to match.
		match (self, other) {
			(Self::OutOfFuel, _) | (_, Self::OutOfFuel) => Self::OutOfFuel,
			(_, other) => other,
		}
	}
}

// `nom`'s own default is to return `other` unchanged, which already preserves the fuel variant.
impl<'data> nom::error::ContextError<Input<'data>> for Error<'data> {}

impl<'data> nom::error::FromExternalError<Input<'data>, OutOfFuel> for Error<'data> {
	fn from_external_error(
		_input: Input<'data>,
		_kind: nom::error::ErrorKind,
		_error: OutOfFuel,
	) -> Self {
		Self::OutOfFuel
	}
}

/// Implements [`FromExternalError`](nom::error::FromExternalError) for the errors that carry no
/// information [`Error`] treats specially, deferring to [`nom::error::Error`]'s own handling
/// (which is to keep the position and the [`ErrorKind`](nom::error::ErrorKind)).
macro_rules! impl_from_external_error {
	($($error:ty),* $(,)?) => {
		$(
			impl<'data> nom::error::FromExternalError<Input<'data>, $error> for Error<'data> {
				fn from_external_error(
					input: Input<'data>,
					kind: nom::error::ErrorKind,
					error: $error,
				) -> Self {
					Self::Parse(nom::error::Error::from_external_error(input, kind, error))
				}
			}
		)*
	};
}

impl_from_external_error!(url::ParseError, TryFromIntError);

impl<'data> ParseError<'data> for Error<'data> {}

impl Display for Error<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		match self {
			Self::OutOfFuel => Display::fmt(&OutOfFuel, f),
			Self::Parse(error) => Display::fmt(error, f),
		}
	}
}

impl std::error::Error for Error<'_> {}

#[cfg(test)]
mod test {
	use nom::error::{ContextError, ErrorKind, FromExternalError, ParseError as _};

	use super::{Error, OutOfFuel};
	use crate::Input;

	fn input() -> Input<'static> {
		Input::from("x")
	}

	fn out_of_fuel() -> Error<'static> {
		Error::from_external_error(input(), ErrorKind::Fail, OutOfFuel)
	}

	fn ordinary() -> Error<'static> {
		Error::from_error_kind(input(), ErrorKind::Alt)
	}

	/// The external error the parser reports reaches the caller intact.
	#[test]
	fn out_of_fuel_survives_the_generic_plumbing() {
		let error = out_of_fuel();
		assert!(error.is_out_of_fuel());
		assert_eq!(error.to_string(), "parser ran out of fuel");
	}

	/// The [`ErrorKind`] carries no meaning: a failure built from the very kind the fuel check
	/// passes is still an ordinary failure. Identifying fuel exhaustion by its kind would report
	/// this one as out of fuel.
	#[test]
	fn error_kind_is_not_the_signal() {
		let error = Error::from_error_kind(input(), ErrorKind::Fail);
		assert!(!error.is_out_of_fuel());
		assert!(!ordinary().is_out_of_fuel());
	}

	/// Combinators wrap errors as a failure unwinds. None of that may bury the fuel variant, or
	/// the caller is back to guessing.
	#[test]
	fn out_of_fuel_is_not_buried_by_surrounding_combinators() {
		assert!(Error::append(input(), ErrorKind::Many1, out_of_fuel()).is_out_of_fuel());
		assert!(Error::add_context(input(), "context", out_of_fuel()).is_out_of_fuel());
		assert!(out_of_fuel().or(ordinary()).is_out_of_fuel());
		assert!(ordinary().or(out_of_fuel()).is_out_of_fuel());

		// ...and an ordinary failure is not promoted into one on the way past.
		assert!(!Error::append(input(), ErrorKind::Many1, ordinary()).is_out_of_fuel());
		assert!(!ordinary().or(ordinary()).is_out_of_fuel());
	}
}
