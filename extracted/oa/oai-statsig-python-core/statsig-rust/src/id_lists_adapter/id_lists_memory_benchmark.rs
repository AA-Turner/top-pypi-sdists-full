//! Opt-in process-memory benchmark driven by an external `/proc` sampler.
//!
//! This deliberately exercises SpecStore publication and IdList updates rather
//! than a second implementation of the set. All identifiers are synthetic.

use super::{IdListMetadata, IdListUpdate, IdListsUpdateListener};
use crate::sdk_event_emitter::SdkEventEmitter;
use crate::spec_store::{SpecStore, SpecStoreData};
use crate::statsig_runtime::StatsigRuntime;
use serde_json::json;
use std::collections::HashMap;
use std::hint::black_box;
use std::io::{self, Write};
use std::sync::Arc;
use std::time::Instant;

fn key(mut value: usize) -> String {
    const ALPHABET: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let mut bytes = [b'A'; 8];
    for byte in &mut bytes {
        *byte = ALPHABET[value & 63];
        value >>= 6;
    }
    String::from_utf8(bytes.to_vec()).unwrap()
}

fn metadata(index: usize) -> IdListMetadata {
    IdListMetadata {
        name: format!("synthetic-{index}"),
        url: format!("https://unused.invalid/synthetic-{index}"),
        file_id: Some("synthetic-generation-1".into()),
        size: 0,
        creation_time: 1,
    }
}

fn checkpoint(phase: &str, elapsed_ms: f64, counts: &[usize]) {
    println!(
        "ID_LIST_BENCH {}",
        json!({
            "phase": phase,
            "elapsed_ms": elapsed_ms,
            "pid": std::process::id(),
            "lists": counts.len(),
            "memberships": counts.iter().sum::<usize>(),
        })
    );
    io::stdout().flush().unwrap();
    let mut input = String::new();
    assert!(io::stdin().read_line(&mut input).unwrap() > 0);
}

fn check_snapshot(data: &SpecStoreData, counts: &[usize], generation: usize, sparse: usize) {
    assert_eq!(data.id_lists.len(), counts.len());
    for (index, count) in counts.iter().copied().enumerate() {
        let list = &data.id_lists[&metadata(index).name];
        assert_eq!(list.ids.len(), count);
        let changed = usize::from(generation > 0) + usize::from(generation > 1 && index == sparse);
        assert_eq!(list.ids.contains(&key(0)), changed == 0);
        assert_eq!(list.ids.contains(&key(count)), changed > 0);
        assert_eq!(list.ids.contains(&key(count + 1)), changed > 1);
        if count > 1 {
            assert_eq!(list.ids.contains(&key(1)), changed < 2);
        }
        assert!(!list.ids.contains(&key(count + 2)));
    }
}

fn updates(
    counts: &[usize],
    initial: bool,
    sparse: Option<usize>,
) -> HashMap<String, IdListUpdate> {
    counts
        .iter()
        .copied()
        .enumerate()
        .map(|(index, count)| {
            let metadata = metadata(index);
            let raw_changeset = if initial {
                let mut body = String::with_capacity(count * 10);
                for id in 0..count {
                    body.push('+');
                    body.push_str(&key(id));
                    body.push('\n');
                }
                Some(body)
            } else if sparse.is_none() || sparse == Some(index) {
                let offset = usize::from(sparse.is_some());
                Some(format!("+{}\n-{}\n", key(count + offset), key(offset)))
            } else {
                // The real listener takes a complete manifest. Unchanged lists
                // must stay present with no changeset or they would be removed.
                None
            };
            (
                metadata.name.clone(),
                IdListUpdate {
                    new_metadata: metadata,
                    raw_changeset,
                },
            )
        })
        .collect()
}

#[test]
#[ignore = "large opt-in memory benchmark; requires external checkpoint driver"]
fn id_list_memory_benchmark() {
    let path = std::env::var("STATSIG_ID_LIST_BENCH_COUNTS").expect("counts file required");
    let counts: Vec<usize> = std::fs::read_to_string(path)
        .unwrap()
        .split_whitespace()
        .map(|item| item.parse().unwrap())
        .collect();
    assert!(!counts.is_empty() && counts.iter().all(|count| *count >= 2));
    let sparse = counts
        .iter()
        .enumerate()
        .max_by_key(|(_, count)| *count)
        .unwrap()
        .0;
    let store = SpecStore::new(
        "synthetic-memory-benchmark",
        "synthetic-memory-benchmark".into(),
        StatsigRuntime::get_runtime_with_thread_count(Some(1)),
        Arc::new(SdkEventEmitter::default()),
        None,
    );
    checkpoint("empty", 0.0, &counts);

    let started = Instant::now();
    store.did_receive_id_list_updates(updates(&counts, true, None));
    let build_ms = started.elapsed().as_secs_f64() * 1000.0;
    check_snapshot(&store.load_data(), &counts, 0, sparse);
    checkpoint("steady", build_ms, &counts);

    let initial = store.load_data();
    let started = Instant::now();
    store.did_receive_id_list_updates(updates(&counts, false, None));
    let update_ms = started.elapsed().as_secs_f64() * 1000.0;
    check_snapshot(&initial, &counts, 0, sparse);
    check_snapshot(&store.load_data(), &counts, 1, sparse);
    checkpoint("all_updated_old_pinned", update_ms, &counts);
    drop(initial);
    checkpoint("all_updated_released", 0.0, &counts);

    let before_sparse = store.load_data();
    let started = Instant::now();
    store.did_receive_id_list_updates(updates(&counts, false, Some(sparse)));
    let sparse_ms = started.elapsed().as_secs_f64() * 1000.0;
    check_snapshot(&before_sparse, &counts, 1, sparse);
    check_snapshot(&store.load_data(), &counts, 2, sparse);
    checkpoint("sparse_updated_old_pinned", sparse_ms, &counts);
    drop(before_sparse);
    checkpoint("sparse_updated_released", 0.0, &counts);

    // Precompute keys so the measured lookup loop measures membership checks,
    // not identifier formatting. Every list gets both a hit and a miss.
    let queries: Vec<_> = counts
        .iter()
        .map(|count| (key(*count), key(*count + 2)))
        .collect();
    let repeats = std::env::var("STATSIG_ID_LIST_BENCH_LOOKUPS")
        .map_or(10_000, |value| value.parse::<usize>().unwrap());
    let data = store.load_data();
    let lists: Vec<_> = (0..counts.len())
        .map(|i| &data.id_lists[&metadata(i).name])
        .collect();
    let started = Instant::now();
    let mut hits = 0;
    for _ in 0..repeats {
        for (list, (present, absent)) in lists.iter().zip(&queries) {
            hits += usize::from(black_box(list.ids.contains(black_box(present))));
            hits += usize::from(black_box(list.ids.contains(black_box(absent))));
        }
    }
    assert_eq!(hits, repeats * lists.len());
    let lookup_ms = started.elapsed().as_secs_f64() * 1000.0;
    checkpoint("lookup", lookup_ms, &counts);

    // Spread probes over the actual tables instead of revisiting one hot bucket.
    // Key preparation is outside the timer and after the steady memory phases.
    drop(queries);
    let distributed: Vec<Vec<(String, String)>> = counts
        .iter()
        .map(|count| {
            (0..512)
                .map(|index| {
                    let present = if *count > 2 {
                        2 + (index * 104_729) % (count - 2)
                    } else {
                        *count
                    };
                    (key(present), key(count + 2 + index))
                })
                .collect()
        })
        .collect();
    let distributed_repeats = (repeats / 512).max(1);
    let started = Instant::now();
    let mut hits = 0;
    for _ in 0..distributed_repeats {
        for (list, queries) in lists.iter().zip(&distributed) {
            for (present, absent) in queries {
                hits += usize::from(black_box(list.ids.contains(black_box(present))));
                hits += usize::from(black_box(list.ids.contains(black_box(absent))));
            }
        }
    }
    assert_eq!(hits, distributed_repeats * lists.len() * 512);
    let lookup_ms = started.elapsed().as_secs_f64() * 1000.0;
    checkpoint("lookup_distributed", lookup_ms, &counts);
    black_box(data);
}
