use discord_markdown::Options;
use gungraun::prelude::*;
use nom::error::Error;
use std::fs;
use std::hint::black_box;

fn corpus(name: &str) -> String {
	fs::read_to_string(format!("test_content/{name}/content.md")).unwrap()
}

/// 1,000 opens, an `x`, then 1,000 closes.
fn nested(open: &str, close: &str) -> String {
	open.repeat(1_000) + "x" + &close.repeat(1_000)
}

#[library_benchmark]
#[bench::discordjs_announcement(args = ("discordjs_announcement"), setup = corpus)]
#[bench::helldivers_announcement(args = ("helldivers_announcement"), setup = corpus)]
#[bench::ddevs_announcement(args = ("ddevs_announcement"), setup = corpus)]
#[bench::paren(args = ("(", ")"), setup = nested)]
#[bench::angle(args = ("<", ">"), setup = nested)]
#[bench::bracket(args = ("[", "]"), setup = nested)]
#[bench::brace(args = ("{", "}"), setup = nested)]
#[bench::strikethrough(args = ("~~", "~~"), setup = nested)]
#[bench::underscore(args = ("_", "_"), setup = nested)]
#[bench::underline(args = ("__", "__"), setup = nested)]
#[bench::italic(args = ("*", "*"), setup = nested)]
#[bench::bold(args = ("**", "**"), setup = nested)]
#[bench::angle_url(args = ("<", ":/"), setup = nested)]
#[bench::angle_emoji(args = ("<:", ":>"), setup = nested)]
fn parse(text: String) {
	let _ = black_box(discord_markdown::parse::<(), Error<_>>(
		black_box(text.as_str()),
		Options::default(),
	));
}

library_benchmark_group!(name = parser, benchmarks = parse);
main!(library_benchmark_groups = parser);
