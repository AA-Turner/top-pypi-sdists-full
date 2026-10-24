use std::{fmt::Debug, marker::PhantomData};

use nom::{OutputMode, PResult, Parser, bytes::tag, combinator::fail};
use tracing::Level;

use crate::{
	Input,
	error::ParseError,
	node::inline::{
		code, code_block, emoji,
		link::{self, detection},
		mention, timestamp,
	},
	span::TraceOk,
};

use super::Syntax;

pub struct StartSequence<E>(pub Syntax, pub PhantomData<E>);

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

	#[tracing::instrument(name = "syntax_start_sequence", level = Level::TRACE, fields(ok))]
	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		match self.0 {
			Syntax::CustomEmoji => tag(emoji::custom::OPEN_DELIMITER).process::<OM>(input),
			Syntax::ColonEmoji => tag(emoji::colon_delimited::DELIMITER).process::<OM>(input),
			Syntax::MaskedLink => tag(&[link::masked::TEXT_OPENER][..]).process::<OM>(input),
			Syntax::DetectedLink => detection::start_sequence().process::<OM>(input),
			Syntax::AutoLink | Syntax::ContactLink => {
				tag(link::auto::OPEN_DELIMITER).process::<OM>(input)
			}
			Syntax::UserMention => tag(mention::USER_MENTION_OPEN_DELIMITER).process::<OM>(input),
			Syntax::ChannelMention => {
				tag(mention::CHANNEL_MENTION_OPEN_DELIMITER).process::<OM>(input)
			}
			Syntax::RoleMention => tag(mention::ROLE_MENTION_OPEN_DELIMITER).process::<OM>(input),
			Syntax::GameMention => tag(mention::GAME_MENTION_OPEN_DELIMITER).process::<OM>(input),
			Syntax::CommandMention => tag(mention::command::OPEN_DELIMITER).process::<OM>(input),
			Syntax::EveryoneMention => tag(mention::EVERYONE).process::<OM>(input),
			Syntax::HereMention => tag(mention::HERE).process::<OM>(input),
			Syntax::StaticMention => tag(mention::r#static::PREFIX).process::<OM>(input),
			Syntax::Timestamp => tag(timestamp::OPEN_DELIMITER).process::<OM>(input),
			Syntax::CodeBlock => tag(code_block::DELIMITER).process::<OM>(input),
			Syntax::Code => tag(code::SINGLE_DELIMITER).process::<OM>(input),
			Syntax::DoubleCode => tag(code::DOUBLE_DELIMITER).process::<OM>(input),
			Syntax::UnicodeEmoji
			| Syntax::Bold
			| Syntax::AsteriskItalic
			| Syntax::UnderscoreItalic
			| Syntax::Underline
			| Syntax::Strikethrough
			| Syntax::Spoiler
			| Syntax::Heading
			| Syntax::List
			| Syntax::Quote
			| Syntax::MultilineQuote
			| Syntax::Small => fail().process::<OM>(input),
		}
		.trace_ok()
	}
}
