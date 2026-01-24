from fitrequest.decorators.cli_method import cli_method
from fitrequest.decorators.fit import delete, fit, get, patch, post, put
from fitrequest.decorators.hybrid_syntax import hybrid_syntax
from fitrequest.decorators.paginated import AbstractPage, PageDict, paginated
from fitrequest.decorators.retry import retry

__all__ = [
    'AbstractPage',
    'PageDict',
    'cli_method',
    'delete',
    'fit',
    'get',
    'hybrid_syntax',
    'paginated',
    'patch',
    'post',
    'put',
    'retry',
]
