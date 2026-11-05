use std::{
	fmt::{Debug, Display},
	ops::Deref,
};

use memchr::memmem::find;

use crate::{
	context::fuel::OutOfFuel,
	error::{Fail, PResult},
	lossless::TokenKind,
	span::{Span, Spanned, Syntax},
};

/// A cursor over the text being parsed.
///
/// Parsers take it by `&mut` and advance it as they consume. A parser that fails may leave it
/// anywhere: whoever tries an alternative after a failure restores it, which [`Self::attempt`]
/// does.
///
/// Comparison and ordering look only at [`Self::content`] and [`Self::start`]: [`Self::source`] is
/// the same string for every input derived from one parse, so including it would only ever add work.
#[derive(Debug, Clone, Copy)]
pub struct Input<'data> {
	/// The text content to be parsed.
	pub content: &'data str,
	/// Offset from the original string. `0` if this is the entire content.
	pub start: usize,
	/// The whole string this input was derived from, retained so a parser can look at what precedes
	/// its own position. [`Self::content`] is a suffix of this starting at [`Self::start`].
	///
	/// Link detection needs it: a schemaless host is only a link when it begins a token, and nothing
	/// else tells a parser whether it sits mid-word (see
	/// [`crate::node::inline::link::detection::at_token_start`]).
	source: &'data str,
}

impl PartialEq for Input<'_> {
	fn eq(&self, other: &Self) -> bool {
		self.content == other.content && self.start == other.start
	}
}

impl Eq for Input<'_> {}

impl PartialOrd for Input<'_> {
	fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
		Some(self.cmp(other))
	}
}

impl Ord for Input<'_> {
	fn cmp(&self, other: &Self) -> std::cmp::Ordering {
		self.content
			.cmp(other.content)
			.then_with(|| self.start.cmp(&other.start))
	}
}

impl<'data> Input<'data> {
	/// Create a new [`Span`] from `start` to [`Self::start`].
	#[must_use]
	pub fn span<S>(&self, start: usize) -> S
	where
		S: Span,
	{
		S::new(start, self.start)
	}

	/// The character immediately before this input's position, or [`None`] at the start of the parse.
	///
	/// It is typically bad practice to rely on previous input, since parsers should only look
	/// forward. If a parser needs to consider something "previous", then that previous token should
	/// be implemented as part of the parser itself rather than as a look back. This method is
	/// implemented for compatibility with coded links, but should not be used for new functionality.
	#[must_use]
	#[deprecated = "parsers that need the previous char should include that char directly"]
	pub fn preceding_char(&self) -> Option<char> {
		self.source[..self.start].chars().next_back()
	}

	/// The next character, without consuming it.
	#[must_use]
	pub fn peek(&self) -> Option<char> {
		self.content.chars().next()
	}

	/// Consume `len` bytes, returning them.
	///
	/// # Panics
	/// If `len` is past the end or not on a character boundary.
	pub fn advance(&mut self, len: usize) -> &'data str {
		let (taken, rest) = self.content.split_at(len);
		self.content = rest;
		self.start += len;
		taken
	}

	/// Consume the rest of the input.
	pub fn rest(&mut self) -> &'data str {
		self.advance(self.content.len())
	}

	/// Consume any one character.
	///
	/// # Errors
	/// At the end of the input.
	pub fn any_char(&mut self) -> PResult<char> {
		self.satisfy(|_| true)
	}

	/// Consume the next character if `predicate` accepts it.
	///
	/// # Errors
	/// If it does not, or at the end of the input.
	pub fn satisfy(&mut self, predicate: impl FnOnce(char) -> bool) -> PResult<char> {
		match self.peek() {
			Some(ch) if predicate(ch) => {
				self.advance(ch.len_utf8());
				Ok(ch)
			}
			_ => Err(Fail::NoMatch),
		}
	}

	/// Consume `ch`.
	///
	/// # Errors
	/// If the input does not begin with it.
	pub fn char(&mut self, ch: char) -> PResult<char> {
		self.satisfy(|next| next == ch)
	}

	/// Consume the ASCII byte `byte`.
	///
	/// # Errors
	/// If the input does not begin with it.
	pub fn byte(&mut self, byte: u8) -> PResult<()> {
		debug_assert!(byte.is_ascii(), "a non-ASCII byte splits a character");
		if self.content.as_bytes().first() == Some(&byte) {
			self.advance(1);
			Ok(())
		} else {
			Err(Fail::NoMatch)
		}
	}

	/// Consume `tag`.
	///
	/// # Errors
	/// If the input does not begin with it.
	pub fn tag(&mut self, tag: &str) -> PResult<&'data str> {
		if self.content.starts_with(tag) {
			Ok(self.advance(tag.len()))
		} else {
			Err(Fail::NoMatch)
		}
	}

	/// Consume `tag` if the input begins with it, saying whether it did.
	pub fn eat(&mut self, tag: &str) -> bool {
		self.tag(tag).is_ok()
	}

	/// Consume the longest prefix whose every character `predicate` accepts, which may be empty.
	pub fn take_while(&mut self, mut predicate: impl FnMut(char) -> bool) -> &'data str {
		let len = self
			.content
			.find(|ch| !predicate(ch))
			.unwrap_or(self.content.len());
		self.advance(len)
	}

	/// As [`Self::take_while`], but at least one character.
	///
	/// # Errors
	/// If the first character is not accepted.
	pub fn take_while1(&mut self, predicate: impl FnMut(char) -> bool) -> PResult<&'data str> {
		match self.take_while(predicate) {
			"" => Err(Fail::NoMatch),
			taken => Ok(taken),
		}
	}

	/// Consume everything before the next `tag`, which must be at least one byte.
	///
	/// # Errors
	/// If `tag` does not occur, or begins the input.
	pub fn take_until1(&mut self, tag: &str) -> PResult<&'data str> {
		match find(self.content.as_bytes(), tag.as_bytes()) {
			None | Some(0) => Err(Fail::NoMatch),
			Some(len) => Ok(self.advance(len)),
		}
	}

	/// Consume a decimal number.
	///
	/// # Errors
	/// If the input does not begin with a digit, or the number does not fit.
	pub fn u64(&mut self) -> PResult<u64> {
		let digits = self.content.bytes().take_while(u8::is_ascii_digit).count();
		let value = self.content[..digits].parse().map_err(|_| Fail::NoMatch)?;
		self.advance(digits);
		Ok(value)
	}

	/// Consume a decimal number with an optional sign.
	///
	/// # Errors
	/// If the input does not begin with a number, or the number does not fit.
	pub fn i64(&mut self) -> PResult<i64> {
		let sign = usize::from(self.content.starts_with(['+', '-']));
		let digits = self.content[sign..]
			.bytes()
			.take_while(u8::is_ascii_digit)
			.count();
		let len = sign + digits;
		let value = self.content[..len].parse().map_err(|_| Fail::NoMatch)?;
		self.advance(len);
		Ok(value)
	}

	/// Consume a `\n` or `\r\n`.
	///
	/// # Errors
	/// If the input does not begin with one.
	pub fn line_ending(&mut self) -> PResult<&'data str> {
		if self.content.starts_with('\n') {
			Ok(self.advance(1))
		} else if self.content.starts_with("\r\n") {
			Ok(self.advance(2))
		} else {
			Err(Fail::NoMatch)
		}
	}

	/// Consume a line ending, or nothing at the end of the input.
	///
	/// # Errors
	/// Anywhere else.
	pub fn line_ending_or_eof(&mut self) -> PResult<&'data str> {
		if self.content.is_empty() {
			Ok("")
		} else {
			self.line_ending()
		}
	}

	/// Whether the input begins with a line ending or is empty.
	#[must_use]
	pub fn at_line_end(&self) -> bool {
		self.content.is_empty()
			|| self.content.starts_with('\n')
			|| self.content.starts_with("\r\n")
	}

	/// Consume spaces and tabs, possibly none.
	pub fn space0(&mut self) -> &'data str {
		self.take_while(|ch| matches!(ch, ' ' | '\t'))
	}

	/// Consume at least one space or tab.
	///
	/// # Errors
	/// If the input does not begin with one.
	pub fn space1(&mut self) -> PResult<&'data str> {
		self.take_while1(|ch| matches!(ch, ' ' | '\t'))
	}

	/// Run `parser`, restoring the input if it does not match. Running out of fuel is not a
	/// mismatch: it ends the whole parse, so it is passed on.
	///
	/// # Errors
	/// If `parser` runs out of fuel.
	pub fn attempt<T>(
		&mut self,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> Result<Option<T>, OutOfFuel> {
		let saved = *self;
		match parser(self) {
			Ok(output) => Ok(Some(output)),
			Err(Fail::NoMatch) => {
				*self = saved;
				Ok(None)
			}
			Err(Fail::OutOfFuel) => Err(OutOfFuel),
		}
	}

	/// Whether `parser` matches here, without consuming anything.
	///
	/// # Errors
	/// If `parser` runs out of fuel.
	pub fn matches<T>(
		&self,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> Result<bool, OutOfFuel> {
		let mut lookahead = *self;
		Ok(lookahead.attempt(parser)?.is_some())
	}

	/// Run `parser`, returning what it consumed instead of its output.
	///
	/// # Errors
	/// If `parser` fails.
	pub fn recognize<T>(
		&mut self,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> PResult<&'data str> {
		let before = *self;
		parser(self)?;
		Ok(&before.content[..self.start - before.start])
	}

	/// Run `parser`, with a `kind` token covering what it consumed.
	///
	/// # Errors
	/// If `parser` fails.
	pub fn with_token<S: Span, T>(
		&mut self,
		kind: TokenKind,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> PResult<(T, S::Syntax)> {
		let start = self.start;
		let output = parser(self)?;
		Ok((output, token::<S>(kind, start, self.start)))
	}

	/// As [`Self::with_token`], dropping the output.
	///
	/// # Errors
	/// If `parser` fails.
	pub fn token<S: Span, T>(
		&mut self,
		kind: TokenKind,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> PResult<S::Syntax> {
		self.with_token::<S, T>(kind, parser)
			.map(|(_, syntax)| syntax)
	}

	/// Run `parser`, spanning its output over what it consumed.
	///
	/// # Errors
	/// If `parser` fails.
	pub fn spanned<S: Span, T>(
		&mut self,
		parser: impl FnOnce(&mut Self) -> PResult<T>,
	) -> PResult<Spanned<T, S>> {
		let start = self.start;
		let value = parser(self)?;
		Ok(Spanned {
			value,
			span: self.span(start),
		})
	}

	/// As [`Self::spanned`] for a parser that also reports its syntax, which joins the span.
	///
	/// # Errors
	/// If `parser` fails.
	pub fn spanned_with_syntax<S: Span, T>(
		&mut self,
		parser: impl FnOnce(&mut Self) -> PResult<(T, S::Syntax)>,
	) -> PResult<Spanned<T, S>> {
		let start = self.start;
		let (value, syntax) = parser(self)?;
		let mut span: S = self.span(start);
		span.attach(syntax);
		Ok(Spanned { value, span })
	}
}

/// A `kind` token from `start` to `end`, or nothing if they are the same.
#[must_use]
pub fn token<S: Span>(kind: TokenKind, start: usize, end: usize) -> S::Syntax {
	if end > start {
		S::Syntax::token(kind, start, end)
	} else {
		S::Syntax::default()
	}
}

impl Display for Input<'_> {
	fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
		write!(f, "{}", self.content)
	}
}

impl<'data> From<&'data str> for Input<'data> {
	fn from(value: &'data str) -> Self {
		Self {
			content: value,
			start: 0,
			source: value,
		}
	}
}

impl Deref for Input<'_> {
	type Target = str;

	fn deref(&self) -> &Self::Target {
		self.content
	}
}

impl PartialEq<&str> for Input<'_> {
	fn eq(&self, other: &&str) -> bool {
		self.content == *other
	}
}

impl PartialEq<String> for Input<'_> {
	fn eq(&self, other: &String) -> bool {
		self.content == *other
	}
}
