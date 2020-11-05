"""empty message

Revision ID: 6dee8a8ca653
Revises: a08349bb4da6
Create Date: 2020-11-05 20:39:45.722531

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6dee8a8ca653'
down_revision = 'a08349bb4da6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('period_total', 'credit_total_begining_of_period')
    op.drop_column('period_total', 'credit_total_end_of_period')
    op.drop_column('period_total', 'overdraft_total_end_of_period')
    op.drop_column('period_total', 'overdraft_total_begining_of_period')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('period_total', sa.Column('overdraft_total_begining_of_period', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('period_total', sa.Column('overdraft_total_end_of_period', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('period_total', sa.Column('credit_total_end_of_period', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('period_total', sa.Column('credit_total_begining_of_period', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
