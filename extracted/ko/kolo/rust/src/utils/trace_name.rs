use hashbrown::HashMap;
use std::ops::Range;

use super::frame_store::FrameSequence;
#[cfg(test)]
use super::frame_store::SerializedFrame;

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) enum TraceNameObservationKind {
    StartTest {
        test_name: String,
        test_class: Option<String>,
    },
    DjangoRequest {
        method: String,
        path: String,
    },
    DjangoResponse {
        status: String,
    },
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct TraceNameObservation {
    pub(crate) frame_index: usize,
    pub(crate) kind: TraceNameObservationKind,
}

const TRACE_NAME_OBSERVATION_LIMIT: usize = 64;
const TRACE_NAME_OBSERVATION_BYTES_LIMIT: usize = 64 * 1024;

#[derive(Clone, Debug, PartialEq, Eq)]
pub(crate) struct TraceNameIndex {
    // None means observation retention exceeded its hard bound. Exact naming
    // then falls back to positional frame reads at build/save time.
    observations: Option<Vec<TraceNameObservation>>,
    retained_bytes: usize,
}

impl Default for TraceNameIndex {
    fn default() -> Self {
        Self {
            observations: Some(Vec::new()),
            retained_bytes: 0,
        }
    }
}

fn observation_bytes(observation: &TraceNameObservation) -> usize {
    match &observation.kind {
        TraceNameObservationKind::StartTest {
            test_name,
            test_class,
        } => test_name.len() + test_class.as_ref().map_or(0, String::len),
        TraceNameObservationKind::DjangoRequest { method, path } => method.len() + path.len(),
        TraceNameObservationKind::DjangoResponse { status } => status.len(),
    }
}

impl TraceNameIndex {
    pub(crate) fn observations(&self) -> Option<&[TraceNameObservation]> {
        self.observations.as_deref()
    }

    pub(crate) fn mark_incomplete(&mut self) {
        self.observations = None;
        self.retained_bytes = 0;
    }

    pub(crate) fn observe(&mut self, frame_index: usize, frame_type: &str, frame: &[u8]) {
        if self.observations.is_none() {
            return;
        }
        if !matches!(
            frame_type,
            "start_test" | "django_request" | "django_response"
        ) {
            return;
        }
        let Some(observation) = trace_name_observation(frame_index, frame_type, frame) else {
            // A relevant frame which the sidecar cannot reproduce must not be
            // silently omitted: the positional resolver still observes it and
            // its first-request/last-response precedence may affect the name.
            self.mark_incomplete();
            return;
        };
        let observations = self
            .observations
            .as_mut()
            .expect("trace-name index completeness checked above");
        let retained_bytes = self
            .retained_bytes
            .saturating_add(observation_bytes(&observation));
        if observations.len() >= TRACE_NAME_OBSERVATION_LIMIT
            || retained_bytes > TRACE_NAME_OBSERVATION_BYTES_LIMIT
        {
            self.mark_incomplete();
            return;
        }
        observations.push(observation);
        self.retained_bytes = retained_bytes;
    }

    pub(crate) fn merge(&mut self, mut other: Self) {
        let (Some(observations), Some(other_observations)) =
            (self.observations.as_mut(), other.observations.as_mut())
        else {
            self.mark_incomplete();
            return;
        };
        let retained_bytes = self.retained_bytes.saturating_add(other.retained_bytes);
        if observations.len().saturating_add(other_observations.len())
            > TRACE_NAME_OBSERVATION_LIMIT
            || retained_bytes > TRACE_NAME_OBSERVATION_BYTES_LIMIT
        {
            self.mark_incomplete();
            return;
        }
        observations.append(other_observations);
        observations.sort_unstable_by_key(|observation| observation.frame_index);
        self.retained_bytes = retained_bytes;
    }

    pub(crate) fn drain(&mut self, range: Range<usize>) -> Self {
        let Some(observations) = self.observations.as_mut() else {
            return Self {
                observations: None,
                retained_bytes: 0,
            };
        };
        let mut removed = Vec::new();
        let mut remaining = Vec::new();
        for mut observation in observations.drain(..) {
            if range.contains(&observation.frame_index) {
                observation.frame_index -= range.start;
                removed.push(observation);
            } else {
                if observation.frame_index >= range.end {
                    observation.frame_index -= range.len();
                }
                remaining.push(observation);
            }
        }
        let removed_bytes = removed.iter().map(observation_bytes).sum();
        self.retained_bytes = remaining.iter().map(observation_bytes).sum();
        *observations = remaining;
        Self {
            observations: Some(removed),
            retained_bytes: removed_bytes,
        }
    }

    pub(crate) fn shift_for_insert(&mut self, index: usize, inserted_frames: usize) {
        let Some(observations) = self.observations.as_mut() else {
            return;
        };
        for observation in observations {
            if observation.frame_index >= index {
                observation.frame_index += inserted_frames;
            }
        }
    }
}

fn map_string(frame_map: &[(rmpv::Value, rmpv::Value)], key: &str) -> Option<String> {
    frame_map
        .iter()
        .find(|(candidate, _)| candidate.as_str() == Some(key))
        .and_then(|(_, value)| value.as_str())
        .map(str::to_string)
}

/// Extract only the tiny fields needed to name a complete capture. Irrelevant
/// plugin frame types return before decoding, and ordinary Python callbacks do
/// not enter the plugin batch path at all.
pub(crate) fn trace_name_observation(
    frame_index: usize,
    frame_type: &str,
    frame: &[u8],
) -> Option<TraceNameObservation> {
    if !matches!(
        frame_type,
        "start_test" | "django_request" | "django_response"
    ) {
        return None;
    }
    let mut frame = frame;
    let rmpv::Value::Map(frame_map) = rmpv::decode::read_value(&mut frame).ok()? else {
        return None;
    };
    let kind = match frame_type {
        "start_test" => TraceNameObservationKind::StartTest {
            test_name: map_string(&frame_map, "test_name")?,
            test_class: map_string(&frame_map, "test_class"),
        },
        "django_request" => TraceNameObservationKind::DjangoRequest {
            method: map_string(&frame_map, "method")?,
            path: map_string(&frame_map, "path_info")?,
        },
        "django_response" => {
            let status = frame_map
                .iter()
                .find(|(candidate, _)| candidate.as_str() == Some("status_code"))
                .and_then(|(_, value)| match value {
                    rmpv::Value::Integer(value) => Some(value.to_string()),
                    _ => None,
                })?;
            TraceNameObservationKind::DjangoResponse { status }
        }
        _ => unreachable!("relevant frame types checked above"),
    };
    Some(TraceNameObservation { frame_index, kind })
}

fn trace_name_from_observations(
    observations: &[TraceNameObservation],
    frame_count: usize,
) -> Option<String> {
    let relevant = relevant_frame_indices(frame_count);
    let mut request = None;
    let mut response = None;
    for observation in observations
        .iter()
        .filter(|observation| relevant.binary_search(&observation.frame_index).is_ok())
    {
        match &observation.kind {
            TraceNameObservationKind::StartTest {
                test_name,
                test_class,
            } => {
                return Some(match test_class {
                    Some(test_class) => format!("{test_class}.{test_name}"),
                    None => test_name.clone(),
                });
            }
            TraceNameObservationKind::DjangoRequest { method, path } if request.is_none() => {
                request = Some((method, path));
            }
            TraceNameObservationKind::DjangoResponse { status } => response = Some(status),
            _ => {}
        }
    }
    request
        .zip(response)
        .map(|((method, path), status)| format!("{status} {method} {path}"))
}

pub(crate) fn resolve_full_trace_name(
    cached_trace_name: &mut Option<String>,
    observations: &[TraceNameObservation],
    frame_count: usize,
) -> Option<String> {
    if let Some(trace_name) = cached_trace_name.clone() {
        return Some(trace_name);
    }
    let trace_name = trace_name_from_observations(observations, frame_count);
    *cached_trace_name = trace_name.clone();
    trace_name
}

/// Extract HTTP request/response information from frames to set a trace name.
/// Looks for django_request and django_response frame types from the Django filter.
fn relevant_frame_indices(frame_count: usize) -> Vec<usize> {
    let mut indices: Vec<_> = (0..frame_count.min(3)).collect();
    let tail_start = frame_count.saturating_sub(3);
    indices.extend(tail_start..frame_count);
    indices.sort_unstable();
    indices.dedup();
    indices
}

pub fn extract_http_trace_name<S: FrameSequence>(
    frames_by_thread: &HashMap<String, S>,
    current_thread_id: &str,
) -> Option<String> {
    let frames = frames_by_thread.get(current_thread_id)?;

    let mut request_frame = None;
    let mut response_frame = None;

    // Look for django_request and django_response frames
    let mut scratch = Vec::new();
    for index in relevant_frame_indices(frames.len()) {
        let frame_bytes = frames.frame(index, &mut scratch).ok()?;
        if let Ok(frame) = rmpv::decode::read_value(&mut &frame_bytes[..]) {
            if let rmpv::Value::Map(frame_map) = frame {
                // Extract frame type
                let frame_type = frame_map
                    .iter()
                    .find(|(k, _)| k == &rmpv::Value::String("type".into()))
                    .and_then(|(_, v)| match v {
                        rmpv::Value::String(s) => s.as_str(),
                        _ => None,
                    });

                match frame_type {
                    Some("django_request") if request_frame.is_none() => {
                        // First request frame wins
                        request_frame = Some(frame_map);
                    }
                    Some("django_response") => {
                        // Last response frame wins (since we're iterating in order)
                        response_frame = Some(frame_map);
                    }
                    _ => {}
                }
            }
        }
    }

    // Extract trace name components if we have both frames
    if let (Some(req), Some(res)) = (&request_frame, &response_frame) {
        let method = req
            .iter()
            .find(|(k, _)| k == &rmpv::Value::String("method".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None,
            });

        let path = req
            .iter()
            .find(|(k, _)| k == &rmpv::Value::String("path_info".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None,
            });

        let status_code = res
            .iter()
            .find(|(k, _)| k == &rmpv::Value::String("status_code".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::Integer(n) => Some(n.to_string()),
                _ => None,
            });

        if let (Some(method), Some(path), Some(status)) = (method, path, status_code) {
            return Some(format!("{} {} {}", status, method, path));
        }
    }

    None
}

pub fn extract_test_trace_name<S: FrameSequence>(
    frames_by_thread: &HashMap<String, S>,
    current_thread_id: &str,
) -> Option<String> {
    let frames = frames_by_thread.get(current_thread_id)?;
    if frames.is_empty() {
        return None;
    }

    let mut start_test_frame = None;
    // we don't actually need anything stored under _end_test_frame yet
    let mut _end_test_frame = None;

    // Look for start_test and end_test frames
    let mut scratch = Vec::new();
    for index in relevant_frame_indices(frames.len()) {
        let frame_bytes = frames.frame(index, &mut scratch).ok()?;
        if let Ok(frame) = rmpv::decode::read_value(&mut &frame_bytes[..]) {
            if let rmpv::Value::Map(frame_map) = frame {
                // Extract frame type
                let frame_type = frame_map
                    .iter()
                    .find(|(k, _)| k == &rmpv::Value::String("type".into()))
                    .and_then(|(_, v)| match v {
                        rmpv::Value::String(s) => s.as_str(),
                        _ => None,
                    });

                match frame_type {
                    Some("start_test") if start_test_frame.is_none() => {
                        // First start_test frame wins
                        start_test_frame = Some(frame_map);
                    }
                    Some("end_test") => {
                        // Last end_test frame wins (since we're iterating in order)
                        _end_test_frame = Some(frame_map);
                    }
                    _ => {}
                }
            }
        }
    }

    // Extract trace name components if we have both frames
    if let Some(start) = start_test_frame {
        let test_name = start
            .iter()
            .find(|(k, _)| k == &rmpv::Value::String("test_name".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None,
            })?;

        let test_class = start
            .iter()
            .find(|(k, _)| k == &rmpv::Value::String("test_class".into()))
            .and_then(|(_, v)| match v {
                rmpv::Value::String(s) => s.as_str(),
                _ => None,
            });

        return Some(match test_class {
            Some(class_name) => format!("{}.{}", class_name, test_name),
            None => test_name.to_string(),
        });
    }

    None
}

pub fn extract_trace_name<S: FrameSequence>(
    frames_by_thread: &HashMap<String, S>,
    current_thread_id: &str,
) -> Option<String> {
    extract_test_trace_name(frames_by_thread, current_thread_id)
        .or_else(|| extract_http_trace_name(frames_by_thread, current_thread_id))
}

pub fn resolve_trace_name<S: FrameSequence>(
    cached_trace_name: &mut Option<String>,
    frames_by_thread: &HashMap<String, S>,
    current_thread_id: &str,
    should_cache: bool,
) -> Option<String> {
    if let Some(trace_name) = cached_trace_name.clone() {
        return Some(trace_name);
    }

    let trace_name = extract_trace_name(frames_by_thread, current_thread_id);
    if should_cache {
        *cached_trace_name = trace_name.clone();
    }
    trace_name
}

#[cfg(test)]
mod trace_name_tests {
    use super::*;
    use rmpv::Value;

    fn pack_frame(entries: Vec<(&str, Value)>) -> SerializedFrame {
        let value = Value::Map(
            entries
                .into_iter()
                .map(|(key, value)| (Value::String(key.into()), value))
                .collect(),
        );
        let mut frame = Vec::new();
        rmpv::encode::write_value(&mut frame, &value).unwrap();
        frame
    }

    #[test]
    fn test_resolve_trace_name_caches_test_name() {
        let mut frames_by_thread = HashMap::new();
        frames_by_thread.insert(
            "thread".to_string(),
            vec![pack_frame(vec![
                ("type", Value::String("start_test".into())),
                ("test_name", Value::String("test_example".into())),
                ("test_class", Value::String("Suite".into())),
            ])],
        );

        let mut trace_name = None;
        assert_eq!(
            resolve_trace_name(&mut trace_name, &frames_by_thread, "thread", true),
            Some("Suite.test_example".to_string())
        );
        assert_eq!(trace_name.as_deref(), Some("Suite.test_example"));
    }

    #[test]
    fn test_resolve_trace_name_preserves_existing_name() {
        let mut frames_by_thread = HashMap::new();
        frames_by_thread.insert(
            "thread".to_string(),
            vec![pack_frame(vec![
                ("type", Value::String("start_test".into())),
                ("test_name", Value::String("test_example".into())),
            ])],
        );

        let mut trace_name = Some("existing".to_string());
        assert_eq!(
            resolve_trace_name(&mut trace_name, &frames_by_thread, "thread", true),
            Some("existing".to_string())
        );
        assert_eq!(trace_name.as_deref(), Some("existing"));
    }

    #[test]
    fn test_resolve_trace_name_can_skip_caching() {
        let mut frames_by_thread = HashMap::new();
        frames_by_thread.insert(
            "thread".to_string(),
            vec![pack_frame(vec![
                ("type", Value::String("start_test".into())),
                ("test_name", Value::String("test_example".into())),
            ])],
        );

        let mut trace_name = None;
        assert_eq!(
            resolve_trace_name(&mut trace_name, &frames_by_thread, "thread", false),
            Some("test_example".to_string())
        );
        assert_eq!(trace_name, None);
    }

    #[test]
    fn full_trace_observations_match_test_and_http_name_semantics() {
        let request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            ("path_info", Value::String("/polls".into())),
        ]);
        let ignored_request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("POST".into())),
            ("path_info", Value::String("/ignored".into())),
        ]);
        let ignored_response = pack_frame(vec![
            ("type", Value::String("django_response".into())),
            ("status_code", Value::Integer(500.into())),
        ]);
        let response = pack_frame(vec![
            ("type", Value::String("django_response".into())),
            ("status_code", Value::Integer(u64::MAX.into())),
        ]);
        let start_test = pack_frame(vec![
            ("type", Value::String("start_test".into())),
            ("test_name", Value::String("test_poll".into())),
            ("test_class", Value::String("PollTests".into())),
        ]);

        let http_observations = [
            trace_name_observation(0, "django_request", &request).unwrap(),
            trace_name_observation(1, "django_request", &ignored_request).unwrap(),
            trace_name_observation(4, "django_response", &ignored_response).unwrap(),
            trace_name_observation(5, "django_response", &response).unwrap(),
        ];
        let mut trace_name = None;
        assert_eq!(
            resolve_full_trace_name(&mut trace_name, &http_observations, 6).as_deref(),
            Some("18446744073709551615 GET /polls")
        );

        let mut test_observations = http_observations.to_vec();
        test_observations.push(trace_name_observation(2, "start_test", &start_test).unwrap());
        test_observations.sort_unstable_by_key(|observation| observation.frame_index);
        let mut trace_name = None;
        assert_eq!(
            resolve_full_trace_name(&mut trace_name, &test_observations, 6).as_deref(),
            Some("PollTests.test_poll"),
            "test names retain precedence over HTTP names"
        );

        let mut cached = Some("explicit".to_string());
        assert_eq!(
            resolve_full_trace_name(&mut cached, &test_observations, 6).as_deref(),
            Some("explicit"),
            "an explicit cached name retains precedence over observations"
        );
    }

    #[test]
    fn full_trace_observations_preserve_first_and_last_three_boundary() {
        let request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            ("path_info", Value::String("/middle".into())),
        ]);
        let response = pack_frame(vec![
            ("type", Value::String("django_response".into())),
            ("status_code", Value::Integer(200.into())),
        ]);
        let observations = [
            trace_name_observation(3, "django_request", &request).unwrap(),
            trace_name_observation(6, "django_response", &response).unwrap(),
        ];
        let mut trace_name = None;
        assert_eq!(
            resolve_full_trace_name(&mut trace_name, &observations, 7),
            None,
            "an HTTP request outside the first/last-three window stays invisible"
        );
    }

    #[test]
    fn irrelevant_or_malformed_frames_create_no_observation() {
        assert_eq!(trace_name_observation(0, "frame", b"not msgpack"), None);
        assert_eq!(
            trace_name_observation(0, "django_request", b"not msgpack"),
            None
        );
    }

    #[test]
    fn malformed_relevant_frame_forces_positional_fallback() {
        let mut index = TraceNameIndex::default();
        index.observe(0, "frame", b"not msgpack");
        assert_eq!(index.observations(), Some([].as_slice()));

        index.observe(1, "django_request", b"not msgpack");
        assert_eq!(index.observations(), None);

        let request_missing_method = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("path_info", Value::String("/first".into())),
        ]);
        let mut index = TraceNameIndex::default();
        index.observe(0, "django_request", &request_missing_method);
        assert_eq!(index.observations(), None);
    }

    #[test]
    fn trace_name_index_is_bounded_by_count_and_propagates_incompleteness() {
        let request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            ("path_info", Value::String("/polls".into())),
        ]);
        let mut index = TraceNameIndex::default();
        for frame_index in 0..=TRACE_NAME_OBSERVATION_LIMIT {
            index.observe(frame_index, "django_request", &request);
        }
        assert_eq!(index.observations(), None);

        let removed = index.drain(0..1);
        assert_eq!(index.observations(), None);
        assert_eq!(removed.observations(), None);

        let mut complete = TraceNameIndex::default();
        complete.merge(removed);
        assert_eq!(complete.observations(), None);
    }

    #[test]
    fn trace_name_index_rejects_one_oversized_field() {
        let request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            (
                "path_info",
                Value::String("x".repeat(TRACE_NAME_OBSERVATION_BYTES_LIMIT + 1).into()),
            ),
        ]);
        let mut index = TraceNameIndex::default();
        index.observe(0, "django_request", &request);
        assert_eq!(index.observations(), None);
    }

    #[test]
    fn merging_complete_indexes_enforces_combined_count_and_byte_bounds() {
        let request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            ("path_info", Value::String("/polls".into())),
        ]);
        let mut left = TraceNameIndex::default();
        let mut right = TraceNameIndex::default();
        for frame_index in 0..32 {
            left.observe(frame_index, "django_request", &request);
        }
        for frame_index in 32..64 {
            right.observe(frame_index, "django_request", &request);
        }
        assert!(left.observations().is_some());
        assert!(right.observations().is_some());
        left.merge(right);
        assert_eq!(left.observations().unwrap().len(), 64);

        let mut left = TraceNameIndex::default();
        let mut right = TraceNameIndex::default();
        for frame_index in 0..32 {
            left.observe(frame_index, "django_request", &request);
        }
        for frame_index in 32..65 {
            right.observe(frame_index, "django_request", &request);
        }
        left.merge(right);
        assert_eq!(left.observations(), None);

        let exact_half_request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            (
                "path_info",
                Value::String(
                    "x".repeat(TRACE_NAME_OBSERVATION_BYTES_LIMIT / 2 - "GET".len())
                        .into(),
                ),
            ),
        ]);
        let mut left = TraceNameIndex::default();
        let mut right = TraceNameIndex::default();
        left.observe(0, "django_request", &exact_half_request);
        right.observe(1, "django_request", &exact_half_request);
        left.merge(right);
        assert_eq!(left.retained_bytes, TRACE_NAME_OBSERVATION_BYTES_LIMIT);
        assert_eq!(left.observations().unwrap().len(), 2);

        let one_byte_over_half_request = pack_frame(vec![
            ("type", Value::String("django_request".into())),
            ("method", Value::String("GET".into())),
            (
                "path_info",
                Value::String(
                    "x".repeat(TRACE_NAME_OBSERVATION_BYTES_LIMIT / 2 - "GET".len() + 1)
                        .into(),
                ),
            ),
        ]);
        let mut left = TraceNameIndex::default();
        let mut right = TraceNameIndex::default();
        left.observe(0, "django_request", &exact_half_request);
        right.observe(1, "django_request", &one_byte_over_half_request);
        left.merge(right);
        assert_eq!(left.observations(), None);
    }
}
