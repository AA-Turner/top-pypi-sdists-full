use std::{fmt::Debug, hash::Hash};

use enumset::{EnumSet, EnumSetType, enum_set, enum_set_union};

#[cfg(doc)]
use super::node::{Block, Inline};

use super::grammar::{Grammar, GrammarSet};

/// A rule represents the various formatting concepts, as opposed to a [`Grammar`] which defines
/// variants therein.
///
/// For example: [`Rule::Link`] represents the entire concept of a link, whereas
/// [`Grammar::AutoLink`] and [`Grammar::MaskedLinkText`] are among the ways a link node is defined.
///
/// Rules are what a caller allows. How each is recognized varies: a [`ParsedRule`] has a parser,
/// [`MODIFIER_RULES`] are resolved from delimiters after the parse (see [`crate::range`]), and
/// [`GATE_RULES`] widen another rule.
///
/// A rule maps roughly 1:1 with [`Block`] and [`Inline`] variants and can broadly be considered
/// the content-less form of a node. However, there are some nodes that do not have a corresponding
/// rule; these nodes are considered base nodes and have no semantic meaning as a rule. Current base
/// nodes are [`Inline::Text`], [`Block::Paragraph`], and [`Block::Empty`]. The inverse also exists: a
/// [`GATE_RULES`] member has no node and gates a variant of another rule.
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
	/// Links carrying the `dev` scheme, e.g. `dev://branch/main`.
	///
	/// Without this rule a `dev` URL is not a URL, so every way of writing one is text. See
	/// [`GATE_RULES`].
	DevLink,
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

/// A [`Rule`] with a parser of its own: one of [`INLINE_RULES`] or [`BLOCK_RULES`].
///
/// Declared in the order the parser tries them.
#[derive(EnumSetType, Debug, PartialOrd, Ord, Hash)]
pub enum ParsedRule {
	// inline
	Emoji,
	Link,
	Mention,
	Timestamp,
	CodeBlock,
	Code,
	// block
	Heading,
	List,
	Quote,
	Small,
}

/// A collection of [`ParsedRule`]s.
pub type ParsedRuleSet = EnumSet<ParsedRule>;

impl ParsedRule {
	/// The rules parsed within a line.
	pub const INLINE: ParsedRuleSet = enum_set!(
		Self::Emoji | Self::Link | Self::Mention | Self::Timestamp | Self::CodeBlock | Self::Code
	);

	/// The rules parsed only at the start of a line.
	pub const BLOCK: ParsedRuleSet =
		enum_set!(Self::Heading | Self::List | Self::Quote | Self::Small);

	/// The [`Rule`] that allows this one.
	#[must_use]
	pub const fn rule(self) -> Rule {
		match self {
			Self::Emoji => Rule::Emoji,
			Self::Link => Rule::Link,
			Self::Mention => Rule::Mention,
			Self::Timestamp => Rule::Timestamp,
			Self::CodeBlock => Rule::CodeBlock,
			Self::Code => Rule::Code,
			Self::Heading => Rule::Heading,
			Self::List => Rule::List,
			Self::Quote => Rule::Quote,
			Self::Small => Rule::Small,
		}
	}

	/// The parsed rules that `rules` allows.
	#[must_use]
	pub fn allowed(rules: RuleSet) -> ParsedRuleSet {
		ParsedRuleSet::all()
			.iter()
			.filter(|parsed| rules.contains(parsed.rule()))
			.collect()
	}

	/// Grammars the correlate to this rule. For example, all link grammars are included if this is
	/// [`ParsedRule::Link`].
	#[must_use]
	pub const fn grammar(self) -> GrammarSet {
		match self {
			Self::Heading | Self::List | Self::Small => GrammarSet::empty(),
			Self::Quote => enum_set!(Grammar::Quote | Grammar::QuoteRest),
			// TODO: is this accurate? masked link grammars are only valid inside masked links
			Self::Link => {
				enum_set!(
					Grammar::AutoLink
						| Grammar::MaskedLinkLink
						| Grammar::MaskedLinkText
						| Grammar::LinkDetection
				)
			}
			Self::Code => enum_set!(Grammar::Code | Grammar::DoubleCode),
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
/// [`Block::Paragraph`] which is the base "block" node.
pub const INLINE_RULES: RuleSet = enum_set_union!(
	Rule::Emoji,
	Rule::Link,
	Rule::Mention,
	Rule::Timestamp,
	Rule::CodeBlock,
	Rule::Code,
);

/// Set of [`Rule`]s that are considered "modifier".
///
/// A modifier wraps only inline content. Covering several blocks, it splits into a fragment inside
/// each -- so `*1. foo\n2. bar*` is a list of two italics. See [`Inline::modifier_kind`].
pub const MODIFIER_RULES: RuleSet = enum_set_union!(
	Rule::Bold,
	Rule::Italic,
	Rule::Strikethrough,
	Rule::Underline,
	Rule::Spoiler,
);

/// Set of [`Rule`]s that are considered "block".
///
/// Block rules _must_ be immediately preceded by a new line or they must be the beginning of
/// content.
pub const BLOCK_RULES: RuleSet =
	enum_set_union!(Rule::Heading, Rule::List, Rule::Quote, Rule::Small);

/// Set of [`Rule`]s that widen what another rule accepts rather than producing a node.
///
/// These have no parser, so they are deliberately absent from the other sets. See
/// [`Rule::DevLink`].
pub const GATE_RULES: RuleSet = enum_set_union!(Rule::DevLink);

/// A collection of [`Rule`]s. Rules are divided into [`INLINE_RULES`], [`BLOCK_RULES`],
/// [`MODIFIER_RULES`], and [`GATE_RULES`].
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

	use super::{
		BLOCK_RULES, GATE_RULES, INLINE_RULES, MODIFIER_RULES, ParsedRule, ParsedRuleSet, Rule,
		RuleSet,
	};

	#[test]
	fn every_grammar() {
		let grammars = ParsedRuleSet::all()
			.iter()
			.flat_map(ParsedRule::grammar)
			.collect::<GrammarSet>();

		let allowed_missing = Grammar::None | Grammar::Block | Grammar::InlineBlock;
		assert_eq!(grammars, GrammarSet::all().difference(allowed_missing));
	}

	#[test]
	fn inline_block_sets() {
		assert_eq!(
			RuleSet::all(),
			INLINE_RULES ^ BLOCK_RULES ^ MODIFIER_RULES ^ GATE_RULES
		);
	}

	/// Exactly the inline and block rules have parsers.
	#[test]
	fn parsed_rules_are_inline_and_block() {
		let rules = |set: ParsedRuleSet| set.iter().map(ParsedRule::rule).collect::<RuleSet>();
		assert_eq!(rules(ParsedRule::INLINE), INLINE_RULES);
		assert_eq!(rules(ParsedRule::BLOCK), BLOCK_RULES);
		assert_eq!(ParsedRule::INLINE ^ ParsedRule::BLOCK, ParsedRuleSet::all());
		assert_eq!(
			ParsedRule::allowed(RuleSet::all() - Rule::Link - Rule::Bold),
			ParsedRuleSet::all() - ParsedRule::Link
		);
	}

	/// The bindings take rule sets as lists of these names.
	#[cfg(feature = "serde")]
	#[test]
	fn rules_serialize_by_name() {
		let set: RuleSet = super::Rule::DevLink | super::Rule::Link;
		assert_eq!(
			serde_json::to_string(&set).expect("a rule set serializes"),
			r#"["link","dev_link"]"#
		);
	}
}
