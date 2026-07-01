use std::borrow::Cow;

use nom::{
	bytes::{tag, take_while1},
	character::{char, complete::u64},
	combinator::opt,
	error::ParseError,
	sequence::delimited,
	AsChar, IResult, Parser,
};

use crate::{unparse::Unparse, Input};

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

impl Unparse for Custom<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self {
				animated: true,
				name,
				id,
			} => write!(f, "{OPEN_DELIMITER}:a:{name}:{id}{CLOSE_DELIMITER}"),
			Self {
				animated: false,
				name,
				id,
			} => write!(f, "{OPEN_DELIMITER}{name}:{id}{CLOSE_DELIMITER}"),
		}
	}
}

/// Parse a custom emoji.
///
/// # Errors
/// If the content does not begin with a custom emoji.
pub fn parse<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Custom<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		tag(OPEN_DELIMITER),
		(
			opt(char('a')).map(|animated| animated.is_some()),
			char(':'),
			take_while1(|ch: char| ch.is_alphanum() || ch == '_'),
			char(':'),
			u64,
		),
		tag(CLOSE_DELIMITER),
	)
	.map(
		|(animated, _, name, _, id): (bool, char, Input<'data>, char, u64)| Custom {
			animated,
			name: name.content,
			id,
		},
	)
	.parse_complete(data)
}
