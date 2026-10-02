use std::{fmt::Debug, marker::PhantomData};

use enumset::{EnumSet, EnumSetType};
use global_terminal_sequence::{GlobalTerminalSequence, GlobalTerminalSequenceSet};
use memchr::{memchr, memmem::find};
use nom::Parser;
use start_sequence::StartSequence;
use terminal_sequence::TerminalSequence;
use variant_struct::VariantStruct;

use crate::{
	error::ParseError,
	grammar::line_prefix::{LinePrefix, LINE_PREFIX_GRAMMARS},
};

use super::{
	inline::{link, spoiler},
	rule::{Rule, RuleSet},
	Input,
};

/// A precomputed hint about whether a grammar's necessary bytes are present in the remaining
/// input. Used to skip O(N) inner-parse work when the grammar cannot possibly match.
///
/// Set once per top-level [`crate::inline::inline`] call via
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
mod line_prefix;
mod override_start_sequence;
mod override_terminal_sequence;

pub use override_start_sequence::GRAMMARS as OVERRIDE_START_GRAMMARS;
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
	/// Quote, with `>>>` marking the rest of the content as quote
	QuoteRest,
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
	/// [`None`] for the majority of grammars, which define no override.
	#[must_use]
	pub fn override_terminal_sequence<'data, E>(
		self,
	) -> Option<impl Parser<Input<'data>, Output = Input<'data>, Error = E>>
	where
		E: ParseError<'data>,
	{
		override_terminal_sequence::parser(self)
	}

	/// Override the [`Grammar::start_sequence`] in case there are specific supersets of the start
	/// sequence which should be treated as literal text rather than opening the grammar.
	///
	/// Unlike [`Grammar::override_terminal_sequence`], which is consulted for the grammar currently
	/// being parsed, this is consulted for every grammar whose start sequence could fire here; see
	/// [`crate::Context::override_start_sequences`].
	///
	/// [`None`] for the majority of grammars, which define no override.
	#[must_use]
	pub fn override_start_sequence<'data, E>(
		self,
	) -> Option<impl Parser<Input<'data>, Output = Input<'data>, Error = E>>
	where
		E: ParseError<'data>,
	{
		override_start_sequence::parser(self)
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

	/// The prefix this grammar requires at the start of each of its lines. Grammars that are not
	/// containers match the empty string; see [`LinePrefix`].
	#[must_use]
	pub fn line_prefix<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		LinePrefix(self, PhantomData)
	}

	/// Whether this grammar is a container that requires a prefix at the start of each of its
	/// lines. See [`LINE_PREFIX_GRAMMARS`].
	#[must_use]
	pub fn has_line_prefix(self) -> bool {
		LINE_PREFIX_GRAMMARS.contains(self)
	}

	/// For grammars that delimit a region with balanced bracket-like pairs, returns the open
	/// and close strings. Used by [`crate::Context::matched_pairs`] to efficiently find the
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
			Self::Quote | Self::QuoteRest => Rule::Quote.into(),
			// most grammars don't disable any rules as children
			_ => RuleSet::empty(),
		}
	}

	/// Rules whose start sequence begins with, and is longer than, this grammar's terminal
	/// sequence.
	///
	/// The `*` that opens a `**` bold is not an asterisk italic's closer, but
	/// [`Self::terminal_sequence`] cannot tell the two apart -- it matches a bare `*`. Left alone
	/// the italic closes on the bold's opener, the second asterisk opens a second italic, and the
	/// bold is destroyed. [`crate::Context::guard_terminal_sequence`] consults this so the terminal
	/// can yield to the longer delimiter when one of these rules actually parses here.
	///
	/// Empty for the majority of grammars. `Code` and `CodeBlock` overlap the same way but are
	/// deliberately absent: their content is raw, so no child parser runs inside them and no
	/// terminal guard ever has to make this choice.
	#[must_use]
	pub fn overlapping_rules(self) -> RuleSet {
		match self {
			Self::AsteriskItalic => Rule::Bold.into(),
			Self::UnderscoreItalic => Rule::Underline.into(),
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

#[cfg(test)]
mod test {
	use super::{Grammar, GrammarSet};
	use crate::inline::{bold, italic, underline};

	/// Callers reach for [`Grammar::overlapping_rules`] once per character and short-circuit on an
	/// empty set, so pin exactly which grammars have one.
	#[test]
	fn only_the_italics_have_overlapping_rules() {
		let with_overlap = GrammarSet::all()
			.iter()
			.filter(|grammar| !grammar.overlapping_rules().is_empty())
			.collect::<GrammarSet>();

		assert_eq!(
			with_overlap,
			Grammar::AsteriskItalic | Grammar::UnderscoreItalic
		);
	}

	/// ...and pin the delimiter relationship that mapping encodes, so that moving a delimiter
	/// fails here rather than silently reinstating the bug the mapping exists to fix: an italic
	/// closing on the first half of the sequence that opens the longer rule.
	#[test]
	fn overlapping_rules_track_the_delimiters() {
		for (terminal, opener) in [
			(italic::ASTERISK_DELIMITER, bold::DELIMITER),
			(italic::UNDERSCORE_DELIMITER, underline::DELIMITER),
		] {
			assert!(
				opener.starts_with(terminal) && opener.len() > terminal.len(),
				"{opener:?} is no longer a strict extension of {terminal:?}"
			);
		}
	}
}
