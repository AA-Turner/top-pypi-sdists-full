use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion};
use discord_markdown::{inline::emoji::unicode::load_emoji_metadata, Options};
use nom::error::Error;
use std::fs;

pub fn bench_parse(c: &mut Criterion) {
	// let text = "_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
	// let text = "_foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_ _foo t_a **bat** <a:abcd:1234><t:1234><@1234> butt_";
	let djs_announcement =
		fs::read_to_string("./test_content/discordjs_announcement/content.md").unwrap();

	let helldivers_announcement =
		fs::read_to_string("test_content/helldivers_announcement/content.md").unwrap();

	let ddevs_announcement =
		fs::read_to_string("test_content/ddevs_announcement/content.md").unwrap();

	c.bench_function("init_emojis", |b| b.iter(load_emoji_metadata));

	c.bench_with_input(
		BenchmarkId::new("parser::parse", "discordjs announcement"),
		&djs_announcement,
		|b, text| {
			b.iter(|| discord_markdown::parse::<(), Error<_>>(&**text, Options::default()));
		},
	);

	c.bench_with_input(
		BenchmarkId::new("parser::parse", "helldivers announcement"),
		&helldivers_announcement,
		|b, text| b.iter(|| discord_markdown::parse::<(), Error<_>>(&**text, Options::default())),
	);

	c.bench_with_input(
		BenchmarkId::new("parser::parse", "ddevs announcement"),
		&ddevs_announcement,
		|b, text| b.iter(|| discord_markdown::parse::<(), Error<_>>(&**text, Options::default())),
	);

	let opens = ["(", "<", "[", "{", "~~", "_", "__", "*", "**", "<", "<:"];
	let closes = [")", ">", "]", "}", "~~", "_", "__", "*", "**", ":/", ":>"];
	for (i, open_c) in opens.iter().enumerate() {
		let close_c = closes[i];
		let open_s = open_c.repeat(1_000);
		let close_s = close_c.repeat(1_000);
		let s = open_s + "x" + &close_s;
		c.bench_with_input(
			BenchmarkId::new("parser::parse", format!("{}{}", open_c, close_c)),
			&s,
			|b, text| {
				b.iter(|| {
					discord_markdown::parse::<(), Error<_>>(text.as_str(), Options::default())
				})
			},
		);
	}
}

criterion_group!(benches, bench_parse);
criterion_main!(benches);
