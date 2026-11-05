//! Masked link parsing
//!
//! Masked links are links that have text and optionally a title. For example:
//!
//! ```md
//! [Discord](https://discord.com "this is a link to Discord")
//! ```

use std::{borrow::Cow, sync::LazyLock};

use discord_confusables::{Direction, display_order, internal_skeleton};
use enumset::{enum_set, enum_set_difference};
use tracing::Level;

use crate::{
	Input,
	context::{Context, fuel::OutOfFuel},
	error::{Fail, PResult},
	input::token,
	lossless::TokenKind,
	span::{Span, Syntax as _, Trace},
	syntax::{Syntax, SyntaxSet},
	util::ByteSet,
};

use super::{Link, ParsedLink, Scope, auto, detection, is_suspicious_whitespace, verify_url};

mod link;
mod text;

/// Whether text a masked link shows the reader is free of anything that reads as a link.
///
/// `[https://evil.com](https://good.com)` shows the reader one link and sends them to another, so a
/// text segment that contains a link is not a masked link at all. The title is shown on hover and
/// spoofs a destination the same way, so it is held to the same rule. This covers links written
/// without a scheme as well: `discord.gg/evil` resolves for the reader exactly like a URL does, so
/// hiding one behind a masked link is the same attack.
///
/// # Errors
/// If the parse runs out of fuel. Each candidate the search reads costs a unit, and an empty tank
/// must not read as text with no link in it.
#[tracing::instrument(level = Level::TRACE)]
fn has_no_link(text: &str, context: &Context) -> Result<bool, OutOfFuel> {
	let context = context.fresh();
	let process_text = |text: &str| -> Result<bool, OutOfFuel> {
		// Search for a URL as it would be seen, not as it is encoded: reorder bidirectional text
		// into display order, drop invisible whitespace that could split a link without changing
		// how it looks, then map every confusable to its prototype. Controls steer the reordering,
		// so they are only stripped after it.
		let text = display_order(Direction::Ltr, text);
		let text: Cow<str> = if text.chars().any(is_suspicious_whitespace) {
			text.chars()
				.filter(|ch| !is_suspicious_whitespace(*ch))
				.collect::<String>()
				.into()
		} else {
			text
		};
		let text = internal_skeleton(&text);

		for start in candidates(&text) {
			// `detection::url` leads with its start-sequence gate, so a candidate that cannot
			// begin a link costs a tag comparison rather than a scan of everything after it.
			// The slice starts the input, so every candidate reads as a token start. That is on
			// purpose here: this text *is* what the reader is shown as the link, so a schemaless
			// host anywhere in it is already the deception.
			if Input::from(&text[start..]).matches(|input| detection::url(input, &context))? {
				return Ok(false);
			}
		}

		Ok(true)
	};

	Ok(process_text(&text.chars().rev().collect::<String>())? && process_text(text)?)
}

/// Byte offsets where a link could begin.
///
/// Every offset found here goes on to run a parser, so this only has to be cheap and never miss:
/// it is every offset whose byte can begin a start sequence, which [`detection::url`] then gates.
/// Every such byte is ASCII, so each offset is a character boundary.
fn candidates(text: &str) -> impl Iterator<Item = usize> + '_ {
	static FIRST_BYTES: LazyLock<ByteSet> = LazyLock::new(|| {
		let mut bytes = ByteSet::default();
		detection::insert_first_bytes(&mut bytes);
		bytes
	});

	text.bytes()
		.enumerate()
		.filter(|&(_, byte)| FIRST_BYTES.contains(byte))
		.map(|(start, _)| start)
}

/// The character that marks the beginning of the text portion.
pub const TEXT_OPENER: u8 = b'[';
/// The character that marks the end of the text portion.
pub const TEXT_TERMINAL: u8 = b']';
/// The character that marks the end of the link & title portion.
pub const LINK_TERMINAL: u8 = b')';
/// The character that marks the beginning of the link & title portion.
pub const LINK_OPENER: u8 = b'(';
/// The sequence that separates the text portion from the link & title portion.
pub const TEXT_LINK_DIVIDER: &[u8] = b"](";

/// Syntax that is not allowed to parse inside the text portion.
// this is intentionally setup to exclude most syntax by default
pub const DISABLED_MASKED_LINK_SYNTAXES: SyntaxSet = {
	let allowed = enum_set!(
		Syntax::Bold
			| Syntax::AsteriskItalic
			| Syntax::UnderscoreItalic
			| Syntax::Strikethrough
			| Syntax::Underline
			| Syntax::Code
			| Syntax::DoubleCode
	);
	let all = SyntaxSet::all();
	enum_set_difference!(all, allowed)
};

/// What a complete `[text](url "title")` reads as.
#[derive(Debug)]
pub enum Masked<'data, S: Span> {
	Link(ParsedLink<'data, S>),
	/// A masked link whose text is blank or whose text or title reads as a link, with the
	/// [`TokenKind::Text`] token covering it.
	///
	/// This is all of the source text, not a failure: had it failed, the parse would carry on just
	/// past the `[`, and the link in the text would run on through `](` into the destination.
	/// `[https://example.com/](https://example.com/)` would become one link to
	/// `https://example.com/](https://example.com/)`. Blank text would leave `[ ](` before a link
	/// to the destination. None of it is a link.
	Spoof(&'data str, S::Syntax),
}

/// Parse a masked link.
///
/// # Errors
/// If the content does not begin with a masked link.
#[tracing::instrument(name = "masked_parser", level = Level::TRACE, skip_all, fields(ok, output))]
pub fn masked<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<Masked<'data, S>> {
	if input.as_bytes().first() != Some(&TEXT_OPENER) {
		return Err(Fail::NoMatch);
	}

	let start = *input;
	let (text, text_syntax) = text::segment::<S>(input, context)?;
	let (url, title, link_syntax) = link::segment::<S>(input, context)?;
	// Guarded only once the whole link has been read, so a spoof is known to span all of it.
	let spoof = !text::segment_is_not_whitespace(&text)
		|| !text::segment_has_no_link(&text, context)?
		|| match &title {
			Some(title) => !has_no_link(title, context)?,
			None => false,
		};
	let masked = if spoof {
		Masked::Spoof(
			&start.content[..input.start - start.start],
			token::<S>(TokenKind::Text, start.start, input.start),
		)
	} else {
		let link = Link {
			text: Some(text),
			url,
			title,
		};
		Masked::Link((link, text_syntax.join(link_syntax)))
	};
	Ok(masked).trace()
}
#[cfg(test)]
mod test {
	use url::Url;

	use super::{Masked, has_no_link, masked};
	use crate::Input;
	use crate::context::{Context, Options, fuel::OutOfFuel};
	use crate::error::{Fail, PResult};
	use crate::node::inline::link::{Link, ParsedLink};
	use crate::node::{Element, Inline};
	use crate::test_utils::{inline_content, resolved_inlines, run};

	fn parsed(s: &str) -> PResult<(Input<'_>, Masked<'_, ()>)> {
		run(s, |input| masked::<()>(input, &Context::default()))
	}

	/// `s` as a masked link, which it must not be a spoof of.
	fn masked_link(s: &str) -> PResult<(Input<'_>, ParsedLink<'_, ()>)> {
		parsed(s).map(|(rem, masked)| match masked {
			Masked::Link(link) => (rem, link),
			Masked::Spoof(..) => panic!("{s:?} is a spoof"),
		})
	}

	/// `s`, all of it, is a spoof.
	fn assert_spoof(s: &str) {
		let (rem, masked) = parsed(s).expect("unable to parse");
		assert_eq!(rem, "", "{s}");
		assert!(
			matches!(masked, Masked::Spoof(source, ()) if source == s),
			"{s:?} is {masked:?}"
		);
	}

	/// Resolve the delimiters in a link's text, as a whole parse would.
	fn resolved_link(link: Link<(), Element<'_, ()>>) -> Link<(), Inline<'_, ()>> {
		Link {
			text: link.text.map(resolved_inlines),
			url: link.url,
			title: link.title,
		}
	}
	use crate::{bold, italic, link, spanned_vec, text};

	/// Every candidate the guard reads costs fuel, and an empty tank is not text without a link in
	/// it.
	#[test]
	fn guard_does_not_read_exhaustion_as_no_link() {
		let empty = Context::new(Options {
			fuel: 0,
			..Default::default()
		});
		assert_eq!(has_no_link("https://evil.com", &empty), Err(OutOfFuel));
		assert_eq!(
			has_no_link("https://evil.com", &Context::default()),
			Ok(false)
		);
	}

	/// Whatever the budget, a spoof is never a link: a tank that runs dry partway through the guard
	/// fails the parse rather than letting the link through.
	#[test]
	fn a_spoof_is_never_a_link_for_lack_of_fuel() {
		for s in [
			"[https://evil.com](https://good.com)",
			"[a](https://good.com \"https://evil.com\")",
		] {
			let mut spoofed = false;
			for fuel in 0..100 {
				let context = Context::new(Options {
					fuel,
					..Default::default()
				});
				match run(s, |input| masked::<()>(input, &context)) {
					Err(Fail::OutOfFuel) => {}
					Ok((rem, Masked::Spoof(..))) if rem.is_empty() => {
						spoofed = true;
						break;
					}
					other => panic!("{s:?} with {fuel} fuel parsed as {other:?}"),
				}
			}
			assert!(spoofed, "{s:?} never parsed as a spoof");
		}
	}

	/// A schemaless link in the text segment is rejected the same way a URL is.
	#[test]
	fn schemaless_link_in_text_is_rejected() {
		for s in [
			r"[discord.gg/evil](https://good.com)",
			// the guard also reads the text backwards, to catch right-to-left overrides
			r"[live/gg.drocsid](https://good.com)",
		] {
			assert_spoof(s);
		}
	}

	/// Directional controls are read before invisible whitespace is stripped, so a link that only
	/// forms once part of the text is overridden is still found, even if split by invisible
	/// characters.
	#[test]
	fn link_formed_by_directional_override_is_rejected() {
		for s in [
			// displays as `discord.gg/x`: neither the logical order nor its reverse is a link
			"[discord\u{202e}g.\u{202c}g/x](https://good.com)",
			"[discord\u{202e}g\u{200b}\u{2009}.\u{202c}g/x](https://good.com)",
			"[discord\u{2009}.gg/x](https://good.com)",
		] {
			assert_spoof(s);
		}
	}

	/// The guard reads the text segment at every depth.
	///
	/// `Inline::content` used to stop at the direct children, so two levels of markup looked like a
	/// segment with no text in it and `[**_https://evil.com_**](https://good.com)` was accepted.
	#[test]
	fn nested_markup_in_text_is_still_read() {
		for s in [
			r"[**discord.gg/evil**](https://good.com)",
			r"[**_discord.gg/evil_**](https://good.com)",
			r"[**__~~discord.gg/evil~~__**](https://good.com)",
			r"[**https://evil.com**](https://good.com)",
			r"[**_https://evil.com_**](https://good.com)",
			r"[**__~~https://evil.com~~__**](https://good.com)",
		] {
			assert_spoof(s);
		}
	}

	/// A spoof is text, all of it, whether its text reads as a link or is blank. Were it only a
	/// failed parse, the parse would carry on past the `[` and find a link: the one in the text,
	/// which runs on through `](` -- `[https://example.com/](https://example.com/)` was a link to
	/// `https://example.com/](https://example.com/)` -- or, past blank text, the destination.
	#[test]
	fn spoof_is_not_a_link_at_all() {
		for s in [
			r"[https://example.com/](https://example.com/)",
			r"[https://evil.com](https://good.com)",
			r"[see https://evil.com/ here](https://good.com)",
			r"[discord.gg/evil](https://good.com)",
			r"[**https://evil.com/**](https://good.com)",
			r#"[foo](https://good.com "https://evil.com/")"#,
			// blank text hides the link altogether
			r"[ ](https://good.com)",
			r"[](https://good.com)",
			r"[**](https://good.com)",
			"[ \u{200d}\u{3164}](https://good.com)",
		] {
			assert_eq!(
				inline_content(s),
				spanned_vec![Inline::Text(s.into())],
				"{s}"
			);
		}
	}

	/// Only the spoof is text: what follows it parses as usual.
	#[test]
	fn text_after_a_spoof_still_parses() {
		let s = r"[https://evil.com](https://good.com) **https://good.com**";
		assert_eq!(
			inline_content(s),
			spanned_vec![
				text!(r"[https://evil.com](https://good.com) "),
				bold!(link!("https://good.com")),
			]
		);
	}

	/// A masked link that is not one at all leaves its text to the rest of the parse, where a link
	/// ends at the `](` instead of taking the destination with it.
	#[test]
	fn link_in_text_of_a_failed_masked_link_ends_at_the_destination() {
		for (s, url, rest) in [
			(
				"[https://example.com/](foobar)",
				"https://example.com/",
				"](foobar)",
			),
			(
				"[https://example.com/a.](foobar)",
				"https://example.com/a",
				".](foobar)",
			),
			(
				"[https://example.com/]](foobar)",
				"https://example.com/",
				"]](foobar)",
			),
			// a `(` the `](` leaves unclosed is still part of the link
			(
				"[https://example.com/(a](foobar)",
				"https://example.com/(a",
				"](foobar)",
			),
			// unclosed, so the second link is a link of its own
			(
				"[https://example.com/](https://",
				"https://example.com/",
				"](https://",
			),
		] {
			assert_eq!(
				inline_content(s),
				spanned_vec![
					text!("["),
					Inline::Link(Link {
						text: None,
						url: Url::parse(url).unwrap(),
						title: None,
					}),
					Inline::Text(rest.into()),
				],
				"{s}"
			);
		}
	}

	/// Only a link written without delimiters ends at `](`: delimiters say where the URL ends.
	#[test]
	fn delimited_link_runs_through_the_destination_opener() {
		assert_eq!(
			inline_content("<https://example.com/](x)>"),
			spanned_vec![link!("https://example.com/](x)")]
		);
		let s = "[text](https://example.com/](x))";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res.url.as_str(), "https://example.com/](x)");
	}

	/// Reading every depth must not reject ordinary markup.
	/// The `)` closing a masked link's URL is not trailing text, so punctuation before it stays in
	/// the URL instead of leaving the link unclosed.
	#[test]
	fn punctuation_before_closing_paren_stays_in_url() {
		for s in [
			r"[text](https://good.com.)",
			r"[text](https://good.com/a..)",
		] {
			let (rem, (res, ())) = masked_link(s).expect("unable to parse");
			assert_eq!(rem, "", "{s}");
			let inner = &s[s.find('(').unwrap() + 1..s.len() - 1];
			assert_eq!(res.url.as_str(), Url::parse(inner).unwrap().as_str(), "{s}");
		}
	}

	#[test]
	fn nested_markup_without_a_link_is_allowed() {
		for s in [
			r"[**click here**](https://good.com)",
			r"[**_click here_**](https://good.com)",
			r"[**my discord server**](https://good.com)",
		] {
			masked_link(s).expect("unable to parse");
		}
	}

	/// The reader is shown the title on hover, so it gets the same guard as the text segment.
	#[test]
	fn link_in_title_is_rejected() {
		for s in [
			r#"[foo](https://good.com "https://evil.com")"#,
			r#"[foo](https://good.com "discord.gg/evil")"#,
			// the guard also reads the title backwards, to catch right-to-left overrides
			r#"[foo](https://good.com "moc.live//:sptth")"#,
			r#"[foo](https://good.com "live/gg.drocsid")"#,
			"[foo](https://good.com \"\u{202E}moc.drocsid//:sptth\")",
			// confusables are mapped to their prototype before the search
			r#"[foo](https://good.com "ℎttps://evil.com")"#,
			"[foo](https://good.com \"https\u{A789}//evil.com\")",
			// suspicious whitespace between the characters does not hide it either
			"[foo](https://good.com \"https://ev\u{034f}il.com\")",
		] {
			assert_spoof(s);
		}
	}

	/// The title guard must not reject titles that only read like prose.
	#[test]
	fn benign_title_is_allowed() {
		let s = r#"[foo](https://good.com "my discord server")"#;
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://good.com").unwrap(),
				text: Some(spanned_vec![text!("foo")]),
				title: Some("my discord server".to_string()),
			}
		);
	}

	/// The guard looks for links, not for the word `discord`.
	#[test]
	fn benign_text_mentioning_discord_is_allowed() {
		let s = r"[my discord server](https://good.com)";
		masked_link(s).expect("unable to parse");
	}

	/// A schemaless link is a valid target.
	#[test]
	fn schemaless_link_target() {
		let s = r"[join](discord.gg/abc)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://discord.gg/abc").unwrap(),
				text: Some(spanned_vec![text!("join")]),
				title: None,
			}
		);
	}

	/// A path the client does not route is not schemaless, so there is no target.
	#[test]
	fn schemaless_non_routed_target_is_rejected() {
		let s = r"[docs](discord.com/developers/docs)";
		masked_link(s).expect_err("able to parse");
	}

	#[test]
	fn simple_masked_link() {
		let s = r"[test](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("test")]),
				title: None,
			}
		);
	}

	#[test]
	fn inline_masked_link() {
		let s = r"[_foo_ **bar**](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![italic!("foo"), text!(" "), bold!("bar")]),
				title: None,
			}
		);
	}

	#[test]
	fn masked_link_with_new_line() {
		let s = "[foo\nbar](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo\nbar")]),
				title: None,
			}
		);
	}

	#[test]
	fn invalid_masked_url() {
		let s = r"[foo](foobar)";
		masked_link(s).expect_err("unable to parse");
	}

	// TODO - we need to conditionally allow this. Webhooks are allowed to do this.
	#[test]
	fn no_emoji() {
		let s = r"[<:abcd:1234>](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("<:abcd:1234>")]),
				title: None,
			}
		);
	}

	#[test]
	fn masked_link_with_title() {
		let s = "[foo](https://wnelson.dev  \"Will Nelson's website\")";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo")]),
				title: Some("Will Nelson's website".to_string()),
			}
		);
	}

	#[test]
	fn masked_autolink_with_title() {
		let s = "[foo](<https://wnelson.dev> \"Will Nelson's website\")";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo")]),
				title: Some("Will Nelson's website".to_string()),
			}
		);
	}

	/// A backslash escapes a double quote or a backslash in the title, and is literal before
	/// anything else.
	#[test]
	fn masked_link_with_escaped_title() {
		for (s, title) in [
			(r#"[foo](https://good.com "say \"hi\"")"#, r#"say "hi""#),
			(r#"[foo](https://good.com "\"")"#, r#"""#),
			(r#"[foo](https://good.com "back\\")"#, r"back\"),
			(r#"[foo](https://good.com "a\\\"b")"#, r#"a\"b"#),
			(r#"[foo](https://good.com "a\b")"#, r"a\b"),
		] {
			let (rem, (res, ())) = masked_link(s).expect("unable to parse");
			assert_eq!(rem, "", "unexpected remainder for {s:?}");
			assert_eq!(
				res.title.as_deref(),
				Some(title),
				"unexpected title for {s:?}"
			);
		}
	}

	/// An escaped quote does not close the title.
	#[test]
	fn masked_link_with_unclosed_escaped_title() {
		for s in [
			r#"[foo](https://good.com "abc\")"#,
			r#"[foo](https://good.com "\")"#,
			r#"[foo](https://good.com "abc\"#,
			r#"[foo](https://good.com "")"#,
		] {
			masked_link(s).expect_err("able to parse");
		}
	}

	/// Escapes cannot smuggle a link past the title guard.
	#[test]
	fn escaped_link_in_title_is_rejected() {
		assert_spoof(r#"[foo](https://good.com "\"https://evil.com\"")"#);
	}

	#[test]
	fn masked_link_with_parens() {
		let s = "[Endemic](https://en.wikipedia.org/wiki/Endemic_(epidemiology))";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)").unwrap(),
				text: Some(spanned_vec![text!("Endemic")]),
				title: None,
			}
		);
	}

	/// Markup between the characters of a URL must not hide it from [`super::has_no_link`]:
	/// `**h**ttp*s*://foo` renders as `https://foo`, so the masked link is rejected.
	#[test]
	fn masked_link_with_link() {
		let s = r"[foo **h**ttp*s*://foo](https://wnelson.dev)";
		assert_spoof(s);
	}

	/// The underscore spelling of the case above is no longer a hiding technique: an intraword `_`
	/// does not delimit an italic (see [`crate::range`]), so the
	/// text renders as the literal `http_s_://foo`, which is not a URL and does not spoof one.
	#[test]
	fn masked_link_with_intraword_underscores_is_not_a_hidden_link() {
		let s = r"[foo **h**ttp_s_://foo](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![
					text!("foo "),
					bold!("h"),
					text!("ttp_s_://foo")
				]),
				title: None,
			}
		);
	}

	#[test]
	fn sms_masked_link() {
		let s = r"[test](sms:+18005882300)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("sms:+18005882300").unwrap(),
				text: Some(spanned_vec![text!("test")]),
				title: None,
			}
		);
	}

	#[test]
	fn mailto_masked_link() {
		let s = r"[test](mailto:tim@apple.com)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("mailto:tim@apple.com").unwrap(),
				text: Some(spanned_vec![text!("test")]),
				title: None,
			}
		);
	}

	#[test]
	fn masked_link_with_matching_brackets() {
		let s = r"[[foo] bar](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("[foo] bar")]),
				title: None,
			}
		);
	}

	#[test]
	fn masked_link_with_complex_matching_brackets() {
		let s = r"[foo [bar_baz]](https://wnelson.dev)";
		let (rem, (res, ())) = masked_link(s).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_link(res),
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo [bar_baz]")]),
				title: None,
			}
		);
	}
}
