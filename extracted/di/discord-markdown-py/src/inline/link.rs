//! Link parsing.
//!
//! All links are [`url::Url`]s, but are highly restricted to prevent abuse.

use std::{borrow::Cow, cell::Cell, fmt::Debug, marker::PhantomData};

use icu_properties::{props::GeneralCategory, CodePointMapData, CodePointMapDataBorrowed};
use itertools::Itertools;
use nom::{
	branch::alt,
	character::{
		complete::{anychar, char},
		satisfy,
	},
	combinator::{map, map_opt, not, opt, peek, recognize},
	multi::many1_count,
	IResult, Parser,
};
use tracing::Level;
use url::{SyntaxViolation, Url};

use crate::{
	context::{Context, TerminalOutput},
	error::ParseError,
	node::SpannedNodes,
	rule::RuleSet,
	span::{Span, TraceOk, TraceParse},
	unparse::Unparse,
	Input,
};

use super::Grammar;

pub mod auto;
pub mod contact;
pub mod detection;
pub mod masked;
pub mod scheme;

/// The subdomains a Discord app domain may carry: the deployment environments, plus `www.`.
pub const APP_SUBDOMAINS: [&str; 3] = ["canary.", "ptb.", "www."];

/// There is no canary `discord.gg`, so the invite and template hosts take only `www.`.
pub const WWW_SUBDOMAIN: [&str; 1] = ["www."];

/// Leading path segments of a Discord app domain that the client routes.
///
/// Sorted for binary search.
pub const APP_PATHS: [&str; 15] = [
	"__development",
	"activities",
	"application-directory",
	"channels",
	"discovery",
	"events",
	"game-servers",
	"game-shop",
	"games",
	"invite",
	"oauth2",
	"quests",
	"shop",
	"template",
	"users",
];

/// What a [`SchemalessDomain`] accepts as a path when no scheme was written.
///
/// Without this, `discord.com/anything at all` reads as a link, which dresses arbitrary text up as
/// something the client would resolve.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PathFilter {
	/// A single invite or template code, as in `discord.gg/discord-developers`.
	Code,
	/// One of these leading segments, or no path at all.
	///
	/// The slice MUST be sorted.
	Segments(&'static [&'static str]),
}

impl PathFilter {
	/// Whether the path of `url` is one this filter accepts.
	#[must_use]
	fn accepts(self, url: &Url) -> bool {
		let Some(segments) = url.path_segments() else {
			return false;
		};
		// A trailing slash and an empty path both yield empty segments.
		let mut segments = segments.filter(|segment| !segment.is_empty());

		match self {
			Self::Code => {
				segments.next().is_some_and(|code| {
					code.chars()
						.all(|ch| ch.is_ascii_alphanumeric() || ch == '-')
				}) && segments.next().is_none()
			}
			// A bare host is a link to Discord itself.
			Self::Segments(allowed) => segments
				.next()
				.is_none_or(|segment| allowed.binary_search(&segment).is_ok()),
		}
	}
}

/// A domain that parses without a scheme, given `https`.
///
/// These exist for `join my discord server at discord.gg/discord-developers`, where the user isn't
/// required to write a scheme. Only the paths the client resolves are worth that convenience, hence
/// the [`PathFilter`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SchemalessDomain {
	/// The registrable domain, e.g. `discord.com`.
	pub domain: &'static str,
	/// Subdomains that may precede [`Self::domain`], with their trailing dots.
	pub subdomains: &'static [&'static str],
	/// The paths this domain accepts without a scheme.
	pub path: PathFilter,
}

impl SchemalessDomain {
	/// Whether `text` begins with this domain.
	///
	/// Only a gate: a prefix match also accepts `discord.company.com`, so [`Self::matches_host`]
	/// is what decides.
	#[must_use]
	fn starts(&self, text: &str) -> bool {
		if text.starts_with(self.domain) {
			return true;
		}

		self.subdomains.iter().any(|subdomain| {
			text.strip_prefix(subdomain)
				.is_some_and(|rest| rest.starts_with(self.domain))
		})
	}

	/// Whether `host` is this domain, give or take an allowed subdomain.
	#[must_use]
	fn matches_host(&self, host: &str) -> bool {
		if host == self.domain {
			return true;
		}

		self.subdomains
			.iter()
			.any(|subdomain| host.strip_prefix(subdomain) == Some(self.domain))
	}
}

/// The domains that do not require a scheme, and the paths each accepts without one.
pub const SCHEMALESS_DOMAINS: [SchemalessDomain; 4] = [
	SchemalessDomain {
		domain: "discord.gg",
		subdomains: &WWW_SUBDOMAIN,
		path: PathFilter::Code,
	},
	SchemalessDomain {
		domain: "discord.new",
		subdomains: &WWW_SUBDOMAIN,
		path: PathFilter::Code,
	},
	SchemalessDomain {
		domain: "discord.com",
		subdomains: &APP_SUBDOMAINS,
		path: PathFilter::Segments(&APP_PATHS),
	},
	SchemalessDomain {
		domain: "discordapp.com",
		subdomains: &APP_SUBDOMAINS,
		path: PathFilter::Segments(&APP_PATHS),
	},
];

/// A plain link with no special significance.
///
/// See [`Link`] for other variants.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct Link<'data, S: Span> {
	/// The text of the link. Never contains emoji or link elements.
	pub text: Option<SpannedNodes<'data, S>>,
	pub url: Url, // TODO: serialize this as struct
	pub title: Option<String>,
}

impl<S: Span> Unparse for Link<'_, S> {
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

/// Whether a character terminates a link.
fn is_terminal_char(ch: char) -> bool {
	matches!(ch, '<' | '.' | ',' | ':' | ';' | '"' | '\'' | ']' | ')') || ch.is_ascii_whitespace()
}

/// Parse a character that terminates a link.
fn parse_terminal_char<'data, E>(data: Input<'data>) -> IResult<Input<'data>, char, E>
where
	E: ParseError<'data>,
{
	nom::error::context("link::parse_terminal_char", satisfy(is_terminal_char))
		.parse_complete(data)
}

/// Parse a link character that is not terminal. A balanced `(…)` group is consumed whole by
/// [`LinkCharsParser`], so any `)` reaching here is unmatched and belongs to the surrounding text
/// unless the link plainly runs past it: `https://discord.com).` ends at `com`.
fn parse_non_terminal_link_chars<'data, E>(
	data: Input<'data>,
) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<'data>,
{
	alt((
		recognize((char(')'), peek(satisfy(|ch| !is_terminal_char(ch))))),
		parse_non_terminal_link_chars_no_close_paren,
	))
	.parse_complete(data)
}

/// Like [`parse_non_terminal_link_chars`] but never consumes `)`. Used inside balanced
/// parentheses, where the enclosing group must find its closing paren on the first try to avoid
/// O(n²) backtracking on URLs with many nested groups (e.g. `key=(value:(nested))`).
///
/// This differs from [`parse_link_char`] by looking ahead and ensuring that the next character is
/// also valid. Since terminal chars are a superset of link chars, this allows for skipping
/// terminal characters if there are 2 valid link chars in a row.
fn parse_non_terminal_link_chars_no_close_paren<'data, E>(
	data: Input<'data>,
) -> IResult<Input<'data>, Input<'data>, E>
where
	E: ParseError<'data>,
{
	alt((
		// confirm following character can capture
		recognize((
			satisfy(|ch| !ch.is_ascii_whitespace() && ch != '<' && ch != ')'),
			peek(parse_link_char),
		)),
		// Otherwise, make sure this character is not the terminal
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
		// This ensures the group's closing char(')') always succeeds without backtracking.
		let non_terminal: fn(Input<'data>) -> IResult<Input<'data>, Input<'data>, E> =
			if self.inside_parens {
				parse_non_terminal_link_chars_no_close_paren
			} else {
				parse_non_terminal_link_chars
			};
		recognize(many1_count(alt((
			// The group's content is optional so that an empty pair -- `prepareForReuse()` --
			// still matches, since `LinkCharsParser` itself demands at least one char.
			recognize((
				char('('),
				opt(LinkCharsParser {
					context: self.context,
					inside_parens: true,
					error: PhantomData,
				}),
				char(')'),
			)),
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
/// [`detection::start_sequence`] which is more restrictive and includes non-schemes.
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
			parse_and_validate_url(input.content, context.allowed_rules)
		}),
	)
}

/// Parse text content as a URL, ensuring that the URL is safe.
///
/// Returns [`None`] if the URL is invalid, either because it is not a URL or because it fails
/// validation.
///
/// Adds a schema to any [`SCHEMALESS_DOMAINS`] before parsing, although an allowed schemaless
/// domain can still fail parsing for other reasons -- including its [`PathFilter`], which only a
/// link written without a scheme has to satisfy. `https://discord.com/developers/docs` is an
/// ordinary URL; `discord.com/developers/docs` is not a link at all.
///
/// The resulting scheme is one of [`scheme::ALL`] that `rules` permits. If it is [`scheme::DEV`],
/// the [`Url::domain`] is one of [`scheme::VALID_DEV_DOMAINS`].
///
/// # Panics
/// If a new [`SyntaxViolation`] has been added upstream without updating the internal logic.
#[must_use]
pub fn parse_and_validate_url(text: &str, rules: RuleSet) -> Option<Url> {
	// if the text contains any suspicious whitespace, this URL is suspicious
	if text.is_empty() || text.chars().any(is_suspicious_whitespace) {
		return None;
	}

	let schemaless = SCHEMALESS_DOMAINS
		.iter()
		.find(|schemaless_domain| schemaless_domain.starts(text));
	let text = match schemaless {
		Some(_) => Cow::Owned(format!("https://{text}")),
		None => Cow::Borrowed(text),
	};

	let has_syntax_violation = Cell::new(false);
	Url::options()
		.syntax_violation_callback(Some(&|violation| {
			match violation {
    			// less than 2 slashes separating the scheme and host
    			// e.g. https:/discord.com -> https://discord.com
				SyntaxViolation::ExpectedDoubleSlash
				// has at least one backslash somewhere in the URL where a forward slash should normally be
				// https://discord.com\app -> https://discord.com/app
				| SyntaxViolation::Backslash
				// tab and new line are not normally part of URLs
				// https://\tdiscord.com -> https://discord.com
				| SyntaxViolation::TabOrNewlineIgnored => {
					has_syntax_violation.set(true);
				}
				// this can change the visual representation (since they will get encoded)
				SyntaxViolation::NonUrlCodePoint
				// we don't allow file scheme at all
				| SyntaxViolation::ExpectedFileDoubleSlash
				| SyntaxViolation::FileWithHostAndWindowsDrive
				// fragments aren't super important for validation
				| SyntaxViolation::NullInFragment
				// this only happens in the path segment, which doesn't get decoded
				| SyntaxViolation::PercentDecode
				// the parser doesn't capture content that begins or ends with whitespace
				| SyntaxViolation::C0SpaceIgnored
				// while this is not recommended, who are we to stop them?
				| SyntaxViolation::EmbeddedCredentials
				| SyntaxViolation::UnencodedAtSign => {}
				_ => panic!("unexpected syntax violation: {violation}")
			}
		}))
		.parse(&text)
		.ok()
		.filter(|url| {
			// All URLs must pass these conditions
			if has_syntax_violation.get() || has_percent_encoded_domain(url.scheme(), &text) {
				return false;
			}

			// A URL that only got its scheme because it looked schemaless has to earn it. The host
			// comes from the parsed URL rather than the prefix that matched above, because a prefix
			// is not a host: `discord.company.com` starts with `discord.com`.
			if let Some(schemaless_domain) = schemaless {
				let is_domain = url
					.host_str()
					.is_some_and(|host| schemaless_domain.matches_host(host));

				if !is_domain
					|| url.port().is_some()
					|| !url.username().is_empty()
					|| url.password().is_some()
					|| !schemaless_domain.path.accepts(url)
				{
					return false;
				}
			}

			scheme::ALL
				.iter()
				.any(|scheme| scheme.allowed_by(rules) && scheme.validate(url))
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
	static CODE_POINTS: CodePointMapDataBorrowed<'static, GeneralCategory> =
		CodePointMapData::new();

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
		CODE_POINTS.get(ch),
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
			map(auto::auto(context.clone()), |url| Link {
				text: None,
				title: None,
				url,
			}),
			contact::contact(context.clone()),
		)),
	)
}

#[cfg(test)]
mod test {
	use url::Url;

	use super::parse_and_validate_url;
	use crate::rule::{Rule, RuleSet};

	/// Validate `s` with every rule allowed.
	fn validate(s: &str) -> Option<Url> {
		parse_and_validate_url(s, RuleSet::all())
	}

	#[test]
	fn valid_url() {
		let s = "https://wnelson.dev";
		let res = validate(s);
		assert_eq!(res, Some(Url::parse(s).unwrap()));
	}

	#[test]
	fn percent_encoded_domain() {
		let s = "https://%64%69%73%63%6F%72%64%2E%67%67";
		let res = validate(s);
		assert_eq!(res, None);
	}

	#[test]
	fn single_slash() {
		let s = "https:/wnelson.dev";
		let res = validate(s);
		assert_eq!(res, None);
	}

	#[test]
	fn no_slash() {
		let s = "https:wnelson.dev";
		let res = validate(s);
		assert_eq!(res, None);
	}

	/// Each of the client's own surfaces is a `dev` domain.
	#[test]
	fn dev_domains() {
		for s in DEV_URLS {
			assert_eq!(validate(s), Some(Url::parse(s).unwrap()), "{s}");
		}

		assert_eq!(validate("dev://nonsense/foo"), None);
	}

	/// A `dev` URL for each surface the client routes.
	const DEV_URLS: [&str; 4] = [
		"dev://branch/main",
		"dev://experiment/foo",
		"dev://playground/mana",
		"dev://devtools/shop_collectibles",
	];

	/// Without [`Rule::DevLink`] a `dev` URL is not a URL at all.
	#[test]
	fn dev_scheme_needs_its_rule() {
		let without_dev = RuleSet::all() - Rule::DevLink;

		for s in DEV_URLS {
			assert_eq!(parse_and_validate_url(s, without_dev), None, "{s}");
		}

		// Only `dev` is gated.
		assert_eq!(
			parse_and_validate_url("https://wnelson.dev", without_dev),
			Some(Url::parse("https://wnelson.dev").unwrap())
		);
		assert_eq!(
			parse_and_validate_url("mailto:tim@apple.com", without_dev),
			Some(Url::parse("mailto:tim@apple.com").unwrap())
		);
	}

	#[test]
	fn invalid_scheme() {
		let s = "foo://bar/baz";
		let res = validate(s);
		assert_eq!(res, None);
	}

	#[test]
	fn suspicious_whitespace() {
		let s = "https://wnelson.dev/foo\u{1160}bar";
		let res = validate(s);
		assert_eq!(res, None);
	}

	#[test]
	fn schemaless_domain() {
		let s = "discord.gg/foo";
		let res = validate(s);
		assert_eq!(res, Some(Url::parse("https://discord.gg/foo").unwrap()));
	}

	#[test]
	fn non_schemaless_domain() {
		let s = "discard.gg/foo";
		let res = validate(s);
		assert_eq!(res, None);
	}

	/// The paths a schemaless domain carries.
	#[test]
	fn schemaless_paths() {
		for s in [
			// an invite or template code, which is all these domains serve
			"discord.gg/discord-developers",
			"discord.new/abc",
			// the app paths, on either domain and any allowed subdomain
			"discord.com/invite/abc",
			"discord.com/channels/1/2/3",
			"discord.com/channels/@me/2",
			"discord.com/shop?tab=orbs",
			"discord.com/invite/abc?event=1",
			"discordapp.com/quests/1",
			"canary.discord.com/quests/1",
			"ptb.discordapp.com/users/1",
			"www.discord.com/games/1/a-slug",
			// no deployment subdomain on these hosts
			"www.discord.gg/abc",
			"www.discord.new/abc",
			// the bare host is a link to Discord itself
			"discord.com",
			"discord.com/",
		] {
			assert_eq!(
				validate(s),
				Some(Url::parse(&format!("https://{s}")).unwrap()),
				"{s}"
			);
		}
	}

	/// A path the client does not route is not worth linking without a scheme.
	#[test]
	fn schemaless_path_must_be_one_the_client_routes() {
		for s in [
			"discord.com/developers/docs",
			// `/shop` has to end the path segment, or the link points somewhere else entirely
			"discord.com/shopping-cart",
			// an invite code is one segment of code characters and nothing else
			"discord.gg/abc/def",
			"discord.gg/a%2Fb",
			"discord.gg",
			// `/invite` is a discord.com path, not a discord.gg one
			"discord.gg/invite/abc",
		] {
			assert_eq!(validate(s), None, "{s}");
		}
	}

	/// The host has to be the domain, not merely start with it: `discord.com` is a prefix of
	/// `discord.company.com`.
	#[test]
	fn schemaless_host_must_be_the_domain() {
		for s in [
			"discord.company.com/invite/abc",
			"discord.gg.evil.com/abc",
			"discord.comfy/invite/abc",
			// a subdomain is only ever one the domain allows
			"evil.discord.com/invite/abc",
			"canary.discord.gg/abc",
			"ptb.discord.new/abc",
			// credentials and ports put the reader somewhere other than where the text reads
			"discord.com:8080/invite/abc",
			"discord.com@evil.com/invite/abc",
		] {
			assert_eq!(validate(s), None, "{s}");
		}
	}

	/// Path filtering applies only to a link written without a scheme.
	#[test]
	fn a_scheme_needs_no_path_filter() {
		for s in [
			"https://discord.com/developers/docs",
			"http://discord.com/shopping-cart",
			"https://discord.company.com/anything",
		] {
			assert_eq!(validate(s), Some(Url::parse(s).unwrap()), "{s}");
		}
	}

	#[test]
	fn app_paths_are_sorted() {
		assert!(super::APP_PATHS.is_sorted());
	}
}
