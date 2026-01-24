_D='ix_events_event_type'
_C='event_type'
_B='events'
_A=None
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
revision:str='f7a3c9b8d5e2'
down_revision:str|Sequence[str]|_A='e8f9a12c6d4b'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:op.add_column(_B,sa.Column(_C,sa.TEXT(),nullable=True,comment="The type of event (e.g., 'iam.policy_evaluation'). Extracted from attributes.event.type for efficient filtering."));op.create_index(op.f(_D),_B,[_C],unique=False);op.execute("\n        UPDATE events\n        SET event_type = json_extract(attributes, '$.event.type')\n        WHERE attributes IS NOT NULL\n          AND json_extract(attributes, '$.event.type') IS NOT NULL\n    ")
def downgrade()->_A:op.drop_index(op.f(_D),table_name=_B);op.drop_column(_B,_C)