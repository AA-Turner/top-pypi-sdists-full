use std::{fmt::Debug, marker::PhantomData};

use enumset::{enum_set, enum_set_difference, EnumSet};
use nom::{combinator::map, error::ErrorKind, sequence::pair, Mode, Parser};
use tracing::Level;

use crate::{
	context::Context,
	error::ParseError,
	grammar::ByteHint,
	rule::{Rule, RuleSet},
	span::Span,
	Input,
};

use super::{auto, verify_url, Grammar, Link, Normal};

mod link;
mod text;

pub const TEXT_OPENER: u8 = b'[';
pub const TEXT_TERMINAL: u8 = b']';
pub const LINK_TERMINAL: u8 = b')';
pub const LINK_OPENER: u8 = b'(';
pub const TEXT_LINK_DIVIDER: &[u8] = b"](";

// this is intentionally setup to exclude most rules by default
pub const DISABLED_MASKED_LINK_RULES: EnumSet<Rule> = {
	let allowed_rules =
		enum_set!(Rule::Bold | Rule::Code | Rule::Italic | Rule::Strikethrough | Rule::Underline);
	let all_rules = RuleSet::all();
	enum_set_difference!(all_rules, allowed_rules)
};

struct MaskedParser<'ctx, S, E> {
	context: &'ctx Context,
	span: PhantomData<S>,
	error: PhantomData<E>,
}

impl<S, E> Debug for MaskedParser<'_, S, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("MaskedParser")
			.field("context", &self.context)
			.field("error", &self.error)
			.finish()
	}
}

impl<'ctx, 'data, S, E> Parser<Input<'data>> for MaskedParser<'ctx, S, E>
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	type Output = Link<'data, S>;
	type Error = E;

	#[tracing::instrument(name = "masked_parser", level = Level::TRACE, fields(ok, output))]
	fn process<OM: nom::OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> nom::PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let bytes = input.as_bytes();
		if bytes.first() != Some(&TEXT_OPENER) {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Char)
			})));
		}

		if *self.context.hints.get(&Grammar::MaskedLinkText) == ByteHint::Absent {
			return Err(nom::Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input.clone(), ErrorKind::Alt)
			})));
		}

		map(
			pair(
				text::segment::<S, E>(self.context.clone()),
				link::segment::<E>(self.context),
			),
			|(text, (url, title))| {
				Link::Normal(Normal {
					text: Some(text),
					url,
					title,
				})
			},
		)
		.process::<OM>(input)
	}
}

/// Parse a masked link.
///
/// # Errors
/// If the content does not begin with a masked link.
#[must_use]
pub fn masked<'ctx, 'data, S, E>(
	context: &'ctx Context,
) -> impl Parser<Input<'data>, Output = Link<'data, S>, Error = E> + 'ctx
where
	S: Span,
	E: ParseError<'data> + 'ctx,
{
	MaskedParser {
		context,
		span: PhantomData,
		error: PhantomData,
	}
}
#[cfg(test)]
mod test {
	use nom::{Finish, Parser};
	use url::Url;

	use super::masked;
	use crate::context::Context;
	use crate::inline::link::{Link, Normal};
	use crate::node::Node;
	use crate::test_utils::handle_nom_err;
	use crate::{bold, italic, spanned_vec, text};

	#[test]
	fn simple_masked_link() {
		let s = r"[test](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("test")]),
				title: None,
			})
		);
	}

	#[test]
	fn inline_masked_link() {
		let s = r"[_foo_ **bar**](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![italic!("foo"), text!(" "), bold!("bar")]),
				title: None,
			})
		);
	}

	#[test]
	fn masked_link_with_new_line() {
		let s = "[foo\nbar](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo\nbar")]),
				title: None,
			})
		);
	}

	#[test]
	fn invalid_masked_url() {
		let s = r"[foo](foobar)";
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("unable to parse");
	}

	// TODO - we need to conditionally allow this. Webhooks are allowed to do this.
	#[test]
	fn no_emoji() {
		let s = r"[<:abcd:1234>](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("<:abcd:1234>")]),
				title: None,
			})
		);
	}

	#[test]
	fn masked_link_with_title() {
		let s = "[foo](https://wnelson.dev  \"Will Nelson's website\")";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![text!("foo")]),
				title: Some("Will Nelson's website".to_string()),
			})
		);
	}

	#[test]
	fn masked_autolink_with_title() {
		let s = "[foo](<https://wnelson.dev> \"Will Nelson's website\")";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("foo".into())]),
				title: Some("Will Nelson's website".to_string()),
			})
		);
	}

	#[test]
	fn masked_link_with_parens() {
		let s = "[Endemic](https://en.wikipedia.org/wiki/Endemic_(epidemiology))";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://en.wikipedia.org/wiki/Endemic_(epidemiology)").unwrap(),
				text: Some(spanned_vec![Node::Text("Endemic".into())]),
				title: None,
			})
		);
	}

	#[test]
	fn masked_link_with_link() {
		let s = r"[foo **h**ttp_s_://foo](https://wnelson.dev)";
		masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect_err("able to parse");
	}

	#[test]
	fn masked_link_with_matching_brackets() {
		let s = r"[[foo] bar](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("[foo] bar".into())]),
				title: None,
			})
		);
	}

	#[test]
	fn masked_link_with_complex_matching_brackets() {
		let s = r"[foo [bar_baz]](https://wnelson.dev)";
		let (rem, res) = masked::<(), _>(&Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");

		assert_eq!(rem, "");
		assert_eq!(
			res,
			Link::Normal(Normal {
				url: Url::parse("https://wnelson.dev").unwrap(),
				text: Some(spanned_vec![Node::Text("foo [bar_baz]".into())]),
				title: None,
			})
		);
	}
}
