_A=None
from collections.abc import Sequence
from alembic import op
revision:str='9ed2b5cd885a'
down_revision:str|Sequence[str]|_A='7eed698e1759'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:A='spans';op.execute('DROP TRIGGER IF EXISTS enforce_span_limit;');op.execute("\n        CREATE TRIGGER enforce_span_limit\n        BEFORE INSERT ON spans\n        WHEN (SELECT COUNT(*) FROM spans) >= 1000\n        BEGIN\n            SELECT RAISE(ABORT, 'The Spans table is limited to 1000 rows.');\n        END;\n    ");op.drop_index(op.f('ix_spans_is_write_operation'),table_name=A);op.drop_column(A,'is_write_operation')
def downgrade()->_A:0