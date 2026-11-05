use url::Url;

use crate::{
	Input,
	context::Context,
	error::{Fail, PResult},
	lossless::TokenKind,
	node::Element,
	span::{Span, Spanned, Syntax, Trace},
};

use super::{Link, ParsedLink, parse_and_validate_url};

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParsedContact<'data> {
	pub url: Url,
	pub text: &'data str,
}

fn is_valid_email_char(ch: char) -> bool {
	!ch.is_ascii_whitespace() && ch != '<' && ch != '>' && ch != '@'
}

/// A digit, or digits in parentheses.
fn phone_group(input: &mut Input) -> PResult<()> {
	if input.satisfy(|ch| ch.is_ascii_digit()).is_ok() {
		return Ok(());
	}
	input.char('(')?;
	input.take_while1(|ch| ch.is_ascii_digit())?;
	input.char(')')?;
	Ok(())
}

fn phone(input: &mut Input) -> PResult<()> {
	input.char('+')?;
	phone_group(input)?;
	while input
		.attempt(|input| {
			let _ = input.satisfy(|ch| matches!(ch, '-' | ' ' | '/' | '.'));
			phone_group(input)
		})?
		.is_some()
	{}
	Ok(())
}

fn email(input: &mut Input) -> PResult<()> {
	input.take_while1(is_valid_email_char)?;
	input.char('@')?;
	input.take_while1(is_valid_email_char)?;
	Ok(())
}

/// Convert a Markdown-style email address or phone number to a URL
fn verify_phone_email<'data>(
	input: &mut Input<'data>,
	dev_links: bool,
) -> PResult<ParsedContact<'data>> {
	let phone = input.attempt(|input| {
		let text = input.recognize(phone)?;
		let url =
			parse_and_validate_url(&format!("tel:{}", text.replace([' ', '/'], "-")), dev_links)
				.ok_or(Fail::NoMatch)?;
		Ok(ParsedContact { url, text })
	})?;
	if let Some(phone) = phone {
		return Ok(phone);
	}

	let text = input.recognize(email)?;
	let url = parse_and_validate_url(&format!("mailto:{text}"), dev_links).ok_or(Fail::NoMatch)?;
	Ok(ParsedContact { url, text })
}

pub const DELIMITER: &str = ">";

/// Parse email/phone-number auto-link content.
///
/// # Errors
/// If the content does not begin with an auto-linked email/phone number.
#[tracing::instrument(name = "contact_parser", level = "trace", skip_all, fields(ok, output))]
pub fn contact<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<ParsedLink<'data, S>> {
	let open = input.token::<S, _>(TokenKind::LinkOpen, |input| input.char('<'))?;
	// the text records its token; the sequence holding it spans the same, bare
	let start = input.start;
	let contact = input.spanned_with_syntax::<S, _>(|input| {
		input.with_token::<S, _>(TokenKind::Text, |input| {
			verify_phone_email(input, context.dev_links)
		})
	})?;
	let span = input.span(start);
	let close = input.token::<S, _>(TokenKind::LinkClose, |input| input.char('>'))?;

	let text = Spanned {
		value: Element::Text(contact.value.text.into()),
		span: contact.span,
	};
	let link = Link {
		text: Some(Spanned {
			value: vec![text],
			span,
		}),
		title: None,
		url: contact.value.url,
	};
	Ok((link, open.join(close))).trace()
}

#[cfg(test)]
mod test {
	use url::Url;

	use super::contact;
	use crate::context::Context;
	use crate::lossless::LinkKind;
	use crate::node::inline::link::Link;
	use crate::node::{Element, Inline};
	use crate::test_utils::{resolved_inline, run};
	use crate::{spanned_vec, text};

	#[test]
	fn phone_number_link() {
		let s = "<+1 (800) 588-2300>";
		let (rem, (res, ())) =
			run(s, |input| contact::<()>(input, &Context::default())).expect("unable to parse");

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
		run(s, |input| contact::<()>(input, &Context::default())).expect_err("able to parse");
	}

	#[test]
	fn email_address_link() {
		let s = "<tim@apple.com>";
		let (rem, (res, ())) =
			run(s, |input| contact::<()>(input, &Context::default())).expect("unable to parse");

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
