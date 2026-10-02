include!(concat!(env!("OUT_DIR"), "/emoji.rs"));

#[cfg(test)]
mod test {
	use super::{EMOJI_BY_SHORTNAME, EMOJI_SHORTNAME_CHARS};

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
}
