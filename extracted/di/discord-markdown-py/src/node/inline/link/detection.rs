//! Link detection parsing
//!
//! This module attempts to parse link content from otherwise unmarked content.

use url::Url;

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	node::inline::link::scheme,
	span::{Span, Trace},
	util::ByteSet,
};

use super::{
	Link, ParsedLink, SCHEMALESS_DOMAINS, authority_could_validate, is_special_scheme,
	link_chars_run, shown_url, verify_url,
};

/// Whether `input` begins with a valid starting sequence for URL detection.
///
/// This is intentially more restrictive than schemes allowed in [`super::parse_and_validate_url`]
/// because we allow a greater range of schemes as URLs than the schemes that we want to
/// automatically detect. For example, `<discord://foo>` is a valid URL but it will not be
/// automatically detected.
///
/// Every candidate this accepts costs a scan of the link characters after it, so it only accepts
/// what could still validate. A detected scheme needs a host, and validation rejects one written
/// without its `//`, so a scheme only counts as `scheme://`: otherwise `dev:dev:dev:` would scan the
/// whole run at every `dev:`. A schemaless host has to be the whole host for the same reason; see
/// [`super::SchemalessDomain::begins_host`].
#[must_use]
pub fn starts_at(input: &Input) -> bool {
	starts_with_detected_scheme(input)
		// A schemaless host is the only start sequence that carries no delimiter of its own, so
		// it is the only one that can begin in the middle of a word. Requiring a token boundary
		// is what keeps `getscammeddiscord.gg/x` from lending a scam domain a real invite, and
		// what keeps `ftp://discord.gg/x` from having its scheme quietly dropped.
		|| (at_token_start(input)
			&& SCHEMALESS_DOMAINS
				.iter()
				.any(|domain| domain.begins_host(input)))
}

/// The length of the longest name in [`scheme::DETECTED`], every one of which is lowercase ASCII.
const MAX_DETECTED_SCHEME_LEN: usize = 5;

/// Whether `text` begins with one of [`scheme::DETECTED`] and its `://`.
///
/// This runs at every byte that could begin a scheme, so it reads the scheme off the text, which
/// costs at most a few byte comparisons, before comparing it with any name.
fn starts_with_detected_scheme(text: &str) -> bool {
	detected_scheme(text).is_some()
}

/// The name of the scheme in [`scheme::DETECTED`] that `text` begins with, with its `://`.
fn detected_scheme(text: &str) -> Option<&str> {
	let len = text
		.bytes()
		.take(MAX_DETECTED_SCHEME_LEN + 1)
		.take_while(u8::is_ascii_lowercase)
		.count();
	let name = &text[..len];
	(text[len..].starts_with("://") && scheme::DETECTED.iter().any(|scheme| scheme.name() == name))
		.then_some(name)
}

/// Where the authority of the URL that `text` begins with ends, if a character ends it, and whether
/// its scheme is special, as the URL parser reads it: after the scheme's `://`, the credentials,
/// host and port run to the first `/`, `?` or `#`, and a special scheme's to a `\` too. A
/// schemaless host is given `https://`, so it is all authority from its first byte.
///
/// `text` has to begin a link by [`starts_at`], and a special scheme's `://` must not be followed
/// by another `/` or `\`, which the URL parser would take as part of the same separator.
fn authority_end(text: &str) -> Option<(usize, bool)> {
	let (start, special) = match detected_scheme(text) {
		Some(name) => (name.len() + "://".len(), is_special_scheme(name)),
		None => (0, true),
	};

	text[start..]
		.bytes()
		.position(|byte| matches!(byte, b'/' | b'?' | b'#') || (special && byte == b'\\'))
		.map(|offset| (start + offset, special))
}

/// Whether the URL that `input` begins with is ruled out by the part of it up to a character that
/// is decisive, without reading on to the end of its run.
///
/// A run can hold a candidate at every scheme in it, as in `https://^https://^…`, and each one
/// would read on to the end of the run and then hand all of it to the URL parser. A few characters
/// decide most of them, so long as the run carries on past them, which only takes scanning that
/// far:
///
/// - for a special scheme, a `/` or `\` straight after its `://`: the URL parser takes every one
///   of them as a single separator, and anything but exactly `//` is a syntax violation;
/// - the one that ends the authority: everything [`authority_could_validate`] reads is before
///   it, and a special scheme's path that starts with `\` is a syntax violation;
/// - for a special scheme, the first `\` in the path, which is a syntax violation too, unless a
///   `?` or `#` comes before it.
fn ruled_out(input: &Input, context: &Context) -> PResult<bool> {
	let bytes = input.as_bytes();
	if let Some(name) = detected_scheme(input)
		&& is_special_scheme(name)
	{
		let after_separator = name.len() + "://".len();
		if matches!(bytes.get(after_separator), Some(b'/' | b'\\')) {
			return runs_past(input, context, after_separator);
		}
	}

	let Some((end, special)) = authority_end(input) else {
		return Ok(false);
	};
	if runs_past(input, context, end)?
		&& ((special && bytes[end] == b'\\')
			|| !authority_could_validate(&input[..end], context.dev_links))
	{
		return Ok(true);
	}

	let path = &bytes[end..];
	match memchr::memchr3(b'\\', b'?', b'#', path) {
		Some(offset) if special && path[offset] == b'\\' => runs_past(input, context, end + offset),
		_ => Ok(false),
	}
}

/// Whether the run of link characters that `input` begins carries on past `input[last]`, so that
/// the URL it holds has everything up to there in it.
fn runs_past(input: &Input, context: &Context, last: usize) -> PResult<bool> {
	let mut run = *input;
	let reach = input.start + last + 1;
	match link_chars_run(&mut run, context, reach) {
		Ok(()) => Ok(run.start >= reach),
		Err(Fail::NoMatch) => Ok(false),
		Err(fail) => Err(fail),
	}
}

/// Add every byte that can begin a link by [`starts_at`] to `bytes`.
pub fn insert_first_bytes(bytes: &mut ByteSet) {
	for scheme in scheme::DETECTED {
		bytes.extend(scheme.name().bytes().next());
	}
	for domain in SCHEMALESS_DOMAINS {
		bytes.extend(domain.first_bytes());
	}
}

/// Whether the preceding character cannot continue a token.
///
/// That means the start of the parse or a whitespace character. A zero-width space is deliberately
/// not whitespace: `getscammed<ZWSP>discord.gg/x` reads as one token, and U+200B is not
/// `White_Space`.
#[must_use]
pub fn at_token_start(input: &Input) -> bool {
	#[allow(
		deprecated,
		reason = "preceding_char is implemented specifically for coded links"
	)]
	input.preceding_char().is_none_or(char::is_whitespace)
}

/// Turn away a position that cannot begin a URL, or whose candidate is ruled out early.
///
/// The [`starts_at`] gate is not an optimization: a URL is read with [`super::link_chars`], which
/// is O(n) in the run after it, so that must not run at a position that cannot begin a link at
/// all. Past the gate, a candidate whose authority rules it out is turned away before that scan,
/// for the same fuel as one that is scanned.
fn admit(input: &Input, context: &Context) -> PResult<()> {
	if !starts_at(input) {
		return Err(Fail::NoMatch);
	}
	if ruled_out(input, context)? {
		context.remaining_fuel().spend()?;
		return Err(Fail::NoMatch);
	}
	Ok(())
}

/// Parse a URL at a position that could begin one.
///
/// # Errors
/// If the content does not begin with a URL.
pub fn url(input: &mut Input, context: &Context) -> PResult<Url> {
	admit(input, context)?;
	verify_url(input, context)
}

/// Parse content that starts with content that can be parsed into a URL.
///
/// For example, this will pull the URL out of `https://discord.com hello world`, leaving the
/// remaining content as ` hello world`.
///
/// # Errors
/// If the content is not a valid link for link detection.
#[tracing::instrument(
	name = "detection_parser",
	level = "trace",
	skip_all,
	fields(ok, output)
)]
pub fn detection<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<ParsedLink<'data, S>> {
	admit(input, context)?;
	let (url, text, syntax) = shown_url(input, context)?;
	let link = Link {
		text,
		url,
		title: None,
	};
	Ok((link, syntax)).trace()
}

#[cfg(test)]
mod test {
	use url::Url;

	use super::detection;
	use crate::Input;
	use crate::context::Context;
	use crate::error::PResult;
	use crate::node::Element;
	use crate::node::inline::link::{Link, ParsedLink};
	use crate::spanned_vec;
	use crate::test_utils::run;

	/// Parse `s` as a detected link, expecting it to succeed.
	fn parse(s: &str) -> (Input<'_>, Link<(), Element<'_, ()>>) {
		let (rem, (link, ())) = try_parse(s).expect("unable to parse");
		(rem, link)
	}

	fn try_parse(s: &str) -> PResult<(Input<'_>, ParsedLink<'_, ()>)> {
		run(s, |input| detection::<()>(input, &Context::default()))
	}

	/// Build the expectation for a text-less link.
	fn url(s: &str) -> Link<(), Element<'_, ()>> {
		Link {
			text: None,
			url: Url::parse(s).unwrap(),
			title: None,
		}
	}

	/// Build the expectation for a link written as `s`, without a scheme, which is its text.
	fn schemaless(s: &str) -> Link<(), Element<'_, ()>> {
		Link {
			text: Some(spanned_vec![Element::Text(s.into())]),
			url: Url::parse(&format!("https://{s}")).unwrap(),
			title: None,
		}
	}

	/// Every schemaless host starts a link, with or without its subdomains, and a longer host
	/// that merely begins with one does not.
	#[test]
	fn starts_at_every_schemaless_host() {
		use super::starts_at;
		use crate::node::inline::link::SCHEMALESS_DOMAINS;

		for domain in SCHEMALESS_DOMAINS {
			let hosts = std::iter::once(domain.domain.to_owned()).chain(
				domain
					.subdomains
					.iter()
					.map(|subdomain| format!("{subdomain}{}", domain.domain)),
			);
			for host in hosts {
				for s in [host.clone(), format!("{host}/x"), format!("{host}.")] {
					assert!(starts_at(&Input::from(s.as_str())), "{s}");
				}
				for s in [format!("{host}x"), format!("{host}-x"), format!("{host}1")] {
					assert!(!starts_at(&Input::from(s.as_str())), "{s}");
				}
			}
		}
	}

	/// [`super::starts_with_detected_scheme`] reads at most this many lowercase letters.
	#[test]
	fn detected_schemes_fit_the_scan() {
		use crate::node::inline::link::scheme::DETECTED;

		for scheme in DETECTED {
			let name = scheme.name();
			assert!(name.len() <= super::MAX_DETECTED_SCHEME_LEN, "{name}");
			assert!(name.bytes().all(|byte| byte.is_ascii_lowercase()), "{name}");
		}
	}

	/// A candidate turned away by its authority, or by the first `\` in its path, is one that the
	/// whole URL would have turned away too, and the ones that cannot be decided that early are
	/// left to it.
	#[test]
	fn early_rejection_agrees_with_the_whole_url() {
		use crate::context::Options;
		use crate::node::inline::link::verify_url;

		let ruled_out = [
			"https://^https://^",
			"https://a:99999/x",
			"https://%41.com/x",
			"https://a\\b",
			"https://a:1\\b",
			// one separator, but not exactly `//`
			"https:///a.com/x",
			"https://\\a.com/x",
			"http://\\\\a.com/x",
			"https://a/b\\c",
			"https://a.b/x/\\",
			// a group the scan has to look past
			"https://a.b/(x\\",
			"discord.gg:1/abc",
			"discord.gg@a/abc",
			"discord.gg.x/abc",
			"discord.gg\\abc",
			"dev://nonsense/x",
			"dev://a\\b/x",
			"dev:///x",
		];
		let undecided = [
			"https://a.com/x",
			"https://a@b.com/x",
			"https://@a/x",
			"https://a:1/x",
			"https://[::1]/x",
			"https://a?b\\c",
			"https://a#b\\c",
			"https://a",
			"discord.gg/abc",
			"discord.gg/a/b/../",
			"discord.gg?x/",
		];
		// a `dev` path keeps its backslashes, unlike a special scheme's
		let needs_dev_links = [
			"dev://branch/x",
			"dev://branch/a\\b",
			"dev://branch/\\",
			"dev://branch/\\/..",
		];

		for dev_links in [false, true] {
			let context = Context::new(Options {
				dev_links,
				..Default::default()
			});
			let cases = ruled_out
				.iter()
				.map(|&s| (s, true))
				.chain(undecided.iter().map(|&s| (s, false)))
				.chain(needs_dev_links.iter().map(|&s| (s, !dev_links)));
			for (s, expected) in cases {
				assert_eq!(
					super::ruled_out(&Input::from(s), &context),
					Ok(expected),
					"{s} with dev_links {dev_links}"
				);
				for s in [s.to_owned(), format!("{s}x y"), format!("{s}.")] {
					let input = Input::from(s.as_str());
					assert!(super::starts_at(&input), "{s}");
					let early = input.matches(|input| super::url(input, &context));
					let whole = input.matches(|input| verify_url(input, &context));
					assert_eq!(early, whole, "{s} with dev_links {dev_links}");
				}
			}
		}
	}

	/// A detected scheme only starts a link with its `//`, which validation demands anyway.
	#[test]
	fn scheme_needs_its_double_slash() {
		use super::starts_at;

		for s in ["xhttps://x", "httpsx://x", "devv://x"] {
			assert!(!starts_at(&Input::from(s)), "{s}");
		}
		for s in ["https://x", "http://x", "dev://x"] {
			assert!(starts_at(&Input::from(s)), "{s}");
		}
		for s in ["https:x", "https:/x", "http", "dev:dev:", "https:\\\\x"] {
			assert!(!starts_at(&Input::from(s)), "{s}");
			try_parse(s).expect_err("able to parse");
		}
	}

	#[test]
	fn schemaless_invite() {
		let s = "discord.gg/discord-developers";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, schemaless(s));
	}

	/// The terminal character rules apply to a schemaless link exactly as they do to a URL.
	#[test]
	fn schemaless_link_leaves_trailing_terminal() {
		let s = "discord.gg/abc.";
		let (rem, res) = parse(s);
		assert_eq!(rem, ".");
		assert_eq!(res, schemaless("discord.gg/abc"));
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
			assert_eq!(res, schemaless(s), "{s}");
		}
	}

	/// A path the client does not route is not a schemaless link, so there is nothing to detect.
	#[test]
	fn schemaless_link_needs_a_path_the_client_routes() {
		for s in [
			"discord.com/developers/docs",
			"discord.com/shopping-cart",
			// a bare host is not a path at all
			"discord.com",
			// `discord.com` is a prefix of this host, but it is not this host
			"discord.company.com/invite/abc",
		] {
			try_parse(s).expect_err("able to parse");
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
		try_parse(s).expect_err("unable to parse");
	}

	#[test]
	fn complex_url() {
		let s = "https://en.wikipedia.org/wiki/Endemic_(epidemiology)";
		let (rem, res) = parse(s);
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
		let (rem, res) = parse(s);
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

	/// None of a run of trailing punctuation belongs to the link, however long the run is.
	#[test]
	fn url_leaves_all_trailing_punctuation() {
		for (s, expected, expected_rem) in [
			("https://wnelson.dev..", "https://wnelson.dev", ".."),
			("https://google.com/foo.,", "https://google.com/foo", ".,"),
			("https://google.com/foo...", "https://google.com/foo", "..."),
			(
				"https://google.com/foo'.\"",
				"https://google.com/foo",
				"'.\"",
			),
			("https://discord.com.).", "https://discord.com", ".)."),
			(
				"https://google.com/search?q=cat(s)..",
				"https://google.com/search?q=cat(s)",
				"..",
			),
		] {
			let (rem, res) = parse(s);
			assert_eq!(rem, expected_rem, "{s}");
			assert_eq!(res, url(expected), "{s}");
		}

		let (rem, res) = parse("discord.gg/abc..");
		assert_eq!(rem, "..");
		assert_eq!(res, schemaless("discord.gg/abc"));
	}

	/// A URL written with a scheme reads back as written without any text of its own.
	#[test]
	fn schemed_link_has_no_text() {
		let s = "https://discord.gg/abc";
		let (rem, res) = parse(s);
		assert_eq!(rem, "");
		assert_eq!(res, url(s));
	}

	/// A run of punctuation the link carries on past is part of the link.
	#[test]
	fn url_keeps_interior_punctuation() {
		for s in [
			"https://google.com/foo..bar",
			"https://google.com/a.,b",
			"https://discord.com.)x",
			"https://en.wikipedia.org/wiki/Foo_(bar.)",
		] {
			let (rem, res) = parse(s);
			assert_eq!(rem, "", "{s}");
			assert_eq!(res, url(s), "{s}");
		}
	}

	// (stuff https://google.com) <-- not include
	// https://google.com/cat(s) <-- should include
	// https://google.com/bob)a <-- should include

	#[test]
	fn url_avoids_including_unmatched_terminal_parenthesis() {
		let s = "https://google.com)";
		let (rem, res) = parse(s);
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
		let (rem, res) = parse(s);
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
		assert_eq!(
			res,
			url("https://en.wikipedia.org/wiki/Endemic_(epidemiology)")
		);
	}

	#[test]
	// see the note on the timeout tests in `crate::test` for why debug gets a larger budget
	#[cfg_attr(debug_assertions, ntest::timeout(3000))]
	#[cfg_attr(not(debug_assertions), ntest::timeout(1000))]
	fn deeply_nested_parens_in_query_string() {
		// URLs with many nested paren groups (e.g. Datadog qson params) must parse in O(n) time.
		let s = "https://example.com/?a=qson:(data:(x:1,y:2),v:0)&b=qson:(data:(p:(selected:count),q:(selected:count),r:(selected:p95),topN:5),v:0)&c=qson:(data:(visible:true,hits:(selected:total),errors:(selected:total),latency:(selected:p95)),v:1)";
		let (rem, res) = parse(s);
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
