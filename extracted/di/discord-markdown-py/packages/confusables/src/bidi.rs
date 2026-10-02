//! Display reordering per the Unicode Bidirectional Algorithm, covering steps
//! 1–3 of the `bidiSkeleton` transform from [UTS #39 §4]: rules L1–L2 (via
//! [`unicode_bidi`]), L3 (combining mark reordering), and L4 (mirroring).
//!
//! The output is intended solely as input to `internalSkeleton`, not for
//! display.
//!
//! Note: the Unicode versions of the `unicode-bidi` hardcoded tables, the ICU
//! baked property data, and the confusables data fetched by `build.rs` may
//! differ slightly.
//!
//! [UTS #39 §4]: https://www.unicode.org/reports/tr39/#Confusable_Detection

use icu_properties::{CodePointMapData, props::BidiMirroringGlyph};
use unicode_bidi::{BidiClass, BidiInfo, Level, bidi_class};

use crate::Direction;

/// Reorder `text` into display order as a standalone paragraph sequence with
/// the given base direction.
pub(crate) fn reorder(direction: Direction, text: &str) -> String {
	let level = match direction {
		Direction::Ltr => Some(Level::ltr()),
		Direction::Rtl => Some(Level::rtl()),
		Direction::FirstStrong => None,
	};

	let bidi_info = BidiInfo::new(text, level);
	let mirroring = CodePointMapData::<BidiMirroringGlyph>::new();

	let mut reordered = String::with_capacity(text.len());
	for paragraph in &bidi_info.paragraphs {
		let (levels, runs) = bidi_info.visual_runs(paragraph, paragraph.range.clone());
		for run in runs {
			if !levels[run.start].is_rtl() {
				reordered.push_str(&text[run]);
				continue;
			}

			// L3: within a reversed run, combining marks must still follow
			// their base, so reverse in clusters of base + nonspacing marks.
			// L4: characters with resolved direction R take their mirrored
			// glyph.
			let mut clusters: Vec<&str> = Vec::new();
			for (idx, ch) in text[run.clone()].char_indices() {
				if idx == 0 || bidi_class(ch) != BidiClass::NSM {
					clusters.push(&text[run.start + idx..run.start + idx + ch.len_utf8()]);
				} else {
					let cluster = clusters
						.last_mut()
						.expect("idx != 0 implies a prior cluster");
					*cluster =
						&text[run.start + idx - cluster.len()..run.start + idx + ch.len_utf8()];
				}
			}

			for cluster in clusters.into_iter().rev() {
				for ch in cluster.chars() {
					let glyph = mirroring.get(ch);
					match glyph.mirroring_glyph {
						Some(mirrored) if glyph.mirrored => reordered.push(mirrored),
						_ => reordered.push(ch),
					}
				}
			}
		}
	}

	reordered
}
