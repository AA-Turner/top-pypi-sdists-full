use std::{
	fmt::{Debug, Display},
	iter::Enumerate,
	ops::Deref,
};

use memchr::memmem::find;
use nom::{Compare, ExtendInto, FindSubstring, Needed, Offset};

use super::span::Span;

/// The input type for parsing.
///
/// Comparison and ordering look only at [`Self::content`] and [`Self::start`]: [`Self::source`] is
/// the same string for every input derived from one parse, so including it would only ever add work.
#[derive(Debug, Clone)]
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
	/// [`crate::inline::link::detection::at_token_start`]).
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

impl Input<'_> {
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

	fn map<T>(&self, f: impl FnOnce(&str) -> T) -> T {
		f(self.content)
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

impl<'data> nom::Input for Input<'data> {
	type Item = char;
	type Iter = std::str::Chars<'data>;
	type IterIndices = Enumerate<Self::Iter>;

	fn input_len(&self) -> usize {
		self.content.len()
	}

	fn take(&self, index: usize) -> Self {
		Self {
			content: &self.content[..index],
			start: self.start,
			source: self.source,
		}
	}

	fn take_from(&self, index: usize) -> Self {
		Self {
			content: &self.content[index..],
			start: self.start + index,
			source: self.source,
		}
	}

	fn take_split(&self, index: usize) -> (Self, Self) {
		(self.take_from(index), self.take(index))
	}

	fn position<P>(&self, predicate: P) -> Option<usize>
	where
		P: Fn(Self::Item) -> bool,
	{
		self.content.find(predicate)
	}

	fn iter_elements(&self) -> Self::Iter {
		self.content.chars()
	}

	fn iter_indices(&self) -> Self::IterIndices {
		self.iter_elements().enumerate()
	}

	fn slice_index(&self, count: usize) -> Result<usize, Needed> {
		self.map(|content| content.slice_index(count))
	}
}

impl ExtendInto for Input<'_> {
	type Item = char;
	type Extender = String;

	fn new_builder(&self) -> Self::Extender {
		String::new()
	}

	fn extend_into(&self, acc: &mut Self::Extender) {
		acc.push_str(self.content);
	}
}

impl Compare<&str> for Input<'_> {
	fn compare(&self, t: &str) -> nom::CompareResult {
		self.map(|content| content.compare(t))
	}

	fn compare_no_case(&self, t: &str) -> nom::CompareResult {
		// TODO: this can be improved with unicode aware casing
		self.map(|content| content.compare_no_case(t))
	}
}

impl Compare<&[u8]> for Input<'_> {
	fn compare(&self, t: &[u8]) -> nom::CompareResult {
		self.map(|content| content.compare(t))
	}

	fn compare_no_case(&self, t: &[u8]) -> nom::CompareResult {
		self.map(|content| content.compare_no_case(t))
	}
}

impl Offset for Input<'_> {
	fn offset(&self, second: &Self) -> usize {
		second.start - self.start
	}
}

impl FindSubstring<&str> for Input<'_> {
	fn find_substring(&self, substr: &str) -> Option<usize> {
		find(self.content.as_bytes(), substr.as_bytes())
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
