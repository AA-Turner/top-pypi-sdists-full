/// Identifies a node within one parse: unique, though neither consecutive nor in document order.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(transparent)
)]
pub struct Id(pub u32);

impl Id {
	/// The `n`th id of the block starting at this one.
	#[must_use]
	pub fn nth(self, n: usize) -> Self {
		Self(self.0.saturating_add(u32::try_from(n).unwrap_or(u32::MAX)))
	}
}

/// Hands out the [`Id`]s of one parse.
#[derive(Debug, Default)]
pub struct Ids {
	next: Id,
}

impl Ids {
	/// Take a block of `count` ids, returning its first.
	pub fn reserve(&mut self, count: usize) -> Id {
		let first = self.next;
		self.next = first.nth(count);
		first
	}
}
