use crate::odbc::{
    build_connection_string, is_sql_modifying_command, redact_connection_string, OdbcConfig,
    OdbcHandler,
};
use guacr_handlers::ProtocolHandler;
use std::collections::HashMap;

#[test]
fn test_odbc_handler_new() {
    let handler = OdbcHandler::with_defaults();
    assert_eq!(<OdbcHandler as ProtocolHandler>::name(&handler), "odbc");
}

#[test]
fn test_odbc_config() {
    let config = OdbcConfig::default();
    assert_eq!(config.default_port, 5432);
}

#[test]
fn test_build_connection_string_dsn() {
    let mut params = HashMap::new();
    params.insert("dsn".to_string(), "MyDSN".to_string());
    params.insert("username".to_string(), "admin".to_string());
    params.insert("password".to_string(), "secret".to_string());

    let result = build_connection_string(&params, 5432);
    assert_eq!(result, "DSN=MyDSN;UID=admin;PWD=secret");
}

#[test]
fn test_build_connection_string_raw() {
    let mut params = HashMap::new();
    params.insert(
        "connection-string".to_string(),
        "DRIVER={PostgreSQL};SERVER=db.example.com;PORT=5432".to_string(),
    );

    let result = build_connection_string(&params, 5432);
    assert_eq!(
        result,
        "DRIVER={PostgreSQL};SERVER=db.example.com;PORT=5432"
    );
}

#[test]
fn test_build_connection_string_components() {
    let mut params = HashMap::new();
    params.insert("driver".to_string(), "IBM DB2 ODBC DRIVER".to_string());
    params.insert("hostname".to_string(), "db2.example.com".to_string());
    params.insert("port".to_string(), "50000".to_string());
    params.insert("database".to_string(), "SAMPLE".to_string());
    params.insert("username".to_string(), "db2admin".to_string());
    params.insert("password".to_string(), "password123".to_string());

    let result = build_connection_string(&params, 5432);
    assert_eq!(
        result,
        "DRIVER={IBM DB2 ODBC DRIVER};SERVER=db2.example.com;\
         PORT=50000;DATABASE=SAMPLE;UID=db2admin;PWD=password123"
    );
}

#[test]
fn test_build_connection_string_defaults() {
    let params = HashMap::new();
    let result = build_connection_string(&params, 5432);
    assert_eq!(
        result,
        "DRIVER={PostgreSQL};SERVER=localhost;PORT=5432;DATABASE=;UID=;PWD="
    );
}

#[test]
fn test_dsn_priority_over_components() {
    // When DSN is provided, it should take priority over hostname/port/etc.
    let mut params = HashMap::new();
    params.insert("dsn".to_string(), "MyDSN".to_string());
    params.insert("hostname".to_string(), "ignored.example.com".to_string());
    params.insert("port".to_string(), "9999".to_string());
    params.insert("username".to_string(), "user".to_string());
    params.insert("password".to_string(), "pass".to_string());

    let result = build_connection_string(&params, 5432);
    assert!(result.starts_with("DSN=MyDSN"));
    assert!(!result.contains("ignored.example.com"));
    assert!(!result.contains("9999"));
}

#[test]
fn test_connection_string_priority_over_components() {
    // When connection-string is provided (but no DSN), it takes priority
    let mut params = HashMap::new();
    params.insert(
        "connection-string".to_string(),
        "DRIVER={Custom};SERVER=custom.host".to_string(),
    );
    params.insert("hostname".to_string(), "ignored.example.com".to_string());

    let result = build_connection_string(&params, 5432);
    assert_eq!(result, "DRIVER={Custom};SERVER=custom.host");
}

#[test]
fn test_redact_connection_string() {
    let conn = "DRIVER={PostgreSQL};SERVER=localhost;PWD=supersecret;UID=admin";
    let redacted = redact_connection_string(conn);
    assert!(redacted.contains("PWD=***"));
    assert!(!redacted.contains("supersecret"));
    assert!(redacted.contains("UID=admin"));
}

#[test]
fn test_redact_connection_string_pwd_at_end() {
    let conn = "DRIVER={PostgreSQL};UID=admin;PWD=supersecret";
    let redacted = redact_connection_string(conn);
    assert!(redacted.contains("PWD=***"));
    assert!(!redacted.contains("supersecret"));
}

#[test]
fn test_redact_no_password() {
    let conn = "DRIVER={PostgreSQL};SERVER=localhost;UID=admin";
    let redacted = redact_connection_string(conn);
    assert_eq!(redacted, conn);
}

#[test]
fn test_is_sql_modifying_command() {
    // Modifying commands
    assert!(is_sql_modifying_command("INSERT INTO t VALUES (1)"));
    assert!(is_sql_modifying_command("UPDATE t SET x = 1"));
    assert!(is_sql_modifying_command("DELETE FROM t"));
    assert!(is_sql_modifying_command("DROP TABLE t"));
    assert!(is_sql_modifying_command("TRUNCATE TABLE t"));
    assert!(is_sql_modifying_command("ALTER TABLE t ADD col INT"));
    assert!(is_sql_modifying_command("CREATE TABLE t (id INT)"));
    assert!(is_sql_modifying_command("GRANT SELECT ON t TO user1"));
    assert!(is_sql_modifying_command("REVOKE SELECT ON t FROM user1"));
    assert!(is_sql_modifying_command(
        "MERGE INTO t USING s ON t.id=s.id"
    ));
    assert!(is_sql_modifying_command("EXEC sp_my_procedure"));
    assert!(is_sql_modifying_command("EXECUTE my_proc"));
    assert!(is_sql_modifying_command("CALL my_proc()"));
    assert!(is_sql_modifying_command("UPSERT INTO t VALUES (1)"));
    assert!(is_sql_modifying_command("REPLACE INTO t VALUES (1)"));
    assert!(is_sql_modifying_command("RENAME TABLE t TO t2"));

    // Case insensitive
    assert!(is_sql_modifying_command("  insert INTO t VALUES (1)"));
    assert!(is_sql_modifying_command("  Delete FROM t"));

    // Non-modifying commands
    assert!(!is_sql_modifying_command("SELECT * FROM t"));
    assert!(!is_sql_modifying_command("SHOW TABLES"));
    assert!(!is_sql_modifying_command("DESCRIBE t"));
    assert!(!is_sql_modifying_command("EXPLAIN SELECT 1"));
    assert!(!is_sql_modifying_command("USE mydb"));
    assert!(!is_sql_modifying_command("SET search_path TO public"));
}

#[test]
fn test_prompt_with_database() {
    let database = "mydb";
    let read_only = false;
    let prompt = if !database.is_empty() {
        if read_only {
            format!("odbc [{}] [RO]> ", database)
        } else {
            format!("odbc [{}]> ", database)
        }
    } else {
        "odbc> ".to_string()
    };
    assert_eq!(prompt, "odbc [mydb]> ");
}

#[test]
fn test_prompt_with_read_only() {
    let database = "mydb";
    let read_only = true;
    let prompt = if !database.is_empty() {
        if read_only {
            format!("odbc [{}] [RO]> ", database)
        } else {
            format!("odbc [{}]> ", database)
        }
    } else if read_only {
        "odbc [RO]> ".to_string()
    } else {
        "odbc> ".to_string()
    };
    assert_eq!(prompt, "odbc [mydb] [RO]> ");
}

#[test]
fn test_prompt_without_database() {
    let database = "";
    let read_only = false;
    let prompt = if !database.is_empty() {
        format!("odbc [{}]> ", database)
    } else if read_only {
        "odbc [RO]> ".to_string()
    } else {
        "odbc> ".to_string()
    };
    assert_eq!(prompt, "odbc> ");
}

#[test]
fn test_prompt_read_only_without_database() {
    let database = "";
    let read_only = true;
    let prompt = if !database.is_empty() {
        if read_only {
            format!("odbc [{}] [RO]> ", database)
        } else {
            format!("odbc [{}]> ", database)
        }
    } else if read_only {
        "odbc [RO]> ".to_string()
    } else {
        "odbc> ".to_string()
    };
    assert_eq!(prompt, "odbc [RO]> ");
}

#[test]
fn test_build_connection_string_dsn_empty_credentials() {
    let mut params = HashMap::new();
    params.insert("dsn".to_string(), "MyDSN".to_string());

    let result = build_connection_string(&params, 5432);
    assert_eq!(result, "DSN=MyDSN;UID=;PWD=");
}

#[test]
fn test_build_connection_string_sap_hana() {
    let mut params = HashMap::new();
    params.insert("driver".to_string(), "HDBODBC".to_string());
    params.insert("hostname".to_string(), "hana.example.com".to_string());
    params.insert("port".to_string(), "30015".to_string());
    params.insert("database".to_string(), "HDB".to_string());
    params.insert("username".to_string(), "SYSTEM".to_string());
    params.insert("password".to_string(), "Manager1".to_string());

    let result = build_connection_string(&params, 5432);
    assert!(result.contains("DRIVER={HDBODBC}"));
    assert!(result.contains("SERVER=hana.example.com"));
    assert!(result.contains("PORT=30015"));
    assert!(result.contains("DATABASE=HDB"));
}

#[test]
fn test_build_connection_string_teradata() {
    let mut params = HashMap::new();
    params.insert(
        "driver".to_string(),
        "Teradata Database ODBC Driver 17.20".to_string(),
    );
    params.insert("hostname".to_string(), "td.example.com".to_string());
    params.insert("port".to_string(), "1025".to_string());
    params.insert("database".to_string(), "DBC".to_string());
    params.insert("username".to_string(), "dbc".to_string());
    params.insert("password".to_string(), "dbc".to_string());

    let result = build_connection_string(&params, 5432);
    assert!(result.contains("DRIVER={Teradata Database ODBC Driver 17.20}"));
    assert!(result.contains("SERVER=td.example.com"));
    assert!(result.contains("PORT=1025"));
}

#[test]
fn test_build_connection_string_db2() {
    let mut params = HashMap::new();
    params.insert("driver".to_string(), "IBM DB2 ODBC DRIVER".to_string());
    params.insert("hostname".to_string(), "db2.example.com".to_string());
    params.insert("port".to_string(), "50000".to_string());
    params.insert("database".to_string(), "SAMPLE".to_string());
    params.insert("username".to_string(), "db2inst1".to_string());
    params.insert("password".to_string(), "ibmdb2".to_string());

    let result = build_connection_string(&params, 5432);
    assert!(result.contains("DRIVER={IBM DB2 ODBC DRIVER}"));
    assert!(result.contains("PORT=50000"));
    assert!(result.contains("DATABASE=SAMPLE"));
}
