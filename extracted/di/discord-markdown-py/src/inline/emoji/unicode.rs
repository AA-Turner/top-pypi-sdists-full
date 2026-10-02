//! Unicode emoji parsing.
//!
//! This matches emoji sequences from [`discord_emoji`].

use std::{fmt::Debug, marker::PhantomData, sync::LazyLock};

use aho_corasick::{AhoCorasick, Anchored, MatchKind, StartKind};
use discord_emoji::CODE_POINTS;
use icu_properties::{CodePointSetData, CodePointSetDataBorrowed, props::Emoji};
use nom::{
	Mode, Parser,
	combinator::fail,
	error::{ErrorKind, ParseError},
};
use tracing::{Level, Span};

use crate::{Input, span::TraceOk};

static CODE_POINT_FINDER: LazyLock<AhoCorasick> = LazyLock::new(|| {
	AhoCorasick::builder()
		.match_kind(MatchKind::LeftmostLongest)
		.start_kind(StartKind::Anchored)
		.build(CODE_POINTS.iter())
		.unwrap()
});

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

struct EmojiParser<E>(PhantomData<E>);

impl<E> Debug for EmojiParser<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("EmojiParser").field(&self.0).finish()
	}
}

impl<'data, E> Parser<Input<'data>> for EmojiParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "emoji_parser", level = Level::TRACE, fields(ok))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		if !starts_with_emoji(&input) {
			Span::current().record("ok", false);
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Satisfy)
			})));
		}

		let end_byte = CODE_POINT_FINDER
			.find(aho_corasick::Input::new(&*input).anchored(Anchored::Yes))
			.map(|mat| mat.end());

		match end_byte {
			Some(end) => {
				let (rest, emoji) = nom::Input::take_split(&input, end);
				Ok((rest, OM::Output::bind(|| emoji)))
			}
			None => fail().process::<OM>(input),
		}
		.trace_ok()
	}
}

/// Parse an emoji.
///
/// The produced value is guaranteed to be a valid emoji, based on [`discord_emoji`].
///
/// # Errors
/// If the content does not begin with a Unicode emoji.
#[must_use]
pub fn emoji<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<Input<'data>>,
{
	EmojiParser(PhantomData)
}

#[cfg(test)]
mod test {
	use std::{
		fs::File,
		io::{self, BufRead, BufReader},
	};

	use nom::{Finish, Parser};

	use crate::test_utils::handle_nom_err;

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

	#[derive(Debug)]
	struct Case {
		code_points: String,
		status: String,
	}

	fn parse_test_data() -> impl Iterator<Item = Result<Case, io::Error>> {
		let file =
			File::open("src/inline/emoji/emoji-test.txt").expect("test data should be present");
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

			let (rem, res) = emoji()
				.parse_complete((&*case.code_points).into())
				.finish()
				.map_err(handle_nom_err(&case.code_points))
				.expect("unable to parse");
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
