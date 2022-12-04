"""add column activities table

Revision ID: de667d1646df
Revises: 
Create Date: 2022-12-03 17:33:34.098977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de667d1646df'
down_revision = None
branch_labels = None
depends_on = None


# Using this file just as an example of alembic usage
def upgrade() -> None:
    op.add_column("activities", sa.Column("just_to_see" , sa.String(), default="just_to_see"))
    pass


def downgrade() -> None:
    op.drop_column("actitivies", "just_to_see")
    pass
