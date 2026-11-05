use std::{fmt::Debug, sync::LazyLock};

use enumset::{EnumSet, EnumSetType, enum_set};

use crate::error::{Fail, PResult};

use super::{
	Input,
	node::{block::quote, inline::link},
	syntax::{Syntax, SyntaxSet},
	util::ByteSet,
};

/// The scopes that require a prefix at the start of each of their lines.
pub const LINE_PREFIX_SCOPES: ScopeSet = enum_set!(Scope::Quote);

/// A region of input that a parser has entered, which shapes how the parsers inside it behave.
///
/// This is what enables non-greedy parsing such that a terminal for a parent scope will terminate
/// the parent rather than beginning a new node.
///
/// This also enables global terminals which act as an unconditional terminal sequence for any
/// inline parser, and lets a scope disable syntax inside it.
///
/// Scopes are internal; what a caller enables is [`Syntax`].
#[derive(Debug, EnumSetType)]
pub enum Scope {
	/// Base scope that fails all parsing.
	None,
	/// Top level scope that covers all block content.
	Block,
	// TODO: is this still necessary
	InlineBlock,
	/// The content of a [`Syntax::Quote`].
	Quote,
	/// The content of a [`Syntax::MultilineQuote`].
	QuoteRest,
	/// The URL of an auto link or contact link, with delimiters `<` and `>`.
	AutoLink,
	/// The text portion of masked links, with delimiters `[` and `]`
	MaskedLinkText,
	/// The URL portion of masked links, with delimiters `(` and `)`
	MaskedLinkLink,
}

/// What ends a [`Scope`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Terminal {
	/// Nothing: the scope runs to the end of its parent.
	None,
	/// A line ending, or the end of the input.
	LineEnd,
	/// This byte.
	Byte(u8),
}

impl Scope {
	/// Whether this scope terminates every parser inside it at `input`, not only its own.
	///
	/// This differs from [`Scope::ends_at`] only for [`Scope::InlineBlock`]: a paragraph ends at a
	/// line ending, but does not force the syntax inside it to.
	// TODO: investigate if we can consolidate everything to a global terminal somehow
	#[must_use]
	pub fn ends_everything_at(self, input: &Input) -> bool {
		self != Self::InlineBlock && self.ends_at(input)
	}

	/// Whether this scope's terminal sequence begins `input`.
	#[must_use]
	pub fn ends_at(self, input: &Input) -> bool {
		let mut lookahead = *input;
		self.terminal_sequence(&mut lookahead).is_ok()
	}

	/// What ends this scope.
	#[must_use]
	pub fn terminal(self) -> Terminal {
		match self {
			Self::None | Self::QuoteRest => Terminal::None,
			Self::InlineBlock | Self::Block | Self::Quote => Terminal::LineEnd,
			Self::AutoLink => Terminal::Byte(link::auto::TERMINAL),
			Self::MaskedLinkText => Terminal::Byte(link::masked::TEXT_TERMINAL),
			Self::MaskedLinkLink => Terminal::Byte(link::masked::LINK_TERMINAL),
		}
	}

	/// Consume whatever denotes the end of the scope.
	///
	/// # Errors
	/// If the input does not begin with it.
	pub fn terminal_sequence(self, input: &mut Input) -> PResult<()> {
		match self.terminal() {
			Terminal::None => Err(Fail::NoMatch),
			Terminal::LineEnd => input.line_ending_or_eof().map(|_| ()),
			Terminal::Byte(byte) => input.byte(byte),
		}
	}

	/// Add every byte that can begin [`Self::terminal_sequence`], or the opener of this scope's
	/// [`Self::bracket_delimiters`], to `bytes`. The end of the input is a terminal too, but has no
	/// byte.
	pub fn insert_boundary_bytes(self, bytes: &mut ByteSet) {
		match self.terminal() {
			Terminal::None => {}
			Terminal::LineEnd => bytes.extend(*b"\n\r"),
			Terminal::Byte(byte) => bytes.insert(byte),
		}
		bytes.extend(self.bracket_delimiters().map(|(open, _)| open));
	}

	/// Whether `byte` is one that [`Self::insert_boundary_bytes`] adds for any scope.
	#[must_use]
	pub fn is_boundary_byte(byte: u8) -> bool {
		static BOUNDARIES: LazyLock<ByteSet> = LazyLock::new(|| {
			let mut bytes = ByteSet::default();
			for scope in ScopeSet::all() {
				scope.insert_boundary_bytes(&mut bytes);
			}
			bytes
		});

		BOUNDARIES.contains(byte)
	}

	/// Consume the prefix this scope requires at the start of each of its lines. Scopes that are
	/// not containers consume nothing.
	///
	/// # Errors
	/// If the input does not begin with the prefix.
	pub fn line_prefix<'data>(self, input: &mut Input<'data>) -> PResult<&'data str> {
		match self {
			// `>` plus exactly one space on a content line, or a bare `>` on an otherwise empty
			// line. The latter leaves the line ending for the block loop to turn into an
			// `Element::Empty`.
			//
			// Only one space belongs to the prefix: the rest is content, and multi-line block rules
			// need it to measure their own indentation. Consuming it greedily would flatten
			// `>   - bar` onto column zero, which would flatten lists.
			Self::Quote => input.recognize(|input| {
				input.char(quote::LINE_PREFIX)?;
				if !input.at_line_end() {
					input.satisfy(|ch| matches!(ch, ' ' | '\t'))?;
				}
				Ok(())
			}),
			scope => {
				debug_assert!(!LINE_PREFIX_SCOPES.contains(scope));
				Ok("")
			}
		}
	}

	/// Whether this scope is a container that requires a prefix at the start of each of its
	/// lines. See [`LINE_PREFIX_SCOPES`].
	#[must_use]
	pub fn has_line_prefix(self) -> bool {
		LINE_PREFIX_SCOPES.contains(self)
	}

	/// For scopes that delimit a region with balanced bracket-like pairs, returns the open
	/// and close bytes. Used by [`crate::Context::matched_pairs`] to efficiently find the
	/// matching close without running the full inner parser.
	#[must_use]
	pub fn bracket_delimiters(&self) -> Option<(u8, u8)> {
		match self {
			Self::MaskedLinkText => Some((link::masked::TEXT_OPENER, link::masked::TEXT_TERMINAL)),
			_ => None,
		}
	}

	/// Syntax which cannot appear inside this scope.
	#[must_use]
	pub fn disabled_syntaxes(&self) -> SyntaxSet {
		match self {
			Self::MaskedLinkText => link::masked::DISABLED_MASKED_LINK_SYNTAXES,
			// a quote cannot nest, whichever way either is written
			Self::Quote | Self::QuoteRest => Syntax::QUOTES,
			// most scopes don't disable any syntax inside them
			_ => SyntaxSet::empty(),
		}
	}
}

/// A set of scopes.
pub type ScopeSet = EnumSet<Scope>;

#[cfg(test)]
mod test {
	use enumset::enum_set;

	use super::{LINE_PREFIX_SCOPES, Scope};

	#[test]
	fn set_consistency() {
		assert_eq!(
			enum_set!(Scope::Quote),
			LINE_PREFIX_SCOPES,
			"if this test fails, update either the set or the logic"
		);
	}
}
