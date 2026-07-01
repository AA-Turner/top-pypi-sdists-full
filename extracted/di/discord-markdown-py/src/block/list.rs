use nom::branch::alt;
use nom::character::complete::{one_of, space1, u32};
use nom::combinator::{peek, value};
use nom::multi::fold_many0;
use nom::sequence::{pair, terminated};
use nom::{
	character::complete::char,
	combinator::map,
	multi::{fold_many_m_n, many0_count},
	IResult, Parser,
};

use item::Item;

use crate::context::Context;
use crate::error::ParseError;
use crate::span::{Span, Spanned, WithSpan};
use crate::unparse::Unparse;
use crate::Input;

/// List item parsing.
pub mod item;

/// The character used for indentation.
pub const INDENT_CHAR: char = ' ';

/// Characters that denote the beginning of an unordered list.
pub const UNORDERED_CONTROL_CHARS: &str = "-*";

/// The maximum number of spaces beyond the current indent level within which to consider an item
/// belonging to the parent.
///
/// In the following example, "bar" is still considered nested inside "foo" despite being indented
/// more than the current indent level since it is not additionally indented more than this value.
/// ```md
/// 1. foo
///    bar
/// ```
///
/// In the following example, "bar" is _not_ nested inside "foo" because it is indented further than
/// the current indent level and this value.
/// ```md
/// 1. foo
///      bar
/// ```
pub const MAX_INDENT: usize = 2;

/// The type of the list item. [`Type::Ordered`] corresponds to `1. [text]` and [`Type::Unordered`]
/// corresponds to either `- [text]` or `* [text]`. The value in ordered items is directly parsed
/// from the content and no assertions are made about its validity (aside that it is a number).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum Type {
	Ordered(u32),
	Unordered,
}

/// A list element. Each item describes its own type.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct List<'data, S: Span> {
	#[cfg_attr(feature = "serde", serde(rename = "type", flatten))]
	pub kind: Type,
	pub items: Spanned<Vec<Item<'data, S>>, S>,
}

impl<S> Unparse for List<'_, S>
where
	S: Span,
{
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		// TODO: preserve indentation for nested lists
		match self.kind {
			Type::Ordered(number) => write!(f, "{}. {}", number, self.items.unparse()),
			// TODO: preserve the control character
			Type::Unordered => write!(f, "* {}", self.items.unparse()),
		}
	}
}

/// Parse an unknown amount of indentation, including 0, returning the amount of indentation
/// parsed. [`INDENT_CHAR`] is used to detect indentation. This does not consume the parsed
/// indentation.
///
/// # Errors
/// Never.
pub fn peek_indent<'data, E>(data: Input<'data>) -> IResult<Input<'data>, usize, E>
where
	E: ParseError<'data>,
{
	peek(many0_count(char(INDENT_CHAR))).parse_complete(data)
}

/// Parse either [`unordered_type`] or [`ordered_type`].
///
/// # Errors
/// If the content does not begin with either type.
pub fn unknown_type<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Type, E>
where
	E: ParseError<'data>,
{
	alt((unordered_type, ordered_type)).parse_complete(data)
}

/// Parse the type of an ordered list, including its value.
///
/// # Errors
/// If the content does not begin with an ordered list signature.
pub fn ordered_type<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Type, E>
where
	E: ParseError<'data>,
{
	map(terminated(u32, pair(char('.'), space1)), Type::Ordered).parse_complete(data)
}

/// Parse the type of an unordered list, as determined by any of [`UNORDERED_CONTROL_CHARS`].
///
/// # Errors
/// If the content does not begin with an unordered list signature.
pub fn unordered_type<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Type, E>
where
	E: ParseError<'data>,
{
	value(
		Type::Unordered,
		terminated(one_of(UNORDERED_CONTROL_CHARS), space1),
	)
	.parse_complete(data)
}

/// Parse an amount of indentation in the range `min_indent..=min_indent + `[`MAX_INDENT`],
/// returning the amount of indentation parsed. [`INDENT_CHAR`] is used to detect indentation.
#[must_use]
pub fn indent<'data, E>(min_indent: usize) -> impl Parser<Input<'data>, Output = usize, Error = E>
where
	E: ParseError<'data>,
{
	let max_indent = min_indent + MAX_INDENT;

	fold_many_m_n(
		min_indent,
		max_indent,
		char(INDENT_CHAR),
		|| 0,
		|acc, _| acc + 1,
	)
}

/// Parse a list with a specified amount of indentation, parsed by [`indent`].
#[must_use]
pub fn indented<'data, S, E>(
	context: Context,
	amount: usize,
) -> impl Parser<Input<'data>, Output = List<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	move |data| {
		let (data, (kind, first_item)) =
			item::item(context.clone(), amount, unknown_type).parse_complete(data)?;

		let parse_type = move |data| match kind {
			Type::Unordered => unordered_type(data),
			Type::Ordered(_) => ordered_type(data),
		};

		map(
			fold_many0(
				item::item(context.clone(), amount, parse_type),
				move || vec![first_item.clone()],
				|mut acc, (_, item)| {
					acc.push(item);
					acc
				},
			)
			.span(),
			move |items| List { kind, items },
		)
		.parse_complete(data)
	}
}

/// Parse a list.
///
/// Detects the appropriate amount of indentation with which to start. Use [`indented`] to parse
/// with a specific amount of indentation.
#[must_use]
pub fn list<'data, S, E>(
	context: Context,
) -> impl Parser<Input<'data>, Output = List<'data, S>, Error = E>
where
	S: Span,
	E: ParseError<'data>,
{
	move |data| {
		let (data, indent) = peek_indent(data)?;
		indented(context.clone(), indent).parse_complete(data)
	}
}

#[cfg(test)]
mod test {
	use nom::{Finish, Parser};
	use pretty_assertions::assert_eq;

	use crate::{
		list, list_item, list_items, paragraph,
		test_utils::handle_nom_err,
		{block::list::Type, context::Context},
	};

	use super::{list, List};

	#[test]
	fn unordered_item() {
		let s = "- foo";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"))
			}
		);
	}

	#[test]
	fn multiple_unordered_items() {
		let s = "- foo\n- bar";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"), list_item!("bar"))
			}
		);
	}

	#[test]
	fn sub_items() {
		let s = "- foo\n  - bar";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items![list_item!(paragraph!("foo"), list!(-[list_item!("bar")]))]
			}
		);
	}

	#[test]
	fn sub_items_with_content() {
		let s = "- foo\n  - bar\n  baz\n  - box";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items![list_item!(
					paragraph!("foo"),
					list!(-[list_item!("bar")]),
					paragraph!("baz"),
					list!(-[list_item!("box")])
				)],
			}
		);
	}

	#[test]
	fn two_spaces_required_for_nested_level() {
		let s = "- foo\n - bar\n  - baz";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items![
					list_item!("foo"),
					list_item![paragraph!("bar"), list!(-[list_item!("baz")])]
				],
			}
		);
	}

	#[test]
	fn ordered_list() {
		let s = "1. foo\n2. bar";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Ordered(1),
				items: list_items!(list_item!("foo"), list_item!("bar"))
			}
		);
	}

	#[test]
	fn dedented() {
		let s = "- foo\n  - bar\n- baz";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items![
					list_item![paragraph!("foo"), list!(-[list_item!("bar")])],
					list_item!("baz")
				],
			}
		);
	}

	#[test]
	fn indent_one() {
		let s = " - foo\n - bar\n - baz";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"), list_item!("bar"), list_item!("baz")),
			}
		);
	}

	/// This test is to validate that if someone has a list that has the root elements indented
	/// and the backend strips the very first leading space of the message, the list will
	/// still correctly render the overall list with all the root elements on the same line
	#[test]
	fn indent_one_but_not_first() {
		let s = "- foo\n - bar\n - baz";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"), list_item!("bar"), list_item!("baz")),
			}
		);
	}

	#[test]
	fn indent_one_but_not_first_and_with_content() {
		// All the items were originally aligned such that all bullets had 1 space of leading
		// spacing before the bullet: (' - ') and as such their trailing content had 3 spaces
		// of leading space to align with the first line of the bullet:
		//
		// | - foo
		// |   test
		// | - bar
		// |   hi
		//
		// However, often the first list item will have its leading spaces removed before the
		// bullet because of backend message trimming. That results in:
		// |- foo
		// |   test
		// | - bar
		// |   hi
		//
		// This test ensures that even though the trailing content for the "foo" bullet has an
		// undesirable leading space ("   test") instead of an aligned leading space ("  test")
		// that leading space will not appear in the AST. The trailing node will be "test", not " test"
		let s = "- foo\n   test\n - bar\n   hi\n - baz\n   yo";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Unordered,
				items: list_items!(
					list_item![paragraph!("foo"), paragraph!("test")],
					list_item![paragraph!("bar"), paragraph!("hi")],
					list_item![paragraph!("baz"), paragraph!("yo")]
				),
			}
		);
	}
}
