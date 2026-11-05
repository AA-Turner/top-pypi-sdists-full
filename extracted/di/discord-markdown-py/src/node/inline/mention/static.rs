use std::fmt::Display;

use crate::{Input, error::PResult};

pub const PREFIX: &str = "<id:";
pub const SUFFIX: char = '>';

pub struct StaticFromStrError;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum Static {
	Home,
	Browse,
	Customize,
	Guide,
	LinkedRoles(Option<u64>),
}

impl Display for Static {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		match self {
			Self::Home => f.write_str("home"),
			Self::Browse => f.write_str("browse"),
			Self::Customize => f.write_str("customize"),
			Self::Guide => f.write_str("guide"),
			Self::LinkedRoles(id) => {
				f.write_str("linked-roles")?;
				if let Some(id) = id {
					write!(f, ":{id}")?;
				}

				Ok(())
			}
		}
	}
}

/// Parse a static mention.
///
/// # Errors
/// If the content does not begin with a static mention.
pub fn parse(input: &mut Input) -> PResult<Static> {
	input.tag(PREFIX)?;
	let named = [
		("home", Static::Home),
		("browse", Static::Browse),
		("customize", Static::Customize),
		("guide", Static::Guide),
	]
	.into_iter()
	.find_map(|(name, mention)| input.eat(name).then_some(mention));
	let mention = if let Some(mention) = named {
		mention
	} else {
		input.tag("linked-roles")?;
		let id = input.attempt(|input| {
			input.char(':')?;
			input.u64()
		})?;
		Static::LinkedRoles(id)
	};
	input.char(SUFFIX)?;
	Ok(mention)
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::{Static, parse};

	#[test]
	fn basic() {
		let (rem, res) = run("<id:home>", parse).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::Home);
	}

	#[test]
	fn linked_roles_empty() {
		let (rem, res) = run("<id:linked-roles>", parse).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::LinkedRoles(None));
	}

	#[test]
	fn linked_roles_value() {
		let (rem, res) = run("<id:linked-roles:1234>", parse).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::LinkedRoles(Some(1234)));
	}
}
