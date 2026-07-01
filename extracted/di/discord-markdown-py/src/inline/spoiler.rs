use enumset::enum_set;
use nom::{bytes::complete::tag, sequence::delimited, Parser};

use crate::{
	context::Context,
	error::ParseError,
	grammar::Grammar,
	inline,
	node::SpannedNodes,
	rule::{Rule, RuleSet},
	span::Span,
	unparse::Unparse,
	Input,
};

pub const DELIMITER: &str = "||";
pub const DISABLED_RULES: RuleSet = enum_set!(Rule::Spoiler);

/// Unparse spoiler content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

/// Parse a spoiler.
///
/// # Errors
/// If the content does not begin with a spoiler.
#[must_use]
pub fn spoiler<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	nom::error::context(
		"spoiler",
		delimited(
			tag(DELIMITER),
			inline::inline(context.with_grammar(Grammar::Spoiler)),
			tag(DELIMITER),
		),
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{context::Context, spanned_vec, test_utils::handle_nom_err, text};

	use super::spoiler;

	#[test]
	fn simple_spoiler() {
		let s = r"||foo bar||";
		let (rem, res) = spoiler::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo bar")]);
	}

	#[test]
	fn escaped_spoiler() {
		let s = r"||foo\|\|bar||";
		let (rem, res) = spoiler::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo||bar")]);
	}

	#[test]
	fn allow_unescaped_single_pipes() {
		let s = r"||foo|bar|banana||";
		let (rem, res) = spoiler::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "", "unexpected input remaining");
		assert_eq!(res, spanned_vec![text!("foo|bar|banana")]);
	}
}
