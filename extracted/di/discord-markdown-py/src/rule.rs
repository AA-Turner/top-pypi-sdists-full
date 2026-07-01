use std::{fmt::Debug, hash::Hash};

use enumset::{enum_set, enum_set_union, EnumSet, EnumSetType};

#[cfg(doc)]
use super::node::Node;

use super::grammar::{Grammar, GrammarSet};

/// A rule represents the various formatting concepts, as opposed to a [`Grammar`] which defines
/// variants therein.
///
/// For example: [`Rule::Italic`] represents the entire concept of italic,
/// whereas [`Grammar::UnderscoreItalic`] and [`Grammar::AsteriskItalic`] represent
/// the 2 (currently) supported ways that an italic node is defined. In most cases there is only
/// 1 grammar for each rule.
///
/// A rule maps roughly 1:1 with [`Node`] and can broadly be considered the content-less form of
/// a node. However, there are some nodes that do not have a corresponding rule; these nodes are
/// considered base nodes and have no semantic meaning as a rule. Current base nodes are
/// [`Node::Text`], [`Node::Paragraph`], and [`Node::Empty`].
///
/// See [`RuleSet`] for information about what a collection of Rules means.
#[derive(EnumSetType, Debug, PartialOrd, Ord, Hash)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(rename_all = "snake_case"),
	enumset(serialize_repr = "list")
)]
pub enum Rule {
	// inline
	Bold,
	Emoji,
	Italic,
	Link,
	Mention,
	Strikethrough,
	Timestamp,
	Underline,
	CodeBlock,
	Code,
	Spoiler,
	// block
	Heading,
	List,
	Quote,
	Small,
}

impl Rule {
	/// Grammars the correlate to this rule. For example, all link grammars are included if this is
	/// [`Rule::Link`].
	#[must_use]
	pub const fn grammar(&self) -> GrammarSet {
		match self {
			Self::Heading | Self::List | Self::Small => GrammarSet::empty(),
			Self::Quote => enum_set!(Grammar::Quote),
			Self::Bold => enum_set!(Grammar::Bold),
			Self::Italic => enum_set!(Grammar::AsteriskItalic | Grammar::UnderscoreItalic),
			// TODO: is this accurate? masked link grammars are only valid inside masked links
			Self::Link => {
				enum_set!(
					Grammar::AutoLink
						| Grammar::MaskedLinkLink
						| Grammar::MaskedLinkText
						| Grammar::LinkDetection
				)
			}
			Self::Strikethrough => enum_set!(Grammar::Strikethrough),
			Self::Underline => enum_set!(Grammar::Underline),
			Self::Spoiler => enum_set!(Grammar::Spoiler),
			Self::Code => enum_set!(Grammar::Code),
			Self::CodeBlock => enum_set!(Grammar::CodeBlock),
			Self::Timestamp => enum_set!(Grammar::Timestamp),
			Self::Emoji => enum_set!(Grammar::CustomEmoji | Grammar::ColonDelimitedEmoji),
			Self::Mention => {
				enum_set!(
					Grammar::EveryoneMention
						| Grammar::HereMention
						| Grammar::UserMention
						| Grammar::ChannelMention
						| Grammar::RoleMention
						| Grammar::CommandMention
				)
			}
		}
	}
}

/// Set of [`Rule`]s that are considered "inline".
///
/// Inline rules can appear anywhere, although a top-level inline rule will get wrapped in a
/// [`Node::Paragraph`] which is the base "block" node.
pub const INLINE_RULES: RuleSet = enum_set_union!(
	Rule::Bold,
	Rule::Emoji,
	Rule::Italic,
	Rule::Link,
	Rule::Mention,
	Rule::Strikethrough,
	Rule::Timestamp,
	Rule::Underline,
	Rule::CodeBlock,
	Rule::Code,
	Rule::Spoiler,
);

/// Set of [`Rule`]s that are considered "block".
///
/// Block rules _must_ be immediately preceded by a new line or they must be the beginning of
/// content.
pub const BLOCK_RULES: RuleSet =
	enum_set_union!(Rule::Heading, Rule::List, Rule::Quote, Rule::Small);

/// A collection of [`Rule`]s. Rules are divided into [`INLINE_RULES`] and [`BLOCK_RULES`].
///
/// A strict definition of inline/block rules might preclude block elements (like the heading) from
/// appearing inside inline elements (like the italics). We are explicitly less strict because, for
/// example, it is more intuitive to italicize a large chunk of content by surrounding the entire
/// thing in italics rather than italicizing each block individually.
///
/// ```md
/// _
/// # foo
/// _
/// ```
///
#[allow(clippy::module_name_repetitions)]
/// cbindgen:ignore
pub type RuleSet = EnumSet<Rule>;

#[cfg(test)]
mod test {
	use crate::grammar::{Grammar, GrammarSet};

	use super::{RuleSet, BLOCK_RULES, INLINE_RULES};

	#[test]
	fn every_grammar() {
		let rules = RuleSet::all();
		let grammars = rules
			.iter()
			.flat_map(|rule| rule.grammar())
			.collect::<GrammarSet>();

		let allowed_missing = Grammar::None | Grammar::Block | Grammar::InlineBlock;
		assert_eq!(grammars, GrammarSet::all().difference(allowed_missing));
	}

	#[test]
	fn inline_block_sets() {
		assert_eq!(RuleSet::all(), INLINE_RULES ^ BLOCK_RULES);
	}
}
