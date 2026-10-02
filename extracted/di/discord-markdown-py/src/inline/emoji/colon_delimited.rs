//! Parse colon-delimited emojis
//!
//! While most Discord clients send actual emoji characters, bots in particular often send emoji
//! as colon-delimited strings instead: for example, `:foot:` instead of `🦶`. Powered by
//! [`discord_emoji`], this module normalizes those colon-delimited emoji into their real
//! characters.

use std::marker::PhantomData;

use discord_emoji::{EMOJI_BY_SHORTNAME, EMOJI_SHORTNAME_CHARS};
use nom::{
	branch::alt,
	bytes::complete::{tag, take_while1},
	character::satisfy,
	combinator::recognize,
	error::ParseError,
	sequence::delimited,
	IResult, Parser,
};

use crate::Input;

/// The delimiter for colon-delimited emoji.
pub const DELIMITER: &str = ":";

/// Parse a colon-delimited emoji.
///
/// # Errors
/// If the content does not begin with a colon-delimited emoji.
#[must_use]
pub fn emoji<'data, E>() -> impl Parser<Input<'data>, Output = &'static str, Error = E>
where
	E: ParseError<Input<'data>>,
{
	ColonDelimitedParser(PhantomData)
}

struct ColonDelimitedParser<E>(PhantomData<E>);

impl<'data, E> Parser<Input<'data>> for ColonDelimitedParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = &'static str;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		delimited(
			tag(DELIMITER),
			alt((
				recognize((parse_emoji_chars, tag("::"), parse_skin_tone())),
				parse_emoji_chars,
			)),
			tag(DELIMITER),
		)
		.map_opt(|name| EMOJI_BY_SHORTNAME.get(name.content).copied())
		.process::<OM>(input)
	}
}

fn parse_emoji_chars<'data, E>(input: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	take_while1(|ch| EMOJI_SHORTNAME_CHARS.contains(&ch)).parse_complete(input)
}

fn parse_skin_tone<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	recognize((tag("skin-tone-"), satisfy(|ch| ch.is_ascii_digit())))
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

	use super::emoji;

	#[test]
	fn basic_parse() {
		let s = ":foot:";
		let (rem, res) = emoji()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("able to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "🦶");
	}

	#[test]
	fn parse_with_skin_tone() {
		let s = ":foot::skin-tone-1:";
		let (rem, res) = emoji()
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("able to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "🦶🏻");
	}
}
