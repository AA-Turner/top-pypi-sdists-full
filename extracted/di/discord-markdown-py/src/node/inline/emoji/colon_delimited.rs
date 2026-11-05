//! Parse colon-delimited emojis
//!
//! While most Discord clients send actual emoji characters, bots in particular often send emoji
//! as colon-delimited strings instead: for example, `:foot:` instead of `🦶`. Powered by
//! [`discord_emoji`], this module normalizes those colon-delimited emoji into their real
//! characters.

use discord_emoji::{EMOJI_BY_SHORTNAME, is_shortname_char};

use crate::{
	Input,
	error::{Fail, PResult},
};

/// The delimiter for colon-delimited emoji.
pub const DELIMITER: &str = ":";

/// Parse a colon-delimited emoji.
///
/// # Errors
/// If the content does not begin with a colon-delimited emoji.
pub fn emoji(input: &mut Input) -> PResult<&'static str> {
	input.tag(DELIMITER)?;
	let name = match input.attempt(|input| {
		input.recognize(|input| {
			emoji_chars(input)?;
			input.tag("::")?;
			skin_tone(input)
		})
	})? {
		Some(name) => name,
		None => emoji_chars(input)?,
	};
	input.tag(DELIMITER)?;

	EMOJI_BY_SHORTNAME.get(name).copied().ok_or(Fail::NoMatch)
}

fn emoji_chars<'data>(input: &mut Input<'data>) -> PResult<&'data str> {
	input.take_while1(is_shortname_char)
}

fn skin_tone(input: &mut Input) -> PResult<()> {
	input.tag("skin-tone-")?;
	// Multi-person emoji have up to 25 tones, one per pair of skin tones.
	let digits = input.bytes().take(2).take_while(u8::is_ascii_digit).count();
	if digits == 0 {
		return Err(Fail::NoMatch);
	}
	input.advance(digits);
	Ok(())
}

#[cfg(test)]
mod test {
	use crate::test_utils::run;

	use super::emoji;

	#[test]
	fn basic_parse() {
		let s = ":foot:";
		let (rem, res) = run(s, emoji).expect("able to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "🦶");
	}

	#[test]
	fn parse_with_skin_tone() {
		let s = ":foot::skin-tone-1:";
		let (rem, res) = run(s, emoji).expect("able to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "🦶🏻");
	}

	#[test]
	fn parse_with_two_digit_skin_tone() {
		let s = ":couple_mm::skin-tone-20:";
		let (rem, res) = run(s, emoji).expect("able to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "👨🏾‍❤️‍👨🏿");
	}

	#[test]
	fn rejects_three_digit_skin_tone() {
		let s = ":couple_mm::skin-tone-200:";
		assert!(run(s, emoji).is_err());
	}
}
