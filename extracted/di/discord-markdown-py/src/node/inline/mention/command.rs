//! Command mention parsing.

use icu_properties::{props::Script, script::ScriptWithExtensions};

use crate::{
	Input,
	error::{Fail, PResult},
};

use super::CLOSE_DELIMITER;

pub const OPEN_DELIMITER: &str = "</";

/// The most characters a command name, or each of its subcommands, may have.
const MAX_NAME_LEN: usize = 32;

/// A command mention.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Command {
	pub name: String,
	pub id: u64,
}

/// Parse a command mention: a name with up to two subcommands, as in `</abcd efgh ijkl:1234>`.
///
/// # Errors
/// If the content does not begin with a command mention.
pub fn command(input: &mut Input) -> PResult<Command> {
	input.tag(OPEN_DELIMITER)?;
	let name = input.recognize(|input| {
		parse_name(input)?;
		for _ in 0..2 {
			input.attempt(|input| {
				input.char(' ')?;
				parse_name(input)
			})?;
		}
		Ok(())
	})?;
	input.char(':')?;
	let id = input.u64()?;
	input.tag(CLOSE_DELIMITER)?;

	Ok(Command {
		name: name.to_string(),
		id,
	})
}

fn parse_name(input: &mut Input) -> PResult<()> {
	let len = input
		.char_indices()
		.take(MAX_NAME_LEN)
		.take_while(|&(_, ch)| {
			ch == '-' || ch == '_' || ch.is_alphanumeric() || is_devanagari(ch) || is_thai(ch)
		})
		.last()
		.map(|(index, ch)| index + ch.len_utf8())
		.ok_or(Fail::NoMatch)?;
	input.advance(len);
	Ok(())
}

fn is_devanagari(ch: char) -> bool {
	ScriptWithExtensions::new().has_script(ch, Script::Devanagari)
}

fn is_thai(ch: char) -> bool {
	ScriptWithExtensions::new().has_script(ch, Script::Thai)
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::{Command, command};

	#[test]
	fn basic_command() {
		let s = r"</abcd:1234>";
		let (rem, res) = run(s, command).expect("unable to parse");
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
		let (rem, res) = run(s, command).expect("unable to parse");
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
