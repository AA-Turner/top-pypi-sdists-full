use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	bytes::take_until1,
	character::complete::{char, space1},
	combinator::opt,
	sequence::{delimited, preceded},
	IResult, Parser,
};
use tracing::Level;
use url::Url;

use crate::{
	context::Context,
	error::ParseError,
	span::{TraceOk, TraceParse},
	Input,
};

use super::{auto, verify_url, Grammar};

/// Parse a masked link title.
fn parse_title<'data, E>(data: Input<'data>) -> IResult<Input<'data>, String, E>
where
	E: ParseError<'data>,
{
	delimited(char('"'), take_until1("\""), char('"'))
		.map(|title: Input<'data>| title.to_string())
		.parse_complete(data)
}

struct SegmentParser<'ctx, E> {
	context: &'ctx Context,
	link_grammar: Context,
	error: PhantomData<E>,
}

impl<E> Debug for SegmentParser<'_, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("SegmentParser")
			.field("context", &self.context)
			.field("link_grammar", &self.link_grammar)
			.field("error", &self.error)
			.finish()
	}
}

impl<'ctx, 'data, E> Parser<Input<'data>> for SegmentParser<'ctx, E>
where
	E: ParseError<'data> + 'ctx,
{
	type Output = (Url, Option<String>);
	type Error = E;

	#[tracing::instrument(name = "segment_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		delimited(
			char('('),
			(
				// TODO: handle matched parentheses inside the link content
				alt((
					auto::auto(self.context.clone()),
					verify_url(&self.link_grammar),
				)),
				opt(preceded(space1, parse_title)),
			),
			char(')'),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse the link segment of a masked link, including its title.
pub fn segment<'ctx, 'data, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = (Url, Option<String>), Error = E> + 'ctx
where
	E: ParseError<'data> + 'ctx,
{
	let link_grammar = context.clone().with_grammar(Grammar::MaskedLinkLink);
	SegmentParser {
		context,
		link_grammar,
		error: PhantomData,
	}
}
