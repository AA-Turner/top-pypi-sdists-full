import logging

from python_agent.common.token.token_data import TokenData
from python_agent.packages import jwt

log = logging.getLogger(__name__)


class TokenParser(object):
    @staticmethod
    def parse_and_validate(raw_token):
        try:
            token_data = (
                jwt.decode(
                    raw_token, algorithms=["RS512"], options={"verify_signature": False}
                )
                or {}
            )
            token_data = TokenData(
                token_data.get("subject"),
                token_data.get("x-sl-role"),
                token_data.get("x-sl-server"),
            )
            TokenParser.validate_data(token_data)
            return token_data, raw_token
        except Exception as e:
            log.error("Failed parsing token. Error: %s" % str(e))
            return TokenData(None, None, None), raw_token

    @staticmethod
    def validate_data(token_data):
        if not token_data.customerId:
            token_data.validation_errors.append(
                Exception("customerId cannot be null or empty")
            )
        if not token_data.role:
            token_data.validation_errors.append(
                Exception("role cannot be null or empty")
            )
        if token_data.role != "agent":
            token_data.validation_errors.append(
                Exception("Expected role: 'agent'. Actual role: '%s'" % token_data.role)
            )
        if not token_data.server:
            token_data.validation_errors.append(
                Exception("server cannot be null or empty")
            )
