use std::marker::PhantomData;

use discord_emoji::EMOJI_BY_SHORTNAME;
use nom::{
	branch::alt, bytes::tag, character::complete::satisfy, combinator::recognize,
	error::ParseError, multi::many1_count, sequence::delimited, IResult, Parser,
};

use crate::Input;

pub const DELIMITER: &str = ":";

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
				recognize((parse_emoji_chars, tag("::"), parse_emoji_chars)),
				parse_emoji_chars,
			)),
			tag(DELIMITER),
		)
		.map_opt(|name| EMOJI_BY_SHORTNAME.get(&name.content).copied())
		.process::<OM>(input)
	}
}

fn parse_emoji_chars<'data, E>(input: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	recognize(many1_count(satisfy(|ch| {
		ch.is_ascii_alphanumeric() || ch == '-' || ch == '_'
	})))
	.parse_complete(input)
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
