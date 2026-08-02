//! Wire format for transporting a `JSONTools` configuration as a JSON blob,
//! used to cross a serialization boundary from Python (`python.rs`'s pickle
//! support and, for a genuinely distributed PySpark path, a `mapInPandas`
//! partition function -- see `PyJSONTools::to_config_json`/`from_config_json`).
//!
//! Deliberately NOT feature-gated: unlike `python`, which is only compiled
//! when the `python` binding feature is enabled, this module is always
//! compiled so it has no dependency on that feature being active.

use serde::{Deserialize, Serialize};

use crate::builder::JSONTools;
use crate::config::{
    BooleanConversionConfig, DateConversionConfig, NullConversionConfig, NumberConversionConfig,
};
use crate::error::JsonToolsError;

/// Mirrors `JSONTools`'s builder options. Every field is optional on the way
/// *in* (`Deserialize`) so a field left unset by the caller falls through to
/// `JSONTools::new()`'s own defaults -- this keeps `builder.rs` the single
/// source of truth for defaults across every language binding, rather than
/// duplicating them here. `Serialize` is also derived (`JSONTools::
/// to_config_json` populates every field, so the two directions share one
/// struct definition and can never drift apart on field names/shape).
#[derive(Deserialize, Serialize, Default)]
#[serde(deny_unknown_fields, rename_all = "snake_case")]
pub(crate) struct Config {
    pub(crate) mode: Option<String>,
    pub(crate) separator: Option<String>,
    pub(crate) lowercase_keys: Option<bool>,
    #[serde(default)]
    pub(crate) key_replacements: Vec<(String, String)>,
    #[serde(default)]
    pub(crate) value_replacements: Vec<(String, String)>,
    #[serde(default)]
    pub(crate) key_exclusions: Vec<String>,
    #[serde(default)]
    pub(crate) value_exclusions: Vec<String>,
    pub(crate) remove_empty_strings: Option<bool>,
    pub(crate) remove_nulls: Option<bool>,
    pub(crate) remove_empty_objects: Option<bool>,
    pub(crate) remove_empty_arrays: Option<bool>,
    pub(crate) handle_key_collision: Option<bool>,
    #[serde(default)]
    pub(crate) always_array_keys: Vec<String>,
    pub(crate) auto_convert_types: Option<bool>,
    pub(crate) convert_dates: Option<bool>,
    pub(crate) date_conversion_config: Option<DateConversionConfigWire>,
    pub(crate) convert_nulls: Option<bool>,
    pub(crate) null_conversion_config: Option<NullConversionConfigWire>,
    pub(crate) convert_booleans: Option<bool>,
    pub(crate) boolean_conversion_config: Option<BooleanConversionConfigWire>,
    pub(crate) convert_numbers: Option<bool>,
    pub(crate) number_conversion_config: Option<NumberConversionConfigWire>,
    pub(crate) parallel_threshold: Option<usize>,
    pub(crate) num_threads: Option<usize>,
    pub(crate) nested_parallel_threshold: Option<usize>,
    pub(crate) max_array_index: Option<usize>,
}

/// Per-category customization mirrors of `DateConversionConfig`/etc. -- kept as
/// separate wire types (rather than (de)serializing the public config structs
/// directly) since `#[non_exhaustive]` blocks constructing those outside this
/// crate, and because every field here is optional on the way in (unset =
/// "don't override this knob"), unlike the public structs' plain bools.
#[derive(Deserialize, Serialize, Default)]
#[serde(deny_unknown_fields, rename_all = "snake_case")]
pub(crate) struct DateConversionConfigWire {
    pub(crate) normalize_to_utc: Option<bool>,
    pub(crate) assume_utc_for_naive: Option<bool>,
}

#[derive(Deserialize, Serialize, Default)]
#[serde(deny_unknown_fields, rename_all = "snake_case")]
pub(crate) struct NullConversionConfigWire {
    #[serde(default)]
    pub(crate) extra_tokens: Vec<String>,
}

#[derive(Deserialize, Serialize, Default)]
#[serde(deny_unknown_fields, rename_all = "snake_case")]
pub(crate) struct BooleanConversionConfigWire {
    #[serde(default)]
    pub(crate) extra_true_tokens: Vec<String>,
    #[serde(default)]
    pub(crate) extra_false_tokens: Vec<String>,
}

#[derive(Deserialize, Serialize, Default)]
#[serde(deny_unknown_fields, rename_all = "snake_case")]
pub(crate) struct NumberConversionConfigWire {
    pub(crate) currency: Option<bool>,
    pub(crate) percent: Option<bool>,
    pub(crate) basis_points: Option<bool>,
    pub(crate) suffixes: Option<bool>,
    pub(crate) fractions: Option<bool>,
    pub(crate) radix: Option<bool>,
}

pub(crate) fn build_tools(config_json: &str) -> Result<JSONTools, JsonToolsError> {
    let config: Config = serde_json::from_str(config_json)
        .map_err(|e| JsonToolsError::input_validation_error(format!("invalid config JSON: {e}")))?;

    let mut tools = JSONTools::new();
    tools = match config.mode.as_deref() {
        Some("flatten") => tools.flatten(),
        Some("unflatten") => tools.unflatten(),
        Some("normal") => tools.normal(),
        Some(other) => {
            return Err(JsonToolsError::configuration_error(format!(
                "unknown mode '{other}': expected 'flatten', 'unflatten', or 'normal'"
            )));
        }
        None => tools,
    };
    if let Some(separator) = config.separator {
        tools = tools.separator(separator);
    }
    if let Some(v) = config.lowercase_keys {
        tools = tools.lowercase_keys(v);
    }
    for (find, replace) in config.key_replacements {
        tools = tools.key_replacement(find, replace);
    }
    for (find, replace) in config.value_replacements {
        tools = tools.value_replacement(find, replace);
    }
    for pattern in config.key_exclusions {
        tools = tools.exclude_key(pattern);
    }
    for pattern in config.value_exclusions {
        tools = tools.exclude_value(pattern);
    }
    if let Some(v) = config.remove_empty_strings {
        tools = tools.remove_empty_strings(v);
    }
    if let Some(v) = config.remove_nulls {
        tools = tools.remove_nulls(v);
    }
    if let Some(v) = config.remove_empty_objects {
        tools = tools.remove_empty_objects(v);
    }
    if let Some(v) = config.remove_empty_arrays {
        tools = tools.remove_empty_arrays(v);
    }
    if let Some(v) = config.handle_key_collision {
        tools = tools.handle_key_collision(v);
    }
    if !config.always_array_keys.is_empty() {
        tools = tools.always_array_keys(config.always_array_keys);
    }
    if let Some(v) = config.auto_convert_types {
        tools = tools.auto_convert_types(v);
    }
    // Nested customization applied first, then the top-level bool -- the bool only
    // ever touches `enabled`, so applying it last preserves customization already
    // set via the nested config block (same ordering principle as the Rust/Python
    // builders' `_config` methods).
    if let Some(date_cfg) = config.date_conversion_config {
        let mut cfg = DateConversionConfig::new();
        if let Some(v) = date_cfg.normalize_to_utc {
            cfg = cfg.normalize_to_utc(v);
        }
        if let Some(v) = date_cfg.assume_utc_for_naive {
            cfg = cfg.assume_utc_for_naive(v);
        }
        tools = tools.convert_dates_config(cfg);
    }
    if let Some(v) = config.convert_dates {
        tools = tools.convert_dates(v);
    }
    if let Some(null_cfg) = config.null_conversion_config {
        let mut cfg = NullConversionConfig::new();
        for token in null_cfg.extra_tokens {
            cfg = cfg.add_extra_token(token);
        }
        tools = tools.convert_nulls_config(cfg);
    }
    if let Some(v) = config.convert_nulls {
        tools = tools.convert_nulls(v);
    }
    if let Some(bool_cfg) = config.boolean_conversion_config {
        let mut cfg = BooleanConversionConfig::new();
        for token in bool_cfg.extra_true_tokens {
            cfg = cfg.add_extra_true_token(token);
        }
        for token in bool_cfg.extra_false_tokens {
            cfg = cfg.add_extra_false_token(token);
        }
        tools = tools.convert_booleans_config(cfg);
    }
    if let Some(v) = config.convert_booleans {
        tools = tools.convert_booleans(v);
    }
    if let Some(num_cfg) = config.number_conversion_config {
        let mut cfg = NumberConversionConfig::new();
        if let Some(v) = num_cfg.currency {
            cfg = cfg.currency(v);
        }
        if let Some(v) = num_cfg.percent {
            cfg = cfg.percent(v);
        }
        if let Some(v) = num_cfg.basis_points {
            cfg = cfg.basis_points(v);
        }
        if let Some(v) = num_cfg.suffixes {
            cfg = cfg.suffixes(v);
        }
        if let Some(v) = num_cfg.fractions {
            cfg = cfg.fractions(v);
        }
        if let Some(v) = num_cfg.radix {
            cfg = cfg.radix(v);
        }
        tools = tools.convert_numbers_config(cfg);
    }
    if let Some(v) = config.convert_numbers {
        tools = tools.convert_numbers(v);
    }
    if let Some(v) = config.parallel_threshold {
        tools = tools.parallel_threshold(v);
    }
    if let Some(v) = config.num_threads {
        tools = tools.num_threads(Some(v));
    }
    if let Some(v) = config.nested_parallel_threshold {
        tools = tools.nested_parallel_threshold(v);
    }
    if let Some(v) = config.max_array_index {
        tools = tools.max_array_index(v);
    }
    Ok(tools)
}
