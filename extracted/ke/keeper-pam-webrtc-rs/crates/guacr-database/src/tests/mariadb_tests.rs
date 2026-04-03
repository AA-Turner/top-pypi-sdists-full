use crate::mariadb::MariaDbHandler;

#[test]
fn test_mariadb_is_mysql_compatible() {
    let handler = MariaDbHandler::with_defaults();
    // MariaDB uses same handler, but will be registered as "mariadb"
    assert_eq!(
        <_ as guacr_handlers::ProtocolHandler>::name(&handler),
        "mysql"
    );
}
