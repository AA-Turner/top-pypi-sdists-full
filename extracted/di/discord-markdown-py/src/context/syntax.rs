use std::{borrow::Cow, fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser, combinator::fail};
use tracing::Level;

use crate::{
	Input,
	error::ParseError,
	lossless::{LinkKind, QuoteKind, TokenKind},
	node::{
		Element,
		block::{heading, list, quote, small},
		inline::{
			code, code_block,
			emoji::{self, Emoji},
			link::{self, Link},
			mention::{self, Mention},
			timestamp,
		},
	},
	span::{Span, TraceOk, TraceParse, WithToken},
	syntax::Syntax,
};

use super::Context;

/// A [`Syntax`]'s parser, run in a [`Context`].
pub struct ContextualSyntax<'ctx, S, E> {
	pub syntax: Syntax,
	pub context: &'ctx Context,
	pub span: PhantomData<S>,
	pub error: PhantomData<E>,
}

impl<S, E> Debug for ContextualSyntax<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("ContextualSyntax")
			.field("syntax", &self.syntax)
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

/// An element written as one piece, like a mention: its whole input is one [`TokenKind::Atom`].
fn atom<'data, S, P>(
	parser: P,
	element: impl Fn(P::Output) -> Element<'data, S>,
) -> impl Parser<Input<'data>, Output = (Element<'data, S>, S::Syntax), Error = P::Error>
where
	S: Span,
	P: Parser<Input<'data>>,
{
	parser
		.with_token::<S>(TokenKind::Atom)
		.map(move |(value, syntax)| (element(value), syntax))
}

/// An element whose syntax its own parsers record, in the spans inside it.
fn block<S: Span>(element: Element<'_, S>) -> (Element<'_, S>, S::Syntax) {
	(element, S::Syntax::default())
}

impl<'data, S, E> Parser<Input<'data>> for ContextualSyntax<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	/// The element, with the syntax it was written with outside its children.
	type Output = (Element<'data, S>, S::Syntax);
	type Error = E;

	#[tracing::instrument(name = "contextual_syntax", level = Level::TRACE, fields(ok, output))]
	#[allow(clippy::too_many_lines, reason = "one arm per syntax")]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let context = self.context;
		match self.syntax {
			Syntax::CustomEmoji => atom(emoji::custom::parse, |custom| {
				Element::Emoji(Emoji::Custom(custom))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::ColonEmoji => atom(emoji::colon_delimited::emoji(), |emoji| {
				Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji)))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::UnicodeEmoji => atom(emoji::unicode::emoji(), |emoji: Input<'data>| {
				Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji.content)))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::MaskedLink => link::masked::masked(context)
				.map(|(link, syntax)| (Element::Link(LinkKind::Masked, link), syntax))
				.trace_parse()
				.process::<OM>(input),
			Syntax::DetectedLink => link::detection::detection(context)
				.map(|(link, syntax)| (Element::Link(LinkKind::Detected, link), syntax))
				.trace_parse()
				.process::<OM>(input),
			Syntax::AutoLink => link::auto::auto::<S, E>(context.clone())
				.map(|(url, syntax)| {
					let link = Link {
						text: None,
						title: None,
						url,
					};
					(Element::Link(LinkKind::Auto, link), syntax)
				})
				.trace_parse()
				.process::<OM>(input),
			Syntax::ContactLink => link::contact::contact(context.clone())
				.map(|(link, syntax)| (Element::Link(LinkKind::Contact, link), syntax))
				.trace_parse()
				.process::<OM>(input),
			Syntax::UserMention => atom(mention::user(), |id| Element::Mention(Mention::User(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::ChannelMention => atom(mention::channel(), |id| {
				Element::Mention(Mention::Channel(id))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::RoleMention => atom(mention::role(), |id| Element::Mention(Mention::Role(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::GameMention => atom(mention::game(), |id| Element::Mention(Mention::Game(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::CommandMention => atom(mention::command::command(), |command| {
				Element::Mention(Mention::Command(command))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::EveryoneMention => {
				atom(mention::everyone(), |_| Element::Mention(Mention::Everyone))
					.trace_parse()
					.process::<OM>(input)
			}
			Syntax::HereMention => atom(mention::here(), |_| Element::Mention(Mention::Here))
				.trace_parse()
				.process::<OM>(input),
			Syntax::StaticMention => atom(mention::r#static::parser(), |mention| {
				Element::Mention(Mention::Static(mention))
			})
			.trace_parse()
			.process::<OM>(input),
			Syntax::Timestamp => atom(timestamp::timestamp(), Element::Timestamp)
				.trace_parse()
				.process::<OM>(input),
			Syntax::CodeBlock => code_block::code_block::<S, E>()
				.map(|(code_block, syntax)| (Element::CodeBlock(code_block), syntax))
				.trace_parse()
				.process::<OM>(input),
			Syntax::Code => code::single::<S, E>()
				.map(|(code, syntax): (Input<'data>, _)| {
					(Element::Code(code.content.into()), syntax)
				})
				.trace_parse()
				.process::<OM>(input),
			Syntax::DoubleCode => code::double::<S, E>()
				.map(|(code, syntax): (Input<'data>, _)| {
					(Element::Code(code.content.into()), syntax)
				})
				.trace_parse()
				.process::<OM>(input),
			Syntax::Heading => heading::heading(context.clone())
				.map(|heading| block(Element::Heading(heading)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::List => list::list(context.clone())
				.map(|list| block(Element::List(list)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::Quote => quote::quote_line(context.clone())
				.map(|content| block(Element::Quote(QuoteKind::Line, content)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::MultilineQuote => quote::quote_rest(context.clone())
				.map(|content| block(Element::Quote(QuoteKind::Rest, content)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::Small => small::small(context.clone())
				.map(|small| block(Element::Small(small)))
				.trace_parse()
				.process::<OM>(input),
			// recorded as delimiters and resolved after the parse; see `crate::range`
			Syntax::Bold
			| Syntax::AsteriskItalic
			| Syntax::UnderscoreItalic
			| Syntax::Underline
			| Syntax::Strikethrough
			| Syntax::Spoiler => fail().process::<OM>(input),
		}
		.trace_ok()
	}
}
