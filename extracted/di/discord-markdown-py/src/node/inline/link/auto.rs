//! Auto-link parsing
//!
//! Note that this is _not_ [`crate::node::inline::link::detection`]. Auto-links are links inside angle
//! brackets, such as `<https://discord.com>`.

use url::Url;

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	lossless::TokenKind,
	scope::Scope,
	span::{Span, Syntax as _, Trace},
	syntax::Syntax,
};

use super::{Link, ParsedLink, shown_url, verify_url};

/// The sequence that opens an auto-link.
pub const OPEN_DELIMITER: &str = "<";
/// The terminal character of an auto-link.
pub const TERMINAL: u8 = b'>';

/// Parse `url` between an auto-link's delimiters.
fn delimited<'data, S: Span, T>(
	input: &mut Input<'data>,
	context: &Context,
	url: impl FnOnce(&mut Input<'data>, &Context) -> PResult<(T, S::Syntax)>,
) -> PResult<(T, S::Syntax)> {
	// also run inside a masked link, whose URL can be written as an auto link
	if context.hints.rules_out(Syntax::AutoLink) {
		return Err(Fail::NoMatch);
	}
	let context = context.clone().with_scope(Scope::AutoLink);

	let open = input.token::<S, _>(TokenKind::LinkOpen, |input| input.char('<'))?;
	let (url, syntax) = url(input, &context)?;
	let close = input.token::<S, _>(TokenKind::LinkClose, |input| input.char('>'))?;
	Ok((url, open.join(syntax).join(close)))
}

/// Parse auto-link content that is only a destination, as a masked link's URL can be written.
///
/// # Errors
/// If the content does not begin with an auto-link.
#[tracing::instrument(name = "auto_parser", level = "trace", skip_all, fields(ok, output))]
pub fn auto<S: Span>(input: &mut Input, context: &Context) -> PResult<(Url, S::Syntax)> {
	delimited::<S, _>(input, context, |input, context| {
		input.with_token::<S, _>(TokenKind::Url, |input| verify_url(input, context))
	})
	.trace()
}

/// Parse an auto-link that is shown on its own, with the text it was written as if its URL
/// alone would not read back that way. See [`shown_url`].
///
/// # Errors
/// If the content does not begin with an auto-link.
#[tracing::instrument(
	name = "auto_link_parser",
	level = "trace",
	skip_all,
	fields(ok, output)
)]
pub fn link<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<ParsedLink<'data, S>> {
	let ((url, text), syntax) = delimited::<S, _>(input, context, |input, context| {
		let (url, text, syntax) = shown_url(input, context)?;
		Ok(((url, text), syntax))
	})?;
	let link = Link {
		text,
		url,
		title: None,
	};
	Ok((link, syntax)).trace()
}

#[cfg(test)]
mod test {
	use crate::{Context, node::Element, spanned_vec, test_utils::run};

	use super::{Link, auto, link};

	#[test]
	fn simple_link() {
		let s = "<https://wnelson.dev>";
		let (rem, (res, ())) =
			run(s, |input| auto::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "https://wnelson.dev".parse().unwrap());
	}

	/// A schemaless link is still schemaless inside an autolink.
	#[test]
	fn schemaless_link() {
		let s = "<discord.gg/abc>";
		let (rem, (res, ())) =
			run(s, |input| auto::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "https://discord.gg/abc".parse().unwrap());
	}

	/// Shown on its own, a schemaless link's text is what was written, without the scheme it
	/// was given.
	#[test]
	fn shown_schemaless_link_keeps_its_text() {
		let s = "<discord.gg/abc>";
		let (rem, (res, ())) =
			run(s, |input| link::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				text: Some(spanned_vec![Element::Text("discord.gg/abc".into())]),
				url: "https://discord.gg/abc".parse().unwrap(),
				title: None,
			}
		);
	}

	/// A URL with a scheme reads back as written, so it needs no text.
	#[test]
	fn shown_link_with_a_scheme_has_no_text() {
		let s = "<https://wnelson.dev>";
		let (rem, (res, ())) =
			run(s, |input| link::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res.text, None);
	}

	#[test]
	fn tel_link() {
		let s = "<tel:+1-800-588-2300>";
		let (rem, (res, ())) =
			run(s, |input| auto::<()>(input, &Context::default())).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(res, "tel:+1-800-588-2300".parse().unwrap());
	}

	/// A path the client does not route is not schemaless, so there is no URL here at all.
	#[test]
	fn schemaless_non_routed_link_is_rejected() {
		let s = "<discord.com/developers/docs>";
		run(s, |input| auto::<()>(input, &Context::default())).expect_err("able to parse");
	}
}
