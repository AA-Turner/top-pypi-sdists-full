use std::num::NonZero;

use nom::branch::alt;
use nom::character::complete::{one_of, satisfy, space1};
use nom::combinator::{fail, peek, value};
use nom::error::context as with_context;
use nom::multi::{fold, fold_many0};
use nom::sequence::{pair, preceded, terminated};
use nom::{
	IResult, Parser,
	character::complete::char,
	combinator::map,
	multi::{fold_many_m_n, many0_count},
};

use item::Item;

use crate::Input;
use crate::context::Context;
use crate::error::ParseError;
use crate::span::{Span, Spanned, WithSpan};
use crate::unparse::Unparse;

/// List item parsing.
pub mod item;

/// The character used for indentation.
pub const INDENT_CHAR: char = ' ';

/// Characters that denote the beginning of an unordered list.
pub const UNORDERED_CONTROL_CHARS: &str = "-*";

/// The maximum depth allowable for lists. Any lists below this depth will not parse as lists.
///
/// See [`Context::list_depth`] for details on how this is used in the parser.
///
/// Depth is 1-indexed: an unnested list is at depth 1, and each nested list is one deeper. For
/// example:
///
/// ```md
/// - foo
///   - bar
/// ```
///
/// `foo` is at depth 1 and `bar` is at depth 2. This value is therefore the total number of list
/// levels that can be nested inside one another.
pub const MAX_DEPTH: u8 = 10;

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

/// The minimum value an ordered list can start with: see [`Type::Ordered`].
pub const MIN_ORDERED_START_VALUE: NonZero<u32> = NonZero::new(1).unwrap();

/// The maximum value an ordered list can start with: see [`Type::Ordered`].
pub const MAX_ORDERED_START_VALUE: NonZero<u32> = NonZero::new(1_000_000_000).unwrap();

/// The type of the list item, i.e. ordered or unordered. Joined with the associated content in
/// [`List`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case")
)]
pub enum Type {
	/// e.g. `1. [text]`, where `1` is the value
	///
	/// Its value is between [`MIN_ORDERED_START_VALUE`] and [`MAX_ORDERED_START_VALUE`].
	Ordered(NonZero<u32>),
	/// Either `- [text]` or `* [text]`.
	Unordered,
}

/// A list element.
#[derive(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(feature = "serde", derive(serde::Serialize, serde::Deserialize))]
pub struct List<'data, S: Span> {
	/// The type of the list, either ordered or unordered.
	///
	/// Since the type is only stored alongside the list as a whole, only the first ordered value
	/// is stored. This is consistent with rendering requirements, since renderers must begin the
	/// list at this value and increment subsequent values by 1, regardless of their actual value.
	#[cfg_attr(feature = "serde", serde(rename = "type", flatten))]
	pub kind: Type,
	/// The content of the list, where each item in the `Vec` represents each item in the list.
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

/// Parse an unknown amount of indentation, including 0.
///
/// Returns the amount of indentation parsed. [`INDENT_CHAR`] is used to detect indentation. This
/// does not consume the parsed indentation.
///
/// # Errors
/// Never.
pub fn peek_indent<'data, E>(data: Input<'data>) -> IResult<Input<'data>, usize, E>
where
	E: ParseError<'data>,
{
	peek(many0_count(char(INDENT_CHAR))).parse_complete(data)
}

/// Parse either [`unordered_type`] or [`ordered_type`] for the first item of the list.
///
/// # Errors
/// If the content does not begin with either type.
pub fn start_type<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Type, E>
where
	E: ParseError<'data>,
{
	alt((unordered_type, ordered_type)).parse_complete(data)
}

/// Parse the type of an ordered list, including its value.
///
/// This accepts arbitrarily large list item numbers and clamps the value between
/// [`MIN_ORDERED_START_VALUE`] and [`MAX_ORDERED_START_VALUE`].
///
/// # Errors
/// If the content does not begin with an ordered list signature.
pub fn ordered_type<'data, E>(data: Input<'data>) -> IResult<Input<'data>, Type, E>
where
	E: ParseError<'data>,
{
	terminated(
		fold(
			1..,
			satisfy(|ch: char| ch.is_ascii_digit()),
			|| 0u32,
			|acc, ch| {
				acc.saturating_mul(10)
					.saturating_add(u32::from(ch as u8 - b'0'))
			},
		),
		pair(char('.'), space1),
	)
	.map(|value| {
		NonZero::new(value)
			.unwrap_or(MIN_ORDERED_START_VALUE)
			.clamp(MIN_ORDERED_START_VALUE, MAX_ORDERED_START_VALUE)
	})
	.map(Type::Ordered)
	.parse_complete(data)
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

/// Parse an amount of indentation in the range `min_indent..=min_indent + `[`MAX_INDENT`].
///
/// Returns the amount of indentation parsed. [`INDENT_CHAR`] is used to detect indentation.
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
		// descend into the list we're about to parse before checking, so that the depth being
		// compared is this list's own depth rather than its parent's
		let context = context.with_deeper_list();

		if context.list_depth > MAX_DEPTH {
			return with_context("max list depth exceeded", fail::<_, List<'data, S>, E>())
				.parse(data);
		}

		let (data, (kind, first_item)) =
			item::item(context.clone(), amount, start_type).parse_complete(data)?;

		let parse_type = move |data| match kind {
			Type::Unordered => unordered_type(data),
			Type::Ordered(_) => ordered_type(data),
		};

		map(
			fold_many0(
				preceded(
					context.clone().line_prefix(),
					item::item(context, amount, parse_type),
				),
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
		context::Context, list, list_item, list_items, node::Node, paragraph, span::Span,
		test_utils::handle_nom_err,
	};

	use super::{List, MAX_DEPTH, MAX_ORDERED_START_VALUE, Type, item::INDENT_STEP, list};

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
				kind: Type::Ordered(1.try_into().unwrap()),
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

	/// Build markdown with `levels` levels of nested unordered lists, each item indented by
	/// [`INDENT_STEP`] relative to its parent. For example, `levels == 3`:
	///
	/// ```md
	/// - foo
	///   - foo
	///     - foo
	/// ```
	fn nested_list(levels: usize) -> String {
		(0..levels)
			.map(|level| format!("{}- foo", " ".repeat(level * INDENT_STEP)))
			.collect::<Vec<_>>()
			.join("\n")
	}

	/// The depth of the most deeply nested list, matching the 1-indexed convention of
	/// [`MAX_DEPTH`]: `list` itself counts as one level.
	fn nesting_depth<S: Span>(list: &List<'_, S>) -> u8 {
		let deepest_child = list
			.items
			.iter()
			.flat_map(|item| item.content.iter())
			.filter_map(|node| match &node.value {
				Node::List(nested) => Some(nesting_depth(nested)),
				_ => None,
			})
			.max()
			.unwrap_or(0);

		1 + deepest_child
	}

	/// Lists nested exactly to [`MAX_DEPTH`] still parse as lists all the way down.
	#[test]
	fn max_depth_nesting() {
		let s = nested_list(MAX_DEPTH as usize);
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.as_str().into())
			.finish()
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(nesting_depth(&res), MAX_DEPTH);
	}

	/// Lists nested beyond [`MAX_DEPTH`] stop nesting: the too-deep bullet is parsed as text
	/// content of the deepest allowed item instead of opening another list.
	#[test]
	fn beyond_max_depth_is_not_a_list() {
		let s = nested_list(MAX_DEPTH as usize + 1);
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.as_str().into())
			.finish()
			.map_err(handle_nom_err(&s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		// the extra level did not deepen the tree
		assert_eq!(nesting_depth(&res), MAX_DEPTH);

		// walk down to the deepest list and check its item swallowed the bullet as text
		let mut deepest = &res;
		for _ in 1..MAX_DEPTH {
			deepest = deepest
				.items
				.iter()
				.flat_map(|item| item.content.iter())
				.find_map(|node| match &node.value {
					Node::List(nested) => Some(nested),
					_ => None,
				})
				.expect("expected a nested list");
		}
		assert_eq!(
			deepest.items.value,
			vec![list_item![paragraph!("foo"), paragraph!("- foo")]]
		);
	}

	#[test]
	fn very_large_ordered_value() {
		let s = "9999999999999999999999999. foo\n9999999999999999999999999. bar";
		let (rem, res) = list::<(), _>(Context::default())
			.parse_complete(s.into())
			.finish()
			.map_err(handle_nom_err(s))
			.expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			res,
			List {
				kind: Type::Ordered(MAX_ORDERED_START_VALUE),
				items: list_items!(list_item!("foo"), list_item!("bar")),
			}
		);
	}
}
