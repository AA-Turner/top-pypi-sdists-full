use std::{fmt::Debug, marker::PhantomData};

use nom::{combinator::map, OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	block::{heading, list, quote, small},
	error::ParseError,
	grammar::{ByteHint, Grammar},
	inline::{
		bold, code, code_block, emoji, italic, link, mention, spoiler, strikethrough, timestamp,
		underline,
	},
	node::Node,
	rule::Rule,
	span::{Span, TraceOk, TraceParse},
	Input,
};

use super::Context;

pub struct ContextualRule<'ctx, S, E> {
	pub rule: Rule,
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
	type Output = Node<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "contextual_rule", level = Level::TRACE, fields(ok, output))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.rule {
			Rule::Bold => map(bold::bold(self.context.clone()), Node::Bold)
				.trace_parse()
				.process::<OM>(input),
			Rule::Emoji => {
				if *self.context.hints.get(&Grammar::CustomEmoji) == ByteHint::Absent {
					map(emoji::parse_unicode, Node::Emoji)
						.trace_parse()
						.process::<OM>(input)
				} else {
					map(emoji::parse, Node::Emoji)
						.trace_parse()
						.process::<OM>(input)
				}
			}
			Rule::Italic => map(italic::italic(self.context.clone()), Node::Italic)
				.trace_parse()
				.process::<OM>(input),
			Rule::Link => map(link::link(self.context), Node::Link)
				.trace_parse()
				.process::<OM>(input),
			Rule::Mention => map(mention::mention(), Node::Mention)
				.trace_parse()
				.process::<OM>(input),
			Rule::Strikethrough => map(
				strikethrough::strikethrough(self.context.clone()),
				Node::Strikethrough,
			)
			.trace_parse()
			.process::<OM>(input),
			Rule::Timestamp => map(timestamp::timestamp(), Node::Timestamp)
				.trace_parse()
				.process::<OM>(input),
			Rule::Underline => map(underline::underline(self.context.clone()), Node::Underline)
				.trace_parse()
				.process::<OM>(input),
			Rule::Code => map(code::code(), |code| Node::Code(code.content))
				.trace_parse()
				.process::<OM>(input),
			Rule::CodeBlock => map(code_block::code_block(), Node::CodeBlock)
				.trace_parse()
				.process::<OM>(input),
			Rule::Spoiler => map(spoiler::spoiler(self.context.clone()), Node::Spoiler)
				.trace_parse()
				.process::<OM>(input),
			Rule::Heading => map(heading::heading(self.context.clone()), Node::Heading)
				.trace_parse()
				.process::<OM>(input),
			Rule::List => map(list::list(self.context.clone()), Node::List)
				.trace_parse()
				.process::<OM>(input),
			Rule::Quote => map(quote::quote(self.context.clone()), Node::Quote)
				.trace_parse()
				.process::<OM>(input),
			Rule::Small => map(small::small(self.context.clone()), Node::Small)
				.trace_parse()
				.process::<OM>(input),
		}
		.trace_ok()
	}
}
