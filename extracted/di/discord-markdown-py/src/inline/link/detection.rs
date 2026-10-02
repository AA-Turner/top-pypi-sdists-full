//! Link detection parsing
//!
//! This module attempts to parse link content from otherwise unmarked content.

use std::{fmt::Debug, marker::PhantomData};

use crate::{
	context::Context,
	error::ParseError,
	inline::link::scheme,
	span::{Span, TraceOk, TraceParse},
	util::iter_alt,
	Input,
};
use nom::{
	branch::alt,
	bytes::complete::tag,
	combinator::{map, peek},
	error::ErrorKind,
	sequence::preceded,
	Mode, Parser,
};
use tracing::Level;
use url::Url;

use super::{verify_url, Link};

/// Host prefixes that are enough to know a run of text might be a link written without a scheme.
///
/// These are deliberately longer than the subdomains in [`super::APP_SUBDOMAINS`]: `www.` or
/// `canary.` on their own would make every such word in a message a detection candidate, and each
/// candidate costs a full scan of the link characters that follow it.
pub const HOST_START_SEQUENCES: [&str; 7] = [
	"discord.gg",
	"discord.new",
	"discord.com",
	"discordapp.com",
	"canary.discord",
	"ptb.discord",
	"www.discord",
];

/// Parse a valid starting sequence for URL detection.
///
/// This is intentially more restrictive than schemes allowed in [`super::parse_and_validate_url`]
/// because we allow a greater range of schemes as URLs than the schemes that we want to
/// automatically detect. For example, `<discord://foo>` is a valid URL but it will not be
/// automatically detected.
#[must_use]
pub fn start_sequence<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	alt((
		iter_alt(|| scheme::DETECTED.iter().map(|scheme| tag(scheme.name()))),
		// A schemaless host is the only start sequence that carries no delimiter of its own, so
		// it is the only one that can begin in the middle of a word. Requiring a token boundary
		// is what keeps `getscammeddiscord.gg/x` from lending a scam domain a real invite, and
		// what keeps `ftp://discord.gg/x` from having its scheme quietly dropped.
		preceded(
			at_token_start(),
			iter_alt(|| HOST_START_SEQUENCES.into_iter().map(tag)),
		),
	))
}

/// Match, without consuming anything, only where the preceding character cannot continue a token.
///
/// That means the start of the parse or a whitespace character. A zero-width space is deliberately
/// not whitespace: `getscammed<ZWSP>discord.gg/x` reads as one token, and U+200B is not
/// `White_Space`.
#[must_use]
pub fn at_token_start<'data, E>() -> impl Parser<Input<'data>, Output = (), Error = E>
where
	E: ParseError<'data>,
{
	AtTokenStart(PhantomData)
}

/// The parser behind [`at_token_start`].
struct AtTokenStart<E>(PhantomData<E>);

impl<E> Debug for AtTokenStart<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.write_str("AtTokenStart")
	}
}

impl<'data, E> Parser<Input<'data>> for AtTokenStart<E>
where
	E: ParseError<'data>,
{
	type Output = ();
	type Error = E;

	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		#[allow(
			deprecated,
			reason = "preceding_char is implemented specifically for coded links"
		)]
		match input.preceding_char() {
			None => Ok((input, OM::Output::bind(|| ()))),
			Some(ch) if ch.is_whitespace() => Ok((input, OM::Output::bind(|| ()))),
			Some(_) => Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Verify)
			}))),
		}
	}
}

/// Parse a URL at a position that could begin one.
///
/// The [`start_sequence`] gate is not an optimization: [`verify_url`] leads with
/// [`super::link_chars`], which is O(n) in the run after it, so it must not run at a position that
/// cannot begin a link at all.
#[must_use]
pub fn url<'ctx, 'data: 'ctx, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Url, Error = E> + 'ctx
where
	E: ParseError<'data> + 'ctx,
{
	preceded(peek(start_sequence()), verify_url(context))
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
			map(url(self.context), |url| Link {
				text: None,
				url,
				title: None,
			}),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse content that starts with content that can be parsed into a URL.
///
/// For example, this will pull the URL out of `https://discord.com hello world`, leaving the
/// remaining content as ` hello world`.
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
	use crate::inline::link::Link;
	use crate::test_utils::handle_nom_err;

	/// Parse `s` as a detected link, expecting it to succeed.
	fn parse(s: &str) -> (crate::Input<'_>, Link<'_, ()>) {
		detection::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse")
	}

	/// Build the expectation for a text-less link.
	fn url(s: &str) -> Link<'_, ()> {
		Link {
			text: None,
			url: Url::parse(s).unwrap(),
			title: None,
		}
	}

	/// [`super::HOST_START_SEQUENCES`] is what makes a schemaless domain reachable at all, so a
	/// domain -- or a subdomain of one -- that no sequence covers is dead weight in the table.
	#[test]
	fn start_sequences_cover_every_schemaless_domain() {
		use crate::inline::link::SCHEMALESS_DOMAINS;

		let covers = |host: &str| {
			super::HOST_START_SEQUENCES
				.iter()
				.any(|sequence| host.starts_with(sequence))
		};

		for domain in SCHEMALESS_DOMAINS {
			assert!(covers(domain.domain), "{}", domain.domain);

			for subdomain in domain.subdomains {
				let host = format!("{subdomain}{}", domain.domain);
				assert!(covers(&host), "{host}");
			}
		}
	}

	#[test]
	fn schemaless_invite() {
		let s = "discord.gg/discord-developers";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url("https://discord.gg/discord-developers"));
	}

	/// The terminal character rules apply to a schemaless link exactly as they do to a URL.
	#[test]
	fn schemaless_link_leaves_trailing_terminal() {
		let s = "discord.gg/abc.";
		let (rem, res) = parse(s);
		assert_eq!(rem, ".");
		assert_eq!(res, url("https://discord.gg/abc"));
	}

	#[test]
	fn schemaless_link_on_subdomains() {
		for s in [
			"discord.com/quests/1",
			"discordapp.com/quests/1",
			"canary.discord.com/quests/1",
			"ptb.discord.com/quests/1",
			"www.discordapp.com/quests/1",
			"www.discord.gg/abc",
		] {
			let (rem, res) = parse(s);
			assert_eq!(rem, "", "{s}");
			assert_eq!(res, url(&format!("https://{s}")), "{s}");
		}
	}

	/// A path the client does not route is not a schemaless link, so there is nothing to detect.
	#[test]
	fn schemaless_link_needs_a_path_the_client_routes() {
		for s in [
			"discord.com/developers/docs",
			"discord.com/shopping-cart",
			// `discord.com` is a prefix of this host, but it is not this host
			"discord.company.com/invite/abc",
		] {
			detection::<(), _>(&Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect_err("able to parse");
		}
	}

	/// A scheme skips the path filter.
	#[test]
	fn non_routed_discord_path_with_a_scheme_stays_a_url() {
		let s = "https://discord.com/developers/docs";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url(s));
	}

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
			Link {
				url: Url::parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)").unwrap(),
				text: None,
				title: None,
			}
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
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: None,
				title: None,
			}
		);
	}

	/// A comma ends a link the way any other terminal character does, but only at the end: a
	/// comma between two link characters is part of the URL.
	#[test]
	fn url_with_trailing_comma() {
		let (rem, res) = parse("https://google.com/foo,");
		assert_eq!(rem, ",");
		assert_eq!(res, url("https://google.com/foo"));

		let s = "https://google.com/foo,bar";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url(s));
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
			Link {
				url: Url::parse("https://google.com").unwrap(),
				text: None,
				title: None,
			}
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
			Link {
				url: Url::parse("https://google.com/search?q=cat(s)").unwrap(),
				text: None,
				title: None,
			}
		);
	}

	/// A pair only holds together over characters a link can contain, so whitespace ends the link
	/// where it falls rather than being swallowed by the surrounding parens.
	#[test]
	fn parenthesis_does_not_span_whitespace() {
		let s = "https://google.com/(cat s)";
		let (rem, res) = parse(s);
		assert_eq!(rem, " s)");
		assert_eq!(res, url("https://google.com/(cat"));
	}

	/// An empty pair is still a matched pair, so a trailing `()` belongs to the URL.
	#[test]
	fn allows_terminal_empty_parentheses() {
		let s = "https://developer.apple.com/documentation/uikit/uitableviewcell/prepareforreuse()";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url(s));
	}

	/// A URL that plainly runs past an unmatched `)` keeps it -- terminating there would cut a
	/// real path short.
	#[test]
	fn continues_with_unmatched_parenthesis_when_not_followed_by_terminal_char() {
		let s = "https://google.com/search?q=cat)thing";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url(s));
	}

	/// An unmatched `)` is part of the sentence, not the URL, so it ends the link even when more
	/// characters follow it.
	#[test]
	fn unmatched_parenthesis_before_punctuation_ends_link() {
		for s in [
			"https://discord.com).",
			"https://discord.com),",
			"https://discord.com)\".",
			"https://discord.com).x",
			"https://discord.com))x",
		] {
			let (_, res) = parse(s);
			assert_eq!(res, url("https://discord.com"), "{s}");
		}

		let (rem, _) = parse("https://discord.com).");
		assert_eq!(rem, ").");
	}

	/// The paren a group closes is matched, so only the extra one terminates the link.
	#[test]
	fn matched_parentheses_survive_trailing_punctuation() {
		let (rem, res) = parse("https://google.com/search?q=cat(s).");
		assert_eq!(rem, ".");
		assert_eq!(res, url("https://google.com/search?q=cat(s)"));

		let (rem, res) = parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)).");
		assert_eq!(rem, ").");
		assert_eq!(res, url("https://en.wikipedia.org/wiki/Endemic_(epidemiology)"));
	}

	#[test]
	// see the note on the timeout tests in `crate::test` for why debug gets a larger budget
	#[cfg_attr(debug_assertions, ntest::timeout(3000))]
	#[cfg_attr(not(debug_assertions), ntest::timeout(1000))]
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
			Link {
				url: Url::parse(s).unwrap(),
				text: None,
				title: None
			}
		);
	}
}
