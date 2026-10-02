use std::fmt::Display;

use nom::{
	branch::alt,
	bytes::complete::tag,
	character::complete::{char, u64},
	combinator::{map, opt, value},
	sequence::{delimited, preceded},
	Parser,
};

use crate::{error::ParseError, unparse::Unparse, Input};

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

impl Unparse for Static {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		write!(f, "{PREFIX}{self}{SUFFIX}")
	}
}

#[must_use]
pub fn parser<'data, E>() -> impl Parser<Input<'data>, Output = Static, Error = E>
where
	E: ParseError<'data>,
{
	delimited(
		tag(PREFIX),
		alt((
			value(Static::Home, tag("home")),
			value(Static::Browse, tag("browse")),
			value(Static::Customize, tag("customize")),
			value(Static::Guide, tag("guide")),
			map(
				preceded(tag("linked-roles"), opt(preceded(char(':'), u64))),
				Static::LinkedRoles,
			),
		)),
		char(SUFFIX),
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

	use super::{parser, Static};

	#[test]
	fn basic() {
		let (rem, res) = parser()
			.parse("<id:home>".into())
			.finish()
			.map_err(handle_nom_err("<id:home>"))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::Home);
	}

	#[test]
	fn linked_roles_empty() {
		let (rem, res) = parser()
			.parse("<id:linked-roles>".into())
			.finish()
			.map_err(handle_nom_err("<id:linked-roles>"))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::LinkedRoles(None));
	}

	#[test]
	fn linked_roles_value() {
		let (rem, res) = parser()
			.parse("<id:linked-roles:1234>".into())
			.finish()
			.map_err(handle_nom_err("<id:linked-roles:1234>"))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, Static::LinkedRoles(Some(1234)));
	}
}
