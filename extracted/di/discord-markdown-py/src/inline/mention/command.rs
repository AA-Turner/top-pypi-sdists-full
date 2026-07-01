use std::marker::PhantomData;

use icu_properties::{props::Script, script::ScriptWithExtensions};
use nom::{
	bytes::tag,
	character::{
		char,
		complete::{anychar, u64},
	},
	combinator::{opt, recognize, verify},
	error::ParseError,
	multi::fold_many_m_n,
	sequence::{delimited, separated_pair},
	IResult, Parser,
};

use crate::{inline::mention::CLOSE_DELIMITER, unparse::Unparse, Input};

pub const OPEN_DELIMITER: &str = "</";

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Command {
	pub name: String,
	pub id: u64,
}

impl Unparse for Command {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		write!(
			f,
			"{}{}:{}{}",
			OPEN_DELIMITER, self.name, self.id, CLOSE_DELIMITER
		)
	}
}

#[must_use]
pub fn command<'data, E>() -> impl Parser<Input<'data>, Output = Command, Error = E>
where
	E: ParseError<Input<'data>>,
{
	CommandParser(PhantomData)
}

struct CommandParser<E>(PhantomData<E>);

impl<'data, E> Parser<Input<'data>> for CommandParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = Command;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		delimited(
			tag(OPEN_DELIMITER),
			separated_pair(
				recognize((
					parse_name,
					opt((char(' '), parse_name)),
					opt((char(' '), parse_name)),
				)),
				char(':'),
				u64,
			),
			tag(CLOSE_DELIMITER),
		)
		.map(|(name, id)| Command {
			name: name.to_string(),
			id,
		})
		.process::<OM>(input)
	}
}

fn parse_name<'data, E>(input: Input<'data>) -> IResult<Input<'data>, (), E>
where
	E: ParseError<Input<'data>>,
{
	fold_many_m_n(
		1,
		32,
		verify(anychar::<Input, _>, |ch| {
			*ch == '-' || *ch == '_' || ch.is_alphanumeric() || is_devanagari(*ch) || is_thai(*ch)
		}),
		|| (),
		|(), _| (),
	)
	.parse_complete(input)
}

fn is_devanagari(ch: char) -> bool {
	ScriptWithExtensions::new().has_script(ch, Script::Devanagari)
}

fn is_thai(ch: char) -> bool {
	ScriptWithExtensions::new().has_script(ch, Script::Thai)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

	use super::{command, Command};

	#[test]
	fn basic_command() {
		let s = r"</abcd:1234>";
		let (rem, res) = command()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Command {
				name: "abcd".to_string(),
				id: 1234
			}
		);
	}

	#[test]
	fn command_with_subcommands() {
		let s = r"</abcd efgh ijkl:1234>";
		let (rem, res) = command()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Command {
				name: "abcd efgh ijkl".to_string(),
				id: 1234
			}
		);
	}
}
