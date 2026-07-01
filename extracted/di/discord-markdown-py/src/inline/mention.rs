use std::fmt::Display;

use nom::{
	branch::alt,
	bytes::complete::tag,
	character::complete::{char, u64},
	combinator::{map, opt, value},
	error::{ContextError, FromExternalError, ParseError},
	sequence::delimited,
	Parser,
};

use crate::{inline::mention::command::Command, unparse::Unparse, Input};

pub mod command;

pub const EVERYONE: &str = "@everyone";
pub const HERE: &str = "@here";

pub const USER_MENTION_OPEN_DELIMITER: &str = "<@";
pub const CHANNEL_MENTION_OPEN_DELIMITER: &str = "<#";
pub const ROLE_MENTION_OPEN_DELIMITER: &str = "<@&";
pub const GAME_MENTION_OPEN_DELIMITER: &str = "<@$";

pub const CLOSE_DELIMITER: &str = ">";

#[must_use]
pub fn open_delimiter<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	alt((
		tag(EVERYONE),
		tag(HERE),
		tag(USER_MENTION_OPEN_DELIMITER),
		tag(CHANNEL_MENTION_OPEN_DELIMITER),
		tag(ROLE_MENTION_OPEN_DELIMITER),
		tag(command::OPEN_DELIMITER),
		tag(GAME_MENTION_OPEN_DELIMITER),
	))
}

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
		}
	}
}

impl Unparse for Mention {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self::User(id) => write!(f, "{USER_MENTION_OPEN_DELIMITER}{id}{CLOSE_DELIMITER}"),
			Self::Channel(id) => write!(f, "{CHANNEL_MENTION_OPEN_DELIMITER}{id}{CLOSE_DELIMITER}"),
			Self::Role(id) => write!(f, "{ROLE_MENTION_OPEN_DELIMITER}{id}{CLOSE_DELIMITER}"),
			Self::Game(id) => write!(f, "{GAME_MENTION_OPEN_DELIMITER}{id}{CLOSE_DELIMITER}"),
			Self::Command(command) => command.fmt(f),
			Self::Everyone => f.write_str(EVERYONE),
			Self::Here => f.write_str(HERE),
		}
	}
}

/// Parse a mention.
///
/// # Errors
/// If the content does not begin with a mention.
pub fn mention<'data, E>() -> impl Parser<Input<'data>, Output = Mention, Error = E>
where
	E: ParseError<Input<'data>>
		+ ContextError<Input<'data>>
		+ FromExternalError<Input<'data>, url::ParseError>,
{
	alt((
		map(user(), Mention::User),
		map(channel(), Mention::Channel),
		map(role(), Mention::Role),
		map(game(), Mention::Game),
		map(command::command(), Mention::Command),
		value(Mention::Everyone, everyone()),
		value(Mention::Here, here()),
	))
}

/// Parse an @everyone mention.
///
/// # Errors
/// If the content does not begin with "@everyone".
#[must_use]
pub fn everyone<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	tag(EVERYONE)
}

/// Parse a @here mention.
///
/// # Errors
/// If the content does not begin with "@here".
#[must_use]
pub fn here<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	tag(HERE)
}

/// Parse a user mention.
///
/// # Errors
/// If the content does not begin with a user mention.
pub fn user<'data, E>() -> impl Parser<Input<'data>, Output = u64, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		(tag(USER_MENTION_OPEN_DELIMITER), opt(char('!'))),
		u64,
		tag(CLOSE_DELIMITER),
	)
}

/// Parse a channel mention.
///
/// # Errors
/// If the content does not begin with a channel mention.
pub fn channel<'data, E>() -> impl Parser<Input<'data>, Output = u64, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(
		tag(CHANNEL_MENTION_OPEN_DELIMITER),
		u64,
		tag(CLOSE_DELIMITER),
	)
}

/// Parse a role mention.
///
/// # Errors
/// If the content does not begin with a role mention.
pub fn role<'data, E>() -> impl Parser<Input<'data>, Output = u64, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(tag(ROLE_MENTION_OPEN_DELIMITER), u64, tag(CLOSE_DELIMITER))
}

/// Parse a game mention.
///
/// # Errors
/// If the content does not begin with a game mention.
pub fn game<'data, E>() -> impl Parser<Input<'data>, Output = u64, Error = E>
where
	E: ParseError<Input<'data>>,
{
	delimited(tag(GAME_MENTION_OPEN_DELIMITER), u64, tag(CLOSE_DELIMITER))
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::{channel, game, role, user};
	use crate::{
		inline::mention::{mention, Mention},
		test_utils::handle_nom_err,
	};

	#[test]
	fn basic_user() {
		let s = r"<@1234>";
		let (rem, res) = user()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn user_deprecated() {
		let s = r"<@!1234>";
		let (rem, res) = user()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_channel() {
		let s = r"<#1234>";
		let (rem, res) = channel()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_role() {
		let s = r"<@&1234>";
		let (rem, res) = role()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn basic_game() {
		let s = r"<@$1234>";
		let (rem, res) = game()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, 1234);
	}

	#[test]
	fn everyone() {
		let s = r"@everyone";
		let (rem, res) = mention()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, Mention::Everyone);
	}

	#[test]
	fn here() {
		let s = r"@here";
		let (rem, res) = mention()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, Mention::Here);
	}
}
