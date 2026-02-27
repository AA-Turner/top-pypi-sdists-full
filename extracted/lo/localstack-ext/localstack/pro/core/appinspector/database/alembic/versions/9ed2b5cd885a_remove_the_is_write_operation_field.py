_E='ix_spans_is_write_operation'
_D='DROP TRIGGER IF EXISTS enforce_span_limit;'
_C='is_write_operation'
_B='spans'
_A=None
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from localstack.pro.core.appinspector import config
revision:str='9ed2b5cd885a'
down_revision:str|Sequence[str]|_A='7eed698e1759'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:op.execute(_D);op.execute(f"""
        CREATE TRIGGER enforce_span_limit
        BEFORE INSERT ON spans
        WHEN (SELECT COUNT(*) FROM spans) >= 1000
        BEGIN
            SELECT RAISE(ABORT, '{config.SPANS_TABLE_LIMIT_MESSAGE}');
        END;
    """);op.drop_index(op.f(_E),table_name=_B);op.drop_column(_B,_C)
def downgrade()->_A:A=False;op.add_column(_B,sa.Column(_C,sa.Boolean(),nullable=A,default=A,comment='If the operation triggering the span is a write operation, e.g., PutObject, Invoke, etc.'));op.create_index(op.f(_E),_B,[_C],unique=A);op.execute(_D);op.execute(f"""
        CREATE TRIGGER enforce_span_limit
        BEFORE INSERT ON spans
        WHEN NEW.is_write_operation = 1 AND (SELECT COUNT(*) FROM spans WHERE is_write_operation = 1) >= 1000
        BEGIN
            SELECT RAISE(ABORT, '{config.SPANS_TABLE_LIMIT_MESSAGE}');
        END;
    """)