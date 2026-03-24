_A=None
from collections.abc import Sequence
from alembic import op
revision:str='5e9f8ae22116'
down_revision:str|Sequence[str]|_A='9ed2b5cd885a'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:op.execute('DROP TRIGGER IF EXISTS enforce_span_limit;')
def downgrade()->_A:0