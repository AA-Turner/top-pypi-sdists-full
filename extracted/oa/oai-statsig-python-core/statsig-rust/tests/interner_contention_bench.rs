use std::{
    collections::HashMap,
    hint::black_box,
    sync::{Arc, Barrier},
    time::Instant,
};

use statsig_rust::{
    evaluation::dynamic_returnable::DynamicReturnable, interned_string::InternedString,
};

#[test]
#[ignore = "manual benchmark; run in release mode with --ignored --nocapture"]
fn benchmark_concurrent_interned_handle_drops() {
    let thread_count = env_usize("INTERNER_BENCH_THREADS", 32);
    let iterations = env_usize("INTERNER_BENCH_ITERATIONS", 1_000);
    let batch_size = env_usize("INTERNER_BENCH_BATCH_SIZE", 128);

    let string = Arc::new(InternedString::from_str_ref("initialize_benchmark_gate"));
    let returnable = Arc::new(DynamicReturnable::from_map(HashMap::from([
        (
            "string".to_owned(),
            serde_json::Value::String("initialize benchmark".to_owned()),
        ),
        ("number".to_owned(), serde_json::Value::from(42)),
    ])));
    let start = Arc::new(Barrier::new(thread_count + 1));

    let threads = (0..thread_count)
        .map(|_| {
            let string = Arc::clone(&string);
            let returnable = Arc::clone(&returnable);
            let start = Arc::clone(&start);
            std::thread::spawn(move || {
                start.wait();
                let mut checksum = 0usize;
                for _ in 0..iterations {
                    let batch = (0..batch_size)
                        .map(|_| ((*string).clone(), (*returnable).clone()))
                        .collect::<Vec<_>>();
                    checksum ^= black_box(batch.len());
                    drop(batch);
                }
                checksum
            })
        })
        .collect::<Vec<_>>();

    start.wait();
    let started = Instant::now();
    let checksum = threads
        .into_iter()
        .map(|thread| thread.join().expect("benchmark thread should finish"))
        .fold(0usize, |acc, value| acc ^ value);
    let elapsed = started.elapsed();
    let handle_drops = thread_count * iterations * batch_size * 2;
    let drops_per_second = handle_drops as f64 / elapsed.as_secs_f64();

    println!(
        "interner_contention_bench threads={thread_count} iterations={iterations} batch_size={batch_size} handle_drops={handle_drops} elapsed_ms={:.3} drops_per_second={drops_per_second:.0} checksum={checksum}",
        elapsed.as_secs_f64() * 1_000.0,
    );
}

fn env_usize(name: &str, default: usize) -> usize {
    std::env::var(name)
        .ok()
        .and_then(|value| value.parse().ok())
        .filter(|value| *value > 0)
        .unwrap_or(default)
}
