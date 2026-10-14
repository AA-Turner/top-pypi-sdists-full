use std::{cell::Cell, fmt::Display, marker::PhantomData, rc::Rc};

use nom::Parser;

use crate::{Input, error::ParseError};

/// Indicates that a parse exhausted its [`Fuel`].
///
/// This is the external error the parser reports through
/// [`FromExternalError`](nom::error::FromExternalError) when the tank runs dry. It is what an
/// error type receives, not what a caller gets back:
/// [`Error::OutOfFuel`](crate::error::Error::OutOfFuel) is the variant that survives to
/// [`crate::parse`]'s return value.
///
/// See [`crate::context::Options::fuel`] for what fuel is and how to budget it.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct OutOfFuel;

impl OutOfFuel {
	/// This as the error `E` reports at `input`. Raise it as a [`nom::Err::Failure`], so that it
	/// aborts the parse instead of being swallowed by an `alt` that would retry against an empty
	/// tank. The [`ErrorKind`](nom::error::ErrorKind) is only what nom's signature demands.
	#[must_use]
	pub fn error<'data, E: ParseError<'data>>(input: Input<'data>) -> E {
		E::from_external_error(input, nom::error::ErrorKind::Fail, Self)
	}
}

impl Display for OutOfFuel {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str("parser ran out of fuel")
	}
}

impl std::error::Error for OutOfFuel {}

/// A tank of work units that parsers draw down, bounding how much work they can do in total.
///
/// Clones are handles to the same tank, so a budget handed to nested parsers cannot be multiplied.
/// The tank is not thread-safe; it is meant to be shared within one single-threaded parse.
///
/// Comparisons look at the units remaining, not at whether two handles share a tank.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Fuel(Rc<Cell<u32>>);

impl Fuel {
	/// Create a tank holding `amount` units.
	#[must_use]
	pub fn new(amount: u32) -> Self {
		Self(Rc::new(Cell::new(amount)))
	}

	/// The units left in the tank.
	#[must_use]
	pub fn get(&self) -> u32 {
		self.0.get()
	}

	/// Spend one unit, returning `false` and spending nothing if the tank is empty.
	#[must_use]
	pub fn consume(&self) -> bool {
		match self.0.get() {
			0 => false,
			remaining => {
				self.0.set(remaining - 1);
				true
			}
		}
	}

	/// Wrap `parser` so that every invocation spends one unit first, whether or not `parser` then
	/// matches.
	///
	/// Once the tank is empty, the wrapper fails with [`OutOfFuel`] without running `parser`. The
	/// failure is a [`nom::Err::Failure`], so combinators like `alt` give up rather than trying
	/// another branch.
	pub fn consume_parser<P, E>(&self, parser: P) -> FuelParser<'_, P, E> {
		FuelParser {
			fuel: self,
			parser,
			error: PhantomData,
		}
	}
}

/// Compares the units left in the tank.
impl PartialEq<u32> for Fuel {
	fn eq(&self, other: &u32) -> bool {
		self.0.get().eq(other)
	}
}

/// A parser that spends [`Fuel`] on every invocation; see [`Fuel::consume_parser`].
pub struct FuelParser<'fuel, P, E> {
	fuel: &'fuel Fuel,
	parser: P,
	error: PhantomData<E>,
}

impl<'data, P, E> Parser<Input<'data>> for FuelParser<'_, P, E>
where
	P: Parser<Input<'data>, Error = E>,
	E: ParseError<'data>,
{
	type Output = P::Output;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		if !self.fuel.consume() {
			return Err(nom::Err::Failure(OutOfFuel::error(input)));
		}

		self.parser.process::<OM>(input)
	}
}

/// Method syntax for [`Fuel::consume_parser`], implemented for every parser.
pub trait ApplyFuel<'fuel> {
	/// The metered parser.
	type Output<E>;

	/// Spend a unit of `fuel` on every invocation of this parser; see [`Fuel::consume_parser`].
	#[must_use]
	fn apply_fuel<E>(self, fuel: &'fuel Fuel) -> Self::Output<E>;
}

impl<'fuel, 'data, P> ApplyFuel<'fuel> for P
where
	P: Parser<Input<'data>>,
{
	type Output<E> = FuelParser<'fuel, Self, E>;

	fn apply_fuel<E>(self, fuel: &'fuel Fuel) -> Self::Output<E> {
		fuel.consume_parser(self)
	}
}

#[cfg(test)]
mod test {
	use nom::{Parser, branch::alt, bytes::complete::tag};

	use super::{ApplyFuel, Fuel};
	use crate::error::Error;

	#[test]
	fn consume_stops_at_empty() {
		let fuel = Fuel::new(2);

		assert!(fuel.consume());
		assert!(fuel.consume());
		assert_eq!(fuel, 0);
		assert!(!fuel.consume());
		assert_eq!(fuel, 0);
	}

	/// Clones are one tank, so handing a copy to a nested parser cannot mint more.
	#[test]
	fn clones_share_one_tank() {
		let fuel = Fuel::new(3);
		let clones = [fuel.clone(), fuel.clone(), fuel.clone()];

		for clone in &clones {
			assert!(clone.consume());
			assert_eq!(&fuel, clone);
		}

		assert_eq!(fuel, 0);
		assert!(clones.iter().all(|clone| !clone.consume()));
	}

	/// A parse costs a unit whether it matches or not, so abandoned branches still pay.
	#[test]
	fn every_parse_costs_a_unit() {
		let fuel = Fuel::new(2);

		tag::<_, _, Error<'_>>("a")
			.apply_fuel(&fuel)
			.parse_complete("a".into())
			.expect("a matches");
		assert_eq!(fuel, 1);

		tag::<_, _, Error<'_>>("b")
			.apply_fuel(&fuel)
			.parse_complete("a".into())
			.expect_err("b does not match a");
		assert_eq!(fuel, 0);
	}

	/// An empty tank is a failure rather than an error, so an `alt` cannot retry past it.
	#[test]
	fn exhaustion_is_not_recoverable() {
		let fuel = Fuel::new(0);

		let err = alt((tag("a").apply_fuel(&fuel), tag("a")))
			.parse_complete("a".into())
			.expect_err("the fallback branch must not run");
		assert_eq!(err, nom::Err::Failure(Error::OutOfFuel));
	}
}
