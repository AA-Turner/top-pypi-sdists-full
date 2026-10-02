use std::{fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	error::ParseError,
	node::Node,
	rule::RuleSet,
	span::{Span, TraceOk, TraceParse},
	util::iter_alt,
	Input,
};

use super::{rule::ContextualRule, Context};

/// [`RuleSet`] with [`Context`], enabling parsing.
#[derive(Clone)]
pub struct ContextualRules<'ctx, S, E> {
	context: &'ctx Context,
	rules: RuleSet,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for ContextualRules<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("ContextualRules")
			.field("context", &self.context)
			.field("rules", &self.rules)
			.field("error", &self.error)
			.finish_non_exhaustive()
	}
}

impl<'ctx, S, E> ContextualRules<'ctx, S, E> {
	#[must_use]
	pub fn from_context(context: &'ctx Context, rules: RuleSet) -> Self {
		ContextualRules {
			context,
			rules,
			span: PhantomData,
			error: PhantomData,
		}
	}
}

impl<'data, S, E> Parser<Input<'data>> for ContextualRules<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Error = E;
	type Output = Node<'data, S>;

	#[tracing::instrument(name = "contextual_rules", level = Level::TRACE, fields(ok, output))]
	fn process<OM>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error>
	where
		OM: OutputMode,
	{
		iter_alt(|| {
			self.rules.iter().map(|rule| ContextualRule {
				rule,
				context: self.context,
				span: PhantomData,
				error: PhantomData,
			})
		})
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}
