use std::num::NonZero;

use derive_where::derive_where;
use item::Item;

use crate::Input;
use crate::context::Context;
use crate::error::{Fail, PResult};
use crate::lossless::TokenKind;
use crate::node::Element;
use crate::span::{Span, Spanned, Syntax};

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
#[derive_where(Debug, Clone, PartialEq, Eq; N)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(bound(
		serialize = "N: serde::Serialize",
		deserialize = "N: serde::Deserialize<'de>"
	))
)]
pub struct List<S: Span, N> {
	/// The type of the list, either ordered or unordered.
	///
	/// Since the type is only stored alongside the list as a whole, only the first ordered value
	/// is stored. This is consistent with rendering requirements, since renderers must begin the
	/// list at this value and increment subsequent values by 1, regardless of their actual value.
	#[cfg_attr(feature = "serde", serde(rename = "type", flatten))]
	pub kind: Type,
	/// The content of the list, where each item in the `Vec` represents each item in the list.
	pub items: Spanned<Vec<Item<S, N>>, S>,
}

/// The amount of leading indentation, including 0, without consuming it. [`INDENT_CHAR`] is used
/// to detect indentation.
#[must_use]
pub fn peek_indent(input: &Input) -> usize {
	input.chars().take_while(|&ch| ch == INDENT_CHAR).count()
}

/// Parse either [`unordered_type`] or [`ordered_type`] for the first item of the list. Like
/// them, it leaves the space after the marker to [`item::item`].
///
/// # Errors
/// If the content does not begin with either type.
pub fn start_type(input: &mut Input) -> PResult<Type> {
	match input.attempt(unordered_type)? {
		Some(kind) => Ok(kind),
		None => ordered_type(input),
	}
}

/// Parse the type of an ordered list, including its value.
///
/// This accepts arbitrarily large list item numbers and clamps the value between
/// [`MIN_ORDERED_START_VALUE`] and [`MAX_ORDERED_START_VALUE`].
///
/// # Errors
/// If the content does not begin with an ordered list signature.
pub fn ordered_type(input: &mut Input) -> PResult<Type> {
	let digits = input.take_while1(|ch| ch.is_ascii_digit())?;
	input.char('.')?;

	let value = digits.bytes().fold(0u32, |acc, digit| {
		acc.saturating_mul(10)
			.saturating_add(u32::from(digit - b'0'))
	});
	Ok(Type::Ordered(
		NonZero::new(value)
			.unwrap_or(MIN_ORDERED_START_VALUE)
			.clamp(MIN_ORDERED_START_VALUE, MAX_ORDERED_START_VALUE),
	))
}

/// Parse the type of an unordered list, as determined by any of [`UNORDERED_CONTROL_CHARS`].
///
/// # Errors
/// If the content does not begin with an unordered list signature.
pub fn unordered_type(input: &mut Input) -> PResult<Type> {
	input.satisfy(|ch| UNORDERED_CONTROL_CHARS.contains(ch))?;
	Ok(Type::Unordered)
}

/// Parse an amount of indentation in the range `min_indent..=min_indent + `[`MAX_INDENT`],
/// returning the amount parsed. [`INDENT_CHAR`] is used to detect indentation.
///
/// # Errors
/// If there is less than `min_indent` of it.
pub fn indent(input: &mut Input, min_indent: usize) -> PResult<usize> {
	let amount = peek_indent(input).min(min_indent + MAX_INDENT);
	if amount < min_indent {
		return Err(Fail::NoMatch);
	}
	input.advance(amount * INDENT_CHAR.len_utf8());
	Ok(amount)
}

/// Parse a list with a specified amount of indentation, parsed by [`indent`].
///
/// # Errors
/// If the content does not begin with a list at that indentation, or the list would be nested
/// deeper than [`MAX_DEPTH`].
pub fn indented<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
	amount: usize,
) -> PResult<List<S, Element<'data, S>>> {
	// descend into the list we're about to parse before checking, so that the depth being
	// compared is this list's own depth rather than its parent's
	let context = context.with_deeper_list();
	if context.list_depth > MAX_DEPTH {
		return Err(Fail::NoMatch);
	}

	let (kind, first_item) = item::item(input, &context, amount, start_type)?;
	let parse_type: fn(&mut Input) -> PResult<Type> = match kind {
		Type::Unordered => unordered_type,
		Type::Ordered(_) => ordered_type,
	};

	let items = input.spanned_with_syntax(|input| {
		let mut items = vec![first_item];
		let mut syntax = S::Syntax::default();
		while let Some((prefix, (_, item))) = input.attempt(|input| {
			let prefix =
				input.token::<S, _>(TokenKind::QuotePrefix, |input| context.line_prefix(input))?;
			Ok((prefix, item::item(input, &context, amount, parse_type)?))
		})? {
			items.push(item);
			syntax.append(prefix);
		}
		Ok((items, syntax))
	})?;

	Ok(List { kind, items })
}

/// Parse a list.
///
/// Detects the appropriate amount of indentation with which to start. Use [`indented`] to parse
/// with a specific amount of indentation.
///
/// # Errors
/// If the content does not begin with a list.
pub fn list<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<List<S, Element<'data, S>>> {
	let indent = peek_indent(input);
	indented(input, context, indent)
}

#[cfg(test)]
mod test {
	use pretty_assertions::assert_eq;

	use crate::{
		context::Context,
		list, list_item, list_items,
		node::{Block, Element},
		paragraph,
		span::Span,
		test_utils::{resolved_block, run},
	};

	use super::{List, MAX_DEPTH, MAX_ORDERED_START_VALUE, Type, item::INDENT_STEP, list};

	/// Resolve the delimiters in a list, as a whole parse would.
	fn resolved_list(list: List<(), Element<'_, ()>>) -> List<(), Block<'_, ()>> {
		match resolved_block(Element::List(list)) {
			Block::List(list) => list,
			other => panic!("expected a list, got {other:?}"),
		}
	}

	#[test]
	fn unordered_item() {
		let s = "- foo";
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"))
			}
		);
	}

	#[test]
	fn multiple_unordered_items() {
		let s = "- foo\n- bar";
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
			List {
				kind: Type::Unordered,
				items: list_items!(list_item!("foo"), list_item!("bar"))
			}
		);
	}

	#[test]
	fn sub_items() {
		let s = "- foo\n  - bar";
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
			List {
				kind: Type::Unordered,
				items: list_items![list_item!(paragraph!("foo"), list!(-[list_item!("bar")]))]
			}
		);
	}

	#[test]
	fn sub_items_with_content() {
		let s = "- foo\n  - bar\n  baz\n  - box";
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
			List {
				kind: Type::Ordered(1.try_into().unwrap()),
				items: list_items!(list_item!("foo"), list_item!("bar"))
			}
		);
	}

	#[test]
	fn dedented() {
		let s = "- foo\n  - bar\n- baz";
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
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
	fn nesting_depth<S: Span>(list: &List<S, Element<'_, S>>) -> u8 {
		let deepest_child = list
			.items
			.iter()
			.flat_map(|item| item.content.iter())
			.filter_map(|node| match &node.value {
				Element::List(nested) => Some(nesting_depth(nested)),
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
		let (rem, res) =
			run(&s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(nesting_depth(&res), MAX_DEPTH);
	}

	/// Lists nested beyond [`MAX_DEPTH`] stop nesting: the too-deep bullet is parsed as text
	/// content of the deepest allowed item instead of opening another list.
	#[test]
	fn beyond_max_depth_is_not_a_list() {
		let s = nested_list(MAX_DEPTH as usize + 1);
		let (rem, res) =
			run(&s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		// the extra level did not deepen the tree
		assert_eq!(nesting_depth(&res), MAX_DEPTH);

		// walk down to the deepest list and check its item swallowed the bullet as text
		let res = resolved_list(res);
		let mut deepest = &res;
		for _ in 1..MAX_DEPTH {
			deepest = deepest
				.items
				.iter()
				.flat_map(|item| item.content.iter())
				.find_map(|node| match &node.value {
					Block::List(nested) => Some(nested),
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
		let (rem, res) =
			run(s, |input| list::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(
			resolved_list(res),
			List {
				kind: Type::Ordered(MAX_ORDERED_START_VALUE),
				items: list_items!(list_item!("foo"), list_item!("bar")),
			}
		);
	}
}
