use std::{fmt::Debug, marker::PhantomData};

use nom::{
	branch::alt,
	character::{
		complete::{char, digit1, one_of},
		satisfy,
	},
	combinator::{map, map_opt, opt, recognize},
	error::ErrorKind,
	multi::{many0_count, many1_count},
	sequence::delimited,
	AsChar, Mode, Parser,
};
use tracing::Level;
use url::Url;

use crate::{
	context::Context,
	error::ParseError,
	grammar::{ByteHint, Grammar},
	node::Node,
	rule::RuleSet,
	span::{Span, Spanned, TraceOk, TraceParse, WithSpan},
	Input,
};

use super::{parse_and_validate_url, Link};

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
	rules: RuleSet,
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
						rules,
					)?,
					text: input.content,
				})
			}),
			map_opt(email(), move |input: Input<'data>| {
				Some(ParsedContact {
					url: parse_and_validate_url(&format!("mailto:{}", input.content), rules)?,
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
	type Output = Link<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "contact_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		if *self.context.hints.get(&Grammar::AutoLink) == ByteHint::Absent {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Alt)
			})));
		}
		nom::error::context(
			"link::contact",
			map(
				delimited(
					char('<'),
					verify_phone_email(self.context.allowed_rules).span::<S>(),
					char('>'),
				),
				|Spanned { value, span }| Link {
					text: Some(Spanned {
						value: vec![Spanned {
							value: Node::Text(value.text.into()),
							span: span.clone(),
						}],
						span,
					}),
					title: None,
					url: value.url,
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
) -> impl Parser<Input<'data>, Output = Link<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	ContactParser {
		context: context.with_grammar(Grammar::AutoLink),
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
	use crate::inline::link::Link;
	use crate::test_utils::handle_nom_err;
	use crate::{spanned_vec, text};

	#[test]
	fn phone_number_link() {
		let s = "<+1 (800) 588-2300>";
		let (rem, res) = contact::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("tel:+1-(800)-588-2300").unwrap(),
				text: Some(spanned_vec![text!("+1 (800) 588-2300")]),
				title: None,
			}
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
		let (rem, res) = contact::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link {
				url: Url::parse("mailto:tim@apple.com").unwrap(),
				text: Some(spanned_vec![text!("tim@apple.com")]),
				title: None,
			}
		);
	}
}
