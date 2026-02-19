from datetime import datetime, timedelta

from adam.config import Config
from adam.utils_log import log_exc
from adam.utils_rdbms.athena import Athena
from adam.commands.audit.utils_audits import Audits
from adam.utils_context import NULL

def run_configured_query(config_key: str, args: list[str], ctx = NULL):
    limit, date_condition = extract_limit_and_duration(args)
    if query := Config().get(config_key, None):
        query = '\n    '.join(query.split('\n'))
        query = query.replace('{date_condition}', date_condition)
        query = query.replace('{limit}', str(limit))

        ctx.log2(query)
        ctx.log2()
        Athena.run_query(query, ctx=ctx)

def extract_limit_and_duration(args: list[str]) -> tuple[int, datetime]:
    limit = 10
    _from = datetime.now() - timedelta(days=30)
    if args:
        with log_exc():
            limit = int(args[0])

        if len(args) > 2 and args[1] == 'over':
            if args[2] == 'day':
                _from = datetime.now() - timedelta(days=1)

    return (limit, Audits.date_from(_from))