use std::borrow::Cow;

use crate::{Input, error::PResult};

pub const OPEN_DELIMITER: &str = "<";
pub const CLOSE_DELIMITER: &str = ">";

/// A custom emoji.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Custom<'data> {
	pub animated: bool,
	pub name: Cow<'data, str>,
	pub id: u64,
}

/// Parse a custom emoji.
///
/// # Errors
/// If the content does not begin with a custom emoji.
pub fn parse<'data>(input: &mut Input<'data>) -> PResult<Custom<'data>> {
	input.tag(OPEN_DELIMITER)?;
	let animated = input.eat("a");
	input.char(':')?;
	let name = input.take_while1(|ch| ch.is_ascii_alphanumeric() || ch == '_')?;
	input.char(':')?;
	let id = input.u64()?;
	input.tag(CLOSE_DELIMITER)?;

	Ok(Custom {
		animated,
		name: Cow::Borrowed(name),
		id,
	})
}
