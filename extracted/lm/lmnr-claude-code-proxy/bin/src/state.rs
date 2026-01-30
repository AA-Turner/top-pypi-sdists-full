use dashmap::DashMap;
use serde::Deserialize;
use std::sync::{Arc, Mutex};

#[derive(Debug, Clone, Deserialize)]
pub struct CurrentTraceAndLaminarContext {
    pub trace_id: String,
    pub span_id: String,
    pub project_api_key: String,
    #[serde(default)]
    pub span_ids_path: Vec<String>, // Vec<UUID>
    #[serde(default)]
    pub span_path: Vec<String>,
    #[serde(default = "default_laminar_url")]
    pub laminar_url: String,
}

fn default_laminar_url() -> String {
    std::env::var("LMNR_BASE_URL").unwrap_or("https://api.lmnr.ai".to_string())
}

#[derive(Debug, Clone)]
pub struct State {
    pub trace_context: Option<CurrentTraceAndLaminarContext>,
    // Cache of inferred schemes: key is base URL (without scheme), value is "http" or "https"
    pub inferred_schemes: DashMap<String, String>,
}

impl State {
    pub fn new() -> Self {
        Self {
            trace_context: None,
            inferred_schemes: DashMap::new(),
        }
    }
}

pub type SharedState = Arc<Mutex<State>>;

pub fn new_state() -> SharedState {
    Arc::new(Mutex::new(State::new()))
}
