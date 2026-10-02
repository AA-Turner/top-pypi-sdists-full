//! Port of `software.amazon.kinesis.leases.KinesisShardDetector`.
//!
//! Concrete [`ShardDetector`] backed by the async `aws_sdk_kinesis` client:
//! a caching layer over paginated `ListShards`, plus `GetShardIterator` +
//! `GetRecords`-based child-shard lookup, with retry/backoff on throttling and
//! cache invalidation heuristics.
//!
//! # Concurrency (deviation resolving the arch-map-flagged inconsistency)
//!
//! Java mixes two distinct monitors: `shard()` uses `synchronized(this)`
//! double-checked-locking around the cache, while the `listShards*` /
//! `getListShardsResponse` methods use Lombok `@Synchronized` (a *different*
//! auto-generated `$lock` field). The arch map flags this as a latent
//! inconsistency ("looks like an oversight"). This port **consolidates to a
//! single lock**: a [`tokio::sync::Mutex`] guarding the cache state
//! (`cached_shard_map` + `last_cache_update_time`). We stay **async** — no
//! blocking `FutureUtils.resolveOrCancelFuture`; SDK futures are `.await`ed
//! directly (with a `tokio::time::timeout` mirroring `kinesisRequestTimeout`).
//!
//! The Java `null`-return sentinels ("stream not ACTIVE/UPDATING, retry later")
//! are modeled as `Ok(None)` internally and surfaced as errors / empty lists at
//! the trait boundary exactly as Java does:
//! - `listShardsWithFilterInternal` returning `null` → the trait `list_shards*`
//!   methods return `Ok(Vec::new())`? No — Java's public `listShards()` returns
//!   the `null` list straight through; callers treat `null` as "transient". The
//!   Rust trait returns `Result<Vec<Shard>, LeasingError>`, and the KCL callers
//!   that need the null-vs-empty distinction call
//!   `list_shards_without_consuming_resource_not_found_exception` (used by
//!   `HierarchicalShardSyncer::get_shard_list`, which maps a would-be `null`/RNF
//!   into an IO error). We therefore surface a transient-unavailable state as
//!   [`LeasingError::dependency`] with the Java "not in ACTIVE/UPDATING" message
//!   so no bogus empty shard list is cached.

use std::collections::HashMap;
use std::sync::atomic::{AtomicI32, Ordering};
use std::time::Duration;

use async_trait::async_trait;
use aws_sdk_kinesis::operation::list_shards::{ListShardsInput, ListShardsOutput};
use aws_sdk_kinesis::types::{ChildShard, Shard, ShardFilter, ShardIteratorType};
use aws_sdk_kinesis::Client as KinesisClient;
use chrono::{DateTime, Utc};
use tokio::sync::Mutex;

use crate::common::StreamIdentifier;
use crate::leases::exceptions::LeasingError;
use crate::leases::ShardDetector;

const THROW_RESOURCE_NOT_FOUND_EXCEPTION: bool = true;

/// Guards the shard cache. Consolidates the two Java monitors into one lock.
#[derive(Default)]
struct CacheState {
    /// `shardId -> Shard` (Java `cachedShardMap`); `None` until first load.
    cached_shard_map: Option<HashMap<String, Shard>>,
    /// When the cache was last populated (Java `lastCacheUpdateTime`).
    last_cache_update_time: Option<DateTime<Utc>>,
}

/// Concrete [`ShardDetector`] backed by `aws_sdk_kinesis`.
pub struct KinesisShardDetector {
    kinesis_client: KinesisClient,
    stream_identifier: StreamIdentifier,
    list_shards_backoff_time_in_millis: u64,
    max_list_shards_retry_attempts: i32,
    list_shards_cache_allowed_age_in_seconds: i64,
    max_cache_misses_before_reload: i32,
    cache_miss_warning_modulus: i32,
    kinesis_request_timeout: Duration,

    cache: Mutex<CacheState>,
    cache_misses: AtomicI32,
}

impl KinesisShardDetector {
    /// Construct a detector (mirrors the 8-arg Java constructor).
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        kinesis_client: KinesisClient,
        stream_identifier: StreamIdentifier,
        list_shards_backoff_time_in_millis: u64,
        max_list_shards_retry_attempts: i32,
        list_shards_cache_allowed_age_in_seconds: i64,
        max_cache_misses_before_reload: i32,
        cache_miss_warning_modulus: i32,
        kinesis_request_timeout: Duration,
    ) -> Self {
        Self {
            kinesis_client,
            stream_identifier,
            list_shards_backoff_time_in_millis,
            max_list_shards_retry_attempts,
            list_shards_cache_allowed_age_in_seconds,
            max_cache_misses_before_reload,
            cache_miss_warning_modulus,
            kinesis_request_timeout,
            cache: Mutex::new(CacheState::default()),
            cache_misses: AtomicI32::new(0),
        }
    }

    /// Test seam: the current `cache_misses` counter value (Java package-access
    /// `cacheMisses()`).
    pub fn cache_misses(&self) -> i32 {
        self.cache_misses.load(Ordering::SeqCst)
    }

    /// Test seam: directly populate the cache from a shard list (Java
    /// package-access `cachedShardMap(List<Shard>)`).
    pub async fn set_cached_shard_map(&self, shards: Vec<Shard>) {
        let map = shards
            .into_iter()
            .map(|s| (s.shard_id().to_string(), s))
            .collect();
        let mut cache = self.cache.lock().await;
        cache.cached_shard_map = Some(map);
        cache.last_cache_update_time = Some(Utc::now());
    }

    /// Whether the cache is older than `list_shards_cache_allowed_age_in_seconds`
    /// (Java `shouldRefreshCache`). Assumes the cache has been populated.
    fn should_refresh_cache(&self, last_update: Option<DateTime<Utc>>) -> bool {
        match last_update {
            None => true,
            Some(last) => {
                let seconds_since = (Utc::now() - last).num_seconds();
                seconds_since > self.list_shards_cache_allowed_age_in_seconds
            }
        }
    }

    /// Paginated ListShards with retry/backoff, populating the cache on success.
    ///
    /// Returns `Ok(None)` when the stream is not in ACTIVE/UPDATING (Java's
    /// `null` sentinel), which the trait methods map appropriately.
    async fn list_shards_with_filter_internal(
        &self,
        shard_filter: Option<ShardFilter>,
        should_propagate_resource_not_found: bool,
        consumer_id: &str,
    ) -> Result<Option<Vec<Shard>>, LeasingError> {
        let mut shards: Vec<Shard> = Vec::new();
        let mut next_token: Option<String> = None;

        loop {
            let result = self
                .list_shards_paged(
                    shard_filter.clone(),
                    next_token.as_deref(),
                    should_propagate_resource_not_found,
                    consumer_id,
                )
                .await?;

            match result {
                // Java: `if (result == null) return null;`
                None => return Ok(None),
                Some(output) => {
                    shards.extend(output.shards().iter().cloned());
                    next_token = output.next_token().map(str::to_string);
                    if next_token.as_deref().map(str::is_empty).unwrap_or(true) {
                        break;
                    }
                }
            }
        }

        self.cache_shards(&shards).await;
        Ok(Some(shards))
    }

    /// One paginated ListShards call with the Java retry/backoff loop.
    ///
    /// Returns `Ok(None)` for the ResourceInUse ("not ACTIVE/UPDATING") case.
    // `last_limit_exceeded` is written on the throttle path and read on
    // retry-exhaustion; a subsequent success on a later retry legitimately
    // leaves the last write unread.
    #[allow(unused_assignments)]
    async fn list_shards_paged(
        &self,
        shard_filter: Option<ShardFilter>,
        next_token: Option<&str>,
        should_propagate_resource_not_found: bool,
        _consumer_id: &str,
    ) -> Result<Option<ListShardsOutput>, LeasingError> {
        let mut remaining_retries = self.max_list_shards_retry_attempts;
        let mut last_limit_exceeded: Option<String> = None;

        loop {
            let mut builder = self.kinesis_client.list_shards();
            match next_token {
                Some(token) if !token.is_empty() => {
                    builder = builder.next_token(token);
                }
                _ => {
                    builder = builder.stream_name(self.stream_identifier.stream_name());
                    if let Some(f) = shard_filter.clone() {
                        builder = builder.shard_filter(f);
                    }
                    if let Some(arn) = self.stream_identifier.stream_arn_optional() {
                        builder = builder.stream_arn(arn.to_string());
                    }
                }
            }

            let fut = builder.send();
            let call = tokio::time::timeout(self.kinesis_request_timeout, fut).await;

            match call {
                // Timeout → Java wraps TimeoutException in RuntimeException.
                Err(_elapsed) => {
                    return Err(LeasingError::dependency(
                        "Timed out waiting for ListShards response",
                    ));
                }
                Ok(Ok(output)) => return Ok(Some(output)),
                Ok(Err(sdk_err)) => {
                    let service_err = sdk_err.into_service_error();
                    if service_err.is_resource_in_use_exception() {
                        // Stream not in Active/Updating status → null sentinel.
                        return Ok(None);
                    } else if service_err.is_limit_exceeded_exception() {
                        // Backoff and retry.
                        tokio::time::sleep(Duration::from_millis(
                            self.list_shards_backoff_time_in_millis,
                        ))
                        .await;
                        last_limit_exceeded = Some(service_err.to_string());
                    } else if service_err.is_resource_not_found_exception() {
                        if should_propagate_resource_not_found {
                            // Box exactly once: HierarchicalShardSyncer
                            // downcasts the source back to `ListShardsError`
                            // to recognize a deleted stream (Java catches the
                            // raw ResourceNotFoundException).
                            return Err(LeasingError::dependency_caused_by(
                                "Stream no longer exists",
                                service_err,
                            ));
                        }
                        // Return an empty (non-null) response so the stream is
                        // treated as having zero shards.
                        return Ok(Some(
                            ListShardsOutput::builder()
                                .set_shards(Some(Vec::new()))
                                .build(),
                        ));
                    } else {
                        return Err(LeasingError::dependency_caused_by(
                            "ListShards failed",
                            Box::new(service_err),
                        ));
                    }
                }
            }

            remaining_retries -= 1;
            if remaining_retries <= 0 {
                return match last_limit_exceeded {
                    Some(msg) => Err(LeasingError::provisioned_throughput(msg)),
                    None => Err(LeasingError::invalid_state(
                        "Received null from ListShards call.",
                    )),
                };
            }
        }
    }

    /// Populate the cache (Java `cachedShardMap(List<Shard>)`).
    async fn cache_shards(&self, shards: &[Shard]) {
        let map = shards
            .iter()
            .map(|s| (s.shard_id().to_string(), s.clone()))
            .collect();
        let mut cache = self.cache.lock().await;
        cache.cached_shard_map = Some(map);
        cache.last_cache_update_time = Some(Utc::now());
    }
}

#[async_trait]
impl ShardDetector for KinesisShardDetector {
    async fn shard(&self, shard_id: &str) -> Result<Option<Shard>, LeasingError> {
        // Fast path: populated cache & a hit.
        {
            let cache = self.cache.lock().await;
            if let Some(map) = &cache.cached_shard_map {
                if let Some(shard) = map.get(shard_id) {
                    return Ok(Some(shard.clone()));
                }
            }
        }

        // If the cache was empty, load it (Java double-checked-locking's first block).
        {
            let is_empty = {
                let cache = self.cache.lock().await;
                cache
                    .cached_shard_map
                    .as_ref()
                    .map(|m| m.is_empty())
                    .unwrap_or(true)
            };
            if is_empty {
                self.list_shards().await?;
                let cache = self.cache.lock().await;
                if let Some(map) = &cache.cached_shard_map {
                    if let Some(shard) = map.get(shard_id) {
                        return Ok(Some(shard.clone()));
                    }
                }
            }
        }

        // Miss: increment counter, maybe force a refresh (Java second block).
        let misses = self.cache_misses.fetch_add(1, Ordering::SeqCst) + 1;
        let last_update = { self.cache.lock().await.last_cache_update_time };
        if misses > self.max_cache_misses_before_reload || self.should_refresh_cache(last_update) {
            // Re-check under refresh.
            {
                let cache = self.cache.lock().await;
                if let Some(map) = &cache.cached_shard_map {
                    if let Some(shard) = map.get(shard_id) {
                        self.cache_misses.store(0, Ordering::SeqCst);
                        return Ok(Some(shard.clone()));
                    }
                }
            }
            self.list_shards().await?;
            let cache = self.cache.lock().await;
            let found = cache
                .cached_shard_map
                .as_ref()
                .and_then(|m| m.get(shard_id))
                .cloned();
            self.cache_misses.store(0, Ordering::SeqCst);
            return Ok(found);
        }

        // Not found and no refresh triggered.
        let _ = self.cache_miss_warning_modulus; // (used only for log level in Java)
        Ok(None)
    }

    async fn list_shards(&self) -> Result<Vec<Shard>, LeasingError> {
        // Java `listShards()` returns the (possibly null) list straight through;
        // a null result means "not ACTIVE/UPDATING". Surface that as an error so
        // no bogus empty list is treated as authoritative.
        match self
            .list_shards_with_filter_internal(None, !THROW_RESOURCE_NOT_FOUND_EXCEPTION, "")
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Received null from ListShards call.",
            )),
        }
    }

    async fn list_shards_for_consumer(
        &self,
        consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        match self
            .list_shards_with_filter_internal(
                None,
                !THROW_RESOURCE_NOT_FOUND_EXCEPTION,
                consumer_id,
            )
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Received null from ListShards call.",
            )),
        }
    }

    async fn list_shards_without_consuming_resource_not_found_exception(
        &self,
    ) -> Result<Vec<Shard>, LeasingError> {
        match self
            .list_shards_with_filter_internal(None, THROW_RESOURCE_NOT_FOUND_EXCEPTION, "")
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Stream is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
            )),
        }
    }

    async fn list_shards_without_consuming_resource_not_found_exception_for_consumer(
        &self,
        consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        match self
            .list_shards_with_filter_internal(None, THROW_RESOURCE_NOT_FOUND_EXCEPTION, consumer_id)
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Stream is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
            )),
        }
    }

    async fn list_shards_with_filter(
        &self,
        shard_filter: ShardFilter,
    ) -> Result<Vec<Shard>, LeasingError> {
        match self
            .list_shards_with_filter_internal(
                Some(shard_filter),
                !THROW_RESOURCE_NOT_FOUND_EXCEPTION,
                "",
            )
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Stream is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
            )),
        }
    }

    async fn list_shards_with_filter_for_consumer(
        &self,
        shard_filter: ShardFilter,
        consumer_id: &str,
    ) -> Result<Vec<Shard>, LeasingError> {
        match self
            .list_shards_with_filter_internal(
                Some(shard_filter),
                !THROW_RESOURCE_NOT_FOUND_EXCEPTION,
                consumer_id,
            )
            .await?
        {
            Some(shards) => Ok(shards),
            None => Err(LeasingError::invalid_state(
                "Stream is not in ACTIVE OR UPDATING state - will retry getting the shard list.",
            )),
        }
    }

    fn stream_identifier(&self) -> Result<StreamIdentifier, LeasingError> {
        Ok(self.stream_identifier.clone())
    }

    async fn get_list_shards_response(
        &self,
        request: ListShardsInput,
    ) -> Result<ListShardsOutput, LeasingError> {
        // Rebuild a fluent request from the input and send it (bounded by the
        // request timeout, mirroring FutureUtils.resolveOrCancelFuture).
        let mut builder = self.kinesis_client.list_shards();
        if let Some(v) = request.stream_name() {
            builder = builder.stream_name(v);
        }
        if let Some(v) = request.next_token() {
            builder = builder.next_token(v);
        }
        if let Some(v) = request.shard_filter() {
            builder = builder.shard_filter(v.clone());
        }
        if let Some(v) = request.stream_arn() {
            builder = builder.stream_arn(v);
        }
        match tokio::time::timeout(self.kinesis_request_timeout, builder.send()).await {
            Err(_) => Err(LeasingError::dependency(
                "Timed out waiting for ListShards response",
            )),
            Ok(Ok(output)) => Ok(output),
            Ok(Err(e)) => Err(LeasingError::dependency_caused_by(
                "ListShards failed",
                Box::new(e),
            )),
        }
    }

    async fn get_child_shards(&self, shard_id: &str) -> Result<Vec<ChildShard>, LeasingError> {
        let mut iter_builder = self
            .kinesis_client
            .get_shard_iterator()
            .stream_name(self.stream_identifier.stream_name())
            .shard_iterator_type(ShardIteratorType::Latest)
            .shard_id(shard_id);
        if let Some(arn) = self.stream_identifier.stream_arn_optional() {
            iter_builder = iter_builder.stream_arn(arn.to_string());
        }

        let iter_resp =
            match tokio::time::timeout(self.kinesis_request_timeout, iter_builder.send()).await {
                Err(_) => {
                    return Err(LeasingError::dependency(
                        "Timed out waiting for GetShardIterator",
                    ))
                }
                Ok(Ok(r)) => r,
                Ok(Err(e)) => {
                    return Err(LeasingError::dependency_caused_by(
                        "GetShardIterator failed",
                        Box::new(e),
                    ))
                }
            };

        let mut records_builder = self
            .kinesis_client
            .get_records()
            .set_shard_iterator(iter_resp.shard_iterator().map(str::to_string));
        if let Some(arn) = self.stream_identifier.stream_arn_optional() {
            records_builder = records_builder.stream_arn(arn.to_string());
        }

        let records_resp = match tokio::time::timeout(
            self.kinesis_request_timeout,
            records_builder.send(),
        )
        .await
        {
            Err(_) => return Err(LeasingError::dependency("Timed out waiting for GetRecords")),
            Ok(Ok(r)) => r,
            Ok(Err(e)) => {
                return Err(LeasingError::dependency_caused_by(
                    "GetRecords failed",
                    Box::new(e),
                ))
            }
        };

        Ok(records_resp.child_shards().to_vec())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retrieval::polling::test_support::mock_kinesis_client;
    use aws_sdk_kinesis::operation::list_shards::{ListShardsError, ListShardsOutput};
    use aws_sdk_kinesis::types::error::{
        LimitExceededException, ResourceInUseException, ResourceNotFoundException,
    };
    use aws_smithy_mocks::mock;

    const MAX_LIST_SHARDS_RETRY_ATTEMPTS: i32 = 5;
    const MAX_CACHE_MISSES_BEFORE_RELOAD: i32 = 10;

    // Java KinesisShardDetectorTest mocks KinesisAsyncClient (Mockito). In Rust
    // we inject canned responses/errors into a *real* `aws_sdk_kinesis::Client`
    // via `aws_smithy_mocks`, then assert on the detector's behavior. The
    // list-shards SDK-call tests below mirror the Java list/get tests; the
    // Java null-response test relies on `CompletableFuture.completedFuture(null)`
    // which is impossible with the Rust SDK type system (a `ListShardsOutput`
    // can never be null), so that scenario is not portable and is skipped.

    fn shard(id: &str) -> Shard {
        Shard::builder().shard_id(id).build().unwrap()
    }

    fn detector() -> KinesisShardDetector {
        // A client is required by the constructor but is never called by the
        // cache-hit tests below.
        let config = aws_sdk_kinesis::Config::builder()
            .behavior_version(aws_sdk_kinesis::config::BehaviorVersion::latest())
            .region(aws_sdk_kinesis::config::Region::new("us-east-1"))
            .build();
        let client = KinesisClient::from_conf(config);
        detector_with_client(client)
    }

    fn detector_with_client(client: KinesisClient) -> KinesisShardDetector {
        KinesisShardDetector::new(
            client,
            StreamIdentifier::single_stream_instance("TestStream"),
            50,                             // backoff
            MAX_LIST_SHARDS_RETRY_ATTEMPTS, // max retries
            10,                             // cache age seconds
            MAX_CACHE_MISSES_BEFORE_RELOAD, // max cache misses before reload
            2,                              // cache miss warning modulus
            Duration::from_secs(5),
        )
    }

    fn shard_list() -> Vec<Shard> {
        (0..5)
            .map(|i| shard(&format!("shardId-{:012}", i)))
            .collect()
    }

    #[tokio::test]
    async fn get_shard_cache_hit_does_not_call_client() {
        // Java testGetShard: cache pre-populated, shard found, client never called.
        let d = detector();
        d.set_cached_shard_map(shard_list()).await;
        let found = d.shard("shardId-000000000001").await.unwrap();
        assert_eq!(found, Some(shard("shardId-000000000001")));
    }

    #[tokio::test]
    async fn get_shard_nonexistent_first_miss_increments_counter() {
        // Java testGetShardNonExistentShard: shard 5 not in the 5-shard cache;
        // first miss increments cacheMisses to 1, no refresh triggered.
        let d = detector();
        d.set_cached_shard_map(shard_list()).await;
        let found = d.shard("shardId-000000000005").await.unwrap();
        assert_eq!(found, None);
        assert_eq!(d.cache_misses(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testListShardsSingleResponse`.
    #[tokio::test]
    async fn list_shards_single_response() {
        let list = mock!(aws_sdk_kinesis::Client::list_shards)
            .then_output(|| ListShardsOutput::builder().set_shards(Some(vec![])).build());
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);

        let shards = d.list_shards().await.unwrap();

        assert!(shards.is_empty());
        assert_eq!(list.num_calls(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testListShardsResouceInUse`.
    ///
    /// Java `listShards()` returns `null` on ResourceInUse; the Rust port surfaces
    /// that null-sentinel as an `InvalidState` error from `list_shards()`. Only one
    /// SDK call is made (no retry on ResourceInUse).
    #[tokio::test]
    async fn list_shards_resource_in_use() {
        let list = mock!(aws_sdk_kinesis::Client::list_shards).then_error(|| {
            ListShardsError::ResourceInUseException(ResourceInUseException::builder().build())
        });
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);

        let err = d.list_shards().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::InvalidState { .. }),
            "got {err:?}"
        );
        assert_eq!(list.num_calls(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testListShardsThrottled`.
    ///
    /// LimitExceeded is retried up to `MAX_LIST_SHARDS_RETRY_ATTEMPTS` times, then
    /// surfaces as a `ProvisionedThroughput` error. Java expects exactly that many
    /// SDK calls.
    #[tokio::test(start_paused = true)]
    async fn list_shards_throttled() {
        let list = mock!(aws_sdk_kinesis::Client::list_shards)
            .sequence()
            .error(|| {
                ListShardsError::LimitExceededException(LimitExceededException::builder().build())
            })
            .times(MAX_LIST_SHARDS_RETRY_ATTEMPTS as usize)
            .build();
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);

        let err = d.list_shards().await.unwrap_err();
        assert!(
            matches!(err, LeasingError::ProvisionedThroughput { .. }),
            "got {err:?}"
        );
        assert_eq!(list.num_calls(), MAX_LIST_SHARDS_RETRY_ATTEMPTS as usize);
    }

    /// Port of `KinesisShardDetectorTest.testListShardsResourceNotFoundReturnsEmptyResponse`.
    ///
    /// On the non-propagating path, ResourceNotFound yields an empty (non-null)
    /// response, so `list_shards()` returns an empty list after one SDK call.
    #[tokio::test]
    async fn list_shards_resource_not_found_returns_empty_response() {
        let list = mock!(aws_sdk_kinesis::Client::list_shards).then_error(|| {
            ListShardsError::ResourceNotFoundException(ResourceNotFoundException::builder().build())
        });
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);

        let shards = d.list_shards().await.unwrap();

        assert_eq!(shards.len(), 0);
        assert_eq!(list.num_calls(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testGetShardEmptyCache`.
    #[tokio::test]
    async fn get_shard_empty_cache_loads_from_service() {
        let list = mock!(aws_sdk_kinesis::Client::list_shards).then_output(|| {
            ListShardsOutput::builder()
                .set_shards(Some(shard_list()))
                .build()
        });
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);

        let found = d.shard("shardId-000000000001").await.unwrap();

        assert_eq!(found, Some(shard("shardId-000000000001")));
        assert_eq!(list.num_calls(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testGetShardNewShardForceRefresh`.
    ///
    /// The cache has shards 0-4. `shard("shardId-5")` is called
    /// `MAX_CACHE_MISSES_BEFORE_RELOAD + 1` times: the first
    /// `MAX_CACHE_MISSES_BEFORE_RELOAD` return `None`, and the final call (which
    /// crosses the reload threshold) force-refreshes from the service — the fresh
    /// list now contains shard 5, so the last response is that shard. Exactly one
    /// SDK call is made.
    #[tokio::test]
    async fn get_shard_new_shard_force_refresh() {
        let new_id = "shardId-000000000005";
        let mut refreshed = shard_list();
        refreshed.push(shard(new_id));
        let refreshed_for_mock = refreshed.clone();
        let list = mock!(aws_sdk_kinesis::Client::list_shards).then_output(move || {
            ListShardsOutput::builder()
                .set_shards(Some(refreshed_for_mock.clone()))
                .build()
        });
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);
        d.set_cached_shard_map(shard_list()).await;

        let mut responses = Vec::new();
        for _ in 0..=MAX_CACHE_MISSES_BEFORE_RELOAD {
            responses.push(d.shard(new_id).await.unwrap());
        }

        for r in responses
            .iter()
            .take(MAX_CACHE_MISSES_BEFORE_RELOAD as usize)
        {
            assert_eq!(*r, None);
        }
        assert_eq!(
            responses[MAX_CACHE_MISSES_BEFORE_RELOAD as usize],
            Some(shard(new_id))
        );
        assert_eq!(list.num_calls(), 1);
    }

    /// Port of `KinesisShardDetectorTest.testGetShardNonExistentShardForceRefresh`.
    ///
    /// Same as above but the refreshed list still lacks shard 5, so every response
    /// is `None`; after the force-refresh the cache-miss counter is reset to 0 and
    /// exactly one SDK call is made.
    #[tokio::test]
    async fn get_shard_nonexistent_shard_force_refresh() {
        let missing_id = "shardId-000000000005";
        let list = mock!(aws_sdk_kinesis::Client::list_shards).then_output(|| {
            ListShardsOutput::builder()
                .set_shards(Some(shard_list()))
                .build()
        });
        let client = mock_kinesis_client(&[&list]);
        let d = detector_with_client(client);
        d.set_cached_shard_map(shard_list()).await;

        let mut responses = Vec::new();
        for _ in 0..=MAX_CACHE_MISSES_BEFORE_RELOAD {
            responses.push(d.shard(missing_id).await.unwrap());
        }

        for r in &responses {
            assert_eq!(*r, None);
        }
        assert_eq!(d.cache_misses(), 0);
        assert_eq!(list.num_calls(), 1);
    }
}
