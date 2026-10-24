use std::{fmt::Debug, marker::PhantomData};

use enumset::{EnumSet, EnumSetType};
use global_terminal_sequence::{GlobalTerminalSequence, GlobalTerminalSequenceSet};
use nom::Parser;
use terminal_sequence::TerminalSequence;

use crate::{
	error::ParseError,
	scope::line_prefix::{LINE_PREFIX_SCOPES, LinePrefix},
};

use super::{
	Input,
	node::inline::link,
	syntax::{Syntax, SyntaxSet},
};

mod global_terminal_sequence;
mod line_prefix;
mod terminal_sequence;

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

impl Scope {
	/// Get the terminal character for this scope, upon which any child parsers should immediately
	/// yield back to the parent parser. The parent should attempt to consume this character before
	/// yielding to its parent.
	///
	/// This is distinct from [`Scope::terminal_sequence`] in that this applies to _any_ child
	/// parser, whereas the former method only applies to the current scope. Practically this
	/// means that [`Scope::terminal_sequence`] serves to terminate a scope only when no other
	/// syntax has started.
	///
	/// This behavior is entirely useful in the context of [`super::node::Element::Paragraph`] nodes
	/// which terminate on newline but do not force children to terminate on newline. No other scopes
	/// rely on this behavior; the vast majority of scopes should match
	/// [`Scope::terminal_sequence`] with this value.
	///
	/// The default behavior falls back to [`Scope::terminal_sequence`], which most scopes should
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

	/// Define the terminal sequence of the scope. This is a parser that matches whatever
	/// denotes the end of the scope.
	#[must_use]
	pub fn terminal_sequence<'data, E>(
		self,
	) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
	where
		E: ParseError<'data>,
	{
		TerminalSequence(self, PhantomData)
	}

	/// The prefix this scope requires at the start of each of its lines. Scopes that are not
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

/// Parse global terminals.
#[must_use]
pub fn global_terminals<'data, E>(
	set: ScopeSet,
) -> impl Parser<Input<'data>, Output = Input<'data>, Error = E>
where
	E: ParseError<'data>,
{
	GlobalTerminalSequenceSet(set, PhantomData)
}
