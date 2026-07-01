use nom::{
	branch::alt,
	bytes::complete::tag,
	character::complete::{char, space1},
	combinator::eof,
	multi::many1,
	sequence::preceded,
	Parser,
};

use crate::{
	context::Context, error::ParseError, grammar::Grammar, node::SpannedNodes, span::Span,
	unparse::Unparse, util::take_line, Input,
};

use super::block;

pub const PREFIX: char = '>';

/// Unparse quote content back to markdown.
///
/// # Errors
/// If formatting fails
pub fn unparse<S: Span>(
	content: &SpannedNodes<S>,
	f: &mut std::fmt::Formatter,
) -> std::fmt::Result {
	// Quotes need special handling - prefix each line with "> "
	let content_str = content.unparse().to_string();
	let lines: Vec<&str> = content_str.lines().collect();
	for (i, line) in lines.iter().enumerate() {
		if i > 0 {
			f.write_str("\n")?;
		}
		write!(f, "{PREFIX} {line}")?;
	}
	Ok(())
}

/// Parse a quote block.
///
/// # Errors
/// If the data does not begin with quote content.
pub fn quote<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = SpannedNodes<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	many1(alt((
		preceded((char(PREFIX), space1), take_line),
		preceded(char(PREFIX), alt((tag("\n"), eof))),
	)))
	.map(|lines| lines.into_iter().collect::<Input>())
	.and_then(block(context.with_grammar(Grammar::Quote)))
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};

	use crate::{
		bold, italic, paragraph, spanned_vec,
		test_utils::handle_nom_err,
		text, underline,
		{context::Context, node::Node},
	};

	use super::quote;

	#[test]
	fn basic_quote() {
		let s = "> foo";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn quote_with_new_line() {
		let s = "> foo\nbar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "bar");
		assert_eq!(res, spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn multi_line_quote() {
		let s = "> foo\n> bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec!(paragraph!("foo"), paragraph!("bar")));
	}

	#[test]
	fn multi_line_quote_with_empty() {
		let s = "> foo\n>\n> bar";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec!(paragraph!("foo"), Node::Empty, paragraph!("bar"))
		);
	}

	#[test]
	fn quote_at_end() {
		let s = "> foo\n>";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, spanned_vec!(paragraph!("foo")));
	}

	#[test]
	fn quote_with_styling() {
		let s = "> **foo _bob_**\n> cat __a kitty cat__";
		let (rem, res) = quote::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			spanned_vec!(
				paragraph!(bold!(text!("foo "), italic!("bob"))),
				paragraph!(text!("cat "), underline!("a kitty cat"))
			)
		);
	}
}
