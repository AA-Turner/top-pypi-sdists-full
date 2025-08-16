from enum import Enum


class GetScriptByPathResponse200Language(str, Enum):
    ANSIBLE = "ansible"
    BASH = "bash"
    BIGQUERY = "bigquery"
    BUN = "bun"
    CSHARP = "csharp"
    DENO = "deno"
    DUCKDB = "duckdb"
    GO = "go"
    GRAPHQL = "graphql"
    JAVA = "java"
    MSSQL = "mssql"
    MYSQL = "mysql"
    NATIVETS = "nativets"
    NU = "nu"
    ORACLEDB = "oracledb"
    PHP = "php"
    POSTGRESQL = "postgresql"
    POWERSHELL = "powershell"
    PYTHON3 = "python3"
    RUBY = "ruby"
    RUST = "rust"
    SNOWFLAKE = "snowflake"

    def __str__(self) -> str:
        return str(self.value)
