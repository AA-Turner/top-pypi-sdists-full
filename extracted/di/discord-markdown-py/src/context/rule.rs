use std::{fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser, combinator::map};
use tracing::Level;

use crate::{
	Input,
	block::{heading, list, quote, small},
	error::ParseError,
	grammar::{ByteHint, Grammar},
	inline::{code, code_block, emoji, link, mention, timestamp},
	node::{Element, ParsedNode},
	rule::ParsedRule,
	span::{Span, TraceOk, TraceParse},
};

use super::Context;

pub struct ContextualRule<'ctx, S, E> {
	pub rule: ParsedRule,
	pub context: &'ctx Context,
	pub span: PhantomData<S>,
	pub error: PhantomData<E>,
}

impl<S, E> Debug for ContextualRule<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("RuleContext")
			.field("rule", &self.rule)
			.field("context", &self.context)
			.field("span", &self.span)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for ContextualRule<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = Element<'data, S, ParsedNode<'data, S>>;
	type Error = E;

	#[tracing::instrument(name = "contextual_rule", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.rule {
			ParsedRule::Emoji => {
				if *self.context.hints.get(&Grammar::CustomEmoji) == ByteHint::Absent {
					map(emoji::parse_unicode, Element::Emoji)
						.trace_parse()
						.process::<OM>(input)
				} else {
					map(emoji::parse, Element::Emoji)
						.trace_parse()
						.process::<OM>(input)
				}
			}
			ParsedRule::Link => map(link::link(self.context), Element::Link)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Mention => map(mention::mention(), Element::Mention)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Timestamp => map(timestamp::timestamp(), Element::Timestamp)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Code => map(code::code(), |code| Element::Code(code.content.into()))
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::CodeBlock => map(code_block::code_block(), Element::CodeBlock)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Heading => map(heading::heading(self.context.clone()), Element::Heading)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::List => map(list::list(self.context.clone()), Element::List)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Quote => map(quote::quote(self.context.clone()), Element::Quote)
				.trace_parse()
				.process::<OM>(input),
			ParsedRule::Small => map(small::small(self.context.clone()), Element::Small)
				.trace_parse()
				.process::<OM>(input),
		}
		.trace_ok()
	}
}
