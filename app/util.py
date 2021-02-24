from app import app, db
from app.models import Userinput, PeriodTotal


def _reset_userinput_product(userinput):
    userinput.produce_quantity = 0
    userinput.sell_price = 10
    userinput.marketing_costs = 0
    userinput.research_and_development_costs = 0
    userinput.marketing_research_price = False
    userinput.marketing_research_sales = False
    userinput.marketing_research_quality = False
    userinput.marketing_research_marketing_costs = False


def _reset_userinput_period(period_total):
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





