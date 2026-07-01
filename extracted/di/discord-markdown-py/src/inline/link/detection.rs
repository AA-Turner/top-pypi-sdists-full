use std::{fmt::Debug, marker::PhantomData};

use crate::{
	context::Context,
	error::ParseError,
	span::{Span, TraceOk, TraceParse},
	Input,
};
use nom::{
	branch::alt,
	bytes::complete::tag,
	combinator::{map, peek},
	sequence::preceded,
	Parser,
};
use tracing::Level;

use super::{mention, verify_url, Link, Normal};

pub const OPEN_DELIMITERS: (&str, &str) = ("http", "https");

/// Parse allowed URL schemes for URL detection.
///
/// This is intentially more restrictive than schemes allowed in [`super::parse_and_validate_url`]
/// because we allow a greater range of schemes as URLs than the schemes that we want to
#[allow(clippy::doc_markdown)]
/// automatically detect. For example, \<discord://foo\> is a valid URL but it will not be
/// automatically detected.
///
/// See [`OPEN_DELIMITERS`] for a list of schemes that this considers.
#[must_use]
pub fn valid_schemes<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	alt((tag(OPEN_DELIMITERS.0), tag(OPEN_DELIMITERS.1)))
}

struct DetectionParser<'ctx, S, E> {
	context: &'ctx Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for DetectionParser<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("DetectionParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for DetectionParser<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = Link<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "detection_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		nom::error::context(
			"link::parse_url",
			alt((
				map(mention::mention_link(), Link::Mention),
				map(
					preceded(peek(valid_schemes()), verify_url(self.context)),
					|url| {
						Link::Normal(Normal {
							text: None,
							url,
							title: None,
						})
					},
				),
			)),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse content that is probably a link.
///
/// # Errors
/// If the content is not a valid link for link detection.
#[must_use]
pub fn detection<'ctx, 'data, S, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Link<'data, S>, Error = E> + 'ctx
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	DetectionParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};
	use url::Url;

	use super::detection;
	use crate::context::Context;
	use crate::inline::link::{Link, Normal};
	use crate::test_utils::handle_nom_err;

	#[test]
	fn invalid_url() {
		let s = "foobar";
		detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("unable to parse");
	}

	#[test]
	fn complex_url() {
		let s = "https://en.wikipedia.org/wiki/Endemic_(epidemiology)";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)").unwrap(),
				text: None,
				title: None,
			})
		);
	}

	#[test]
	fn url_with_terminal() {
		let s = "https://wnelson.dev.";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, ".");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: None,
				title: None,
			})
		);
	}

	// (stuff https://google.com) <-- not include
	// https://google.com/cat(s) <-- should include
	// https://google.com/bob)a <-- should include

	#[test]
	fn url_avoids_including_unmatched_terminal_parenthesis() {
		let s = "https://google.com)";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, ")");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://google.com").unwrap(),
				text: None,
				title: None,
			})
		);
	}

	#[test]
	fn allows_terminal_parenthesis_when_matched() {
		let s = "https://google.com/search?q=cat(s)";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://google.com/search?q=cat(s)").unwrap(),
				text: None,
				title: None,
			})
		);
	}

	#[test]
	fn continues_with_unmatched_parenthesis_when_not_followed_by_terminal_char() {
		let s = "https://google.com/search?q=cat)thing";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://google.com/search?q=cat)thing").unwrap(),
				text: None,
				title: None,
			})
		);
	}

	#[test]
	#[ntest::timeout(1000)]
	fn deeply_nested_parens_in_query_string() {
		// URLs with many nested paren groups (e.g. Datadog qson params) must parse in O(n) time.
		let s = "https://example.com/?a=qson:(data:(x:1,y:2),v:0)&b=qson:(data:(p:(selected:count),q:(selected:count),r:(selected:p95),topN:5),v:0)&c=qson:(data:(visible:true,hits:(selected:total),errors:(selected:total),latency:(selected:p95)),v:1)";
		let (rem, res) = detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse(s).unwrap(),
				text: None,
				title: None
			})
		);
	}
}
