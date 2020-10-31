"""empty message

Revision ID: 587cf9ca8592
Revises: 
Create Date: 2020-10-31 00:36:23.030185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '587cf9ca8592'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('current_period', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('demand_scenario_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
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
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('display_name', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('member1', sa.String(length=120), nullable=True),
    sa.Column('member2', sa.String(length=120), nullable=True),
    sa.Column('member3', sa.String(length=120), nullable=True),
    sa.Column('member4', sa.String(length=120), nullable=True),
    sa.Column('member5', sa.String(length=120), nullable=True),
    sa.Column('member6', sa.String(length=120), nullable=True),
    sa.Column('member7', sa.String(length=120), nullable=True),
    sa.Column('member8', sa.String(length=120), nullable=True),
    sa.Column('member9', sa.String(length=120), nullable=True),
    sa.Column('member10', sa.String(length=120), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('money_total', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('display_name')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('userinput',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('produce_quantity', sa.Integer(), nullable=True),
    sa.Column('sell_price', sa.Integer(), nullable=True),
    sa.Column('marketing_costs', sa.Integer(), nullable=True),
    sa.Column('research_and_development_costs', sa.Integer(), nullable=True),
    sa.Column('marketing_research_price', sa.Boolean(), nullable=True),
    sa.Column('marketing_research_sales', sa.Boolean(), nullable=True),
    sa.Column('marketing_research_quality', sa.Boolean(), nullable=True),
    sa.Column('marketing_research_marketing_costs', sa.Boolean(), nullable=True),
    sa.Column('approved_by_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('period',
    sa.Column('id', sa.String(length=64), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('period_number', sa.Integer(), nullable=True),
    sa.Column('userinput_id', sa.String(length=64), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('income_from_sells', sa.Integer(), nullable=True),
    sa.Column('labot_costs', sa.Integer(), nullable=True),
    sa.Column('material_costs', sa.Integer(), nullable=True),
    sa.Column('gross_proffit', sa.Integer(), nullable=True),
    sa.Column('marketing_costs', sa.Integer(), nullable=True),
    sa.Column('research_and_development_costs', sa.Integer(), nullable=True),
    sa.Column('transport_costs', sa.Integer(), nullable=True),
    sa.Column('storage_costs', sa.Integer(), nullable=True),
    sa.Column('administrative_costs', sa.Integer(), nullable=True),
    sa.Column('marketing_research_costs', sa.Integer(), nullable=True),
    sa.Column('interest_costs', sa.Integer(), nullable=True),
    sa.Column('other_costs', sa.Integer(), nullable=True),
    sa.Column('products_sold', sa.Integer(), nullable=True),
    sa.Column('products_in_stock_beggining_of_period', sa.Integer(), nullable=True),
    sa.Column('products_in_stock_end_of_period', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['userinput_id'], ['userinput.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    # ### end Alembic commands ###

    # add default admin
    op.execute('INSERT INTO "user" (id, is_admin, username, email, password_hash) '
               'VALUES (default, TRUE, "admin", "filipov.bogomil@gmal.com", '
               '"pbkdf2:sha256:150000$4cxvcwnI$dd8e2193d11aed58163e6e2fbe57283cf69cb3dd'
               'af24dec0b4ae8b579112bf29");')

    # populate products
    for product in [(1, 'a'), (2, 'b'), (3, 'c')]:
        op.execute(f'INSERT INTO "product" (id) VALUES ({product[0]});')

    # populate scenario
    for product in [1, 2, 3]:
        cost_materials = product + 2
        cost_unpredicted = 1000 if product == 3 else 0

        for period in range(1, 21):
            op.execute('INSERT INTO "scenario" (id, demand_scenario_id, period, product_id, '
                       'demand_quantity, sensitivity_price, sensitivity_quality, sensitivity_marketing, '
                       'correction_cost_labor, correction_cost_materials_for_one_product, '
                       'cost_unpredicted, cost_materials_for_one_product, cost_labor, investment_for_one_marketing, '
                       'investment_for_one_quality, quality_index_min, quality_index_max, marketing_keep_effect, '
                       'base_value_rand_quality, cost_transport, cost_storage, cost_fixed_administrative, '
                       'cost_product_manager, cost_new_product_manager, price_research, interest_credit, '
                       'interest_overdraft, max_price) '
                       f'VALUES (default, 1, {period}, {product}, 3850, 1, 1.05, 0.95, 1, 1, {cost_unpredicted}, '
                       f'{cost_materials}, 5, 200, 1000, 5, 5, 0.5, 0.7, 1.5, 0.5, 5000, 1000, 1500, 500, 0.05, '
                       f'0.1, 50);')
    # populate scenario


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('period')
    op.drop_table('userinput')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('scenario')
    op.drop_table('product')
    op.drop_table('game')
    # ### end Alembic commands ###
