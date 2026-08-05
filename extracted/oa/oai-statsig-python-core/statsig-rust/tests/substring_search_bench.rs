use std::hint::black_box;
use std::time::{Duration, Instant};

const SAMPLE_COUNT: usize = 31;
const TARGET_SAMPLE_TIME: Duration = Duration::from_millis(30);

struct Scenario {
    name: &'static str,
    haystack: &'static str,
    needles: &'static [&'static str],
    expected: bool,
}

const LONG_CUSTOM_FIELD: &str = concat!(
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "tenant=openai;environment=production;region=us-west-2;workspace=enterprise;",
    "feature=bulk-evaluation;release=2026.06.27;cohort=employee;plan=business;",
    "target=statsig-rust-core",
);

const SCENARIOS: &[Scenario] = &[
    Scenario {
        name: "email_hit_first",
        haystack: "daniel@statsig.com",
        needles: &["@statsig.com", "@statsig.io"],
        expected: true,
    },
    Scenario {
        name: "email_hit_second",
        haystack: "daniel@statsig.com",
        needles: &["@example.com", "@statsig.com"],
        expected: true,
    },
    Scenario {
        name: "email_miss",
        haystack: "daniel@example.com",
        needles: &["@statsig.com", "@statsig.io"],
        expected: false,
    },
    Scenario {
        name: "short_needle_1_hit",
        haystack: "environment=production",
        needles: &["p"],
        expected: true,
    },
    Scenario {
        name: "short_needle_1_miss",
        haystack: "environment=production",
        needles: &["/"],
        expected: false,
    },
    Scenario {
        name: "short_needle_2_hit",
        haystack: "environment=production",
        needles: &["on"],
        expected: true,
    },
    Scenario {
        name: "short_needle_2_miss",
        haystack: "environment=production",
        needles: &["zz"],
        expected: false,
    },
    Scenario {
        name: "short_needle_3_hit",
        haystack: "environment=production",
        needles: &["pro"],
        expected: true,
    },
    Scenario {
        name: "short_needle_3_miss",
        haystack: "environment=production",
        needles: &["xyz"],
        expected: false,
    },
    Scenario {
        name: "short_needle_4_hit",
        haystack: "environment=production",
        needles: &["prod"],
        expected: true,
    },
    Scenario {
        name: "short_needle_4_miss",
        haystack: "environment=production",
        needles: &["test"],
        expected: false,
    },
    Scenario {
        name: "user_agent_hit_third",
        haystack: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        needles: &["Googlebot", "Firefox/", "Chrome/126.0.0.0", "curl/"],
        expected: true,
    },
    Scenario {
        name: "user_agent_miss_many",
        haystack: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        needles: &[
            "Googlebot",
            "Firefox/",
            "Edg/",
            "curl/",
            "PostmanRuntime",
            "okhttp",
        ],
        expected: false,
    },
    Scenario {
        name: "long_custom_field_hit_last",
        haystack: LONG_CUSTOM_FIELD,
        needles: &[
            "tier=staging",
            "region=eu-west-1",
            "workspace=consumer",
            "feature=legacy-evaluation",
            "cohort=external",
            "target=statsig-rust-core",
        ],
        expected: true,
    },
    Scenario {
        name: "long_custom_field_miss_many",
        haystack: LONG_CUSTOM_FIELD,
        needles: &[
            "tier=staging",
            "region=eu-west-1",
            "workspace=consumer",
            "feature=legacy-evaluation",
            "cohort=external",
            "target=statsig-node-core",
        ],
        expected: false,
    },
];

#[test]
#[ignore = "manual benchmark; run in release mode with --ignored --nocapture"]
fn benchmark_std_contains_against_memmem() {
    println!(
        "substring search benchmark: samples={SAMPLE_COUNT}, target_sample_ms={}\n",
        TARGET_SAMPLE_TIME.as_millis()
    );
    println!(
        "{:<31} {:>9} {:>9} {:>10} {:>13} {:>20}",
        "scenario", "bytes", "needles", "std ns", "candidate ns", "candidate latency"
    );

    for scenario in SCENARIOS {
        assert_eq!(std_contains_any(scenario), scenario.expected);
        assert_eq!(candidate_contains_any(scenario), scenario.expected);

        let iterations = calibrate_iterations(scenario);
        let warmup_iterations = iterations.max(10_000);
        black_box(run_std(scenario, warmup_iterations));
        black_box(run_candidate(scenario, warmup_iterations));

        let mut std_samples = Vec::with_capacity(SAMPLE_COUNT);
        let mut candidate_samples = Vec::with_capacity(SAMPLE_COUNT);
        let mut paired_ratios = Vec::with_capacity(SAMPLE_COUNT);

        for sample_index in 0..SAMPLE_COUNT {
            let (std_ns, candidate_ns) = if sample_index % 2 == 0 {
                let std_ns = measure(iterations, || run_std(scenario, iterations));
                let candidate_ns = measure(iterations, || run_candidate(scenario, iterations));
                (std_ns, candidate_ns)
            } else {
                let candidate_ns = measure(iterations, || run_candidate(scenario, iterations));
                let std_ns = measure(iterations, || run_std(scenario, iterations));
                (std_ns, candidate_ns)
            };
            std_samples.push(std_ns);
            candidate_samples.push(candidate_ns);
            paired_ratios.push(candidate_ns / std_ns);
        }

        std_samples.sort_by(f64::total_cmp);
        candidate_samples.sort_by(f64::total_cmp);
        paired_ratios.sort_by(f64::total_cmp);

        let std_median = percentile(&std_samples, 0.50);
        let candidate_median = percentile(&candidate_samples, 0.50);
        let ratio_median = percentile(&paired_ratios, 0.50);
        println!(
            "{:<31} {:>9} {:>9} {:>10.2} {:>13.2} {:>+19.1}%",
            scenario.name,
            scenario.haystack.len(),
            scenario.needles.len(),
            std_median,
            candidate_median,
            (ratio_median - 1.0) * 100.0,
        );
        println!(
            "  iterations={iterations}; std p10/p90={:.2}/{:.2} ns; candidate p10/p90={:.2}/{:.2} ns; paired delta p10/p90={:+.1}%/{:+.1}%",
            percentile(&std_samples, 0.10),
            percentile(&std_samples, 0.90),
            percentile(&candidate_samples, 0.10),
            percentile(&candidate_samples, 0.90),
            (percentile(&paired_ratios, 0.10) - 1.0) * 100.0,
            (percentile(&paired_ratios, 0.90) - 1.0) * 100.0,
        );
    }
}

#[inline(always)]
fn std_contains_any(scenario: &Scenario) -> bool {
    scenario
        .needles
        .iter()
        .any(|needle| scenario.haystack.contains(*needle))
}

#[inline(always)]
fn candidate_contains_any(scenario: &Scenario) -> bool {
    scenario.needles.iter().any(|needle| {
        if needle.len() <= 1 {
            scenario.haystack.contains(*needle)
        } else {
            memchr::memmem::find(scenario.haystack.as_bytes(), needle.as_bytes()).is_some()
        }
    })
}

#[inline(never)]
fn run_std(scenario: &Scenario, iterations: usize) -> usize {
    let mut matches = 0usize;
    for _ in 0..iterations {
        matches += black_box(std_contains_any(black_box(scenario))) as usize;
    }
    black_box(matches)
}

#[inline(never)]
fn run_candidate(scenario: &Scenario, iterations: usize) -> usize {
    let mut matches = 0usize;
    for _ in 0..iterations {
        matches += black_box(candidate_contains_any(black_box(scenario))) as usize;
    }
    black_box(matches)
}

fn calibrate_iterations(scenario: &Scenario) -> usize {
    let mut iterations = 1_000usize;
    loop {
        let start = Instant::now();
        black_box(run_std(scenario, iterations));
        let elapsed = start.elapsed();
        if elapsed >= TARGET_SAMPLE_TIME || iterations >= 100_000_000 {
            return iterations;
        }

        let scale = (TARGET_SAMPLE_TIME.as_nanos() / elapsed.as_nanos().max(1)) as usize;
        iterations = iterations.saturating_mul(scale.clamp(2, 10));
    }
}

fn measure(iterations: usize, mut run: impl FnMut() -> usize) -> f64 {
    let start = Instant::now();
    black_box(run());
    start.elapsed().as_nanos() as f64 / iterations as f64
}

fn percentile(sorted_samples: &[f64], quantile: f64) -> f64 {
    let index = ((sorted_samples.len() - 1) as f64 * quantile).round() as usize;
    sorted_samples[index]
}
