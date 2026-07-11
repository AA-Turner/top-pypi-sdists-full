use std::{
    collections::VecDeque,
    hint::black_box,
    time::{Duration, Instant},
};

use memchr::memchr2;

use super::{Token, TokenWindow, Tokenizer, TokenizerResult};

const CORPUS: &str = include_str!("../../../../../tests/data/test_user_agents.txt");
const EDGE_CASES: &[&str] = &[
    "",
    " ",
    ";",
    "  leading;;and  repeated;delimiters  ",
    "Mozilla/5.0\t(Windows NT 10.0)\nChrome/134.0",
    "机器人/1.0 (兼容; Android 14; 设备 🚀) crawler/2.0",
    "Mözilla/5.0 (X11; Línux x86_64) Brøwser/1.2.3",
    "e\u{301}/1.0; café/2.0; 東京/3.0",
    "non\u{a0}breaking\u{a0}spaces/1.0; regular delimiter",
    "quoted/1.0 (\"odd; value\") +bot/3.0",
    ";;;;    ; ; trailing;",
];

#[test]
fn memchr_window_preserves_legacy_tokenizer_results() {
    for user_agent in corpus().into_iter().chain(EDGE_CASES.iter().copied()) {
        assert_equivalent(user_agent);
    }

    let long_odd_input = format!(
        "{}; {};{}  {}",
        "é".repeat(400),
        "token".repeat(100),
        "🚀".repeat(200),
        "tail".repeat(100)
    );
    assert_equivalent(&long_odd_input);
}

#[test]
#[ignore = "manual benchmark; run with --release --ignored --nocapture"]
fn benchmark_memchr_window_against_legacy_tokenizer() {
    let corpus = corpus();
    let samples = std::env::var("UA_BENCH_SAMPLES")
        .ok()
        .and_then(|value| value.parse().ok())
        .unwrap_or(31);
    let warmup = std::env::var("UA_BENCH_WARMUP")
        .ok()
        .and_then(|value| value.parse().ok())
        .unwrap_or(5);

    for _ in 0..warmup {
        black_box(run_candidate(&corpus));
        black_box(run_memchr_deque(&corpus));
        black_box(run_std_array(&corpus));
        black_box(run_legacy(&corpus));
    }

    let mut candidate = Vec::with_capacity(samples);
    let mut memchr_deque = Vec::with_capacity(samples);
    let mut std_array = Vec::with_capacity(samples);
    let mut legacy = Vec::with_capacity(samples);
    for sample in 0..samples {
        match sample % 4 {
            0 => {
                candidate.push(measure(|| run_candidate(&corpus)));
                memchr_deque.push(measure(|| run_memchr_deque(&corpus)));
                std_array.push(measure(|| run_std_array(&corpus)));
                legacy.push(measure(|| run_legacy(&corpus)));
            }
            1 => {
                memchr_deque.push(measure(|| run_memchr_deque(&corpus)));
                std_array.push(measure(|| run_std_array(&corpus)));
                legacy.push(measure(|| run_legacy(&corpus)));
                candidate.push(measure(|| run_candidate(&corpus)));
            }
            2 => {
                std_array.push(measure(|| run_std_array(&corpus)));
                legacy.push(measure(|| run_legacy(&corpus)));
                candidate.push(measure(|| run_candidate(&corpus)));
                memchr_deque.push(measure(|| run_memchr_deque(&corpus)));
            }
            _ => {
                legacy.push(measure(|| run_legacy(&corpus)));
                candidate.push(measure(|| run_candidate(&corpus)));
                memchr_deque.push(measure(|| run_memchr_deque(&corpus)));
                std_array.push(measure(|| run_std_array(&corpus)));
            }
        }
    }

    let candidate_stats = BenchStats::new(candidate, corpus.len());
    let memchr_deque_stats = BenchStats::new(memchr_deque, corpus.len());
    let std_array_stats = BenchStats::new(std_array, corpus.len());
    let legacy_stats = BenchStats::new(legacy, corpus.len());

    println!(
        "user_agent_tokenizer_bench corpus={} samples={} warmup={}",
        corpus.len(),
        samples,
        warmup
    );
    legacy_stats.print("legacy std::str::split");
    memchr_deque_stats.print("memchr2 + VecDeque");
    std_array_stats.print("std::split + array");
    candidate_stats.print("memchr2 + array");
    println!(
        "median_saved_pct memchr_only={:.2}% array_only={:.2}% combined={:.2}%",
        legacy_stats.saved_pct(&memchr_deque_stats),
        legacy_stats.saved_pct(&std_array_stats),
        legacy_stats.saved_pct(&candidate_stats),
    );
}

fn corpus() -> Vec<&'static str> {
    CORPUS
        .lines()
        .skip(1)
        .filter_map(|line| line.split_once('|').map(|(user_agent, _)| user_agent))
        .chain(EDGE_CASES.iter().copied())
        .collect()
}

fn assert_equivalent(input: &str) {
    let candidate = Tokenizer::run(input);
    let memchr_deque =
        Tokenizer::run_with_window(DequeWindow::new(TestAsciiDelimiterSplit::new(input)));
    let std_array = Tokenizer::run_with_window(ArrayWindow::new(input.split([';', ' '])));
    let legacy = Tokenizer::run_with_window(DequeWindow::new(input.split([';', ' '])));

    assert_result_eq(&candidate, &legacy, input);
    assert_result_eq(&memchr_deque, &legacy, input);
    assert_result_eq(&std_array, &legacy, input);
}

fn assert_result_eq(candidate: &TokenizerResult<'_>, legacy: &TokenizerResult<'_>, input: &str) {
    assert_eq!(candidate.position, legacy.position, "input: {input:?}");
    assert_eq!(
        candidate.tokens.len(),
        legacy.tokens.len(),
        "input: {input:?}"
    );
    for (candidate, legacy) in candidate.tokens.iter().zip(&legacy.tokens) {
        assert_eq!(candidate.position, legacy.position, "input: {input:?}");
        assert_eq!(candidate.tag, legacy.tag, "input: {input:?}");
        assert_eq!(candidate.version, legacy.version, "input: {input:?}");
    }
    assert_token_eq(
        candidate.possible_os_token.as_ref(),
        legacy.possible_os_token.as_ref(),
        input,
    );
    assert_token_eq(
        candidate.possible_browser_token.as_ref(),
        legacy.possible_browser_token.as_ref(),
        input,
    );
    assert_eq!(candidate.linux_hint, legacy.linux_hint, "input: {input:?}");
    assert_eq!(candidate.ios_hint, legacy.ios_hint, "input: {input:?}");
    assert_eq!(candidate.macos_hint, legacy.macos_hint, "input: {input:?}");
    assert_eq!(
        candidate.windows_hint, legacy.windows_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.mobile_hint, legacy.mobile_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.safari_hint, legacy.safari_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.playstation_hint, legacy.playstation_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.huawei_hint, legacy.huawei_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.cfnetwork_hint, legacy.cfnetwork_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.crawler_hint, legacy.crawler_hint,
        "input: {input:?}"
    );
    assert_eq!(
        candidate.bot_detected, legacy.bot_detected,
        "input: {input:?}"
    );
}

fn assert_token_eq(candidate: Option<&Token<'_>>, legacy: Option<&Token<'_>>, input: &str) {
    assert_eq!(
        candidate.map(|token| (token.position, token.tag, token.version)),
        legacy.map(|token| (token.position, token.tag, token.version)),
        "input: {input:?}"
    );
}

fn run_candidate(corpus: &[&str]) -> usize {
    run(corpus, Tokenizer::run)
}

fn run_legacy(corpus: &[&str]) -> usize {
    run(corpus, |user_agent| {
        Tokenizer::run_with_window(DequeWindow::new(user_agent.split([';', ' '])))
    })
}

fn run_memchr_deque(corpus: &[&str]) -> usize {
    run(corpus, |user_agent| {
        Tokenizer::run_with_window(DequeWindow::new(TestAsciiDelimiterSplit::new(user_agent)))
    })
}

fn run_std_array(corpus: &[&str]) -> usize {
    run(corpus, |user_agent| {
        Tokenizer::run_with_window(ArrayWindow::new(user_agent.split([';', ' '])))
    })
}

struct DequeWindow<'a, I> {
    iter: I,
    window: VecDeque<&'a str>,
}

impl<'a, I: Iterator<Item = &'a str>> DequeWindow<'a, I> {
    fn new(mut iter: I) -> Self {
        let mut window = VecDeque::new();
        for _ in 0..4 {
            if let Some(word) = iter.next() {
                window.push_back(word);
            }
        }

        Self { iter, window }
    }
}

impl<'a, I: Iterator<Item = &'a str>> TokenWindow<'a> for DequeWindow<'a, I> {
    #[allow(clippy::get_first)]
    fn get_window(
        &self,
    ) -> (
        Option<&'a str>,
        Option<&'a str>,
        Option<&'a str>,
        Option<&'a str>,
    ) {
        (
            self.window.get(0).copied(),
            self.window.get(1).copied(),
            self.window.get(2).copied(),
            self.window.get(3).copied(),
        )
    }

    fn slide_window_by(&mut self, n: usize) {
        for _ in 0..n {
            self.window.pop_front();
            if let Some(word) = self.iter.next() {
                self.window.push_back(word);
            }
        }
    }

    fn is_empty(&self) -> bool {
        self.window.is_empty()
    }
}

struct ArrayWindow<'a, I> {
    iter: I,
    window: [Option<&'a str>; 4],
}

impl<'a, I: Iterator<Item = &'a str>> ArrayWindow<'a, I> {
    fn new(mut iter: I) -> Self {
        let window = std::array::from_fn(|_| iter.next());
        Self { iter, window }
    }
}

impl<'a, I: Iterator<Item = &'a str>> TokenWindow<'a> for ArrayWindow<'a, I> {
    fn get_window(
        &self,
    ) -> (
        Option<&'a str>,
        Option<&'a str>,
        Option<&'a str>,
        Option<&'a str>,
    ) {
        let [curr, next1, next2, next3] = self.window;
        (curr, next1, next2, next3)
    }

    fn slide_window_by(&mut self, n: usize) {
        for _ in 0..n {
            self.window.rotate_left(1);
            self.window[3] = self.iter.next();
        }
    }

    fn is_empty(&self) -> bool {
        self.window[0].is_none()
    }
}

struct TestAsciiDelimiterSplit<'a> {
    remainder: Option<&'a str>,
}

impl<'a> TestAsciiDelimiterSplit<'a> {
    fn new(input: &'a str) -> Self {
        Self {
            remainder: Some(input),
        }
    }
}

impl<'a> Iterator for TestAsciiDelimiterSplit<'a> {
    type Item = &'a str;

    fn next(&mut self) -> Option<Self::Item> {
        let remainder = self.remainder.take()?;
        let Some(delimiter) = memchr2(b';', b' ', remainder.as_bytes()) else {
            return Some(remainder);
        };

        let (word, rest) = remainder.split_at(delimiter);
        self.remainder = Some(&rest[1..]);
        Some(word)
    }
}

fn run<'a>(
    corpus: &'a [&'a str],
    mut tokenize: impl FnMut(&'a str) -> TokenizerResult<'a>,
) -> usize {
    let mut checksum = 0;
    for user_agent in corpus {
        let result = black_box(tokenize(black_box(user_agent)));
        checksum = black_box(
            checksum
                ^ result.tokens.len()
                ^ result.position
                ^ usize::from(result.bot_detected)
                ^ usize::from(result.crawler_hint),
        );
    }
    checksum
}

fn measure(mut run: impl FnMut() -> usize) -> Duration {
    let start = Instant::now();
    black_box(run());
    start.elapsed()
}

struct BenchStats {
    median: f64,
    p95: f64,
    median_ns_per_user_agent: f64,
}

impl BenchStats {
    fn new(mut samples: Vec<Duration>, corpus_len: usize) -> Self {
        samples.sort_unstable();
        let median = percentile(&samples, 0.50).as_secs_f64() * 1_000.0;
        let p95 = percentile(&samples, 0.95).as_secs_f64() * 1_000.0;
        Self {
            median,
            p95,
            median_ns_per_user_agent: median * 1_000_000.0 / corpus_len as f64,
        }
    }

    fn print(&self, name: &str) {
        println!(
            "{name:<24} median={:>9.3}ms p95={:>9.3}ms median={:>9.1}ns/ua",
            self.median, self.p95, self.median_ns_per_user_agent
        );
    }

    fn saved_pct(&self, candidate: &Self) -> f64 {
        (self.median - candidate.median) / self.median * 100.0
    }
}

fn percentile(samples: &[Duration], percentile: f64) -> Duration {
    let index = ((samples.len() - 1) as f64 * percentile).round() as usize;
    samples[index]
}
