_A=None
from collections.abc import Sequence
from alembic import op
revision:str='d568b67cab7a'
down_revision:str|Sequence[str]|_A='443b451f15d0'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:op.execute("\n        CREATE TRIGGER enforce_span_limit\n        BEFORE INSERT ON spans\n        WHEN NEW.is_write_operation = 1 AND (SELECT COUNT(*) FROM spans WHERE is_write_operation = 1) >= 1000\n        BEGIN\n            SELECT RAISE(ABORT, 'The Spans table is limited to 100 rows.');\n        END;\n    ")
def downgrade()->_A:0