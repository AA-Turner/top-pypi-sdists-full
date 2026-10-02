#![doc = include_str!("../README.md")]

include!(concat!(env!("OUT_DIR"), "/confusables.rs"));

mod bidi;
mod script;
mod skeleton;

pub use script::{
	AugmentedScript, ConfusableClass, ScriptSet, classify_confusable, is_single_script,
	resolved_script_set,
};
pub use skeleton::{Direction, bidi_skeleton, is_confusable, is_confusable_in, skeleton};

#[cfg(test)]
mod test {
	use super::{
		AugmentedScript, ConfusableClass, Direction, PROTOTYPES_BY_SOURCE, SOURCES_BY_PROTOTYPE,
		ScriptSet, bidi_skeleton, classify_confusable, is_confusable, is_confusable_in,
		is_single_script, resolved_script_set, skeleton,
	};

	#[test]
	fn has_prototypes_by_source() {
		assert_ne!(PROTOTYPES_BY_SOURCE.len(), 0);
	}

	#[test]
	fn has_sources_by_prototype() {
		assert_ne!(SOURCES_BY_PROTOTYPE.len(), 0);
	}

	#[test]
	fn maps_prototypes() {
		// CYRILLIC SMALL LETTER A is confusable with LATIN SMALL LETTER A.
		assert_eq!(skeleton("\u{0430}"), "a");
		assert_eq!(skeleton("p\u{0430}yp\u{0430}l"), skeleton("paypal"));
	}

	#[test]
	fn reapplies_nfd() {
		// ANGSTROM SIGN, LATIN CAPITAL LETTER A WITH RING ABOVE, and the
		// decomposed pair all share a skeleton.
		assert_eq!(skeleton("\u{212B}"), skeleton("A\u{030A}"));
		assert_eq!(skeleton("\u{00C5}"), skeleton("A\u{030A}"));
	}

	#[test]
	fn removes_default_ignorables() {
		// ZERO WIDTH SPACE and ZERO WIDTH JOINER are removed.
		assert_eq!(skeleton("a\u{200B}b\u{200D}c"), skeleton("abc"));
	}

	#[test]
	fn is_idempotent() {
		// Note: `bidiSkeleton` itself is not idempotent over right-to-left
		// strings (reapplying it reorders again); only the prototype mapping
		// is, so restrict to left-to-right inputs.
		for input in ["p\u{0430}yp\u{0430}l", "\u{212B}", "ℎttps://discord.com"] {
			assert_eq!(skeleton(&skeleton(input)), skeleton(input));
		}
	}

	#[test]
	fn detects_masked_link_spoof() {
		assert!(skeleton("ℎttps://discord.com").starts_with("https"));
	}

	#[test]
	fn reverses_rtl_runs() {
		// A purely right-to-left string displays reversed in a left-to-right
		// paragraph.
		assert_eq!(
			bidi_skeleton(Direction::Ltr, "\u{05D0}\u{05D1}\u{05D2}"),
			"\u{05D2}\u{05D1}\u{05D0}",
		);
	}

	#[test]
	fn mirrors_in_rtl_runs() {
		// ALEF ( BET ) GIMEL: the run is reversed and the parentheses are
		// mirrored by L4, so they still wrap BET in display order.
		assert_eq!(
			bidi_skeleton(Direction::Ltr, "\u{05D0}(\u{05D1})\u{05D2}"),
			"\u{05D2}(\u{05D1})\u{05D0}",
		);
	}

	#[test]
	fn keeps_combining_marks_after_base() {
		// QAMATS stays attached after its ALEF through the reversal (L3).
		assert_eq!(
			bidi_skeleton(Direction::Ltr, "\u{05D0}\u{05B8}\u{05D1}"),
			"\u{05D1}\u{05D0}\u{05B8}",
		);
	}

	#[test]
	fn reorders_rtl_override() {
		// RIGHT-TO-LEFT OVERRIDE forces "bc" into a reversed run even though
		// no character has bidi class R or AL, so the LTR fast path must not
		// trigger here.
		assert_eq!(skeleton("a\u{202E}bc\u{202C}"), "acb");
	}

	#[test]
	fn first_strong_detects_direction() {
		assert_eq!(
			bidi_skeleton(Direction::FirstStrong, "\u{05D0}\u{05D1}"),
			bidi_skeleton(Direction::Rtl, "\u{05D0}\u{05D1}"),
		);
		assert_eq!(
			bidi_skeleton(Direction::FirstStrong, "ab"),
			bidi_skeleton(Direction::Ltr, "ab"),
		);
	}

	#[test]
	fn reorders_paragraphs_independently() {
		assert_eq!(
			bidi_skeleton(Direction::FirstStrong, "\u{05D0}\u{05D1}\nab"),
			format!("{}ab", bidi_skeleton(Direction::Rtl, "\u{05D0}\u{05D1}\n")),
		);
	}

	#[test]
	fn detects_confusable_pairs() {
		assert!(is_confusable("p\u{0430}yp\u{0430}l", "paypal"));
		assert!(!is_confusable("paypal", "discord"));
	}

	#[test]
	fn confusability_depends_on_direction() {
		// Both strings display as "abcגבא" in a left-to-right paragraph: the
		// Hebrew suffix of `x` reverses, while `y` pins it with a
		// LEFT-TO-RIGHT OVERRIDE. In a right-to-left paragraph `x` displays
		// with the Hebrew run first ("גבאabc") but `y` is unchanged.
		let x = "abc\u{05D0}\u{05D1}\u{05D2}";
		let y = "abc\u{202D}\u{05D2}\u{05D1}\u{05D0}\u{202C}";
		assert!(is_confusable_in(Direction::Ltr, x, y));
		assert!(!is_confusable_in(Direction::Rtl, x, y));
	}

	#[test]
	fn resolves_script_sets() {
		// Common characters resolve to all scripts.
		assert_eq!(resolved_script_set("123"), ScriptSet::All);
		assert_eq!(resolved_script_set(""), ScriptSet::All);

		// Han and Hiragana intersect in Japanese.
		let ScriptSet::Scripts(scripts) = resolved_script_set("\u{6F22}\u{306A}") else {
			panic!("expected an explicit script set");
		};
		assert!(scripts.contains(&AugmentedScript::Jpan));
		assert!(!scripts.contains(&AugmentedScript::Kore));

		// Latin and Cyrillic do not intersect.
		assert!(is_single_script("paypal"));
		assert!(!is_single_script("p\u{0430}yp\u{0430}l"));
	}

	#[test]
	fn classifies_whole_script_confusables() {
		// Latin "scope" vs. Cyrillic DZE ES O ER IE: confusable, and each
		// string is single-script.
		assert_eq!(
			classify_confusable("scope", "\u{0455}\u{0441}\u{043E}\u{0440}\u{0435}"),
			Some(ConfusableClass::WholeScript),
		);
	}

	#[test]
	fn classifies_mixed_script_confusables() {
		assert_eq!(
			classify_confusable("\u{0430}bc", "abc"),
			Some(ConfusableClass::MixedScript),
		);
	}

	#[test]
	fn classifies_single_script_confusables() {
		// SMALL ROMAN NUMERAL FIFTY is Latin, like "l".
		assert_eq!(
			classify_confusable("l", "\u{217C}"),
			Some(ConfusableClass::SingleScript),
		);
	}

	#[test]
	fn classifies_non_confusables() {
		assert_eq!(classify_confusable("paypal", "discord"), None);
	}
}
