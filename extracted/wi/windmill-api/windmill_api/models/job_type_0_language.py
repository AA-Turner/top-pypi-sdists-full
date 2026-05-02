from enum import Enum


class JobType0Language(str, Enum):
    ANSIBLE = "ansible"
    BASH = "bash"
    BIGQUERY = "bigquery"
    BUN = "bun"
    BUNNATIVE = "bunnative"
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
    RLANG = "rlang"
    RUBY = "ruby"
    RUST = "rust"
    SNOWFLAKE = "snowflake"

    def __str__(self) -> str:
        return str(self.value)
