//! Modifiers: markup that wraps content without being inline or block itself.
//!
//! A modifier applies to whatever lies between its delimiters, regardless of position relative to
//! other rules: `*1. foo\n2. bar*` is an italic list. Modifiers are not parsed as rules; their
//! delimiters are recorded while parsing and resolved into the finished tree afterwards, by
//! [`crate::range`]. Each module here defines a modifier's delimiters and how to write it back.

use derive_where::derive_where;

use crate::{rule::Rule, span::Span, unparse::Unparse};

use super::{Id, SpannedNodes};
use spoiler::Spoiler;

pub mod bold;
pub mod italic;
pub mod spoiler;
pub mod strikethrough;
pub mod underline;

/// The kinds of modifier, one per [`crate::rule::MODIFIER_RULES`] member. Each has its own
/// [`Modifier`] variant; see [`Modifier::kind`].
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

	/// Unparse `content` wrapped in this kind's delimiters.
	///
	/// # Errors
	/// If formatting fails
	pub fn unparse<S: Span>(
		self,
		content: &SpannedNodes<S>,
		f: &mut std::fmt::Formatter,
	) -> std::fmt::Result {
		match self {
			Self::Bold => bold::unparse(content, f),
			Self::Italic => italic::unparse(content, f),
			Self::Underline => underline::unparse(content, f),
			Self::Strikethrough => strikethrough::unparse(content, f),
			Self::Spoiler => spoiler::unparse(content, f),
		}
	}
}

/// Markup that wraps content without being inline or block itself: inline content where it opened
/// mid-line, block content where it opened at the start of a line. See [`crate::range`].
#[derive_where(Debug, Clone, PartialEq, Eq)]
#[cfg_attr(
	feature = "serde",
	derive(serde::Serialize, serde::Deserialize),
	serde(tag = "type", content = "value", rename_all = "snake_case", bound = "")
)]
pub enum Modifier<'data, S: Span> {
	Bold(SpannedNodes<'data, S>),
	Italic(SpannedNodes<'data, S>),
	Underline(SpannedNodes<'data, S>),
	Strikethrough(SpannedNodes<'data, S>),
	Spoiler(Spoiler<'data, S>),
}

impl<'data, S: Span> Modifier<'data, S> {
	/// The modifier of `kind` wrapping `content`.
	#[must_use]
	pub fn new(kind: ModifierKind, content: SpannedNodes<'data, S>) -> Self {
		match kind {
			ModifierKind::Bold => Self::Bold(content),
			ModifierKind::Italic => Self::Italic(content),
			ModifierKind::Underline => Self::Underline(content),
			ModifierKind::Strikethrough => Self::Strikethrough(content),
			// numbered by `crate::range::resolve`
			ModifierKind::Spoiler => Self::Spoiler(Spoiler {
				id: Id::default(),
				content,
			}),
		}
	}

	#[must_use]
	pub fn kind(&self) -> ModifierKind {
		match self {
			Self::Bold(_) => ModifierKind::Bold,
			Self::Italic(_) => ModifierKind::Italic,
			Self::Underline(_) => ModifierKind::Underline,
			Self::Strikethrough(_) => ModifierKind::Strikethrough,
			Self::Spoiler(_) => ModifierKind::Spoiler,
		}
	}

	#[must_use]
	pub fn content(&self) -> &SpannedNodes<'data, S> {
		match self {
			Self::Bold(content)
			| Self::Italic(content)
			| Self::Underline(content)
			| Self::Strikethrough(content)
			| Self::Spoiler(Spoiler { content, .. }) => content,
		}
	}

	pub fn content_mut(&mut self) -> &mut SpannedNodes<'data, S> {
		match self {
			Self::Bold(content)
			| Self::Italic(content)
			| Self::Underline(content)
			| Self::Strikethrough(content)
			| Self::Spoiler(Spoiler { content, .. }) => content,
		}
	}
}

impl<S: Span> Unparse for Modifier<'_, S> {
	fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
		self.kind().unparse(self.content(), f)
	}
}
