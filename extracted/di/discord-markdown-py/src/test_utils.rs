use crate::{
	Input, Options,
	error::PResult,
	node::{Block, Blocks, Element, Elements, Ids, Inline, Inlines},
	parse,
	range::{Unmatched, resolve, resolve_inline},
	span::{Span, Spanned},
	syntax::SyntaxSet,
};

/// Run `parser` over `s`, with what it left unconsumed.
pub fn run<'data, T>(
	s: &'data str,
	parser: impl FnOnce(&mut Input<'data>) -> PResult<T>,
) -> PResult<(Input<'data>, T)> {
	let mut input = Input::from(s);
	let output = parser(&mut input)?;
	Ok((input, output))
}

/// Parse `s` with the default options.
pub fn parsed(s: &str) -> Blocks<'_, ()> {
	parse::<()>(s, Options::default()).expect("unable to parse")
}

/// The inline content of `s`, which must parse to a single paragraph.
pub fn inline_content(s: &str) -> Inlines<'_, ()> {
	let mut nodes = parsed(s);
	match nodes.value.as_mut_slice() {
		[
			Spanned {
				value: Block::Paragraph(content),
				..
			},
		] => std::mem::take(content),
		_ => panic!("expected {s:?} to parse to one paragraph, got {nodes:?}"),
	}
}

/// Resolve the delimiters in a sequence of blocks a sub-parser produced, as [`parse`] would for a
/// whole message.
pub fn resolved_blocks<S: Span>(nodes: Elements<'_, S>) -> Blocks<'_, S> {
	let value = resolve(
		nodes.value,
		SyntaxSet::all(),
		Unmatched::Text,
		&mut Ids::default(),
	)
	.expect("only a rejecting resolve fails");
	Spanned {
		value,
		span: nodes.span,
	}
}

/// [`resolved_blocks`] for inline content.
pub fn resolved_inlines<S: Span>(nodes: Elements<'_, S>) -> Inlines<'_, S> {
	Spanned {
		value: resolve_inline(nodes.value, SyntaxSet::all(), &mut Ids::default()),
		span: nodes.span,
	}
}

/// `node` alone in a sequence.
fn alone<S: Span>(node: Element<'_, S>) -> Elements<'_, S> {
	Spanned {
		value: vec![Spanned {
			value: node,
			span: S::default(),
		}],
		span: S::default(),
	}
}

/// [`resolved_blocks`] for a single block, which must resolve to a single block.
pub fn resolved_block<S: Span>(node: Element<'_, S>) -> Block<'_, S> {
	let mut nodes = resolved_blocks(alone(node));
	assert_eq!(nodes.len(), 1, "expected a single block, got {nodes:?}");
	nodes.value.remove(0).value
}

/// [`resolved_inlines`] for a single node, which must resolve to a single node.
pub fn resolved_inline<S: Span>(node: Element<'_, S>) -> Inline<'_, S> {
	let mut nodes = resolved_inlines(alone(node));
	assert_eq!(nodes.len(), 1, "expected a single node, got {nodes:?}");
	nodes.value.remove(0).value
}
