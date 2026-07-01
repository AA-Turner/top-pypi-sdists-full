use std::{fmt::Debug, marker::PhantomData};

use enumset::{EnumSet, EnumSetType};
use global_terminal_sequence::{GlobalTerminalSequence, GlobalTerminalSequenceSet};
use memchr::{memchr, memmem::find};
use nom::Parser;
use override_terminal_sequence::OverrideTerminalSequence;
use start_sequence::StartSequence;
use terminal_sequence::TerminalSequence;
use variant_struct::VariantStruct;

use crate::error::ParseError;

use super::{
	inline::{link, spoiler},
	rule::{Rule, RuleSet},
	Input,
};

/// A precomputed hint about whether a grammar's necessary bytes are present in the remaining
/// input. Used to skip O(N) inner-parse work when the grammar cannot possibly match.
///
/// Set once per top-level [`crate::inline::InlineParser`] call via
/// [`Grammar::precheck_hint`] and propagated to child contexts so the scan is amortized.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub enum ByteHint {
	/// Not yet computed — the hint must be derived before use.
	#[default]
	Unknown,
	/// This grammar requires no precheck; always attempt it normally.
	NotApplicable,
	/// The necessary bytes are absent; the grammar cannot match at any position.
	Absent,
	/// The necessary bytes are present; the first occurrence is at this absolute byte offset.
	Present(usize),
}

mod global_terminal_sequence;
mod override_terminal_sequence;
mod start_sequence;
mod terminal_sequence;

/// Defines behavior of child parsers based on the current rule.
///
/// This is what enables non-greedy parsing such that a terminal for a parent rule will terminate
/// the parent rather than beginning a new node.
///
/// This also enables global terminals which act as an unconditional terminal sequence for any
/// inline rule.
// NOTE: when adding a grammar here, make sure to update Rule::grammar as well
#[derive(Debug, EnumSetType, VariantStruct)]
pub enum Grammar {
	/// Base grammar that fails all parsing.
	None,
	/// Top level grammar that covers all block content.
	Block,
	// TODO: is this still necessary
	InlineBlock,
	Quote,
	/// Bold, with delimiter `**`
	Bold,
	/// Underscore italic, with delimitier `_`
	UnderscoreItalic,
	/// Asterisk italic, with delimiter `*`
	AsteriskItalic,
	/// Spoiler, with delimiter `||`
	Spoiler,
	/// Strikethrough, with delimiter `~~`
	Strikethrough,
	/// Underline, with delimiter `__`
	Underline,
	/// Auto link, with delimiters `<` and `>`.
	AutoLink,
	/// The text portion of masked links, with delimiters `[` and `]`
	MaskedLinkText,
	/// The URL portion of masked links, with delimiters `(` and `)`
	MaskedLinkLink,
	/// Inline code, with delimiter \`
	Code,
	/// Code block content, with delimiter \`\`\`
	CodeBlock,
	/// Timestamp content, with delimiters `<` and `>`
	Timestamp,
	/// Custom emoji content, with delimiters `<` and `>`
	CustomEmoji,
	/// Colon-delimited emoji content, e.g. :smile:
	ColonDelimitedEmoji,
	/// Find links in content, starting with valid URL schemes.
	LinkDetection,
	/// An `@everyone` mention, matching this string exactly
	EveryoneMention,
	/// A `@here` mention, matching this string exactly
	HereMention,
	/// User mention, with delimiters `<@` and `>`
	UserMention,
	/// Channel mention, with delimiters `<#` and `>`
	ChannelMention,
	/// Rule mention, with delimiters `<@&` and `>`
	RoleMention,
	/// Command mention, with delimiters `</` and `>`
	CommandMention,
}

impl Grammar {
	/// Get the terminal character for this grammar, upon which any child rules should immediately
	/// yield back to the parent parser. The parent should attempt to consume this character before
	/// yielding to its parent.
	///
	/// This is distinct from [`Grammar::terminal_sequence`] in that this applies to _any_ child
	/// parser, whereas the former method only applies to the current rule context. Practically this
	/// means that [`Grammar::terminal_sequence`] serves to terminate a rule only when no other rules
	/// have started.
	///
	/// This behavior is entirely useful in the context of [`super::node::Node::Paragraph`] nodes
	/// which terminate on newline but do not force children to terminate on newline. No other rules
	/// rely on this behavior; the vast majority of grammars should match
	/// [`Grammar::terminal_sequence`] with this value.
	///
	/// The default behavior falls back to [`Grammar::terminal_sequence`], which most grammars should
	/// leave as-is.
	// TODO: investigate if we can consolidate everything to a global terminal somehow
	#[must_use]
	pub fn global_terminal_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		GlobalTerminalSequence(self, PhantomData)
	}

	/// Override the [`Grammar::terminal_sequence`] in case there are specific supersets of the
	/// terminal sequence where parsing should continue.
	///
	/// Does nothing by default.
	#[must_use]
	pub fn override_terminal_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		OverrideTerminalSequence(self, PhantomData::<E>)
	}

	/// Define the terminal sequence of the grammar. This is a parser that matches whatever
	/// denotes the start of the grammar.
	#[must_use]
	pub fn start_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		StartSequence(self, PhantomData)
	}

	/// Define the terminal sequence of the grammar. This is a parser that matches whatever
	/// denotes the end of the grammar.
	#[must_use]
	pub fn terminal_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		TerminalSequence(self, PhantomData)
	}

	/// For grammars that delimit a region with balanced bracket-like pairs, returns the open
	/// and close strings. Used by [`crate::context::matched_pairs`] to efficiently find the
	/// matching close without running the full inner parser.
	#[must_use]
	pub fn bracket_delimiters(&self) -> Option<(u8, u8)> {
		match self {
			Self::MaskedLinkText => Some((link::masked::TEXT_OPENER, link::masked::TEXT_TERMINAL)),
			_ => None,
		}
	}

	/// Rules which cannot appear as children of this grammar.
	#[must_use]
	pub fn disabled_rules(&self) -> RuleSet {
		match self {
			Self::Spoiler => spoiler::DISABLED_RULES,
			Self::MaskedLinkText => link::masked::DISABLED_MASKED_LINK_RULES,
			Self::Quote => Rule::Quote.into(),
			// most grammars don't disable any rules as children
			_ => RuleSet::empty(),
		}
	}

	/// Compute a precheck hint for this grammar given the remaining input.
	///
	/// Returns [`ByteHint::NotApplicable`] for grammars that already fail in O(1) and need no
	/// precheck. Returns [`ByteHint::Absent`] or [`ByteHint::Present`] for grammars whose inner
	/// parser would do O(N) work before failing on adversarial input.
	///
	/// Every grammar returns a non-[`ByteHint::Unknown`] value so that [`crate::context::GrammarHints`]
	/// can detect when all hints are populated and short-circuit future calls.
	#[must_use]
	pub fn precheck_hint(self, input: &Input) -> ByteHint {
		let bytes = input.as_bytes();

		match self {
			Self::MaskedLinkText => match find(bytes, link::masked::TEXT_LINK_DIVIDER) {
				None => ByteHint::Absent,
				Some(pos) => {
					if memchr(
						link::masked::LINK_TERMINAL,
						&bytes[pos + link::masked::TEXT_LINK_DIVIDER.len()..],
					)
					.is_some()
					{
						ByteHint::Present(input.start + pos)
					} else {
						ByteHint::Absent
					}
				}
			},
			Self::AutoLink
			| Self::UserMention
			| Self::ChannelMention
			| Self::RoleMention
			| Self::CommandMention
			| Self::Timestamp
			| Self::CustomEmoji => match memchr(b'>', bytes) {
				None => ByteHint::Absent,
				Some(pos) => ByteHint::Present(input.start + pos),
			},
			_ => ByteHint::NotApplicable,
		}
	}
}

/// A set of grammars.
pub type GrammarSet = EnumSet<Grammar>;

/// Parse global terminals.
#[must_use]
pub fn global_terminals<'data, E>(
	set: GrammarSet,
) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	GlobalTerminalSequenceSet(set, PhantomData)
}
