import logging

from project.core.setup_logging import setup_logging
from project.sqlalchemy_db_.sqlalchemy_db import get_cached_sqlalchemy_db
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM, ApiKeyDBM, UserTokenDBM

_logger = logging.getLogger(__name__)


def create_first_data_for_api():
    with get_cached_sqlalchemy_db().new_session() as session:
        user_dbm = (
            session
            .query(UserDBM)
            .filter(UserDBM.roles.any(UserDBM.Roles.admin))
            .first()
        )
        if user_dbm is None:
            user_dbm = UserDBM(
                username="admin",
                roles=[UserDBM.Roles.client, UserDBM.Roles.admin],
                password="admin",
            )
            session.add(user_dbm)
            session.commit()
            _logger.info("admin was created")

            user_token_dbm = (
                session
                .query(UserTokenDBM)
                .filter(UserTokenDBM.user_id == user_dbm.id)
                .first()
            )
            if user_token_dbm is None:
                user_token_dbm = UserTokenDBM(
                    value="1",
                    user_id=user_dbm.id
                )
                session.add(user_token_dbm)
                session.commit()
                _logger.info("admin token was created")

        api_key_dbm = (
            session
            .query(ApiKeyDBM)
            .first()
        )
        if api_key_dbm is None:
            api_key_dbm = ApiKeyDBM(
                value="1",
                title="First api key"
            )
            session.add(api_key_dbm)
            session.commit()
            _logger.info("api key was created")


def command():
    setup_logging()
    create_first_data_for_api()


if __name__ == '__main__':
    command()
