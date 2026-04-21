use crate::anthropic::stream::StreamEvent;

pub fn parse_sse_events(sse_text: &str) -> Vec<StreamEvent> {
    let mut events = Vec::new();
    let mut current_data = String::new();

    for line in sse_text.lines() {
        if line.starts_with("data: ") {
            current_data = line.strip_prefix("data: ").unwrap_or("").to_string();
        } else if line.is_empty() && !current_data.is_empty() {
            if let Ok(event) = serde_json::from_str::<StreamEvent>(&current_data) {
                events.push(event);
            }
            current_data.clear();
        }
    }

    if !current_data.is_empty() {
        if let Ok(event) = serde_json::from_str::<StreamEvent>(&current_data) {
            events.push(event);
        }
    }

    events
}

/// Parse and drain complete SSE events from a mutable buffer.
///
/// Extracts all complete `\n\n`-delimited events from `buf`, removes the consumed
/// prefix in place, and returns the parsed events. Incomplete trailing data is kept.
pub fn drain_sse_events(buf: &mut String) -> Vec<StreamEvent> {
    let mut events = Vec::new();
    let mut consumed = 0;
    let mut search_start = 0;

    while let Some(rel) = buf[search_start..].find("\n\n") {
        let event_end = search_start + rel;
        let event_text = &buf[consumed..event_end];
        let data: String = event_text
            .lines()
            .filter_map(|line| line.strip_prefix("data: "))
            .collect::<Vec<_>>()
            .join("");
        if !data.is_empty() {
            if let Ok(event) = serde_json::from_str::<StreamEvent>(&data) {
                events.push(event);
            }
        }
        consumed = event_end + 2;
        search_start = consumed;
    }

    if consumed > 0 {
        buf.drain(..consumed);
    }

    events
}
