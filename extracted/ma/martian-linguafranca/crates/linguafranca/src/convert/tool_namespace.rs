//! Stateless mapping between Open Responses namespaced tools and flat tool names.
//!
//! Chat Completions and Anthropic Messages have no tool namespaces, so a namespaced tool is exposed
//! as `{namespace}--{name}`. Response conversion splits the name at the first `--` to restore the
//! namespace. Clients such as Codex dispatch tool calls by `(namespace, name)`, so the round trip
//! must be exact. Namespaces must not contain the separator or end with `-`, which keeps the split
//! unambiguous.

use std::collections::HashSet;

use crate::convert::ctx::ConversionCtx;
use crate::error::{ConversionError, WarningAction};
use crate::open_responses::types::Tool;

pub(crate) const NAMESPACE_SEPARATOR: &str = "--";

/// Longest tool name accepted by Anthropic Messages.
const MAX_FLATTENED_NAME_LEN: usize = 128;

/// Joins a namespace and tool name into the flat name exposed to formats without namespaces.
pub(crate) fn flatten_tool_name(namespace: Option<&str>, name: String) -> String {
    match namespace {
        Some(namespace) if !namespace.is_empty() => {
            format!("{namespace}{NAMESPACE_SEPARATOR}{name}")
        }
        _ => name,
    }
}

/// Splits a flat tool name at the first separator; names without a separator stay plain.
pub(crate) fn split_tool_name(name: String) -> (Option<String>, String) {
    match name.split_once(NAMESPACE_SEPARATOR) {
        Some((namespace, tool)) if !namespace.is_empty() && !tool.is_empty() => {
            (Some(namespace.to_string()), tool.to_string())
        }
        _ => (None, name),
    }
}

/// Expands namespace tools into top-level function and custom tools with flattened names.
///
/// Each tool is paired with its source field path for warnings. Fails when a namespace cannot round-trip or a flattened name collides with another tool, since
/// the response could otherwise not identify the called tool.
pub(crate) fn flatten_namespace_tools<C>(
    tools: Vec<Tool>,
    ctx: &mut ConversionCtx<C>,
) -> Result<Vec<(String, Tool)>, ConversionError> {
    let mut flattened = Vec::with_capacity(tools.len());
    let mut plain_names = HashSet::new();
    let mut namespaced_names = HashSet::new();

    for (i, tool) in tools.into_iter().enumerate() {
        let Tool::Namespace {
            name: namespace,
            description,
            tools: members,
        } = tool
        else {
            if let Some(name) = tool_name(&tool) {
                if name.contains(NAMESPACE_SEPARATOR) {
                    ctx.warn(
                        &format!("tools[{i}].name"),
                        WarningAction::Changed,
                        format!(
                            "tool name contains namespace separator `{NAMESPACE_SEPARATOR}`; \
                             Open Responses calls to it are reported as namespaced"
                        ),
                    );
                }
                plain_names.insert(name.to_string());
            }
            flattened.push((format!("tools[{i}]"), tool));
            continue;
        };

        if !namespace_round_trips(&namespace) {
            return Err(ConversionError::InvalidInput(format!(
                "tools[{i}].name: namespace {namespace:?} must be non-empty, must not contain \
                 `{NAMESPACE_SEPARATOR}`, and must not end with `-`"
            )));
        }

        for (j, member) in members.into_iter().enumerate() {
            let field = format!("tools[{i}].tools[{j}]");
            let Some(member) = flatten_namespace_member(member, &namespace, description.as_deref())
            else {
                ctx.warn(
                    &field,
                    WarningAction::Dropped,
                    "only function and custom tools are supported in a namespace",
                );
                continue;
            };

            let name = tool_name(&member).expect("namespace members are named tools");
            if !namespaced_names.insert(name.to_string()) {
                return Err(ConversionError::InvalidInput(format!(
                    "{field}: duplicate namespaced tool name {name:?}"
                )));
            }
            if name.len() > MAX_FLATTENED_NAME_LEN {
                ctx.warn(
                    &format!("{field}.name"),
                    WarningAction::Changed,
                    format!(
                        "flattened tool name is longer than {MAX_FLATTENED_NAME_LEN} characters \
                         and may be rejected by the target"
                    ),
                );
            }
            flattened.push((field, member));
        }
    }

    if let Some(name) = namespaced_names.intersection(&plain_names).next() {
        return Err(ConversionError::InvalidInput(format!(
            "flattened namespaced tool name {name:?} collides with another tool"
        )));
    }

    Ok(flattened)
}

/// Rebuilds tool search references from flat names, grouping adjacent tools from one namespace.
///
/// Only adjacent references are merged so flattening the result restores the original order.
pub(crate) fn tool_references_from_flat_names(
    names: impl IntoIterator<Item = String>,
) -> Vec<Tool> {
    let mut tools: Vec<Tool> = Vec::new();
    for flat_name in names {
        let (namespace, name) = split_tool_name(flat_name);
        let function = Tool::Function {
            name,
            description: None,
            parameters: None,
            strict: None,
            defer_loading: None,
        };
        let Some(namespace) = namespace else {
            tools.push(function);
            continue;
        };

        let previous_group = match tools.last_mut() {
            Some(Tool::Namespace { name, tools, .. }) if *name == namespace => Some(tools),
            _ => None,
        };
        match previous_group {
            Some(members) => members.push(function),
            None => tools.push(Tool::Namespace {
                name: namespace,
                description: None,
                tools: vec![function],
            }),
        }
    }
    tools
}

/// Expands namespace tools without validation, for tool references such as tool search output.
pub(crate) fn flatten_namespace_tool_references(tools: Vec<Tool>) -> Vec<Tool> {
    tools
        .into_iter()
        .flat_map(|tool| match tool {
            Tool::Namespace {
                name: namespace,
                tools: members,
                ..
            } => members
                .into_iter()
                .filter_map(|member| flatten_namespace_member(member, &namespace, None))
                .collect(),
            other => vec![other],
        })
        .collect()
}

/// A trailing `-` would merge into the separator and move the first `--` split point.
fn namespace_round_trips(namespace: &str) -> bool {
    !namespace.is_empty() && !namespace.contains(NAMESPACE_SEPARATOR) && !namespace.ends_with('-')
}

fn flatten_namespace_member(
    member: Tool,
    namespace: &str,
    namespace_description: Option<&str>,
) -> Option<Tool> {
    match member {
        Tool::Function {
            name,
            description,
            parameters,
            strict,
            defer_loading,
        } => Some(Tool::Function {
            name: flatten_tool_name(Some(namespace), name),
            description: merge_descriptions(namespace_description, description),
            parameters,
            strict,
            defer_loading,
        }),
        Tool::Custom {
            name,
            description,
            format,
            defer_loading,
        } => Some(Tool::Custom {
            name: flatten_tool_name(Some(namespace), name),
            description: merge_descriptions(namespace_description, description),
            format,
            defer_loading,
        }),
        Tool::WebSearch { .. } | Tool::ToolSearch { .. } | Tool::Namespace { .. } => None,
    }
}

/// Keeps the namespace description, which the flat tool list cannot otherwise express.
fn merge_descriptions(namespace: Option<&str>, tool: Option<String>) -> Option<String> {
    match (namespace.map(str::trim).filter(|d| !d.is_empty()), tool) {
        (Some(namespace), Some(tool)) if !tool.trim().is_empty() => {
            Some(format!("{namespace}\n\n{tool}"))
        }
        (Some(namespace), _) => Some(namespace.to_string()),
        (None, tool) => tool,
    }
}

fn tool_name(tool: &Tool) -> Option<&str> {
    match tool {
        Tool::Function { name, .. } | Tool::Custom { name, .. } => Some(name),
        Tool::WebSearch { .. } | Tool::ToolSearch { .. } | Tool::Namespace { .. } => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn function(name: &str) -> Tool {
        Tool::Function {
            name: name.into(),
            description: Some("Run it.".into()),
            parameters: None,
            strict: None,
            defer_loading: None,
        }
    }

    fn namespace(name: &str, tools: Vec<Tool>) -> Tool {
        Tool::Namespace {
            name: name.into(),
            description: Some("Agent tools.".into()),
            tools,
        }
    }

    #[test]
    fn flat_names_round_trip() {
        for (namespace, name) in [
            (Some("multi_agent_v1"), "spawn_agent"),
            (Some("mcp__github__"), "create_issue"),
            (Some("mcp__codex_apps__gmail"), "_get_recent_emails"),
            (Some("ns"), "tool--with--separators"),
            (None, "plain_tool"),
        ] {
            let flat = flatten_tool_name(namespace, name.into());
            assert_eq!(
                split_tool_name(flat),
                (namespace.map(str::to_string), name.to_string())
            );
        }
    }

    #[test]
    fn names_without_both_sides_stay_plain() {
        for name in ["get-weather", "--leading", "trailing--", "--"] {
            assert_eq!(split_tool_name(name.into()), (None, name.to_string()));
        }
    }

    #[test]
    fn namespace_tools_are_flattened_with_namespace_description() {
        let mut ctx = ConversionCtx::<()>::new();
        let tools = flatten_namespace_tools(
            vec![
                function("exec_command"),
                namespace("multi_agent_v1", vec![function("spawn_agent")]),
            ],
            &mut ctx,
        )
        .unwrap();

        assert_eq!(
            tools,
            vec![
                ("tools[0]".to_string(), function("exec_command")),
                (
                    "tools[1].tools[0]".to_string(),
                    Tool::Function {
                        name: "multi_agent_v1--spawn_agent".into(),
                        description: Some("Agent tools.\n\nRun it.".into()),
                        parameters: None,
                        strict: None,
                        defer_loading: None,
                    }
                ),
            ]
        );
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn plain_tool_with_separator_warns() {
        let mut ctx = ConversionCtx::<()>::new();
        let tools = flatten_namespace_tools(vec![function("apify--web-fetch")], &mut ctx).unwrap();

        assert_eq!(
            tools,
            vec![("tools[0]".to_string(), function("apify--web-fetch"))]
        );
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tools[0].name");
    }

    #[test]
    fn unsupported_namespace_member_is_dropped() {
        let mut ctx = ConversionCtx::<()>::new();
        let web_search = Tool::WebSearch {
            search_context_size: None,
            user_location: None,
            filters: None,
        };
        let tools =
            flatten_namespace_tools(vec![namespace("ns", vec![web_search])], &mut ctx).unwrap();

        assert!(tools.is_empty());
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tools[0].tools[0]");
    }

    #[test]
    fn long_flattened_name_warns() {
        let mut ctx = ConversionCtx::<()>::new();
        let name = "t".repeat(MAX_FLATTENED_NAME_LEN);
        flatten_namespace_tools(vec![namespace("ns", vec![function(&name)])], &mut ctx).unwrap();

        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "tools[0].tools[0].name");
    }

    #[test]
    fn ambiguous_namespaces_and_collisions_are_rejected() {
        for tools in [
            vec![namespace("bad--ns", vec![function("tool")])],
            vec![namespace("trailing-", vec![function("tool")])],
            vec![namespace("", vec![function("tool")])],
            vec![
                function("ns--tool"),
                namespace("ns", vec![function("tool")]),
            ],
            vec![
                namespace("ns", vec![function("tool")]),
                namespace("ns", vec![function("tool")]),
            ],
        ] {
            let mut ctx = ConversionCtx::<()>::new();
            assert!(matches!(
                flatten_namespace_tools(tools, &mut ctx),
                Err(ConversionError::InvalidInput(_))
            ));
        }
    }

    #[test]
    fn tool_references_regroup_namespaced_names() {
        let reference = |name: &str| Tool::Function {
            name: name.into(),
            description: None,
            parameters: None,
            strict: None,
            defer_loading: None,
        };
        let names = ["ns--lookup", "ns--fetch", "plain", "ns--run"].map(String::from);
        let tools = tool_references_from_flat_names(names.clone());

        let namespace = |tools| Tool::Namespace {
            name: "ns".into(),
            description: None,
            tools,
        };
        assert_eq!(
            tools,
            vec![
                namespace(vec![reference("lookup"), reference("fetch")]),
                reference("plain"),
                namespace(vec![reference("run")]),
            ]
        );
        let flattened: Vec<_> = flatten_namespace_tool_references(tools)
            .into_iter()
            .filter_map(|tool| tool_name(&tool).map(str::to_string))
            .collect();
        assert_eq!(flattened, names);
    }
}
