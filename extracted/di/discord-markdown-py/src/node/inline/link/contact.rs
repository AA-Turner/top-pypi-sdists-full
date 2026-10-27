use std::{fmt::Debug, marker::PhantomData};

use nom::{
	AsChar, Parser,
	branch::alt,
	character::{
		complete::{char, digit1, one_of},
		satisfy,
	},
	combinator::{map, map_opt, opt, recognize},
	multi::{many0_count, many1_count},
};
use tracing::Level;
use url::Url;

use crate::{
	Input,
	context::Context,
	error::ParseError,
	lossless::TokenKind,
	node::Element,
	scope::Scope,
	span::{Span, Spanned, Syntax, TraceOk, TraceParse, WithSpan, WithToken, attach},
};

use super::{Link, parse_and_validate_url};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParsedContact<'data> {
	pub url: Url,
	pub text: &'data str,
}

fn is_valid_email_char(ch: char) -> bool {
	!ch.is_ascii_whitespace() && ch != '<' && ch != '>' && ch != '@'
}

fn phone_group<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	alt((
		recognize(satisfy(AsChar::is_dec_digit)),
		recognize((char('('), digit1, char(')'))),
	))
}

fn phone<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	recognize((
		char('+'),
		phone_group(),
		many0_count((opt(one_of("- /.")), phone_group())),
	))
}

fn email<'data, E>() -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	recognize((
		many1_count(satisfy(is_valid_email_char)),
		char('@'),
		many1_count(satisfy(is_valid_email_char)),
	))
}

/// Convert a Markdown-style email address or phone number to a URL
#[must_use]
fn verify_phone_email<'data, E>(
	dev_links: bool,
) -> impl Parser<Input<'data>, Output = ParsedContact<'data>, Error = E>
where
	E: ParseError<'data>,
{
	nom::error::context(
		"link::verify_phone_email",
		alt((
			map_opt(phone(), move |input: Input<'data>| {
				Some(ParsedContact {
					url: parse_and_validate_url(
						&format!("tel:{}", input.content.replace([' ', '/'], "-")),
						dev_links,
					)?,
					text: input.content,
				})
			}),
			map_opt(email(), move |input: Input<'data>| {
				Some(ParsedContact {
					url: parse_and_validate_url(&format!("mailto:{}", input.content), dev_links)?,
					text: input.content,
				})
			}),
		)),
	)
}

pub const DELIMITER: &str = ">";

struct ContactParser<S, E> {
	context: Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for ContactParser<S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("ContactParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, S, E> Parser<Input<'data>> for ContactParser<S, E>
where
	S: Span,
	E: ParseError<'data>,
{
	type Output = (Link<S, Element<'data, S>>, S::Syntax);
	type Error = E;

	#[tracing::instrument(name = "contact_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		nom::error::context(
			"link::contact",
			map(
				(
					char('<').token::<S>(TokenKind::LinkOpen),
					// the text records its token; the sequence holding it spans the same, bare
					verify_phone_email(self.context.dev_links)
						.with_token::<S>(TokenKind::Text)
						.span::<S>()
						.map(attach)
						.span::<S>(),
					char('>').token::<S>(TokenKind::LinkClose),
				),
				|(open, Spanned { value: text, span }, close)| {
					let url = text.value.url;
					let text = Spanned {
						value: Element::Text(text.value.text.into()),
						span: text.span,
					};
					let link = Link {
						text: Some(Spanned {
							value: vec![text],
							span,
						}),
						title: None,
						url,
					};
					(link, open.join(close))
				},
			),
		)
		.trace_parse()
		.process::<OM>(input)
		.trace_ok()
	}
}

/// Parse email/phone-number auto-link content.
///
/// # Errors
/// If the content does not begin with an auto-linked email/phone number.
#[must_use]
pub fn contact<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = (Link<S, Element<'data, S>>, S::Syntax), Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	ContactParser {
		context: context.with_scope(Scope::AutoLink),
		span: PhantomData,
		error: PhantomData,
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};
	use url::Url;

	use super::contact;
	use crate::context::Context;
	use crate::lossless::LinkKind;
	use crate::node::inline::link::Link;
	use crate::node::{Element, Inline};
	use crate::test_utils::{handle_nom_err, resolved_inline};
	use crate::{spanned_vec, text};

	#[test]
	fn phone_number_link() {
		let s = "<+1 (800) 588-2300>";
		let (rem, (res, ())) = contact::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inline(Element::Link(LinkKind::Contact, res)),
			Inline::Link(Link {
				url: Url::parse("tel:+1-(800)-588-2300").unwrap(),
				text: Some(spanned_vec![text!("+1 (800) 588-2300")]),
				title: None,
			})
		);
	}

	#[test]
	fn phone_number_overlong() {
		// This should fail, and not take an exponential amount of time to do so
		let s =
			"<+1(111)1111111-11111111111111.1111111/11111111 11111111111111111111111111111111a>";
		contact::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn email_address_link() {
		let s = "<tim@apple.com>";
		let (rem, (res, ())) = contact::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			resolved_inline(Element::Link(LinkKind::Contact, res)),
			Inline::Link(Link {
				url: Url::parse("mailto:tim@apple.com").unwrap(),
				text: Some(spanned_vec![text!("tim@apple.com")]),
				title: None,
			})
		);
	}
}
