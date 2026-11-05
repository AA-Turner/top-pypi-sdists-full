//! Unicode emoji parsing.
//!
//! This matches emoji sequences from [`discord_emoji`].

use discord_emoji::{CODE_POINTS, MAX_CODE_POINT_LEN};
use icu_properties::{CodePointSetData, CodePointSetDataBorrowed, props::Emoji};

use crate::{
	Input,
	error::{Fail, PResult},
	span::Trace,
};

const EMOJI: CodePointSetDataBorrowed = CodePointSetData::new::<Emoji>();

/// The `Emoji=Yes` code points below `0x80`: `#`, `*` and the digits.
const ASCII_EMOJI: u128 = (1 << b'#') | (1 << b'*') | (0x3FF << b'0');

/// Whether `input` begins with a code point that can start an emoji sequence.
///
/// Empty input does not start with an emoji.
fn starts_with_emoji(input: &str) -> bool {
	if let Some(&first) = input.as_bytes().first()
		&& first.is_ascii()
	{
		ASCII_EMOJI & (1 << first) != 0
	} else {
		input.chars().next().is_some_and(|ch| EMOJI.contains(ch))
	}
}

/// Whether an emoji can begin with `byte`: an ASCII emoji, or the lead byte of any other code
/// point.
#[must_use]
pub fn may_start_with(byte: u8) -> bool {
	!byte.is_ascii() || ASCII_EMOJI & (1 << byte) != 0
}

/// Parse an emoji.
///
/// The produced value is guaranteed to be a valid emoji, based on [`discord_emoji`].
///
/// # Errors
/// If the content does not begin with a Unicode emoji.
#[tracing::instrument(name = "emoji_parser", level = "trace", skip_all, fields(ok, output))]
pub fn emoji<'data>(input: &mut Input<'data>) -> PResult<&'data str> {
	if !starts_with_emoji(input) {
		return Err(Fail::NoMatch);
	}

	let end = longest_code_point(input.content).ok_or(Fail::NoMatch)?;
	Ok(input.advance(end)).trace()
}

/// The length of the longest prefix of `content` in [`CODE_POINTS`].
///
/// Only the first code point of a sequence can be ASCII (`#`, `*` and the digits of a keycap), so
/// the search stops at the first ASCII code point after it, which ends nearly every emoji in prose
/// after a single lookup.
fn longest_code_point(content: &str) -> Option<usize> {
	let mut longest = None;
	for (start, ch) in content.char_indices() {
		let end = start + ch.len_utf8();
		if end > MAX_CODE_POINT_LEN || (start > 0 && ch.is_ascii()) {
			break;
		}
		if CODE_POINTS.contains(&content[..end]) {
			longest = Some(end);
		}
	}
	longest
}

#[cfg(test)]
mod test {
	use std::{
		fs::File,
		io::{self, BufRead, BufReader},
	};

	use discord_emoji::CODE_POINTS;

	use crate::test_utils::run;

	use super::{EMOJI, emoji, starts_with_emoji};

	#[test]
	fn ascii_bitmap_matches_the_emoji_property() {
		for byte in 0..0x80u8 {
			let ch = char::from(byte);
			assert_eq!(
				starts_with_emoji(&ch.to_string()),
				EMOJI.contains(ch),
				"{ch:?} (U+{byte:04X})"
			);
		}
	}

	#[test]
	fn only_the_first_code_point_is_ascii() {
		for code_point in &CODE_POINTS {
			assert!(
				!code_point.chars().skip(1).any(|ch| ch.is_ascii()),
				"{code_point:?}"
			);
		}
	}

	#[derive(Debug)]
	struct Case {
		code_points: String,
		status: String,
	}

	fn parse_test_data() -> impl Iterator<Item = Result<Case, io::Error>> {
		let file = File::open("src/node/inline/emoji/emoji-test.txt")
			.expect("test data should be present");
		let reader = BufReader::new(file);
		reader.lines().filter_map(|line| match line {
			Ok(str) if str.starts_with('#') || str.is_empty() => None,
			Ok(str) => {
				let (code_points, status) = str.split_once(';').unwrap();
				let code_points = code_points
					.split_whitespace()
					.map(|code_point| {
						char::from_u32(u32::from_str_radix(code_point, 16).unwrap()).unwrap()
					})
					.collect::<String>();
				let status = status.split_once('#').unwrap().0.trim().to_string();
				Some(Ok(Case {
					code_points,
					status,
				}))
			}
			Err(e) => Some(Err(e)),
		})
	}

	#[test]
	fn verify_test_data() {
		let cases = parse_test_data();
		for case in cases {
			let case = case.unwrap();

			if case.status != "fully-qualified" {
				continue;
			}

			let (rem, res) = run(&case.code_points, emoji).expect("unable to parse");
			assert_eq!(
				rem,
				"",
				"input {case:?} chars: {}",
				case.code_points.chars().count()
			);
			assert_eq!(res, case.code_points, "input {case:?}");
		}
	}
}
