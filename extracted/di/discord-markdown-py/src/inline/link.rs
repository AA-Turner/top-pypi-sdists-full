use std::{cell::Cell, fmt::Debug, marker::PhantomData};

use icu_properties::{props::GeneralCategory, CodePointMapData};
use itertools::Itertools;
use nom::{
	branch::alt,
	character::{
		complete::{anychar, char},
		satisfy,
	},
	combinator::{map, map_opt, not, peek, recognize},
	multi::many1_count,
	sequence::delimited,
	IResult, Parser,
};
use tracing::Level;
use url::{SyntaxViolation, Url};

use crate::{
	context::{Context, TerminalOutput},
	error::ParseError,
	node::SpannedNodes,
	span::{Span, TraceOk, TraceParse},
	unparse::Unparse,
	Input,
};

use super::Grammar;

pub mod auto;
pub mod detection;
pub mod masked;
pub mod mention;

#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum Link<'data, S: Span> {
	Mention(mention::MentionLink),
	Normal(Normal<'data, S>),
}

impl<S: Span> Unparse for Link<'_, S> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self::Mention(mention) => Unparse::fmt(mention, f),
			Self::Normal(normal) => Unparse::fmt(normal, f),
		}
	}
}

/// A link element.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Normal<'data, S: Span> {
	/// The text of the link. Never contains emoji or link elements.
	pub text: Option<SpannedNodes<'data, S>>,
	pub url: Url, // TODO: serialize this as struct
	pub title: Option<String>,
}

impl<S: Span> Unparse for Normal<'_, S> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		match self {
			Self {
				text: None,
				url,
				title: None,
				// TODO: retain whether the link came from auto or detection
			} => write!(f, "{url}"),
			Self {
				text: Some(text),
				url,
				title: None,
			} => write!(f, "[{}]({})", text.unparse(), url),
			Self {
				text: Some(text),
				url,
				title: Some(title),
			} => write!(f, "[{}]({} {})", text.unparse(), url, title),
			Self {
				text: None,
				title: Some(_),
				..
			} => unreachable!("a link cannot have a title with no text"),
		}
	}
}

/// Parse a valid character that can belong to a link.
// ^((?:https?|steam):\/\/[^\s<]+[^<.,:;"'\]\s])
fn parse_link_char<'data, E>(data: Input<'data>) -> IResult<Input<'data>, char, E>
where
	E: ParseError<'data>,
{
	nom::error::context(
		"link::parse_link_char",
		satisfy(|ch| !ch.is_ascii_whitespace() && ch != '<'),
	)
	.parse_complete(data)
}

/// Parse a character that terminates a link.
fn parse_terminal_char<'data, E>(data: Input<'data>) -> IResult<Input<'data>, char, E>
where
	E: ParseError<'data>,
{
	nom::error::context(
		"link::parse_terminal_char",
		satisfy(|ch| {
			matches!(ch, '<' | '.' | ':' | ';' | '"' | '\'' | ']' | ')') || ch.is_ascii_whitespace()
		}),
	)
	.parse_complete(data)
}

/// Parse a link character that is not terminal. This differs from [`parse_link_char`] by looking
/// ahead and ensuring that the next character is also valid. Since terminal chars are a superset
/// of link chars, this allows for skipping terminal characters if there are 2 valid link chars in
/// a row.
fn parse_non_terminal_link_chars<'data, E>(
	data: Input<'data>,
) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<'data>,
{
	alt((
		// confirm following character can capture
		recognize((parse_link_char, peek(parse_link_char))),
		// Otherwise, make sure this character is not the terminal
		recognize((not(peek(parse_terminal_char)), anychar)),
	))
	.parse_complete(data)
}

/// Like [`parse_non_terminal_link_chars`] but used inside balanced parentheses. Excludes `)` from
/// branch 1 so that the enclosing `delimited` can always find its closing paren on the first try,
/// preventing O(n²) backtracking when URLs contain many nested paren groups (e.g. query strings
/// with `key=(value:(nested))`).
fn parse_non_terminal_link_chars_inner<'data, E>(
	data: Input<'data>,
) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<'data>,
{
	alt((
		recognize((
			satisfy(|ch| !ch.is_ascii_whitespace() && ch != '<' && ch != ')'),
			peek(parse_link_char),
		)),
		recognize((not(peek(parse_terminal_char)), anychar)),
	))
	.parse_complete(data)
}

struct LinkCharsParser<'ctx, E> {
	context: &'ctx Context,
	/// True when this parser was spawned inside a `(…)` balanced-paren group. Controls which
	/// variant of the non-terminal link char parser is used.
	inside_parens: bool,
	error: PhantomData<E>,
}

impl<E> Clone for LinkCharsParser<'_, E> {
	fn clone(&self) -> Self {
		Self {
			context: self.context,
			inside_parens: self.inside_parens,
			error: PhantomData,
		}
	}
}

impl<E> Debug for LinkCharsParser<'_, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("LinkCharsParser")
			.field("context", &self.context)
			.field("inside_parens", &self.inside_parens)
			.field("error", &self.error)
			.finish()
	}
}

impl<'ctx, 'data, E> Parser<Input<'data>> for LinkCharsParser<'ctx, E>
where
	E: ParseError<'data> + 'ctx,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "link_chars_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		// Inside balanced parens, use the stricter variant so ) is never consumed as a link char.
		// This ensures delimited(..., char(')')) always succeeds without backtracking.
		let non_terminal: fn(Input<'data>) -> IResult<Input<'data>, Input<'data>, E> =
			if self.inside_parens {
				parse_non_terminal_link_chars_inner
			} else {
				parse_non_terminal_link_chars
			};
		recognize(many1_count(alt((
			delimited(
				char('('),
				LinkCharsParser {
					context: self.context,
					inside_parens: true,
					error: PhantomData,
				},
				char(')'),
			),
			self.context
				.guard_terminal_sequence(move || non_terminal)
				.map(TerminalOutput::inner),
		))))
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse content that is considered part of the link.
fn link_chars<'ctx, 'data, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E> + 'ctx
where
	E: ParseError<'data> + 'ctx,
{
	LinkCharsParser {
		context,
		inside_parens: false,
		error: PhantomData,
	}
}

/// Parse a URL and verify that it has valid schemes. This is _not_ the same as
/// [`detection::valid_schemes`] which is more restrictive.
#[must_use]
pub fn verify_url<'ctx, 'data: 'ctx, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Url, Error = E> + 'ctx
where
	E: ParseError<'data> + 'ctx,
{
	nom::error::context(
		"link::verify_url",
		map_opt(link_chars(context), |input| {
			parse_and_validate_url(&input.content)
		}),
	)
}

/// Parse text content as a URL. Returns None if the URL is invalid, either because it is not a URL
/// or because it fails validation.
#[must_use]
pub fn parse_and_validate_url(text: &str) -> Option<Url> {
	for ch in text.chars() {
		// if the text contains any suspicious whitespace, this URL is suspicious
		if is_suspicious_whitespace(ch) {
			return None;
		}
	}

	let has_syntax_violation = Cell::new(false);
	Url::options()
		.syntax_violation_callback(Some(&|violation| {
			if matches!(
				violation,
				// less than 2 slashes separating the scheme and host
				// e.g. https:/discord.com -> https://discord.com
				SyntaxViolation::ExpectedDoubleSlash
					// has at least one backslash somewhere in the URL where a forward slash should normally be
					// https://discord.com\app -> https://discord.com/app
					| SyntaxViolation::Backslash
					// tab and new line are not normally part of URLs
					// https://\tdiscord.com -> https://discord.com
					| SyntaxViolation::TabOrNewlineIgnored,
				// we allow:
				// - NonUrlCodePoint: this can change the visual representation (since they will get encoded)
				//   but isn't an abuse vector
				// - NullInFragment: fragments aren't super important for validation
				// - PercentDecode: this only happens in the path segment, which doesn't get decoded
				// - C0SpaceIgnored: the parser doesn't capture content that begins or ends with whitespace
				// - EmbeddedCredentials: while this is not recommended, who are we to stop them?
			) {
				has_syntax_violation.set(true);
			}
		}))
		.parse(text)
		.ok()
		.filter(|url| {
			matches!(url.scheme(), "http" | "https" | "discord")
				&& url.has_host()
				&& !url.cannot_be_a_base()
				&& !has_percent_encoded_domain(url.scheme(), text)
				&& !has_syntax_violation.get()
		})
}

/// Manually parse the host section of the URL from `url_str` and return whether it has any
/// percent-encoded characters in it. This is a best-effort attempt and is not URL-compliant.
fn has_percent_encoded_domain(scheme: &str, url_str: &str) -> bool {
	// we can assume 2 slashes are present because we validate this assumption before calling this function
	let scheme_and_separator = format!("{scheme}://");

	if let Some(host_start) = url_str.find(&scheme_and_separator) {
		let after_scheme = &url_str[host_start + scheme_and_separator.len()..];

		let host_end = after_scheme.find('/').unwrap_or(after_scheme.len());

		let raw_host = &after_scheme[..host_end];
		contains_percent_encoding(raw_host)
	} else {
		false
	}
}

/// Check whether the string contains any percent-encoded characters.
fn contains_percent_encoding(s: &str) -> bool {
	s.chars().tuple_windows().any(|(first, second, third)| {
		first == '%' && second.is_ascii_hexdigit() && third.is_ascii_hexdigit()
	})
}

/// Check whether a character is considered suspicious whitespace. Suspicious whitespace includes
/// the following Unicode categories, excluding \n and space:
///
/// - [`GeneralCategory::Format`]
/// - [`GeneralCategory::LineSeparator`]
/// - [`GeneralCategory::Control`]
/// - [`GeneralCategory::SpaceSeparator`]
///
/// Some other characters not normally included in these sets are manually included.
fn is_suspicious_whitespace(ch: char) -> bool {
	if matches!(ch, '\n' | ' ') {
		return false;
	}

	matches!(
		ch,
		'\u{034f}' | // combining grapheme joiner
		'\u{17b4}' | // khmer vowel inherent aq
		'\u{17b5}' | // khmer vowel inherent aa
		'\u{1160}' | // hangul filler {jungseong}
		'\u{3164}' | // hangul filler {chauem}
		'\u{ffa0}' // halfwidth hangurl filler
	) || matches!(
		CodePointMapData::new().get(ch),
		GeneralCategory::Format
			| GeneralCategory::LineSeparator
			| GeneralCategory::ParagraphSeparator
			| GeneralCategory::Control
			| GeneralCategory::SpaceSeparator
	)
}

/// Parse a URL.
///
/// # Errors
/// If the content does not begin with a URL.
#[must_use]
pub fn link<'ctx, 'data, S, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Link<'data, S>, Error = E> + 'ctx
where
	S: Span,
	E: ParseError<'data> + 'ctx,
	'data: 'ctx,
{
	nom::error::context(
		"link::parse_inline",
		alt((
			masked::masked(context),
			detection::detection(context),
			map(auto::auto(context.clone()), |url| {
				Link::Normal(Normal {
					text: None,
					title: None,
					url,
				})
			}),
		)),
	)
}

#[cfg(test)]
mod test {
	use url::Url;

	use super::parse_and_validate_url;

	#[test]
	fn valid_url() {
		let s = "https://wnelson.dev";
		let res = parse_and_validate_url(s);
		assert_eq!(res, Some(Url::parse(s).unwrap()));
	}

	#[test]
	fn percent_encoded_domain() {
		let s = "https://%64%69%73%63%6F%72%64%2E%67%67";
		let res = parse_and_validate_url(s);
		assert_eq!(res, None);
	}

	#[test]
	fn single_slash() {
		let s = "https:/wnelson.dev";
		let res = parse_and_validate_url(s);
		assert_eq!(res, None);
	}

	#[test]
	fn no_slash() {
		let s = "https:wnelson.dev";
		let res = parse_and_validate_url(s);
		assert_eq!(res, None);
	}

	#[test]
	fn invalid_scheme() {
		let s = "foo://bar/baz";
		let res = parse_and_validate_url(s);
		assert_eq!(res, None);
	}

	#[test]
	fn suspicious_whitespace() {
		let s = "https://wnelson.dev/foo\u{1160}bar";
		let res = parse_and_validate_url(s);
		assert_eq!(res, None);
	}
}
