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

#[cfg(all(test, feature = "serde"))]
mod test {
	use static_assertions::assert_impl_all;

	use super::Blocks;
	use crate::{context::Options, parse};

	// `serde_json::from_value` and the like require `DeserializeOwned` outright, so a
	// `#[serde(borrow)]` attribute anywhere in the AST would keep it from being read back.
	assert_impl_all!(Blocks<'static, ()>: serde::de::DeserializeOwned);

	/// Markdown reaching every inline and block node, mentions included for their 64-bit ids.
	const CORPUS: &[&str] = &[
		"plain text",
		"**bold** _italic_ __underline__ ~~strikethrough~~ ||spoiler|| `code`",
		"<@873227248453443624> <#873227248453443624> <@&873227248453443624> @everyone @here",
		"</settings:873227248453443624> <id:home>",
		"<t:1234567890> <t:1234567890:R>",
		"<:pepe:873227248453443624> <a:pepe:873227248453443624> 😀",
		"https://example.com/ [text](https://example.com/) [titled](https://example.com/ \"title\")",
		"# heading\n## heading\n-# small text\n> quoted line\n- item\n1. item",
		"```js\nconst a = 1;\n```",
	];

	/// The AST has to survive a round trip through a deserializer that cannot borrow.
	///
	/// The static bound above is necessary but not sufficient: `&'de str` satisfies
	/// `Deserialize<'de>` for every `'de`, so a borrowed field type-checks and only fails at run
	/// time, with "expected a borrowed string".
	#[test]
	fn round_trips_through_an_owned_deserializer() {
		for s in CORPUS {
			let nodes = parse::<()>(*s, Options::default())
				.unwrap_or_else(|err| panic!("unable to parse {s:?}: {err}"));

			let value = serde_json::to_value(&nodes)
				.unwrap_or_else(|err| panic!("unable to serialize {s:?}: {err}"));
			let owned: Blocks<'static, ()> = serde_json::from_value(value)
				.unwrap_or_else(|err| panic!("unable to deserialize {s:?}: {err}"));

			assert_eq!(owned, nodes, "{s:?}");
		}
	}

	/// The same round trip over the fixtures, which reach the nesting [`CORPUS`] does not.
	#[test]
	fn fixtures_round_trip_through_an_owned_deserializer() {
		for entry in std::fs::read_dir("test_content").expect("unable to read test_content") {
			let path = entry.expect("unable to read entry").path();
			let markdown =
				std::fs::read_to_string(path.join("content.md")).expect("unable to read content");

			let nodes = parse::<()>(&*markdown, Options::default())
				.unwrap_or_else(|err| panic!("unable to parse {}: {err}", path.display()));

			let value = serde_json::to_value(&nodes)
				.unwrap_or_else(|err| panic!("unable to serialize {}: {err}", path.display()));
			// `from_value` deserializes owned whatever the lifetime, which must match `nodes`: a
			// node is invariant in its lifetime
			let owned: Blocks<'_, ()> = serde_json::from_value(value)
				.unwrap_or_else(|err| panic!("unable to deserialize {}: {err}", path.display()));

			assert_eq!(owned, nodes, "{}", path.display());
		}
	}
}
