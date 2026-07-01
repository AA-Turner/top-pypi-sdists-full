use std::{fmt::Debug, marker::PhantomData};

use discord_confusables::SOURCES_BY_PROTOTYPE;
use nom::{
	character::complete::char,
	combinator::{not, verify},
	sequence::delimited,
	Check, Complete, Finish, OutputM, Parser,
};
use tracing::Level;

use crate::{
	context::Context,
	error::ParseError,
	inline::{
		self,
		link::{is_suspicious_whitespace, verify_url},
	},
	node::SpannedNodes,
	span::{Span, TraceOk, TraceParse},
	Input,
};

use super::Grammar;

#[tracing::instrument(level = Level::TRACE)]
fn has_no_url<'data, S: Span>(nodes: &SpannedNodes<'data, S>, context: &Context) -> bool {
	let text = nodes
		.iter()
		.map(|span| span.content())
		.collect::<String>() // TODO: figure out lifetimes to avoid this
		.chars()
		.filter(|ch| !is_suspicious_whitespace(*ch))
		.collect::<String>();

	let process_text = |mut text: String| -> bool {
		for prot in ["h", "t", "p", "s"] {
			let sources = SOURCES_BY_PROTOTYPE[prot];
			for source in sources {
				text = text.replace(*source, prot);
			}
		}

		let context = context.fresh();
		for (idx, _) in text.match_indices("http") {
			let parse_result = not(verify_url::<()>(&context))
				.process::<OutputM<Check, Check, Complete>>((&text[idx..]).into())
				.finish();
			if parse_result.is_err() {
				return false;
			}
		}

		true
	};

	process_text(text.chars().rev().collect()) && process_text(text)
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
				|nodes| has_no_url::<S>(nodes, &self.context),
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
}
