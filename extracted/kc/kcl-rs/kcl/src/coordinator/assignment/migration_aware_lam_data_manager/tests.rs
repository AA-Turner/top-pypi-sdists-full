//! Port of `MigrationAwareLAMDataManagerTest`.
//!
//! Java mocks `EntityDAO` + `WorkerMetricStatsDAO` + both delegates + the
//! status provider. Here we use `MockEntityDAO` + `MockWorkerMetricsDao` +
//! `MockWorkerMetricsDelegate` + `MockTableMigrationStatusProvider`, with a
//! summary-capturing closure.

use std::collections::HashMap;
use std::sync::{Arc, Mutex};

use super::*;
use crate::coordinator::migration::table_migration_status_provider::MockTableMigrationStatusProvider;
use crate::leases::{Entity, EntityScanList};
use crate::metrics::NullMetricsScope;

const REPORTER_FREQ_MILLIS: i64 = 60 * 60 * 1000; // 1 hour

fn config() -> WorkerUtilizationAwareAssignmentConfig {
    WorkerUtilizationAwareAssignmentConfig {
        worker_metrics_reporter_freq_in_millis: REPORTER_FREQ_MILLIS,
        stale_worker_metrics_entry_cleanup_duration: Duration::from_secs(1000 * 24 * 60 * 60),
        ..WorkerUtilizationAwareAssignmentConfig::default()
    }
}

fn lease(key: &str, owner: Option<&str>) -> Lease {
    let mut l = Lease::default();
    l.set_lease_key(key);
    if let Some(o) = owner {
        l.set_lease_owner(Some(o.to_string()));
    }
    l.set_lease_counter(10);
    l
}

fn active_wm(worker_id: &str) -> WorkerMetricStats {
    let mut ms = HashMap::new();
    ms.insert("C".to_string(), vec![50.0, 50.0]);
    let mut op = HashMap::new();
    op.insert("C".to_string(), vec![80i64]);
    WorkerMetricStats::legacy_builder()
        .worker_id(worker_id)
        .last_update_time(chrono::Utc::now().timestamp())
        .metric_stats(ms)
        .operating_range(op)
        .build()
}

fn expired_wm(worker_id: &str) -> WorkerMetricStats {
    let mut ms = HashMap::new();
    ms.insert("C".to_string(), vec![50.0, 50.0]);
    let mut op = HashMap::new();
    op.insert("C".to_string(), vec![80i64]);
    WorkerMetricStats::legacy_builder()
        .worker_id(worker_id)
        .last_update_time(0) // epoch 0 = always expired
        .metric_stats(ms)
        .operating_range(op)
        .build()
}

fn invalid_wm(worker_id: &str) -> WorkerMetricStats {
    // no last_update_time -> invalid.
    let mut ms = HashMap::new();
    ms.insert("C".to_string(), vec![50.0, 50.0]);
    let mut op = HashMap::new();
    op.insert("C".to_string(), vec![80i64]);
    WorkerMetricStats::legacy_builder()
        .worker_id(worker_id)
        .metric_stats(ms)
        .operating_range(op)
        .build()
}

fn wm_with_support(
    worker_id: &str,
    support_code: Option<i32>,
    epoch: Option<i64>,
) -> WorkerMetricStats {
    let mut ms = HashMap::new();
    ms.insert("C".to_string(), vec![50.0, 50.0]);
    let mut op = HashMap::new();
    op.insert("C".to_string(), vec![80i64]);
    let mut b = WorkerMetricStats::legacy_builder()
        .worker_id(worker_id)
        .last_update_time(chrono::Utc::now().timestamp())
        .metric_stats(ms)
        .operating_range(op);
    if let Some(sc) = support_code {
        b = b.support_code(sc);
    }
    if let Some(e) = epoch {
        b = b.support_code_update_epoch_seconds(e);
    }
    b.build()
}

fn scan_result(
    leases: Vec<Lease>,
    metrics: Vec<WorkerMetricStats>,
) -> HashMap<EntityType, EntityScanList> {
    scan_result_with_failures(leases, metrics, vec![])
}

fn scan_result_with_failures(
    leases: Vec<Lease>,
    metrics: Vec<WorkerMetricStats>,
    failures: Vec<String>,
) -> HashMap<EntityType, EntityScanList> {
    let lease_entities: Vec<Box<dyn Entity>> = leases
        .into_iter()
        .map(|l| Box::new(l) as Box<dyn Entity>)
        .collect();
    let metric_entities: Vec<Box<dyn Entity>> = metrics
        .into_iter()
        .map(|m| Box::new(m) as Box<dyn Entity>)
        .collect();
    let mut map = HashMap::new();
    map.insert(
        EntityType::Lease,
        EntityScanList::builder()
            .entities(lease_entities)
            .deserialization_failures(failures)
            .build(),
    );
    map.insert(
        EntityType::WorkerMetricStats,
        EntityScanList::builder().entities(metric_entities).build(),
    );
    map
}

struct Harness {
    manager: MigrationAwareLamDataManager,
    captured: Arc<Mutex<Option<TableMigrationSummary>>>,
}

fn build(
    status: TableMigrationStatus,
    scan: HashMap<EntityType, EntityScanList>,
    legacy_metrics: Option<Vec<WorkerMetricStats>>,
) -> Harness {
    let mut entity_dao = crate::leases::entity_dao::MockEntityDAO::new();
    let scan = Arc::new(Mutex::new(Some(scan)));
    let scan2 = scan.clone();
    entity_dao
        .expect_scan_entities()
        .returning(move |_| Ok(scan2.lock().unwrap().take().unwrap_or_default()));

    let mut dao = MockWorkerMetricsDao::new();
    // lease delegate is always fetched (for potential deletes); no deletes expected here.
    dao.expect_lease_table_delegate().returning(|| {
        let mut d = MockWorkerMetricsDelegate::new();
        d.expect_delete_metrics().returning(|_| Ok(true));
        Arc::new(d)
    });
    match legacy_metrics {
        Some(metrics) => {
            dao.expect_legacy_table_delegate().returning(move || {
                let metrics = metrics.clone();
                let mut d = MockWorkerMetricsDelegate::new();
                d.expect_get_all_worker_metric_stats()
                    .returning(move || Ok(metrics.clone()));
                d.expect_delete_metrics().returning(|_| Ok(true));
                Some(Arc::new(d))
            });
        }
        None => {
            dao.expect_legacy_table_delegate().returning(|| None);
        }
    }

    let mut provider = MockTableMigrationStatusProvider::new();
    provider
        .expect_get_table_migration_status()
        .returning(move || status);

    let captured: Arc<Mutex<Option<TableMigrationSummary>>> = Arc::new(Mutex::new(None));
    let cap2 = captured.clone();
    let consumer: MigrationSummaryConsumer = Arc::new(move |s| {
        *cap2.lock().unwrap() = Some(s);
    });

    let manager = MigrationAwareLamDataManager::new(
        Arc::new(entity_dao),
        Arc::new(dao),
        Arc::new(provider),
        consumer,
        &config(),
    );
    Harness { manager, captured }
}

#[tokio::test]
async fn migration_complete_does_not_scan_legacy_table() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![lease("lease1", Some("worker1"))],
            vec![active_wm("worker1")],
        ),
        None, // legacy delegate is None -> not scanned
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.leases().len(), 1);
    assert_eq!(snapshot.worker_metric_stats().len(), 1);
    assert_eq!(
        snapshot.worker_metric_stats()[0].worker_id(),
        Some("worker1")
    );
}

#[tokio::test]
async fn migration_not_complete_scans_both_tables() {
    let h = build(
        TableMigrationStatus::Init,
        scan_result(
            vec![lease("lease1", Some("worker1"))],
            vec![active_wm("worker1")],
        ),
        Some(vec![active_wm("worker2")]),
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.leases().len(), 1);
    assert_eq!(snapshot.worker_metric_stats().len(), 2);
}

#[tokio::test]
async fn filters_invalid_worker_metrics() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![],
            vec![active_wm("validWorker"), invalid_wm("invalidWorker")],
        ),
        None,
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.worker_metric_stats().len(), 1);
    assert_eq!(
        snapshot.worker_metric_stats()[0].worker_id(),
        Some("validWorker")
    );
}

#[tokio::test]
async fn filters_expired_worker_metrics() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![],
            vec![active_wm("activeWorker"), expired_wm("expiredWorker")],
        ),
        None,
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.worker_metric_stats().len(), 1);
    assert_eq!(
        snapshot.worker_metric_stats()[0].worker_id(),
        Some("activeWorker")
    );
}

#[tokio::test]
async fn publishes_migration_summary() {
    let h = build(
        TableMigrationStatus::Init,
        scan_result(
            vec![lease("lease1", Some("worker1"))],
            vec![active_wm("worker1")],
        ),
        Some(vec![active_wm("worker2")]),
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_active_workers_with_metrics(), 2);
    assert_eq!(s.active_workers_with_metrics_in_lease_table(), 1);
    assert_eq!(s.active_workers_with_metrics_in_legacy_table(), 1);
    assert_eq!(s.workers_with_unexpired_leases(), 1);
    assert_eq!(s.total_workers_with_leases(), 1);
    assert_eq!(s.lease_owners_with_active_metrics(), 1);
}

#[tokio::test]
async fn min_support_code_no_lease_owners_is_negative_one() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(vec![], vec![active_wm("worker1")]),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(
        (*h.captured.lock().unwrap()).unwrap().min_support_code(),
        -1
    );
}

#[tokio::test]
async fn min_support_code_lease_owner_with_no_metrics_is_zero() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![lease("lease1", Some("worker2"))],
            vec![active_wm("worker1")],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!((*h.captured.lock().unwrap()).unwrap().min_support_code(), 0);
}

#[tokio::test]
async fn min_support_code_all_fresh_returns_min() {
    let fresh = chrono::Utc::now().timestamp();
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![
                lease("lease1", Some("worker1")),
                lease("lease2", Some("worker2")),
            ],
            vec![
                wm_with_support("worker1", Some(2), Some(fresh)),
                wm_with_support("worker2", Some(3), Some(fresh)),
            ],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!((*h.captured.lock().unwrap()).unwrap().min_support_code(), 2);
}

#[tokio::test]
async fn min_support_code_null_support_code_returns_zero() {
    let fresh = chrono::Utc::now().timestamp();
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![lease("lease1", Some("worker1"))],
            vec![wm_with_support("worker1", None, Some(fresh))],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!((*h.captured.lock().unwrap()).unwrap().min_support_code(), 0);
}

#[tokio::test]
async fn min_support_code_expired_support_code_returns_zero() {
    let stale = chrono::Utc::now().timestamp() - 10 * 24 * 60 * 60;
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![lease("lease1", Some("worker1"))],
            vec![wm_with_support("worker1", Some(2), Some(stale))],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!((*h.captured.lock().unwrap()).unwrap().min_support_code(), 0);
}

#[tokio::test]
async fn deserialization_failures_reported() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result_with_failures(vec![], vec![], vec!["badLease1".into(), "badLease2".into()]),
        None,
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.lease_deserialization_failures().len(), 2);
    assert!(snapshot
        .lease_deserialization_failures()
        .contains(&"badLease1".to_string()));
}

#[tokio::test]
async fn entity_dao_error_propagates() {
    let mut entity_dao = crate::leases::entity_dao::MockEntityDAO::new();
    entity_dao
        .expect_scan_entities()
        .returning(|_| Err(LeasingError::dependency("DDB unavailable")));
    let mut dao = MockWorkerMetricsDao::new();
    dao.expect_lease_table_delegate()
        .returning(|| Arc::new(MockWorkerMetricsDelegate::new()));
    dao.expect_legacy_table_delegate().returning(|| None);
    let mut provider = MockTableMigrationStatusProvider::new();
    provider
        .expect_get_table_migration_status()
        .returning(|| TableMigrationStatus::Complete);
    let consumer: MigrationSummaryConsumer = Arc::new(|_| {});
    let manager = MigrationAwareLamDataManager::new(
        Arc::new(entity_dao),
        Arc::new(dao),
        Arc::new(provider),
        consumer,
        &config(),
    );
    assert!(manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .is_err());
}

#[tokio::test]
async fn migration_deployed_scans_both_tables() {
    let h = build(
        TableMigrationStatus::Deployed,
        scan_result(vec![], vec![active_wm("worker1")]),
        Some(vec![active_wm("worker2")]),
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.worker_metric_stats().len(), 2);
}

#[tokio::test]
async fn empty_results_returns_empty_snapshot() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(vec![], vec![]),
        None,
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert!(snapshot.leases().is_empty());
    assert!(snapshot.worker_metric_stats().is_empty());
    assert!(snapshot.lease_deserialization_failures().is_empty());
}

#[tokio::test]
async fn legacy_delegate_null_does_not_scan_legacy_table() {
    let h = build(
        TableMigrationStatus::Init,
        scan_result(vec![], vec![active_wm("worker1")]),
        None, // no legacy delegate
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.worker_metric_stats().len(), 1);
}

#[tokio::test]
async fn only_unowned_leases_workers_with_unexpired_leases_is_zero() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(vec![lease("lease1", None)], vec![active_wm("worker1")]),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(
        (*h.captured.lock().unwrap())
            .unwrap()
            .workers_with_unexpired_leases(),
        0
    );
}

#[tokio::test]
async fn merged_metrics_from_both_tables_both_returned() {
    let h = build(
        TableMigrationStatus::Init,
        scan_result(vec![], vec![active_wm("worker1")]),
        Some(vec![active_wm("worker1")]),
    );
    let snapshot = h
        .manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(snapshot.worker_metric_stats().len(), 2);
}

#[tokio::test]
async fn total_workers_with_leases_counts_all_owners() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![
                lease("lease1", Some("worker1")),
                lease("lease2", Some("worker2")),
                lease("lease3", Some("worker1")),
            ],
            vec![active_wm("worker1"), active_wm("worker2")],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(
        (*h.captured.lock().unwrap())
            .unwrap()
            .total_workers_with_leases(),
        2
    );
}

#[tokio::test]
async fn total_workers_with_leases_excludes_null_owners() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![lease("lease1", Some("worker1")), lease("lease2", None)],
            vec![active_wm("worker1")],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    assert_eq!(
        (*h.captured.lock().unwrap())
            .unwrap()
            .total_workers_with_leases(),
        1
    );
}

#[tokio::test]
async fn lease_owners_with_active_metrics_all_owners_emitting() {
    // 2 lease owners, both have active metrics (worker1 in lease table, worker2 in legacy).
    let h = build(
        TableMigrationStatus::Init,
        scan_result(
            vec![
                lease("lease1", Some("worker1")),
                lease("lease2", Some("worker2")),
            ],
            vec![active_wm("worker1")],
        ),
        Some(vec![active_wm("worker2")]),
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_workers_with_leases(), 2);
    assert_eq!(s.lease_owners_with_active_metrics(), 2);
    // All lease owners are emitting → these are equal.
    assert_eq!(
        s.total_workers_with_leases(),
        s.lease_owners_with_active_metrics()
    );
}

#[tokio::test]
async fn lease_owners_with_active_metrics_no_leases() {
    // No leases, but workers exist with metrics.
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(vec![], vec![active_wm("worker1")]),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_workers_with_leases(), 0);
    assert_eq!(s.lease_owners_with_active_metrics(), 0);
}

#[tokio::test]
async fn lease_owners_with_active_metrics_some_not_emitting() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![
                lease("lease1", Some("worker1")),
                lease("lease2", Some("worker2")),
                lease("lease3", Some("worker3")),
            ],
            vec![active_wm("worker1"), active_wm("worker3")],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_workers_with_leases(), 3);
    assert_eq!(s.lease_owners_with_active_metrics(), 2);
}

#[tokio::test]
async fn lease_owners_with_active_metrics_owner_has_expired_metrics() {
    let h = build(
        TableMigrationStatus::Complete,
        scan_result(
            vec![
                lease("lease1", Some("worker1")),
                lease("lease2", Some("worker2")),
            ],
            vec![active_wm("worker1"), expired_wm("worker2")],
        ),
        None,
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_workers_with_leases(), 2);
    assert_eq!(s.lease_owners_with_active_metrics(), 1);
}

#[tokio::test]
async fn lease_owners_with_active_metrics_metrics_in_legacy_table_count() {
    let h = build(
        TableMigrationStatus::Init,
        scan_result(vec![lease("lease1", Some("worker1"))], vec![]),
        Some(vec![active_wm("worker1")]),
    );
    h.manager
        .load_data(&mut NullMetricsScope::new())
        .await
        .unwrap();
    let s = (*h.captured.lock().unwrap()).unwrap();
    assert_eq!(s.total_workers_with_leases(), 1);
    assert_eq!(s.lease_owners_with_active_metrics(), 1);
    assert_eq!(s.active_workers_with_metrics_in_lease_table(), 0);
    assert_eq!(s.active_workers_with_metrics_in_legacy_table(), 1);
}
