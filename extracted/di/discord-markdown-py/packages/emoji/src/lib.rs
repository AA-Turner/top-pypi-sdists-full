include!(concat!(env!("OUT_DIR"), "/emoji.rs"));

/// Whether `ch` is in [`EMOJI_SHORTNAME_CHARS`], without hashing it when it is ASCII.
#[must_use]
pub fn is_shortname_char(ch: char) -> bool {
	if ch.is_ascii() {
		ASCII_SHORTNAME_CHARS & 1 << u32::from(ch) != 0
	} else {
		EMOJI_SHORTNAME_CHARS.contains(&ch)
	}
}

#[cfg(test)]
mod test {
	use super::{EMOJI_BY_SHORTNAME, EMOJI_SHORTNAME_CHARS, is_shortname_char};

	#[test]
	fn shortname_chars_agree_with_the_set() {
		for ch in (0..0x80u8).map(char::from).chain(['ñ', 'é']) {
			assert_eq!(
				is_shortname_char(ch),
				EMOJI_SHORTNAME_CHARS.contains(&ch),
				"{ch:?}"
			);
		}
	}

	#[test]
	fn has_data() {
		assert_ne!(EMOJI_BY_SHORTNAME.len(), 0);
	}

	#[test]
	fn has_chars() {
		assert_ne!(EMOJI_SHORTNAME_CHARS.len(), 0);
		assert!(EMOJI_SHORTNAME_CHARS.contains(&'+'));
	}

	#[test]
	fn chars_does_not_include_colon() {
		assert!(!EMOJI_SHORTNAME_CHARS.contains(&':'));
	}

	#[test]
	fn skin_tones_start_lightest() {
		assert_eq!(EMOJI_BY_SHORTNAME["man_cook::skin-tone-1"], "👨🏻‍🍳");
		assert_eq!(EMOJI_BY_SHORTNAME["man_cook::skin-tone-5"], "👨🏿‍🍳");
	}

	#[test]
	fn pair_skin_tones_go_by_first_person_then_second() {
		assert_eq!(EMOJI_BY_SHORTNAME["couple::skin-tone-1"], "👫🏻");
		assert_eq!(EMOJI_BY_SHORTNAME["couple::skin-tone-2"], "👩🏻‍🤝‍👨🏼");
		assert_eq!(EMOJI_BY_SHORTNAME["couple::skin-tone-6"], "👩🏼‍🤝‍👨🏻");
		assert_eq!(EMOJI_BY_SHORTNAME["couple::skin-tone-25"], "👫🏿");
	}
}
