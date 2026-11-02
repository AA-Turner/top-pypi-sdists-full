use std::collections::{BTreeMap, BTreeSet};
use std::env;
use std::fs;
use std::path::Path;

use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::anthropic::response::AnthropicResponse;
use linguafranca::anthropic::stream::AnthropicStreamEvent;
use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use linguafranca::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
use linguafranca::chat_completions_openai::stream::ChatCompletionsStreamChunk;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::open_responses::stream::OpenResponsesStreamEvent;
use schemars::Schema;
use schemars::generate::SchemaSettings;
use serde_json::{Map, Value, json};

type DynError = Box<dyn std::error::Error>;
type DocumentMap = BTreeMap<String, Value>;

#[derive(Clone, Copy)]
struct RootSpec {
    file_name: &'static str,
    title: &'static str,
}

#[derive(Clone, Copy)]
struct FamilySpec {
    name: &'static str,
    shared_file_name: &'static str,
    shared_title: &'static str,
    roots: &'static [RootSpec],
}

const OPEN_RESPONSES_ROOTS: &[RootSpec] = &[
    RootSpec {
        file_name: "open_responses_request.json",
        title: "OpenResponsesRequest",
    },
    RootSpec {
        file_name: "open_responses_response.json",
        title: "OpenResponsesResponse",
    },
    RootSpec {
        file_name: "open_responses_stream_event.json",
        title: "OpenResponsesStreamEvent",
    },
];

const CHAT_COMPLETIONS_ROOTS: &[RootSpec] = &[
    RootSpec {
        file_name: "chat_completions_request.json",
        title: "ChatCompletionsOpenAiRequest",
    },
    RootSpec {
        file_name: "chat_completions_response.json",
        title: "ChatCompletionsOpenAiResponse",
    },
    RootSpec {
        file_name: "chat_completions_stream_chunk.json",
        title: "ChatCompletionsStreamChunk",
    },
];

const ANTHROPIC_ROOTS: &[RootSpec] = &[
    RootSpec {
        file_name: "anthropic_request.json",
        title: "AnthropicRequest",
    },
    RootSpec {
        file_name: "anthropic_response.json",
        title: "AnthropicResponse",
    },
    RootSpec {
        file_name: "anthropic_stream_event.json",
        title: "AnthropicStreamEvent",
    },
];

const FAMILIES: &[FamilySpec] = &[
    FamilySpec {
        name: "open_responses",
        shared_file_name: "open_responses_shared.json",
        shared_title: "OpenResponsesShared",
        roots: OPEN_RESPONSES_ROOTS,
    },
    FamilySpec {
        name: "chat_completions",
        shared_file_name: "chat_completions_shared.json",
        shared_title: "ChatCompletionsShared",
        roots: CHAT_COMPLETIONS_ROOTS,
    },
    FamilySpec {
        name: "anthropic",
        shared_file_name: "anthropic_shared.json",
        shared_title: "AnthropicShared",
        roots: ANTHROPIC_ROOTS,
    },
];

fn root_schema_value<T>() -> Result<Value, DynError>
where
    T: schemars::JsonSchema,
{
    let schema: Schema = SchemaSettings::draft2020_12()
        .into_generator()
        .into_root_schema_for::<T>();
    Ok(serde_json::to_value(schema)?)
}

fn generate_raw_roots() -> Result<DocumentMap, DynError> {
    let mut documents = BTreeMap::new();
    documents.insert(
        "open_responses_request.json".to_owned(),
        root_schema_value::<OpenResponsesRequest>()?,
    );
    documents.insert(
        "open_responses_response.json".to_owned(),
        root_schema_value::<OpenResponsesResponse>()?,
    );
    documents.insert(
        "open_responses_stream_event.json".to_owned(),
        root_schema_value::<OpenResponsesStreamEvent>()?,
    );
    documents.insert(
        "chat_completions_request.json".to_owned(),
        root_schema_value::<ChatCompletionsOpenAiRequest>()?,
    );
    documents.insert(
        "chat_completions_response.json".to_owned(),
        root_schema_value::<ChatCompletionsOpenAiResponse>()?,
    );
    documents.insert(
        "chat_completions_stream_chunk.json".to_owned(),
        root_schema_value::<ChatCompletionsStreamChunk>()?,
    );
    documents.insert(
        "anthropic_request.json".to_owned(),
        root_schema_value::<AnthropicRequest>()?,
    );
    documents.insert(
        "anthropic_response.json".to_owned(),
        root_schema_value::<AnthropicResponse>()?,
    );
    documents.insert(
        "anthropic_stream_event.json".to_owned(),
        root_schema_value::<AnthropicStreamEvent>()?,
    );
    Ok(documents)
}

fn get_object_mut(value: &mut Value) -> Result<&mut Map<String, Value>, DynError> {
    value
        .as_object_mut()
        .ok_or_else(|| "schema root is not an object".into())
}

fn get_defs_map(value: &Value) -> Option<&Map<String, Value>> {
    value.get("$defs").and_then(Value::as_object)
}

fn get_defs_map_mut(value: &mut Value) -> Option<&mut Map<String, Value>> {
    value.get_mut("$defs").and_then(Value::as_object_mut)
}

fn require_defs_map_mut(value: &mut Value) -> Result<&mut Map<String, Value>, DynError> {
    get_object_mut(value)?
        .entry("$defs".to_owned())
        .or_insert_with(|| Value::Object(Map::new()))
        .as_object_mut()
        .ok_or_else(|| "$defs is not an object".into())
}

fn remove_empty_defs(value: &mut Value) {
    if get_defs_map(value).is_some_and(Map::is_empty)
        && let Some(obj) = value.as_object_mut()
    {
        obj.remove("$defs");
    }
}

fn canonical_string(value: &Value) -> String {
    match value {
        Value::Null => "null".to_owned(),
        Value::Bool(v) => v.to_string(),
        Value::Number(v) => v.to_string(),
        Value::String(v) => format!("{v:?}"),
        Value::Array(items) => {
            let parts: Vec<String> = items.iter().map(canonical_string).collect();
            format!("[{}]", parts.join(","))
        }
        Value::Object(map) => {
            let mut entries: Vec<(&str, &Value)> = map
                .iter()
                .filter(|(key, _)| {
                    !matches!(
                        key.as_str(),
                        "$schema" | "title" | "description" | "examples" | "default"
                    )
                })
                .map(|(key, value)| (key.as_str(), value))
                .collect();
            entries.sort_by(|a, b| a.0.cmp(b.0));

            let parts: Vec<String> = entries
                .into_iter()
                .map(|(key, value)| format!("{key:?}:{}", canonical_string(value)))
                .collect();
            format!("{{{}}}", parts.join(","))
        }
    }
}

fn root_body_digest(value: &Value) -> Result<String, DynError> {
    let mut body = value.clone();
    let obj = body
        .as_object_mut()
        .ok_or_else(|| "schema root is not an object".to_owned())?;
    obj.remove("$defs");
    Ok(canonical_string(&body))
}

fn local_def_target(ref_value: &str) -> Option<&str> {
    ref_value.strip_prefix("#/$defs/")
}

fn collect_local_refs(value: &Value, refs: &mut BTreeSet<String>) {
    match value {
        Value::Object(map) => {
            if let Some(Value::String(target)) = map.get("$ref")
                && let Some(name) = local_def_target(target)
            {
                refs.insert(name.to_owned());
            }
            for child in map.values() {
                collect_local_refs(child, refs);
            }
        }
        Value::Array(items) => {
            for item in items {
                collect_local_refs(item, refs);
            }
        }
        Value::Null | Value::Bool(_) | Value::Number(_) | Value::String(_) => {}
    }
}

fn rewrite_refs(value: &mut Value, resolver: &impl Fn(&str) -> Option<String>) {
    match value {
        Value::Object(map) => {
            if let Some(Value::String(target)) = map.get_mut("$ref")
                && let Some(name) = local_def_target(target).map(str::to_owned)
                && let Some(rewritten) = resolver(&name)
            {
                *target = rewritten;
            }
            for child in map.values_mut() {
                rewrite_refs(child, resolver);
            }
        }
        Value::Array(items) => {
            for item in items {
                rewrite_refs(item, resolver);
            }
        }
        Value::Null | Value::Bool(_) | Value::Number(_) | Value::String(_) => {}
    }
}

fn collect_repeated_defs(
    documents: &DocumentMap,
    family: &FamilySpec,
) -> Result<BTreeSet<String>, DynError> {
    let mut owners: BTreeMap<String, Vec<(String, String)>> = BTreeMap::new();

    for root in family.roots {
        let document = documents
            .get(root.file_name)
            .ok_or_else(|| format!("missing schema {}", root.file_name))?;
        if let Some(defs) = get_defs_map(document) {
            for (name, schema) in defs {
                owners
                    .entry(name.clone())
                    .or_default()
                    .push((root.file_name.to_owned(), canonical_string(schema)));
            }
        }
    }

    let mut repeated = BTreeSet::new();
    for (name, candidates) in owners {
        if candidates.len() < 2 {
            continue;
        }
        let first = &candidates[0].1;
        if candidates.iter().all(|(_, digest)| digest == first) {
            repeated.insert(name);
        } else {
            let files: Vec<String> = candidates.into_iter().map(|(file, _)| file).collect();
            return Err(format!(
                "family {} has conflicting repeated $defs/{name} across {}",
                family.name,
                files.join(", ")
            )
            .into());
        }
    }

    Ok(repeated)
}

fn collect_shared_closure(
    documents: &DocumentMap,
    family: &FamilySpec,
    root_titles: &BTreeMap<String, String>,
    initial: BTreeSet<String>,
) -> Result<BTreeSet<String>, DynError> {
    let mut shared = initial;

    loop {
        let mut changed = false;
        let current: Vec<String> = shared.iter().cloned().collect();

        for root in family.roots {
            let Some(defs) = documents.get(root.file_name).and_then(get_defs_map) else {
                continue;
            };

            for shared_name in &current {
                let Some(schema) = defs.get(shared_name) else {
                    continue;
                };

                let mut refs = BTreeSet::new();
                collect_local_refs(schema, &mut refs);

                for target in refs {
                    if root_titles.contains_key(&target) || shared.contains(&target) {
                        continue;
                    }
                    if defs.contains_key(&target) {
                        changed |= shared.insert(target);
                    }
                }
            }
        }

        if !changed {
            break;
        }
    }

    Ok(shared)
}

fn build_shared_defs(
    documents: &DocumentMap,
    family: &FamilySpec,
    shared_defs: &BTreeSet<String>,
) -> Result<BTreeMap<String, Value>, DynError> {
    let mut output = BTreeMap::new();

    for name in shared_defs {
        let mut canonical: Option<(String, Value, String)> = None;

        for root in family.roots {
            let Some(defs) = documents.get(root.file_name).and_then(get_defs_map) else {
                continue;
            };
            let Some(schema) = defs.get(name) else {
                continue;
            };

            let digest = canonical_string(schema);
            match &canonical {
                None => canonical = Some((root.file_name.to_owned(), schema.clone(), digest)),
                Some((_, _, existing)) if *existing == digest => {}
                Some((owner, _, _)) => {
                    return Err(format!(
                        "family {} has conflicting shared schema bodies for $defs/{name} in {} and {}",
                        family.name, owner, root.file_name
                    )
                    .into());
                }
            }
        }

        let Some((_, schema, _)) = canonical else {
            return Err(format!(
                "family {} selected shared $defs/{name} but no owner was found",
                family.name
            )
            .into());
        };
        output.insert(name.clone(), schema);
    }

    Ok(output)
}

fn canonicalize_family(documents: &mut DocumentMap, family: &FamilySpec) -> Result<(), DynError> {
    let root_titles: BTreeMap<String, String> = family
        .roots
        .iter()
        .map(|root| (root.title.to_owned(), root.file_name.to_owned()))
        .collect();
    let root_schema_digests: BTreeMap<String, String> = family
        .roots
        .iter()
        .map(|root| {
            let digest = documents
                .get(root.file_name)
                .map(root_body_digest)
                .ok_or_else(|| format!("missing schema {}", root.file_name))?;
            Ok((root.file_name.to_owned(), digest?))
        })
        .collect::<Result<_, DynError>>()?;

    for root in family.roots {
        let document = documents
            .get_mut(root.file_name)
            .ok_or_else(|| format!("missing schema {}", root.file_name))?;
        let Some(defs) = get_defs_map_mut(document) else {
            continue;
        };

        let duplicate_roots: Vec<String> = defs
            .iter()
            .filter_map(|(name, schema)| {
                let owner = root_titles.get(name)?;
                if owner == root.file_name {
                    return None;
                }
                let owner_digest = root_schema_digests.get(owner)?;
                (canonical_string(schema) == *owner_digest).then(|| name.clone())
            })
            .collect();

        if duplicate_roots.is_empty() {
            continue;
        }

        rewrite_refs(document, &|name| {
            let owner = root_titles.get(name)?;
            (owner != root.file_name).then(|| format!("{owner}#"))
        });

        let defs = require_defs_map_mut(document)?;
        for name in duplicate_roots {
            defs.remove(&name);
        }
        remove_empty_defs(document);
    }

    let repeated_defs = collect_repeated_defs(documents, family)?;
    let shared_defs = collect_shared_closure(documents, family, &root_titles, repeated_defs)?;
    let mut shared_schema_defs = build_shared_defs(documents, family, &shared_defs)?;

    for schema in shared_schema_defs.values_mut() {
        rewrite_refs(schema, &|name| {
            if shared_defs.contains(name) {
                Some(format!("{}#/$defs/{name}", family.shared_file_name))
            } else {
                root_titles.get(name).map(|owner| format!("{owner}#"))
            }
        });
    }

    for root in family.roots {
        let document = documents
            .get_mut(root.file_name)
            .ok_or_else(|| format!("missing schema {}", root.file_name))?;

        rewrite_refs(document, &|name| {
            if shared_defs.contains(name) {
                Some(format!("{}#/$defs/{name}", family.shared_file_name))
            } else {
                let owner = root_titles.get(name)?;
                (owner != root.file_name).then(|| format!("{owner}#"))
            }
        });

        if let Some(defs) = get_defs_map_mut(document) {
            for name in &shared_defs {
                defs.remove(name);
            }
        }
        remove_empty_defs(document);
    }

    let shared_value = json!({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": family.shared_title,
        "$defs": shared_schema_defs,
    });
    documents.insert(family.shared_file_name.to_owned(), shared_value);

    Ok(())
}

fn canonicalize_family_graphs(mut documents: DocumentMap) -> Result<DocumentMap, DynError> {
    for family in FAMILIES {
        canonicalize_family(&mut documents, family)?;
    }
    Ok(documents)
}

fn write_documents(dir: &Path, documents: &DocumentMap) -> Result<(), DynError> {
    for (file_name, document) in documents {
        fs::write(dir.join(file_name), serde_json::to_string_pretty(document)?)?;
    }
    Ok(())
}

fn main() -> Result<(), DynError> {
    let out_dir = env::args()
        .nth(1)
        .ok_or("usage: export_json_schemas <out_dir>")?;
    let out = Path::new(&out_dir);
    fs::create_dir_all(out)?;

    let documents = canonicalize_family_graphs(generate_raw_roots()?)?;
    write_documents(out, &documents)?;

    Ok(())
}
