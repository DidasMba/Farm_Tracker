"""Initialized migrations

Revision ID: 276edaf22241
Revises: 
Create Date: 2024-02-23 10:44:30.126104

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '276edaf22241'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('role', sa.String(length=20), nullable=False, server_default='default_value'))

    # ### end Alembic commands ###


def downgrade():
    op.drop_column('user', 'role')
    # ### end Alembic commands ###
