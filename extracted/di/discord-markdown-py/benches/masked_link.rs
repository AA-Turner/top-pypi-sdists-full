//! Benchmarks for the masked link text guard (`has_no_url`).
//!
//! The guard scans the text segment of `[TEXT](url)` for anything that parses as a URL. It is
//! quadratic in the worst case — every candidate offset re-scans the link-char run that follows it
//! — so the cases below are built to pin the density of candidate offsets rather than raw length.
//!
//! Each body is `unit` repeated `n` times, sized to ~[`MESSAGE_LIMIT`].

use discord_markdown::Options;
use gungraun::prelude::*;
use nom::error::Error;
use std::fs;
use std::hint::black_box;

/// Roughly the Discord message length limit, which is the largest text segment that can reach the
/// guard in practice.
const MESSAGE_LIMIT: usize = 4_000;

fn run(text: &str) {
	let _ = black_box(discord_markdown::parse::<(), Error<_>>(
		black_box(text),
		Options::default(),
	));
}

/// A complete masked link, so the guard actually runs.
fn masked(unit: &str, n: usize) -> String {
	format!("[{}](https://example.com)", unit.repeat(n))
}

/// The same body with no `](`, so `ByteHint::Absent` short circuits before the guard.
fn bare(unit: &str, n: usize) -> String {
	format!("[{}]", unit.repeat(n))
}

fn corpus(name: &str) -> String {
	fs::read_to_string(format!("test_content/{name}/content.md")).unwrap()
}

#[library_benchmark(setup = masked)]
// Scheme-shaped but with no `:`, so the prefix filter rejects every offset.
#[bench::http_repeat("http", 1_000)]
#[bench::dev_repeat("dev", 1_333)]
#[bench::discord_repeat("discord", 571)]
// Scheme-shaped with a `:`, so every offset costs a full link-char scan and URL parse.
#[bench::dev_colon_repeat("dev:", 1_000)]
#[bench::http_colon_repeat("http:", 800)]
#[bench::https_colon_repeat("https:", 666)]
#[bench::discord_colon_repeat("discord:", 500)]
// Schemaless domains, which need no `:` to be candidates.
#[bench::discord_gg_repeat("discord.gg", 400)]
#[bench::discordapp_com_repeat("discordapp.com", 285)]
// Uppercase variants, only candidates once the scan is case insensitive.
#[bench::dev_colon_upper_repeat("DEV:", 1_000)]
#[bench::http_colon_upper_repeat("HTTP:", 800)]
// Pure prefilter: every byte is scanned, no offset is ever a candidate.
#[bench::d_repeat("d", MESSAGE_LIMIT)]
#[bench::h_repeat("h", MESSAGE_LIMIT)]
// No scanned byte at all, the floor for the guard.
#[bench::x_repeat("x", MESSAGE_LIMIT)]
fn guard(text: String) {
	run(&text);
}

// The bodies from `guard` without the guard. With `compare_by_id`, the delta reported against
// `guard` is the cost of the guard itself.
#[library_benchmark(setup = bare)]
#[bench::http_repeat("http", 1_000)]
#[bench::dev_repeat("dev", 1_333)]
#[bench::discord_repeat("discord", 571)]
#[bench::dev_colon_repeat("dev:", 1_000)]
#[bench::http_colon_repeat("http:", 800)]
#[bench::https_colon_repeat("https:", 666)]
#[bench::discord_colon_repeat("discord:", 500)]
#[bench::discord_gg_repeat("discord.gg", 400)]
#[bench::discordapp_com_repeat("discordapp.com", 285)]
#[bench::dev_colon_upper_repeat("DEV:", 1_000)]
#[bench::http_colon_upper_repeat("HTTP:", 800)]
#[bench::d_repeat("d", MESSAGE_LIMIT)]
#[bench::h_repeat("h", MESSAGE_LIMIT)]
#[bench::x_repeat("x", MESSAGE_LIMIT)]
fn no_guard(text: String) {
	run(&text);
}

// Doubling the body length should roughly quadruple the instruction count, confirming the guard
// stays quadratic and has not become something worse.
#[library_benchmark(setup = masked)]
#[bench::dev_colon_500("dev:", 500)]
#[bench::dev_colon_1000("dev:", 1_000)]
#[bench::dev_colon_2000("dev:", 2_000)]
fn scaling(text: String) {
	run(&text);
}

// Content that should not be affected by the guard at all.
#[library_benchmark]
#[bench::repeated_links("[Discord](https://discord.com) ".repeat(130))]
#[bench::discordjs_announcement(args = ("discordjs_announcement"), setup = corpus)]
#[bench::helldivers_announcement(args = ("helldivers_announcement"), setup = corpus)]
#[bench::ddevs_announcement(args = ("ddevs_announcement"), setup = corpus)]
fn benign(text: String) {
	run(&text);
}

library_benchmark_group!(
	name = masked_link,
	compare_by_id = true,
	benchmarks = [guard, no_guard]
);
library_benchmark_group!(name = masked_link_scaling, benchmarks = scaling);
library_benchmark_group!(name = masked_link_benign, benchmarks = benign);
main!(
	library_benchmark_groups = masked_link,
	masked_link_scaling,
	masked_link_benign
);
