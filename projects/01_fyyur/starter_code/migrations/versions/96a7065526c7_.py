"""empty message

Revision ID: 96a7065526c7
Revises: d3de086f1f53
Create Date: 2021-05-19 09:29:37.288628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '96a7065526c7'
down_revision = 'd3de086f1f53'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('show_id', sa.Integer(), nullable=False))
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'venue_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shows', 'artist_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('shows', 'show_id')
    # ### end Alembic commands ###
