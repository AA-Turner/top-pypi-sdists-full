//! Link parsing.
//!
//! All links are [`url::Url`]s, but are highly restricted to prevent abuse.

use std::{borrow::Cow, cell::Cell, collections::HashSet};

use derive_where::derive_where;
use icu_properties::{CodePointMapData, CodePointMapDataBorrowed, props::GeneralCategory};
use itertools::Itertools;
use url::{SyntaxViolation, Url};

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	input::token,
	lossless::TokenKind,
	node::{Element, Elements, Sequence},
	scope::Scope,
	span::{Span, Spanned, Trace},
};

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
	/// One of these leading segments.
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
			// A bare host is just the name of the site, not a link to anything in particular.
			Self::Segments(allowed) => segments
				.next()
				.is_some_and(|segment| allowed.binary_search(&segment).is_ok()),
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

	/// Whether `text` begins with this domain, give or take an allowed subdomain, with nothing
	/// after it that carries on the host.
	///
	/// Unlike [`Self::starts`], this turns away `discord.company.com` before anything parses it: an
	/// ASCII letter, digit or `-` after the domain can only make the host a different one, which
	/// [`Self::matches_host`] would reject. Anything else is left for the parse to decide.
	#[must_use]
	pub fn begins_host(&self, text: &str) -> bool {
		let text = self
			.subdomains
			.iter()
			.find_map(|subdomain| text.strip_prefix(subdomain))
			.unwrap_or(text);

		text.strip_prefix(self.domain).is_some_and(|rest| {
			!rest
				.bytes()
				.next()
				.is_some_and(|byte| byte.is_ascii_alphanumeric() || byte == b'-')
		})
	}

	/// Whether the authority of `url`, which was parsed from a link written without a scheme, is
	/// this domain and nothing else: the host, give or take an allowed subdomain, with no port or
	/// credentials to put the reader somewhere other than where the text reads.
	#[must_use]
	fn is_authority_of(&self, url: &Url) -> bool {
		url.host_str().is_some_and(|host| self.matches_host(host))
			&& url.port().is_none()
			&& url.username().is_empty()
			&& url.password().is_none()
	}

	/// The bytes that can begin this domain, with or without one of its subdomains.
	pub fn first_bytes(&self) -> impl Iterator<Item = u8> {
		std::iter::once(self.domain)
			.chain(self.subdomains.iter().copied())
			.filter_map(|start| start.bytes().next())
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

/// The schemaless domain `text` begins with, if it begins with one.
///
/// Only a gate, as [`SchemalessDomain::starts`] is.
fn schemaless_domain(text: &str) -> Option<&'static SchemalessDomain> {
	SCHEMALESS_DOMAINS
		.iter()
		.find(|schemaless_domain| schemaless_domain.starts(text))
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
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound(
		serialize = "N: serde::Serialize",
		deserialize = "N: serde::Deserialize<'de>"
	))
)]
pub struct Link<S: Span, N> {
	/// The text of the link. Never contains emoji or link elements.
	pub text: Option<Sequence<S, N>>,
	pub url: Url, // TODO: serialize this as struct
	pub title: Option<String>,
}

/// A parsed link, with the syntax it was written with outside its text.
pub type ParsedLink<'data, S> = (Link<S, Element<'data, S>>, <S as Span>::Syntax);

/// Whether a character can belong to a link.
// ^((?:https?|steam):\/\/[^\s<]+[^<.,:;"'\]\s])
fn is_link_char(ch: char) -> bool {
	!ch.is_ascii_whitespace() && ch != '<'
}

/// Whether a character is punctuation that a link can contain but not end with. That includes
/// modifier delimiters, so `**https://discord.com**` is a bold link, while `foo_bar` and
/// `Endemic_(epidemiology)` stay inside one.
fn is_trailing_punctuation(ch: char) -> bool {
	matches!(
		ch,
		'.' | ',' | ':' | ';' | '"' | '\'' | ']' | '*' | '_' | '~' | '|'
	)
}

/// Whether a character terminates a link.
fn is_terminal_char(ch: char) -> bool {
	is_trailing_punctuation(ch) || matches!(ch, '<' | ')') || ch.is_ascii_whitespace()
}

/// Whether `byte` is a link character that [`link_chars_run`] takes without a second look: printable
/// ASCII that cannot end a link, open or close a group, or begin the terminal of any scope.
fn is_plain_link_byte(byte: u8) -> bool {
	byte.is_ascii_graphic()
		&& !is_trailing_punctuation(char::from(byte))
		&& !matches!(byte, b'<' | b'>' | b'(' | b')' | b'[')
}

/// Consume a link character that is not terminal. A balanced `(…)` group is consumed whole by
/// [`link_chars_run`], so any `)` reaching here is unmatched and belongs to the surrounding text
/// unless the link plainly runs past it: `https://discord.com).` ends at `com`.
fn non_terminal_link_chars(input: &mut Input) -> PResult<()> {
	if let Some(after) = input.strip_prefix(')')
		&& after.chars().next().is_some_and(|ch| !is_terminal_char(ch))
	{
		input.advance(1);
		return Ok(());
	}

	// A run of punctuation only belongs to the link if the link carries on past it:
	// `https://discord.com.).` ends at `com`, while `https://discord.com.)x` does not.
	let punctuation = input.take_while(is_trailing_punctuation).len();
	if punctuation > 0 {
		return if input.matches(non_terminal_link_chars)? {
			Ok(())
		} else {
			Err(Fail::NoMatch)
		};
	}

	non_terminal_char(input)
}

/// Like [`non_terminal_link_chars`] but never consumes `)`. Used inside balanced parentheses,
/// where the enclosing group must find its closing paren on the first try to avoid O(n²)
/// backtracking on URLs with many nested groups (e.g. `key=(value:(nested))`).
///
/// A run of punctuation is consumed whole, and only when a link character follows it, so the
/// link can carry on through `foo..bar` without picking up the `..` in `foo..`. Inside a group
/// that following character can be the group's closing `)`, which keeps `(foo.)` together.
fn non_terminal_link_chars_no_close_paren(input: &mut Input) -> PResult<()> {
	let punctuation = input.take_while(is_trailing_punctuation).len();
	if punctuation > 0 {
		return if input.peek().is_some_and(is_link_char) {
			Ok(())
		} else {
			Err(Fail::NoMatch)
		};
	}

	non_terminal_char(input)
}

/// Whether `input` begins with a run of punctuation that ends in the `](` between a masked link's
/// text and its destination.
///
/// A link written without delimiters ends there. Otherwise a masked link that is not one, like
/// `[https://example.com/](foobar)`, leaves its text to be read as a link to
/// `https://example.com/](foobar)`, masked link syntax and all.
fn opens_destination(input: &Input) -> bool {
	// every trailing punctuation character is ASCII
	let bytes = input.as_bytes();
	let punctuation = bytes
		.iter()
		.take_while(|&&byte| is_trailing_punctuation(char::from(byte)))
		.count();
	punctuation > 0
		&& bytes[punctuation - 1] == masked::TEXT_TERMINAL
		&& bytes.get(punctuation) == Some(&masked::LINK_OPENER)
}

/// Consume a single character that cannot terminate a link.
fn non_terminal_char(input: &mut Input) -> PResult<()> {
	input.satisfy(|ch| !is_terminal_char(ch)).map(|_| ())
}

/// Consume a run of link characters, at least one, with any balanced `(…)` groups in it.
///
/// Groups nest without recursion: `opens` holds the offset of each `(` still waiting for its `)`.
/// A group whose content stops anywhere but a `)` is unclosed, and so is every group around it,
/// since each would carry on from that `(` exactly as its content did. They all go into
/// `unclosed`, never to be tried again, and the run resumes at the outermost of them as an
/// ordinary character. Retrying them instead makes `https://a.b/((((…x` re-scan every level
/// inside each one, which is exponential in the nesting.
///
/// The run stops early once it reaches `reach` outside every group. Nothing it has consumed there
/// can be given back, since a group only ever rewinds to its own `(`, so the whole run would end
/// at or past that point: a run that stops short of `reach` is the whole run, and one that does
/// not reads only as far as it has to.
fn link_chars_run(input: &mut Input, context: &Context, reach: usize) -> PResult<()> {
	// Inside balanced parens, use the stricter variant so ) is never consumed as a link char.
	// This ensures the group's closing `)` always matches without backtracking. A masked link's
	// URL is closed by `)` the same way, so punctuation right before it stays in the URL rather
	// than leaving the masked link without its closing paren.
	let outer_non_terminal = if context.scope == Scope::MaskedLinkLink {
		non_terminal_link_chars_no_close_paren
	} else {
		non_terminal_link_chars
	};
	// Delimiters say where these URLs end, so `](` inside one is just part of the URL.
	let delimited = matches!(context.scope, Scope::AutoLink | Scope::MaskedLinkLink);

	let start = input.start;
	let mut opens = Vec::new();
	let mut outermost = *input;
	let mut unclosed = HashSet::new();
	loop {
		if opens.is_empty() && input.start >= reach {
			break;
		}

		let plain = input
			.bytes()
			.take_while(|&byte| is_plain_link_byte(byte))
			.count();
		if plain > 0 {
			input.advance(plain);
			continue;
		}

		let at_open = input.peek() == Some('(');
		if at_open && !unclosed.contains(&input.start) {
			if opens.is_empty() {
				outermost = *input;
			}
			opens.push(input.start);
			input.advance(1);
			continue;
		}

		let inside_parens = !opens.is_empty();
		let non_terminal = if inside_parens {
			non_terminal_link_chars_no_close_paren
		} else {
			outer_non_terminal
		};
		// an unclosed `(` ends the group it is in
		let ends = (inside_parens && at_open)
			|| (!delimited && opens_destination(input))
			|| context.at_terminal(input)
			|| input.attempt(non_terminal)?.is_none();
		if !ends {
			continue;
		}

		if !inside_parens {
			break;
		}
		// an empty pair -- `prepareForReuse()` -- closes too
		if input.eat(")") {
			opens.pop();
		} else {
			unclosed.extend(opens.drain(..));
			*input = outermost;
		}
	}

	if input.start == start {
		Err(Fail::NoMatch)
	} else {
		Ok(())
	}
}

/// Parse content that is considered part of the link.
///
/// Each scan costs a unit of fuel, whether or not what it reads turns out to be a URL: a run can
/// hold a candidate at every scheme in it, and each one can read to the end of the run. The scan
/// itself is linear in what it reads; see [`link_chars_run`].
#[tracing::instrument(
	name = "link_chars_parser",
	level = "trace",
	skip_all,
	fields(ok, output)
)]
fn link_chars<'data>(input: &mut Input<'data>, context: &Context) -> PResult<&'data str> {
	context.remaining_fuel().spend()?;
	input
		.recognize(|input| link_chars_run(input, context, usize::MAX))
		.trace()
}

/// Parse a URL and verify that it has valid schemes. This is _not_ the same as
/// [`detection::starts_at`] which is more restrictive and includes non-schemes.
///
/// # Errors
/// If the content does not begin with a valid URL.
pub fn verify_url(input: &mut Input, context: &Context) -> PResult<Url> {
	let text = link_chars(input, context)?;
	parse_and_validate_url(text, context.dev_links).ok_or(Fail::NoMatch)
}

/// Parse a URL that is shown as it is written, as a detected link's or an auto link's is, with the
/// text to show for it if the URL alone would not read back as written.
///
/// That is a URL written without a scheme: the reader wrote `discord.gg/abc`, not
/// `https://discord.gg/abc`. Its text is a [`TokenKind::Text`] token in place of the
/// [`TokenKind::Url`] one, as a contact link's is.
///
/// # Errors
/// If the content does not begin with a valid URL.
pub fn shown_url<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<(Url, Option<Elements<'data, S>>, S::Syntax)> {
	let start = input.start;
	let text = link_chars(input, context)?;
	let url = parse_and_validate_url(text, context.dev_links).ok_or(Fail::NoMatch)?;
	if schemaless_domain(text).is_none() {
		return Ok((url, None, token::<S>(TokenKind::Url, start, input.start)));
	}

	// the text records its token; the sequence holding it spans the same, bare
	let mut span: S = input.span(start);
	span.attach(token::<S>(TokenKind::Text, start, input.start));
	let text = Spanned {
		value: vec![Spanned {
			value: Element::Text(text.into()),
			span,
		}],
		span: input.span(start),
	};
	Ok((url, Some(text), S::Syntax::default()))
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
/// The resulting scheme is one of [`scheme::ALL`] that `dev_links` permits. If it is [`scheme::DEV`],
/// the [`Url::domain`] is one of [`scheme::VALID_DEV_DOMAINS`].
///
/// # Panics
/// If a new [`SyntaxViolation`] has been added upstream without updating the internal logic.
#[must_use]
pub fn parse_and_validate_url(text: &str, dev_links: bool) -> Option<Url> {
	// if the text contains any suspicious whitespace, this URL is suspicious
	if text.is_empty() || text.chars().any(is_suspicious_whitespace) {
		return None;
	}

	let schemaless = schemaless_domain(text);
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
			if let Some(schemaless_domain) = schemaless
				&& !(schemaless_domain.is_authority_of(url) && schemaless_domain.path.accepts(url))
			{
				return false;
			}

			scheme::ALL
				.iter()
				.any(|scheme| scheme.allowed_by(dev_links) && scheme.validate(url))
		})
}

/// Whether any URL whose authority ends where `text` does could pass [`parse_and_validate_url`].
///
/// `text` is a link's text cut off at the character that ends its authority: the first `/`, `?`
/// or `#` after the scheme's slashes, or a `\` too for a scheme the URL standard calls special. The
/// URL parser reads the scheme, credentials, host and port off that prefix alone, and nothing after
/// it can make the parse fail, so a prefix that does not parse, or whose authority validation
/// turns down, rules out every URL it begins. That is what lets link detection reject a candidate
/// without reading to the end of its run. What depends on the rest -- syntax violations, the path
/// a schemaless domain accepts -- is left to [`parse_and_validate_url`], so `true` decides nothing.
///
/// Every scheme a candidate can carry is validated by its scheme and authority alone; a
/// [`scheme::Contact`] reads the path, but never begins a candidate.
#[must_use]
fn authority_could_validate(text: &str, dev_links: bool) -> bool {
	if text.chars().any(is_suspicious_whitespace) {
		return false;
	}

	// The character after `text` ends the authority, and no domain contains one, so a domain that
	// begins the whole URL begins `text`.
	let schemaless = schemaless_domain(text);
	let text = match schemaless {
		Some(_) => Cow::Owned(format!("https://{text}")),
		None => Cow::Borrowed(text),
	};

	let Ok(url) = Url::parse(&text) else {
		return false;
	};
	// the host this reads runs to the first `/`, so the whole URL's runs at least as far
	if has_percent_encoded_domain(url.scheme(), &text) {
		return false;
	}
	if let Some(schemaless_domain) = schemaless
		&& !schemaless_domain.is_authority_of(&url)
	{
		return false;
	}

	scheme::ALL
		.iter()
		.any(|scheme| scheme.allowed_by(dev_links) && scheme.validate(&url))
}

/// Whether `scheme` is one the URL standard calls special, which ends an authority at `\` as well
/// as `/` and takes any run of either after its `:`.
#[must_use]
fn is_special_scheme(scheme: &str) -> bool {
	matches!(scheme, "ftp" | "file" | "http" | "https" | "ws" | "wss")
}

/// Manually parse the host section of the URL from `url_str` and return whether it has any
/// percent-encoded characters in it. This is a best-effort attempt and is not URL-compliant.
fn has_percent_encoded_domain(scheme: &str, url_str: &str) -> bool {
	// nearly every URL begins with its scheme, where the search below would find it first anyway
	if let Some(after_scheme) = url_str
		.strip_prefix(scheme)
		.and_then(|rest| rest.strip_prefix("://"))
	{
		let host_end = after_scheme.find('/').unwrap_or(after_scheme.len());
		return contains_percent_encoding(&after_scheme[..host_end]);
	}

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
	// the only suspicious ASCII is the controls, which skips the lookup for nearly every character
	if ch.is_ascii() {
		return ch.is_ascii_control();
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
pub fn link<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<ParsedLink<'data, S>> {
	match input.attempt(|input| masked::masked(input, context))? {
		Some(masked::Masked::Link(link)) => return Ok(link),
		// none of a spoof is a link, and every other alternative would find one in it
		Some(masked::Masked::Spoof(..)) => return Err(Fail::NoMatch),
		None => {}
	}
	if let Some(link) = input.attempt(|input| detection::detection(input, context))? {
		return Ok(link);
	}
	if let Some(link) = input.attempt(|input| auto::link(input, context))? {
		return Ok(link);
	}
	contact::contact(input, context)
}

#[cfg(test)]
mod test {
	use url::Url;

	use super::parse_and_validate_url;

	/// Validate `s` with every rule allowed.
	fn validate(s: &str) -> Option<Url> {
		parse_and_validate_url(s, true)
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

	/// A special scheme's path can't hold a backslash, but a `dev` one keeps it as written.
	#[test]
	fn backslash_in_path() {
		assert_eq!(validate("https://wnelson.dev/foo\\bar"), None);

		let s = "dev://branch/foo\\bar";
		assert_eq!(validate(s), Some(Url::parse(s).unwrap()));
	}

	/// A `dev` URL for each surface the client routes.
	const DEV_URLS: [&str; 4] = [
		"dev://branch/main",
		"dev://experiment/foo",
		"dev://playground/mana",
		"dev://devtools/shop_collectibles",
	];

	/// Without [`crate::Options::dev_links`] a `dev` URL is not a URL at all.
	#[test]
	fn dev_scheme_needs_dev_links() {
		let without_dev = false;

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
			// the bare host names the site rather than linking to anything in it
			"discord.com",
			"discord.com/",
			"www.discordapp.com",
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

	/// A plain link byte is skipped without asking whether it ends the scope, so it must not be
	/// able to.
	#[test]
	fn plain_link_bytes_end_no_scope() {
		use crate::{scope::ScopeSet, util::ByteSet};

		let mut boundaries = ByteSet::default();
		for scope in ScopeSet::all() {
			scope.insert_boundary_bytes(&mut boundaries);
		}
		for byte in boundaries.iter() {
			assert!(!super::is_plain_link_byte(byte), "{:?}", char::from(byte));
		}
	}

	#[test]
	fn app_paths_are_sorted() {
		assert!(super::APP_PATHS.is_sorted());
	}
}
