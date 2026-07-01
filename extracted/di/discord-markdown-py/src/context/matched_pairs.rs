use std::marker::PhantomData;

use enumset::enum_set;
use memchr::memchr2_iter;
use nom::{
	error::{ErrorKind, ParseError},
	Input as _, Mode, Parser,
};

use crate::{
	grammar::{Grammar, GrammarSet},
	Input,
};

pub const GRAMMARS: GrammarSet = enum_set!(Grammar::MaskedLinkText);

pub struct MatchedPairsParser<E> {
	pub grammars: GrammarSet,
	pub error: PhantomData<E>,
}

/// Scans `s` for a balanced bracket span beginning at position 0 and returns its byte length
/// (including both the opening and closing bracket). Returns `None` if `s` does not start with
/// `open` or has no matching `close`.
fn find_balanced_span(s: &str, open: u8, close: u8) -> Option<usize> {
	let s_bytes = s.as_bytes();

	if s_bytes.first() != Some(&open) {
		return None;
	}

	let mut depth = 0usize;
	for pos in memchr2_iter(open, close, s_bytes) {
		if s_bytes[pos] == open {
			depth += 1;
		} else {
			depth -= 1;
			if depth == 0 {
				// +1 to include the closing byte in the returned span length
				return Some(pos + 1);
			}
		}
	}

	None
}

impl<'data, E> Parser<Input<'data>> for MatchedPairsParser<E>
where
	E: ParseError<Input<'data>>,
{
	type Output = Input<'data>;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		for grammar in (self.grammars & GRAMMARS).iter() {
			let Some((open, close)) = grammar.bracket_delimiters() else {
				continue;
			};
			if let Some(span_len) = find_balanced_span(&input, open, close) {
				let (remaining, span) = input.take_split(span_len);
				return Ok((remaining, OM::Output::bind(|| span)));
			}
		}
		Err(nom::Err::Error(OM::Error::bind(|| {
			E::from_error_kind(input, ErrorKind::Alt)
		})))
	}
}
