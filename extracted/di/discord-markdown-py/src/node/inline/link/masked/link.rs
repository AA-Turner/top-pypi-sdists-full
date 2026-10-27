use std::{fmt::Debug, marker::PhantomData};

use nom::{
	IResult, Parser,
	branch::alt,
	bytes::take_until1,
	character::complete::{char, space1},
	combinator::{opt, verify},
	sequence::delimited,
};
use tracing::Level;
use url::Url;

use crate::{
	Input,
	context::Context,
	error::ParseError,
	lossless::TokenKind,
	span::{Span, Syntax, TraceOk, TraceParse, WithToken},
};

use super::{Scope, auto, has_no_link, verify_url};

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

struct SegmentParser<'ctx, S, E> {
	context: &'ctx Context,
	link_grammar: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for SegmentParser<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("SegmentParser")
			.field("context", &self.context)
			.field("link_grammar", &self.link_grammar)
			.field("error", &self.error)
			.finish()
	}
}

impl<'ctx, 'data, S, E> Parser<Input<'data>> for SegmentParser<'ctx, S, E>
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	type Output = (Url, Option<String>, S::Syntax);
	type Error = E;

	#[tracing::instrument(name = "segment_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let context = self.context;
		(
			char('(').token::<S>(TokenKind::DestinationOpen),
			// TODO: handle matched parentheses inside the link content
			alt((
				auto::auto::<S, E>(self.context.clone()),
				verify_url(&self.link_grammar).with_token::<S>(TokenKind::Url),
			)),
			opt((
				space1.token::<S>(TokenKind::Whitespace),
				(|data| parse_title(data, context)).with_token::<S>(TokenKind::Title),
			)),
			char(')').token::<S>(TokenKind::DestinationClose),
		)
			.map(|(open, (url, url_syntax), title, close)| {
				let (title, title_syntax) = match title {
					Some((space, (title, title_syntax))) => (Some(title), space.join(title_syntax)),
					None => (None, S::Syntax::default()),
				};
				let syntax = open.join(url_syntax).join(title_syntax).join(close);
				(url, title, syntax)
			})
			.trace_parse()
			.process::<OM>(input)
			.trace_ok()
	}
}

/// Parse the link segment of a masked link, including its title.
pub fn segment<'ctx, 'data, S, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = (Url, Option<String>, S::Syntax), Error = E> + 'ctx
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	let link_grammar = context.clone().with_scope(Scope::MaskedLinkLink);
	SegmentParser {
		context,
		link_grammar,
		span: PhantomData::<S>,
		error: PhantomData,
	}
}
