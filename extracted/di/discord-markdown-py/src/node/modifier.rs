//! Modifiers: markup that wraps inline content.
//!
//! A modifier applies to whatever lies between its delimiters, regardless of position relative to
//! other rules. Covering several blocks, it splits into a fragment inside each: `*1. foo\n2. bar*`
//! is a list of two italics. Modifiers are not parsed as rules; their delimiters are recorded while
//! parsing and resolved into the finished tree afterwards, by [`crate::range`]. Each module here
//! defines a modifier's delimiters and how to write it back.

use crate::rule::Rule;

pub mod bold;
pub mod italic;
pub mod spoiler;
pub mod strikethrough;
pub mod underline;

/// The kinds of modifier, one per [`crate::rule::MODIFIER_RULES`] member. Each has its own
/// [`super::Inline`] variant; see [`super::Inline::modifier_kind`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ModifierKind {
	Bold,
	Italic,
	Underline,
	Strikethrough,
	Spoiler,
}

impl ModifierKind {
	#[must_use]
	pub const fn rule(self) -> Rule {
		match self {
			Self::Bold => Rule::Bold,
			Self::Italic => Rule::Italic,
			Self::Underline => Rule::Underline,
			Self::Strikethrough => Rule::Strikethrough,
			Self::Spoiler => Rule::Spoiler,
		}
	}

	/// How many delimiter characters it spends at each end.
	#[must_use]
	pub const fn delimiter_len(self) -> usize {
		match self {
			Self::Italic => 1,
			_ => 2,
		}
	}

	/// Whether two adjacent modifiers of this kind merge into one. Spoilers don't: two of them are
	/// two independently revealable regions.
	#[must_use]
	pub const fn merges(self) -> bool {
		!matches!(self, Self::Spoiler)
	}
}
