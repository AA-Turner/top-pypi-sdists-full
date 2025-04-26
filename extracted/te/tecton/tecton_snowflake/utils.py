import random
import string

import sqlparse


def generate_random_name() -> str:
    return "".join(random.choice(string.ascii_uppercase) for i in range(20))


def format_sql(sql_str: str) -> str:
    return sqlparse.format(sql_str, reindent=True)
