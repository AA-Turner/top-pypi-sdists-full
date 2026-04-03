// MariaDB is MySQL wire protocol compatible
// Reuse MySQL handler

use crate::mysql::MySqlHandler;

/// MariaDB handler - reuses MySQL implementation
///
/// MariaDB uses the same wire protocol as MySQL, so we can reuse the MySQL handler.
pub type MariaDbHandler = MySqlHandler;
