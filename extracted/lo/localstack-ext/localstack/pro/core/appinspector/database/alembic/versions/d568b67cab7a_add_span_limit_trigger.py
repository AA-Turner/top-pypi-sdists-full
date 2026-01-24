_A=None
from collections.abc import Sequence
from alembic import op
from localstack.pro.core.appinspector import config
revision:str='d568b67cab7a'
down_revision:str|Sequence[str]|_A='443b451f15d0'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:op.execute(f"""
        CREATE TRIGGER enforce_span_limit
        BEFORE INSERT ON spans
        WHEN NEW.is_write_operation = 1 AND (SELECT COUNT(*) FROM spans WHERE is_write_operation = 1) >= 1000
        BEGIN
            SELECT RAISE(ABORT, '{config.SPANS_TABLE_LIMIT_MESSAGE}');
        END;
    """)
def downgrade()->_A:op.execute('DROP TRIGGER IF EXISTS enforce_span_limit;')