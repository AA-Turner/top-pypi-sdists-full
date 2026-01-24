//! SpanProcessor - Core logic for tracking and completing spans across requests

use dashmap::DashMap;
use std::sync::Arc;

use crate::anthropic::request::{ContentBlock, MessageContent, PostMessagesRequest};
use crate::anthropic::response::{
    MessageResponse, ResponseContentBlock, WebSearchToolResultContent,
};

use super::matching::{
    extract_tool_result_ids, messages_contain_prompt, messages_match_bash_command,
};
use super::types::{
    CompletedSpawningToolSpan, CompletedToolSpan, NestedContext, PendingSpawningTool,
    PendingToolSpan, RegistrationContext, SpanHierarchy, SpawningToolType, extract_tool_output,
};
use super::utils::{bytes_to_uuid_like_string, generate_span_id};

/// Processes spans across requests with proper context management
#[derive(Debug, Clone)]
pub struct SpanProcessor {
    /// Pending spawning tool calls waiting for nested LLM call entry
    /// Key: prompt/query (for matching first nested request)
    pending_spawning_tools: Arc<DashMap<String, PendingSpawningTool>>,

    /// Maps tool_use_ids to their nested context
    /// This is how we track the chain after initial prompt match
    /// Key: tool_use_id from any tool call in a nested context
    tool_to_nested_context: Arc<DashMap<String, NestedContext>>,

    /// Pending tool spans waiting for results
    /// Key: tool_use_id
    pending_tool_spans: Arc<DashMap<String, PendingToolSpan>>,

    /// Tracks the latest child span end time for each spawning tool
    /// Key: parent_tool_use_id (from NestedContext)
    /// Value: latest child span end time in nanoseconds
    spawning_tool_child_end_times: Arc<DashMap<String, u64>>,
}

impl Default for SpanProcessor {
    fn default() -> Self {
        Self::new()
    }
}

impl SpanProcessor {
    pub fn new() -> Self {
        Self {
            pending_spawning_tools: Arc::new(DashMap::new()),
            tool_to_nested_context: Arc::new(DashMap::new()),
            pending_tool_spans: Arc::new(DashMap::new()),
            spawning_tool_child_end_times: Arc::new(DashMap::new()),
        }
    }

    /// Update the latest child span end time for a spawning tool
    /// Called when an LLM span completes within a nested context
    pub fn update_child_end_time(&self, parent_tool_use_id: &str, end_time_unix_nano: u64) {
        self.spawning_tool_child_end_times
            .entry(parent_tool_use_id.to_string())
            .and_modify(|t| {
                if end_time_unix_nano > *t {
                    *t = end_time_unix_nano;
                }
            })
            .or_insert(end_time_unix_nano);
    }

    /// Get and remove the latest child end time for a spawning tool
    fn take_child_end_time(&self, parent_tool_use_id: &str) -> Option<u64> {
        self.spawning_tool_child_end_times
            .remove(parent_tool_use_id)
            .map(|(_, t)| t)
    }

    /// Resolve effective parent context based on nested context
    fn resolve_effective_context(
        &self,
        ctx: &RegistrationContext,
        nested_context: Option<&NestedContext>,
    ) -> RegistrationContext {
        if let Some(nested) = nested_context {
            RegistrationContext::new(
                nested.hierarchy.trace_id_bytes.clone(),
                nested.hierarchy.span_id_bytes.clone(), // Parent is the spawning tool
                nested.hierarchy.span_ids_path.clone(),
                nested.hierarchy.span_path.clone(),
                ctx.start_time_unix_nano,
            )
        } else {
            ctx.clone()
        }
    }

    /// Try to find which nested context this request belongs to
    /// Returns Some(NestedContext) if this is a nested request (subagent, websearch, etc.)
    pub fn find_nested_context(&self, request: &PostMessagesRequest) -> Option<NestedContext> {
        // First, check if any tool_result in this request matches a known nested chain
        let tool_result_ids = extract_tool_result_ids(request);
        for id in &tool_result_ids {
            if let Some(ctx) = self.tool_to_nested_context.get(id) {
                return Some(ctx.clone());
            }
        }

        // Second, check if the messages contain a pending spawning tool's prompt (entry point)
        // We don't remove the entry here - cleanup happens when ToolResult arrives
        for entry in self.pending_spawning_tools.iter() {
            let prompt = entry.key();
            let pending_tool = entry.value();

            // Use different matching strategy based on tool type
            let is_match = match pending_tool.tool_type {
                SpawningToolType::Bash => messages_match_bash_command(&request.messages, prompt),
                _ => messages_contain_prompt(&request.messages, prompt),
            };

            if is_match {
                return Some(pending_tool.to_nested_context());
            }
        }

        None
    }

    /// Register spawning tool calls from a response (Task, WebSearch, etc.)
    pub fn register_spawning_tool_calls(
        &self,
        response: &MessageResponse,
        nested_context: Option<&NestedContext>,
        ctx: &RegistrationContext,
    ) {
        let effective_ctx = self.resolve_effective_context(ctx, nested_context);

        for block in &response.content {
            if let ResponseContentBlock::ToolUse { id, name, input } = block {
                let tool_type = match SpawningToolType::from_name(name) {
                    Some(t) => t,
                    None => continue,
                };

                let prompt_field = tool_type.prompt_field();
                let prompt = input
                    .get(prompt_field)
                    .and_then(|v| v.as_str())
                    .unwrap_or("")
                    .to_string();

                if prompt.is_empty() {
                    continue;
                }

                let tool_span_id_bytes = match generate_span_id() {
                    Ok(id) => id,
                    Err(_) => continue,
                };

                let tool_span_id_string = match bytes_to_uuid_like_string(&tool_span_id_bytes) {
                    Ok(s) => s,
                    Err(_) => continue,
                };

                // Build the tool's own paths
                let mut tool_span_ids_path = effective_ctx.span_ids_path.clone();
                tool_span_ids_path.push(tool_span_id_string);

                let mut tool_span_path = effective_ctx.span_path.clone();
                tool_span_path.push(name.clone());

                let hierarchy = SpanHierarchy {
                    trace_id_bytes: effective_ctx.trace_id_bytes.clone(),
                    span_id_bytes: tool_span_id_bytes,
                    parent_span_id_bytes: effective_ctx.parent_span_id_bytes.clone(),
                    span_ids_path: tool_span_ids_path,
                    span_path: tool_span_path,
                };

                let pending_tool = PendingSpawningTool {
                    tool_use_id: id.clone(),
                    tool_type,
                    prompt: prompt.clone(),
                    hierarchy,
                    start_time_unix_nano: effective_ctx.start_time_unix_nano,
                };

                self.pending_spawning_tools
                    .insert(prompt.clone(), pending_tool);

                // Also add to tool_to_nested_context for chain tracking
                if let Some(nested) = nested_context {
                    self.tool_to_nested_context
                        .insert(id.clone(), nested.clone());
                }
            }
        }
    }

    /// Register spawning tools as pending tool spans for timing purposes
    pub fn register_spawning_tools_as_pending(
        &self,
        response: &MessageResponse,
        ctx: &RegistrationContext,
    ) {
        for block in &response.content {
            if let ResponseContentBlock::ToolUse { id, name, input } = block {
                if !SpawningToolType::is_spawning_tool(name) {
                    continue;
                }

                let tool_type = SpawningToolType::from_name(name).unwrap();
                let prompt_field = tool_type.prompt_field();
                let prompt = input
                    .get(prompt_field)
                    .and_then(|v| v.as_str())
                    .unwrap_or("")
                    .to_string();

                // Look up the PendingSpawningTool to get the pre-generated span ID and proper paths
                let (preset_span_id, tool_ctx) =
                    if let Some(pending) = self.pending_spawning_tools.get(&prompt) {
                        (
                            Some(pending.hierarchy.span_id_bytes.clone()),
                            RegistrationContext::new(
                                pending.hierarchy.trace_id_bytes.clone(),
                                pending.hierarchy.parent_span_id_bytes.clone(),
                                pending.hierarchy.span_ids_path.clone(),
                                pending.hierarchy.span_path.clone(),
                                pending.start_time_unix_nano,
                            ),
                        )
                    } else {
                        (None, ctx.clone())
                    };

                let pending_tool = PendingToolSpan {
                    start_time_unix_nano: tool_ctx.start_time_unix_nano,
                    trace_id_bytes: tool_ctx.trace_id_bytes,
                    parent_span_id_bytes: tool_ctx.parent_span_id_bytes,
                    span_ids_path: tool_ctx.span_ids_path,
                    span_path: tool_ctx.span_path,
                    tool_name: name.clone(),
                    tool_input: input.clone(),
                    nested_prompt: None,
                    preset_span_id_bytes: preset_span_id,
                };

                self.pending_tool_spans.insert(id.clone(), pending_tool);
            }
        }
    }

    /// Register regular tool calls from a response
    pub fn register_tool_calls(
        &self,
        response: &MessageResponse,
        nested_context: Option<&NestedContext>,
        ctx: &RegistrationContext,
    ) {
        let effective_ctx = self.resolve_effective_context(ctx, nested_context);

        for block in &response.content {
            let (id, name, input) = match block {
                ResponseContentBlock::ToolUse { id, name, input } => (id, name, input),
                ResponseContentBlock::ServerToolUse {
                    id, name, input, ..
                } => (id, name, input),
                _ => continue,
            };

            if SpawningToolType::is_spawning_tool(name) {
                continue;
            }

            let pending_tool = PendingToolSpan {
                start_time_unix_nano: effective_ctx.start_time_unix_nano,
                trace_id_bytes: effective_ctx.trace_id_bytes.clone(),
                parent_span_id_bytes: effective_ctx.parent_span_id_bytes.clone(),
                span_ids_path: effective_ctx.span_ids_path.clone(),
                span_path: effective_ctx.span_path.clone(),
                tool_name: name.clone(),
                tool_input: input.clone(),
                nested_prompt: nested_context.map(|ctx| ctx.prompt.clone()),
                preset_span_id_bytes: None,
            };

            self.pending_tool_spans.insert(id.clone(), pending_tool);

            if let Some(nested) = nested_context {
                self.tool_to_nested_context
                    .insert(id.clone(), nested.clone());
            }
        }
    }

    /// Extract completed server tool spans from a response
    pub fn extract_server_tool_spans(
        &self,
        response: &MessageResponse,
        nested_context: Option<&NestedContext>,
        ctx: &RegistrationContext,
    ) -> Vec<CompletedToolSpan> {
        use std::collections::HashMap;

        let effective_ctx = self.resolve_effective_context(ctx, nested_context);
        let mut completed = Vec::new();

        // First, collect all server tool uses by their ID
        let mut server_tool_uses: HashMap<String, (String, serde_json::Value)> = HashMap::new();
        for block in &response.content {
            if let ResponseContentBlock::ServerToolUse {
                id, name, input, ..
            } = block
            {
                server_tool_uses.insert(id.clone(), (name.clone(), input.clone()));
            }
        }

        // Then, find matching tool results and create completed spans
        for block in &response.content {
            let (tool_use_id, tool_output) = match block {
                ResponseContentBlock::WebSearchToolResult {
                    tool_use_id,
                    content,
                    ..
                } => {
                    let output = match content {
                        WebSearchToolResultContent::Results(results) => {
                            serde_json::to_string(results).unwrap_or_default()
                        }
                        WebSearchToolResultContent::Error { error_code, .. } => {
                            format!("Error: {}", error_code)
                        }
                    };
                    (tool_use_id, Some(output))
                }
                ResponseContentBlock::WebFetchToolResult {
                    tool_use_id,
                    content,
                    ..
                } => (tool_use_id, Some(content.to_string())),
                ResponseContentBlock::CodeExecutionToolResult {
                    tool_use_id,
                    content,
                    ..
                } => (tool_use_id, Some(content.to_string())),
                _ => continue,
            };

            if let Some((tool_name, tool_input)) = server_tool_uses.get(tool_use_id) {
                let span_id_bytes = generate_span_id().unwrap_or_default();

                completed.push(CompletedToolSpan {
                    start_time_unix_nano: effective_ctx.start_time_unix_nano,
                    end_time_unix_nano: effective_ctx.start_time_unix_nano,
                    trace_id_bytes: effective_ctx.trace_id_bytes.clone(),
                    parent_span_id_bytes: effective_ctx.parent_span_id_bytes.clone(),
                    span_id_bytes,
                    span_ids_path: effective_ctx.span_ids_path.clone(),
                    span_path: effective_ctx.span_path.clone(),
                    tool_name: tool_name.clone(),
                    tool_input: tool_input.clone(),
                    tool_output,
                    is_error: false,
                });
            }
        }

        completed
    }

    /// Complete tool spans when we receive tool_results
    pub fn complete_tool_spans(
        &self,
        request: &PostMessagesRequest,
        end_time_unix_nano: u64,
    ) -> Vec<CompletedToolSpan> {
        let mut completed = Vec::new();

        for message in &request.messages {
            if let MessageContent::Blocks(blocks) = &message.content {
                for block in blocks {
                    if let ContentBlock::ToolResult {
                        tool_use_id,
                        content,
                        is_error,
                        ..
                    } = block
                    {
                        if let Some((_, pending)) = self.pending_tool_spans.remove(tool_use_id) {
                            // Skip spawning tools - handled by complete_spawning_tool_spans
                            if SpawningToolType::is_spawning_tool(&pending.tool_name) {
                                self.pending_tool_spans.insert(tool_use_id.clone(), pending);
                                continue;
                            }

                            let span_id_bytes = pending
                                .preset_span_id_bytes
                                .clone()
                                .unwrap_or_else(|| generate_span_id().unwrap_or_default());

                            // Build span_ids_path and span_path
                            let mut span_ids_path = pending.span_ids_path.clone();
                            if let Ok(span_id_str) = bytes_to_uuid_like_string(&span_id_bytes) {
                                span_ids_path.push(span_id_str);
                            }

                            let mut span_path = pending.span_path.clone();
                            span_path.push(pending.tool_name.clone());

                            let tool_output = extract_tool_output(content.as_ref());

                            // Update parent spawning tool's child end time if in nested context
                            if let Some(nested_prompt) = &pending.nested_prompt {
                                if let Some(ctx) = self.tool_to_nested_context.get(tool_use_id) {
                                    self.update_child_end_time(
                                        &ctx.parent_tool_use_id,
                                        end_time_unix_nano,
                                    );
                                } else {
                                    for entry in self.tool_to_nested_context.iter() {
                                        if &entry.prompt == nested_prompt {
                                            self.update_child_end_time(
                                                &entry.parent_tool_use_id,
                                                end_time_unix_nano,
                                            );
                                            break;
                                        }
                                    }
                                }
                            }

                            completed.push(CompletedToolSpan {
                                start_time_unix_nano: pending.start_time_unix_nano,
                                end_time_unix_nano,
                                trace_id_bytes: pending.trace_id_bytes,
                                parent_span_id_bytes: pending.parent_span_id_bytes,
                                span_id_bytes,
                                span_ids_path,
                                span_path,
                                tool_name: pending.tool_name,
                                tool_input: pending.tool_input,
                                tool_output,
                                is_error: is_error.unwrap_or(false),
                            });
                        }
                    }
                }
            }
        }

        completed
    }

    /// Complete spawning tool spans when we receive their tool_results
    pub fn complete_spawning_tool_spans(
        &self,
        request: &PostMessagesRequest,
        end_time_unix_nano: u64,
    ) -> Vec<CompletedSpawningToolSpan> {
        let mut completed = Vec::new();

        for message in &request.messages {
            if let MessageContent::Blocks(blocks) = &message.content {
                for block in blocks {
                    if let ContentBlock::ToolResult {
                        tool_use_id,
                        content,
                        ..
                    } = block
                    {
                        if let Some((_, pending)) = self.pending_tool_spans.remove(tool_use_id) {
                            let tool_type = match SpawningToolType::from_name(&pending.tool_name) {
                                Some(t) => t,
                                None => {
                                    self.pending_tool_spans.insert(tool_use_id.clone(), pending);
                                    continue;
                                }
                            };

                            let tool_span_id_bytes = pending
                                .preset_span_id_bytes
                                .clone()
                                .unwrap_or_else(|| generate_span_id().unwrap_or_default());

                            let tool_output = extract_tool_output(content.as_ref());

                            let description = pending
                                .tool_input
                                .get("description")
                                .and_then(|v| v.as_str())
                                .map(|s| s.to_string());

                            let prompt_field = tool_type.prompt_field();
                            let prompt = pending
                                .tool_input
                                .get(prompt_field)
                                .and_then(|v| v.as_str())
                                .unwrap_or("")
                                .to_string();

                            // Use the latest child span end time if available
                            let actual_end_time = self
                                .take_child_end_time(tool_use_id)
                                .unwrap_or(end_time_unix_nano);

                            completed.push(CompletedSpawningToolSpan {
                                start_time_unix_nano: pending.start_time_unix_nano,
                                end_time_unix_nano: actual_end_time,
                                trace_id_bytes: pending.trace_id_bytes,
                                parent_span_id_bytes: pending.parent_span_id_bytes,
                                tool_span_id_bytes,
                                span_ids_path: pending.span_ids_path,
                                span_path: pending.span_path,
                                tool_name: pending.tool_name,
                                tool_type: tool_type.clone(),
                                description,
                                prompt: prompt.clone(),
                                tool_output,
                            });

                            // Clean up nested context entries and pending spawning tools
                            self.tool_to_nested_context
                                .retain(|_, ctx| ctx.prompt != prompt);
                            self.pending_spawning_tools.remove(&prompt);
                        }
                    }
                }
            }
        }

        completed
    }
}
