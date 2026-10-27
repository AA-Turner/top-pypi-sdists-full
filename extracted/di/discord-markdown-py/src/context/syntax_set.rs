use std::{fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser};
use tracing::Level;

use crate::{
	Input,
	error::ParseError,
	node::Element,
	span::{Span, TraceOk, TraceParse},
	syntax::{Syntax, SyntaxSet},
	util::iter_alt,
};

use super::{Context, syntax::ContextualSyntax};

/// [`SyntaxSet`] with [`Context`], enabling parsing. Tries each syntax in
/// [`Syntax::PARSE_ORDER`], skipping any the context's hints rule out.
#[derive(Clone)]
pub struct ContextualSyntaxes<'ctx, S, E> {
	context: &'ctx Context,
	syntaxes: SyntaxSet,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for ContextualSyntaxes<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("ContextualSyntaxes")
			.field("context", &self.context)
			.field("syntaxes", &self.syntaxes)
			.field("error", &self.error)
			.finish_non_exhaustive()
	}
}

impl<'ctx, S, E> ContextualSyntaxes<'ctx, S, E> {
	#[must_use]
	pub fn from_context(context: &'ctx Context, syntaxes: SyntaxSet) -> Self {
		ContextualSyntaxes {
			context,
			syntaxes,
			span: PhantomData,
			error: PhantomData,
		}
	}
}

impl<'data, S, E> Parser<Input<'data>> for ContextualSyntaxes<'_, S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Error = E;
	type Output = (Element<'data, S>, S::Syntax);

	#[tracing::instrument(name = "contextual_syntaxes", level = Level::TRACE, fields(ok, output))]
	fn process<OM>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error>
	where
		OM: OutputMode,
	{
		iter_alt(|| {
			Syntax::PARSE_ORDER
				.into_iter()
				.filter(|&syntax| {
					self.syntaxes.contains(syntax) && !self.context.hints.rules_out(syntax)
				})
				.map(|syntax| ContextualSyntax {
					syntax,
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
