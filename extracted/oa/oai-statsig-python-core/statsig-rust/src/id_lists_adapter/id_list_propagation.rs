use std::ops::Range;

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

#[derive(Default)]
pub(crate) struct IdListPropagationState {
    file_id: Option<String>,
    url: String,
    applied_size: u64,
    ts: u64,
}

impl IdListPropagationState {
    // Called only after the list snapshot has been published, under the store update lock.
    pub(crate) fn apply(
        &mut self,
        update: IdListPropagationUpdate,
        initialized: bool,
        now: u64,
    ) -> Option<(u64, u64)> {
        if update.file_id.as_deref().is_none_or(str::is_empty) {
            self.applied_size = 0;
            return None;
        }
        let file_changed = self.file_id != update.file_id;
        if file_changed || self.url != update.url {
            self.file_id = update.file_id;
            self.url = update.url;
            self.applied_size = 0;
        }
        let previous_size = self.applied_size;
        let installed_empty_file = file_changed && update.applied_range == Some(0..0);
        if let Some(range) = update.applied_range {
            if range.start <= self.applied_size {
                self.applied_size = self.applied_size.max(range.end);
            }
        }
        let ts = update.ts?;
        // ts belongs to the readable file. Use its existing advertised size as the
        // boundary, rather than adding another field or inspecting individual IDs.
        if ts <= self.ts || ts > now || update.size > self.applied_size {
            return None;
        }
        let previous_ts = self.ts;
        self.ts = ts;
        // Metadata arriving after its bytes were applied cannot establish t2.
        (initialized && (previous_size < update.size || installed_empty_file))
            .then_some((ts, previous_ts))
    }
}

// This proof is only for telemetry. An absent/invalid range never fails a download.
pub(super) fn downloaded_range(
    status: Option<u16>,
    content_range: Option<&str>,
    requested_start: u64,
    body_len: usize,
    cdn_query_range: bool,
) -> Option<Range<u64>> {
    let len = u64::try_from(body_len).ok()?;
    if let Some(header) = content_range {
        let (range, total) = header.strip_prefix("bytes ")?.split_once('/')?;
        let (start, end) = range.split_once('-')?;
        let start = start.parse::<u64>().ok()?;
        let end = end.parse::<u64>().ok()?.checked_add(1)?;
        let total = total.parse::<u64>().ok()?;
        return (end <= total && end.checked_sub(start) == Some(len)).then_some(start..end);
    }
    // The default CDN implements ranges through a query parameter and returns HTTP 200.
    // A normal HTTP server may ignore Range and return the entire file instead.
    if status != Some(200) {
        return None;
    }
    let start = if cdn_query_range { requested_start } else { 0 };
    Some(start..start.checked_add(len)?)
}
