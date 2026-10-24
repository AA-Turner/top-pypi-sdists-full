use std::{fmt::Debug, marker::PhantomData};

use nom::{
	OutputMode, PResult, Parser,
	branch::alt,
	bytes::complete::tag,
	character::complete::line_ending,
	combinator::{eof, fail},
};
use tracing::Level;

use crate::{Input, error::ParseError, node::inline::link, span::TraceOk};

use super::Scope;

pub struct TerminalSequence<E>(pub Scope, pub PhantomData<E>);

impl<E> Debug for TerminalSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("TerminalSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for TerminalSequence<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "grammar_terminal_sequence", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			// QuoteRest has no terminal sequence
			Scope::None | Scope::QuoteRest => fail().process::<OM>(input),
			Scope::InlineBlock | Scope::Block | Scope::Quote => {
				alt((line_ending, eof)).process::<OM>(input)
			}
			Scope::AutoLink => tag(&[link::auto::TERMINAL][..]).process::<OM>(input),
			Scope::MaskedLinkText => tag(&[link::masked::TEXT_TERMINAL][..]).process::<OM>(input),
			Scope::MaskedLinkLink => tag(&[link::masked::LINK_TERMINAL][..]).process::<OM>(input),
		}
		.trace_ok()
	}
}
