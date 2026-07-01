use nom::bytes::complete::tag;
use nom::sequence::delimited;
use nom::Parser;

use crate::context::Context;
use crate::error::ParseError;
use crate::node::SpannedNodes;
use crate::span::Span;
use crate::unparse::Unparse;
use crate::{inline, Input};

use super::Grammar;

pub const DELIMITER: &str = "~~";

/// Unparse strikethrough content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	write!(f, "{}{}{}", DELIMITER, content.unparse(), DELIMITER)
}

/// Parse a strikethrough.
///
/// # Errors
/// If the content does not begin with a strikethrough.
#[must_use]
pub fn strikethrough<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	delimited(
		tag(DELIMITER),
		inline::inline(context.with_grammar(Grammar::Strikethrough)),
		tag(DELIMITER),
	)
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use super::strikethrough;
	use crate::context::Context;
	use crate::node::Node;
	use crate::spanned_vec;
	use crate::test_utils::handle_nom_err;

	#[test]
	fn simple_strikethrough() {
		let s = r"~~foo~~";
		let (rem, res) = strikethrough::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![Node::Text(r"foo".into())]);
	}

	#[test]
	fn escaped_strikethrough() {
		let s = r"~~foo\~\~bar\~\~baz~~";
		let (rem, res) = strikethrough::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec![Node::Text("foo~~bar~~baz".into())]);
	}
}
