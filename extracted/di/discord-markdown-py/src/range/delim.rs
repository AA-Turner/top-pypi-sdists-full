//! Delimiter runs, recorded while parsing and paired by [`super::resolve`].

use std::{fmt::Debug, marker::PhantomData};

use nom::{Emit, Err, Input as _, Mode, OutputM, OutputMode, PResult, Parser, error::ErrorKind};
use variant_struct::VariantStruct;

use crate::{
	Input,
	error::ParseError,
	node::modifier::ModifierKind,
	rule::{Rule, RuleSet},
};

/// A byte offset in the input.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub struct Offset(usize);

/// A character whose runs delimit modifiers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, VariantStruct)]
pub enum DelimChar {
	Asterisk,
	Underscore,
	Tilde,
	Pipe,
}

impl DelimChar {
	#[must_use]
	pub const fn from_char(ch: char) -> Option<Self> {
		Some(match ch {
			'*' => Self::Asterisk,
			'_' => Self::Underscore,
			'~' => Self::Tilde,
			'|' => Self::Pipe,
			_ => return None,
		})
	}

	#[must_use]
	pub const fn char(self) -> char {
		match self {
			Self::Asterisk => '*',
			Self::Underscore => '_',
			Self::Tilde => '~',
			Self::Pipe => '|',
		}
	}

	/// The kinds its runs can delimit.
	#[must_use]
	pub const fn kinds(self) -> &'static [ModifierKind] {
		match self {
			Self::Asterisk => &[ModifierKind::Bold, ModifierKind::Italic],
			Self::Underscore => &[ModifierKind::Underline, ModifierKind::Italic],
			Self::Tilde => &[ModifierKind::Strikethrough],
			Self::Pipe => &[ModifierKind::Spoiler],
		}
	}

	/// The shortest run that is a delimiter: a lone `~` or `|` is text.
	#[must_use]
	pub fn min_len(self) -> usize {
		self.kinds()
			.iter()
			.map(|kind| kind.delimiter_len())
			.min()
			.unwrap_or(1)
	}

	/// Whether any of its kinds is allowed.
	#[must_use]
	pub fn allowed(self, allowed: RuleSet) -> bool {
		self.kinds()
			.iter()
			.any(|kind| allowed.contains(kind.rule()))
	}

	/// What a run of `len` between `prev` and `next` can do.
	#[must_use]
	pub fn flanking(
		self,
		len: usize,
		prev: Neighbor,
		next: Neighbor,
		spoiler: SpoilerState,
	) -> Flanking {
		match self {
			// `1 * 2 * 3` is not italic, but `** foo**` and `**foo **` are bold
			Self::Asterisk => Flanking {
				opens: len >= 2 || !next.is_whitespace(),
				closes: true,
			},
			// `snake_case` holds no delimiter, and `Endemic_(` cannot open one
			Self::Underscore => {
				let after_word = prev.is_word();
				let intraword = after_word && next.is_word();
				Flanking {
					opens: !(intraword || after_word && next == Neighbor::Char('(')),
					closes: !intraword,
				}
			}
			// a spoiler cannot hold a spoiler, so inside one `||` can only close it
			Self::Pipe => Flanking {
				opens: spoiler == SpoilerState::Closed,
				closes: true,
			},
			Self::Tilde => Flanking {
				opens: true,
				closes: true,
			},
		}
	}

	/// Whether a run of `remaining` that could open does so, rather than closing an opener with
	/// `opener` left. `later` is the longest run after it that could close.
	#[must_use]
	pub fn opens_instead(self, remaining: usize, opener: usize, later: usize) -> bool {
		if !self.kinds().contains(&ModifierKind::Italic) {
			return false;
		}
		// a lone `*` does not close a `**`, so `**a *b* c**` holds an italic -- though it closes
		// the italic half of a `***` -- or, with nothing later to close it, `__a_`
		let shorter = remaining < opener
			&& !remaining.is_multiple_of(2)
			&& opener.is_multiple_of(2)
			&& later >= remaining;
		// and a `**` that something later can close opens a bold, so `*a **b** c*` holds one: an
		// italic yields to a bold
		let longer = remaining > opener && later >= remaining;
		shorter || longer
	}

	/// The kind of range a pair of runs spends on. [`None`] if they cannot pair.
	#[must_use]
	pub fn spend(self, remaining: usize, opener: usize, allowed: RuleSet) -> Option<ModifierKind> {
		let both = remaining.min(opener);
		// `***foo***` is a bold around an italic, so an odd pair of runs spends one first
		let odd = !remaining.is_multiple_of(2) && !opener.is_multiple_of(2);
		Some(match self {
			Self::Asterisk if both >= 2 && !odd && allowed.contains(Rule::Bold) => {
				ModifierKind::Bold
			}
			Self::Underscore if both >= 2 && allowed.contains(Rule::Underline) => {
				ModifierKind::Underline
			}
			Self::Asterisk | Self::Underscore if allowed.contains(Rule::Italic) => {
				ModifierKind::Italic
			}
			Self::Tilde if both >= 2 => ModifierKind::Strikethrough,
			Self::Pipe if both >= 2 => ModifierKind::Spoiler,
			_ => return None,
		})
	}
}

/// Whether a spoiler is open where a delimiter run sits.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SpoilerState {
	Open,
	Closed,
}

/// Whether a delimiter run can open a range and whether it can close one.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Flanking {
	pub opens: bool,
	pub closes: bool,
}

/// What sits beside a delimiter run.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Neighbor {
	Char(char),
	/// An atom, like a mention: neither a word character nor whitespace.
	Atom,
}

impl Neighbor {
	pub const LINE_END: Self = Self::Char('\n');

	#[must_use]
	pub fn is_whitespace(self) -> bool {
		matches!(self, Self::Char(ch) if ch.is_whitespace())
	}

	#[must_use]
	pub fn is_word(self) -> bool {
		matches!(self, Self::Char(ch) if ch.is_alphanumeric())
	}
}

/// A run of one modifier delimiter character, recorded while parsing and consumed by
/// [`super::resolve`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Delim {
	pub ch: DelimChar,
	pub len: usize,
	pub start: Offset,
	/// Whether block syntax was recognized after it on the same line, as in `*1. foo`.
	pub before_block: bool,
	/// Whether it is alone on its line, like the `||` around a spoiled list.
	pub alone: bool,
}

/// The allowed delimiter character `text` begins with.
fn first(text: &str, allowed: RuleSet) -> Option<DelimChar> {
	text.chars()
		.next()
		.and_then(DelimChar::from_char)
		.filter(|ch| ch.allowed(allowed))
}

/// Whether a delimiter run that [`delim`] would read begins `text`. Text stops here.
#[must_use]
pub fn starts_delimiter(text: &str, allowed: RuleSet) -> bool {
	first(text, allowed).is_some_and(|ch| {
		let run = text.chars().take_while(|&next| next == ch.char());
		run.take(ch.min_len()).count() == ch.min_len()
	})
}

pub struct DelimParser<E> {
	allowed: RuleSet,
	error: PhantomData<E>,
}

impl<E> Debug for DelimParser<E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("DelimParser")
			.field("allowed", &self.allowed)
			.field("error", &self.error)
			.finish()
	}
}

impl<'data, E> Parser<Input<'data>> for DelimParser<E>
where
	E: ParseError<'data>,
{
	type Output = Delim;
	type Error = E;

	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let Some(ch) = first(&input, self.allowed) else {
			return Err(Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Char)
			})));
		};
		let len = input.chars().take_while(|&next| next == ch.char()).count();
		if len < ch.min_len() {
			return Err(Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Char)
			})));
		}
		let start = Offset(input.start);
		let (rest, _) = input.take_split(len * ch.char().len_utf8());
		Ok((
			rest,
			OM::Output::bind(|| Delim {
				ch,
				len,
				start,
				before_block: false,
				alone: false,
			}),
		))
	}
}

/// Parse a run of one delimiter character.
///
/// # Errors
/// If the input does not begin with an allowed delimiter.
#[must_use]
pub fn delim<'data, E>(allowed: RuleSet) -> impl Parser<Input<'data>, Output = Delim, Error = E>
where
	E: ParseError<'data>,
{
	DelimParser {
		allowed,
		error: PhantomData,
	}
}

pub struct OpenerParser<F, E> {
	delim: DelimParser<E>,
	disabled: F,
}

impl<F, E> Debug for OpenerParser<F, E> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		f.debug_struct("OpenerParser")
			.field("delim", &self.delim)
			.finish_non_exhaustive()
	}
}

impl<'data, F, E> Parser<Input<'data>> for OpenerParser<F, E>
where
	F: Fn(Offset) -> bool,
	E: ParseError<'data>,
{
	type Output = Delim;
	type Error = E;

	fn process<OM: OutputMode>(
		&mut self,
		input: Input<'data>,
	) -> PResult<OM, Input<'data>, Self::Output, Self::Error> {
		let (rest, delim) = self
			.delim
			.process::<OutputM<Emit, OM::Error, OM::Incomplete>>(input.clone())?;
		if rest.chars().next().is_none_or(char::is_whitespace) {
			return Err(Err::Error(OM::Error::bind(|| {
				E::from_error_kind(rest, ErrorKind::Satisfy)
			})));
		}
		let closable = rest.contains(&delim.ch.char().to_string().repeat(delim.ch.min_len()));
		if (self.disabled)(delim.start) || !closable {
			return Err(Err::Error(OM::Error::bind(|| {
				E::from_error_kind(input, ErrorKind::Verify)
			})));
		}
		Ok((
			rest,
			OM::Output::bind(|| Delim {
				before_block: true,
				..delim
			}),
		))
	}
}

/// Parse a run of delimiters opening block syntax on the same line, as `*` does in `*1. foo`. It
/// must be followed by a non-space, so `* foo` stays a list bullet, and must not start at an
/// offset `disabled` rules out: an opener that went unmatched last time, whose line is a paragraph.
///
/// An opener whose delimiter never appears again cannot be matched, so it is refused outright
/// rather than costing [`super::resolve`] a round to find that out.
///
/// # Errors
/// If the input does not begin with such a run.
#[must_use]
pub fn opener<'data, E>(
	allowed: RuleSet,
	disabled: impl Fn(Offset) -> bool,
) -> impl Parser<Input<'data>, Output = Delim, Error = E>
where
	E: ParseError<'data>,
{
	OpenerParser {
		delim: DelimParser {
			allowed,
			error: PhantomData,
		},
		disabled,
	}
}
