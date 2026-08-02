//! Configuration types for JSONTools operations.
//!
//! Defines operation modes, filtering flags, collision handling, replacement
//! patterns, and processing thresholds. Supports environment variable overrides
//! for parallelism settings.

use smallvec::SmallVec;
use std::sync::LazyLock;

/// Parse an environment variable once at process startup.
pub(crate) fn parse_env_usize(name: &str, default: usize) -> usize {
    std::env::var(name)
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(default)
}

/// Parse an optional environment variable (returns None if unset).
pub(crate) fn parse_env_usize_opt(name: &str) -> Option<usize> {
    std::env::var(name).ok().and_then(|v| v.parse().ok())
}

pub(crate) static DEFAULT_PARALLEL_THRESHOLD: LazyLock<usize> =
    LazyLock::new(|| parse_env_usize("JSON_TOOLS_PARALLEL_THRESHOLD", 100));
pub(crate) static DEFAULT_NESTED_PARALLEL_THRESHOLD: LazyLock<usize> =
    LazyLock::new(|| parse_env_usize("JSON_TOOLS_NESTED_PARALLEL_THRESHOLD", 100));
pub(crate) static DEFAULT_MAX_ARRAY_INDEX: LazyLock<usize> =
    LazyLock::new(|| parse_env_usize("JSON_TOOLS_MAX_ARRAY_INDEX", 100_000));
pub(crate) static DEFAULT_NUM_THREADS: LazyLock<Option<usize>> =
    LazyLock::new(|| parse_env_usize_opt("JSON_TOOLS_NUM_THREADS"));

/// Operation mode for the unified JSONTools API
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)] // Smaller discriminant for better cache locality
pub(crate) enum OperationMode {
    /// Flatten JSON structures
    Flatten,
    /// Unflatten JSON structures
    Unflatten,
    /// Normal processing (no flatten/unflatten) applying transformations recursively
    Normal,
}

/// Configuration for filtering operations
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct FilteringConfig {
    /// Remove keys with empty string values
    pub remove_empty_strings: bool,
    /// Remove keys with null values. Checked as the last step of a value's
    /// processing pipeline, after any configured `value_replacement` and
    /// `auto_convert_types` have both run -- so a value that only becomes `null`
    /// through a replacement (e.g. replacing a sentinel with a recognized null
    /// token) or through type conversion is still caught. This ordering is applied
    /// consistently across `.flatten()`, `.unflatten()`, and `.normal()` mode, and
    /// applies identically to single-document and batch input. A root-level `null`
    /// (the entire document, not a nested key) is never removed, since there's no
    /// parent key to omit it under.
    pub remove_nulls: bool,
    /// Remove keys with empty object values
    pub remove_empty_objects: bool,
    /// Remove keys with empty array values
    pub remove_empty_arrays: bool,
}

impl FilteringConfig {
    /// Create a new FilteringConfig with all filters disabled
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable removal of empty strings
    #[must_use]
    pub fn remove_empty_strings(mut self, enabled: bool) -> Self {
        self.remove_empty_strings = enabled;
        self
    }

    /// Enable removal of null values. See the field doc comment on
    /// [`FilteringConfig::remove_nulls`] for the ordering guarantee relative to
    /// `value_replacement`/`auto_convert_types`.
    #[must_use]
    pub fn remove_nulls(mut self, enabled: bool) -> Self {
        self.remove_nulls = enabled;
        self
    }

    /// Enable removal of empty objects
    #[must_use]
    pub fn remove_empty_objects(mut self, enabled: bool) -> Self {
        self.remove_empty_objects = enabled;
        self
    }

    /// Enable removal of empty arrays
    #[must_use]
    pub fn remove_empty_arrays(mut self, enabled: bool) -> Self {
        self.remove_empty_arrays = enabled;
        self
    }

    /// Check if any filtering is enabled
    pub fn has_any_filter(&self) -> bool {
        self.remove_empty_strings
            || self.remove_nulls
            || self.remove_empty_objects
            || self.remove_empty_arrays
    }
}

/// Configuration for collision handling strategies
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct CollisionConfig {
    /// Handle key collisions by collecting values into arrays
    pub handle_collisions: bool,
    /// Flattened key names that must always render as a JSON array, even
    /// when only one value is present in a given document -- so a field
    /// that collides in *some* documents of a batch but not others (e.g.
    /// because of `key_replacement`) has a consistent scalar-or-array shape
    /// across every document, not just within one. Matched against the
    /// final flattened key (after separator-joining and any key
    /// transforms), independent of `handle_collisions`: a key listed here
    /// always gets array treatment (collecting every colliding value, not
    /// just last-wins) regardless of that flag.
    pub always_array_keys: SmallVec<[String; 4]>,
}

impl CollisionConfig {
    /// Create a new CollisionConfig with collision handling disabled
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable collision handling by collecting values into arrays
    #[must_use]
    pub fn handle_collisions(mut self, enabled: bool) -> Self {
        self.handle_collisions = enabled;
        self
    }

    /// Set the flattened key names that must always render as an array --
    /// see `always_array_keys`'s own doc comment.
    #[must_use]
    pub fn always_array_keys<I, S>(mut self, keys: I) -> Self
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        self.always_array_keys = keys.into_iter().map(Into::into).collect();
        self
    }

    /// Check if any collision handling is enabled
    pub fn has_collision_handling(&self) -> bool {
        self.handle_collisions
    }

    /// Check if any always-array keys are configured.
    pub fn has_always_array_keys(&self) -> bool {
        !self.always_array_keys.is_empty()
    }
}

/// Configuration for replacement operations
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct ReplacementConfig {
    /// Key replacement patterns (find, replace)
    /// Uses SmallVec to avoid heap allocation for 0-2 replacements (common case)
    pub key_replacements: SmallVec<[(String, String); 2]>,
    /// Value replacement patterns (find, replace)
    /// Uses SmallVec to avoid heap allocation for 0-2 replacements (common case)
    pub value_replacements: SmallVec<[(String, String); 2]>,
    /// Patterns for excluding entire keys (and their values/subtrees) by name.
    /// Literal substring match by default; wrap in `r'...'` for regex, matching
    /// `key_replacements`'s convention. A key matches if any pattern is found in its
    /// full dot-path (flatten/unflatten) or in its own name at that nesting level
    /// (normal mode) -- matching a container key drops its entire subtree without
    /// walking it. See `crate::builder::JSONTools::exclude_key` for full docs.
    pub key_exclusions: SmallVec<[String; 2]>,
    /// Patterns for dropping a key-value pair by *value* content. Literal substring
    /// match by default; wrap in `r'...'` for regex. Only ever applies to scalar leaf
    /// values (strings/numbers/booleans/null) -- containers have no single value to
    /// check. Checked against the final value after any configured
    /// `value_replacement`/`auto_convert_types` have run, matching `remove_nulls`'s
    /// ordering guarantee. A no-op at the document root (no parent key to drop the
    /// value from), same precedent as `remove_nulls`. See
    /// `crate::builder::JSONTools::exclude_value` for full docs including the
    /// unflatten quoted-form caveat.
    pub value_exclusions: SmallVec<[String; 2]>,
}

impl ReplacementConfig {
    /// Create a new ReplacementConfig with no replacements
    pub fn new() -> Self {
        Self {
            key_replacements: SmallVec::new(),
            value_replacements: SmallVec::new(),
            key_exclusions: SmallVec::new(),
            value_exclusions: SmallVec::new(),
        }
    }

    /// Add a key replacement pattern
    #[must_use]
    pub fn add_key_replacement(
        mut self,
        find: impl Into<String>,
        replace: impl Into<String>,
    ) -> Self {
        self.key_replacements.push((find.into(), replace.into()));
        self
    }

    /// Add a value replacement pattern
    #[must_use]
    pub fn add_value_replacement(
        mut self,
        find: impl Into<String>,
        replace: impl Into<String>,
    ) -> Self {
        self.value_replacements.push((find.into(), replace.into()));
        self
    }

    /// Check if any key replacements are configured
    pub fn has_key_replacements(&self) -> bool {
        !self.key_replacements.is_empty()
    }

    /// Check if any value replacements are configured
    pub fn has_value_replacements(&self) -> bool {
        !self.value_replacements.is_empty()
    }

    /// Add a key exclusion pattern
    #[must_use]
    pub fn add_key_exclusion(mut self, pattern: impl Into<String>) -> Self {
        self.key_exclusions.push(pattern.into());
        self
    }

    /// Check if any key exclusions are configured
    pub fn has_key_exclusions(&self) -> bool {
        !self.key_exclusions.is_empty()
    }

    /// Add a value exclusion pattern
    #[must_use]
    pub fn add_value_exclusion(mut self, pattern: impl Into<String>) -> Self {
        self.value_exclusions.push(pattern.into());
        self
    }

    /// Check if any value exclusions are configured
    pub fn has_value_exclusions(&self) -> bool {
        !self.value_exclusions.is_empty()
    }
}

/// Configuration for date/datetime string detection and UTC normalization, used by
/// [`TypeConversionConfig`].
#[derive(Debug, Clone, PartialEq)]
#[non_exhaustive]
pub struct DateConversionConfig {
    /// Enable date/datetime detection and conversion
    pub enabled: bool,
    /// Normalize recognized dates/datetimes to UTC (default: true). When false, a
    /// value recognized as a date/datetime is left byte-for-byte unchanged, but is
    /// still protected from being misinterpreted as a number by the numbers category.
    pub normalize_to_utc: bool,
    /// For naive datetimes with no timezone info (e.g. `"2024-01-15T10:30:00"`),
    /// assume UTC and append `Z` (default: true). When false, naive datetimes are
    /// left as-is (still protected from number parsing, but not rewritten) since
    /// their true offset is unknown.
    pub assume_utc_for_naive: bool,
}

impl Default for DateConversionConfig {
    fn default() -> Self {
        Self {
            enabled: false,
            normalize_to_utc: true,
            assume_utc_for_naive: true,
        }
    }
}

impl DateConversionConfig {
    /// Create a new DateConversionConfig with default settings (disabled)
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable or disable date/datetime conversion
    #[must_use]
    pub fn enabled(mut self, enabled: bool) -> Self {
        self.enabled = enabled;
        self
    }

    /// Configure UTC normalization of recognized dates/datetimes
    #[must_use]
    pub fn normalize_to_utc(mut self, enabled: bool) -> Self {
        self.normalize_to_utc = enabled;
        self
    }

    /// Configure whether naive (timezone-less) datetimes are assumed to be UTC
    #[must_use]
    pub fn assume_utc_for_naive(mut self, enabled: bool) -> Self {
        self.assume_utc_for_naive = enabled;
        self
    }
}

/// Configuration for null-string detection, used by [`TypeConversionConfig`].
#[derive(Debug, Clone, PartialEq, Default)]
#[non_exhaustive]
pub struct NullConversionConfig {
    /// Enable null-string detection and conversion
    pub enabled: bool,
    /// Additional strings recognized as null, beyond the built-in list (`"null"`,
    /// `"NULL"`, `"Null"`, `"nil"`, `"NIL"`, `"Nil"`, `"none"`, `"NONE"`, `"None"`,
    /// `"N/A"`, `"n/a"`, `"NA"`, `"na"`). Additive only -- cannot narrow the built-in
    /// list. Matched exactly (case-sensitive).
    pub extra_tokens: SmallVec<[String; 2]>,
}

impl NullConversionConfig {
    /// Create a new NullConversionConfig with default settings (disabled)
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable or disable null-string conversion
    #[must_use]
    pub fn enabled(mut self, enabled: bool) -> Self {
        self.enabled = enabled;
        self
    }

    /// Add an additional string to recognize as null, beyond the built-in list
    #[must_use]
    pub fn add_extra_token(mut self, token: impl Into<String>) -> Self {
        self.extra_tokens.push(token.into());
        self
    }

    /// Check if any extra null tokens are configured
    pub fn has_extra_tokens(&self) -> bool {
        !self.extra_tokens.is_empty()
    }
}

/// Configuration for boolean-string detection, used by [`TypeConversionConfig`].
#[derive(Debug, Clone, PartialEq, Default)]
#[non_exhaustive]
pub struct BooleanConversionConfig {
    /// Enable boolean-string detection and conversion
    pub enabled: bool,
    /// Additional strings recognized as `true`, beyond the built-in list (`"true"`,
    /// `"TRUE"`, `"True"`, `"yes"`, `"YES"`, `"Yes"`, `"y"`, `"Y"`, `"on"`, `"ON"`,
    /// `"On"`). Additive only. Matched exactly (case-sensitive).
    pub extra_true_tokens: SmallVec<[String; 2]>,
    /// Additional strings recognized as `false`, beyond the built-in list (`"false"`,
    /// `"FALSE"`, `"False"`, `"no"`, `"NO"`, `"No"`, `"n"`, `"N"`, `"off"`, `"OFF"`,
    /// `"Off"`). Additive only. Matched exactly (case-sensitive).
    pub extra_false_tokens: SmallVec<[String; 2]>,
}

impl BooleanConversionConfig {
    /// Create a new BooleanConversionConfig with default settings (disabled)
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable or disable boolean-string conversion
    #[must_use]
    pub fn enabled(mut self, enabled: bool) -> Self {
        self.enabled = enabled;
        self
    }

    /// Add an additional string to recognize as `true`, beyond the built-in list
    #[must_use]
    pub fn add_extra_true_token(mut self, token: impl Into<String>) -> Self {
        self.extra_true_tokens.push(token.into());
        self
    }

    /// Add an additional string to recognize as `false`, beyond the built-in list
    #[must_use]
    pub fn add_extra_false_token(mut self, token: impl Into<String>) -> Self {
        self.extra_false_tokens.push(token.into());
        self
    }

    /// Check if any extra boolean tokens are configured
    pub fn has_extra_tokens(&self) -> bool {
        !self.extra_true_tokens.is_empty() || !self.extra_false_tokens.is_empty()
    }
}

/// Configuration for numeric-string detection, used by [`TypeConversionConfig`].
///
/// Plain integers/decimals, scientific notation, and thousands-separator cleanup
/// (`"1,234.56"`, `"1.234,56"`, `"1 234.56"`) are always-on "core" behavior whenever
/// `enabled` is true -- no one asked to disable unambiguous number parsing. The
/// remaining sub-formats are individually toggleable because each is "opinionated"
/// (can reinterpret a string that wasn't meant to be a number) in a way plain numeric
/// parsing isn't.
#[derive(Debug, Clone, PartialEq)]
#[non_exhaustive]
pub struct NumberConversionConfig {
    /// Enable numeric-string detection and conversion
    pub enabled: bool,
    /// Strip currency symbols (`$`, etc.), 3-letter currency codes (`USD`, `EUR`,
    /// ... -- only when followed by a space), and credit/debit suffixes (`CR`/`DR`).
    /// Default: true.
    pub currency: bool,
    /// Parse `%`, `\u{2030}` (permille), and `\u{2031}` (per-ten-thousand) suffixes.
    /// Default: true.
    pub percent: bool,
    /// Parse text basis-point suffixes: `"25bp"`/`"25bps"`/`"25 bp"`/`"25 bps"`.
    /// Default: true.
    pub basis_points: bool,
    /// Parse K/M/B/T magnitude suffixes: `"1K"`, `"2.5M"`, `"3B"`, `"1T"`.
    /// Default: true.
    pub suffixes: bool,
    /// Parse fractions: `"1/2"`, `"2 1/2"`. Default: true.
    pub fractions: bool,
    /// Parse hex/binary/octal literals: `"0x1A2B"`, `"0b1010"`, `"0o777"`.
    /// Default: true.
    pub radix: bool,
}

impl Default for NumberConversionConfig {
    fn default() -> Self {
        Self {
            enabled: false,
            currency: true,
            percent: true,
            basis_points: true,
            suffixes: true,
            fractions: true,
            radix: true,
        }
    }
}

impl NumberConversionConfig {
    /// Create a new NumberConversionConfig with default settings (disabled)
    pub fn new() -> Self {
        Self::default()
    }

    /// Enable or disable numeric-string conversion
    #[must_use]
    pub fn enabled(mut self, enabled: bool) -> Self {
        self.enabled = enabled;
        self
    }

    /// Configure currency symbol/code/credit-debit-suffix stripping
    #[must_use]
    pub fn currency(mut self, enabled: bool) -> Self {
        self.currency = enabled;
        self
    }

    /// Configure percent/permille/per-ten-thousand suffix parsing
    #[must_use]
    pub fn percent(mut self, enabled: bool) -> Self {
        self.percent = enabled;
        self
    }

    /// Configure text basis-point suffix parsing
    #[must_use]
    pub fn basis_points(mut self, enabled: bool) -> Self {
        self.basis_points = enabled;
        self
    }

    /// Configure K/M/B/T magnitude suffix parsing
    #[must_use]
    pub fn suffixes(mut self, enabled: bool) -> Self {
        self.suffixes = enabled;
        self
    }

    /// Configure fraction parsing
    #[must_use]
    pub fn fractions(mut self, enabled: bool) -> Self {
        self.fractions = enabled;
        self
    }

    /// Configure hex/binary/octal literal parsing
    #[must_use]
    pub fn radix(mut self, enabled: bool) -> Self {
        self.radix = enabled;
        self
    }
}

/// Bundles all four type-conversion categories (dates, nulls, booleans, numbers).
/// Assembled by [`crate::JSONTools`]'s `convert_*`/`convert_*_config`/
/// `auto_convert_types` builder methods and consumed by the processing engine.
#[derive(Debug, Clone, Default)]
#[non_exhaustive]
pub struct TypeConversionConfig {
    /// Date/datetime conversion settings
    pub dates: DateConversionConfig,
    /// Null-string conversion settings
    pub nulls: NullConversionConfig,
    /// Boolean-string conversion settings
    pub booleans: BooleanConversionConfig,
    /// Numeric-string conversion settings
    pub numbers: NumberConversionConfig,
}

impl TypeConversionConfig {
    /// Create a new TypeConversionConfig with all categories disabled
    pub fn new() -> Self {
        Self::default()
    }

    /// Configure date/datetime conversion
    #[must_use]
    pub fn dates(mut self, config: DateConversionConfig) -> Self {
        self.dates = config;
        self
    }

    /// Configure null-string conversion
    #[must_use]
    pub fn nulls(mut self, config: NullConversionConfig) -> Self {
        self.nulls = config;
        self
    }

    /// Configure boolean-string conversion
    #[must_use]
    pub fn booleans(mut self, config: BooleanConversionConfig) -> Self {
        self.booleans = config;
        self
    }

    /// Configure numeric-string conversion
    #[must_use]
    pub fn numbers(mut self, config: NumberConversionConfig) -> Self {
        self.numbers = config;
        self
    }

    /// Check if any type-conversion category is enabled
    pub fn has_any_enabled(&self) -> bool {
        self.dates.enabled || self.nulls.enabled || self.booleans.enabled || self.numbers.enabled
    }

    /// Classify into the fast-path bucket used by the hot per-string call sites in
    /// `flatten.rs`/`unflatten.rs`/`transform.rs`. Cheap (a handful of field/
    /// `is_empty()` comparisons, no allocation) -- computed once per `execute()` call
    /// in `ProcessingConfig::from_json_tools()`, not per string. See
    /// `TypeConversionMode`'s own doc comment for why this split exists.
    pub(crate) fn classify(&self) -> TypeConversionMode {
        if !self.has_any_enabled() {
            return TypeConversionMode::Disabled;
        }
        let all_default = self.dates
            == DateConversionConfig {
                enabled: true,
                ..DateConversionConfig::default()
            }
            && self.nulls
                == NullConversionConfig {
                    enabled: true,
                    ..NullConversionConfig::default()
                }
            && self.booleans
                == BooleanConversionConfig {
                    enabled: true,
                    ..BooleanConversionConfig::default()
                }
            && self.numbers
                == NumberConversionConfig {
                    enabled: true,
                    ..NumberConversionConfig::default()
                };
        if all_default {
            TypeConversionMode::AllDefault
        } else {
            TypeConversionMode::Custom
        }
    }
}

/// Precomputed fast-path classification of a [`TypeConversionConfig`], cached on
/// [`ProcessingConfig`]. Not part of the public API -- purely an internal dispatch
/// optimization that lets the hot per-string call sites in `flatten.rs`/
/// `unflatten.rs`/`transform.rs` avoid re-deriving "is this the untouched-default
/// case" on every single string value. `AllDefault` routes to the original,
/// unmodified `try_convert_string_to_json_bytes` (zero behavior/performance change
/// from before this type existed); `Custom` routes to the new
/// `try_convert_string_to_json_bytes_configured`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub(crate) enum TypeConversionMode {
    /// No type-conversion category is enabled
    Disabled,
    /// All four categories are enabled with untouched default sub-settings
    AllDefault,
    /// At least one category is enabled with non-default sub-settings, or only a
    /// subset of categories is enabled
    Custom,
}

/// Comprehensive configuration for JSON processing operations
#[derive(Debug, Clone)]
#[non_exhaustive]
pub struct ProcessingConfig {
    /// Separator for nested keys (default: ".")
    pub separator: String,
    /// Convert all keys to lowercase
    pub lowercase_keys: bool,
    /// Filtering configuration
    pub filtering: FilteringConfig,
    /// Collision handling configuration
    pub collision: CollisionConfig,
    /// Replacement configuration
    pub replacements: ReplacementConfig,
    /// Type-conversion configuration (dates, nulls, booleans, numbers)
    pub type_conversion: TypeConversionConfig,
    /// Precomputed fast-path classification of `type_conversion`, cached here so the
    /// hot per-string call sites never re-derive it. See `TypeConversionMode`'s doc
    /// comment.
    pub(crate) type_conversion_mode: TypeConversionMode,
    /// Minimum batch size for parallel processing
    pub parallel_threshold: usize,
    /// Number of threads for parallel processing (None = use system default)
    pub num_threads: Option<usize>,
    /// Minimum object/array size for nested parallel processing within a single JSON document
    /// Only objects/arrays with more than this many keys/items will be processed in parallel
    /// Default: 100 (can be overridden with JSON_TOOLS_NESTED_PARALLEL_THRESHOLD environment variable)
    pub nested_parallel_threshold: usize,
    /// Maximum array index allowed during unflattening to prevent DoS via malicious keys
    /// Default: 100,000 (can be overridden with JSON_TOOLS_MAX_ARRAY_INDEX environment variable)
    pub max_array_index: usize,
}

impl Default for ProcessingConfig {
    fn default() -> Self {
        Self {
            separator: ".".to_string(),
            lowercase_keys: false,
            filtering: FilteringConfig::default(),
            collision: CollisionConfig::default(),
            replacements: ReplacementConfig::default(),
            type_conversion: TypeConversionConfig::default(),
            type_conversion_mode: TypeConversionMode::Disabled,
            parallel_threshold: *DEFAULT_PARALLEL_THRESHOLD,
            num_threads: None, // Use system default (number of logical CPUs)
            nested_parallel_threshold: *DEFAULT_NESTED_PARALLEL_THRESHOLD,
            max_array_index: *DEFAULT_MAX_ARRAY_INDEX,
        }
    }
}

impl ProcessingConfig {
    /// Create a new ProcessingConfig with default settings
    pub fn new() -> Self {
        Self::default()
    }

    /// Resolve the thread count to use for a parallel workload of `item_count` items,
    /// honoring an explicit `num_threads` override and never exceeding `item_count`.
    pub(crate) fn effective_thread_count(&self, item_count: usize) -> usize {
        let base = self.num_threads.unwrap_or_else(|| {
            std::thread::available_parallelism()
                .map(|p| p.get())
                .unwrap_or(4)
        });
        base.max(1).min(item_count)
    }

    /// Set the separator for nested keys
    #[must_use]
    pub fn separator(mut self, separator: impl Into<String>) -> Self {
        self.separator = separator.into();
        self
    }

    /// Enable lowercase key conversion
    #[must_use]
    pub fn lowercase_keys(mut self, enabled: bool) -> Self {
        self.lowercase_keys = enabled;
        self
    }

    /// Configure filtering options
    #[must_use]
    pub fn filtering(mut self, filtering: FilteringConfig) -> Self {
        self.filtering = filtering;
        self
    }

    /// Configure collision handling options
    #[must_use]
    pub fn collision(mut self, collision: CollisionConfig) -> Self {
        self.collision = collision;
        self
    }

    /// Configure replacement options
    #[must_use]
    pub fn replacements(mut self, replacements: ReplacementConfig) -> Self {
        self.replacements = replacements;
        self
    }

    /// Configure type-conversion options (dates, nulls, booleans, numbers)
    #[must_use]
    pub fn type_conversion(mut self, type_conversion: TypeConversionConfig) -> Self {
        self.type_conversion_mode = type_conversion.classify();
        self.type_conversion = type_conversion;
        self
    }
}
