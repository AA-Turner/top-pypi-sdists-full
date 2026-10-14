use nom_language::error::{VerboseError, convert_error};

use crate::{
	Input, Options,
	node::{Element, Ids, Node, ParsedNode, ParsedNodes, SpannedNodes},
	parse,
	range::{Content, Unmatched, resolve},
	rule::RuleSet,
	span::{Span, Spanned},
};

pub fn handle_nom_err<'data>(input: &'data str) -> impl Fn(VerboseError<Input<'data>>) -> String {
	move |error| {
		let error = convert_error(input.into(), error);
		eprintln!("{error}");
		error
	}
}

/// Parse `s` with the default options.
pub fn parsed(s: &str) -> SpannedNodes<'_, ()> {
	parse::<(), _>(s, Options::default())
		.map_err(handle_nom_err(s))
		.expect("unable to parse")
}

/// The inline content of `s`, which must parse to a single paragraph.
pub fn inline_content(s: &str) -> SpannedNodes<'_, ()> {
	let mut nodes = parsed(s);
	match nodes.value.as_mut_slice() {
		[
			Spanned {
				value: Node::Element(Element::Paragraph(content)),
				..
			},
		] => std::mem::take(content),
		_ => panic!("expected {s:?} to parse to one paragraph, got {nodes:?}"),
	}
}

/// Resolve the delimiters in what a sub-parser produced, as [`parse`] would for a whole message.
pub fn resolved<S: Span>(nodes: ParsedNodes<'_, S>, content: Content) -> SpannedNodes<'_, S> {
	let value = resolve(
		nodes.value,
		RuleSet::all(),
		content,
		Unmatched::Text,
		&mut Ids::default(),
	)
	.expect("only a rejecting resolve fails");
	Spanned {
		value,
		span: nodes.span,
	}
}

/// [`resolved`] for a single node, which must resolve to a single node.
pub fn resolved_node<S: Span>(node: ParsedNode<'_, S>, content: Content) -> Node<'_, S> {
	let mut nodes = resolved(
		Spanned {
			value: vec![Spanned {
				value: node,
				span: S::default(),
			}],
			span: S::default(),
		},
		content,
	);
	assert_eq!(nodes.len(), 1, "expected a single node, got {nodes:?}");
	nodes.value.remove(0).value
}
