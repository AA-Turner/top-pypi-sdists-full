//! Text parsing.

use std::fmt::Debug;
use std::marker::PhantomData;

use nom::character::streaming::none_of;
use nom::combinator::{not, recognize};
use nom::error::ErrorKind;
use nom::sequence::preceded;
use nom::{Input as _, Mode, Offset as _, Parser};
use tracing::Level;

use crate::context::Context;
use crate::context::TerminalOutput;
use crate::error::ParseError;
use crate::span::TraceOk;
use crate::Input;

use super::emoji;

/// The shrug emoticon, whose initial `¯\` would otherwise be read as an escape.
const SHRUG: &str = "_(ツ)_/¯";

struct NormalParser<E> {
	outer: TextParser<E>,
}

impl<'data, E> Parser<Input<'data>> for NormalParser<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		self.outer
			.context
			.guard_terminal_sequence(|| {
				preceded(
					(
						not(emoji::unicode::emoji()),
						not(self.outer.context.allowed_start_sequences()),
					),
					recognize(none_of("\\")),
				)
			})
			.map(TerminalOutput::inner)
			.process::<OM>(input)
	}
}

/// A resolved escape sequence.
struct Escape<'data> {
	/// The text the sequence expands to.
	expansion: &'data str,
	/// How many bytes of the input the sequence covers, counting the backslash itself.
	consumed: usize,
}

/// Resolve the escape sequence at the start of `rest`, which begins with a backslash.
fn escape(rest: &str) -> Escape<'_> {
	let tail = &rest[1..];

	if tail.starts_with(SHRUG) {
		// The emoticon keeps its backslash -- `¯\_(ツ)_/¯` is text, not an escape.
		Escape {
			expansion: &rest[..=SHRUG.len()],
			consumed: 1 + SHRUG.len(),
		}
	} else if tail.starts_with("__") {
		// Allow escaping a double underscore with a single backslash.
		Escape {
			expansion: &tail[..2],
			consumed: 3,
		}
	} else {
		match tail.chars().next() {
			// TODO - Add support for non-latin languages by removing the 'ascii' bit here.
			Some(ch) if !ch.is_ascii_alphanumeric() && !ch.is_ascii_whitespace() => Escape {
				expansion: &tail[..ch.len_utf8()],
				consumed: 1 + ch.len_utf8(),
			},
			// Not an escape we recognise: the next character is alphanumeric or whitespace, or
			// the input ends here. The backslash is literal text, and nothing after it is
			// consumed, so the next character is parsed as normal text -- crucially including a
			// terminal sequence, which has to stay unconsumed for the run to end there.
			_ => Escape {
				expansion: "\\",
				consumed: 1,
			},
		}
	}
}

struct TextParser<E> {
	context: Context,
	error: PhantomData<E>,
}

impl<E> Clone for TextParser<E> {
	fn clone(&self) -> Self {
		Self {
			context: self.context.clone(),
			error: PhantomData,
		}
	}
}

impl<E> Debug for TextParser<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("TextParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for TextParser<E>
where
	E: ParseError<'data>,
{
	type Output = String;
	type Error = E;

	#[tracing::instrument(
		name = "text_parser",
		level = Level::TRACE,
		fields(context = ?self.context, ok, output),
		skip(self)
	)]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		// This is nom's `escaped_transform` specialised to our escape grammar. It is spelled out
		// rather than composed because `escaped_transform` fails the *whole* run when an escape
		// is not recognised -- including when the backslash is the final byte of the input, a
		// case it rejects without consulting the transform parser at all. A failed run sends the
		// inline parser's `anychar` fallback (see `crate::inline`) one character further along to
		// try again, rescanning to the same backslash every time: quadratic in the run's length,
		// and silently dropping every escape before the offending one. See the tests below.
		let mut normal = NormalParser {
			outer: self.clone(),
		};
		let mut captured = OM::Output::bind(String::new);
		let mut index = 0;

		while index < input.input_len() {
			match normal.process::<OM>(input.take_from(index)) {
				Ok((remaining, matched)) => {
					let next = input.offset(&remaining);
					// A parser that consumed nothing would spin here forever.
					if next == index {
						break;
					}
					// Take the text from `matched` rather than re-slicing `input`: `str`'s
					// `Index` checks UTF-8 boundaries, and this runs once per character.
					captured = OM::Output::combine(matched, captured, |matched, mut captured| {
						captured.push_str(matched.content);
						captured
					});
					index = next;
				}
				// `normal` rejects the backslash so that escapes land here; anything else it
				// rejects is a terminal sequence, an emoji or a start sequence, which ends the
				// run.
				Err(nom::Err::Error(_)) => {
					if !input.content[index..].starts_with('\\') {
						break;
					}
					let escape = escape(&input.content[index..]);
					captured = OM::Output::map(captured, |mut captured| {
						captured.push_str(escape.expansion);
						captured
					});
					index += escape.consumed;
				}
				Err(err) => return Err(err),
			}
		}

		if index == 0 {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Verify)
			})));
		}

		let captured = OM::Output::map(captured, |captured| {
			tracing::Span::current().record("output", tracing::field::debug(&captured));
			captured
		});
		Ok((input.take_from(index), captured)).trace_ok()
	}
}

/// Parse text.
///
/// This is the fallback rule which successfully parses any non-empty content up to the
/// context's terminal sequence, an emoji, or any of [`Context::allowed_start_sequences`].
// \\([^0-9A-Za-z\s])
#[must_use]
pub fn text<'data, E>(context: Context) -> impl Parser<Input<'data>, Output = String, Error = E>
where
	E: ParseError<'data>,
{
	TextParser {
		context,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::text;
	use crate::{context::Context, test_utils::handle_nom_err};

	#[test]
	fn simple_text() {
		let s = r"foo bar";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo bar");
	}

	#[test]
	fn escaped_text() {
		let s = r"foo\_1bar";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo_1bar");
	}

	#[test]
	fn escaped_backslash() {
		let s = r"foo\\1bar";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"foo\1bar");
	}

	#[test]
	fn shrug() {
		let s = r"¯\_(ツ)_/¯";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"¯\_(ツ)_/¯");
	}

	/// A backslash before a character that cannot be escaped is literal text, and does not stop
	/// the run.
	#[test]
	fn unrecognised_escape_is_literal() {
		for (s, expected) in [
			(r"foo\bar", r"foo\bar"),
			(r"foo\ bar", r"foo\ bar"),
			(r"foo\9bar", r"foo\9bar"),
		] {
			let (rem, res) = text(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
	}

	/// A backslash at the very end of the input is literal text. `escaped_transform` rejects this
	/// outright, which is one of the reasons the escape loop is spelled out by hand.
	#[test]
	fn trailing_backslash_is_literal() {
		let s = r"foo\";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"foo\");
	}

	/// An unrecognised escape must not retroactively disable the escapes before it, which is what
	/// happened while a failed run was being retried one character at a time.
	#[test]
	fn unrecognised_escape_does_not_disable_earlier_escapes() {
		for (s, expected) in [(r"a\_b\_c \z", r"a_b_c \z"), ("a\\_b\\_c \\", "a_b_c \\")] {
			let (rem, res) = text(Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
	}

	/// A terminal sequence after an unrecognised escape has to stay unconsumed, or the run would
	/// swallow the character that ends it.
	#[test]
	fn unrecognised_escape_does_not_consume_terminal_sequence() {
		let s = "foo\\\nbar";
		let (rem, res) = text(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "\nbar");
		assert_eq!(res, "foo\\");
	}
}
