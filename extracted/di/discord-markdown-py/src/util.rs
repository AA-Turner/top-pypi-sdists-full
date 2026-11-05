use memchr::memchr2_iter;

/// A set of bytes.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct ByteSet([u64; 4]);

impl ByteSet {
	/// Add `byte` to the set.
	pub fn insert(&mut self, byte: u8) {
		self.0[usize::from(byte >> 6)] |= 1 << (byte & 63);
	}

	/// Add each of `bytes` to the set.
	pub fn extend(&mut self, bytes: impl IntoIterator<Item = u8>) {
		for byte in bytes {
			self.insert(byte);
		}
	}

	/// Whether `byte` is in the set.
	#[must_use]
	pub fn contains(&self, byte: u8) -> bool {
		self.0[usize::from(byte >> 6)] & (1 << (byte & 63)) != 0
	}

	/// The bytes in the set, in ascending order.
	pub fn iter(self) -> impl Iterator<Item = u8> {
		self.0.into_iter().zip(0u8..).flat_map(|(mut bits, word)| {
			std::iter::from_fn(move || {
				// `trailing_zeros` is 64 once no bits are left
				let bit = u8::try_from(bits.trailing_zeros())
					.ok()
					.filter(|&bit| bit < 64)?;
				bits &= bits - 1;
				Some(word * 64 + bit)
			})
		})
	}
}

/// Byte length of the balanced `open`/`close` span at the start of `bytes`, counting both
/// delimiters, whatever the span encloses.
///
/// Returns `None` if `bytes` does not begin with `open` or if nothing closes the span. Depth
/// counting keeps this a single pass with no recursion. `open` and `close` must differ.
#[must_use]
pub fn balanced_span(bytes: &[u8], open: u8, close: u8) -> Option<usize> {
	debug_assert_ne!(
		open, close,
		"a span cannot open and close with the same byte"
	);

	if bytes.first() != Some(&open) {
		return None;
	}

	let mut depth = 0usize;

	for pos in memchr2_iter(open, close, bytes) {
		if bytes[pos] == open {
			depth += 1;
		} else {
			depth -= 1;
			if depth == 0 {
				return Some(pos + 1);
			}
		}
	}

	None
}

#[cfg(test)]
mod test {
	use super::balanced_span;

	/// Span the brackets at the start of `s`.
	fn brackets(s: &str) -> Option<usize> {
		balanced_span(s.as_bytes(), b'[', b']')
	}

	#[test]
	fn byte_set_iterates_its_bytes_in_order() {
		let bytes = [0, 1, 63, 64, 127, 128, 200, 255];
		let mut set = super::ByteSet::default();
		set.extend(bytes.into_iter().rev());
		assert_eq!(set.iter().collect::<Vec<_>>(), bytes);
		assert_eq!(super::ByteSet::default().iter().count(), 0);
	}

	#[test]
	fn spans_a_pair_and_its_nesting() {
		assert_eq!(brackets("[]"), Some(2));
		assert_eq!(brackets("[a]"), Some(3));
		assert_eq!(brackets("[[a][b]]rest"), Some(8));
	}

	#[test]
	fn needs_an_opener_and_a_close() {
		assert_eq!(brackets("a[]"), None);
		assert_eq!(brackets(""), None);
		assert_eq!(brackets("[a"), None);
		assert_eq!(brackets("[[a]"), None);
	}

	/// A span may run past a close that a deeper level already claimed.
	#[test]
	fn closes_at_matching_depth() {
		assert_eq!(brackets("[a[b]c]d"), Some(7));
	}

	/// Nothing between the delimiters is off limits, newlines included.
	#[test]
	fn crosses_any_content() {
		assert_eq!(brackets("[a b\nc]"), Some(7));
	}
}
