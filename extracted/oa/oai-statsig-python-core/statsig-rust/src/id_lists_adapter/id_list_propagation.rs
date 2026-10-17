use std::{collections::VecDeque, ops::Range};

use serde::{Deserialize, Deserializer};

use super::IdListMetadata;

/// Optional delivery evidence for ID-list propagation telemetry.
/// Existing listeners may ignore this and continue receiving ordinary list updates.
pub struct IdListPropagationUpdate {
    pub(crate) file_id: Option<String>,
    pub(crate) url: String,
    pub(crate) ts: Option<u64>,
    pub(crate) size: u64,
    pub(crate) applied_range: Option<Range<u64>>,
}

// Keep telemetry out of the public metadata struct and tolerate malformed optional fields.
#[derive(Deserialize)]
pub(super) struct IdListManifestEntry {
    #[serde(flatten)]
    pub metadata: IdListMetadata,
    #[serde(default, deserialize_with = "optional_u64")]
    ts: Option<u64>,
}

fn optional_u64<'de, D: Deserializer<'de>>(deserializer: D) -> Result<Option<u64>, D::Error> {
    Ok(serde_json::Value::deserialize(deserializer)?.as_u64())
}

impl IdListManifestEntry {
    pub fn propagation_update(&self) -> IdListPropagationUpdate {
        IdListPropagationUpdate {
            file_id: self.metadata.file_id.clone(),
            url: file_identity_url(&self.metadata.url),
            ts: self.ts.filter(|ts| *ts > 0),
            size: self.metadata.size,
            applied_range: None,
        }
    }
}

fn file_identity_url(raw_url: &str) -> String {
    let Ok(mut url) = url::Url::parse(raw_url) else {
        return raw_url.to_owned();
    };
    // SAS renewal changes expiry/signature, not the file. Keep routing fields such as private=true.
    let query: Vec<_> = url
        .query_pairs()
        .filter(|(key, _)| !matches!(key.as_ref(), "se" | "sig"))
        .map(|(key, value)| (key.into_owned(), value.into_owned()))
        .collect();
    url.set_query(None);
    if !query.is_empty() {
        url.query_pairs_mut().extend_pairs(query);
    }
    url.into()
}

// Bound telemetry memory when a manifest omits timestamps for many updates.
const MAX_APPLIED_INTERVALS: usize = 64;

struct AppliedInterval {
    start: u64,
    end: u64,
    applied_at: u64,
}

#[derive(Default)]
pub(crate) struct IdListPropagationState {
    file_id: Option<String>,
    url: String,
    applied_size: u64,
    cold_size: u64,
    ts: u64,
    applied_intervals: VecDeque<AppliedInterval>,
}

impl IdListPropagationState {
    // Called only after the list snapshot has been published, under the store update lock.
    pub(crate) fn apply(
        &mut self,
        update: IdListPropagationUpdate,
        published_size: u64,
        initialized: bool,
        now: u64,
    ) -> Option<(u64, u64, u64)> {
        if update.file_id.as_deref().is_none_or(str::is_empty) {
            self.applied_size = 0;
            self.cold_size = 0;
            self.applied_intervals.clear();
            return None;
        }
        let file_changed = self.file_id != update.file_id;
        if file_changed || self.url != update.url {
            self.file_id = update.file_id;
            self.url = update.url;
            self.applied_size = 0;
            self.cold_size = 0;
            self.applied_intervals.clear();
        }
        if !initialized {
            // Initial hydration can take several downloads. Its original
            // boundary and timestamp remain cold even after the first poll.
            self.cold_size = update.size;
            if let Some(ts) = update.ts.filter(|ts| *ts <= now) {
                self.ts = self.ts.max(ts);
            }
        }
        let previous_size = self.applied_size;
        let installed_empty_file = file_changed && update.applied_range == Some(0..0);
        if let Some(range) = update.applied_range {
            if range.start <= self.applied_size {
                self.applied_size = self.applied_size.max(range.end);
            }
        }
        // Bytes may arrive before their source timestamp. Retain their first
        // publication time, without retiming replays or recording cold loads.
        let start = previous_size.max(self.cold_size);
        if initialized && (start < self.applied_size || installed_empty_file) {
            if self.applied_intervals.len() == MAX_APPLIED_INTERVALS {
                self.applied_intervals.pop_front();
            }
            self.applied_intervals.push_back(AppliedInterval {
                start,
                end: self.applied_size,
                applied_at: now,
            });
        }
        let ts = update.ts?;
        // ts belongs to the readable file. Use its existing advertised size as the
        // boundary, rather than adding another field or inspecting individual IDs.
        // A same-file replay can temporarily reset the published cursor while
        // its original application history remains valid.
        if ts <= self.ts
            || ts > now
            || update.size > self.applied_size
            || update.size > published_size
        {
            return None;
        }
        let previous_ts = self.ts;
        self.ts = ts;
        let applied = self.applied_intervals.iter().find(|interval| {
            (interval.start < update.size && update.size <= interval.end)
                || (update.size == 0 && interval.start == 0 && interval.end == 0)
        })?;
        // An evicted prefix, cold load, or timestamp newer than its bytes cannot
        // establish a propagation sample. Metadata arrival is never a new t2.
        (initialized && ts <= applied.applied_at).then_some((ts, previous_ts, applied.applied_at))
    }
}

#[cfg(test)]
#[path = "__tests__/id_list_propagation_state_tests.rs"]
mod tests;

// Validate the received interval before applying bytes or recording propagation.
pub(super) fn downloaded_range(content_range: &str, body_len: usize) -> Option<Range<u64>> {
    let len = u64::try_from(body_len).ok()?;
    let (range, total) = content_range.strip_prefix("bytes ")?.split_once('/')?;
    let (start, end) = range.split_once('-')?;
    let start = start.parse::<u64>().ok()?;
    let end = end.parse::<u64>().ok()?.checked_add(1)?;
    let total = total.parse::<u64>().ok()?;
    (end <= total && end.checked_sub(start) == Some(len)).then_some(start..end)
}
