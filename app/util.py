from app import app, db
from app.models import Userinput, PeriodTotal, ScenarioPerProduct, ScenarioPerPeriod


def reset_userinput_product(userinput):
    userinput.produce_quantity = 0
    userinput.sell_price = 10
    userinput.marketing_costs = 0
    userinput.research_and_development_costs = 0
    userinput.marketing_research_price = False
    userinput.marketing_research_sales = False
    userinput.marketing_research_quality = False
    userinput.marketing_research_marketing_costs = False


def reset_userinput_period(period_total):
    period_total.take_credit = 0
    period_total.deposit_overdraft = 0


def reset_userinputs():
    """
    Resets inputs for all users in all games. Use carefully.
    """
    inputs = Userinput.query.all()
    for i in inputs:
        _reset_userinput_product(i)
        db.session.add(i)

    for pt in PeriodTotal.query.all():
        _reset_userinput_period(pt)
        db.session.add(pt)
    db.session.commit()


def populate_scenarios(periods, demand_scenario_id):
    for period in range(1, periods):
        sp = ScenarioPerPeriod()
        sp.demand_scenario_id = demand_scenario_id
        sp.period = period
        sp.cost_fixed_administrative = 5000
        sp.interest_credit = 0.02
        sp.interest_overdraft = 0.1
        db.session.add(sp)
        db.session.commit()

        for prod in range(1, 4):
            s = ScenarioPerProduct()

            s.demand_scenario_id = demand_scenario_id
            s.period = period
            s.product_id = prod

            print(f'Adding scenario for period {period}, product {prod}')
            s.demand_quantity = 3850
            s.sensitivity_price = 1
            s.sensitivity_quality = 1.05
            s.sensitivity_marketing = 0.95
            s.correction_cost_labor = 1
            s.correction_cost_materials_for_one_product = 1
            s.cost_unpredicted = 0
            s.cost_materials_for_one_product = s.product_id+2
            s.cost_labor = 5
            s.investment_for_one_marketing = 200
            s.investment_for_one_quality = 1000
            s.quality_index_min = 2
            s.quality_index_max = 5
            s.marketing_index_min = 2
            s.marketing_index_max = 5
            s.marketing_keep_effect = 0.5
            s.base_value_rand_quality = 0.7
            s.cost_transport = 1.5
            s.cost_storage = 0.5
            s.cost_product_manager = 1000
            s.cost_new_product_manager = 1500
            s.price_research = 500
            s.max_price = 50
            db.session.add(s)
            db.session.commit()





