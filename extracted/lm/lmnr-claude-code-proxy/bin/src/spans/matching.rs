//! Prompt and command matching utilities for detecting nested LLM calls

use crate::anthropic::request::{ContentBlock, Message, MessageContent, PostMessagesRequest};

/// Check if request messages contain a specific prompt (for nested call detection)
pub fn messages_contain_prompt(messages: &[Message], prompt: &str) -> bool {
    for message in messages {
        match &message.content {
            MessageContent::String(s) => {
                if s.contains(prompt) {
                    return true;
                }
            }
            MessageContent::Blocks(blocks) => {
                for block in blocks {
                    if let ContentBlock::Text { text, .. } = block {
                        if text.contains(prompt) {
                            return true;
                        }
                    }
                }
            }
        }
    }
    false
}

/// Check if request messages match a Bash command
/// Bash commands may be chained (cmd1 && cmd2 || cmd3), but the internal LLM only sees individual commands
/// So we need to check if any part of the command chain matches
pub fn messages_match_bash_command(messages: &[Message], full_command: &str) -> bool {
    // Split command by &&, ||, ;, and | to get individual commands
    // These are the common shell operators for chaining commands
    let command_parts: Vec<&str> = full_command
        .split("&&")
        .flat_map(|s| s.split("||"))
        .flat_map(|s| s.split(';'))
        .flat_map(|s| s.split('|'))
        .map(|s| s.trim())
        .filter(|s| !s.is_empty())
        .collect();

    for message in messages {
        let texts: Vec<&str> = match &message.content {
            MessageContent::String(s) => vec![s.as_str()],
            MessageContent::Blocks(blocks) => blocks
                .iter()
                .filter_map(|b| {
                    if let ContentBlock::Text { text, .. } = b {
                        Some(text.as_str())
                    } else {
                        None
                    }
                })
                .collect(),
        };

        for text in texts {
            // Check if any command part is in the message
            for part in &command_parts {
                if text.contains(part) {
                    return true;
                }
            }
            // Also check if full command is in message (original behavior)
            if text.contains(full_command) {
                return true;
            }
        }
    }
    false
}

/// Extract all tool_use_ids from tool_result blocks in the request
pub fn extract_tool_result_ids(request: &PostMessagesRequest) -> Vec<String> {
    let mut ids = Vec::new();
    for message in &request.messages {
        if let MessageContent::Blocks(blocks) = &message.content {
            for block in blocks {
                if let ContentBlock::ToolResult { tool_use_id, .. } = block {
                    ids.push(tool_use_id.clone());
                }
            }
        }
    }
    ids
}
