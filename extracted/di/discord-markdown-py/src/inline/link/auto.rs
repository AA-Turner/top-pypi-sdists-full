//! Auto-link parsing
//!
//! Note that this is _not_ [`crate::inline::link::detection`]. Auto-links are links inside angle
//! brackets, such as `<https://discord.com>`.

use std::{fmt::Debug, marker::PhantomData};

use nom::{character::complete::char, error::ErrorKind, sequence::delimited, Mode, Parser};
use tracing::Level;
use url::Url;

use crate::{
	context::Context,
	error::ParseError,
	grammar::{ByteHint, Grammar},
	span::{TraceOk, TraceParse},
	Input,
};

use super::verify_url;

/// The terminal character of an auto-link.
pub const TERMINAL: u8 = b'>';

struct AutoParser<E> {
	context: Context,
	error: PhantomData<E>,
}

impl<E> Debug for AutoParser<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("AutoParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for AutoParser<E>
where
	E: ParseError<'data>,
{
	type Output = Url;
	type Error = E;

	#[tracing::instrument(name = "auto_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		if *self.context.hints.get(&Grammar::AutoLink) == ByteHint::Absent {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Alt)
			})));
		}
		nom::error::context(
			"link::auto",
			delimited(char('<'), verify_url(&self.context), char('>')),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse auto-link content.
///
/// # Errors
/// If the content does not begin with an auto-link.
#[must_use]
pub fn auto<'data, E>(context: Context) -> impl Parser<Input<'data>, Output = Url, Error = E>
where
	E: ParseError<'data>,
{
	AutoParser {
		context: context.with_grammar(Grammar::AutoLink),
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{test_utils::handle_nom_err, Context};

	use super::auto;

	#[test]
	fn simple_link() {
		let s = "<https://wnelson.dev>";
		let (rem, res) = auto(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "https://wnelson.dev".parse().unwrap());
	}

	/// A schemaless link is still schemaless inside an autolink.
	#[test]
	fn schemaless_link() {
		let s = "<discord.gg/abc>";
		let (rem, res) = auto(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "https://discord.gg/abc".parse().unwrap());
	}

	#[test]
	fn tel_link() {
		let s = "<tel:+1-800-588-2300>";
		let (rem, res) = auto(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "tel:+1-800-588-2300".parse().unwrap());
	}

	/// A path the client does not route is not schemaless, so there is no URL here at all.
	#[test]
	fn schemaless_non_routed_link_is_rejected() {
		let s = "<discord.com/developers/docs>";
		auto(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}
}
