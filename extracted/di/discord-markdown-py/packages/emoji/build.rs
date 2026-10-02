use std::collections::{HashMap, HashSet};
use std::env;
use std::fs::{File, read_to_string};
use std::io::Write;
use std::path::Path;

use phf_codegen::{Map, Set};
use serde::Deserialize;

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

const VARIATION_SELECTOR_HEX: &str = "fe0f";
const VARIATION_SELECTOR_16: char = '\u{FE0F}';

fn main() {
	let emoji_data: EmojiMap =
		serde_json::from_str(&read_to_string("./emoji.json").unwrap()).unwrap();

	// Some entries drop the variation selector that qualifies them -- `:transgender_symbol:` is
	// `26a7`, not `26a7 fe0f` -- so learn which code points take one from the entries that do.
	// Trailing only: a skin tone replaces the selector, so `:v_tone1:` is correctly `270c 1f3fb`.
	let needs_variation_selector: HashSet<&str> = emoji_data
		.values()
		.flat_map(|emoji| {
			let code_points = hex_code_points(emoji);

			code_points
				.split('-')
				.zip(code_points.split('-').skip(1))
				.filter_map(|(code_point, next)| {
					(next == VARIATION_SELECTOR_HEX).then_some(code_point)
				})
		})
		.collect();

	// `diversity_children` holds keys, and a key spells only the base sequence: tone 1 of
	// `:person_curly_hair:` is keyed `1f9d1-1f3fb-1f9b1` but qualified `1f9d1-1f3fb-200d-1f9b1`.
	// Resolve through the data so the joiner survives.
	let code_point_by_key: HashMap<&str, String> = emoji_data
		.iter()
		.map(|(key, emoji)| {
			(
				key.as_str(),
				fully_qualified(emoji, &needs_variation_selector),
			)
		})
		.collect();

	let mut shortname_to_codepoint = Map::new();
	let mut emoji_shortname_chars = HashSet::new();
	let mut code_points = HashSet::new();

	let mut insert_shortname = |base: String, name: String, code_point: String| {
		for char in base.chars() {
			emoji_shortname_chars.insert(char);
		}

		code_points.insert(code_point.clone());
		shortname_to_codepoint.entry(name, rust_literal(&code_point));
	};

	for emoji in emoji_data.values() {
		let code_point = fully_qualified(emoji, &needs_variation_selector);

		let clean_shortname = emoji.shortname.trim_matches(':').to_string();
		insert_shortname(
			clean_shortname.clone(),
			clean_shortname.clone(),
			code_point.clone(),
		);

		for alt_name in &emoji.shortname_alternates {
			let clean_alt = alt_name.trim_matches(':').to_string();
			insert_shortname(clean_alt.clone(), clean_alt, code_point.clone());
		}

		// For base emojis that have skin tone variants, also generate ::skin-tone-N entries
		// This is in addition to the existing _toneN entries that are already in the JSON
		for (i, child_key) in emoji.diversity_children.iter().enumerate() {
			let child_code_point = code_point_by_key
				.get(child_key.as_str())
				.cloned()
				.unwrap_or_else(|| decode_hex_emoji(child_key));

			let skin_tone_shortname = format!("{}::skin-tone-{}", clean_shortname, i + 1);
			insert_shortname(
				clean_shortname.clone(),
				skin_tone_shortname,
				child_code_point.clone(),
			);

			for alt_name in &emoji.shortname_alternates {
				let clean_alt = alt_name.trim_matches(':').to_string();
				let skin_tone_alt = format!("{}::skin-tone-{}", clean_alt, i + 1);
				insert_shortname(clean_alt, skin_tone_alt, child_code_point.clone());
			}
		}
	}

	let dest_path = Path::new(&env::var("OUT_DIR").unwrap()).join("emoji.rs");
	let mut file = File::create(&dest_path).expect("failed to create target file");

	writeln!(
		&mut file,
		r#"/// Mapping from emoji shortname to emoji character, including skin tones.
pub static EMOJI_BY_SHORTNAME: phf::Map<&'static str, &'static str> = {};"#,
		shortname_to_codepoint.build()
	)
	.unwrap();

	// Rebuild the set because phf doesn't dedup
	let emoji_shortname_chars =
		emoji_shortname_chars
			.into_iter()
			.fold(Set::new(), |mut acc, byte| {
				acc.entry(byte);
				acc
			});

	writeln!(
		&mut file,
		r#"/// Chars that are included in at least one emoji shortname.
pub static EMOJI_SHORTNAME_CHARS: phf::Set<char> = {};"#,
		emoji_shortname_chars.build()
	)
	.unwrap();

	let emoji_code_points = code_points
		.into_iter()
		.fold(Set::new(), |mut acc, code_point| {
			acc.entry(code_point);
			acc
		});

	writeln!(
		&mut file,
		r#"/// Code points that are valid emoji.
pub static CODE_POINTS: phf::Set<&'static str> = {};"#,
		emoji_code_points.build()
	)
	.unwrap();
}

fn hex_code_points(emoji: &EmojiData) -> &str {
	emoji
		.code_points
		.fully_qualified
		.as_ref()
		.unwrap_or(&emoji.code_points.base)
}

/// The emoji an entry spells, with the omitted variation selector restored.
fn fully_qualified(emoji: &EmojiData, needs_variation_selector: &HashSet<&str>) -> String {
	let code_points = hex_code_points(emoji);
	let mut emoji = decode_hex_emoji(code_points);

	if code_points
		.rsplit('-')
		.next()
		.is_some_and(|last| needs_variation_selector.contains(last))
	{
		emoji.push(VARIATION_SELECTOR_16);
	}

	emoji
}

fn decode_hex_emoji(hex_string: &str) -> String {
	hex_string
		.split('-')
		.filter_map(|hex| u32::from_str_radix(hex, 16).ok().and_then(char::from_u32))
		.collect()
}

/// [`Map::entry`] takes its value as raw source, unlike [`Set::entry`].
fn rust_literal(emoji: &str) -> String {
	let unicode = emoji
		.chars()
		.flat_map(char::escape_unicode)
		.collect::<String>();

	format!("\"{unicode}\"")
}
