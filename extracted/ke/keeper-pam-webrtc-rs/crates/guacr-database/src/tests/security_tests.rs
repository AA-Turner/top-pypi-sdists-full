use crate::security::{
    check_csv_export_allowed, check_csv_import_allowed, check_query_allowed, classify_query,
    DatabaseSecuritySettings, QueryType,
};
use guacr_handlers::{
    is_mysql_export_query, is_mysql_import_query, is_postgres_copy_in, is_postgres_copy_out,
};
use std::collections::HashMap;

#[test]
fn test_classify_query_readonly() {
    assert_eq!(classify_query("SELECT * FROM users"), QueryType::ReadOnly);
    assert_eq!(classify_query("  select id from t"), QueryType::ReadOnly);
    assert_eq!(classify_query("SHOW DATABASES"), QueryType::ReadOnly);
    assert_eq!(classify_query("DESCRIBE users"), QueryType::ReadOnly);
    assert_eq!(classify_query("DESC users"), QueryType::ReadOnly);
    assert_eq!(classify_query("EXPLAIN SELECT 1"), QueryType::ReadOnly);
    assert_eq!(classify_query("USE database_name"), QueryType::ReadOnly);
}

#[test]
fn test_classify_query_modifying() {
    assert_eq!(
        classify_query("INSERT INTO users VALUES (1)"),
        QueryType::Modifying
    );
    assert_eq!(
        classify_query("UPDATE users SET name='x'"),
        QueryType::Modifying
    );
    assert_eq!(classify_query("DELETE FROM users"), QueryType::Modifying);
    assert_eq!(classify_query("DROP TABLE users"), QueryType::Modifying);
    assert_eq!(
        classify_query("ALTER TABLE users ADD col INT"),
        QueryType::Modifying
    );
    assert_eq!(
        classify_query("CREATE TABLE new_table (id INT)"),
        QueryType::Modifying
    );
    assert_eq!(classify_query("TRUNCATE TABLE users"), QueryType::Modifying);
    assert_eq!(
        classify_query("GRANT SELECT ON users TO 'user'"),
        QueryType::Modifying
    );
}

#[test]
fn test_check_query_allowed_readonly_mode() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    let settings = DatabaseSecuritySettings::from_params(&params);

    assert!(check_query_allowed("SELECT * FROM users", &settings).is_ok());
    assert!(check_query_allowed("INSERT INTO users VALUES (1)", &settings).is_err());
    assert!(check_query_allowed("DROP TABLE users", &settings).is_err());
}

#[test]
fn test_check_query_allowed_normal_mode() {
    let settings = DatabaseSecuritySettings::default();

    assert!(check_query_allowed("SELECT * FROM users", &settings).is_ok());
    assert!(check_query_allowed("INSERT INTO users VALUES (1)", &settings).is_ok());
    assert!(check_query_allowed("DROP TABLE users", &settings).is_ok());
}

#[test]
fn test_from_params() {
    let mut params = HashMap::new();
    params.insert("read-only".to_string(), "true".to_string());
    params.insert("disable-copy".to_string(), "1".to_string());
    params.insert("disable-csv-export".to_string(), "true".to_string());

    let settings = DatabaseSecuritySettings::from_params(&params);

    assert!(settings.base.read_only);
    assert!(settings.base.disable_copy);
    assert!(!settings.base.disable_paste);
    assert!(settings.disable_csv_export);
    assert!(!settings.disable_csv_import);
}

#[test]
fn test_csv_export_import_allowed() {
    let mut params = HashMap::new();
    params.insert("disable-csv-export".to_string(), "true".to_string());
    let settings = DatabaseSecuritySettings::from_params(&params);

    assert!(check_csv_export_allowed(&settings).is_err());
    assert!(check_csv_import_allowed(&settings).is_ok());

    // read-only mode blocks import too
    let mut params2 = HashMap::new();
    params2.insert("read-only".to_string(), "true".to_string());
    let settings2 = DatabaseSecuritySettings::from_params(&params2);
    assert!(check_csv_import_allowed(&settings2).is_err());
}

#[test]
fn test_mysql_export_detection() {
    assert!(is_mysql_export_query(
        "SELECT * FROM users INTO OUTFILE '/tmp/users.csv'"
    ));
    assert!(is_mysql_export_query(
        "SELECT * FROM users INTO LOCAL OUTFILE 'users.csv'"
    ));
    assert!(!is_mysql_export_query("SELECT * FROM users"));
}

#[test]
fn test_mysql_import_detection() {
    assert!(is_mysql_import_query(
        "LOAD DATA INFILE '/tmp/users.csv' INTO TABLE users"
    ));
    assert!(is_mysql_import_query(
        "LOAD LOCAL DATA INFILE 'users.csv' INTO TABLE users"
    ));
    assert!(!is_mysql_import_query("SELECT * FROM users"));
}

#[test]
fn test_postgres_copy_detection() {
    assert!(is_postgres_copy_out("COPY users TO STDOUT"));
    assert!(is_postgres_copy_in("COPY users FROM STDIN"));
    assert!(!is_postgres_copy_out("COPY users FROM STDIN"));
    assert!(!is_postgres_copy_in("COPY users TO STDOUT"));
}

// ============================================================================
// Credential supply gate — check_credential_supply_allowed for database handlers
//
// SqlHandler::connect() calls check_credential_supply_allowed(&security.base)
// before connecting to the database.  These tests validate that the gate
// function correctly controls access based on the allow-supply-user parameter.
// ============================================================================

/// When allow-supply-user is absent (default false), the credential supply gate
/// must return Err.  Database connections always carry username + password, so
/// this gate fires unconditionally in connect().
#[test]
fn test_db_credential_supply_blocked_when_flag_absent() {
    use guacr_handlers::check_credential_supply_allowed;

    let params: HashMap<String, String> = HashMap::new();
    // allow-supply-user is absent — default is false
    let settings = DatabaseSecuritySettings::from_params(&params);
    let result = check_credential_supply_allowed(&settings.base);
    assert!(
        result.is_err(),
        "credential supply gate must return Err when allow-supply-user is absent"
    );
}

/// When allow-supply-user=false, the credential supply gate must return Err.
#[test]
fn test_db_credential_supply_blocked_when_flag_false() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "false".to_string());
    let settings = DatabaseSecuritySettings::from_params(&params);
    let result = check_credential_supply_allowed(&settings.base);
    assert!(
        result.is_err(),
        "credential supply gate must return Err when allow-supply-user=false"
    );
}

/// When allow-supply-user=true, the credential supply gate must return Ok —
/// the connection record explicitly authorises runtime credential supply.
#[test]
fn test_db_credential_supply_allowed_when_flag_true() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "true".to_string());
    let settings = DatabaseSecuritySettings::from_params(&params);
    let result = check_credential_supply_allowed(&settings.base);
    assert!(
        result.is_ok(),
        "credential supply gate must return Ok when allow-supply-user=true: {:?}",
        result.err()
    );
}

/// Numeric form allow-supply-user=1 must also be treated as true.
#[test]
fn test_db_credential_supply_allowed_numeric_one() {
    use guacr_handlers::check_credential_supply_allowed;

    let mut params = HashMap::new();
    params.insert("allow-supply-user".to_string(), "1".to_string());
    let settings = DatabaseSecuritySettings::from_params(&params);
    let result = check_credential_supply_allowed(&settings.base);
    assert!(
        result.is_ok(),
        "allow-supply-user=1 must be treated as true: {:?}",
        result.err()
    );
}
