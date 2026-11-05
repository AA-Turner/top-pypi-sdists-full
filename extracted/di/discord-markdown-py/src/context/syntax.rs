use std::borrow::Cow;

use crate::{
	Input,
	error::{Fail, PResult},
	lossless::{LinkKind, QuoteKind, TokenKind},
	node::{
		Element,
		block::{heading, list, quote, small},
		inline::{
			code, code_block,
			emoji::{self, Emoji},
			link::{self, masked::Masked},
			mention::{self, Mention},
			timestamp,
		},
	},
	span::{Span, Trace},
	syntax::Syntax,
};

use super::Context;

/// An element written as one piece, like a mention: its whole input is one [`TokenKind::Atom`].
fn atom<'data, S: Span, T>(
	input: &mut Input<'data>,
	parser: impl FnOnce(&mut Input<'data>) -> PResult<T>,
	element: impl FnOnce(T) -> Element<'data, S>,
) -> PResult<(Element<'data, S>, S::Syntax)> {
	let (value, syntax) = input.with_token::<S, _>(TokenKind::Atom, parser)?;
	Ok((element(value), syntax))
}

/// An element whose syntax its own parsers record, in the spans inside it.
fn block<S: Span>(element: Element<'_, S>) -> (Element<'_, S>, S::Syntax) {
	(element, S::Syntax::default())
}

/// Parse `syntax` in `context`: the element, with the syntax it was written with outside its
/// children.
#[tracing::instrument(
	name = "contextual_syntax",
	level = "trace",
	skip(context, input),
	fields(ok, output)
)]
pub fn parse<'data, S: Span>(
	syntax: Syntax,
	context: &Context,
	input: &mut Input<'data>,
) -> PResult<(Element<'data, S>, S::Syntax)> {
	match syntax {
		Syntax::CustomEmoji => atom(input, emoji::custom::parse, |custom| {
			Element::Emoji(Emoji::Custom(custom))
		}),
		Syntax::ColonEmoji => atom(input, emoji::colon_delimited::emoji, |emoji| {
			Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji)))
		}),
		Syntax::UnicodeEmoji => atom(input, emoji::unicode::emoji, |emoji| {
			Element::Emoji(Emoji::Unicode(Cow::Borrowed(emoji)))
		}),
		Syntax::MaskedLink => link::masked::masked(input, context).map(|masked| match masked {
			Masked::Link((link, syntax)) => (Element::Link(LinkKind::Masked, link), syntax),
			Masked::Spoof(source, syntax) => (Element::Text(Cow::Borrowed(source)), syntax),
		}),
		Syntax::DetectedLink => link::detection::detection(input, context)
			.map(|(link, syntax)| (Element::Link(LinkKind::Detected, link), syntax)),
		Syntax::AutoLink => link::auto::link(input, context)
			.map(|(link, syntax)| (Element::Link(LinkKind::Auto, link), syntax)),
		Syntax::ContactLink => link::contact::contact(input, context)
			.map(|(link, syntax)| (Element::Link(LinkKind::Contact, link), syntax)),
		Syntax::UserMention => atom(input, mention::user, |id| {
			Element::Mention(Mention::User(id))
		}),
		Syntax::ChannelMention => atom(input, mention::channel, |id| {
			Element::Mention(Mention::Channel(id))
		}),
		Syntax::RoleMention => atom(input, mention::role, |id| {
			Element::Mention(Mention::Role(id))
		}),
		Syntax::GameMention => atom(input, mention::game, |id| {
			Element::Mention(Mention::Game(id))
		}),
		Syntax::CommandMention => atom(input, mention::command::command, |command| {
			Element::Mention(Mention::Command(command))
		}),
		Syntax::EveryoneMention => atom(input, mention::everyone, |()| {
			Element::Mention(Mention::Everyone)
		}),
		Syntax::HereMention => atom(input, mention::here, |()| Element::Mention(Mention::Here)),
		Syntax::StaticMention => atom(input, mention::r#static::parse, |mention| {
			Element::Mention(Mention::Static(mention))
		}),
		Syntax::Timestamp => atom(input, timestamp::timestamp, Element::Timestamp),
		Syntax::CodeBlock => code_block::code_block::<S>(input)
			.map(|(code_block, syntax)| (Element::CodeBlock(code_block), syntax)),
		Syntax::Code => {
			code::single::<S>(input).map(|(code, syntax)| (Element::Code(code.into()), syntax))
		}
		Syntax::DoubleCode => {
			code::double::<S>(input).map(|(code, syntax)| (Element::Code(code.into()), syntax))
		}
		Syntax::Heading => {
			heading::heading(input, context).map(|heading| block(Element::Heading(heading)))
		}
		Syntax::List => list::list(input, context).map(|list| block(Element::List(list))),
		Syntax::Quote => quote::quote_line(input, context)
			.map(|content| block(Element::Quote(QuoteKind::Line, content))),
		Syntax::MultilineQuote => quote::quote_rest(input, context)
			.map(|content| block(Element::Quote(QuoteKind::Rest, content))),
		Syntax::Small => small::small(input, context).map(|small| block(Element::Small(small))),
		// recorded as delimiters and resolved after the parse; see `crate::range`
		Syntax::Bold
		| Syntax::AsteriskItalic
		| Syntax::UnderscoreItalic
		| Syntax::Underline
		| Syntax::Strikethrough
		| Syntax::Spoiler => Err(Fail::NoMatch),
	}
	.trace()
}

#[cfg(test)]
mod test {
	use super::parse;
	use crate::{
		Input,
		context::Context,
		syntax::{Syntax, SyntaxSet},
	};

	/// The first-byte filter in `Context::first_syntax` never skips a syntax that would parse.
	#[test]
	fn first_byte_filter_keeps_every_inline_syntax_that_parses() {
		let examples = [
			(Syntax::CustomEmoji, "<:name:123>"),
			(Syntax::ColonEmoji, ":smile:"),
			(Syntax::UnicodeEmoji, "💪"),
			(Syntax::MaskedLink, "[a](https://example.com)"),
			(Syntax::DetectedLink, "https://example.com"),
			(Syntax::AutoLink, "<https://example.com>"),
			(Syntax::ContactLink, "<tim@apple.com>"),
			(Syntax::UserMention, "<@1>"),
			(Syntax::ChannelMention, "<#1>"),
			(Syntax::RoleMention, "<@&1>"),
			(Syntax::GameMention, "<@$1>"),
			(Syntax::CommandMention, "</name:1>"),
			(Syntax::EveryoneMention, "@everyone"),
			(Syntax::HereMention, "@here"),
			(Syntax::StaticMention, "<id:home>"),
			(Syntax::Timestamp, "<t:1>"),
			(Syntax::CodeBlock, "```a```"),
			(Syntax::Code, "`a`"),
			(Syntax::DoubleCode, "``a``"),
		];
		assert_eq!(
			examples
				.iter()
				.map(|&(syntax, _)| syntax)
				.collect::<SyntaxSet>(),
			Syntax::INLINE
		);

		for (syntax, s) in examples {
			let mut input = Input::from(s);
			assert!(
				parse::<()>(syntax, &Context::default(), &mut input).is_ok(),
				"{syntax:?} does not parse {s:?}"
			);
			assert!(
				Syntax::may_parse_at(s.as_bytes()[0]).contains(syntax),
				"{syntax:?} is filtered out of {s:?}"
			);
		}
	}
}
