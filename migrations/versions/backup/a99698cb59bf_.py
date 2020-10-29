"""empty message

Revision ID: a99698cb59bf
Revises: 62bcb007a722
Create Date: 2020-10-11 17:48:34.760549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a99698cb59bf'
down_revision = '62bcb007a722'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('period', sa.Column('in_stock_product_a', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('in_stock_product_b', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('in_stock_product_c', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('price_product_a', sa.Numeric(), nullable=True))
    op.add_column('period', sa.Column('price_product_b', sa.Numeric(), nullable=True))
    op.add_column('period', sa.Column('price_product_c', sa.Numeric(), nullable=True))
    op.add_column('period', sa.Column('product_a_produced', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('product_a_sold', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('product_b_produced', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('product_b_sold', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('product_c_produced', sa.Integer(), nullable=True))
    op.add_column('period', sa.Column('product_c_sold', sa.Integer(), nullable=True))
    op.drop_column('period', 'product_B_produced')
    op.drop_column('period', 'product_A_produced')
    op.drop_column('period', 'in_stock_product_A')
    op.drop_column('period', 'in_stock_product_C')
    op.drop_column('period', 'price_product_B')
    op.drop_column('period', 'price_product_A')
    op.drop_column('period', 'product_B_sold')
    op.drop_column('period', 'in_stock_product_B')
    op.drop_column('period', 'price_product_C')
    op.drop_column('period', 'product_A_sold')
    op.drop_column('period', 'product_C_produced')
    op.drop_column('period', 'product_C_sold')
    op.add_column('user', sa.Column('product_a_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('product_b_count', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('product_c_count', sa.Integer(), nullable=True))
    op.drop_column('user', 'product_A_count')
    op.drop_column('user', 'product_B_count')
    op.drop_column('user', 'product_C_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('product_C_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('product_B_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('user', sa.Column('product_A_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('user', 'product_c_count')
    op.drop_column('user', 'product_b_count')
    op.drop_column('user', 'product_a_count')
    op.add_column('period', sa.Column('product_C_sold', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('product_C_produced', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('product_A_sold', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('price_product_C', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('in_stock_product_B', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('product_B_sold', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('price_product_A', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('price_product_B', sa.NUMERIC(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('in_stock_product_C', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('in_stock_product_A', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('product_A_produced', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('period', sa.Column('product_B_produced', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('period', 'product_c_sold')
    op.drop_column('period', 'product_c_produced')
    op.drop_column('period', 'product_b_sold')
    op.drop_column('period', 'product_b_produced')
    op.drop_column('period', 'product_a_sold')
    op.drop_column('period', 'product_a_produced')
    op.drop_column('period', 'price_product_c')
    op.drop_column('period', 'price_product_b')
    op.drop_column('period', 'price_product_a')
    op.drop_column('period', 'in_stock_product_c')
    op.drop_column('period', 'in_stock_product_b')
    op.drop_column('period', 'in_stock_product_a')
    # ### end Alembic commands ###