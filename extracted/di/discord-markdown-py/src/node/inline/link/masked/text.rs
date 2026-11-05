use tracing::Level;

use crate::{
	Input,
	context::{Context, fuel::OutOfFuel},
	error::PResult,
	lossless::TokenKind,
	node::{
		Elements, Ids,
		inline::{self, link::is_suspicious_whitespace},
	},
	range,
	span::{Span, Syntax, Trace},
};

use super::{Scope, has_no_link};

/// Whether the parsed text segment of a masked link is free of anything that reads as a link.
///
/// The guard reads the segment at every depth, so markup between the characters of a URL cannot
/// hide it: `**h**ttp*s*://foo` renders as `https://foo`. It reads the segment as rendered, with
/// its delimiters resolved -- link text is a scope of its own -- so the ones that pair vanish and
/// the ones that do not, like the underscores in `http_s_://foo`, stay as text.
///
/// # Errors
/// If the parse runs out of fuel.
#[tracing::instrument(level = Level::TRACE)]
pub fn segment_has_no_link<S: Span>(
	nodes: &Elements<'_, S>,
	context: &Context,
) -> Result<bool, OutOfFuel> {
	let rendered =
		range::resolve_inline(nodes.value.clone(), context.syntaxes, &mut Ids::default());
	// TODO: figure out lifetimes to avoid this
	let text = rendered
		.iter()
		.map(|span| span.content())
		.collect::<String>();

	has_no_link(&text, context)
}

/// Whether the parsed text segment of a masked link shows the reader anything at all. Blank text
/// is a link the reader cannot see.
///
/// Read before the delimiters resolve, so a segment of nothing but delimiters, like `[**]`, counts
/// as empty.
pub fn segment_is_not_whitespace<S: Span>(nodes: &Elements<'_, S>) -> bool {
	nodes.iter().any(|node| {
		node.value
			.content()
			.chars()
			.any(|ch| !is_suspicious_whitespace(ch) && !ch.is_whitespace())
	})
}

/// Parse the text segment of a masked link.
///
/// This does not run [`segment_has_no_link`] or [`segment_is_not_whitespace`]: the caller does,
/// once it knows the whole link. The segment can be empty, as in `[](url)`, so that it reaches
/// those guards too.
///
/// # Errors
/// If the content does not begin with a text segment.
#[tracing::instrument(name = "segment_parser", level = Level::TRACE, skip_all, fields(ok, output))]
pub fn segment<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<(Elements<'data, S>, S::Syntax)> {
	let open = input.token::<S, _>(TokenKind::LinkOpen, |input| input.char('['))?;
	let text = match input.attempt(|input| {
		inline::inline(input, &context.clone().with_scope(Scope::MaskedLinkText))
	})? {
		Some(text) => text,
		None => input.spanned(|_| Ok(Vec::new()))?,
	};
	let close = input.token::<S, _>(TokenKind::LinkClose, |input| input.char(']'))?;
	Ok((text, open.join(close))).trace()
}

#[cfg(test)]
mod test {
	use crate::{
		context::Context,
		spanned_vec,
		test_utils::{resolved_inlines, run},
		text,
	};

	use super::{segment, segment_has_no_link, segment_is_not_whitespace};

	fn parse(
		s: &str,
	) -> crate::error::PResult<(crate::Input<'_>, (crate::node::Elements<'_, ()>, ()))> {
		run(s, |input| segment::<()>(input, &Context::default()))
	}

	/// Whether the text segment `s` passes the guard.
	fn has_no_link(s: &str) -> bool {
		let (_, (text, ())) = parse(s).expect("unable to parse");
		segment_has_no_link(&text, &Context::default()).expect("the default budget is enough")
	}

	#[test]
	fn basic_text() {
		let s = "[foo]";
		let (rem, (res, ())) = parse(s).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec!(text!("foo")));
	}

	#[test]
	fn skips_matching_brackets() {
		let s = "[foo [bar]]";
		let (rem, (res, ())) = parse(s).expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec!(text!("foo [bar]")));
	}

	#[test]
	fn detect_reversed_urls() {
		let s = "[moc.drocsid//:sptth]";
		assert!(!has_no_link(s));
	}

	#[test]
	fn detect_confusables() {
		let s = "[ℎttps://discord.com]";
		assert!(!has_no_link(s));
	}

	#[test]
	fn detect_confusable_punctuation() {
		// MODIFIER LETTER COLON in place of the scheme separator.
		let s = "[https\u{A789}//discord.com]";
		assert!(!has_no_link(s));
	}

	#[test]
	fn detect_rtl_override_urls() {
		// RIGHT-TO-LEFT OVERRIDE displays the reversed URL forwards.
		let s = "[\u{202E}moc.drocsid//:sptth]";
		assert!(!has_no_link(s));
	}

	#[test]
	fn text_is_whitespace() {
		for s in ["[ \u{200d}]", "[**]", "[]"] {
			let (rem, (text, ())) = parse(s).expect("unable to parse");
			assert_eq!(rem, "", "{s}");
			assert!(!segment_is_not_whitespace(&text), "{s}");
		}
	}
}
