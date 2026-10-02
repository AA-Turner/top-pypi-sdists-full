//! Benchmarks for the masked link text guard (`has_no_url`).
//!
//! The guard scans the text segment of `[TEXT](url)` for anything that parses as a URL. It is
//! quadratic in the worst case — every candidate offset re-scans the link-char run that follows it
//! — so the cases below are built to pin the density of candidate offsets rather than raw length.

use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion};
use discord_markdown::Options;
use nom::error::Error;
use std::fs;

/// Roughly the Discord message length limit, which is the largest text segment that can reach the
/// guard in practice.
const MESSAGE_LIMIT: usize = 4_000;

/// Bodies sized to ~[`MESSAGE_LIMIT`], each a different density of candidate URL offsets.
fn bodies() -> Vec<(&'static str, String)> {
	vec![
		// Scheme-shaped but with no `:`, so the prefix filter rejects every offset.
		("http_repeat", "http".repeat(1_000)),
		("dev_repeat", "dev".repeat(1_333)),
		("discord_repeat", "discord".repeat(571)),
		// Scheme-shaped with a `:`, so every offset costs a full link-char scan and URL parse.
		("dev_colon_repeat", "dev:".repeat(1_000)),
		("http_colon_repeat", "http:".repeat(800)),
		("https_colon_repeat", "https:".repeat(666)),
		("discord_colon_repeat", "discord:".repeat(500)),
		// Schemaless domains, which need no `:` to be candidates.
		("discord_gg_repeat", "discord.gg".repeat(400)),
		("discordapp_com_repeat", "discordapp.com".repeat(285)),
		// Uppercase variants, only candidates once the scan is case insensitive.
		("dev_colon_upper_repeat", "DEV:".repeat(1_000)),
		("http_colon_upper_repeat", "HTTP:".repeat(800)),
		// Pure prefilter: every byte is scanned, no offset is ever a candidate.
		("d_repeat", "d".repeat(MESSAGE_LIMIT)),
		("h_repeat", "h".repeat(MESSAGE_LIMIT)),
		// No scanned byte at all, the floor for the guard.
		("x_repeat", "x".repeat(MESSAGE_LIMIT)),
	]
}

fn bench_guard(c: &mut Criterion) {
	for (name, body) in bodies() {
		// A complete masked link, so the guard actually runs.
		let masked = format!("[{body}](https://example.com)");
		c.bench_with_input(
			BenchmarkId::new("masked_link::guard", name),
			&masked,
			|b, text| {
				b.iter(|| {
					discord_markdown::parse::<(), Error<_>>(text.as_str(), Options::default())
				})
			},
		);

		// The same body with no `](`, so `ByteHint::Absent` short circuits before the guard. The
		// delta against the case above is the cost of the guard itself.
		let bare = format!("[{body}]");
		c.bench_with_input(
			BenchmarkId::new("masked_link::no_guard", name),
			&bare,
			|b, text| {
				b.iter(|| {
					discord_markdown::parse::<(), Error<_>>(text.as_str(), Options::default())
				})
			},
		);
	}
}

/// Doubling the body length should roughly quadruple the time, confirming the guard stays
/// quadratic and has not become something worse.
fn bench_scaling(c: &mut Criterion) {
	for n in [500, 1_000, 2_000] {
		let s = format!("[{}](https://example.com)", "dev:".repeat(n));
		c.bench_with_input(
			BenchmarkId::new("masked_link::scaling/dev_colon", n),
			&s,
			|b, text| {
				b.iter(|| {
					discord_markdown::parse::<(), Error<_>>(text.as_str(), Options::default())
				})
			},
		);
	}
}

/// Content that should not be affected by the guard at all.
fn bench_benign(c: &mut Criterion) {
	let repeated_links = "[Discord](https://discord.com) ".repeat(130);
	c.bench_with_input(
		BenchmarkId::new("masked_link::benign", "repeated_links"),
		&repeated_links,
		|b, text| {
			b.iter(|| discord_markdown::parse::<(), Error<_>>(text.as_str(), Options::default()))
		},
	);

	for corpus in [
		"discordjs_announcement",
		"helldivers_announcement",
		"ddevs_announcement",
	] {
		let text = fs::read_to_string(format!("test_content/{corpus}/content.md")).unwrap();
		c.bench_with_input(
			BenchmarkId::new("masked_link::benign", corpus),
			&text,
			|b, text| {
				b.iter(|| discord_markdown::parse::<(), Error<_>>(&**text, Options::default()))
			},
		);
	}
}

criterion_group!(benches, bench_guard, bench_scaling, bench_benign);
criterion_main!(benches);
