use std::fmt::Debug;
use std::marker::PhantomData;

use nom::branch::alt;
use nom::bytes::complete::{escaped_transform, tag};
use nom::character::complete::anychar;
use nom::character::streaming::none_of;
use nom::combinator::{not, recognize, verify};
use nom::sequence::preceded;
use nom::Parser;
use tracing::Level;

use crate::context::Context;
use crate::context::TerminalOutput;
use crate::error::ParseError;
use crate::span::{TraceOk, TraceParse};
use crate::Input;

use super::emoji;

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

struct TransformParser<E> {
	error: PhantomData<E>,
}

impl<'data, E> Parser<Input<'data>> for TransformParser<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		alt((
			tag("_(ツ)_/¯").map(|shrug| "\\" + shrug),
			// allow escaping double underscore
			tag("__"),
			recognize(verify(
				anychar,
				// TODO - Add support for non-latin languages by removing the 'ascii' bit here.
				|ch| !ch.is_ascii_alphanumeric() && !ch.is_ascii_whitespace(),
			)),
		))
		.process::<OM>(input)
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
		verify(
			escaped_transform(
				NormalParser {
					outer: self.clone(),
				},
				'\\',
				TransformParser { error: PhantomData },
			),
			|capture: &String| !capture.is_empty(),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse text. This is the fallback rule which successfully parses any non-empty content up to the
/// context's terminal sequence, an emoji, or any of [`Context::allowed_start_sequences`].
///
/// # Errors
/// If the content is empty.
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
}
