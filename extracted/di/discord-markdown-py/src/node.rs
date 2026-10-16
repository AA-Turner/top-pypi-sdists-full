pub use block::Block;
pub use element::{Element, Elements, SpannedElement, merge_text};
pub use id::{Id, Ids};
pub use inline::{Inline, flatten, flatten_owned};
pub use iter::Iter;

use super::span::Spanned;

pub mod block;
mod element;
mod id;
pub mod inline;
mod iter;
pub mod modifier;

/// A vec of `N`, each wrapped in a span, and wrapped in a span itself.
pub type Sequence<S, N> = Spanned<Vec<Spanned<N, S>>, S>;

/// A [`Block`] wrapped in a span.
pub type SpannedBlock<'data, S> = Spanned<Block<'data, S>, S>;
/// A vec of [`Block`]s, all of which are wrapped in a span: what [`crate::parse`] produces.
pub type Blocks<'data, S> = Sequence<S, Block<'data, S>>;
/// An [`Inline`] wrapped in a span.
pub type SpannedInline<'data, S> = Spanned<Inline<'data, S>, S>;
/// A vec of [`Inline`]s, all of which are wrapped in a span.
pub type Inlines<'data, S> = Sequence<S, Inline<'data, S>>;
