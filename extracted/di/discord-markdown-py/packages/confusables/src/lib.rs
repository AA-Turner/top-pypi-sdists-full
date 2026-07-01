include!(concat!(env!("OUT_DIR"), "/confusables.rs"));

#[cfg(test)]
mod test {
	use super::{PROTOTYPES_BY_SOURCE, SOURCES_BY_PROTOTYPE};

	#[test]
	fn has_prototypes_by_source() {
		assert_ne!(PROTOTYPES_BY_SOURCE.len(), 0);
	}

	#[test]
	fn has_sources_by_prototype() {
		assert_ne!(SOURCES_BY_PROTOTYPE.len(), 0);
	}
}
