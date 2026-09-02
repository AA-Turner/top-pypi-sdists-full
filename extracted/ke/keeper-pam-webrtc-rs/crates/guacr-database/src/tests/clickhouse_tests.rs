use crate::clickhouse::ClickHouseHandler;
use guacr_handlers::ProtocolHandler;

#[test]
fn test_clickhouse_handler_new() {
    let handler = ClickHouseHandler::with_defaults();
    assert_eq!(
        <ClickHouseHandler as ProtocolHandler>::name(&handler),
        "clickhouse"
    );
}

#[test]
fn test_clickhouse_as_event_based() {
    let handler = ClickHouseHandler::with_defaults();
    assert!(<ClickHouseHandler as ProtocolHandler>::as_event_based(&handler).is_some());
}
