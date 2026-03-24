_A=None
from collections.abc import Sequence
import sqlalchemy as sa
from alembic import op
revision:str='f7a3c9b8d5e2'
down_revision:str|Sequence[str]|_A='d568b67cab7a'
branch_labels:str|Sequence[str]|_A=_A
depends_on:str|Sequence[str]|_A=_A
def upgrade()->_A:B='event_type';A='events';op.add_column(A,sa.Column(B,sa.TEXT(),nullable=True,comment="The type of event (e.g., 'iam.policy_evaluation'). Extracted from attributes.event.type for efficient filtering."));op.create_index(op.f('ix_events_event_type'),A,[B],unique=False);op.execute("\n        UPDATE events\n        SET event_type = json_extract(attributes, '$.event.type')\n        WHERE attributes IS NOT NULL\n          AND json_extract(attributes, '$.event.type') IS NOT NULL\n    ")
def downgrade()->_A:0