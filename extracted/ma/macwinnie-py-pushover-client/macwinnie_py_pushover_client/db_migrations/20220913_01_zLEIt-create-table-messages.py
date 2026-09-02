"""
CREATE TABLE messages
"""

# Using [yoyo-migrations](https://pypi.org/project/yoyo-migrations/) – has to
# be executed on DB initiating like in [macwinnie_sqlite3](https://macwinnie.github.io/py-sqlite3)
from yoyo import step

__depends__ = {}

steps = [step("""
        CREATE TABLE po_messages (
            id           INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
            message      TEXT     NOT NULL,
            priority     INTEGER  NOT NULL DEFAULT 0,
            expire       INTEGER           DEFAULT NULL,
            retry        INTEGER           DEFAULT NULL,
            api_rc       INTEGER           DEFAULT NULL,
            title        VARCHAR(512)      DEFAULT NULL,
            url          VARCHAR(2048)     DEFAULT NULL,
            url_title    VARCHAR(512)      DEFAULT NULL,
            receipt      VARCHAR(256)      DEFAULT NULL,
            receipt_info TEXT              DEFAULT NULL,
            created      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            confirmation DATETIME          DEFAULT NULL
        );
    """)]
