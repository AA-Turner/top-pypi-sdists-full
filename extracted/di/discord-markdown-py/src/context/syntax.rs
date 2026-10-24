use std::{borrow::Cow, fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser, combinator::fail};
use tracing::Level;

use crate::{
	Input,
	error::ParseError,
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
	span::{Span, TraceOk, TraceParse},
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

impl<'data, S, E> Parser<Input<'data>> for ContextualSyntax<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = Element<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "contextual_syntax", level = Level::TRACE, fields(ok, output))]
	#[allow(clippy::too_many_lines, reason = "one arm per syntax")]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let context = self.context;
		match self.syntax {
			Syntax::CustomEmoji => emoji::custom::parse
				.map(|custom| Element::Emoji(Emoji::Custom(custom)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::ColonEmoji => emoji::colon_delimited::emoji()
				.map(|emoji| Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji))))
				.trace_parse()
				.process::<OM>(input),
			Syntax::UnicodeEmoji => emoji::unicode::emoji()
				.map(|emoji: Input<'data>| {
					Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji.content)))
				})
				.trace_parse()
				.process::<OM>(input),
			Syntax::MaskedLink => link::masked::masked(context)
				.map(Element::Link)
				.trace_parse()
				.process::<OM>(input),
			Syntax::DetectedLink => link::detection::detection(context)
				.map(Element::Link)
				.trace_parse()
				.process::<OM>(input),
			Syntax::AutoLink => link::auto::auto(context.clone())
				.map(|url| {
					Element::Link(Link {
						text: None,
						title: None,
						url,
					})
				})
				.trace_parse()
				.process::<OM>(input),
			Syntax::ContactLink => link::contact::contact(context.clone())
				.map(Element::Link)
				.trace_parse()
				.process::<OM>(input),
			Syntax::UserMention => mention::user()
				.map(|id| Element::Mention(Mention::User(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::ChannelMention => mention::channel()
				.map(|id| Element::Mention(Mention::Channel(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::RoleMention => mention::role()
				.map(|id| Element::Mention(Mention::Role(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::GameMention => mention::game()
				.map(|id| Element::Mention(Mention::Game(id)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::CommandMention => mention::command::command()
				.map(|command| Element::Mention(Mention::Command(command)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::EveryoneMention => mention::everyone()
				.map(|_| Element::Mention(Mention::Everyone))
				.trace_parse()
				.process::<OM>(input),
			Syntax::HereMention => mention::here()
				.map(|_| Element::Mention(Mention::Here))
				.trace_parse()
				.process::<OM>(input),
			Syntax::StaticMention => mention::r#static::parser()
				.map(|mention| Element::Mention(Mention::Static(mention)))
				.trace_parse()
				.process::<OM>(input),
			Syntax::Timestamp => timestamp::timestamp()
				.map(Element::Timestamp)
				.trace_parse()
				.process::<OM>(input),
			Syntax::CodeBlock => code_block::code_block()
				.map(Element::CodeBlock)
				.trace_parse()
				.process::<OM>(input),
			Syntax::Code => code::single()
				.map(|code: Input<'data>| Element::Code(code.content.into()))
				.trace_parse()
				.process::<OM>(input),
			Syntax::DoubleCode => code::double()
				.map(|code: Input<'data>| Element::Code(code.content.into()))
				.trace_parse()
				.process::<OM>(input),
			Syntax::Heading => heading::heading(context.clone())
				.map(Element::Heading)
				.trace_parse()
				.process::<OM>(input),
			Syntax::List => list::list(context.clone())
				.map(Element::List)
				.trace_parse()
				.process::<OM>(input),
			Syntax::Quote => quote::quote_line(context.clone())
				.map(Element::Quote)
				.trace_parse()
				.process::<OM>(input),
			Syntax::MultilineQuote => quote::quote_rest(context.clone())
				.map(Element::Quote)
				.trace_parse()
				.process::<OM>(input),
			Syntax::Small => small::small(context.clone())
				.map(Element::Small)
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
