use serde_json::Value;

/// Common span hierarchy information shared across different span types
#[derive(Debug, Clone)]
pub struct SpanHierarchy {
    pub trace_id_bytes: Vec<u8>,
    pub span_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
}

/// Context passed to span registration methods
#[derive(Debug, Clone)]
pub struct RegistrationContext {
    pub trace_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
    pub start_time_unix_nano: u64,
}

impl RegistrationContext {
    pub fn new(
        trace_id_bytes: Vec<u8>,
        parent_span_id_bytes: Vec<u8>,
        span_ids_path: Vec<String>,
        span_path: Vec<String>,
        start_time_unix_nano: u64,
    ) -> Self {
        Self {
            trace_id_bytes,
            parent_span_id_bytes,
            span_ids_path,
            span_path,
            start_time_unix_nano,
        }
    }
}

/// Types of tools that spawn nested LLM calls
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SpawningToolType {
    /// Task tool - spawns subagent with full conversation
    Task,
    /// WebSearch tool - calls LLM to perform web search
    WebSearch,
    /// Bash tool - calls LLM to analyze command prefix for safety
    Bash,
}

impl SpawningToolType {
    /// Get the field name that contains the prompt/query for matching
    pub fn prompt_field(&self) -> &'static str {
        match self {
            SpawningToolType::Task => "prompt",
            SpawningToolType::WebSearch => "query",
            SpawningToolType::Bash => "command",
        }
    }

    /// Check if a tool name is a spawning tool and return its type
    pub fn from_name(name: &str) -> Option<SpawningToolType> {
        match name {
            "Task" => Some(SpawningToolType::Task),
            "WebSearch" => Some(SpawningToolType::WebSearch),
            "Bash" => Some(SpawningToolType::Bash),
            _ => None,
        }
    }

    /// Check if a tool name is a spawning tool
    pub fn is_spawning_tool(name: &str) -> bool {
        Self::from_name(name).is_some()
    }
}

/// A pending spawning tool call waiting for nested LLM call to start
#[derive(Debug, Clone)]
pub struct PendingSpawningTool {
    pub tool_use_id: String,
    pub tool_type: SpawningToolType,
    pub prompt: String, // The prompt/query used to match nested calls
    pub hierarchy: SpanHierarchy,
    pub start_time_unix_nano: u64,
}

impl PendingSpawningTool {
    /// Create a NestedContext from this pending spawning tool
    pub fn to_nested_context(&self) -> NestedContext {
        NestedContext {
            parent_tool_use_id: self.tool_use_id.clone(),
            parent_tool_type: self.tool_type.clone(),
            prompt: self.prompt.clone(),
            hierarchy: SpanHierarchy {
                trace_id_bytes: self.hierarchy.trace_id_bytes.clone(),
                span_id_bytes: self.hierarchy.span_id_bytes.clone(),
                parent_span_id_bytes: self.hierarchy.parent_span_id_bytes.clone(),
                span_ids_path: self.hierarchy.span_ids_path.clone(),
                span_path: self.hierarchy.span_path.clone(),
            },
            start_time_unix_nano: self.start_time_unix_nano,
        }
    }
}

/// Context for active nested execution (subagent, websearch, etc.)
#[derive(Debug, Clone)]
pub struct NestedContext {
    pub parent_tool_use_id: String,
    pub parent_tool_type: SpawningToolType,
    pub prompt: String,
    pub hierarchy: SpanHierarchy,
    pub start_time_unix_nano: u64,
}

impl NestedContext {
    /// Get the parent tool span ID bytes (the spawning tool's span ID)
    pub fn parent_tool_span_id_bytes(&self) -> &Vec<u8> {
        &self.hierarchy.span_id_bytes
    }

    /// Convenience accessor for span_ids_path
    pub fn span_ids_path(&self) -> &Vec<String> {
        &self.hierarchy.span_ids_path
    }

    /// Convenience accessor for span_path
    pub fn span_path(&self) -> &Vec<String> {
        &self.hierarchy.span_path
    }

    /// Convenience accessor for trace_id_bytes
    pub fn trace_id_bytes(&self) -> &Vec<u8> {
        &self.hierarchy.trace_id_bytes
    }
}

/// A tool span waiting for its result
#[derive(Debug, Clone)]
pub struct PendingToolSpan {
    pub start_time_unix_nano: u64,
    pub trace_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
    pub tool_name: String,
    pub tool_input: Value,
    pub nested_prompt: Option<String>,
    pub preset_span_id_bytes: Option<Vec<u8>>,
}

/// Completed tool span ready to be sent
#[derive(Debug, Clone)]
pub struct CompletedToolSpan {
    pub start_time_unix_nano: u64,
    pub end_time_unix_nano: u64,
    pub trace_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
    pub tool_name: String,
    pub tool_input: Value,
    pub tool_output: Option<String>,
    pub is_error: bool,
}

/// Completed spawning tool span (Task, WebSearch, Bash finished)
#[derive(Debug, Clone)]
pub struct CompletedSpawningToolSpan {
    pub start_time_unix_nano: u64,
    pub end_time_unix_nano: u64,
    pub trace_id_bytes: Vec<u8>,
    pub parent_span_id_bytes: Vec<u8>,
    pub tool_span_id_bytes: Vec<u8>,
    pub span_ids_path: Vec<String>,
    pub span_path: Vec<String>,
    pub tool_name: String,
    pub tool_type: SpawningToolType,
    pub description: Option<String>,
    pub prompt: String,
    pub tool_output: Option<String>,
}

/// Helper to extract tool output from ToolResultContent
pub fn extract_tool_output(
    content: Option<&crate::anthropic::request::ToolResultContent>,
) -> Option<String> {
    use crate::anthropic::request::ToolResultContent;
    content.map(|c| match c {
        ToolResultContent::String(s) => s.clone(),
        ToolResultContent::Blocks(blocks) => serde_json::to_string(blocks).unwrap_or_default(),
    })
}
