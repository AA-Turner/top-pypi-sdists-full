//! Port of `software.amazon.kinesis.leases.dynamodb.LeaseTableScanSegmentResolver`.
//!
//! Determines how many parallel segments to use for a DynamoDB table scan:
//! either an explicit customer-configured value, or dynamically from the table's
//! size (via `DescribeTable`), with 2-hour time-based caching to avoid describing
//! the table on every scan.
//!
//! # Design
//!
//! - Java's `@FunctionalInterface TableDescriber { DescribeTableResponse describe() }`
//!   becomes an async closure type `TableDescriber` (`Arc<dyn Fn -> Future>`),
//!   since the concrete describers make async DynamoDB calls. It returns
//!   `Result<Option<DescribeTableResponse>, LeasingError>` — `Ok(None)` for
//!   "table doesn't exist", `Err` for a genuine failure (which triggers the
//!   graceful fallback).
//! - Java's `synchronized resolveTotalSegments()` → the cache is guarded by a
//!   `tokio::sync::Mutex<Cache>`; `resolve_total_segments` is `async`.
//! - The `configuredTotalSegments > 0` short-circuit, the `calculateTotalSegments`
//!   formula (`clamp(ceil(sizeGB / 0.2GB), 1, 32)`), the fallback-to-last-known /
//!   default-10 on error, and the **no-cache-timestamp-update-on-failure** nuance
//!   (so the very next call retries) are preserved exactly.

use std::future::Future;
use std::pin::Pin;
use std::sync::Arc;

use aws_sdk_dynamodb::operation::describe_table::DescribeTableOutput;
use chrono::{DateTime, Duration as ChronoDuration, Utc};
use tokio::sync::Mutex;

use crate::leases::exceptions::LeasingError;

/// Default parallelism factor used when the table size cannot be determined.
pub const DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR: i32 = 10;

const NUMBER_OF_BYTES_PER_GB: f64 = (1024 * 1024 * 1024) as f64;
const GB_PER_SEGMENT: f64 = 0.2;
const MIN_SCAN_SEGMENTS: i32 = 1;
const MAX_SCAN_SEGMENTS: i32 = 32;
const CACHE_DURATION_HOURS: i64 = 2;

/// Async table-describer supplier (Java `TableDescriber`). Returns `Ok(None)`
/// when the table does not (yet) exist; `Err` on a genuine failure.
pub type TableDescriber = Arc<
    dyn Fn() -> Pin<
            Box<dyn Future<Output = Result<Option<DescribeTableOutput>, LeasingError>> + Send>,
        > + Send
        + Sync,
>;

struct Cache {
    cached_total_segments: Option<i32>,
    expiration_time: Option<DateTime<Utc>>,
}

/// Resolves the number of parallel-scan segments (per-instance cache).
pub struct LeaseTableScanSegmentResolver {
    configured_total_segments: i32,
    table_describer: TableDescriber,
    cache: Mutex<Cache>,
}

impl LeaseTableScanSegmentResolver {
    /// New resolver. `configured_total_segments <= 0` enables dynamic sizing.
    pub fn new(configured_total_segments: i32, table_describer: TableDescriber) -> Self {
        Self {
            configured_total_segments,
            table_describer,
            cache: Mutex::new(Cache {
                cached_total_segments: None,
                expiration_time: None,
            }),
        }
    }

    /// `calculateTotalSegments(tableSizeBytes)` — `clamp(ceil(sizeGB/0.2GB), 1, 32)`.
    pub fn calculate_total_segments(table_size_bytes: i64) -> i32 {
        let table_size_gb = table_size_bytes as f64 / NUMBER_OF_BYTES_PER_GB;
        let raw = (table_size_gb / GB_PER_SEGMENT).ceil() as i32;
        raw.clamp(MIN_SCAN_SEGMENTS, MAX_SCAN_SEGMENTS)
    }

    /// Resolve the number of segments to use (Java `resolveTotalSegments`).
    pub async fn resolve_total_segments(&self) -> i32 {
        if self.configured_total_segments > 0 {
            return self.configured_total_segments;
        }

        let mut cache = self.cache.lock().await;
        if Self::is_cache_valid(&cache) {
            return cache.cached_total_segments.unwrap();
        }

        let mut total_segments = cache
            .cached_total_segments
            .unwrap_or(DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR);

        match (self.table_describer)().await {
            Ok(Some(response)) => {
                let size = response
                    .table()
                    .and_then(|t| t.table_size_bytes())
                    .unwrap_or(0);
                total_segments = Self::calculate_total_segments(size);
                cache.cached_total_segments = Some(total_segments);
                cache.expiration_time =
                    Some(Utc::now() + ChronoDuration::hours(CACHE_DURATION_HOURS));
            }
            Ok(None) => {
                // DescribeTable returned null → use current fallback, cache it.
                cache.cached_total_segments = Some(total_segments);
                cache.expiration_time =
                    Some(Utc::now() + ChronoDuration::hours(CACHE_DURATION_HOURS));
            }
            Err(_e) => {
                // Failure: fall back WITHOUT updating the cache timestamp, so the
                // very next call retries (matches Java).
            }
        }
        total_segments
    }

    fn is_cache_valid(cache: &Cache) -> bool {
        match (cache.cached_total_segments, cache.expiration_time) {
            (Some(_), Some(expiry)) => Utc::now() < expiry,
            _ => false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use aws_sdk_dynamodb::types::TableDescription;
    use std::sync::atomic::{AtomicUsize, Ordering};

    const BYTES_PER_GB: i64 = 1024 * 1024 * 1024;

    fn describe_with_size(bytes: i64) -> DescribeTableOutput {
        DescribeTableOutput::builder()
            .table(TableDescription::builder().table_size_bytes(bytes).build())
            .build()
    }

    fn describer_returning(bytes: i64) -> TableDescriber {
        Arc::new(move || {
            let out = describe_with_size(bytes);
            Box::pin(async move { Ok(Some(out)) })
        })
    }

    #[test]
    fn calculate_total_segments_applies_formula_and_bounds() {
        assert_eq!(
            LeaseTableScanSegmentResolver::calculate_total_segments(0),
            1
        );
        assert_eq!(
            LeaseTableScanSegmentResolver::calculate_total_segments(
                (0.2 * BYTES_PER_GB as f64) as i64
            ),
            1
        );
        assert_eq!(
            LeaseTableScanSegmentResolver::calculate_total_segments(BYTES_PER_GB),
            5
        );
        assert_eq!(
            LeaseTableScanSegmentResolver::calculate_total_segments(100 * BYTES_PER_GB),
            32
        );
    }

    #[tokio::test]
    async fn uses_configured_value_without_describing_and_not_capped() {
        let describe_calls = Arc::new(AtomicUsize::new(0));
        let dc = describe_calls.clone();
        let describer: TableDescriber = Arc::new(move || {
            dc.fetch_add(1, Ordering::SeqCst);
            let out = describe_with_size(100 * BYTES_PER_GB);
            Box::pin(async move { Ok(Some(out)) })
        });
        let resolver = LeaseTableScanSegmentResolver::new(50, describer);
        assert_eq!(resolver.resolve_total_segments().await, 50);
        assert_eq!(describe_calls.load(Ordering::SeqCst), 0);
    }

    #[tokio::test]
    async fn computes_dynamically_when_not_configured() {
        let resolver = LeaseTableScanSegmentResolver::new(0, describer_returning(BYTES_PER_GB));
        assert_eq!(resolver.resolve_total_segments().await, 5);
    }

    #[tokio::test]
    async fn uses_default_factor_when_table_missing() {
        let describer: TableDescriber = Arc::new(|| Box::pin(async { Ok(None) }));
        let resolver = LeaseTableScanSegmentResolver::new(0, describer);
        assert_eq!(
            resolver.resolve_total_segments().await,
            DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR
        );
    }

    #[tokio::test]
    async fn falls_back_gracefully_when_describe_errors() {
        let describer: TableDescriber =
            Arc::new(|| Box::pin(async { Err(LeasingError::dependency("access denied")) }));
        let resolver = LeaseTableScanSegmentResolver::new(0, describer);
        assert_eq!(
            resolver.resolve_total_segments().await,
            DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR
        );
    }

    #[tokio::test]
    async fn retries_describe_after_failure() {
        let describe_calls = Arc::new(AtomicUsize::new(0));
        let dc = describe_calls.clone();
        let describer: TableDescriber = Arc::new(move || {
            let n = dc.fetch_add(1, Ordering::SeqCst) + 1;
            Box::pin(async move {
                if n == 1 {
                    Err(LeasingError::dependency("transient failure"))
                } else {
                    Ok(Some(describe_with_size(BYTES_PER_GB)))
                }
            })
        });
        let resolver = LeaseTableScanSegmentResolver::new(0, describer);
        assert_eq!(
            resolver.resolve_total_segments().await,
            DEFAULT_LEASE_TABLE_SCAN_PARALLELISM_FACTOR
        );
        assert_eq!(resolver.resolve_total_segments().await, 5);
        assert_eq!(describe_calls.load(Ordering::SeqCst), 2);
    }

    #[tokio::test]
    async fn caches_dynamic_result() {
        let describe_calls = Arc::new(AtomicUsize::new(0));
        let dc = describe_calls.clone();
        let describer: TableDescriber = Arc::new(move || {
            dc.fetch_add(1, Ordering::SeqCst);
            let out = describe_with_size(BYTES_PER_GB);
            Box::pin(async move { Ok(Some(out)) })
        });
        let resolver = LeaseTableScanSegmentResolver::new(0, describer);
        assert_eq!(resolver.resolve_total_segments().await, 5);
        assert_eq!(resolver.resolve_total_segments().await, 5);
        assert_eq!(describe_calls.load(Ordering::SeqCst), 1);
    }
}
