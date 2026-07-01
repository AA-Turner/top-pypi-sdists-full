use std::collections::HashMap;
use std::env;
use std::fs::File;
use std::io::Write;
use std::path::Path;

use phf_codegen::Map;
use serde::Deserialize;

const SOURCE_URL: &str = "https://raw.githubusercontent.com/joypixels/emoji-assets/5f3144290e5cd8b8781ac18bb2a90f14972cfbff/emoji.json";

#[derive(Debug, Deserialize)]
struct CodePoints {
	base: String,
	fully_qualified: Option<String>,
}

#[derive(Debug, Deserialize)]
struct EmojiData {
	shortname: String,
	shortname_alternates: Vec<String>,
	diversity_children: Vec<String>,
	code_points: CodePoints,
}

type EmojiMap = HashMap<String, EmojiData>;

fn main() {
	let emoji_data: EmojiMap = reqwest::blocking::get(SOURCE_URL)
		.expect("Unable to fetch emoji data")
		.json()
		.expect("Emoji data in unexpected format");

	let mut shortname_to_codepoint = Map::new();

	for (_codepoint_key, emoji) in emoji_data {
		let code_point = encode_hex_emoji(
			&emoji
				.code_points
				.fully_qualified
				.unwrap_or(emoji.code_points.base),
		);

		let clean_shortname = emoji.shortname.trim_matches(':').to_string();
		shortname_to_codepoint.entry(clean_shortname.clone(), code_point.clone());

		for alt_name in &emoji.shortname_alternates {
			let clean_alt = alt_name.trim_matches(':').to_string();
			shortname_to_codepoint.entry(clean_alt, code_point.clone());
		}

		// For base emojis that have skin tone variants, also generate ::skin-tone-N entries
		// This is in addition to the existing _toneN entries that are already in the JSON
		for (i, child_codepoint) in emoji.diversity_children.iter().enumerate() {
			let skin_tone_shortname = format!("{}::skin-tone-{}", clean_shortname, i + 1);
			shortname_to_codepoint.entry(skin_tone_shortname, encode_hex_emoji(child_codepoint));

			for alt_name in &emoji.shortname_alternates {
				let clean_alt = alt_name.trim_matches(':').to_string();
				let skin_tone_alt = format!("{}::skin-tone-{}", clean_alt, i + 1);
				shortname_to_codepoint.entry(skin_tone_alt, encode_hex_emoji(child_codepoint));
			}
		}
	}

	let dest_path = Path::new(&env::var("OUT_DIR").unwrap()).join("emoji.rs");
	let mut file = File::create(&dest_path).expect("failed to create target file");

	writeln!(
		&mut file,
		"pub static EMOJI_BY_SHORTNAME: phf::Map<&'static str, &'static str> = {};",
		shortname_to_codepoint.build()
	)
	.unwrap();
}

fn encode_hex_emoji(hex_string: &str) -> String {
	let unicode = hex_string
		.split('-')
		.filter_map(|hex| u32::from_str_radix(hex, 16).ok().and_then(char::from_u32))
		.flat_map(char::escape_unicode)
		.collect::<String>();

	format!("\"{unicode}\"")
}
