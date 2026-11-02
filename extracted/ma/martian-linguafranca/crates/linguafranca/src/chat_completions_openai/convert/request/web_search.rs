use crate::convert::ctx::ConversionCtx;
use crate::error::WarningAction;
use crate::open_responses::types::{SearchContextSize, Tool, UserLocation, WebSearchFilters};

pub(super) type Ctx = ConversionCtx<()>;

pub(super) struct WebSearchToolFields {
    pub search_context_size: Option<serde_json::Value>,
    pub user_location: Option<serde_json::Value>,
    pub filters: Option<serde_json::Value>,
    pub domains: Option<serde_json::Value>,
    pub search_content_types: Option<serde_json::Value>,
    pub extra: serde_json::Map<String, serde_json::Value>,
}

pub(super) fn convert_tool(fields: WebSearchToolFields, ctx: &mut Ctx) -> Tool {
    let WebSearchToolFields {
        search_context_size,
        user_location,
        filters,
        domains,
        search_content_types,
        extra,
    } = fields;

    if search_content_types.is_some() {
        ctx.warn(
            "search_content_types",
            WarningAction::Dropped,
            "not supported in Open Responses web_search tools",
        );
    }
    warn_extra_web_search_fields("web_search", &extra, ctx);

    let filters = match (filters, domains) {
        (Some(filters), Some(domains)) => {
            let filters = parse_web_search_filters(filters, "filters", ctx);
            if filters.is_some() {
                ctx.warn(
                    "domains",
                    WarningAction::Dropped,
                    "ignored because filters.allowed_domains was also provided",
                );
                filters
            } else {
                parse_web_search_domains(domains, "domains", ctx)
            }
        }
        (Some(filters), None) => parse_web_search_filters(filters, "filters", ctx),
        (None, Some(domains)) => parse_web_search_domains(domains, "domains", ctx),
        (None, None) => None,
    };

    Tool::WebSearch {
        search_context_size: search_context_size
            .and_then(|value| parse_search_context_size(value, "search_context_size", ctx)),
        user_location: user_location
            .and_then(|value| parse_user_location(value, "user_location", ctx)),
        filters,
    }
}

pub(super) fn convert_options(options: serde_json::Value, ctx: &mut Ctx) -> Tool {
    let Some(object) = options.as_object() else {
        ctx.warn(
            "web_search_options",
            WarningAction::Dropped,
            "expected object; emitted default web_search tool",
        );
        return Tool::WebSearch {
            search_context_size: None,
            user_location: None,
            filters: None,
        };
    };

    ctx.push("web_search_options");

    let search_context_size = object
        .get("search_context_size")
        .filter(|value| !value.is_null())
        .cloned()
        .and_then(|value| parse_search_context_size(value, "search_context_size", ctx));

    let user_location = object
        .get("user_location")
        .filter(|value| !value.is_null())
        .cloned()
        .and_then(|value| parse_chat_web_search_options_user_location(value, ctx));

    for key in object.keys() {
        if key != "search_context_size" && key != "user_location" {
            ctx.warn(
                key,
                WarningAction::Dropped,
                "unsupported web_search_options field",
            );
        }
    }

    ctx.pop();

    Tool::WebSearch {
        search_context_size,
        user_location,
        filters: None,
    }
}

fn parse_chat_web_search_options_user_location(
    value: serde_json::Value,
    ctx: &mut Ctx,
) -> Option<UserLocation> {
    let Some(object) = value.as_object() else {
        ctx.warn("user_location", WarningAction::Dropped, "expected object");
        return None;
    };

    let kind = object
        .get("type")
        .and_then(|value| value.as_str())
        .unwrap_or("approximate");
    if kind != "approximate" {
        ctx.warn(
            "user_location.type",
            WarningAction::Changed,
            "expected approximate; normalized to approximate",
        );
    }

    object
        .get("approximate")
        .filter(|value| !value.is_null())
        .cloned()
        .and_then(|value| parse_user_location(value, "user_location.approximate", ctx))
}

fn parse_search_context_size(
    value: serde_json::Value,
    field: &str,
    ctx: &mut Ctx,
) -> Option<SearchContextSize> {
    match serde_json::from_value(value.clone()) {
        Ok(size) => Some(size),
        Err(_) => {
            ctx.warn(
                field,
                WarningAction::Dropped,
                format!("invalid search_context_size value: {value}"),
            );
            None
        }
    }
}

fn parse_user_location(
    value: serde_json::Value,
    field: &str,
    ctx: &mut Ctx,
) -> Option<UserLocation> {
    let Some(object) = value.as_object() else {
        ctx.warn(field, WarningAction::Dropped, "expected object");
        return None;
    };

    let string_field = |name: &str, ctx: &mut Ctx| -> Option<String> {
        match object.get(name) {
            Some(value) if value.is_null() => None,
            Some(value) => value.as_str().map(String::from).or_else(|| {
                ctx.warn(
                    &format!("{field}.{name}"),
                    WarningAction::Dropped,
                    "expected string",
                );
                None
            }),
            None => None,
        }
    };

    let kind = match object.get("type") {
        Some(serde_json::Value::String(kind)) if kind == "approximate" => "approximate",
        Some(serde_json::Value::String(_)) => {
            ctx.warn(
                &format!("{field}.type"),
                WarningAction::Dropped,
                "expected approximate; normalized to approximate",
            );
            "approximate"
        }
        Some(value) if !value.is_null() => {
            ctx.warn(
                &format!("{field}.type"),
                WarningAction::Dropped,
                "expected string",
            );
            "approximate"
        }
        _ => "approximate",
    };

    Some(UserLocation {
        kind: kind.to_string(),
        city: string_field("city", ctx),
        country: string_field("country", ctx),
        region: string_field("region", ctx),
        timezone: string_field("timezone", ctx),
    })
}

fn parse_web_search_filters(
    value: serde_json::Value,
    field: &str,
    ctx: &mut Ctx,
) -> Option<WebSearchFilters> {
    let Some(object) = value.as_object() else {
        if !value.is_null() {
            ctx.warn(field, WarningAction::Dropped, "expected object");
        }
        return None;
    };

    let allowed_domains = object
        .get("allowed_domains")
        .filter(|value| !value.is_null())
        .cloned()
        .and_then(|value| parse_allowed_domains(value, &format!("{field}.allowed_domains"), ctx))
        .unwrap_or_default();

    for key in object.keys() {
        if key != "allowed_domains" {
            ctx.warn(
                &format!("{field}.{key}"),
                WarningAction::Dropped,
                "unsupported web_search filter field",
            );
        }
    }

    if allowed_domains.is_empty() {
        None
    } else {
        Some(WebSearchFilters { allowed_domains })
    }
}

fn parse_web_search_domains(
    value: serde_json::Value,
    field: &str,
    ctx: &mut Ctx,
) -> Option<WebSearchFilters> {
    parse_allowed_domains(value, field, ctx).and_then(|allowed_domains| {
        if allowed_domains.is_empty() {
            None
        } else {
            Some(WebSearchFilters { allowed_domains })
        }
    })
}

fn parse_allowed_domains(
    value: serde_json::Value,
    field: &str,
    ctx: &mut Ctx,
) -> Option<Vec<String>> {
    let Some(items) = value.as_array() else {
        ctx.warn(field, WarningAction::Dropped, "expected array of strings");
        return None;
    };

    let mut out = Vec::new();
    for (i, item) in items.iter().enumerate() {
        if let Some(domain) = item.as_str() {
            out.push(domain.to_string());
        } else {
            ctx.warn(
                &format!("{field}[{i}]"),
                WarningAction::Dropped,
                "expected string",
            );
        }
    }
    Some(out)
}

fn warn_extra_web_search_fields(
    parent: &str,
    extra: &serde_json::Map<String, serde_json::Value>,
    ctx: &mut Ctx,
) {
    for key in extra.keys() {
        ctx.warn(
            key,
            WarningAction::Dropped,
            format!("unsupported {parent} field"),
        );
    }
}
