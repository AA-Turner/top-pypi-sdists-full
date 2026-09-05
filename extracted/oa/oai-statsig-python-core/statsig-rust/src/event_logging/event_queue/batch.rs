use crate::StatsigErr;
use crate::event_logging::statsig_event_internal::StatsigEventInternal;
use crate::log_event_payload::{LogEventPayload, LogEventRequest, SerializedLogEventRequest};
use crate::statsig_metadata::StatsigMetadataWithLogEventExtras;
use crate::user::{StatsigUserLoggable, statsig_user_loggable::StatsigUserLoggableData};
use ahash::AHashMap;
use serde::ser::{Error as _, SerializeSeq};
use serde::{Serialize, Serializer};
use serde_json::json;
use serde_json::value::{RawValue, to_raw_value};
use std::cell::RefCell;
use std::sync::Arc;

const MAX_CACHED_FAST_USERS_PER_BATCH: usize = 64;
const MAX_CACHED_FAST_USER_BYTES_PER_BATCH: usize = 256 * 1024;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct BorrowedLogEventPayload<'a> {
    events: CachedEventSequence<'a>,
    statsig_metadata: &'a StatsigMetadataWithLogEventExtras,
}

struct CachedEventSequence<'a> {
    events: Vec<&'a StatsigEventInternal>,
}

struct FastUserJsonCache<'a> {
    entries: Vec<FastUserJsonCacheEntry<'a>>,
    total_bytes: usize,
}

struct FastUserJsonCacheEntry<'a> {
    user: &'a StatsigUserLoggable,
    // `None` remembers an oversized serialization so later occurrences do not
    // repeatedly allocate a temporary JSON buffer that cannot be retained.
    json: Option<Box<RawValue>>,
}

struct FastUserReuseIndex<'a> {
    entries_by_data: AHashMap<usize, Vec<FastUserReuseEntry<'a>>>,
}

struct FastUserReuseEntry<'a> {
    user: &'a StatsigUserLoggable,
    repeated: bool,
}

struct CachedFastUser<'event, 'cache> {
    user: &'event StatsigUserLoggable,
    should_cache: bool,
    cache: &'cache RefCell<FastUserJsonCache<'event>>,
}

impl<'a> FastUserReuseIndex<'a> {
    fn new(events: &[&'a StatsigEventInternal]) -> Self {
        // Build a bounded index first so unique-user batches stay on the normal
        // zero-materialization serializer path. Pointer keys are valid for the
        // lifetime of this batch because every event retains its Arc.
        let mut entries_by_data: AHashMap<usize, Vec<FastUserReuseEntry<'a>>> = AHashMap::new();
        let mut tracked_entries = 0;

        for event in events {
            let user = &event.user;
            let Some(data_pointer) = fast_user_data_pointer(user) else {
                continue;
            };

            if let Some(entries) = entries_by_data.get_mut(&data_pointer) {
                if let Some(entry) = entries
                    .iter_mut()
                    .find(|entry| same_fast_user_json(entry.user, user))
                {
                    entry.repeated = true;
                } else if tracked_entries < MAX_CACHED_FAST_USERS_PER_BATCH {
                    entries.push(FastUserReuseEntry {
                        user,
                        repeated: false,
                    });
                    tracked_entries += 1;
                }
            } else if tracked_entries < MAX_CACHED_FAST_USERS_PER_BATCH {
                entries_by_data.insert(
                    data_pointer,
                    vec![FastUserReuseEntry {
                        user,
                        repeated: false,
                    }],
                );
                tracked_entries += 1;
            }
        }

        Self { entries_by_data }
    }

    fn is_repeated(&self, user: &StatsigUserLoggable) -> bool {
        let Some(data_pointer) = fast_user_data_pointer(user) else {
            return false;
        };
        self.entries_by_data
            .get(&data_pointer)
            .is_some_and(|entries| {
                entries
                    .iter()
                    .any(|entry| entry.repeated && same_fast_user_json(entry.user, user))
            })
    }
}

impl Serialize for CachedEventSequence<'_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let reuse_index = FastUserReuseIndex::new(&self.events);
        // The raw JSON cache is serialization-local. It cannot survive a
        // request, retry, concurrent serialization, or EventBatch drop.
        let cache = RefCell::new(FastUserJsonCache {
            entries: Vec::new(),
            total_bytes: 0,
        });
        let mut sequence = serializer.serialize_seq(Some(self.events.len()))?;

        for event in &self.events {
            sequence.serialize_element(&event.with_serializable_user(CachedFastUser {
                user: &event.user,
                should_cache: reuse_index.is_repeated(&event.user),
                cache: &cache,
            }))?;
        }

        sequence.end()
    }
}

impl Serialize for CachedFastUser<'_, '_> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        if !self.should_cache {
            return self.user.serialize(serializer);
        }

        {
            let cache = self.cache.borrow();
            if let Some(entry) = cache
                .entries
                .iter()
                .find(|entry| same_fast_user_json(entry.user, self.user))
            {
                return match &entry.json {
                    Some(json) => json.serialize(serializer),
                    None => self.user.serialize(serializer),
                };
            }

            if cache.entries.len() >= MAX_CACHED_FAST_USERS_PER_BATCH
                || cache.total_bytes >= MAX_CACHED_FAST_USER_BYTES_PER_BATCH
            {
                return self.user.serialize(serializer);
            }
        }

        let json = to_raw_value(self.user).map_err(S::Error::custom)?;
        let json_len = json.get().len();
        let can_cache = {
            let cache = self.cache.borrow();
            cache.entries.len() < MAX_CACHED_FAST_USERS_PER_BATCH
                && cache.total_bytes.saturating_add(json_len)
                    <= MAX_CACHED_FAST_USER_BYTES_PER_BATCH
        };
        let mut cache = self.cache.borrow_mut();
        if can_cache {
            cache.total_bytes += json_len;
            cache.entries.push(FastUserJsonCacheEntry {
                user: self.user,
                json: Some(json),
            });
            let index = cache.entries.len() - 1;
            return cache.entries[index]
                .json
                .as_ref()
                .expect("cache entry was populated")
                .serialize(serializer);
        }

        cache.entries.push(FastUserJsonCacheEntry {
            user: self.user,
            json: None,
        });
        drop(cache);
        json.serialize(serializer)
    }
}

fn same_fast_user_json(left: &StatsigUserLoggable, right: &StatsigUserLoggable) -> bool {
    // FastStatsigUser mutations use Arc::make_mut, so pointer identity also
    // proves that the immutable user-data snapshot has not changed.
    let same_data = match (&left.data, &right.data) {
        (StatsigUserLoggableData::Fast(left), StatsigUserLoggableData::Fast(right)) => {
            Arc::ptr_eq(left, right)
        }
        _ => false,
    };
    if !same_data {
        return false;
    }

    // HashMap equality ignores iteration order, but JSON byte parity does not.
    // DynamicValue::PartialEq is evaluation equality and does not include
    // the json_value that is serialized. Reuse only when the overlay maps
    // produce the same ordered JSON entry stream.
    let same_environment_order = match (&left.environment, &right.environment) {
        (None, None) => true,
        (Some(left), Some(right)) => same_dynamic_value_entries(left.iter(), right.iter()),
        _ => false,
    };
    if !same_environment_order {
        return false;
    }

    let same_global_custom_order = match (&left.global_custom, &right.global_custom) {
        (None, None) => true,
        (Some(left), Some(right)) => same_dynamic_value_entries(left.iter(), right.iter()),
        _ => false,
    };

    same_global_custom_order
}

fn same_dynamic_value_entries<'left, 'right>(
    mut left: impl Iterator<Item = (&'left String, &'left crate::DynamicValue)>,
    mut right: impl Iterator<Item = (&'right String, &'right crate::DynamicValue)>,
) -> bool {
    loop {
        match (left.next(), right.next()) {
            (None, None) => return true,
            (Some((left_key, left_value)), Some((right_key, right_value)))
                if left_key == right_key
                    && same_json_wire_value(&left_value.json_value, &right_value.json_value) => {}
            _ => return false,
        }
    }
}

// This mirrors the compact serde_json representation without allocating raw
// fragments. In particular, object iteration order and signed zero are wire
// relevant even when normal JSON value equality treats them as equal.
fn same_json_wire_value(left: &serde_json::Value, right: &serde_json::Value) -> bool {
    match (left, right) {
        (serde_json::Value::Null, serde_json::Value::Null) => true,
        (serde_json::Value::Bool(left), serde_json::Value::Bool(right)) => left == right,
        (serde_json::Value::Number(left), serde_json::Value::Number(right)) => {
            same_json_number_wire(left, right)
        }
        (serde_json::Value::String(left), serde_json::Value::String(right)) => left == right,
        (serde_json::Value::Array(left), serde_json::Value::Array(right)) => {
            left.len() == right.len()
                && left
                    .iter()
                    .zip(right.iter())
                    .all(|(left, right)| same_json_wire_value(left, right))
        }
        (serde_json::Value::Object(left), serde_json::Value::Object(right)) => {
            left.len() == right.len()
                && left.iter().zip(right.iter()).all(
                    |((left_key, left_value), (right_key, right_value))| {
                        left_key == right_key && same_json_wire_value(left_value, right_value)
                    },
                )
        }
        _ => false,
    }
}

fn same_json_number_wire(left: &serde_json::Number, right: &serde_json::Number) -> bool {
    if left != right {
        return false;
    }

    match (left.is_f64(), right.is_f64()) {
        (false, false) => true,
        (true, true) => left
            .as_f64()
            .zip(right.as_f64())
            .is_some_and(|(left, right)| left.to_bits() == right.to_bits()),
        _ => false,
    }
}

fn fast_user_data_pointer(user: &StatsigUserLoggable) -> Option<usize> {
    match &user.data {
        StatsigUserLoggableData::Fast(data) => Some(Arc::as_ptr(data) as usize),
        StatsigUserLoggableData::Public(_) => None,
    }
}

pub(crate) struct EnqueuedEvent<T> {
    event: T,
    enqueued_at_ms: u64,
}

impl<T> EnqueuedEvent<T> {
    pub(crate) fn new(event: T, enqueued_at_ms: u64) -> Self {
        Self {
            event,
            enqueued_at_ms,
        }
    }

    pub(crate) fn map<U>(self, map_event: impl FnOnce(T) -> U) -> EnqueuedEvent<U> {
        EnqueuedEvent {
            event: map_event(self.event),
            enqueued_at_ms: self.enqueued_at_ms,
        }
    }
}

pub(crate) struct EventBatch {
    attempts: u8,
    events: Vec<EnqueuedEvent<StatsigEventInternal>>,
}

impl EventBatch {
    pub(crate) fn new(events: Vec<EnqueuedEvent<StatsigEventInternal>>) -> Self {
        Self {
            events,
            attempts: 0,
        }
    }

    pub(crate) fn len(&self) -> usize {
        self.events.len()
    }

    pub(crate) fn attempts(&self) -> u8 {
        self.attempts
    }

    pub(crate) fn increment_attempts(&mut self) {
        self.attempts += 1;
    }

    pub(crate) fn iter_events(&self) -> impl Iterator<Item = &StatsigEventInternal> {
        self.events.iter().map(|event| &event.event)
    }

    pub(crate) fn into_events(self) -> impl Iterator<Item = EnqueuedEvent<StatsigEventInternal>> {
        self.events.into_iter()
    }

    pub(crate) fn get_max_event_queue_time_ms(&self, now_ms: u64) -> u64 {
        self.events
            .iter()
            .map(|event| event.enqueued_at_ms)
            .min()
            .map(|enqueued_at_ms| now_ms.saturating_sub(enqueued_at_ms))
            .unwrap_or_default()
    }

    pub(crate) fn get_log_event_request(
        &self,
        statsig_metadata: StatsigMetadataWithLogEventExtras,
    ) -> LogEventRequest {
        let events = self.iter_events().collect::<Vec<_>>();
        let payload = LogEventPayload {
            events: json!(events),
            statsig_metadata: json!(statsig_metadata),
        };

        LogEventRequest {
            payload,
            event_count: self.len() as u64,
            retries: self.attempts as u32,
        }
    }

    pub(crate) fn get_serialized_log_event_request(
        &self,
        statsig_metadata: StatsigMetadataWithLogEventExtras,
    ) -> Result<SerializedLogEventRequest, StatsigErr> {
        let events = self.iter_events().collect::<Vec<_>>();
        let flush_type = statsig_metadata.flush_type.clone();
        let payload = serde_json::to_vec(&BorrowedLogEventPayload {
            events: CachedEventSequence { events },
            statsig_metadata: &statsig_metadata,
        })
        .map_err(|error| StatsigErr::SerializationError(error.to_string()))?;

        Ok(SerializedLogEventRequest {
            payload,
            event_count: self.len() as u64,
            retries: self.attempts as u32,
            flush_type,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        DynamicValue,
        compression::compression_helper::compress_data,
        event_logging::statsig_event::StatsigEvent,
        statsig_metadata::StatsigMetadata,
        user::{
            StatsigUserLoggable,
            fast_statsig_user::{FastStatsigUser, FastUserCustomMap, FastUserData},
            user_data::UserDataMap,
            user_value::UserValue,
        },
    };
    use flate2::{Compression, read::GzDecoder, write::GzEncoder};
    use serde_json::Value;
    use std::collections::HashMap;
    use std::hint::black_box;
    use std::io::{BufWriter, Read, Write};
    use std::time::{Duration, Instant};

    #[derive(Serialize)]
    #[serde(rename_all = "camelCase")]
    struct UncachedBorrowedLogEventPayload<'a> {
        events: Vec<&'a StatsigEventInternal>,
        statsig_metadata: &'a StatsigMetadataWithLogEventExtras,
    }

    fn make_event(time: u64, enqueued_at_ms: u64) -> EnqueuedEvent<StatsigEventInternal> {
        EnqueuedEvent::new(
            StatsigEventInternal::new(
                time,
                StatsigUserLoggable::null(),
                StatsigEvent {
                    event_name: "test_event".to_string(),
                    value: None,
                    metadata: None,
                    statsig_metadata: None,
                },
                None,
            ),
            enqueued_at_ms,
        )
    }

    #[test]
    fn max_event_queue_time_uses_oldest_enqueue_time() {
        let batch = EventBatch::new(vec![make_event(100, 300), make_event(200, 250)]);

        assert_eq!(batch.get_max_event_queue_time_ms(350), 100);
    }

    #[test]
    fn max_event_queue_time_saturates_at_zero() {
        let batch = EventBatch::new(vec![make_event(500, 200)]);

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }

    #[test]
    fn max_event_queue_time_defaults_for_empty_batch() {
        let batch = EventBatch::new(Vec::new());

        assert_eq!(batch.get_max_event_queue_time_ms(100), 0);
    }

    #[test]
    fn enqueue_metadata_is_not_serialized() {
        let batch = EventBatch::new(vec![make_event(100, 250)]);
        let request = batch.get_log_event_request(StatsigMetadata::get_with_log_event_extras(
            10,
            500,
            100,
            "test".to_string(),
        ));

        let events = request.payload.events.as_array().unwrap();
        assert_eq!(events.len(), 1);
        assert_eq!(events[0]["time"], 100);
        assert!(events[0].get("enqueued_at_ms").is_none());
        assert!(events[0].get("enqueuedAtMs").is_none());
    }

    #[test]
    fn serialized_request_matches_value_request() {
        let batch = EventBatch::new(vec![make_event(100, 250), make_event(200, 275)]);
        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "scheduled".to_string());
        let value_request = batch.get_log_event_request(metadata.clone());
        let serialized_request = batch.get_serialized_log_event_request(metadata).unwrap();

        assert_eq!(serialized_request.event_count, value_request.event_count);
        assert_eq!(serialized_request.retries, value_request.retries);
        assert_eq!(serialized_request.flush_type, "scheduled");
        let value_payload_bytes = serde_json::to_vec(&value_request.payload).unwrap();
        assert_eq!(
            serde_json::from_slice::<serde_json::Value>(&serialized_request.payload).unwrap(),
            serde_json::from_slice::<serde_json::Value>(&value_payload_bytes).unwrap(),
        );
        assert_eq!(serialized_request.payload, value_payload_bytes);
    }

    #[test]
    fn repeated_fast_user_cache_preserves_wire_bytes_and_cow_mutation() {
        let mut fast_user = production_fast_user();
        let environment = Some(UserDataMap::from_iter([(
            "tier".to_string(),
            DynamicValue::from_string("production"),
        )]));
        let global_custom = Some(HashMap::from([(
            "custom_0".to_string(),
            DynamicValue::from_string("global-fallback"),
        )]));
        let before = StatsigUserLoggable::new_fast(
            &fast_user.data,
            environment.clone(),
            global_custom.clone(),
        );
        let before_again = StatsigUserLoggable::new_fast(
            &fast_user.data,
            environment.clone(),
            global_custom.clone(),
        );
        assert!(same_fast_user_json(&before, &before_again));

        fast_user.set_email("changed@example.com".to_string());
        let after = StatsigUserLoggable::new_fast(
            &fast_user.data,
            environment.clone(),
            global_custom.clone(),
        );
        let changed_environment = StatsigUserLoggable::new_fast(
            &fast_user.data,
            Some(UserDataMap::from_iter([(
                "tier".to_string(),
                DynamicValue::from_string("staging"),
            )])),
            global_custom.clone(),
        );
        let changed_context = StatsigUserLoggable::new_fast(
            &fast_user.data,
            environment,
            Some(HashMap::from([(
                "custom_0".to_string(),
                DynamicValue::from_string("different-global"),
            )])),
        );
        assert!(!same_fast_user_json(&before, &after));
        assert!(!same_fast_user_json(&after, &changed_environment));
        assert!(!same_fast_user_json(&after, &changed_context));

        let batch = EventBatch::new(vec![
            make_event_for_user(100, before),
            make_event_for_user(101, before_again),
            make_event_for_user(102, after),
            make_event_for_user(103, changed_environment),
            make_event_for_user(104, changed_context),
        ]);
        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "scheduled".to_string());
        let uncached = serialize_uncached(&batch, &metadata);
        let cached = serialize_cached(&batch, &metadata);
        assert_eq!(cached, uncached);

        let payload: Value = serde_json::from_slice(&cached).unwrap();
        assert_eq!(payload["events"][0]["user"]["email"], "person@example.com");
        assert_eq!(payload["events"][2]["user"]["email"], "changed@example.com");
        assert_eq!(
            payload["events"][3]["user"]["statsigEnvironment"]["tier"],
            "staging"
        );
        assert_eq!(
            payload["events"][4]["user"]["custom"]["custom_0"],
            "value-0"
        );
    }

    #[test]
    fn fast_user_cache_rejects_equal_but_wire_distinct_overlay_values() {
        let fast_user = production_fast_user();

        let string_environment = StatsigUserLoggable::new_fast(
            &fast_user.data,
            Some(UserDataMap::from_iter([(
                "tier".to_string(),
                DynamicValue::from_string("1"),
            )])),
            None,
        );
        let integer_environment = StatsigUserLoggable::new_fast(
            &fast_user.data,
            Some(UserDataMap::from_iter([(
                "tier".to_string(),
                DynamicValue::from_i64(1),
            )])),
            None,
        );
        assert!(!same_fast_user_json(
            &string_environment,
            &integer_environment
        ));

        let integer_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_i64(1),
            )])),
        );
        let float_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_f64(1.0),
            )])),
        );
        assert!(!same_fast_user_json(
            &integer_global_custom,
            &float_global_custom
        ));

        let mut nested_left = serde_json::Map::new();
        nested_left.insert("first".to_string(), Value::from(1));
        nested_left.insert("second".to_string(), Value::from(2));
        let mut nested_right = serde_json::Map::new();
        nested_right.insert("second".to_string(), Value::from(2));
        nested_right.insert("first".to_string(), Value::from(1));
        let nested_left_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_json_value(Value::Object(nested_left)),
            )])),
        );
        let nested_right_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_json_value(Value::Object(nested_right)),
            )])),
        );
        assert!(!same_fast_user_json(
            &nested_left_global_custom,
            &nested_right_global_custom
        ));

        let positive_zero_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_f64(0.0),
            )])),
        );
        let negative_zero_global_custom = StatsigUserLoggable::new_fast(
            &fast_user.data,
            None,
            Some(HashMap::from([(
                "wire".to_string(),
                DynamicValue::from_f64(-0.0),
            )])),
        );
        assert!(!same_fast_user_json(
            &positive_zero_global_custom,
            &negative_zero_global_custom
        ));

        let batch = EventBatch::new(vec![
            make_event_for_user(100, string_environment.clone()),
            make_event_for_user(101, integer_environment.clone()),
            make_event_for_user(102, string_environment),
            make_event_for_user(103, integer_environment),
            make_event_for_user(104, integer_global_custom.clone()),
            make_event_for_user(105, float_global_custom.clone()),
            make_event_for_user(106, integer_global_custom),
            make_event_for_user(107, float_global_custom),
            make_event_for_user(108, nested_left_global_custom.clone()),
            make_event_for_user(109, nested_right_global_custom.clone()),
            make_event_for_user(110, nested_left_global_custom),
            make_event_for_user(111, nested_right_global_custom),
            make_event_for_user(112, positive_zero_global_custom.clone()),
            make_event_for_user(113, negative_zero_global_custom.clone()),
            make_event_for_user(114, positive_zero_global_custom),
            make_event_for_user(115, negative_zero_global_custom),
        ]);
        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "scheduled".to_string());
        let uncached = serialize_uncached(&batch, &metadata);
        let cached = serialize_cached(&batch, &metadata);
        assert_eq!(cached, uncached);

        let payload: Value = serde_json::from_slice(&cached).unwrap();
        let events = payload["events"].as_array().unwrap();
        for index in [0, 2] {
            assert_eq!(
                events[index]["user"]["statsigEnvironment"]["tier"],
                Value::from("1")
            );
        }
        for index in [1, 3] {
            assert_eq!(
                events[index]["user"]["statsigEnvironment"]["tier"],
                Value::from(1)
            );
        }
        for index in [4, 6] {
            assert_eq!(events[index]["user"]["custom"]["wire"].to_string(), "1");
        }
        for index in [5, 7] {
            assert_eq!(events[index]["user"]["custom"]["wire"].to_string(), "1.0");
        }
        for index in [8, 10] {
            assert_eq!(
                events[index]["user"]["custom"]["wire"].to_string(),
                r#"{"first":1,"second":2}"#
            );
        }
        for index in [9, 11] {
            assert_eq!(
                events[index]["user"]["custom"]["wire"].to_string(),
                r#"{"second":2,"first":1}"#
            );
        }
        for index in [12, 14] {
            assert_eq!(events[index]["user"]["custom"]["wire"].to_string(), "0.0");
        }
        for index in [13, 15] {
            assert_eq!(events[index]["user"]["custom"]["wire"].to_string(), "-0.0");
        }
    }

    #[test]
    fn fast_user_cache_is_bounded_and_public_users_bypass_it() {
        let repeated_groups = vec![2; MAX_CACHED_FAST_USERS_PER_BATCH + 16];
        let batch = production_shape_batch(&repeated_groups);
        let events = batch.iter_events().collect::<Vec<_>>();
        let reuse_index = FastUserReuseIndex::new(&events);
        let tracked_entries = reuse_index
            .entries_by_data
            .values()
            .map(Vec::len)
            .sum::<usize>();
        assert_eq!(tracked_entries, MAX_CACHED_FAST_USERS_PER_BATCH);

        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "scheduled".to_string());
        assert_eq!(
            serialize_cached(&batch, &metadata),
            serialize_uncached(&batch, &metadata)
        );

        let public_user = StatsigUserLoggable::null();
        let public_batch = EventBatch::new(vec![
            make_event_for_user(1, public_user.clone()),
            make_event_for_user(2, public_user),
        ]);
        let public_events = public_batch.iter_events().collect::<Vec<_>>();
        assert!(
            FastUserReuseIndex::new(&public_events)
                .entries_by_data
                .is_empty()
        );
        assert_eq!(
            serialize_cached(&public_batch, &metadata),
            serialize_uncached(&public_batch, &metadata)
        );
    }

    #[test]
    fn oversized_fast_user_is_not_retained_in_batch_cache() {
        let custom = FastUserCustomMap::from_iter([(
            "oversized".to_string(),
            UserValue::from("x".repeat(MAX_CACHED_FAST_USER_BYTES_PER_BATCH + 1)),
        )]);
        let fast_user = FastStatsigUser::new(FastUserData {
            user_id: Some(UserValue::from("oversized-user".to_string())),
            custom: Some(custom),
            ..FastUserData::default()
        });
        let user = StatsigUserLoggable::new_fast(&fast_user.data, None, None);
        let cache = RefCell::new(FastUserJsonCache {
            entries: Vec::new(),
            total_bytes: 0,
        });
        let cached_user = CachedFastUser {
            user: &user,
            should_cache: true,
            cache: &cache,
        };

        let expected = serde_json::to_vec(&user).unwrap();
        assert_eq!(serde_json::to_vec(&cached_user).unwrap(), expected);
        assert_eq!(serde_json::to_vec(&cached_user).unwrap(), expected);
        let cache = cache.borrow();
        assert_eq!(cache.entries.len(), 1);
        assert!(cache.entries[0].json.is_none());
        assert_eq!(cache.total_bytes, 0);
    }

    #[test]
    fn fast_user_cache_is_request_local_and_concurrent_serialization_is_exact() {
        let batch = production_shape_batch(&[132, 132, 25]);
        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "scheduled".to_string());
        let expected = serialize_uncached(&batch, &metadata);

        std::thread::scope(|scope| {
            let handles = (0..8)
                .map(|_| {
                    scope.spawn(|| {
                        for _ in 0..8 {
                            assert_eq!(serialize_cached(&batch, &metadata), expected);
                        }
                    })
                })
                .collect::<Vec<_>>();
            for handle in handles {
                handle.join().unwrap();
            }
        });
    }

    #[test]
    fn fast_user_cache_preserves_retry_payload_and_request_metadata() {
        let mut batch = production_shape_batch(&[132, 25]);
        let metadata =
            StatsigMetadata::get_with_log_event_extras(10, 500, 100, "retry-test".to_string());
        let first = batch
            .get_serialized_log_event_request(metadata.clone())
            .unwrap();
        batch.increment_attempts();
        let retry = batch.get_serialized_log_event_request(metadata).unwrap();

        assert_eq!(first.payload, retry.payload);
        assert_eq!(first.event_count, retry.event_count);
        assert_eq!(first.flush_type, retry.flush_type);
        assert_eq!(first.retries, 0);
        assert_eq!(retry.retries, 1);
    }

    #[test]
    #[ignore = "manual production-shape event serialization benchmark; run release, ignored, and nocapture"]
    fn benchmark_repeated_fast_user_serialization_and_direct_gzip() {
        const MEASURED_PAIRS: usize = 31;
        const WARMUP_PAIRS: usize = 3;

        let metadata = StatsigMetadata::get_with_log_event_extras(
            10_000,
            500,
            100,
            "scheduled_max_time".to_string(),
        );
        let repeated_batch = production_shape_batch(&[289]);
        let request_grouped_batch = production_shape_batch(&[132, 132, 25]);
        let unique_batch = production_shape_batch(&vec![1; 289]);

        for (name, batch) in [
            ("one repeated user", &repeated_batch),
            ("132-event request groups", &request_grouped_batch),
            ("all unique users", &unique_batch),
        ] {
            let uncached_json = serialize_uncached(batch, &metadata);
            let cached_json = serialize_cached(batch, &metadata);
            assert_eq!(cached_json, uncached_json);

            let json_result = paired_benchmark(
                WARMUP_PAIRS,
                MEASURED_PAIRS,
                || serialize_uncached(batch, &metadata),
                || serialize_cached(batch, &metadata),
            );
            let json_and_gzip_result = paired_benchmark(
                WARMUP_PAIRS,
                MEASURED_PAIRS,
                || compress_data(&serialize_uncached(batch, &metadata)).unwrap(),
                || compress_data(&serialize_cached(batch, &metadata)).unwrap(),
            );

            println!(
                "289-event/35-custom-field {name}: json={} bytes gzip={} bytes",
                uncached_json.len(),
                compress_data(&uncached_json).unwrap().len(),
            );
            print_benchmark("  user JSON cache, JSON only", &json_result, MEASURED_PAIRS);
            print_benchmark(
                "  user JSON cache, JSON + gzip",
                &json_and_gzip_result,
                MEASURED_PAIRS,
            );
        }

        let uncached_json = serialize_uncached(&request_grouped_batch, &metadata);
        let baseline_compressed = compress_data(&uncached_json).unwrap();
        let direct_gzip =
            serialize_uncached_directly_to_buffered_gzip(&request_grouped_batch, &metadata);
        assert_eq!(decompress_gzip(&direct_gzip), uncached_json);
        let direct_gzip_result = paired_benchmark(
            WARMUP_PAIRS,
            MEASURED_PAIRS,
            || compress_data(&serialize_uncached(&request_grouped_batch, &metadata)).unwrap(),
            || serialize_uncached_directly_to_buffered_gzip(&request_grouped_batch, &metadata),
        );

        println!(
            "289-event/35-custom-field buffered direct gzip: baseline={} bytes direct={} bytes",
            baseline_compressed.len(),
            direct_gzip.len(),
        );
        print_benchmark(
            "buffered direct JSON to gzip",
            &direct_gzip_result,
            MEASURED_PAIRS,
        );
    }

    fn production_fast_user() -> FastStatsigUser {
        production_fast_user_with_id("benchmark-user")
    }

    fn production_fast_user_with_id(user_id: &str) -> FastStatsigUser {
        let custom: FastUserCustomMap = (0..35)
            .map(|index| {
                (
                    format!("custom_{index}"),
                    UserValue::from(format!("value-{index}")),
                )
            })
            .collect();
        FastStatsigUser::new(FastUserData {
            user_id: Some(UserValue::from(user_id.to_string())),
            email: Some(UserValue::from("person@example.com".to_string())),
            country: Some(UserValue::from("US".to_string())),
            locale: Some(UserValue::from("en-US".to_string())),
            custom: Some(custom),
            ..FastUserData::default()
        })
    }

    fn production_shape_batch(group_sizes: &[usize]) -> EventBatch {
        let mut events = Vec::with_capacity(group_sizes.iter().sum());
        for (group, group_size) in group_sizes.iter().copied().enumerate() {
            let fast_user = production_fast_user_with_id(&format!("benchmark-user-{group}"));
            let environment = Some(UserDataMap::from_iter([(
                "tier".to_string(),
                DynamicValue::from_string("production"),
            )]));
            let global_custom = Some(
                (0..5)
                    .map(|index| {
                        (
                            format!("custom_{index}"),
                            DynamicValue::from_string(format!("global-{index}")),
                        )
                    })
                    .collect(),
            );
            let loggable =
                StatsigUserLoggable::new_fast(&fast_user.data, environment, global_custom);
            for _ in 0..group_size {
                let time = events.len() as u64;
                events.push(make_event_for_user(time, loggable.clone()));
            }
        }
        EventBatch::new(events)
    }

    fn make_event_for_user(
        time: u64,
        user: StatsigUserLoggable,
    ) -> EnqueuedEvent<StatsigEventInternal> {
        EnqueuedEvent::new(
            StatsigEventInternal::new(
                time,
                user,
                StatsigEvent {
                    event_name: "statsig::config_exposure".to_string(),
                    value: None,
                    metadata: Some(HashMap::from([
                        (
                            "config".to_string(),
                            Value::String("benchmark-config".to_string()),
                        ),
                        (
                            "ruleID".to_string(),
                            Value::String("benchmark-rule".to_string()),
                        ),
                    ])),
                    statsig_metadata: None,
                },
                None,
            ),
            time,
        )
    }

    fn serialize_uncached(
        batch: &EventBatch,
        metadata: &StatsigMetadataWithLogEventExtras,
    ) -> Vec<u8> {
        serde_json::to_vec(&UncachedBorrowedLogEventPayload {
            events: batch.iter_events().collect(),
            statsig_metadata: metadata,
        })
        .unwrap()
    }

    fn serialize_cached(
        batch: &EventBatch,
        metadata: &StatsigMetadataWithLogEventExtras,
    ) -> Vec<u8> {
        serde_json::to_vec(&BorrowedLogEventPayload {
            events: CachedEventSequence {
                events: batch.iter_events().collect(),
            },
            statsig_metadata: metadata,
        })
        .unwrap()
    }

    fn serialize_uncached_directly_to_buffered_gzip(
        batch: &EventBatch,
        metadata: &StatsigMetadataWithLogEventExtras,
    ) -> Vec<u8> {
        let encoder = GzEncoder::new(Vec::new(), Compression::new(6));
        let mut writer = BufWriter::with_capacity(64 * 1024, encoder);
        serde_json::to_writer(
            &mut writer,
            &UncachedBorrowedLogEventPayload {
                events: batch.iter_events().collect(),
                statsig_metadata: metadata,
            },
        )
        .unwrap();
        writer.flush().unwrap();
        let encoder = writer.into_inner().unwrap();
        encoder.finish().unwrap()
    }

    fn decompress_gzip(payload: &[u8]) -> Vec<u8> {
        let mut decoder = GzDecoder::new(payload);
        let mut decompressed = Vec::new();
        decoder.read_to_end(&mut decompressed).unwrap();
        decompressed
    }

    struct BenchmarkResult {
        baseline_median: Duration,
        candidate_median: Duration,
        paired_median_improvement: f64,
        wins: usize,
    }

    fn paired_benchmark(
        warmup_pairs: usize,
        measured_pairs: usize,
        mut baseline: impl FnMut() -> Vec<u8>,
        mut candidate: impl FnMut() -> Vec<u8>,
    ) -> BenchmarkResult {
        let mut baseline_samples = Vec::with_capacity(measured_pairs);
        let mut candidate_samples = Vec::with_capacity(measured_pairs);
        let mut improvements = Vec::with_capacity(measured_pairs);

        for pair in 0..warmup_pairs + measured_pairs {
            let candidate_first = pair % 2 == 1;
            let (first_elapsed, _first_len) = if candidate_first {
                timed(&mut candidate)
            } else {
                timed(&mut baseline)
            };
            let (second_elapsed, _second_len) = if candidate_first {
                timed(&mut baseline)
            } else {
                timed(&mut candidate)
            };

            if pair >= warmup_pairs {
                let (baseline_elapsed, candidate_elapsed) = if candidate_first {
                    (second_elapsed, first_elapsed)
                } else {
                    (first_elapsed, second_elapsed)
                };
                let baseline_ns = baseline_elapsed.as_nanos() as f64;
                let candidate_ns = candidate_elapsed.as_nanos() as f64;
                baseline_samples.push(baseline_elapsed);
                candidate_samples.push(candidate_elapsed);
                improvements.push((baseline_ns - candidate_ns) / baseline_ns * 100.0);
            }
        }

        baseline_samples.sort();
        candidate_samples.sort();
        let wins = improvements
            .iter()
            .filter(|improvement| **improvement > 0.0)
            .count();
        improvements.sort_by(f64::total_cmp);
        BenchmarkResult {
            baseline_median: baseline_samples[measured_pairs / 2],
            candidate_median: candidate_samples[measured_pairs / 2],
            paired_median_improvement: improvements[measured_pairs / 2],
            wins,
        }
    }

    fn timed(run: &mut impl FnMut() -> Vec<u8>) -> (Duration, usize) {
        let start = Instant::now();
        let bytes = black_box(run());
        (start.elapsed(), black_box(bytes.len()))
    }

    fn print_benchmark(name: &str, result: &BenchmarkResult, measured_pairs: usize) {
        println!(
            "{name}: baseline={:.3}ms candidate={:.3}ms paired-median-improvement={:.2}% wins={}/{}",
            result.baseline_median.as_secs_f64() * 1_000.0,
            result.candidate_median.as_secs_f64() * 1_000.0,
            result.paired_median_improvement,
            result.wins,
            measured_pairs,
        );
    }
}
