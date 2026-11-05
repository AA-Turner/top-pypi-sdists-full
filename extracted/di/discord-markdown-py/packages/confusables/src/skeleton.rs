//! The `skeleton` and `bidiSkeleton` transforms and confusability predicates
//! from [UTS #39 §4].
//!
//! [UTS #39 §4]: https://www.unicode.org/reports/tr39/#Confusable_Detection

use std::borrow::Cow;

use icu_normalizer::DecomposingNormalizer;
use icu_properties::{CodePointSetData, props::DefaultIgnorableCodePoint};
use unicode_bidi::{BidiClass, bidi_class};

use crate::{ASCII_PROTOTYPES, PROTOTYPES_BY_SOURCE, bidi};

/// Base paragraph direction used by the `bidiSkeleton` transform (protocol
/// HL1 of UAX #9).
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum Direction {
	/// Force a left-to-right paragraph level.
	Ltr,
	/// Force a right-to-left paragraph level.
	Rtl,
	/// Detect the paragraph level from the first strong character (rules
	/// P2–P3 of UAX #9).
	FirstStrong,
}

/// The `internalSkeleton` transform: NFD, remove default-ignorable code
/// points, map each character to its prototype, and reapply NFD.
///
/// Unlike [`skeleton`], this does no bidirectional reordering, so it suits
/// text already in display order (see [`display_order`]).
pub fn internal_skeleton(x: &str) -> String {
	// ASCII is already NFD, holds no default-ignorables, and maps to prototypes made only of
	// starters with no decomposition, so neither normalization changes anything.
	if x.is_ascii() {
		return x
			.bytes()
			.map(|byte| ASCII_PROTOTYPES[usize::from(byte)])
			.collect();
	}

	unicode_internal_skeleton(x)
}

/// [`internal_skeleton`] for any text.
fn unicode_internal_skeleton(x: &str) -> String {
	let nfd = DecomposingNormalizer::new_nfd();
	let default_ignorable = CodePointSetData::new::<DefaultIgnorableCodePoint>();

	let decomposed = nfd.normalize(x);
	let prototyped = decomposed
		.chars()
		.filter(|ch| !default_ignorable.contains(*ch))
		.flat_map(|ch| {
			PROTOTYPES_BY_SOURCE
				.get(&ch)
				.map_or(Prototype::Source(ch), |prototype| {
					Prototype::Mapped(prototype)
				})
		});

	nfd.normalize_iter(prototyped).collect()
}

/// A character's prototype: either the mapped exemplar string or the
/// character itself.
enum Prototype {
	Source(char),
	Mapped(&'static str),
}

impl Iterator for Prototype {
	type Item = char;

	fn next(&mut self) -> Option<char> {
		match self {
			Prototype::Source(ch) => {
				let ch = *ch;
				*self = Prototype::Mapped("");
				Some(ch)
			}
			Prototype::Mapped(rest) => {
				let mut chars = rest.chars();
				let ch = chars.next()?;
				*rest = chars.as_str();
				Some(ch)
			}
		}
	}
}

/// `true` if `x` cannot be reordered or mirrored by the bidirectional
/// algorithm under a left-to-right paragraph level, in which case
/// `bidiSkeleton(LTR, x) = internalSkeleton(x)`.
///
/// This is stricter than the fast path stated in UTS #39 ("no characters
/// with bidi classes R or AL"): explicit directional controls such as RLO
/// can create right-to-left runs without any R or AL character present.
fn is_reorder_free(x: &str) -> bool {
	!x.chars().any(|ch| {
		if ch.is_ascii() {
			// the only ASCII in these classes is the paragraph separators, class B
			matches!(ch, '\n' | '\r' | '\u{1C}'..='\u{1E}')
		} else {
			can_reorder(ch)
		}
	})
}

/// Whether `ch` has a bidi class that can reorder or mirror text in a left-to-right paragraph.
fn can_reorder(ch: char) -> bool {
	matches!(
		bidi_class(ch),
		BidiClass::R
			| BidiClass::AL
			| BidiClass::AN
			| BidiClass::RLE
			| BidiClass::RLO
			| BidiClass::RLI
			| BidiClass::LRE
			| BidiClass::LRO
			| BidiClass::LRI
			| BidiClass::PDF
			| BidiClass::PDI
			| BidiClass::FSI
			| BidiClass::B
	)
}

/// The `bidiSkeleton` transform of UTS #39 §4: reorder `x` for display per
/// the Unicode Bidirectional Algorithm (rules L1–L4) with base direction
/// `direction`, then apply `internalSkeleton`.
///
/// The result is meant only for confusability comparison, never for display.
pub fn bidi_skeleton(direction: Direction, x: &str) -> String {
	internal_skeleton(&display_order(direction, x))
}

/// Reorder `x` for display per the Unicode Bidirectional Algorithm (rules
/// L1–L4) with base direction `direction`: steps 1–3 of [`bidi_skeleton`].
///
/// The result is meant only for confusability comparison, never for display.
pub fn display_order(direction: Direction, x: &str) -> Cow<'_, str> {
	if direction == Direction::Ltr && is_reorder_free(x) {
		return Cow::Borrowed(x);
	}

	Cow::Owned(bidi::reorder(direction, x))
}

/// The `skeleton` transform of UTS #39 §4, equivalent to
/// [`bidi_skeleton`]`(`[`Direction::Ltr`]`, x)`.
pub fn skeleton(x: &str) -> String {
	bidi_skeleton(Direction::Ltr, x)
}

/// Whether `x` and `y` are confusable: their [`skeleton`]s are equal.
pub fn is_confusable(x: &str, y: &str) -> bool {
	skeleton(x) == skeleton(y)
}

/// Whether `x` and `y` are confusable when displayed with the given base
/// direction: their [`bidi_skeleton`]s are equal.
pub fn is_confusable_in(direction: Direction, x: &str, y: &str) -> bool {
	bidi_skeleton(direction, x) == bidi_skeleton(direction, y)
}

#[cfg(test)]
mod test {
	use super::{can_reorder, internal_skeleton, is_reorder_free, unicode_internal_skeleton};

	fn ascii() -> impl Iterator<Item = char> {
		(0..0x80u8).map(char::from)
	}

	#[test]
	fn ascii_reorders_as_its_bidi_class_says() {
		for ch in ascii() {
			assert_eq!(!is_reorder_free(&ch.to_string()), can_reorder(ch), "{ch:?}");
		}
	}

	/// The ASCII shortcut agrees with the full transform, one character at a time and together.
	#[test]
	fn ascii_skeleton_matches_the_full_transform() {
		for ch in ascii() {
			let s = ch.to_string();
			assert_eq!(
				internal_skeleton(&s),
				unicode_internal_skeleton(&s),
				"{ch:?}"
			);
		}

		let all = ascii().collect::<String>();
		let reversed = all.chars().rev().collect::<String>();
		for s in [all, reversed, "%m1|I0`\"https://discord.gg/x".to_owned()] {
			assert_eq!(
				internal_skeleton(&s),
				unicode_internal_skeleton(&s),
				"{s:?}"
			);
		}
	}
}
