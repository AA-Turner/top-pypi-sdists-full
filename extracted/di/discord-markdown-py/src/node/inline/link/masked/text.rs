use std::{fmt::Debug, marker::PhantomData};

use nom::{Parser, character::complete::char, combinator::verify, sequence::delimited};
use tracing::Level;

use crate::{
	Input,
	context::Context,
	error::ParseError,
	node::{
		Elements, Ids,
		inline::{self, link::is_suspicious_whitespace},
	},
	range,
	span::{Span, TraceOk, TraceParse},
};

use super::{Grammar, has_no_link};

/// Whether the parsed text segment of a masked link is free of anything that reads as a link.
///
/// The guard reads the segment at every depth, so markup between the characters of a URL cannot
/// hide it: `**h**ttp*s*://foo` renders as `https://foo`. It reads the segment as rendered, with
/// its delimiters resolved -- link text is a scope of its own -- so the ones that pair vanish and
/// the ones that do not, like the underscores in `http_s_://foo`, stay as text.
#[tracing::instrument(level = Level::TRACE)]
fn segment_has_no_link<S: Span>(nodes: &Elements<'_, S>, context: &Context) -> bool {
	let rendered = range::resolve_inline(
		nodes.value.clone(),
		context.allowed_rules,
		&mut Ids::default(),
	);
	// TODO: figure out lifetimes to avoid this
	let text = rendered
		.iter()
		.map(|span| span.content())
		.collect::<String>();

	has_no_link(&text, context)
}

/// Read before the delimiters resolve, so a segment of nothing but delimiters, like `[**]`, counts
/// as empty.
fn segment_is_not_whitespace<S: Span>(nodes: &Elements<'_, S>) -> bool {
	nodes.iter().any(|node| {
		node.value
			.content()
			.chars()
			.any(|ch| !is_suspicious_whitespace(ch) && !ch.is_whitespace())
	})
}

struct SegmentParser<S, E> {
	context: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for SegmentParser<S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("TextSegmentParser")
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for SegmentParser<S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = Elements<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "segment_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		delimited(
			char('['),
			verify(
				inline::inline(self.context.clone().with_grammar(Grammar::MaskedLinkText)),
				|nodes| {
					segment_has_no_link::<S>(nodes, &self.context)
						&& segment_is_not_whitespace(nodes)
				},
			),
			char(']'),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse the text segment of a masked link.
pub fn segment<'ctx, 'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = Elements<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	SegmentParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		context::Context,
		spanned_vec,
		test_utils::{handle_nom_err, resolved_inlines},
		text,
	};

	use super::segment;

	#[test]
	fn basic_text() {
		let s = "[foo]";
		let (rem, res) = segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec!(text!("foo")));
	}

	#[test]
	fn skips_matching_brackets() {
		let s = "[foo [bar]]";
		let (rem, res) = segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(resolved_inlines(res), spanned_vec!(text!("foo [bar]")));
	}

	#[test]
	fn detect_reversed_urls() {
		let s = "[moc.drocsid//:sptth]";
		segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn detect_confusables() {
		let s = "[ℎttps://discord.com]";
		segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn detect_confusable_punctuation() {
		// MODIFIER LETTER COLON in place of the scheme separator.
		let s = "[https\u{A789}//discord.com]";
		segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn detect_rtl_override_urls() {
		// RIGHT-TO-LEFT OVERRIDE displays the reversed URL forwards.
		let s = "[\u{202E}moc.drocsid//:sptth]";
		segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn text_is_whitespace() {
		let s = "[ \u{200d}]";
		segment::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}
}
