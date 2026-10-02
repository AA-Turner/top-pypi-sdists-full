use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	bytes::take_until1,
	character::complete::{char, space1},
	combinator::{opt, verify},
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

use super::{auto, has_no_link, verify_url, Grammar};

/// Parse a masked link title.
///
/// The title is shown to the reader on hover, so it carries the same guard as the text segment: a
/// title that reads as a link masks a destination the reader never sees.
fn parse_title<'data, E>(data: Input<'data>, context: &Context) -> IResult<Input<'data>, String, E>
where
	E: ParseError<'data>,
{
	verify(
		delimited(char('"'), take_until1("\""), char('"'))
			.map(|title: Input<'_>| title.to_string()),
		|title: &str| has_no_link(title, context),
	)
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
		let context = self.context;
		delimited(
			char('('),
			(
				// TODO: handle matched parentheses inside the link content
				alt((
					auto::auto(self.context.clone()),
					verify_url(&self.link_grammar),
				)),
				opt(preceded(space1, |data| parse_title(data, context))),
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
