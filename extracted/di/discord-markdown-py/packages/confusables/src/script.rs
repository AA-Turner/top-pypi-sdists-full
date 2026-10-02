//! Resolved script sets ([UTS #39 §5.1]) and the confusable classifications
//! of [UTS #39 §4] that depend on them.
//!
//! [UTS #39 §4]: https://www.unicode.org/reports/tr39/#Confusable_Detection
//! [UTS #39 §5.1]: https://www.unicode.org/reports/tr39/#Mixed_Script_Detection

use std::collections::BTreeSet;

use icu_properties::{props::Script, script::ScriptWithExtensions};

use crate::skeleton::is_confusable;

/// A script in the augmented script sets of UTS #39 §5.1: either a real
/// `Script` property value or one of the combined-script values from ISO
/// 15924 that the augmentation introduces.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum AugmentedScript {
	/// A `Script` property value.
	Script(Script),
	/// Han with Bopomofo, as used in Taiwan.
	Hanb,
	/// Japanese: Han, Hiragana, and Katakana.
	Jpan,
	/// Korean: Han and Hangul.
	Kore,
}

/// A set of [`AugmentedScript`]s, possibly the set of all scripts (produced
/// by Common and Inherited characters).
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ScriptSet {
	/// The set of all scripts.
	All,
	/// An explicit set of scripts.
	Scripts(BTreeSet<AugmentedScript>),
}

impl ScriptSet {
	/// The intersection of two script sets.
	#[must_use]
	pub fn intersect(&self, other: &Self) -> Self {
		match (self, other) {
			(Self::All, _) => other.clone(),
			(_, Self::All) => self.clone(),
			(Self::Scripts(a), Self::Scripts(b)) => {
				Self::Scripts(a.intersection(b).copied().collect())
			}
		}
	}

	/// Whether this set is empty. [`ScriptSet::All`] is never empty.
	pub fn is_empty(&self) -> bool {
		match self {
			Self::All => false,
			Self::Scripts(scripts) => scripts.is_empty(),
		}
	}

	/// Whether the two sets have at least one element in common.
	pub fn intersects(&self, other: &Self) -> bool {
		!self.intersect(other).is_empty()
	}
}

/// The augmented script set of a single character (UTS #39 §5.1): its
/// Script_Extensions values, where Common and Inherited imply all scripts,
/// Han additionally implies Hanb, Jpan, and Kore, Hiragana and Katakana
/// imply Jpan, Hangul implies Kore, and Bopomofo implies Hanb.
fn augmented_script_set(ch: char) -> ScriptSet {
	let extensions = ScriptWithExtensions::new().get_script_extensions_val(ch);

	if extensions.contains(&Script::Common) || extensions.contains(&Script::Inherited) {
		return ScriptSet::All;
	}

	let mut scripts = BTreeSet::new();
	for script in extensions.iter() {
		scripts.insert(AugmentedScript::Script(script));
		match script {
			Script::Han => {
				scripts.insert(AugmentedScript::Hanb);
				scripts.insert(AugmentedScript::Jpan);
				scripts.insert(AugmentedScript::Kore);
			}
			Script::Hiragana | Script::Katakana => {
				scripts.insert(AugmentedScript::Jpan);
			}
			Script::Hangul => {
				scripts.insert(AugmentedScript::Kore);
			}
			Script::Bopomofo => {
				scripts.insert(AugmentedScript::Hanb);
			}
			_ => {}
		}
	}

	ScriptSet::Scripts(scripts)
}

/// The resolved script set of a string (UTS #39 §5.1): the intersection of
/// the augmented script sets of its characters. The empty string resolves to
/// [`ScriptSet::All`].
pub fn resolved_script_set(x: &str) -> ScriptSet {
	x.chars().fold(ScriptSet::All, |set, ch| {
		set.intersect(&augmented_script_set(ch))
	})
}

/// Whether `x` is a single-script string: its [`resolved_script_set`] is not
/// empty.
pub fn is_single_script(x: &str) -> bool {
	!resolved_script_set(x).is_empty()
}

/// Classification of a confusable pair of strings per UTS #39 §4.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub enum ConfusableClass {
	/// The strings' resolved script sets have at least one element in common.
	SingleScript,
	/// The strings' resolved script sets are disjoint, and at least one
	/// string is not single-script.
	MixedScript,
	/// The strings' resolved script sets are disjoint, but each string is
	/// itself single-script.
	WholeScript,
}

/// Classify `x` and `y` per UTS #39 §4, or `None` if they are not confusable
/// (their [`skeleton`](crate::skeleton())s differ).
pub fn classify_confusable(x: &str, y: &str) -> Option<ConfusableClass> {
	if !is_confusable(x, y) {
		return None;
	}

	let x_scripts = resolved_script_set(x);
	let y_scripts = resolved_script_set(y);

	if x_scripts.intersects(&y_scripts) {
		Some(ConfusableClass::SingleScript)
	} else if !x_scripts.is_empty() && !y_scripts.is_empty() {
		Some(ConfusableClass::WholeScript)
	} else {
		Some(ConfusableClass::MixedScript)
	}
}
