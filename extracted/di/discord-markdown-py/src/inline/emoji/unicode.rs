use std::{fmt::Debug, marker::PhantomData, sync::OnceLock};

use enumset::{EnumSet, EnumSetType};
use icu_properties::{
	props::{Emoji, EmojiModifier, EmojiPresentation, RegionalIndicator},
	CodePointSetData, CodePointSetDataBorrowed,
};
use nom::{
	branch::alt,
	bytes::complete::take_while1,
	character::complete::{char, satisfy},
	combinator::{opt, recognize},
	error::{ErrorKind, ParseError},
	multi::separated_list1,
	sequence::{pair, terminated},
	IResult, Mode, Parser,
};
use tracing::{Level, Span};

use crate::{span::TraceOk, Input};

// https://unicode.org/reports/tr51/#EBNF_and_Regex

const ZERO_WIDTH_JOINER: char = '\u{200D}';
const VARIATION_SELECTOR_16: char = '\u{FE0F}';
const COMBINING_ENCLOSING_KEYCAP: char = '\u{20E3}';
const TAG_SPACE: char = '\u{E0020}';
const TAG_TILDE: char = '\u{E007E}';
const TERM_TAG: char = '\u{E007F}';

const MAX_UNICODE: usize = 0x10F_FFF + 1;
static CHAR_ARRAY: OnceLock<Vec<CharMetadata>> = OnceLock::new();

/// Information about a character that is useful for determining if a sequence is an emoji.
#[derive(EnumSetType)]
pub enum CharFlag {
	/// Whether the character belongs to the [`regional_indicator`] set.
	RegionalIndicator,
	/// Whether the character belongs to the [`emoji_modifier`] set.
	EmojiModifier,
	/// Whether the character belongs to the [`emoji_presentation`] set.
	EmojiPresentation,
	/// Whether the character belongs to the [`emoji_set`].
	Emoji,
}

pub type CharMetadata = EnumSet<CharFlag>;

fn get_metadata(ch: char) -> CharMetadata {
	CHAR_ARRAY.get_or_init(load_emoji_metadata)[ch as usize]
}

const REGIONAL_INDICATOR: CodePointSetDataBorrowed = CodePointSetData::new::<RegionalIndicator>();
const EMOJI_MODIFIER: CodePointSetDataBorrowed = CodePointSetData::new::<EmojiModifier>();
const EMOJI_PRESENTATION: CodePointSetDataBorrowed = CodePointSetData::new::<EmojiPresentation>();
const EMOJI: CodePointSetDataBorrowed = CodePointSetData::new::<Emoji>();

/// Loads all Unicode characters into a vec containing precomputed metadata for that character.
/// Each character's index in the vec corresponds to its Unicode scalar value.
#[must_use]
pub fn load_emoji_metadata() -> Vec<CharMetadata> {
	let mut metadata = Vec::with_capacity(MAX_UNICODE);
	metadata.resize(MAX_UNICODE, CharMetadata::empty());

	let relevant_chars = REGIONAL_INDICATOR
		.iter_ranges()
		.flatten()
		.chain(EMOJI_MODIFIER.iter_ranges().flatten())
		.chain(EMOJI_PRESENTATION.iter_ranges().flatten())
		.chain(EMOJI.iter_ranges().flatten());

	for code_point in relevant_chars {
		let index = code_point as usize;

		if REGIONAL_INDICATOR.contains32(code_point) {
			metadata[index] |= CharFlag::RegionalIndicator;
		}

		if EMOJI_MODIFIER.contains32(code_point) {
			metadata[index] |= CharFlag::EmojiModifier;
		}

		if EMOJI_PRESENTATION.contains32(code_point) {
			metadata[index] |= CharFlag::EmojiPresentation;
		}

		if EMOJI.contains32(code_point) {
			metadata[index] |= CharFlag::Emoji;
		}
	}

	metadata
}

fn is_regional_indicator(ch: char) -> bool {
	get_metadata(ch).contains(CharFlag::RegionalIndicator)
}

fn is_emoji_modifier(ch: char) -> bool {
	get_metadata(ch).contains(CharFlag::EmojiModifier)
}

fn is_emoji_presentation(ch: char) -> bool {
	get_metadata(ch).contains(CharFlag::EmojiPresentation)
}

fn is_emoji(ch: char) -> bool {
	get_metadata(ch).contains(CharFlag::Emoji)
}

fn parse_tag_modifier<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	terminated(
		take_while1(|ch| matches!(ch, TAG_SPACE..=TAG_TILDE)),
		char(TERM_TAG),
	)
	.parse_complete(data)
}

fn parse_emoji_modification<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	alt((
		parse_tag_modifier,
		recognize(satisfy(is_emoji_modifier)),
		recognize(pair(
			char(VARIATION_SELECTOR_16), // some unqualified emojis are missing this
			opt(char(COMBINING_ENCLOSING_KEYCAP)),
		)),
	))
	.parse_complete(data)
}

fn parse_flag_sequence<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	recognize(pair(
		satisfy(is_regional_indicator),
		satisfy(is_regional_indicator),
	))
	.parse_complete(data)
}

/// Parse something that is probably part of an emoji sequence. Succeeds if there is a character
/// that is an emoji and emoji presentation that is optionally followed by an emoji modification
/// character OR that is only an emoji followed by a non-optional emoji modification character.
///
/// # Note
/// This is in violation of the recommended approach, which is more lax and simply allows for any
/// emoji character followed by an optional emoji modification character. This deviation is
/// required so that we don't parse things like * and 1 as emojis. However, this also means that we
/// only support fully qualified emojis: this is probably fine (?) since the client doesn't support
/// un/minimally qualified emojis today.
fn parse_emoji_element<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	// TODO: improve support for un/minimally qualified emojis
	alt((
		recognize((
			satisfy(is_emoji_presentation),
			opt(parse_emoji_modification),
		)),
		recognize((satisfy(is_emoji), parse_emoji_modification)),
	))
	.parse_complete(data)
}

fn parse_zwj_element<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<Input<'data>>,
{
	alt((parse_flag_sequence, parse_emoji_element)).parse_complete(data)
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
		if let Some(ch) = nom::Input::iter_elements(&input).next() {
			if get_metadata(ch).is_empty() {
				Span::current().record("ok", false);
				return Err(nom::Err::Error(OM::Error::bind(|| {
					E::from_error_kind(input, ErrorKind::Satisfy)
				})));
			}
		}

		recognize(separated_list1(char(ZERO_WIDTH_JOINER), parse_zwj_element))
			.process::<OM>(input)
			.trace_ok()
	}
}

/// Parse an emoji. This parser follows the recommended approach, but the produced value is not
/// guaranteed to be a valid emoji.
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

	use super::emoji;

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
