_A=None
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import sqlite
revision:str='e8f9a12c6d4b'
down_revision:str|Sequence[str]|_A='d568b67cab7a'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:
	with op.batch_alter_table('spans',schema=_A)as A:A.add_column(sa.Column('links',sqlite.JSON(),nullable=True,comment='A JSON array of span IDs that this span is linked to.'))
def downgrade()->_A:
	with op.batch_alter_table('spans',schema=_A)as A:A.drop_column('links')