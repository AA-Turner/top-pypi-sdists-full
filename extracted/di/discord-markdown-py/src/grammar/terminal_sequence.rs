use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	bytes::complete::tag,
	character::complete::line_ending,
	combinator::{eof, fail},
	error::ParseError,
	OutputMode, PResult, Parser,
};
use tracing::Level;

use crate::{
	inline::{
		bold, code, code_block, emoji, italic, link, mention, spoiler, strikethrough, timestamp,
		underline,
	},
	span::TraceOk,
	Input,
};

use super::Grammar;

pub struct TerminalSequence<E>(pub Grammar, pub PhantomData<E>);

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
	E: ParseError<Input<'data>>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "grammar_terminal_sequence", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Grammar::None | Grammar::EveryoneMention | Grammar::HereMention
			// TODO: this is a hack but link detection terminal chars don't actually matter for parsing purposes
			| Grammar::LinkDetection => fail().process::<OM>(input),
			Grammar::InlineBlock | Grammar::Block | Grammar::Quote => alt((line_ending, eof)).process::<OM>(input),
			Grammar::Bold => tag(bold::DELIMITER).process::<OM>(input),
			Grammar::UnderscoreItalic => tag(italic::UNDERSCORE_DELIMITER).process::<OM>(input),
			Grammar::AsteriskItalic => tag(italic::ASTERISK_DELIMITER).process::<OM>(input),
			Grammar::Spoiler => tag(spoiler::DELIMITER).process::<OM>(input),
			Grammar::Strikethrough => tag(strikethrough::DELIMITER).process::<OM>(input),
			Grammar::Underline => tag(underline::DELIMITER).process::<OM>(input),
			Grammar::AutoLink => tag(&[link::auto::TERMINAL][..]).process::<OM>(input),
			Grammar::MaskedLinkText => tag(&[link::masked::TEXT_TERMINAL][..]).process::<OM>(input),
			Grammar::MaskedLinkLink => tag(&[link::masked::LINK_TERMINAL][..]).process::<OM>(input),
			Grammar::Code => tag(code::DELIMITER).process::<OM>(input),
			Grammar::CodeBlock => tag(code_block::DELIMITER).process::<OM>(input),
			Grammar::Timestamp => tag(timestamp::CLOSE_DELIMITER).process::<OM>(input),
			Grammar::CustomEmoji => tag(emoji::custom::CLOSE_DELIMITER).process::<OM>(input),
			Grammar::ColonDelimitedEmoji => tag(emoji::colon_delimited::DELIMITER).process::<OM>(input),
			Grammar::UserMention | Grammar::ChannelMention | Grammar::RoleMention | Grammar::CommandMention => tag(mention::CLOSE_DELIMITER).process::<OM>(input),
		}
		.trace_ok()
	}
}
