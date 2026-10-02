//! Canonical name computation for code unit metadata.
//!
//! A canonical name is a dot-separated identifier built from a code unit's
//! metadata fields: `database.schema.name` (or `database.schema.package.name`
//! when a package is present) for most object types, or with a
//! `(TYPE,TYPE,...)` suffix for procedures and functions (using base parameter
//! types with length/precision stripped).
//!
//! Two public entry points:
//! - [`compute`] — low-level, accepts individual fields
//! - [`for_code_unit`] — convenience wrapper that extracts fields from a [`CodeUnit`]

use crate::generated::types::{CodeUnit, ObjectType, ParameterDef};

/// Sentinel schema name used when a database is present but no schema
/// is specified. Consumers should be aware this value may appear in
/// canonical names for incompletely-specified metadata.
pub const UNKNOWN_SCHEMA: &str = "UNKNOWN_SCHEMA";

/// Target platform is always Snowflake; baked into target canonical names.
const TARGET_PLATFORM: &str = "snowflake";

/// Selects which side of the code unit metadata to use.
///
/// A [`CodeUnit`] has one shared `signature` block containing both source
/// and target type information on each parameter. `Side` controls which
/// type field is read: `type_` for [`Source`](Side::Source), `target_type`
/// for [`Target`](Side::Target).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Side {
    /// Use source metadata and source parameter types (`type_` field).
    Source,
    /// Use target metadata and target parameter types (`target_type` field).
    Target,
}

/// Compute a canonical name from individual metadata fields.
///
/// Returns `None` when `name` is `None` and `object_type` is not a
/// container type (`Database` or `Schema`).
///
/// `params` comes from the shared `signature.parameters.arguments` array.
/// Each [`ParameterDef`] carries both source (`type_`) and target
/// (`target_type`) types; `side` selects which one to use.
///
/// # Format
///
/// - `database.schema.package.name` — when all four parts are present
/// - `database.schema.name` — when package is absent
/// - `schema.name` — when database is missing
/// - `package.name` — when database and schema are missing but package is present
/// - `name` — when database, schema, and package are all missing
/// - Append `(TYPE,TYPE,...)` for `Procedure` and `Function` object types
/// - If database is present but schema is missing, [`UNKNOWN_SCHEMA`] is
///   substituted, except for the top-level container types `Database` and
///   `Schema`. A schema is itself a child of a database — it has no parent
///   schema slot — so `Schema` follows the same rule as `Database`: an
///   absent `schema` field is omitted rather than replaced with the
///   placeholder. A `schema` value, when explicitly provided, is still
///   honored.
pub fn compute(
    database: Option<&str>,
    schema: Option<&str>,
    package: Option<&str>,
    name: Option<&str>,
    object_type: Option<&ObjectType>,
    params: Option<&[ParameterDef]>,
    side: Side,
) -> Option<String> {
    let is_container = matches!(object_type, Some(ObjectType::Database | ObjectType::Schema));

    if name.is_none() && !is_container {
        return None;
    }

    let mut parts: Vec<&str> = Vec::new();

    if let Some(database) = database {
        parts.push(database);
        match object_type {
            Some(ObjectType::Database) => {}
            Some(ObjectType::Schema) => {
                if let Some(schema) = schema {
                    parts.push(schema);
                }
            }
            _ => parts.push(schema.unwrap_or(UNKNOWN_SCHEMA)),
        }
    } else if let Some(schema) = schema {
        parts.push(schema);
    }

    if let Some(package) = package {
        parts.push(package);
    }

    if let Some(name) = name {
        parts.push(name);
    }

    let mut canonical = parts.join(".");

    let needs_signature = matches!(
        object_type,
        Some(ObjectType::Procedure | ObjectType::Function)
    );
    if needs_signature {
        if let Some(params) = params {
            let param_types: Vec<&str> = params
                .iter()
                .filter_map(|param| {
                    let raw_type = match side {
                        Side::Source => param.type_.as_deref(),
                        Side::Target => param.target_type.as_deref(),
                    };
                    raw_type.map(strip_type_precision)
                })
                .collect();
            if !param_types.is_empty() {
                canonical.push('(');
                canonical.push_str(&param_types.join(","));
                canonical.push(')');
            }
        }
    }

    Some(canonical)
}

/// Compute the canonical name for one side of a [`CodeUnit`].
///
/// Shape varies by `kind`:
/// - `Script`, `Etl`: source uses `"{platform}:{format}:{path}"` from
///   `files.source.path`; target always uses `"snowflake:{format}:{path}"`
///   from `files.converted.path`.
/// - `Custom`: `"{customKind}:[database.][schema.][package.]name"` when a
///   name is set; otherwise falls back to `"{customKind}:{path}"` from
///   `files.source.path` (source side) or `files.converted.path` (target side).
/// - `DatabaseObject` (or unspecified):
///   `database.schema[.package].name[(paramTypes)]`, via [`compute`].
///
/// Each side is computed independently and may be `None` — a generated
/// unit has no source side; a pre-conversion unit has no target side.
pub fn for_code_unit(unit: &CodeUnit, side: Side) -> Option<String> {
    use crate::generated::types::Kind;
    match unit.kind.as_ref() {
        Some(Kind::Script | Kind::Etl) => compute_path_based_canonical_name(unit, side),
        Some(Kind::Custom) => compute_custom_canonical_name(unit, side),
        _ => compute_database_object_canonical_name(unit, side),
    }
}

fn compute_custom_canonical_name(unit: &CodeUnit, side: Side) -> Option<String> {
    let (custom_kind, database, schema, package, name, file_path) = match side {
        Side::Source => {
            let s = unit.source.as_ref()?;
            (
                s.custom_kind.as_deref()?,
                s.database.as_deref(),
                s.schema.as_deref(),
                s.package.as_deref(),
                s.name.as_deref(),
                unit.files
                    .as_ref()
                    .and_then(|f| f.source.as_ref())
                    .and_then(|f| f.path.as_deref()),
            )
        }
        Side::Target => {
            let t = unit.target.as_ref()?;
            (
                t.custom_kind.as_deref()?,
                t.database.as_deref(),
                t.schema.as_deref(),
                None,
                t.name.as_deref(),
                unit.files
                    .as_ref()
                    .and_then(|f| f.converted.as_ref())
                    .and_then(|f| f.path.as_deref()),
            )
        }
    };

    if let Some(name) = name {
        let mut parts: Vec<&str> = Vec::new();
        if let Some(db) = database {
            parts.push(db);
        }
        if let Some(s) = schema {
            parts.push(s);
        }
        if let Some(p) = package {
            parts.push(p);
        }
        parts.push(name);
        Some(format!("{custom_kind}:{}", parts.join(".")))
    } else {
        let path = file_path?;
        Some(format!("{custom_kind}:{path}"))
    }
}

fn compute_path_based_canonical_name(unit: &CodeUnit, side: Side) -> Option<String> {
    let files = unit.files.as_ref()?;
    match side {
        Side::Source => {
            let s = unit.source.as_ref()?;
            let platform = s.platform.as_ref()?;
            let format = s.format.as_ref()?;
            let path = files.source.as_ref()?.path.as_deref()?;
            Some(format!("{platform}:{format}:{path}"))
        }
        Side::Target => {
            let t = unit.target.as_ref()?;
            let format = t.format.as_ref()?;
            let path = files.converted.as_ref()?.path.as_deref()?;
            Some(format!("{TARGET_PLATFORM}:{format}:{path}"))
        }
    }
}

fn compute_database_object_canonical_name(unit: &CodeUnit, side: Side) -> Option<String> {
    let (database, schema, package, name, object_type) = match side {
        Side::Source => {
            let s = unit.source.as_ref()?;
            (
                s.database.as_deref(),
                s.schema.as_deref(),
                s.package.as_deref(),
                s.name.as_deref(),
                s.object_type.as_ref(),
            )
        }
        Side::Target => {
            let t = unit.target.as_ref()?;
            (
                t.database.as_deref(),
                t.schema.as_deref(),
                None,
                t.name.as_deref(),
                t.object_type.as_ref(),
            )
        }
    };

    let params = unit
        .signature
        .as_ref()
        .and_then(|s| s.parameters.as_ref())
        .map(|p| p.arguments.as_slice());

    compute(database, schema, package, name, object_type, params, side)
}

/// Strip length/precision qualifiers from a SQL type.
///
/// `"NVARCHAR(50)"` → `"NVARCHAR"`, `"INT"` → `"INT"`.
fn strip_type_precision(ty: &str) -> &str {
    match ty.find('(') {
        Some(pos) => &ty[..pos],
        None => ty,
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::generated::types::{
        FileEntry, Files, Kind, Parameters, Signature, SourceFormat, SourceMetadata,
        SourcePlatform, TargetFormat, TargetMetadata,
    };
    use test_case::test_case;

    /// `(platform, format, path)` for one side of a path-based code unit.
    /// Each field is independently `Option` so missing-input tests can drop
    /// individual values.
    type SideTriple<'a> = (Option<&'a str>, Option<&'a str>, Option<&'a str>);

    /// Build a path-based-canonical-name code unit (`Script` or `Etl`).
    /// Pass `None` for a side to omit the entire side; pass an inner
    /// `None` to omit a single field.
    fn path_based_unit<'a>(
        kind: Kind,
        source: Option<SideTriple<'a>>,
        target: Option<SideTriple<'a>>,
    ) -> CodeUnit {
        let opt = |s: Option<&str>| s.map(String::from);
        let opt_source_platform =
            |s: Option<&str>| s.and_then(|s| s.parse::<SourcePlatform>().ok());
        let opt_source_format = |s: Option<&str>| s.and_then(|s| s.parse::<SourceFormat>().ok());
        let opt_target_format = |s: Option<&str>| s.and_then(|s| s.parse::<TargetFormat>().ok());
        let files = (source.is_some() || target.is_some()).then(|| Files {
            source: source.map(|(_, _, path)| FileEntry {
                path: opt(path),
                ..Default::default()
            }),
            converted: target.map(|(_, _, path)| FileEntry {
                path: opt(path),
                ..Default::default()
            }),
            ..Default::default()
        });
        CodeUnit {
            kind: Some(kind),
            source: source.map(|(p, f, _)| SourceMetadata {
                platform: opt_source_platform(p),
                format: opt_source_format(f),
                ..Default::default()
            }),
            target: target.map(|(_, f, _)| TargetMetadata {
                format: opt_target_format(f),
                ..Default::default()
            }),
            files,
            ..Default::default()
        }
    }

    /// Build `Vec<ParameterDef>` from `(source_type, target_type)` pairs.
    fn make_params(specs: &[(&str, &str)]) -> Vec<ParameterDef> {
        specs
            .iter()
            .map(|(src, tgt)| ParameterDef {
                type_: Some((*src).to_string()),
                target_type: Some((*tgt).to_string()),
                ..Default::default()
            })
            .collect()
    }

    // `compute()` shape variations with no parameter signature. Covers
    // every combination of present/absent (database, schema, name) plus
    // each container `ObjectType` (Database, Schema) and the
    // "missing-name on non-container returns None" rule.
    #[test_case(Some("DB"),   Some("dbo"),   None,           Some("MyTable"), ObjectType::Table,     Some("DB.dbo.MyTable")              ; "table fully qualified")]
    #[test_case(Some("DB"),   Some("dbo"),   None,           Some("AuditLog"), ObjectType::TemporalTable, Some("DB.dbo.AuditLog")        ; "temporal table fully qualified")]
    #[test_case(None,         Some("dbo"),   None,           Some("Orphan"),  ObjectType::Table,     Some("dbo.Orphan")                  ; "schema and name, no database")]
    #[test_case(None,         None,          None,           Some("Lonely"),  ObjectType::Table,     Some("Lonely")                      ; "name only")]
    #[test_case(Some("MyDB"), None,          None,           Some("Widget"),  ObjectType::Table,     Some("MyDB.UNKNOWN_SCHEMA.Widget")  ; "database without schema falls back to UNKNOWN_SCHEMA")]
    #[test_case(Some("DB"),   Some("dbo"),   None,           None,            ObjectType::Table,     None                                ; "missing name on non-container returns None")]
    #[test_case(Some("MyDB"), None,          None,           None,            ObjectType::Database,  Some("MyDB")                        ; "Database object type uses database only")]
    #[test_case(Some("MyDB"), Some("Sales"), None,           None,            ObjectType::Schema,    Some("MyDB.Sales")                  ; "Schema object type with schema field set")]
    #[test_case(None,         Some("Sales"), None,           None,            ObjectType::Schema,    Some("Sales")                       ; "Schema object type, schema field only")]
    #[test_case(Some("WWI"),  None,          None,           Some("Website"), ObjectType::Schema,    Some("WWI.Website")                 ; "Schema object type with schema name in name field omits UNKNOWN_SCHEMA placeholder")]
    #[test_case(Some("MyDB"), None,          None,           None,            ObjectType::Schema,    Some("MyDB")                        ; "Schema object type with only database does not insert UNKNOWN_SCHEMA")]
    #[test_case(Some("DB"),   Some("dbo"),   None,           Some("NoArgs"),  ObjectType::Procedure, Some("DB.dbo.NoArgs")               ; "procedure with no params omits parens")]
    #[test_case(Some("DB"),   Some("dbo"),   Some("PKG"),    Some("MyProc"),  ObjectType::Procedure, Some("DB.dbo.PKG.MyProc")           ; "package inserted between schema and name")]
    #[test_case(None,         Some("dbo"),   Some("PKG"),    Some("MyProc"),  ObjectType::Procedure, Some("dbo.PKG.MyProc")              ; "package with schema, no database")]
    #[test_case(None,         None,          Some("PKG"),    Some("MyProc"),  ObjectType::Procedure, Some("PKG.MyProc")                  ; "package only, no database or schema")]
    #[test_case(Some("DB"),   None,          Some("PKG"),    Some("T"),       ObjectType::Table,     Some("DB.UNKNOWN_SCHEMA.PKG.T")     ; "package with database but no schema uses UNKNOWN_SCHEMA")]
    fn compute_without_params(
        database: Option<&str>,
        schema: Option<&str>,
        package: Option<&str>,
        name: Option<&str>,
        object_type: ObjectType,
        expected: Option<&str>,
    ) {
        let result = compute(
            database,
            schema,
            package,
            name,
            Some(&object_type),
            None,
            Side::Source,
        );
        assert_eq!(result.as_deref(), expected);
    }

    // `compute()` parameter-signature variations. The `(database, schema,
    // name)` envelope is fixed at `("DB", "dbo", "MyProc")` because these
    // tests are about the signature-rendering behavior — `Side` selecting
    // source vs target types, type-precision stripping, and parameter
    // suppression for non-callable object types.
    #[test_case(
        None,
        ObjectType::Procedure,
        &[("DATETIME", "TIMESTAMP_NTZ"), ("NVARCHAR(50)", "VARCHAR(50)")],
        Side::Source,
        "DB.dbo.MyProc(DATETIME,NVARCHAR)" ;
        "procedure source-side types, precision stripped"
    )]
    #[test_case(
        None,
        ObjectType::Procedure,
        &[("DATETIME", "TIMESTAMP_NTZ"), ("NVARCHAR(50)", "VARCHAR(50)")],
        Side::Target,
        "DB.dbo.MyProc(TIMESTAMP_NTZ,VARCHAR)" ;
        "procedure target-side types, precision stripped"
    )]
    #[test_case(
        None,
        ObjectType::Function,
        &[("INT", "NUMBER")],
        Side::Source,
        "DB.dbo.MyProc(INT)" ;
        "function with single param"
    )]
    #[test_case(
        None,
        ObjectType::View,
        &[("INT", "NUMBER")],
        Side::Source,
        "DB.dbo.MyProc" ;
        "view ignores params (no parens)"
    )]
    #[test_case(
        Some("PKG"),
        ObjectType::Procedure,
        &[("DATETIME", "TIMESTAMP_NTZ")],
        Side::Source,
        "DB.dbo.PKG.MyProc(DATETIME)" ;
        "procedure with package and params"
    )]
    fn compute_with_params(
        package: Option<&str>,
        object_type: ObjectType,
        param_specs: &[(&str, &str)],
        side: Side,
        expected: &str,
    ) {
        let params = make_params(param_specs);
        let result = compute(
            Some("DB"),
            Some("dbo"),
            package,
            Some("MyProc"),
            Some(&object_type),
            Some(&params),
            side,
        );
        assert_eq!(result.as_deref(), Some(expected));
    }

    #[test]
    fn strip_type_precision_works() {
        assert_eq!(strip_type_precision("NVARCHAR(50)"), "NVARCHAR");
        assert_eq!(strip_type_precision("DECIMAL(18,2)"), "DECIMAL");
        assert_eq!(strip_type_precision("INT"), "INT");
        assert_eq!(strip_type_precision("TIMESTAMP_NTZ"), "TIMESTAMP_NTZ");
    }

    #[test]
    fn for_code_unit_source() {
        let unit = CodeUnit {
            source: Some(SourceMetadata {
                object_type: Some(ObjectType::Table),
                database: Some("DB".to_string()),
                schema: Some("dbo".to_string()),
                name: Some("Orders".to_string()),
                ..Default::default()
            }),
            ..Default::default()
        };
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("DB.dbo.Orders")
        );
    }

    #[test]
    fn for_code_unit_target() {
        let unit = CodeUnit {
            target: Some(TargetMetadata {
                object_type: Some(ObjectType::Table),
                database: Some("DB".to_string()),
                schema: Some("DBO".to_string()),
                name: Some("ORDERS".to_string()),
                ..Default::default()
            }),
            ..Default::default()
        };
        assert_eq!(
            for_code_unit(&unit, Side::Target).as_deref(),
            Some("DB.DBO.ORDERS")
        );
    }

    #[test]
    fn for_code_unit_source_with_package() {
        let unit = CodeUnit {
            source: Some(SourceMetadata {
                object_type: Some(ObjectType::Procedure),
                database: Some("DB".to_string()),
                schema: Some("dbo".to_string()),
                package: Some("PKG_REVENUE".to_string()),
                name: Some("GetTotal".to_string()),
                ..Default::default()
            }),
            ..Default::default()
        };
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("DB.dbo.PKG_REVENUE.GetTotal")
        );
    }

    #[test]
    fn for_code_unit_with_signature() {
        let unit = CodeUnit {
            source: Some(SourceMetadata {
                object_type: Some(ObjectType::Procedure),
                database: Some("DB".to_string()),
                schema: Some("dbo".to_string()),
                name: Some("MyProc".to_string()),
                ..Default::default()
            }),
            signature: Some(Signature {
                parameters: Some(Parameters {
                    arguments: vec![ParameterDef {
                        type_: Some("DATETIME".to_string()),
                        target_type: Some("TIMESTAMP_NTZ".to_string()),
                        ..Default::default()
                    }],
                    ..Default::default()
                }),
                ..Default::default()
            }),
            ..Default::default()
        };
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("DB.dbo.MyProc(DATETIME)")
        );
        assert_eq!(
            for_code_unit(&unit, Side::Target),
            None,
            "target metadata is None, should return None"
        );
    }

    #[test]
    fn for_code_unit_no_metadata() {
        let unit = CodeUnit::default();
        assert_eq!(for_code_unit(&unit, Side::Source), None);
        assert_eq!(for_code_unit(&unit, Side::Target), None);
    }

    // Path-based composition is shared by `Script` and `Etl`. Each
    // happy-path test also asserts that the absent side returns `None`,
    // which exercises the per-side independence invariant (D18).

    #[test_case(Kind::Script, "teradata", "bteq", "source/etl/x.bteq" ; "script")]
    #[test_case(Kind::Etl, "ssis", "dtsx", "source/Pipelines/CustomerETL.dtsx" ; "etl")]
    fn for_code_unit_path_based_source_only(kind: Kind, platform: &str, format: &str, path: &str) {
        let unit = path_based_unit(kind, Some((Some(platform), Some(format), Some(path))), None);
        assert_eq!(
            for_code_unit(&unit, Side::Source),
            Some(format!("{platform}:{format}:{path}")),
        );
        assert_eq!(for_code_unit(&unit, Side::Target), None);
    }

    #[test_case(
        Kind::Script, "python",
        "converted/helpers/snowconvert_helpers/__init__.py" ;
        "script (e.g. generated helper)"
    )]
    #[test_case(
        Kind::Etl, "snowflakeScripting",
        "converted/etl/loaders/CustomerLoad.sql" ;
        "etl"
    )]
    fn for_code_unit_path_based_target_only(kind: Kind, format: &str, path: &str) {
        let unit = path_based_unit(kind, None, Some((None, Some(format), Some(path))));
        assert_eq!(for_code_unit(&unit, Side::Source), None);
        assert_eq!(
            for_code_unit(&unit, Side::Target),
            Some(format!("{TARGET_PLATFORM}:{format}:{path}")),
        );
    }

    #[test_case(None, Some("bteq"), Some("source/x.bteq") ; "missing platform")]
    #[test_case(Some("teradata"), None, Some("source/x.bteq") ; "missing format")]
    #[test_case(Some("teradata"), Some("bteq"), None ; "missing path")]
    fn for_code_unit_path_based_source_returns_none_when_input_missing(
        platform: Option<&str>,
        format: Option<&str>,
        path: Option<&str>,
    ) {
        let unit = path_based_unit(Kind::Script, Some((platform, format, path)), None);
        assert_eq!(for_code_unit(&unit, Side::Source), None);
    }

    // ── Custom canonical names ──────────────────────────────────────────

    fn custom_unit(
        source: Option<SourceMetadata>,
        target: Option<TargetMetadata>,
        files: Option<Files>,
    ) -> CodeUnit {
        CodeUnit {
            kind: Some(Kind::Custom),
            source,
            target,
            files,
            ..Default::default()
        }
    }

    #[test]
    fn custom_canonical_name_uses_custom_kind_and_name() {
        let unit = custom_unit(
            Some(SourceMetadata {
                custom_kind: Some("fivetran".into()),
                name: Some("orders_sync".into()),
                ..Default::default()
            }),
            None,
            None,
        );
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("fivetran:orders_sync"),
        );
    }

    #[test]
    fn custom_canonical_name_includes_database_and_schema_when_present() {
        let unit = custom_unit(
            Some(SourceMetadata {
                custom_kind: Some("oraclePackage".into()),
                database: Some("HR".into()),
                schema: Some("APP".into()),
                package: Some("PKG_PAYROLL".into()),
                name: Some("compute_bonus".into()),
                ..Default::default()
            }),
            None,
            None,
        );
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("oraclePackage:HR.APP.PKG_PAYROLL.compute_bonus"),
        );
    }

    #[test]
    fn custom_canonical_name_falls_back_to_path_when_name_missing() {
        let unit = custom_unit(
            Some(SourceMetadata {
                custom_kind: Some("ssasCube".into()),
                ..Default::default()
            }),
            None,
            Some(Files {
                source: Some(FileEntry {
                    path: Some("source/cubes/Sales.bim".into()),
                    ..Default::default()
                }),
                ..Default::default()
            }),
        );
        assert_eq!(
            for_code_unit(&unit, Side::Source).as_deref(),
            Some("ssasCube:source/cubes/Sales.bim"),
        );
    }

    #[test]
    fn custom_canonical_name_target_side_uses_target_metadata() {
        let unit = custom_unit(
            None,
            Some(TargetMetadata {
                custom_kind: Some("dbtModel".into()),
                schema: Some("ANALYTICS".into()),
                name: Some("stg_orders".into()),
                ..Default::default()
            }),
            None,
        );
        assert_eq!(
            for_code_unit(&unit, Side::Target).as_deref(),
            Some("dbtModel:ANALYTICS.stg_orders"),
        );
    }

    #[test]
    fn custom_canonical_name_returns_none_without_kind() {
        let unit = custom_unit(
            Some(SourceMetadata {
                name: Some("orders_sync".into()),
                ..Default::default()
            }),
            None,
            None,
        );
        assert_eq!(for_code_unit(&unit, Side::Source), None);
    }
}
