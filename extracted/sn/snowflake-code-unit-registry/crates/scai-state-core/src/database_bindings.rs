//! Reads the `database-bindings.yml` SnowConvert generates and turns it into the
//! literal token map [`FindOptions::bindings`] consumes, so a read can return
//! physical database names instead of the tokens a bindable conversion wrote.
//!
//! Lives outside `registry` for the same reason [`crate::bindings`] does: it
//! operates on caller-supplied values, not on registry state.
//!
//! # Why this exists
//!
//! A bindable conversion records `${NAME}` in `source.database` and `<%NAME%>` in
//! `target.database` so one artifact can be deployed and tested in whichever
//! database the operator chose. Every consumer therefore has to resolve those
//! tokens before treating the value as a real identifier — and each one that
//! forgets produces a bug far from its cause. Supplying the map at the read
//! removes the whole class rather than patching instances of it.
//!
//! # Grammar ownership
//!
//! [`crate::bindings::apply_bindings`] is deliberately grammar-free: it matches
//! map keys verbatim and knows nothing about wrappers. This module is the *only*
//! place that knows a wrapper spelling, and it is careful about which:
//!
//! * The Snowflake side is Snow CLI templating, `<%NAME%>`, which is invariant —
//!   so [`DatabaseBindings::snow_token_map`] owns it.
//! * The source side is **not** ownable here. The wrapper is a property of the
//!   source script language and may be customer-specific, and more than one form
//!   can be in play for a single name. [`DatabaseBindings::source_token_map`]
//!   therefore takes the form(s) from the caller and defaults to `${NAME}`.
//!
//! # Case
//!
//! [`crate::bindings::apply_bindings`] matches byte-exact and leaves an unmatched
//! token alone, so a bindings file whose key case differs from the case the
//! conversion wrote would resolve nothing — silently. The token map therefore
//! emits as-written, all-lower and all-upper spellings of each name, and input
//! whose intended spelling is ambiguous is rejected outright. See [`wrap`].
//!
//! # Hazard: do not bind a read that mints a frozen identity
//!
//! `apply_bindings` substitutes `target.name` and `target.canonical_name` as well
//! as `target.database`. Consumers that derive a stable identity from those — a
//! baseline lookup key, a stage path, an on-disk layout — must read **without**
//! bindings, or the identity silently changes and previously stored artifacts stop
//! matching with no error raised. Read unbound for identity, bound for anything
//! that needs a physical database.

use std::collections::HashMap;
use std::path::Path;

use crate::error::{Error, Result};

/// Renders a binding name as the literal token a conversion wrote for it.
///
/// Used by [`DatabaseBindings::source_token_map`] to stay independent of any one
/// source-side wrapper spelling.
pub type TokenWrapper = fn(&str) -> String;

/// The default source-side wrapper: `${NAME}`, the BTEQ / shell-style form.
pub fn dollar_brace_token(name: &str) -> String {
    format!("${{{name}}}")
}

/// The invariant Snowflake-side wrapper: `<%NAME%>`, Snow CLI templating.
pub fn snow_cli_token(name: &str) -> String {
    format!("<%{name}%>")
}

/// The two sides of a `database-bindings.yml`.
///
/// ```yaml
/// source:
///   dutchie_test: dutchie_test          # identity when the source is named that
/// snow:
///   dutchie_test: DUTCHIE_EXTRACT_MIG   # the retargeted physical database
/// ```
///
/// Both sections are optional: a project may be bindable on one side only, and an
/// absent section yields an empty map rather than an error.
#[derive(Debug, Clone, Default, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct DatabaseBindings {
    /// Canonical name → physical **source** database.
    #[serde(default)]
    pub source: HashMap<String, String>,
    /// Canonical name → physical **Snowflake** database.
    #[serde(default)]
    pub snow: HashMap<String, String>,
}

/// Parse `database-bindings.yml` contents.
///
/// Unknown top-level sections are rejected: a silently-empty map would make
/// substitution a no-op and hand tokens back to a caller that believes they were
/// resolved, which is the exact failure this module exists to prevent.
///
/// Two keys in one section that differ only by case are rejected for the same
/// reason — see [`reject_case_collisions`].
///
/// Returns `Err(Error::ValidationError)` when the document is not valid YAML or
/// does not match the two-section shape.
pub fn parse_database_bindings(yaml: &str) -> Result<DatabaseBindings> {
    let parsed: DatabaseBindings = serde_norway::from_str(yaml)
        .map_err(|e| Error::validation(format!("database-bindings.yml is not valid: {e}")))?;
    reject_case_collisions("source", &parsed.source)?;
    reject_case_collisions("snow", &parsed.snow)?;
    Ok(parsed)
}

/// Reject two keys in one section that differ only by case.
///
/// [`wrap`] emits a case variant per name, so `{db: A, DB: B}` would have both
/// names claiming the same variant keys and the winner would depend on hash
/// iteration order — a nondeterministic substitution. Rejecting is the only
/// honest answer: nothing here can know which spelling the conversion wrote.
fn reject_case_collisions(section: &str, names: &HashMap<String, String>) -> Result<()> {
    let mut folded: HashMap<String, &str> = HashMap::with_capacity(names.len());
    for name in names.keys() {
        if let Some(other) = folded.insert(name.to_lowercase(), name.as_str()) {
            let (a, b) = if name.as_str() < other {
                (name.as_str(), other)
            } else {
                (other, name.as_str())
            };
            return Err(Error::validation(format!(
                "database-bindings.yml is not valid: `{section}` has two keys differing only by \
                 case (`{a}` and `{b}`); the token map emits case variants, so which one applied \
                 would depend on hash order"
            )));
        }
    }
    Ok(())
}

/// Read and parse a `database-bindings.yml` from disk.
///
/// Convenience over [`parse_database_bindings`] for callers holding a path. IO
/// failures surface as `Error::IoError`, parse failures as in
/// [`parse_database_bindings`].
pub fn read_database_bindings(path: &Path) -> Result<DatabaseBindings> {
    let text = std::fs::read_to_string(path)?;
    parse_database_bindings(&text)
}

impl DatabaseBindings {
    /// `<%NAME%> → physical database`, for reads that should return Snowflake
    /// names instead of target-side tokens.
    ///
    /// Feed straight into [`FindOptions::bindings`]. Empty when the `snow:`
    /// section is absent, which makes the read a no-op rather than an error.
    ///
    /// See the module-level hazard note before binding a read whose result mints
    /// a frozen identity.
    pub fn snow_token_map(&self) -> HashMap<String, String> {
        wrap(&self.snow, &[snow_cli_token])
    }

    /// `wrapper(NAME) → physical database` for every wrapper form supplied.
    ///
    /// Pass the form(s) the conversion actually wrote. Every form becomes its own
    /// key, so a name carrying more than one spelling resolves whichever appears;
    /// a form that was never written simply matches nothing.
    ///
    /// Use [`Self::source_token_map_default`] for the common `${NAME}` case.
    pub fn source_token_map(&self, wrappers: &[TokenWrapper]) -> HashMap<String, String> {
        wrap(&self.source, wrappers)
    }

    /// [`Self::source_token_map`] with the default `${NAME}` wrapper.
    pub fn source_token_map_default(&self) -> HashMap<String, String> {
        wrap(&self.source, &[dollar_brace_token])
    }

    /// Both sides in one map — `${NAME} → source database` and
    /// `<%NAME%> → Snowflake database` — so one read returns fully bound units.
    ///
    /// Merging is safe because the two wrappers are *disjoint*: a `${…}` key can
    /// never match a `<%…%>` token or vice versa, so a slot only ever matches the
    /// side whose grammar it was written in. This is what lets
    /// [`FindOptions::bindings_path`] take a path and nothing else.
    ///
    /// Uses the **default** `${NAME}` source grammar. A project whose conversion
    /// wrote a customer-specific source wrapper gets no source-side resolution
    /// from this — and, `apply_bindings` leaving unmatched tokens alone, would get
    /// it *silently*. Those callers must build the map explicitly with
    /// [`Self::source_token_map`] / [`Self::source_token_map_from_formats`] and
    /// pass `bindings`. The snow side is unaffected: `<%NAME%>` is invariant.
    pub fn token_map(&self) -> HashMap<String, String> {
        let mut out = self.source_token_map_default();
        out.extend(self.snow_token_map());
        out
    }

    /// [`Self::source_token_map`] for callers that can only pass *data*, not a
    /// function pointer — the language bindings.
    ///
    /// `forms` are format strings containing `{name}` (e.g. `"${{{name}}}"` or a
    /// customer's `"@{name}@"`). A callable cannot cross the FFI boundary and
    /// [`TokenWrapper`] cannot be built from one, so the bindings pass strings.
    ///
    /// This exists so the case handling in [`wrap`] applies to the bindings too.
    /// Each of them previously expanded these forms inline, which meant the
    /// custom-wrapper path silently skipped the case spellings — the same defect
    /// this module was just fixed for, reintroduced three times over. One
    /// definition, called from all four surfaces.
    ///
    /// Returns `Err` naming the offending form when one lacks `{name}`; each
    /// binding maps that to its own error type.
    pub fn source_token_map_from_formats(
        &self,
        forms: &[String],
    ) -> std::result::Result<HashMap<String, String>, String> {
        // Empty means "not specified", i.e. the default `${NAME}` grammar -- decided
        // here so all four surfaces agree. They cannot agree by convention: the C# FFI
        // receives the forms as JSON and cannot distinguish an absent list from an
        // empty one, so it always treated empty as the default, while Python and Node
        // passed `[]` straight through and produced an *empty* source map. That
        // divergence resolved nothing on the source side and, `apply_bindings` leaving
        // unmatched tokens alone, said nothing about it.
        if forms.is_empty() {
            return Ok(self.source_token_map_default());
        }
        if let Some(bad) = forms.iter().find(|f| !f.contains("{name}")) {
            return Err(format!("source wrapper {bad:?} must contain '{{name}}'"));
        }
        let mut out = HashMap::with_capacity(self.source.len() * forms.len() * 3);
        for (name, value) in &self.source {
            for spelling in case_spellings(name) {
                for form in forms {
                    out.insert(form.replace("{name}", &spelling), value.clone());
                }
            }
        }
        Ok(out)
    }
}

/// The spellings a conversion may have written for `name`: as-written, all-lower,
/// all-upper. Duplicates are harmless — every consumer inserts into a map.
///
/// See [`wrap`] for why more than the as-written spelling is emitted.
fn case_spellings(name: &str) -> [String; 3] {
    [name.to_string(), name.to_lowercase(), name.to_uppercase()]
}

/// Expand a `name → value` map into `wrapper(spelling) → value` for each wrapper
/// and each case spelling of the name.
///
/// No bare-name key is ever emitted: a bare name would also match *inside* the
/// other side's wrapped token and corrupt it.
///
/// # Why case variants
///
/// [`crate::bindings::apply_bindings`] matches keys **byte-exact**
/// (`substitute_literal` uses `starts_with`), and it leaves an unmatched token
/// untouched rather than erroring. So a `database-bindings.yml` whose key case
/// differs from the case the conversion wrote into the registry would resolve
/// nothing, silently — the token would flow onward and surface far away as a
/// `001003` syntax error on the `<` of `<%NAME%>`.
///
/// The two cases genuinely differ in practice: the engine emits the canonical
/// name lower-case while the config normaliser upper-cases it, which is why the
/// desktop's own `substitute_tokens` casefolds on lookup. Rather than make the
/// core case-insensitive — it is deliberately literal and grammar-free, and
/// folding there would affect every other substitution — the compatibility lives
/// here, in the one place that already knows about spelling.
///
/// Emitting extra *wrapped* forms is safe: each is specific, and a form the
/// engine never wrote simply matches nothing. This covers as-written, all-lower
/// and all-upper; an arbitrary mixed-case spelling the conversion invented
/// (`<%Db_Name%>` from a key `db_name`) is still not matched, which is why
/// [`reject_case_collisions`] refuses input where the intended spelling is
/// ambiguous rather than guessing.
fn wrap(names: &HashMap<String, String>, wrappers: &[TokenWrapper]) -> HashMap<String, String> {
    // 3 spellings per name per wrapper, before dedup.
    let mut out = HashMap::with_capacity(names.len() * wrappers.len() * 3);
    for (name, value) in names {
        // Identical spellings collapse on insert; case collisions across two
        // different names cannot occur, having been rejected at parse time.
        for spelling in case_spellings(name) {
            for wrapper in wrappers {
                out.insert(wrapper(&spelling), value.clone());
            }
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    /// The shape SnowConvert actually writes.
    const REAL: &str =
        "source:\n  dutchie_test: dutchie_test\nsnow:\n  dutchie_test: DUTCHIE_EXTRACT_MIG\n";

    #[test]
    fn parses_the_real_file_shape() {
        let b = parse_database_bindings(REAL).unwrap();
        assert_eq!(b.source.get("dutchie_test").unwrap(), "dutchie_test");
        assert_eq!(b.snow.get("dutchie_test").unwrap(), "DUTCHIE_EXTRACT_MIG");
    }

    #[test]
    fn snow_map_is_wrapped_in_snow_cli_form() {
        let b = parse_database_bindings(REAL).unwrap();
        let m = b.snow_token_map();
        // as-written (== lower here) plus the upper spelling: 2 keys, not 1.
        assert_eq!(m.len(), 2);
        assert_eq!(m.get("<%dutchie_test%>").unwrap(), "DUTCHIE_EXTRACT_MIG");
        assert_eq!(m.get("<%DUTCHIE_TEST%>").unwrap(), "DUTCHIE_EXTRACT_MIG");
        // no bare key: it would match inside the source-side token too
        assert!(!m.contains_key("dutchie_test"));
        assert!(!m.contains_key("DUTCHIE_TEST"));
    }

    /// The regression this module shipped with: byte-exact matching in
    /// `substitute_literal` means a YAML key cased differently from the token the
    /// conversion wrote resolves *nothing*, and `apply_bindings` leaves an
    /// unmatched token alone — so it fails silently and surfaces as a `001003`
    /// syntax error on the `<`, layers from the cause.
    #[test]
    fn key_case_need_not_match_the_token_case() {
        // Upper-case key, as the config normaliser writes it...
        let b = parse_database_bindings("snow:\n  DUTCHIE_TEST: DUTCHIE_EXTRACT_MIG\n").unwrap();
        let m = b.snow_token_map();
        // ...still resolves the lower-case token the engine emits.
        assert_eq!(m.get("<%dutchie_test%>").unwrap(), "DUTCHIE_EXTRACT_MIG");
        assert_eq!(m.get("<%DUTCHIE_TEST%>").unwrap(), "DUTCHIE_EXTRACT_MIG");

        // ...and the mirror case: lower-case key, upper-case token.
        let b = parse_database_bindings("snow:\n  dutchie_test: DUTCHIE_EXTRACT_MIG\n").unwrap();
        assert_eq!(
            b.snow_token_map().get("<%DUTCHIE_TEST%>").unwrap(),
            "DUTCHIE_EXTRACT_MIG"
        );
    }

    /// The language bindings go through this rather than expanding inline; before
    /// they did, the custom-wrapper path skipped the case spellings entirely.
    #[test]
    fn format_string_wrappers_get_the_case_spellings_too() {
        let b = parse_database_bindings("source:\n  MyDb: real_db\n").unwrap();
        // Plain format strings carrying a literal `{name}`, per the documented
        // convention (`"@{name}@"`) -- these are data, not Rust `format!` syntax.
        let m = b
            .source_token_map_from_formats(&["@{name}@".to_string(), "[{name}]".to_string()])
            .unwrap();
        // 2 forms x 3 spellings
        assert_eq!(m.len(), 6);
        for key in ["@MyDb@", "@mydb@", "@MYDB@", "[MyDb]", "[mydb]", "[MYDB]"] {
            assert_eq!(
                m.get(key).map(String::as_str),
                Some("real_db"),
                "missing {key}"
            );
        }
    }

    /// An empty form list means "unspecified", not "resolve nothing" -- the C# FFI
    /// cannot tell absent from empty, so this is the only way the four surfaces agree.
    #[test]
    fn no_wrapper_forms_falls_back_to_the_default_grammar() {
        let b = parse_database_bindings("source:\n  db: real\n").unwrap();
        let from_empty = b.source_token_map_from_formats(&[]).unwrap();
        assert_eq!(from_empty, b.source_token_map_default());
        assert_eq!(from_empty.get("${db}").map(String::as_str), Some("real"));
        assert!(
            !from_empty.is_empty(),
            "an empty form list must not silently resolve nothing"
        );
    }

    #[test]
    fn format_string_wrapper_must_contain_the_name_placeholder() {
        let b = parse_database_bindings("source:\n  db: real\n").unwrap();
        let err = b
            .source_token_map_from_formats(&["no-placeholder".to_string()])
            .unwrap_err();
        assert!(err.contains("must contain"), "unexpected error: {err}");
    }

    #[test]
    fn source_side_gets_the_same_case_treatment() {
        let b = parse_database_bindings("source:\n  MyDb: real_db\n").unwrap();
        let m = b.source_token_map_default();
        assert_eq!(m.get("${MyDb}").unwrap(), "real_db");
        assert_eq!(m.get("${mydb}").unwrap(), "real_db");
        assert_eq!(m.get("${MYDB}").unwrap(), "real_db");
    }

    /// Two names differing only by case make the emitted variants ambiguous, and
    /// nothing here can know which spelling the conversion wrote — so this is
    /// rejected rather than resolved by hash order.
    #[test]
    fn keys_differing_only_by_case_are_rejected() {
        let err =
            parse_database_bindings("snow:\n  dutchie_test: A\n  DUTCHIE_TEST: B\n").unwrap_err();
        let msg = format!("{err}");
        assert!(msg.contains("differing only by"), "unexpected error: {msg}");
        assert!(msg.contains("dutchie_test") && msg.contains("DUTCHIE_TEST"));
    }

    /// The collision check is per-section: the same name on both sides is normal
    /// (that is what the real file looks like) and must stay legal.
    #[test]
    fn the_same_name_on_both_sides_is_not_a_collision() {
        assert!(parse_database_bindings(REAL).is_ok());
    }

    #[test]
    fn source_map_defaults_to_dollar_brace() {
        let b = parse_database_bindings(REAL).unwrap();
        let m = b.source_token_map_default();
        assert_eq!(m.get("${dutchie_test}").unwrap(), "dutchie_test");
        assert!(!m.contains_key("dutchie_test"));
    }

    /// The identity mapping in the real file is not a no-op to detect: the *key*
    /// is still a token, so substitution still has work to do.
    #[test]
    fn identity_mapping_still_strips_the_token() {
        let b = parse_database_bindings(REAL).unwrap();
        let m = b.source_token_map_default();
        assert_eq!(m.get("${dutchie_test}").unwrap(), "dutchie_test");
    }

    #[test]
    fn multiple_source_wrappers_each_get_a_key() {
        fn at_form(name: &str) -> String {
            format!("@{name}@")
        }
        let b = parse_database_bindings(REAL).unwrap();
        let m = b.source_token_map(&[dollar_brace_token, at_form]);
        // 2 wrappers x 2 distinct case spellings of a lower-case name.
        assert_eq!(m.len(), 4);
        assert_eq!(m.get("${dutchie_test}").unwrap(), "dutchie_test");
        assert_eq!(m.get("@dutchie_test@").unwrap(), "dutchie_test");
        assert_eq!(m.get("${DUTCHIE_TEST}").unwrap(), "dutchie_test");
        assert_eq!(m.get("@DUTCHIE_TEST@").unwrap(), "dutchie_test");
    }

    #[test]
    fn one_sided_file_is_accepted() {
        let b = parse_database_bindings("snow:\n  db: PHYSICAL\n").unwrap();
        assert!(b.source.is_empty());
        assert_eq!(b.snow_token_map().get("<%db%>").unwrap(), "PHYSICAL");
        assert_eq!(b.snow_token_map().get("<%DB%>").unwrap(), "PHYSICAL");
        // an absent side yields an empty map, so the read is a no-op not an error
        assert!(b.source_token_map_default().is_empty());
    }

    #[test]
    fn empty_document_is_accepted_as_empty_maps() {
        let b = parse_database_bindings("{}").unwrap();
        assert!(b.source.is_empty() && b.snow.is_empty());
    }

    #[test]
    fn unknown_section_is_rejected() {
        // Silently ignoring it would hand back tokens the caller believes are resolved.
        let err = parse_database_bindings("source:\n  a: b\nsnowflake:\n  a: b\n").unwrap_err();
        assert!(
            format!("{err}").contains("database-bindings.yml is not valid"),
            "unexpected error: {err}"
        );
    }

    #[test]
    fn malformed_yaml_is_rejected() {
        let err = parse_database_bindings("source: [unclosed").unwrap_err();
        assert!(format!("{err}").contains("database-bindings.yml is not valid"));
    }
}
