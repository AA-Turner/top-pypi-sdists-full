use std::{
	borrow::Cow,
	fmt::{Debug, Display},
	iter::Enumerate,
	ops::{Add, Deref},
};

use memchr::memmem::find;
use nom::{Compare, ExtendInto, FindSubstring, Needed, Offset};
use owned_chars::OwnedChars;

use super::span::Span;

#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub struct Input<'data> {
	pub content: Cow<'data, str>,
	pub start: usize,
}

impl Input<'_> {
	#[must_use]
	pub fn span<S>(&self, start: usize) -> S
	where
		S: Span,
	{
		S::new(start, self.start)
	}

	fn map<T>(&self, f: impl FnOnce(&str) -> T) -> T {
		match self.content {
			Cow::Borrowed(content) => f(content),
			Cow::Owned(ref content) => f(content.as_str()),
		}
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
			content: Cow::Borrowed(value),
			start: 0,
		}
	}
}

impl From<String> for Input<'_> {
	fn from(value: String) -> Self {
		Self {
			content: Cow::Owned(value),
			start: 0,
		}
	}
}

impl<'data> nom::Input for Input<'data> {
	type Item = char;
	type Iter = Chars<'data>;
	type IterIndices = Enumerate<Self::Iter>;

	fn input_len(&self) -> usize {
		self.content.len()
	}

	fn take(&self, index: usize) -> Self {
		let content = match self.content {
			Cow::Owned(ref content) => Cow::Owned(content.as_str().take(index).to_owned()),
			Cow::Borrowed(content) => Cow::Borrowed(content.take(index)),
		};

		Self {
			content,
			start: self.start,
		}
	}

	fn take_from(&self, index: usize) -> Self {
		let content = match self.content {
			Cow::Owned(ref content) => Cow::Owned(content.as_str().take_from(index).to_owned()),
			Cow::Borrowed(content) => Cow::Borrowed(content.take_from(index)),
		};

		Self {
			content,
			start: self.start + index,
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
		match self.content {
			Cow::Owned(ref content) => Chars::Owned(OwnedChars::from_string(content.clone())),
			Cow::Borrowed(content) => Chars::Borrowed(content.chars()),
		}
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
		acc.push_str(&self.content);
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
		match self.content {
			Cow::Owned(ref content) => content.as_str(),
			Cow::Borrowed(content) => content,
		}
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

impl<'data> Add<Input<'data>> for &str {
	type Output = Input<'data>;

	fn add(self, rhs: Input<'data>) -> Self::Output {
		Input {
			content: Cow::Owned(self.to_string() + &rhs.content),
			start: rhs.start,
		}
	}
}

impl<'data> FromIterator<Input<'data>> for Input<'data> {
	fn from_iter<T: IntoIterator<Item = Input<'data>>>(iter: T) -> Self {
		let mut iter = iter.into_iter();
		let first = iter.next();
		Self {
			start: first.as_ref().map(|input| input.start).unwrap_or_default(),
			content: Cow::Owned(
				first
					.into_iter()
					.chain(iter)
					.map(|input| input.content)
					.collect(),
			),
		}
	}
}

pub enum Chars<'data> {
	// TODO: use built-in type when string_into_chars is stabilized
	Owned(OwnedChars),
	Borrowed(std::str::Chars<'data>),
}

impl Iterator for Chars<'_> {
	type Item = char;

	fn next(&mut self) -> Option<Self::Item> {
		match self {
			Self::Owned(iter) => iter.next(),
			Self::Borrowed(iter) => iter.next(),
		}
	}
}
