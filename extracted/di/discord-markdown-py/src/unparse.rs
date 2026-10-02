use std::fmt::{from_fn, Display, Formatter, Result};

/// Turns AST nodes back into the markdown that they came from.
///
/// Generally, [`Display`] should produce something approximate to the rendered value and
/// [`Unparse`] should produce the original markdown syntax. See [`UnparseDisplay`] if these are
/// equivalent.
///
/// For example:
///
/// `{"type": "bold": "value": [{"type": "text", "value": "foo"}]}` -> `**foo**`
pub trait Unparse {
	/// Format the output markdown content
	///
	/// # Errors
	/// If formatting fails
	fn fmt(&self, f: &mut Formatter) -> Result;

	fn unparse(&self) -> impl Display {
		from_fn(|f| self.fmt(f))
	}
}

impl<T> Unparse for Vec<T>
where
	T: Unparse,
{
	fn fmt(&self, f: &mut Formatter) -> Result {
		for item in self {
			item.fmt(f)?;
		}

		Ok(())
	}
}

/// Turn anything that can be unparsed back into markdown. The counterpart to [`crate::parse`].
///
/// # Fidelity
///
/// The AST does not retain every detail of how the source was written, so the output is not
/// byte-exact for everything:
///
/// - Text is not re-escaped, so `\*not italic\*` comes back as `*not italic*`, which does parse
///   as italics.
/// - Italics always emit `_`, whichever delimiter was written.
/// - Markup nested inside the same markup is dropped when parsing, since the outer node already
///   applies it -- and that reaches through markup in between, so `*a **b _c_ d** e*` comes back
///   as `_a **b c d** e_`.
/// - Unordered lists always emit `* `, and nested-list indentation and per-item markers are lost.
/// - A link with no text loses whether it was written bare or wrapped in `<>`.
/// - A link written without a scheme comes back with `https://`, since that is the URL it parsed
///   to: `discord.gg/abc` unparses as `https://discord.gg/abc`.
///
/// Everything else round trips exactly.
#[must_use]
pub fn unparse<T>(value: &T) -> String
where
	T: Unparse + ?Sized,
{
	value.unparse().to_string()
}

/// Convenience trait for implementing [`Unparse`] on types that unparse into their [`Display`]
/// impl.
///
/// [`Unparse`] is not implemented for all `T: Display` because some types may unparse into a
/// different value than they display.
pub trait UnparseDisplay: Display {}

impl<T> Unparse for T
where
	T: UnparseDisplay,
{
	fn fmt(&self, f: &mut Formatter) -> Result {
		Display::fmt(self, f)
	}
}

#[cfg(test)]
mod test {
	use std::fmt::Display;

	use static_assertions::assert_impl_all;

	use super::{unparse, Unparse, UnparseDisplay};
	use crate::{context::Options, error::Error, node::SpannedNodes, parse};

	struct Test;

	impl Display for Test {
		fn fmt(&self, _f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
			unimplemented!()
		}
	}

	impl UnparseDisplay for Test {}

	assert_impl_all!(Test: Unparse);

	// `serde_wasm_bindgen::from_value` requires `DeserializeOwned` outright, so a
	// `#[serde(borrow)]` attribute anywhere in the AST breaks the wasm binding's `unparse`.
	#[cfg(feature = "serde")]
	assert_impl_all!(SpannedNodes<'static, ()>: serde::de::DeserializeOwned);

	/// Markdown that survives a parse and an unparse byte for byte.
	///
	/// The omissions are deliberate, and are the cases [`unparse`] documents as lossy: escaped
	/// text, `*italic*`, `- ` lists, nested list indentation, and a code block written without a
	/// leading newline.
	const CORPUS: &[&str] = &[
		// inline
		"plain text",
		"**bold**",
		"__underline__",
		"~~strikethrough~~",
		"||spoiler||",
		"_italic_",
		"`code`",
		"**bold _italic_ and `code`**",
		// an italic whose closer is the first half of the nested rule's opener
		"_foo __bar__ baz_",
		// mentions, which are also the bindings' bigint path
		"<@873227248453443624>",
		"<#873227248453443624>",
		"<@&873227248453443624>",
		"@everyone",
		"@here",
		"</settings:873227248453443624>",
		// timestamps and emoji
		"<t:1234567890>",
		"<t:1234567890:R>",
		"<:pepe:873227248453443624>",
		"<a:pepe:873227248453443624>",
		// links, including the mention links that unparsing exists for
		"https://example.com/",
		"[text](https://example.com/)",
		"https://discord.gg/abc",
		"https://discord.com/invite/abc",
		"https://discord.com/shop?tab=orbs",
		"https://discord.com/channels/1/2",
		"https://discord.com/channels/1/2/3",
		"dev://branch/main",
		// blocks
		"# heading one",
		"## heading two",
		"### heading three",
		"> quoted line",
		"> quote with **bold**",
		"-# small text",
		"# heading with <@873227248453443624>",
		"```js\nconst a = 1;\n```",
		"```\nplain\n```",
		"```js\nno trailing newline```",
	];

	/// A parsed document has to unparse back into exactly what was written.
	#[test]
	fn unparse_round_trips() {
		for s in CORPUS {
			let nodes = parse::<(), Error<'_>>(*s, Options::default())
				.unwrap_or_else(|err| panic!("unable to parse {s:?}: {err}"));

			assert_eq!(unparse(&nodes), *s, "{s:?}");
		}
	}

	/// The AST has to survive a round trip through a deserializer that cannot borrow.
	///
	/// The static bound above is necessary but not sufficient: `&'de str` satisfies
	/// `Deserialize<'de>` for every `'de`, so a borrowed field type-checks and only fails at run
	/// time, with "expected a borrowed string". Every deserializer the bindings use is owned.
	#[cfg(feature = "serde")]
	#[test]
	fn round_trips_through_an_owned_deserializer() {
		for s in CORPUS {
			let nodes = parse::<(), Error<'_>>(*s, Options::default())
				.unwrap_or_else(|err| panic!("unable to parse {s:?}: {err}"));

			let value = serde_json::to_value(&nodes)
				.unwrap_or_else(|err| panic!("unable to serialize {s:?}: {err}"));
			let owned: SpannedNodes<'static, ()> = serde_json::from_value(value)
				.unwrap_or_else(|err| panic!("unable to deserialize {s:?}: {err}"));

			assert_eq!(owned, nodes, "{s:?}");
			assert_eq!(unparse(&owned), *s, "{s:?}");
		}
	}

	/// The same round trip over the fixtures, which reach node types [`CORPUS`] does not: lists,
	/// nested blocks, masked links.
	#[cfg(feature = "serde")]
	#[test]
	fn fixtures_round_trip_through_an_owned_deserializer() {
		for entry in std::fs::read_dir("test_content").expect("unable to read test_content") {
			let path = entry.expect("unable to read entry").path();
			let markdown =
				std::fs::read_to_string(path.join("content.md")).expect("unable to read content");

			let nodes = parse::<(), Error<'_>>(&*markdown, Options::default())
				.unwrap_or_else(|err| panic!("unable to parse {}: {err}", path.display()));

			let value = serde_json::to_value(&nodes)
				.unwrap_or_else(|err| panic!("unable to serialize {}: {err}", path.display()));
			let owned: SpannedNodes<'static, ()> = serde_json::from_value(value)
				.unwrap_or_else(|err| panic!("unable to deserialize {}: {err}", path.display()));

			assert_eq!(owned, nodes, "{}", path.display());
		}
	}

	#[test]
	fn unparses_a_single_node() {
		let nodes =
			parse::<(), Error<'_>>("**bold**", Options::default()).expect("unable to parse");
		let paragraph = &nodes.value[0].value;

		assert_eq!(unparse(paragraph), "**bold**");
	}
}
