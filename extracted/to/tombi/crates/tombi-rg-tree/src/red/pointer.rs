use std::iter::successors;

use super::RedNode;
use crate::Language;

/// A "pointer" to a [`RedNode`], via location in the source code.
#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
pub struct RedNodePtr<L: Language> {
    kind: L::Kind,
    span: tombi_text::Span,
}

impl<L: Language> RedNodePtr<L> {
    /// Returns a [`SyntaxNodePtr`] for the node.
    pub fn new(node: &RedNode<L>) -> Self {
        Self {
            kind: node.kind(),
            span: node.span(),
        }
    }

    /// Like [`Self::try_to_node`] but panics instead of returning `None` on
    /// failure.
    pub fn to_node(&self, root: &RedNode<L>) -> RedNode<L> {
        self.try_to_node(root)
            .unwrap_or_else(|| panic!("can't resolve {self:?} with {root:?}"))
    }

    /// "Dereferences" the pointer to get the [`RedNode`] it points to.
    ///
    /// Returns `None` if the node is not found, so make sure that the `root`
    /// syntax tree is equivalent to (i.e. is build from the same text from) the
    /// tree which was originally used to get this [`SyntaxNodePtr`].
    ///
    /// Also returns `None` if `root` is not actually a root (i.e. it has a
    /// parent).
    ///
    /// The complexity is linear in the depth of the tree and logarithmic in
    /// tree width. As most trees are shallow, thinking about this as
    /// `O(log(N))` in the size of the tree is not too wrong!
    pub fn try_to_node(&self, root: &RedNode<L>) -> Option<RedNode<L>> {
        if root.parent().is_some() {
            return None;
        }
        successors(Some(root.clone()), |node| {
            node.child_or_token_at_span(self.span)?.into_node()
        })
        .find(|it| it.span() == self.span && it.kind() == self.kind)
    }

    /// Returns the kind of the syntax node this points to.
    pub fn kind(&self) -> L::Kind {
        self.kind
    }

    /// Returns the range of the syntax node this points to.
    pub fn span(&self) -> tombi_text::Span {
        self.span
    }
}
