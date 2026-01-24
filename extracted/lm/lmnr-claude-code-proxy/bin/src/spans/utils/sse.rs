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
