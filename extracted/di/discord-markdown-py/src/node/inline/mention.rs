//! Mention parsing.

use std::fmt::Display;

use crate::{
	Input,
	error::{Fail, PResult},
};

use command::Command;

pub mod command;
pub mod r#static;

/// `@everyone`
pub const EVERYONE: &str = "@everyone";
/// `@here`
pub const HERE: &str = "@here";

/// The sequence that begins a user mention.
pub const USER_MENTION_OPEN_DELIMITER: &str = "<@";
/// The sequence that begins a channel mention.
pub const CHANNEL_MENTION_OPEN_DELIMITER: &str = "<#";
/// The sequence that begins a role mention.
pub const ROLE_MENTION_OPEN_DELIMITER: &str = "<@&";
/// The sequence that begins a game mention.
pub const GAME_MENTION_OPEN_DELIMITER: &str = "<@$";

/// The sequence that closes all mentions.
pub const CLOSE_DELIMITER: &str = ">";

/// Parse any mention open sequence, including [`EVERYONE`] and [`HERE`].
///
/// # Errors
/// If the input does not begin with one.
pub fn open_delimiter<'data>(input: &mut Input<'data>) -> PResult<&'data str> {
	[
		EVERYONE,
		HERE,
		USER_MENTION_OPEN_DELIMITER,
		CHANNEL_MENTION_OPEN_DELIMITER,
		ROLE_MENTION_OPEN_DELIMITER,
		command::OPEN_DELIMITER,
		GAME_MENTION_OPEN_DELIMITER,
	]
	.into_iter()
	.find_map(|delimiter| input.tag(delimiter).ok())
	.ok_or(Fail::NoMatch)
}

/// A mention.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case",)
)]
pub enum Mention {
	User(u64),
	Channel(u64),
	Role(u64),
	Command(Command),
	Everyone,
	Here,
	Game(u64),
	Static(r#static::Static),
}

impl Display for Mention {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		match self {
			Self::User(id) | Self::Channel(id) | Self::Role(id) | Self::Game(id) => {
				write!(f, "{id}")
			}
			Self::Command(Command { name, .. }) => write!(f, "{}", name.clone().as_str()),
			Self::Everyone => write!(f, "{EVERYONE}"),
			Self::Here => write!(f, "{HERE}"),
			Self::Static(st) => write!(f, "{st}"),
		}
	}
}

/// Parse a mention.
///
/// # Errors
/// If the content does not begin with a mention.
pub fn mention(input: &mut Input) -> PResult<Mention> {
	let parsers: [fn(&mut Input) -> PResult<Mention>; 8] = [
		|input| user(input).map(Mention::User),
		|input| channel(input).map(Mention::Channel),
		|input| role(input).map(Mention::Role),
		|input| game(input).map(Mention::Game),
		|input| command::command(input).map(Mention::Command),
		|input| everyone(input).map(|()| Mention::Everyone),
		|input| here(input).map(|()| Mention::Here),
		|input| r#static::parse(input).map(Mention::Static),
	];
	for parser in parsers {
		if let Some(mention) = input.attempt(parser)? {
			return Ok(mention);
		}
	}
	Err(Fail::NoMatch)
}

/// Parse an @everyone mention.
///
/// # Errors
/// If the content does not begin with "@everyone".
pub fn everyone(input: &mut Input) -> PResult<()> {
	input.tag(EVERYONE).map(|_| ())
}

/// Parse a @here mention.
///
/// # Errors
/// If the content does not begin with "@here".
pub fn here(input: &mut Input) -> PResult<()> {
	input.tag(HERE).map(|_| ())
}

/// The id and close that end every mention of an id.
fn id_and_close(input: &mut Input) -> PResult<u64> {
	let id = input.u64()?;
	input.tag(CLOSE_DELIMITER)?;
	Ok(id)
}

/// Parse a user mention.
///
/// # Errors
/// If the content does not begin with a user mention.
pub fn user(input: &mut Input) -> PResult<u64> {
	input.tag(USER_MENTION_OPEN_DELIMITER)?;
	input.eat("!");
	id_and_close(input)
}

/// Parse a channel mention.
///
/// # Errors
/// If the content does not begin with a channel mention.
pub fn channel(input: &mut Input) -> PResult<u64> {
	input.tag(CHANNEL_MENTION_OPEN_DELIMITER)?;
	id_and_close(input)
}

/// Parse a role mention.
///
/// # Errors
/// If the content does not begin with a role mention.
pub fn role(input: &mut Input) -> PResult<u64> {
	input.tag(ROLE_MENTION_OPEN_DELIMITER)?;
	id_and_close(input)
}

/// Parse a game mention.
///
/// # Errors
/// If the content does not begin with a game mention.
pub fn game(input: &mut Input) -> PResult<u64> {
	input.tag(GAME_MENTION_OPEN_DELIMITER)?;
	id_and_close(input)
}

#[cfg(test)]
mod test {
	use super::{Mention, channel, game, mention, role, user};
	use crate::test_utils::run;

	#[test]
	fn basic_user() {
		let s = r"<@1234>";
		let (rem, res) = run(s, user).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn user_deprecated() {
		let s = r"<@!1234>";
		let (rem, res) = run(s, user).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_channel() {
		let s = r"<#1234>";
		let (rem, res) = run(s, channel).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_role() {
		let s = r"<@&1234>";
		let (rem, res) = run(s, role).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_game() {
		let s = r"<@$1234>";
		let (rem, res) = run(s, game).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn everyone() {
		let s = r"@everyone";
		let (rem, res) = run(s, mention).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, Mention::Everyone);
	}

	#[test]
	fn here() {
		let s = r"@here";
		let (rem, res) = run(s, mention).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, Mention::Here);
	}
}
