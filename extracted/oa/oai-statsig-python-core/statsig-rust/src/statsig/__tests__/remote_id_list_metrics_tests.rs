use super::*;
use crate::observability::ops_stats::OpsStatsEvent;

#[test]
fn emits_each_cache_hit_and_counts_each_late_comparison_once() {
    let observer = Arc::new(OpsStatsForInstance::new());
    let mut events = observer.subscribe_for_test();
    let metrics = RemoteIdListMetrics {
        observer: Some(observer),
    };

    let pending = LocalFallbackCounts::default();
    pending.add(Some(false));
    pending.add(Some(false));
    metrics.record_completed_fallbacks("members", &pending, true);
    // A timeout that registers after completion drains only its own outstanding count.
    pending.add(None);
    metrics.record_completed_fallbacks("members", &pending, true);
    metrics.record_cache_hit("teams", Some(true), true);
    metrics.record_cache_hit("teams", Some(true), true);

    let mut actual = Vec::new();
    while let Ok(OpsStatsEvent::Observability(event)) = events.try_recv() {
        let tags = event.tags.unwrap();
        assert_eq!(tags["mode"], "compare");
        actual.push((tags["list"].clone(), tags["result"].clone(), event.value));
    }
    actual.sort_by(|a, b| (&a.0, &a.1).cmp(&(&b.0, &b.1)));
    assert_eq!(
        actual,
        [
            ("members".into(), "before_ready_local_missing".into(), 1.0),
            ("members".into(), "before_ready_mismatch".into(), 2.0),
            ("teams".into(), "cache_hit".into(), 1.0),
            ("teams".into(), "cache_hit".into(), 1.0),
            ("teams".into(), "ready_match".into(), 1.0),
            ("teams".into(), "ready_match".into(), 1.0),
        ]
    );
}
