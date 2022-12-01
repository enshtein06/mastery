"""create activities table

Revision ID: f631546e7b02
Revises: 
Create Date: 2022-11-30 19:36:58.914180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f631546e7b02'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("activities", sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("activities")
    pass
