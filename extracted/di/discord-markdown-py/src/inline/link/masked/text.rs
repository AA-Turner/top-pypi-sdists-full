use std::{fmt::Debug, marker::PhantomData};

use nom::{character::complete::char, combinator::verify, sequence::delimited, Parser};
use tracing::Level;

use crate::{
	context::Context,
	error::ParseError,
	inline::{self, link::is_suspicious_whitespace},
	node::SpannedNodes,
	span::{Span, TraceOk, TraceParse},
	Input,
};

use super::{has_no_link, Grammar};

/// Whether the parsed text segment of a masked link is free of anything that reads as a link.
///
/// The guard reads the segment at every depth, so markup between the characters of a URL cannot
/// hide it: `**h**ttp*s*://foo` renders as `https://foo`.
#[tracing::instrument(level = Level::TRACE)]
fn segment_has_no_link<'data, S: Span>(nodes: &SpannedNodes<'data, S>, context: &Context) -> bool {
	// TODO: figure out lifetimes to avoid this
	let text = nodes.iter().map(|span| span.content()).collect::<String>();

	has_no_link(&text, context)
}

fn segment_is_not_whitespace<S: Span>(nodes: &SpannedNodes<'_, S>) -> bool {
	nodes.iter().any(|span| {
		span.content()
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
	type Output = SpannedNodes<'data, S>;
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
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
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

	use crate::{context::Context, node::Node, spanned_vec, test_utils::handle_nom_err};

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
		assert_eq!(res, spanned_vec!(Node::Text("foo".into())));
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
		assert_eq!(res, spanned_vec!(Node::Text("foo [bar]".into())));
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
