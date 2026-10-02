//! The `skeleton` and `bidiSkeleton` transforms and confusability predicates
//! from [UTS #39 §4].
//!
//! [UTS #39 §4]: https://www.unicode.org/reports/tr39/#Confusable_Detection

use icu_normalizer::DecomposingNormalizer;
use icu_properties::{CodePointSetData, props::DefaultIgnorableCodePoint};
use unicode_bidi::{BidiClass, bidi_class};

use crate::{PROTOTYPES_BY_SOURCE, bidi};

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
fn internal_skeleton(x: &str) -> String {
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
	})
}

/// The `bidiSkeleton` transform of UTS #39 §4: reorder `x` for display per
/// the Unicode Bidirectional Algorithm (rules L1–L4) with base direction
/// `direction`, then apply `internalSkeleton`.
///
/// The result is meant only for confusability comparison, never for display.
pub fn bidi_skeleton(direction: Direction, x: &str) -> String {
	if direction == Direction::Ltr && is_reorder_free(x) {
		return internal_skeleton(x);
	}

	internal_skeleton(&bidi::reorder(direction, x))
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
