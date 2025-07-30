import logging
import re
from pathlib import Path
from typing import TYPE_CHECKING

import mysql.connector

if TYPE_CHECKING:
    from canonmap.services.database.mysql.adapters.connection import MySQLConfig

logger = logging.getLogger(__name__)


def _test_connection_util(mysql_config: "MySQLConfig") -> bool:
    """Attempt a short-timeout connect; try socket first (if set), then TCP; return True on first success, False on final failure."""
    base_args = {
        "user": mysql_config.user,
        "password": mysql_config.password,
        "database": mysql_config.database,
        "connection_timeout": 5,
        "raise_on_warnings": True,
    }
    socket_helper = tcp_helper = None

    # 1. Try UNIX socket
    if mysql_config.unix_socket:
        args = base_args.copy()
        args["unix_socket"] = mysql_config.unix_socket
        try:
            logger.info(f"Trying UNIX socket connection: {args}")
            conn = mysql.connector.connect(**args)
            conn.close()
            logger.info("MySQL socket connection succeeded")
            return True
        except mysql.connector.Error as e:
            errno = getattr(e, "errno", None)
            msg = getattr(e, "msg", str(e))
            if errno == 1045:
                match = re.search(r"@'([^']+)'", msg)
                host_part = match.group(1) if match else '%'
                socket_helper = (
                    f"Access denied for user '{mysql_config.user}'@'{host_part}'.\n"
                    f"Connection parameters:\n"
                    f"  user: {mysql_config.user}\n"
                    f"  database: {mysql_config.database or '<none>'}\n"
                    f"  unix_socket: {mysql_config.unix_socket}\n"
                    "Your MySQL user isn't authorized to connect via the proxy socket.\n"
                    "Run the following in your Cloud SQL instance to grant access:\n"
                    f"GRANT ALL PRIVILEGES ON {mysql_config.database or '*'}.* TO '{mysql_config.user}'@'{host_part}' IDENTIFIED BY '{mysql_config.password}';\n"
                    "Or use gcloud:\n"
                    f"gcloud sql users set-password {mysql_config.user} --instance=<INSTANCE_NAME> --host='{host_part}' --password='{mysql_config.password}'"
                )
            else:
                socket_helper = (
                    f"Socket error (errno={errno}): {msg}\n"
                    f"Connection parameters:\n"
                    f"  user: {mysql_config.user}\n"
                    f"  database: {mysql_config.database or '<none>'}\n"
                    f"  unix_socket: {mysql_config.unix_socket}\n"
                    "Ensure the Cloud SQL Auth Proxy is running and that the socket path is correct."
                )
            logger.error(socket_helper)

    # 2. Try TCP host/port
    if mysql_config.host and mysql_config.port:
        args = base_args.copy()
        args["host"] = mysql_config.host
        args["port"] = mysql_config.port
        try:
            logger.info(f"Trying TCP connection: {args}")
            conn = mysql.connector.connect(**args)
            conn.close()
            logger.info("MySQL TCP connection succeeded")
            return True
        except mysql.connector.Error as e:
            msg = getattr(e, 'msg', str(e))
            tcp_helper = (
                f"TCP error (errno={getattr(e,'errno',None)}): {msg}\n"
                f"Ensure host '{mysql_config.host}' and port {mysql_config.port} are reachable and not blocked by firewall."
            )
            logger.error(tcp_helper)

    # 3. Neither succeeded
    combined = ""
    if socket_helper:
        combined += socket_helper + "\n"
    if tcp_helper:
        combined += tcp_helper + "\n"
    if not combined:
        combined = "No socket or host/port configuration provided for MySQL connection."

    # Write troubleshooting file if requested
    if mysql_config.create_troubleshooting_txts:
        helpers_dir = Path(".canonmap_helpers")
        helpers_dir.mkdir(exist_ok=True)
        file_path = helpers_dir / "mysql_troubleshooting.txt"
        file_path.write_text(combined)
        logger.info(f"Wrote troubleshooting guidance to {file_path.resolve()}")

    return False

