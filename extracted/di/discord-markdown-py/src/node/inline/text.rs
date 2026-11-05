//! Text parsing.

use std::borrow::Cow;
use std::sync::LazyLock;

use tracing::Level;

use crate::Input;
use crate::context::Context;
use crate::error::{Fail, PResult};
use crate::input::token;
use crate::lossless::TokenKind;
use crate::range::delim::{self, DelimChar};
use crate::scope::ScopeSet;
use crate::span::{Span, Syntax, Trace};
use crate::syntax::SyntaxSet;
use crate::util::ByteSet;

use super::emoji;

/// The shrug emoticon, whose initial `¯\` would otherwise be read as an escape.
const SHRUG: &str = "_(ツ)_/¯";

/// A resolved escape sequence.
pub struct Escape<'data> {
	/// The text the sequence expands to.
	pub expansion: &'data str,
	/// How many bytes of the input the sequence covers, counting the backslash itself.
	pub consumed: usize,
}

impl Escape<'_> {
	/// Whether the backslash is dropped, rather than kept as text.
	#[must_use]
	pub fn drops_backslash(&self) -> bool {
		self.consumed > self.expansion.len()
	}
}

/// Resolve the escape sequence at the start of `rest`, which begins with a backslash.
#[must_use]
pub fn escape(rest: &str) -> Escape<'_> {
	let tail = &rest[1..];

	if tail.starts_with(SHRUG) {
		// The emoticon keeps its backslash -- `¯\_(ツ)_/¯` is text, not an escape.
		Escape {
			expansion: &rest[..=SHRUG.len()],
			consumed: 1 + SHRUG.len(),
		}
	} else if tail.starts_with("__") {
		// Allow escaping a double underscore with a single backslash.
		Escape {
			expansion: &tail[..2],
			consumed: 3,
		}
	} else {
		match tail.chars().next() {
			// TODO - Add support for non-latin languages by removing the 'ascii' bit here.
			Some(ch) if !ch.is_ascii_alphanumeric() && !ch.is_ascii_whitespace() => Escape {
				expansion: &tail[..ch.len_utf8()],
				consumed: 1 + ch.len_utf8(),
			},
			// Not an escape we recognise: the next character is alphanumeric or whitespace, or
			// the input ends here. The backslash is literal text, and nothing after it is
			// consumed, so the next character is parsed as normal text -- crucially including a
			// terminal sequence, which has to stay unconsumed for the run to end there.
			_ => Escape {
				expansion: "\\",
				consumed: 1,
			},
		}
	}
}

/// Every byte that [`at_plain_char`] might reject, whatever the scope or allowed syntax. A run of
/// bytes outside it is plain text, so text consumes it without checking each character.
///
/// Built from every syntax rather than a context's own, so that it stays a superset however the
/// context's syntax changes. Every non-ASCII byte is in it, so a run outside it is ASCII.
static STOPS: LazyLock<ByteSet> = LazyLock::new(|| {
	let mut stops = ByteSet::default();
	stops.insert(b'\\');
	for scope in ScopeSet::all() {
		scope.insert_boundary_bytes(&mut stops);
	}
	stops.extend((0..=u8::MAX).filter(|&byte| emoji::unicode::may_start_with(byte)));
	for syntax in SyntaxSet::all() {
		syntax.insert_first_bytes(&mut stops);
	}
	stops.extend((0..0x80).filter(|&byte| DelimChar::from_char(char::from(byte)).is_some()));
	stops
});

/// Whether the next character is plain text: not a backslash, and not the start of anything else
/// the inline parser reads.
fn at_plain_char(input: &Input, context: &Context) -> PResult<bool> {
	Ok(input.peek().is_some_and(|ch| ch != '\\')
		&& !context.at_terminal(input)
		&& !input.matches(emoji::unicode::emoji)?
		&& !context.starts_syntax(input)
		// a modifier delimiter, which the inline parser records instead
		&& !delim::starts_delimiter(input, context.syntaxes))
}

/// Parse text.
///
/// This is the fallback rule which successfully parses any non-empty content up to the
/// context's terminal sequence, an emoji, or the start of any of [`Context::syntaxes`]. It returns
/// the unescaped text, with the runs of it and the backslashes the escapes dropped. The text is
/// borrowed from the input unless an escape dropped a backslash.
///
/// # Errors
/// If no text begins the input.
// \\([^0-9A-Za-z\s])
#[tracing::instrument(name = "text_parser", level = Level::TRACE, skip_all, fields(ok, output))]
pub fn text<'data, S: Span>(
	input: &mut Input<'data>,
	context: &Context,
) -> PResult<(Cow<'data, str>, S::Syntax)> {
	let start = input.start;
	let source = input.content;
	// the text before the last dropped backslash, once there is one
	let mut unescaped = String::new();
	let mut syntax = S::Syntax::default();
	// where the run of text since the last dropped backslash begins
	let mut run = start;

	loop {
		let plain = input
			.bytes()
			.take_while(|&byte| !STOPS.contains(byte))
			.count();
		if plain > 0 {
			input.advance(plain);
			continue;
		}
		if at_plain_char(input, context)? {
			input.any_char()?;
			continue;
		}
		// anything else that is not plain text ends the run
		if !input.starts_with('\\') {
			break;
		}
		// An escape that keeps its backslash expands to exactly what it covers, and one that drops
		// it expands to what follows it, so the text is the runs between dropped backslashes.
		let escape = escape(input);
		debug_assert_eq!(
			escape.expansion,
			&input[usize::from(escape.drops_backslash())..escape.consumed]
		);
		if escape.drops_backslash() {
			let backslash = input.start;
			unescaped.push_str(&source[run - start..backslash - start]);
			syntax.append(token::<S>(TokenKind::Text, run, backslash));
			syntax.append(token::<S>(TokenKind::Escape, backslash, backslash + 1));
			run = backslash + 1;
		}
		input.advance(escape.consumed);
	}

	if input.start == start {
		return Err(Fail::NoMatch);
	}
	let last = &source[run - start..input.start - start];
	let text = if run == start {
		Cow::Borrowed(last)
	} else {
		unescaped.push_str(last);
		Cow::Owned(unescaped)
	};
	syntax.append(token::<S>(TokenKind::Text, run, input.start));
	Ok((text, syntax)).trace()
}

#[cfg(test)]
mod test {
	use std::borrow::Cow;

	use super::{STOPS, at_plain_char, text};
	use crate::{
		Input,
		context::Context,
		scope::{Scope, ScopeSet},
		test_utils::run,
	};

	/// A byte outside [`STOPS`] is skipped without [`at_plain_char`], so it has to be plain text
	/// in every scope, nested in every other, whatever follows it: a run of itself, as a delimiter
	/// would be, or any other byte.
	#[test]
	fn stops_cover_everything_but_plain_text() {
		let contexts = ScopeSet::all()
			.iter()
			.map(|scope| {
				ScopeSet::all()
					.iter()
					.fold(Context::default(), Context::with_scope)
					.with_scope(scope)
			})
			.collect::<Vec<_>>();

		for byte in (0..0x80).filter(|&byte| !STOPS.contains(byte)) {
			let ch = char::from(byte);
			let inputs = (0..0x80)
				.map(|next| format!("{ch}{}x", char::from(next)))
				.chain([ch.to_string().repeat(4)]);
			for s in inputs {
				for context in &contexts {
					assert!(
						at_plain_char(&Input::from(&*s), context) == Ok(true),
						"{s:?} is not plain text in {:?}",
						context.scope
					);
				}
			}
		}
	}

	#[test]
	fn simple_text() {
		let s = r"foo bar";
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo bar");
	}

	#[test]
	fn escaped_text() {
		let s = r"foo\_1bar";
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, "foo_1bar");
	}

	#[test]
	fn escaped_backslash() {
		let s = r"foo\\1bar";
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"foo\1bar");
	}

	#[test]
	fn shrug() {
		let s = r"¯\_(ツ)_/¯";
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"¯\_(ツ)_/¯");
	}

	/// A backslash before a character that cannot be escaped is literal text, and does not stop
	/// the run.
	#[test]
	fn unrecognised_escape_is_literal() {
		for (s, expected) in [
			(r"foo\bar", r"foo\bar"),
			(r"foo\ bar", r"foo\ bar"),
			(r"foo\9bar", r"foo\9bar"),
		] {
			let (rem, (res, ())) =
				run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
	}

	/// A backslash at the very end of the input is literal text. nom's `escaped_transform`
	/// rejected this outright, which is one of the reasons the escape loop was spelled out by hand.
	#[test]
	fn trailing_backslash_is_literal() {
		let s = r"foo\";
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
		assert_eq!(rem, "");
		assert_eq!(res, r"foo\");
	}

	/// An unrecognised escape must not retroactively disable the escapes before it, which is what
	/// happened while a failed run was being retried one character at a time.
	#[test]
	fn unrecognised_escape_does_not_disable_earlier_escapes() {
		for (s, expected) in [(r"a\_b\_c \z", r"a_b_c \z"), ("a\\_b\\_c \\", "a_b_c \\")] {
			let (rem, (res, ())) =
				run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
			assert_eq!(rem, "", "unexpected input remaining for {s:?}");
			assert_eq!(res, expected, "unexpected output for {s:?}");
		}
	}

	/// A terminal sequence after an unrecognised escape has to stay unconsumed, or the run would
	/// swallow the character that ends it.
	#[test]
	fn unrecognised_escape_does_not_consume_terminal_sequence() {
		let s = "foo\\\nbar";
		// a paragraph's line, which ends at the newline
		let context = Context::default().with_scope(Scope::InlineBlock);
		let (rem, (res, ())) =
			run(s, |input| text::<()>(input, &context)).expect("unable to parse");
		assert_eq!(rem, "\nbar");
		assert_eq!(res, "foo\\");
	}

	/// Text borrows from the input unless an escape dropped a backslash, which only an owned copy
	/// can leave out.
	#[test]
	fn borrows_unless_a_backslash_is_dropped() {
		for (s, borrowed) in [
			("foo bar", true),
			(r"¯\_(ツ)_/¯", true),
			(r"foo\bar", true),
			(r"foo\", true),
			(r"foo\_bar", false),
			(r"\*foo", false),
			(r"foo\\", false),
		] {
			let (_, (res, ())) =
				run(s, |input| text::<()>(input, &Context::default())).expect("unable to parse");
			assert_eq!(
				matches!(res, Cow::Borrowed(_)),
				borrowed,
				"unexpected ownership for {s:?}"
			);
		}
	}
}
