include!(concat!(env!("OUT_DIR"), "/emoji.rs"));

#[cfg(test)]
mod test {
	use super::EMOJI_BY_SHORTNAME;

	#[test]
	fn has_data() {
		assert_ne!(EMOJI_BY_SHORTNAME.len(), 0);
	}
}
