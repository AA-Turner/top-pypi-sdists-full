# canonmap/services/database/mysql/utils/connect.py
import logging
from typing import TYPE_CHECKING

import mysql.connector
import sys
import os

from canonmap.services.database.mysql.utils.sql_connection_method import MySQLConnectionMethod

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from canonmap.services.database.mysql.config import MySQLConfig

def _connect_util(mysql_config: "MySQLConfig", **kwargs) -> mysql.connector.MySQLConnection:
    """Create and return a MySQL connection using the configured parameters.
    
    Args:
        **kwargs: Additional connection parameters to override defaults
        
    Returns:
        mysql.connector.MySQLConnection: Active MySQL connection
        
    Raises:
        mysql.connector.Error: If connection fails
        ValueError: If no valid connection method is configured
    """
    logger.info(f"Starting MySQL connection with method: {mysql_config.connection_method}")
    
    base_args = {
        "user": mysql_config.user,
        "password": mysql_config.password,
        "database": mysql_config.database,
        "raise_on_warnings": True,
        "allow_local_infile": True,
    }
    
    # Apply any additional kwargs
    if kwargs:
        logger.debug(f"Applying additional connection parameters: {list(kwargs.keys())}")
        base_args.update(kwargs)
    
    # Determine connection method
    if mysql_config.connection_method == MySQLConnectionMethod.SOCKET:
        if not mysql_config.unix_socket:
            logger.error("Socket connection method requires unix_socket to be set")
            raise ValueError("Socket connection method requires unix_socket to be set")
        
        args = base_args.copy()
        args["unix_socket"] = mysql_config.unix_socket
        logger.info(f"Attempting UNIX socket connection to: {mysql_config.unix_socket}")
        logger.debug(f"Socket connection args: user={mysql_config.user}, database={mysql_config.database}")
        
        try:
            conn = mysql.connector.connect(**args)
            logger.info("UNIX socket connection established successfully")
            return conn
        except mysql.connector.errors.InterfaceError as e:
            logger.error(f"UNIX socket interface error: {e}")
            logger.error("Could not reach the MySQL socket file. Try these steps:")
            logger.error(f"  1. Verify the socket path exists and matches the proxy's output: {mysql_config.unix_socket}")
            logger.error(f"  2. Ensure the Cloud SQL Proxy is running and bound to that socket: cloud-sql-proxy --unix-socket={os.path.dirname(mysql_config.unix_socket)} {os.path.basename(mysql_config.unix_socket)}")
            logger.error("  3. Check proxy logs for any startup issues or permission errors")
            logger.error("  4. Confirm your local user has read/write permissions on the socket directory")
            logger.error("  5. If you see authentication errors (invalid_grant), re-authenticate ADC: gcloud auth application-default login")
            logger.error("  6. Or use a service account key: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
            logger.error("  7. Ensure the Cloud SQL Admin API is enabled: gcloud services enable sqladmin.googleapis.com")
            sys.exit("Error: Could not reach the MySQL socket file. Exiting.")
        except mysql.connector.Error as e:
            logger.error(f"UNIX socket connection failed: {e}")
            logger.error(f"  1. Ensure the Cloud SQL Proxy is running with: cloud-sql-proxy --unix-socket={os.path.dirname(mysql_config.unix_socket)} {os.path.basename(mysql_config.unix_socket)}")
            logger.error("  2. If using user credentials, re-authenticate ADC:")
            logger.error("       gcloud auth application-default login")
            logger.error("  3. Or use a service account JSON key:")
            logger.error("       export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
            logger.error("  4. Verify the Cloud SQL Admin API is enabled:")
            logger.error("       gcloud services enable sqladmin.googleapis.com")
            logger.error("  5. Check file permissions on the socket path and ensure your user can read/write it")
            sys.exit("Error: Could not connect via UNIX socket. Exiting.")
        
    elif mysql_config.connection_method == MySQLConnectionMethod.TCP:
        if not mysql_config.host:
            logger.error("TCP connection method requires host to be set")
            raise ValueError("TCP connection method requires host to be set")
        
        args = base_args.copy()
        args["host"] = mysql_config.host
        args["port"] = mysql_config.port
        logger.info(f"Attempting TCP connection to: {mysql_config.host}:{mysql_config.port}")
        logger.debug(f"TCP connection args: user={mysql_config.user}, database={mysql_config.database}")
        
        try:
            conn = mysql.connector.connect(**args)
            logger.info("TCP connection established successfully")
            return conn
        except mysql.connector.Error as e:
            logger.error(f"TCP connection failed: {e}")
            raise
        
    elif mysql_config.connection_method == MySQLConnectionMethod.AUTO:
        logger.info("Using AUTO connection method - will try socket first, then TCP")
        
        # Try socket first if available, then TCP
        if mysql_config.unix_socket:
            try:
                args = base_args.copy()
                args["unix_socket"] = mysql_config.unix_socket
                logger.info(f"Auto: Attempting UNIX socket connection to: {mysql_config.unix_socket}")
                conn = mysql.connector.connect(**args)
                logger.info("Auto: UNIX socket connection established successfully")
                return conn
            except mysql.connector.errors.InterfaceError as e:
                logger.error(f"Auto: UNIX socket interface error: {e}")
                logger.error("Auto: Could not reach the MySQL socket file. Try these steps:")
                logger.error(f"  1. Verify the socket path exists and matches the proxy's output: {mysql_config.unix_socket}")
                logger.error(f"  2. Ensure the Cloud SQL Proxy is running and bound to that socket: cloud-sql-proxy --unix-socket={os.path.dirname(mysql_config.unix_socket)} {os.path.basename(mysql_config.unix_socket)}")
                logger.error("  3. Check proxy logs for any startup issues or permission errors")
                logger.error("  4. Confirm your local user has read/write permissions on the socket directory")
                logger.error("  5. If you see authentication errors (invalid_grant), re-authenticate ADC: gcloud auth application-default login")
                logger.error("  6. Or use a service account key: export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json")
                logger.error("  7. Ensure the Cloud SQL Admin API is enabled: gcloud services enable sqladmin.googleapis.com")
                sys.exit("Error: Could not reach the MySQL socket file (AUTO mode). Exiting.")
            except mysql.connector.Error as e:
                logger.warning(f"Auto: UNIX socket connection failed: {e}")
                if mysql_config.host:
                    logger.info("Auto: Falling back to TCP connection")
                else:
                    logger.error("Auto: Socket failed and no TCP host configured")
                    sys.exit("Error: UNIX socket failed and no TCP host configured. Exiting.")
                
        if mysql_config.host:
            args = base_args.copy()
            args["host"] = mysql_config.host
            args["port"] = mysql_config.port
            logger.info(f"Auto: Attempting TCP connection to: {mysql_config.host}:{mysql_config.port}")
            
            try:
                conn = mysql.connector.connect(**args)
                logger.info("Auto: TCP connection established successfully")
                return conn
            except mysql.connector.Error as e:
                logger.error(f"Auto: TCP connection failed: {e}")
                sys.exit("Error: Could not establish TCP connection. Exiting.")
            
        logger.error("Auto connection method requires either unix_socket or host to be set")
        sys.exit("Error: AUTO connection mode requires unix_socket or host to be set. Exiting.")
    
    else:
        logger.error(f"Unknown connection method: {mysql_config.connection_method}")
        sys.exit(f"Error: Unknown connection method: {mysql_config.connection_method}. Exiting.")
