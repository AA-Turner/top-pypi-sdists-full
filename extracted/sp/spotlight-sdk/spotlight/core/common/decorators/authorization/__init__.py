"""
Authenticated request decorators.
"""

from spotlight.core.common.decorators.authorization.asynchronous import (
    async_authenticated_request,
)
from spotlight.core.common.decorators.authorization.synchronous import (
    authenticated_request,
)
