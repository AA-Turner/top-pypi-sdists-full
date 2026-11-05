use std::{cell::Cell, fmt::Display, rc::Rc};

/// Indicates that a parse exhausted its [`Fuel`].
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

	/// As [`Self::consume`], as an error a parser can `?`.
	///
	/// # Errors
	/// If the tank is empty.
	pub fn spend(&self) -> Result<(), OutOfFuel> {
		if self.consume() {
			Ok(())
		} else {
			Err(OutOfFuel)
		}
	}
}

/// Compares the units left in the tank.
impl PartialEq<u32> for Fuel {
	fn eq(&self, other: &u32) -> bool {
		self.0.get().eq(other)
	}
}

#[cfg(test)]
mod test {
	use super::{Fuel, OutOfFuel};
	use crate::Input;

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
		let mut input = Input::from("a");

		let result = input.attempt(|input| {
			fuel.spend()?;
			input.tag("b")
		});
		assert_eq!(result, Ok(None));
		assert_eq!(fuel, 1);

		let result = input.attempt(|input| {
			fuel.spend()?;
			input.tag("a")
		});
		assert_eq!(result, Ok(Some("a")));
		assert_eq!(fuel, 0);
	}

	/// An empty tank is not a mismatch, so an alternative cannot retry past it.
	#[test]
	fn exhaustion_is_not_recoverable() {
		let fuel = Fuel::new(0);

		let mut input = Input::from("a");
		let result = input.attempt(|input| {
			fuel.spend()?;
			input.tag("a")
		});
		assert_eq!(result, Err(OutOfFuel));
	}
}
