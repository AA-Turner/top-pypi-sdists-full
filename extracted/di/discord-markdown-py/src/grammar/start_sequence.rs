use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	bytes::tag,
	character::complete::line_ending,
	combinator::{eof, fail},
	OutputMode, PResult, Parser,
};
use tracing::Level;

use crate::{
	error::ParseError,
	inline::{
		bold, code, code_block, emoji, italic,
		link::{self, detection::valid_schemes},
		mention, spoiler, strikethrough, timestamp, underline,
	},
	span::TraceOk,
	Input,
};

use super::Grammar;

pub struct StartSequence<E>(pub Grammar, pub PhantomData<E>);

impl<E> Debug for StartSequence<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_tuple("StartSequence")
			.field(&self.0)
			.field(&self.1)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for StartSequence<E>
where
	E: ParseError<'data>,
{
	type Output = Input<'data>;
	type Error = E;

	#[tracing::instrument(name = "grammar_start_sequence", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Grammar::None => fail().process::<OM>(input),
			Grammar::InlineBlock | Grammar::Block | Grammar::Quote => {
				alt((line_ending, eof)).process::<OM>(input)
			}
			Grammar::Bold => tag(bold::DELIMITER).process::<OM>(input),
			Grammar::UnderscoreItalic => tag(italic::UNDERSCORE_DELIMITER).process::<OM>(input),
			Grammar::AsteriskItalic => tag(italic::ASTERISK_DELIMITER).process::<OM>(input),
			Grammar::Spoiler => tag(spoiler::DELIMITER).process::<OM>(input),
			Grammar::Strikethrough => tag(strikethrough::DELIMITER).process::<OM>(input),
			Grammar::Underline => tag(underline::DELIMITER).process::<OM>(input),
			Grammar::AutoLink => tag(&[link::auto::TERMINAL][..]).process::<OM>(input),
			Grammar::MaskedLinkText => tag(&[link::masked::TEXT_OPENER][..]).process::<OM>(input),
			Grammar::MaskedLinkLink => tag(&[link::masked::LINK_OPENER][..]).process::<OM>(input),
			Grammar::Code => tag(code::DELIMITER).process::<OM>(input),
			Grammar::CodeBlock => tag(code_block::DELIMITER).process::<OM>(input),
			Grammar::Timestamp => tag(timestamp::OPEN_DELIMITER).process::<OM>(input),
			Grammar::CustomEmoji => tag(emoji::custom::OPEN_DELIMITER).process::<OM>(input),
			Grammar::ColonDelimitedEmoji => {
				tag(emoji::colon_delimited::DELIMITER).process::<OM>(input)
			}
			Grammar::LinkDetection => valid_schemes().process::<OM>(input),
			Grammar::EveryoneMention => tag(mention::EVERYONE).process::<OM>(input),
			Grammar::HereMention => tag(mention::HERE).process::<OM>(input),
			Grammar::UserMention => tag(mention::USER_MENTION_OPEN_DELIMITER).process::<OM>(input),
			Grammar::ChannelMention => {
				tag(mention::CHANNEL_MENTION_OPEN_DELIMITER).process::<OM>(input)
			}
			Grammar::RoleMention => tag(mention::ROLE_MENTION_OPEN_DELIMITER).process::<OM>(input),
			Grammar::CommandMention => tag(mention::command::OPEN_DELIMITER).process::<OM>(input),
		}
		.trace_ok()
	}
}
