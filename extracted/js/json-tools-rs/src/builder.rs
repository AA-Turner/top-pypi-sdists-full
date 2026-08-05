//! Builder API and execution engine for JSONTools.
//!
//! Provides the fluent builder interface (`JSONTools::new().flatten().execute()`)
//! and orchestrates flattening, unflattening, transformations, and parallel
//! batch processing.

use std::borrow::Cow;

use rayon::prelude::*;
use smallvec::SmallVec;

use crate::config::{
    BooleanConversionConfig, CollisionConfig, DateConversionConfig, FilteringConfig,
    NullConversionConfig, NumberConversionConfig, OperationMode, ProcessingConfig,
    ReplacementConfig, TypeConversionConfig, DEFAULT_MAX_ARRAY_INDEX,
    DEFAULT_NESTED_PARALLEL_THRESHOLD, DEFAULT_NUM_THREADS, DEFAULT_PARALLEL_THRESHOLD,
};
use crate::error::JsonToolsError;
use crate::flatten::process_single_json;
use crate::transform::process_single_json_normal;
use crate::types::{JsonInput, JsonOutput};
use crate::unflatten::process_single_json_for_unflatten;

// ================================================================================================
// ProcessingConfig::from_json_tools() - lives here to avoid circular dependency
// ================================================================================================

impl ProcessingConfig {
    /// Create a ProcessingConfig from a JSONTools builder instance
    pub fn from_json_tools(tools: &JSONTools) -> Self {
        let type_conversion = TypeConversionConfig {
            dates: tools.date_conversion.clone(),
            nulls: tools.null_conversion.clone(),
            booleans: tools.boolean_conversion.clone(),
            numbers: tools.number_conversion.clone(),
        };
        let type_conversion_mode = type_conversion.classify();
        Self {
            separator: tools.separator.to_string(),
            lowercase_keys: tools.lowercase_keys,
            filtering: FilteringConfig {
                remove_empty_strings: tools.remove_empty_string_values,
                remove_nulls: tools.remove_null_values,
                remove_empty_objects: tools.remove_empty_objects,
                remove_empty_arrays: tools.remove_empty_arrays,
            },
            collision: CollisionConfig {
                handle_collisions: tools.handle_key_collision,
                always_array_keys: tools.always_array_keys.clone(),
            },
            replacements: ReplacementConfig {
                key_replacements: tools.key_replacements.clone(),
                value_replacements: tools.value_replacements.clone(),
                key_exclusions: tools.key_exclusions.clone(),
                value_exclusions: tools.value_exclusions.clone(),
            },
            type_conversion,
            type_conversion_mode,
            parallel_threshold: tools.parallel_threshold,
            num_threads: tools.num_threads,
            nested_parallel_threshold: tools.nested_parallel_threshold,
            max_array_index: tools.max_array_index,
        }
    }
}

// ================================================================================================
// JSONTools Builder Struct
// ================================================================================================

/// Unified JSON Tools API with builder pattern for both flattening and unflattening operations
///
/// This is the unified interface for all JSON manipulation operations.
/// It provides a single entry point for all JSON manipulation operations with a consistent builder pattern.
#[derive(Debug, Clone)]
pub struct JSONTools {
    // SmallVec fields (stack-allocated for 0-2 replacements, common case)
    /// Key replacement patterns (find, replace)
    /// Uses SmallVec to avoid heap allocation for 0-2 replacements (90% of use cases)
    key_replacements: SmallVec<[(String, String); 2]>,
    /// Value replacement patterns (find, replace)
    /// Uses SmallVec to avoid heap allocation for 0-2 replacements (90% of use cases)
    value_replacements: SmallVec<[(String, String); 2]>,
    /// Key exclusion patterns -- keys matching any of these are dropped entirely
    /// (along with their subtree). Uses SmallVec to avoid heap allocation for 0-2
    /// patterns (common case)
    key_exclusions: SmallVec<[String; 2]>,
    /// Value exclusion patterns -- a key-value pair is dropped if its (scalar leaf)
    /// value matches any of these. Uses SmallVec to avoid heap allocation for 0-2
    /// patterns (common case)
    value_exclusions: SmallVec<[String; 2]>,
    /// Separator for nested keys (default: "."). `Cow` rather than `String`:
    /// the default and any explicit `.separator(".")` call store a
    /// `Cow::Borrowed`, avoiding an allocation that `SeparatorCache::new`
    /// (`flatten.rs`) would just special-case away anyway (it already
    /// treats `"."` and 11 other common separators as borrowed constants).
    separator: Cow<'static, str>,
    /// Flattened key names that must always render as an array -- see
    /// `CollisionConfig::always_array_keys`'s doc comment. `SmallVec`
    /// (stack-allocated up to 4 keys, the common case; a linear scan beats a
    /// hash lookup for the tiny, developer-configured lists this holds --
    /// measured, see `always_array_keys`'s own doc comment) -- zero
    /// allocation for callers who don't use the feature.
    always_array_keys: SmallVec<[String; 4]>,

    // Medium fields (8 bytes on 64-bit systems)
    /// Minimum batch size to use parallel processing (default: 100)
    parallel_threshold: usize,
    /// Number of threads for parallel processing (None = use system default)
    num_threads: Option<usize>,
    /// Minimum object/array size for nested parallel processing within a single JSON document
    nested_parallel_threshold: usize,
    /// Maximum array index allowed during unflattening (DoS protection)
    max_array_index: usize,

    // Type-conversion sub-configs (dates, nulls, booleans, numbers)
    /// Date/datetime conversion settings
    date_conversion: DateConversionConfig,
    /// Null-string conversion settings
    null_conversion: NullConversionConfig,
    /// Boolean-string conversion settings
    boolean_conversion: BooleanConversionConfig,
    /// Numeric-string conversion settings
    number_conversion: NumberConversionConfig,

    // Medium fields (2 bytes)
    /// Current operation mode (flatten or unflatten)
    mode: Option<OperationMode>,

    // Small fields (1 byte each) - grouped together to minimize padding
    /// Remove keys with empty string values
    remove_empty_string_values: bool,
    /// Remove keys with null values
    remove_null_values: bool,
    /// Remove keys with empty object values
    remove_empty_objects: bool,
    /// Remove keys with empty array values
    remove_empty_arrays: bool,
    /// Convert all keys to lowercase
    lowercase_keys: bool,
    /// Handle key collisions by collecting values into arrays
    handle_key_collision: bool,
}

impl Default for JSONTools {
    fn default() -> Self {
        Self {
            // SmallVec fields - no heap allocation for 0-2 replacements!
            key_replacements: SmallVec::new(),
            value_replacements: SmallVec::new(),
            key_exclusions: SmallVec::new(),
            value_exclusions: SmallVec::new(),
            separator: Cow::Borrowed("."),
            always_array_keys: SmallVec::new(),
            // Medium fields — use shared LazyLock statics from config module
            parallel_threshold: *DEFAULT_PARALLEL_THRESHOLD,
            num_threads: *DEFAULT_NUM_THREADS,
            nested_parallel_threshold: *DEFAULT_NESTED_PARALLEL_THRESHOLD,
            max_array_index: *DEFAULT_MAX_ARRAY_INDEX,
            date_conversion: DateConversionConfig::default(),
            null_conversion: NullConversionConfig::default(),
            boolean_conversion: BooleanConversionConfig::default(),
            number_conversion: NumberConversionConfig::default(),
            mode: None,
            // Small fields
            remove_empty_string_values: false,
            remove_null_values: false,
            remove_empty_objects: false,
            remove_empty_arrays: false,
            lowercase_keys: false,
            handle_key_collision: false,
        }
    }
}

impl JSONTools {
    /// Create a new JSONTools instance with default settings
    pub fn new() -> Self {
        Self::default()
    }

    /// Set the operation mode to flatten
    #[must_use]
    pub fn flatten(mut self) -> Self {
        self.mode = Some(OperationMode::Flatten);
        self
    }

    /// Set the operation mode to unflatten
    #[must_use]
    pub fn unflatten(mut self) -> Self {
        self.mode = Some(OperationMode::Unflatten);
        self
    }

    /// Set the operation mode to normal (apply transformations without flatten/unflatten)
    ///
    /// In normal mode, key/value replacements, filtering, and type conversion are applied
    /// recursively to the JSON structure without flattening or unflattening it.
    ///
    /// # Example
    ///
    /// ```rust
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// let json = r#"{"Name": "John", "Age": "30", "Active": "true"}"#;
    /// let result = JSONTools::new()
    ///     .normal()
    ///     .lowercase_keys(true)
    ///     .auto_convert_types(true)
    ///     .execute(json).unwrap();
    ///
    /// match result {
    ///     JsonOutput::Single(output) => {
    ///         assert!(output.contains(r#""name""#));
    ///         assert!(output.contains(r#":30"#) || output.contains(r#": 30"#));
    ///     }
    ///     _ => unreachable!(),
    /// }
    /// ```
    #[must_use]
    pub fn normal(mut self) -> Self {
        self.mode = Some(OperationMode::Normal);
        self
    }

    /// Set the separator used for nested keys (default: ".")
    ///
    /// Empty separators are rejected at [`execute()`](Self::execute) time with a descriptive error.
    #[must_use]
    pub fn separator(mut self, separator: impl Into<String>) -> Self {
        let separator = separator.into();
        self.separator = match separator.as_str() {
            "." => Cow::Borrowed("."),
            _ => Cow::Owned(separator),
        };
        self
    }

    /// Convert all keys to lowercase
    #[must_use]
    pub fn lowercase_keys(mut self, value: bool) -> Self {
        self.lowercase_keys = value;
        self
    }

    /// Add a key replacement pattern
    ///
    /// Patterns are literal (exact substring match) by default. Wrap a pattern in
    /// `r'...'` (e.g. `r'^admin_'`) to use standard Rust regex syntax instead. A
    /// malformed `r'...'` pattern is silently treated as "no match" rather than
    /// raising an error. Works for both flatten and unflatten operations.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// // Regex pattern, via the r'...' wrapper
    /// let json = r#"{"user_name": "John", "admin_name": "Jane"}"#;
    /// let result = JSONTools::new()
    ///     .flatten()
    ///     .key_replacement("r'(user|admin)_'", "person_")
    ///     .execute(json).unwrap();
    ///
    /// // Literal pattern (the default -- no r'...' wrapper)
    /// let result2 = JSONTools::new()
    ///     .flatten()
    ///     .key_replacement("user_", "person_")
    ///     .execute(json).unwrap();
    /// ```
    #[must_use]
    pub fn key_replacement(mut self, find: impl Into<String>, replace: impl Into<String>) -> Self {
        self.key_replacements.push((find.into(), replace.into()));
        self
    }

    /// Add a value replacement pattern
    ///
    /// Patterns are literal (exact substring match) by default. Wrap a pattern in
    /// `r'...'` (e.g. `r'^admin_'`) to use standard Rust regex syntax instead. A
    /// malformed `r'...'` pattern is silently treated as "no match" rather than
    /// raising an error. Works for both flatten and unflatten operations.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// // Regex pattern, via the r'...' wrapper
    /// let json = r#"{"role": "super", "level": "admin"}"#;
    /// let result = JSONTools::new()
    ///     .flatten()
    ///     .value_replacement("r'^(super|admin)$'", "administrator")
    ///     .execute(json).unwrap();
    ///
    /// // Literal pattern (the default -- no r'...' wrapper)
    /// let result2 = JSONTools::new()
    ///     .flatten()
    ///     .value_replacement("@example.com", "@company.org")
    ///     .execute(json).unwrap();
    /// ```
    #[must_use]
    pub fn value_replacement(
        mut self,
        find: impl Into<String>,
        replace: impl Into<String>,
    ) -> Self {
        self.value_replacements.push((find.into(), replace.into()));
        self
    }

    /// Exclude any key (and its entire value/subtree) whose name contains `pattern`
    ///
    /// Patterns are literal (exact substring match) by default. Wrap a pattern in
    /// `r'...'` (e.g. `r'^crypto_'`) to use standard Rust regex syntax instead,
    /// matching `key_replacement`'s convention. Additive -- call once per keyword to
    /// exclude multiple.
    ///
    /// Checked against the full dot-path in flatten/unflatten mode, and per key at
    /// each nesting level in normal mode. Matching a container key drops its entire
    /// subtree without walking it -- a leaf key is caught by the same check at its
    /// own level. Array elements are never matched (no key name to check).
    ///
    /// # Examples
    ///
    /// ```rust
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// // Matching a container key ("crypto_wallet") drops its entire subtree --
    /// // "coin" and "balance" never appear in the output, without being individually
    /// // matched themselves.
    /// let json = r#"{"user": {"name": "John", "crypto_wallet": {"coin": "BTC", "balance": 100}}}"#;
    /// let result = JSONTools::new()
    ///     .flatten()
    ///     .exclude_key("crypto")
    ///     .execute(json).unwrap();
    /// // Output: {"user.name": "John"}
    /// ```
    #[must_use]
    pub fn exclude_key(mut self, pattern: impl Into<String>) -> Self {
        self.key_exclusions.push(pattern.into());
        self
    }

    /// Drop a key-value pair whose value contains `pattern`
    ///
    /// Patterns are literal (exact substring match) by default. Wrap a pattern in
    /// `r'...'` to use regex, matching `exclude_key`'s convention. Additive -- call
    /// once per pattern to exclude multiple.
    ///
    /// Only ever applies to scalar leaf values (strings/numbers/booleans/null) --
    /// containers have no single value to check, so a value inside a nested object is
    /// still individually checked, but the object itself never is. Checked against the
    /// final value *after* any configured `value_replacement`/`auto_convert_types`
    /// have run, so a value that only matches after being replaced or converted is
    /// still caught -- matching `remove_nulls`'s ordering guarantee. A no-op at the
    /// document root (there's no parent key to drop the value from).
    ///
    /// **Unflatten-specific note**: string values are matched against their JSON-
    /// serialized form (including surrounding quotes), not the unescaped logical
    /// text. Literal patterns are unaffected by this, but a regex with anchors needs
    /// to account for the quotes, e.g. `r'^"admin"$'` rather than `r'^admin$'`, to
    /// match a value that's exactly `"admin"`.
    ///
    /// # Examples
    ///
    /// ```rust
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// let json = r#"{"user": {"name": "John", "status": "banned"}}"#;
    /// let result = JSONTools::new()
    ///     .flatten()
    ///     .exclude_value("banned")
    ///     .execute(json).unwrap();
    /// // Output: {"user.name": "John"}
    /// ```
    #[must_use]
    pub fn exclude_value(mut self, pattern: impl Into<String>) -> Self {
        self.value_exclusions.push(pattern.into());
        self
    }

    /// Remove keys with empty string values
    ///
    /// Works for both flatten and unflatten operations:
    /// - In flatten mode: removes flattened keys that have empty string values
    /// - In unflatten mode: removes keys from the unflattened JSON structure that have empty string values
    #[must_use]
    pub fn remove_empty_strings(mut self, value: bool) -> Self {
        self.remove_empty_string_values = value;
        self
    }

    /// Remove keys with null values
    ///
    /// Works identically in `.flatten()`, `.unflatten()`, and `.normal()` mode, and
    /// for both single-document and batch input:
    /// - In flatten mode: removes flattened keys that have null values
    /// - In unflatten mode: removes keys from the unflattened JSON structure that have null values
    /// - In normal mode: removes keys (at any nesting depth) that have null values
    ///
    /// This check runs *last* in a value's processing pipeline -- after any
    /// configured `value_replacement` and `auto_convert_types` have both been
    /// applied -- so it reliably catches a null produced by either of those, not
    /// just a null present in the original input. A root-level `null` (the entire
    /// document, not a nested key) is never removed, since there's no parent key to
    /// omit it under.
    #[must_use]
    pub fn remove_nulls(mut self, value: bool) -> Self {
        self.remove_null_values = value;
        self
    }

    /// Remove keys with empty object values
    ///
    /// Works for both flatten and unflatten operations:
    /// - In flatten mode: removes flattened keys that have empty object values
    /// - In unflatten mode: removes keys from the unflattened JSON structure that have empty object values
    #[must_use]
    pub fn remove_empty_objects(mut self, value: bool) -> Self {
        self.remove_empty_objects = value;
        self
    }

    /// Remove keys with empty array values
    ///
    /// Works for both flatten and unflatten operations:
    /// - In flatten mode: removes flattened keys that have empty array values
    /// - In unflatten mode: removes keys from the unflattened JSON structure that have empty array values
    #[must_use]
    pub fn remove_empty_arrays(mut self, value: bool) -> Self {
        self.remove_empty_arrays = value;
        self
    }

    /// Handle key collisions by collecting values into arrays
    ///
    /// When enabled, collect all values that would have the same key into an array.
    /// Works for all operations (flatten, unflatten, normal).
    #[must_use]
    pub fn handle_key_collision(mut self, value: bool) -> Self {
        self.handle_key_collision = value;
        self
    }

    /// Flattened key names that must always render as a JSON array, even when
    /// only one value is present in a given document.
    ///
    /// Without this, a key's scalar-vs-array shape depends on whether a
    /// collision actually happened *in that specific document*: a key that
    /// collides in some documents of a batch (e.g. because of
    /// [`key_replacement`](Self::key_replacement)) but not others ends up a
    /// `str` in some outputs and a `list` in others -- an inconsistent shape
    /// that's awkward for any downstream consumer expecting a stable schema
    /// (including building a DataFrame column from the results). Naming a key
    /// here guarantees every document that has that key emits it as an array
    /// -- `[value]` for one value, the full collected array for more --
    /// regardless of [`handle_key_collision`](Self::handle_key_collision).
    ///
    /// Matched against the *final* flattened key name (after separator-joining
    /// and any key transforms), the same name [`handle_key_collision`](Self::handle_key_collision)
    /// resolves collisions on. Works for all operations (flatten, unflatten, normal).
    ///
    /// # Example
    ///
    /// ```rust
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new()
    ///     .flatten()
    ///     .key_replacement("r'(User|Admin)_'", "")
    ///     .always_array_keys(["name"]);
    ///
    /// // Collides in this document -> already an array without this option.
    /// let with_collision = tools.execute(r#"{"User_name": "a", "Admin_name": "b"}"#).unwrap();
    /// // No collision in this one -> without always_array_keys this would be a bare string.
    /// let without_collision = tools.execute(r#"{"User_name": "a"}"#).unwrap();
    /// ```
    #[must_use]
    pub fn always_array_keys<I, S>(mut self, keys: I) -> Self
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        self.always_array_keys = keys.into_iter().map(Into::into).collect();
        self
    }

    /// Enable automatic type conversion from strings to dates, nulls, booleans, and numbers
    ///
    /// When enabled, the library will attempt to convert string values to their native
    /// JSON types:
    /// - **Dates**: ISO-8601 date/datetime strings are normalized to UTC
    /// - **Nulls**: "null"/"NULL"/"nil"/"none"/"N/A"/"NA" -> null
    /// - **Booleans**: "true"/"TRUE"/"True"/"yes"/"on" -> true, "false"/"no"/"off" -> false
    /// - **Numbers**: "123" -> 123, "1,234.56" -> 1234.56, "$99.99" -> 99.99, "1e5" -> 100000
    ///
    /// If conversion fails, the original string value is kept. No errors are thrown.
    ///
    /// Works for all operations (flatten, unflatten, normal).
    ///
    /// This is equivalent to calling [`Self::convert_dates`], [`Self::convert_nulls`],
    /// [`Self::convert_booleans`], and [`Self::convert_numbers`] all with the same
    /// `enable` value -- it only ever flips each category's on/off switch, preserving
    /// any per-category customization already configured via the `convert_*_config`
    /// methods. For independent control over each category, or to customize a
    /// category's behavior (e.g. recognizing extra null tokens, disabling UTC
    /// normalization for dates, or turning off individual number sub-formats like
    /// currency/percent/basis-points/suffixes/fractions/radix), use the `convert_*`
    /// methods directly instead of this one.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::{JSONTools, JsonOutput};
    ///
    /// let json = r#"{"id": "123", "price": "1,234.56", "active": "true"}"#;
    /// let result = JSONTools::new()
    ///     .flatten()
    ///     .auto_convert_types(true)
    ///     .execute(json)
    ///     .unwrap();
    ///
    /// match result {
    ///     JsonOutput::Single(output) => {
    ///         // Result: {"id": 123, "price": 1234.56, "active": true}
    ///         assert!(output.contains(r#""id":123"#));
    ///         assert!(output.contains(r#""price":1234.56"#));
    ///         assert!(output.contains(r#""active":true"#));
    ///     }
    ///     _ => unreachable!(),
    /// }
    /// ```
    #[must_use]
    pub fn auto_convert_types(mut self, enable: bool) -> Self {
        self.date_conversion.enabled = enable;
        self.null_conversion.enabled = enable;
        self.boolean_conversion.enabled = enable;
        self.number_conversion.enabled = enable;
        self
    }

    /// Enable or disable date/datetime string conversion independently of the other
    /// type-conversion categories. See [`Self::auto_convert_types`] for the general
    /// behavior; use [`Self::convert_dates_config`] to customize UTC-normalization
    /// behavior.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new().flatten().convert_dates(true);
    /// ```
    #[must_use]
    pub fn convert_dates(mut self, enable: bool) -> Self {
        self.date_conversion.enabled = enable;
        self
    }

    /// Configure date/datetime conversion with custom settings (e.g. disabling UTC
    /// normalization, or disabling the UTC assumption for timezone-less datetimes).
    /// Sets `enabled` from the passed [`crate::DateConversionConfig`]'s own `enabled`
    /// field.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::{JSONTools, DateConversionConfig};
    ///
    /// let tools = JSONTools::new().flatten().convert_dates_config(
    ///     DateConversionConfig::new().enabled(true).assume_utc_for_naive(false),
    /// );
    /// ```
    #[must_use]
    pub fn convert_dates_config(mut self, config: DateConversionConfig) -> Self {
        self.date_conversion = config;
        self
    }

    /// Enable or disable null-string conversion independently of the other
    /// type-conversion categories. See [`Self::auto_convert_types`] for the general
    /// behavior; use [`Self::convert_nulls_config`] to recognize additional tokens.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new().flatten().convert_nulls(true);
    /// ```
    #[must_use]
    pub fn convert_nulls(mut self, enable: bool) -> Self {
        self.null_conversion.enabled = enable;
        self
    }

    /// Configure null-string conversion with additional recognized tokens, beyond the
    /// built-in list. Sets `enabled` from the passed [`crate::NullConversionConfig`]'s
    /// own `enabled` field.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::{JSONTools, NullConversionConfig};
    ///
    /// let tools = JSONTools::new().flatten().convert_nulls_config(
    ///     NullConversionConfig::new().enabled(true).add_extra_token("missing"),
    /// );
    /// ```
    #[must_use]
    pub fn convert_nulls_config(mut self, config: NullConversionConfig) -> Self {
        self.null_conversion = config;
        self
    }

    /// Enable or disable boolean-string conversion independently of the other
    /// type-conversion categories. See [`Self::auto_convert_types`] for the general
    /// behavior; use [`Self::convert_booleans_config`] to recognize additional tokens.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new().flatten().convert_booleans(true);
    /// ```
    #[must_use]
    pub fn convert_booleans(mut self, enable: bool) -> Self {
        self.boolean_conversion.enabled = enable;
        self
    }

    /// Configure boolean-string conversion with additional recognized true/false
    /// tokens, beyond the built-in lists. Sets `enabled` from the passed
    /// [`crate::BooleanConversionConfig`]'s own `enabled` field.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::{JSONTools, BooleanConversionConfig};
    ///
    /// let tools = JSONTools::new().flatten().convert_booleans_config(
    ///     BooleanConversionConfig::new()
    ///         .enabled(true)
    ///         .add_extra_true_token("si")
    ///         .add_extra_false_token("nope"),
    /// );
    /// ```
    #[must_use]
    pub fn convert_booleans_config(mut self, config: BooleanConversionConfig) -> Self {
        self.boolean_conversion = config;
        self
    }

    /// Enable or disable numeric-string conversion independently of the other
    /// type-conversion categories. See [`Self::auto_convert_types`] for the general
    /// behavior; use [`Self::convert_numbers_config`] to disable individual
    /// sub-formats (currency, percent, basis points, suffixes, fractions, radix).
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new().flatten().convert_numbers(true);
    /// ```
    #[must_use]
    pub fn convert_numbers(mut self, enable: bool) -> Self {
        self.number_conversion.enabled = enable;
        self
    }

    /// Configure numeric-string conversion, individually toggling sub-formats.
    /// Plain integers/decimals, scientific notation, and thousands-separator cleanup
    /// are always applied when `enabled` is true; currency, percent, basis-points,
    /// suffixes, fractions, and radix parsing can each be disabled independently.
    /// Sets `enabled` from the passed [`crate::NumberConversionConfig`]'s own
    /// `enabled` field.
    ///
    /// # Example
    /// ```
    /// use json_tools_rs::{JSONTools, NumberConversionConfig};
    ///
    /// let tools = JSONTools::new().flatten().convert_numbers_config(
    ///     NumberConversionConfig::new().enabled(true).currency(false),
    /// );
    /// ```
    #[must_use]
    pub fn convert_numbers_config(mut self, config: NumberConversionConfig) -> Self {
        self.number_conversion = config;
        self
    }

    /// Read the currently configured date-conversion settings. `pub(crate)` --
    /// used by the Python bindings' read-modify-write kwargs bridging.
    #[cfg(feature = "python")]
    pub(crate) fn date_conversion(&self) -> &DateConversionConfig {
        &self.date_conversion
    }

    /// Read the currently configured null-conversion settings. `pub(crate)` --
    /// used by the Python bindings' read-modify-write kwargs bridging.
    #[cfg(feature = "python")]
    pub(crate) fn null_conversion(&self) -> &NullConversionConfig {
        &self.null_conversion
    }

    /// Read the currently configured boolean-conversion settings. `pub(crate)` --
    /// used by the Python bindings' read-modify-write kwargs bridging.
    #[cfg(feature = "python")]
    pub(crate) fn boolean_conversion(&self) -> &BooleanConversionConfig {
        &self.boolean_conversion
    }

    /// Read the currently configured number-conversion settings. `pub(crate)` --
    /// used by the Python bindings' read-modify-write kwargs bridging.
    #[cfg(feature = "python")]
    pub(crate) fn number_conversion(&self) -> &NumberConversionConfig {
        &self.number_conversion
    }

    /// Set the minimum batch size for parallel processing (only available with 'parallel' feature)
    ///
    /// When processing multiple JSON documents, this threshold determines when to use
    /// parallel processing. Batches smaller than this threshold will be processed sequentially
    /// to avoid the overhead of thread spawning.
    ///
    /// Default: 100 items (can be overridden with JSON_TOOLS_PARALLEL_THRESHOLD environment variable)
    ///
    /// # Arguments
    ///
    /// * `threshold` - Minimum number of items in a batch to trigger parallel processing
    ///
    /// # Example
    ///
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new()
    ///     .flatten()
    ///     .parallel_threshold(50); // Only use parallelism for batches of 50+ items
    /// ```
    #[must_use]
    pub fn parallel_threshold(mut self, threshold: usize) -> Self {
        self.parallel_threshold = threshold;
        self
    }

    /// Configure the number of threads for parallel processing
    ///
    /// By default, the number of logical CPUs is used. This method allows you to override
    /// that behavior for specific workloads or resource constraints.
    ///
    /// # Arguments
    ///
    /// * `num_threads` - Number of threads to use (None = use system default)
    ///
    /// # Examples
    ///
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new()
    ///     .flatten()
    ///     .num_threads(Some(4)); // Use exactly 4 threads
    /// ```
    #[must_use]
    pub fn num_threads(mut self, num_threads: Option<usize>) -> Self {
        self.num_threads = num_threads;
        self
    }

    /// Configure the threshold for nested parallel processing within individual JSON documents
    ///
    /// When flattening or unflattening a single large JSON document, this threshold determines
    /// when to parallelize the processing of objects and arrays. Only objects/arrays with more
    /// than this many keys/items will be processed in parallel.
    ///
    /// Default: 100 (can be overridden with JSON_TOOLS_NESTED_PARALLEL_THRESHOLD environment variable)
    ///
    /// # Arguments
    ///
    /// * `threshold` - Minimum number of keys/items to trigger nested parallelism
    ///
    /// # Examples
    ///
    /// ```
    /// use json_tools_rs::JSONTools;
    ///
    /// let tools = JSONTools::new()
    ///     .flatten()
    ///     .nested_parallel_threshold(200); // Only parallelize objects/arrays with 200+ items
    /// ```
    #[must_use]
    pub fn nested_parallel_threshold(mut self, threshold: usize) -> Self {
        self.nested_parallel_threshold = threshold;
        self
    }

    /// Set the maximum array index allowed during unflattening
    ///
    /// This prevents denial-of-service attacks where a malicious flattened key like
    /// `"items.999999999"` would cause allocation of a massive array. Keys with array
    /// indices exceeding this limit will produce an error during unflattening.
    ///
    /// Default: 100,000 (can be overridden with JSON_TOOLS_MAX_ARRAY_INDEX environment variable)
    #[must_use]
    pub fn max_array_index(mut self, max: usize) -> Self {
        self.max_array_index = max;
        self
    }

    /// Execute the configured operation on the provided JSON input
    ///
    /// This method performs the selected operation based on the mode set by calling
    /// `.flatten()`, `.unflatten()`, or `.normal()`. If no mode was set, an error is returned.
    ///
    /// # Arguments
    /// * `json_input` - JSON input that can be a single string, multiple strings, or other supported types
    ///
    /// # Returns
    /// * `Result<JsonOutput, Box<dyn Error>>` - The processed JSON result or an error
    ///
    /// # Errors
    /// * Returns an error if no operation mode has been set
    /// * Returns an error if the JSON input is invalid
    /// * Returns an error if processing fails for any other reason
    pub fn execute<'a, T>(&self, json_input: T) -> Result<JsonOutput, JsonToolsError>
    where
        T: Into<JsonInput<'a>>,
    {
        let mode = self.mode.as_ref().ok_or_else(|| {
            JsonToolsError::configuration_error(
                "Operation mode not set. Call .flatten(), .unflatten(), or .normal() before .execute()"
            )
        })?;

        if self.separator.is_empty() {
            return Err(JsonToolsError::configuration_error(
                "Separator cannot be empty. Use .separator(\".\") or another non-empty string",
            ));
        }

        if let Some(0) = self.num_threads {
            return Err(JsonToolsError::configuration_error(
                "num_threads must be at least 1. Use None for system default",
            ));
        }

        let input = json_input.into();
        match mode {
            OperationMode::Flatten => self.execute_flatten(input),
            OperationMode::Unflatten => self.execute_unflatten(input),
            OperationMode::Normal => self.execute_normal(input),
        }
    }

    /// Generic batch processing helper that eliminates code duplication
    /// Processes single or multiple JSON inputs using the provided processor function
    #[inline]
    fn execute_with_processor<'a, F>(
        input: JsonInput<'a>,
        config: &ProcessingConfig,
        processor: F,
    ) -> Result<JsonOutput, JsonToolsError>
    where
        F: Fn(&str, &ProcessingConfig) -> Result<String, JsonToolsError> + Sync + Send,
    {
        match input {
            JsonInput::Single(json_cow) => {
                let result = processor(json_cow.as_ref(), config)?;
                Ok(JsonOutput::Single(result))
            }
            JsonInput::Multiple(json_list) => {
                let results = Self::process_batch(json_list, config, &processor)?;
                Ok(JsonOutput::Multiple(results))
            }
            JsonInput::MultipleOwned(vecs) => {
                let results = Self::process_batch(&vecs, config, &processor)?;
                Ok(JsonOutput::Multiple(results))
            }
        }
    }

    /// Process a batch of items (parallel or sequential) using a shared processor function.
    /// Items must implement AsRef<str> + Sync, covering both &str slices and Cow<str> vecs.
    fn process_batch<I, F>(
        items: &[I],
        config: &ProcessingConfig,
        processor: &F,
    ) -> Result<Vec<String>, JsonToolsError>
    where
        I: AsRef<str> + Sync,
        F: Fn(&str, &ProcessingConfig) -> Result<String, JsonToolsError> + Sync + Send,
    {
        if items.len() >= config.parallel_threshold {
            let map_item = |(index, item): (usize, &I)| {
                processor(item.as_ref(), config)
                    .map_err(|e| JsonToolsError::batch_processing_error(index, e))
            };

            // rayon's global pool is already sized to available_parallelism() and persists
            // across calls -- reuse it directly unless the caller explicitly overrode the
            // thread count, in which case a dedicated scoped pool is built for this call only
            // (that override is rare; the common None case stays on the fast persistent pool).
            return match config.num_threads {
                None => items.par_iter().enumerate().map(map_item).collect(),
                Some(n) => {
                    let pool = rayon::ThreadPoolBuilder::new()
                        .num_threads(n)
                        .build()
                        .map_err(|e| {
                            JsonToolsError::configuration_error(format!(
                                "failed to build thread pool with {n} threads: {e}"
                            ))
                        })?;
                    pool.install(|| items.par_iter().enumerate().map(map_item).collect())
                }
            };
        }

        // Sequential processing (default or below threshold)
        let mut results = Vec::with_capacity(items.len());
        for (index, item) in items.iter().enumerate() {
            match processor(item.as_ref(), config) {
                Ok(result) => results.push(result),
                Err(e) => return Err(JsonToolsError::batch_processing_error(index, e)),
            }
        }
        Ok(results)
    }

    fn execute_flatten<'a>(&self, input: JsonInput<'a>) -> Result<JsonOutput, JsonToolsError> {
        let config = ProcessingConfig::from_json_tools(self);
        Self::execute_with_processor(input, &config, process_single_json)
    }

    fn execute_unflatten<'a>(&self, input: JsonInput<'a>) -> Result<JsonOutput, JsonToolsError> {
        let config = ProcessingConfig::from_json_tools(self);
        Self::execute_with_processor(input, &config, process_single_json_for_unflatten)
    }

    fn execute_normal<'a>(&self, input: JsonInput<'a>) -> Result<JsonOutput, JsonToolsError> {
        let config = ProcessingConfig::from_json_tools(self);
        Self::execute_with_processor(input, &config, process_single_json_normal)
    }

    /// Serializes this configuration to a JSON blob that
    /// `config_json::build_tools` can reconstruct an equivalent `JSONTools`
    /// from -- the mechanism behind `PyJSONTools`'s pickle support
    /// (`__reduce__`/`from_config_json` in `python.rs`).
    ///
    /// Every field is populated (not just ones a caller explicitly
    /// customized): the round trip only needs to reproduce the *resolved*
    /// state, not the exact sequence of builder calls used to reach it, so
    /// `auto_convert_types` is deliberately left unset here in favor of the
    /// four per-category `convert_*` flags, which fully capture the same
    /// resolved state unambiguously.
    #[cfg(feature = "python")]
    pub(crate) fn to_config_json(&self) -> String {
        use crate::config_json::{
            BooleanConversionConfigWire, Config, DateConversionConfigWire,
            NullConversionConfigWire, NumberConversionConfigWire,
        };

        let config = Config {
            mode: self.mode.map(|m| {
                match m {
                    OperationMode::Flatten => "flatten",
                    OperationMode::Unflatten => "unflatten",
                    OperationMode::Normal => "normal",
                }
                .to_string()
            }),
            separator: Some(self.separator.to_string()),
            lowercase_keys: Some(self.lowercase_keys),
            key_replacements: self.key_replacements.iter().cloned().collect(),
            value_replacements: self.value_replacements.iter().cloned().collect(),
            key_exclusions: self.key_exclusions.iter().cloned().collect(),
            value_exclusions: self.value_exclusions.iter().cloned().collect(),
            remove_empty_strings: Some(self.remove_empty_string_values),
            remove_nulls: Some(self.remove_null_values),
            remove_empty_objects: Some(self.remove_empty_objects),
            remove_empty_arrays: Some(self.remove_empty_arrays),
            handle_key_collision: Some(self.handle_key_collision),
            always_array_keys: self.always_array_keys.iter().cloned().collect(),
            auto_convert_types: None,
            convert_dates: Some(self.date_conversion.enabled),
            date_conversion_config: Some(DateConversionConfigWire {
                normalize_to_utc: Some(self.date_conversion.normalize_to_utc),
                assume_utc_for_naive: Some(self.date_conversion.assume_utc_for_naive),
            }),
            convert_nulls: Some(self.null_conversion.enabled),
            null_conversion_config: Some(NullConversionConfigWire {
                extra_tokens: self.null_conversion.extra_tokens.iter().cloned().collect(),
            }),
            convert_booleans: Some(self.boolean_conversion.enabled),
            boolean_conversion_config: Some(BooleanConversionConfigWire {
                extra_true_tokens: self
                    .boolean_conversion
                    .extra_true_tokens
                    .iter()
                    .cloned()
                    .collect(),
                extra_false_tokens: self
                    .boolean_conversion
                    .extra_false_tokens
                    .iter()
                    .cloned()
                    .collect(),
            }),
            convert_numbers: Some(self.number_conversion.enabled),
            number_conversion_config: Some(NumberConversionConfigWire {
                currency: Some(self.number_conversion.currency),
                percent: Some(self.number_conversion.percent),
                basis_points: Some(self.number_conversion.basis_points),
                suffixes: Some(self.number_conversion.suffixes),
                fractions: Some(self.number_conversion.fractions),
                radix: Some(self.number_conversion.radix),
            }),
            parallel_threshold: Some(self.parallel_threshold),
            num_threads: self.num_threads,
            nested_parallel_threshold: Some(self.nested_parallel_threshold),
            max_array_index: Some(self.max_array_index),
        };

        // Infallible: `Config` is a plain data struct with no map keys, no
        // floats, nothing `serde_json` can fail to encode.
        serde_json::to_string(&config).expect("Config serialization is infallible")
    }

    /// True if `.flatten()` (not `.unflatten()`/`.normal()`/unset) is the configured
    /// mode -- used by `PyJSONTools::execute_normalise` (`python.rs`) to reject
    /// `normalise=True` early with a clear error, since unflattened/nested JSON
    /// can't produce clean scalar columns for a wide DataFrame.
    #[cfg(feature = "python")]
    pub(crate) fn is_flatten_mode(&self) -> bool {
        matches!(self.mode, Some(OperationMode::Flatten))
    }
}
