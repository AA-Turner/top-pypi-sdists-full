_C='linked_span_ids'
_B='span_links'
_A=None
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.sqlite import JSON
revision:str='7eed698e1759'
down_revision:str|Sequence[str]|_A='f7a3c9b8d5e2'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:F='CASCADE';E='spans.span_id';D='linked_span_id';C='span_id';B=False;A=True;op.create_table(_B,sa.Column('id',sa.Integer(),primary_key=A,autoincrement=A,comment='The unique identifier for the span link.'),sa.Column(C,sa.TEXT(),nullable=B,index=A,comment='The span_id of the source span.'),sa.Column('trace_id',sa.TEXT(),nullable=B,index=A,comment='The trace_id of the source span for efficient querying.'),sa.Column(D,sa.TEXT(),nullable=B,index=A,comment='The span_id of the linked span.'),sa.Column('linked_trace_id',sa.TEXT(),nullable=B,index=A,comment='The trace_id of the linked span for efficient querying.'),sa.ForeignKeyConstraint([C],[E],ondelete=F),sa.ForeignKeyConstraint([D],[E],ondelete=F));op.add_column('spans',sa.Column(_C,JSON,nullable=A,comment='A JSON array of span_ids that this span links to (denormalized for quick access).'))
def downgrade()->_A:op.drop_column('spans',_C);op.drop_table(_B)