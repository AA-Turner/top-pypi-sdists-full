use std::{collections::HashMap, env, fs::File, io::Write, path::Path};

use phf_codegen::Map;

static CONFUSABLES_URL: &str = "https://www.unicode.org/Public/security/16.0.0/confusables.txt";

fn char_from_hex(hex: &str) -> char {
	char::from_u32(
		u32::from_str_radix(hex, 16).unwrap_or_else(|_| panic!("{hex} is not hex encoded")),
	)
	.unwrap_or_else(|| panic!("{hex} is not a char"))
}

fn str_from_hex(hex: &str) -> String {
	hex.split(" ").map(char_from_hex).collect()
}

fn main() {
	let data = reqwest::blocking::get(CONFUSABLES_URL)
		.expect("unable to fetch confusables data")
		.error_for_status()
		.expect("unable to fetch confusables data")
		.text()
		.expect("confusables data in unexpected format");

	let mut prototypes_by_source = Map::new();
	let mut sources_by_prototype = HashMap::<String, Vec<char>>::new();

	for line in data.lines() {
		if line.is_empty() || line.starts_with("#") {
			continue;
		}

		let Some((origin, destination)) = line.split_once(";") else {
			continue;
		};

		let Some((destination, _)) = destination.split_once(";") else {
			continue;
		};

		let origin = char_from_hex(origin.trim());
		let destination = str_from_hex(destination.trim());

		prototypes_by_source.entry(origin, format!("\"{}\"", destination.escape_unicode()));
		sources_by_prototype
			.entry(destination)
			.and_modify(|chars| chars.push(origin))
			.or_insert(vec![origin]);
	}

	let path = Path::new(&env::var("OUT_DIR").unwrap()).join("confusables.rs");
	let mut dest = File::create(path).expect("unable to create target file");

	write!(
		&mut dest,
		r#"/// Mapping of source characters to their confusable prototypes.
pub static PROTOTYPES_BY_SOURCE: phf::Map<char, &'static str> = {};
"#,
		prototypes_by_source.build()
	)
	.expect("unable to write target file");

	let mut sources_by_prototype_map = Map::new();
	for (k, v) in sources_by_prototype {
		sources_by_prototype_map.entry(
			k,
			format!(
				"&[{}]",
				v.iter().fold(String::new(), |acc, v| acc
					+ &format!("'{}', ", v.escape_unicode()))
			),
		);
	}

	write!(
		&mut dest,
		r#"/// Mapping of source characters to their confusable prototypes.
pub static SOURCES_BY_PROTOTYPE: phf::Map<&'static str, &[char]> = {};
"#,
		sources_by_prototype_map.build(),
	)
	.expect("unable to write target file");
}
