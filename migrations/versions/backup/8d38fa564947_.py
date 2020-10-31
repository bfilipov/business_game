"""empty message

Revision ID: 8d38fa564947
Revises: 049f048fb336
Create Date: 2020-10-29 23:12:10.929835

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d38fa564947'
down_revision = '049f048fb336'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scenario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('demand_scenario_id', sa.Integer(), nullable=True),
    sa.Column('period', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('demand_quantity', sa.Integer(), nullable=True),
    sa.Column('sensitivity_price', sa.Float(), nullable=True),
    sa.Column('sensitivity_quality', sa.Float(), nullable=True),
    sa.Column('sensitivity_marketing', sa.Float(), nullable=True),
    sa.Column('correction_cost_labor', sa.Float(), nullable=True),
    sa.Column('correction_cost_materials_for_one_product', sa.Float(), nullable=True),
    sa.Column('cost_unpredicted', sa.Integer(), nullable=True),
    sa.Column('cost_materials_for_one_product', sa.Float(), nullable=True),
    sa.Column('cost_labor', sa.Float(), nullable=True),
    sa.Column('investment_for_one_marketing', sa.Integer(), nullable=True),
    sa.Column('investment_for_one_quality', sa.Integer(), nullable=True),
    sa.Column('quality_index_min', sa.Float(), nullable=True),
    sa.Column('quality_index_max', sa.Float(), nullable=True),
    sa.Column('marketing_keep_effect', sa.Float(), nullable=True),
    sa.Column('base_value_rand_quality', sa.Float(), nullable=True),
    sa.Column('cost_transport', sa.Float(), nullable=True),
    sa.Column('cost_storage', sa.Float(), nullable=True),
    sa.Column('cost_fixed_administrative', sa.Integer(), nullable=True),
    sa.Column('cost_product_manager', sa.Integer(), nullable=True),
    sa.Column('cost_new_product_manager', sa.Integer(), nullable=True),
    sa.Column('price_research', sa.Integer(), nullable=True),
    sa.Column('interest_credit', sa.Float(), nullable=True),
    sa.Column('interest_overdraft', sa.Float(), nullable=True),
    sa.Column('max_price', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('demand')
    op.drop_column('period', 'approved')
    op.add_column('user', sa.Column('display_name', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member1', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member10', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member2', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member3', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member4', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member5', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member6', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member7', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member8', sa.String(length=120), nullable=True))
    op.add_column('user', sa.Column('member9', sa.String(length=120), nullable=True))
    op.create_unique_constraint(None, 'user', ['display_name'])
    op.add_column('userinput', sa.Column('approved_by_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('userinput', 'approved_by_admin')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'member9')
    op.drop_column('user', 'member8')
    op.drop_column('user', 'member7')
    op.drop_column('user', 'member6')
    op.drop_column('user', 'member5')
    op.drop_column('user', 'member4')
    op.drop_column('user', 'member3')
    op.drop_column('user', 'member2')
    op.drop_column('user', 'member10')
    op.drop_column('user', 'member1')
    op.drop_column('user', 'display_name')
    op.add_column('period', sa.Column('approved', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_table('demand',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('demand_scenario_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('period', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('demand_A', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('demand_B', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('demand_C', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='demand_pkey')
    )
    op.drop_table('scenario')
    # ### end Alembic commands ###
