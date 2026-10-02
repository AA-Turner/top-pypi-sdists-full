//! Masked link parsing
//!
//! Masked links are links that have text and optionally a title. For example:
//!
//! ```md
//! [Discord](https://discord.com "this is a link to Discord")
//! ```

use std::{fmt::Debug, marker::PhantomData, sync::LazyLock};

use aho_corasick::{AhoCorasick, Match};
use discord_confusables::skeleton;
use enumset::{enum_set, enum_set_difference, EnumSet};
use nom::{
	combinator::{map, not},
	error::ErrorKind,
	sequence::pair,
	Check, Complete, Finish, Mode, OutputM, Parser,
};
use tracing::Level;

use crate::{
	context::Context,
	error::ParseError,
	grammar::ByteHint,
	rule::{Rule, RuleSet},
	span::Span,
	Input,
};

use super::{auto, detection, is_suspicious_whitespace, scheme, verify_url, Grammar, Link};

mod link;
mod text;

/// Whether text a masked link shows the reader is free of anything that reads as a link.
///
/// `[https://evil.com](https://good.com)` shows the reader one link and sends them to another, so a
/// text segment that contains a link is not a masked link at all. The title is shown on hover and
/// spoofs a destination the same way, so it is held to the same rule. This covers links written
/// without a scheme as well: `discord.gg/evil` resolves for the reader exactly like a URL does, so
/// hiding one behind a masked link is the same attack.
#[tracing::instrument(level = Level::TRACE)]
fn has_no_link(text: &str, context: &Context) -> bool {
	let text = text
		.chars()
		.filter(|ch| !is_suspicious_whitespace(*ch))
		.collect::<String>();

	let process_text = |text: String| -> bool {
		// The skeleton maps every confusable to its prototype and reorders
		// bidirectional text into display order, so a URL is searched for as
		// it would be seen, not as it is encoded.
		let text = skeleton(&text);

		let context = context.fresh();
		for mat in candidates(&text) {
			// `detection::url` leads with its start-sequence gate, so a candidate that cannot
			// begin a link costs a tag comparison rather than a scan of everything after it.
			// The slice starts the input, so every candidate reads as a token start. That is on
			// purpose here: this text *is* what the reader is shown as the link, so a schemaless
			// host anywhere in it is already the deception.
			let parse_result = not(detection::url::<()>(&context))
				.process::<OutputM<Check, Check, Complete>>((&text[mat.start()..]).into())
				.finish();
			if parse_result.is_err() {
				return false;
			}
		}

		true
	};

	process_text(text.chars().rev().collect()) && process_text(text)
}

/// Byte offsets where a link could begin.
///
/// Every offset found here goes on to run a parser, so this only has to be cheap and never miss:
/// it searches for the start sequences themselves, in one pass over the text.
fn candidates(text: &str) -> impl Iterator<Item = Match> + '_ {
	static START_PATTERNS: LazyLock<AhoCorasick> = LazyLock::new(|| {
		AhoCorasick::new(
			detection::HOST_START_SEQUENCES
				.into_iter()
				.chain(scheme::DETECTED.iter().map(|scheme| scheme.name())),
		)
		.expect("start sequences should be valid patterns")
	});

	START_PATTERNS.find_iter(text)
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

/// Rules that not allowed to parse inside the text portion.
// this is intentionally setup to exclude most rules by default
pub const DISABLED_MASKED_LINK_RULES: EnumSet<Rule> = {
	let allowed_rules =
		enum_set!(Rule::Bold | Rule::Code | Rule::Italic | Rule::Strikethrough | Rule::Underline);
	let all_rules = RuleSet::all();
	enum_set_difference!(all_rules, allowed_rules)
};

struct MaskedParser<'ctx, S, E> {
	context: &'ctx Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for MaskedParser<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("MaskedParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'ctx, 'data, S, E> Parser<Input<'data>> for MaskedParser<'ctx, S, E>
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	type Output = Link<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "masked_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let bytes = input.as_bytes();
		if bytes.first() != Some(&TEXT_OPENER) {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Char)
			})));
		}

		if *self.context.hints.get(&Grammar::MaskedLinkText) == ByteHint::Absent {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Alt)
			})));
		}

		map(
			pair(
				text::segment::<S, E>(self.context.clone()),
				link::segment::<E>(self.context),
			),
			|(text, (url, title))| Link {
				text: Some(text),
				url,
				title,
			},
		)
		.process::<OM>(input)
	}
}

/// Parse a masked link.
///
/// # Errors
/// If the content does not begin with a masked link.
#[must_use]
pub fn masked<'ctx, 'data, S, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Link<'data, S>, Error = E> + 'ctx
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	MaskedParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}
#[cfg(test)]
mod test {
	use nom::{Finish, Parser};
	use url::Url;

	use super::masked;
	use crate::context::Context;
	use crate::inline::link::Link;
	use crate::node::Node;
	use crate::test_utils::handle_nom_err;
	use crate::{bold, italic, spanned_vec, text};

	/// A schemaless link in the text segment is rejected the same way a URL is.
	#[test]
	fn schemaless_link_in_text_is_rejected() {
		for s in [
			r"[discord.gg/evil](https://good.com)",
			// the guard also reads the text backwards, to catch right-to-left overrides
			r"[live/gg.drocsid](https://good.com)",
		] {
			masked::<(), _>(&Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect_err("able to parse");
		}
	}

	/// The guard reads the text segment at every depth.
	///
	/// `Node::content` used to stop at the direct children, so two levels of markup looked like a
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
			masked::<(), _>(&Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect_err("able to parse");
		}
	}

	/// Reading every depth must not reject ordinary markup.
	#[test]
	fn nested_markup_without_a_link_is_allowed() {
		for s in [
			r"[**click here**](https://good.com)",
			r"[**_click here_**](https://good.com)",
			r"[**my discord server**](https://good.com)",
		] {
			masked::<(), _>(&Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect("unable to parse");
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
			masked::<(), _>(&Context::default())
				.parse_complete(s.into())
				.finish()
				.map_err(handle_nom_err(s))
				.expect_err("able to parse");
		}
	}

	/// The title guard must not reject titles that only read like prose.
	#[test]
	fn benign_title_is_allowed() {
		let s = r#"[foo](https://good.com "my discord server")"#;
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
	}

	/// A schemaless link is a valid target.
	#[test]
	fn schemaless_link_target() {
		let s = r"[join](discord.gg/abc)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn simple_masked_link() {
		let s = r"[test](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("unable to parse");
	}

	// TODO - we need to conditionally allow this. Webhooks are allowed to do this.
	#[test]
	fn no_emoji() {
		let s = r"[<:abcd:1234>](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("foo".into())]),
				title: Some("Will Nelson's website".to_string()),
			}
		);
	}

	#[test]
	fn masked_link_with_parens() {
		let s = "[Endemic](https://en.wikipedia.org/wiki/Endemic_(epidemiology))";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)").unwrap(),
				text: Some(spanned_vec![Node::Text("Endemic".into())]),
				title: None,
			}
		);
	}

	/// Markup between the characters of a URL must not hide it from [`super::has_no_link`]:
	/// `**h**ttp*s*://foo` renders as `https://foo`, so the masked link is rejected.
	#[test]
	fn masked_link_with_link() {
		let s = r"[foo **h**ttp*s*://foo](https://wnelson.dev)";
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	/// The underscore spelling of the case above is no longer a hiding technique: an intraword `_`
	/// does not open an italic (see [`crate::grammar::Grammar::override_start_sequence`]), so the
	/// text renders as the literal `http_s_://foo`, which is not a URL and does not spoof one.
	#[test]
	fn masked_link_with_intraword_underscores_is_not_a_hidden_link() {
		let s = r"[foo **h**ttp_s_://foo](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
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
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("[foo] bar".into())]),
				title: None,
			}
		);
	}

	#[test]
	fn masked_link_with_complex_matching_brackets() {
		let s = r"[foo [bar_baz]](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("foo [bar_baz]".into())]),
				title: None,
			}
		);
	}
}
