from functools import wraps
import math
import random

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, UserInputForm, ReviewUserInputForm, ScenarioPerProductForm, \
    ScenarioPerPeriodForm, ReviewPeriodForm, ConfirmCurrentPeriodResultsForm, UserInputPeriodTotal, \
    ReviewUserInputPeriodTotal, DoubleConfirmForm, EditProfileForm
from app.models import Game, Period, PeriodTotal, Product, ScenarioPerProduct, ScenarioPerPeriod, User, Userinput

PLAYERS_PER_GAME = 10
SCENARIO_ID = 1
AUTO_APPROVE_RESULTS = True
AUTO_CONFIRM_PERIOD = True
DEFAULT_START_PRODUCTION = 0
INITIAL_CREDIT = 30000


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            # making sure we redirect only to relative paths
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign in', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/results')
@login_required
def results():
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first()

    period_id = f'{game.id}_{user.id}_{game.current_period-1}'
    previous_period_total = None if game.current_period < 2 else PeriodTotal.query.filter_by(id=period_id).first()
    periods = Period.query.filter_by(game_id=user.game_id, user_id=user.id,
                                     period_number=game.current_period - 1).all()
    new_period_total = PeriodTotal.query.filter_by(id=f'{game.id}_{user.id}_{game.current_period}').first()
    return render_template('ot4et.html', periods=periods, previous_period_total=previous_period_total,
                           new_period_total=new_period_total)


@app.route('/marketing')
@login_required
def marketing():
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first_or_404()
    players = game.players.all()
    products = Product.query.all()
    # period_totals = [period
    #            for player in players
    #            for period in player.periods.all()]

    period_id = f'{game.id}_{user.id}_{game.current_period-1}'
    previous_period_total = None if game.current_period < 2 else PeriodTotal.query.filter_by(id=period_id).first()
    # previous_period_products = [None] if game.current_period < 2 else \
    #     Period.query.filter_by(game_id=user.game_id, period_number=game.current_period-1).all()
    if previous_period_total:
        period_prod_1 = Period.query.filter_by(game_id=user.game_id, user_id=user.id,
                                               period_number=game.current_period - 1, product_id=1).first()

        period_prod_2 = Period.query.filter_by(game_id=user.game_id, user_id=user.id,
                                               period_number=game.current_period - 1, product_id=2).first()

        period_prod_3 = Period.query.filter_by(game_id=user.game_id, user_id=user.id,
                                               period_number=game.current_period - 1, product_id=3).first()

        show = {
            'price1': period_prod_1.research_price,
            'price2': period_prod_2.research_price,
            'price3': period_prod_3.research_price,

            'marketing1': period_prod_1.research_marketing,
            'marketing2': period_prod_2.research_marketing,
            'marketing3': period_prod_3.research_marketing,

            'quality1': period_prod_1.research_quality,
            'quality2': period_prod_2.research_quality,
            'quality3': period_prod_3.research_quality,

            'sales1': period_prod_1.research_sales,
            'sales2': period_prod_2.research_sales,
            'sales3': period_prod_3.research_sales,
        }

    else:
        show = {}

    return render_template('marketing.html', user=user, players=players,
                           previous_period_total=previous_period_total, products=products, show=show)


# @app.route('/gameplay')
# def gameplay():
#     return render_template('gameplay.html')

# @app.route('/info/bg')
# def help_bg():
#     return render_template('help_bg.html')

# @app.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template('user.html', user=user)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def user():
    user = current_user
    form = EditProfileForm(obj=user, meta={'user': current_user})
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
    return render_template('user.html', user=user, form=form)

# @app.route('/edit_profile')
# @login_required
# def user():
#     user = current_user
#     return render_template('user.html', user=user)


@app.route('/current_period', methods=['GET', 'POST'])
@login_required
def current_period():
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first()
    if not game:
        flash(f'Your team is currently not participating in the game. '
              f'Please contact administrator.')
        return redirect(url_for('index'))

    products = Product.query.all()
    period_total = PeriodTotal.query.filter_by(id=f'{game.id}_{user.id}_{game.current_period}').first_or_404()

    return render_template('current_period.html', user=user, period_total=period_total, products=products)


@app.route('/current_period/finance', methods=['GET', 'POST'])
@login_required
def current_period_finance():
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first()
    if not game:
        flash(f'Your team is currently not participating in the game. '
              f'Please contact administrator.')
        return redirect(url_for('index'))

    period_id = f'{game.id}_{user.id}_{game.current_period}'
    period_total = PeriodTotal.query.filter_by(id=period_id).first()
    form = UserInputPeriodTotal(obj=period_total)
    if form.validate_on_submit():
        form.populate_obj(period_total)
        if AUTO_APPROVE_RESULTS:
            period_total.input_approved_by_admin = True
        db.session.add(period_total)
        db.session.commit()
        flash(f'Изпратихте формата успешно')

    return render_template('current_period_finance.html', user=user,
                           period_total=period_total, form=form)


@app.route('/current_period/<product>', methods=['GET', 'POST'])
@login_required
def current_period_product(product):
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first()
    if not game:
        flash(f'Your team is currently not participating in the game. '
              f'Please contact administrator.')
        return redirect(url_for('index'))

    product = Product.query.filter_by(id=product).first_or_404()
    period_id = f'{game.id}_{user.id}_{game.current_period}'
    period = Period.query.filter_by(id=f'{period_id}_{product.id}').first()
    userinput = get_or_create(db.session, Userinput, id=f'{period.id}')
    period_total = PeriodTotal.query.filter_by(id=period_id).first_or_404()

    form = UserInputForm(obj=userinput)
    if form.validate_on_submit():
        form.populate_obj(userinput)
        userinput.product_id = product.id
        userinput.period_number = game.current_period
        userinput.user_id = user.id

        if AUTO_APPROVE_RESULTS:
            userinput.approved_by_admin = True

        db.session.add(userinput)
        db.session.commit()
        flash(f'Successfully submitted form!')

    return render_template('current_period_product.html', user=user, period_total=period_total, period=period,
                           current_period=game.current_period, form=form, product=product)


# ADMIN :
@app.route('/confirm_current_period/game/<gameid>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm_current_period(gameid):
    """
    Calculate results for all active games that have all their inputs approved """
    game = Game.query.filter_by(id=gameid).first_or_404()
    players = game.players.all()
    products = Product.query.all()
    periods = [period
               for player in players
               for period in player.periods.filter_by(period_number=game.current_period).all()]

    periods_totals = [period_total
                      for player in players
                      for period_total in player.period_total.filter_by(period_number=game.current_period).all()]

    form = None
    all_confirmed = (periods and all([p.confirmed_by_admin for p in periods])) \
        and (periods_totals and all([pt.input_approved_by_admin for pt in periods_totals]))

    if not all_confirmed:
        flash('There are unconfirmed user inputs.')
    else:
        form = ConfirmCurrentPeriodResultsForm()
        if form.validate_on_submit():
            if form.approved.data:
                game.current_period += 1
                db.session.add(game)
                db.session.flush()

                for player in players:
                    player.game_id = game.id
                    for product in products:

                        previous_period = player.periods.filter_by(
                            period_number=game.current_period-1, product_id=product.id).first()

                        # try to query period in case we come back from future
                        next_period = Period.query.filter_by(
                            id=f'{game.id}_{player.id}_{game.current_period}_{product.id}').first()
                        if not next_period:
                            next_period = Period(
                                id=f'{game.id}_{player.id}_{game.current_period}_{product.id}', game_id=game.id,
                                period_number=game.current_period, product_id=product.id,
                                products_in_stock_beginning_of_period=previous_period.products_in_stock_end_of_period)
                            player.periods.append(next_period)

                    previous_period_total = player.period_total.filter_by(
                        period_number=game.current_period-1).first()

                    next_p_total = PeriodTotal.query.filter_by(
                        id=f'{game.id}_{player.id}_{game.current_period}').first()
                    if not next_p_total:
                        next_p_total = PeriodTotal(
                            id=f'{game.id}_{player.id}_{game.current_period}', game_id=game.id,
                            period_number=game.current_period)

                    # financial calculations
                    next_p_total.credit_total = (previous_period_total.credit_total
                                                 + previous_period_total.take_credit)

                    next_p_total.overdraft_total = (previous_period_total.overdraft_total
                                                    - previous_period_total.deposit_overdraft)

                    next_p_total.money_total_begining_of_period = (previous_period_total.money_total_end_of_period
                                                                   - previous_period_total.deposit_overdraft
                                                                   - previous_period_total.take_credit)

                    # add overdraft_change to next period money
                    if next_p_total.overdraft_total < 0:
                        overdraft_change = -next_p_total.overdraft_total
                        next_p_total.overdraft_total = 0
                        next_p_total.money_total_begining_of_period += overdraft_change

                    # if money for next_p less than 0 add to overdraft forr next_p and set money to 0
                    if next_p_total.money_total_begining_of_period < 0:
                        next_p_total.overdraft_total = (next_p_total.overdraft_total
                                                        - next_p_total.money_total_begining_of_period)
                        next_p_total.money_total_begining_of_period = 0

                    # financial calculations

                    player.period_total.append(next_p_total)
                    db.session.add(player)
                    db.session.commit()
                flash(f'Current game period is {game.current_period}')
                flash(f'Successfully updated game state!')

    return render_template('confirm_game.html', game=game, periods=periods, form=form, players=players)


@app.route('/game/<game>/go_back_one_period', methods=['GET', 'POST'])
@login_required
@admin_required
def go_back_one_period(game):
    game = Game.query.filter_by(id=game).first_or_404()
    form = DoubleConfirmForm()
    title = f'Decrement current period - {game.current_period} for game {game.id}?'
    if form.validate_on_submit():
        if form.approved.data and form.approved2.data:

            game.current_period -= 1
            if game.current_period < 1:
                game.current_period = 1
            db.session.add(game)
            db.session.commit()
            flash(f'Went one period back in time! Current period for game: {game.id} is now: {game.current_period}')
            return redirect(url_for('games'))

    return render_template('simple_form_h1.html', game=game,  title=title, form=form)


@app.route('/calculate_period_results')
@login_required
@admin_required
def calculate_period_results():
    """
    Calculate results for all active games that have all their inputs approved """
    games = Game.query.filter_by(is_active=True).all()
    for game in games:
        period_n = game.current_period

        game_inputs = [game.players[i].userinput.filter_by(period_number=period_n).all()
                       for i in range(len(game.players.all()))]

        # if all user inputs in game for current period are approved
        if all([i.approved_by_admin for game_i in game_inputs for i in game_i]):
            _calculate_period_results(game)
    return redirect(url_for('games'))


@app.route('/check_user_inputs')
@login_required
@admin_required
def check_user_inputs():
    games = Game.query.filter_by(is_active=True).all()
    for game in games:
        for player in game.players:
            _check_inputs(player)
    return redirect(url_for('games'))


@app.route('/games')
@login_required
@admin_required
def games():
    games = Game.query.filter_by(is_active=True).all()
    periods = Period.query.all()
    return render_template('games.html', games=games, periods=periods)


@app.route('/game/<game>/user/<user>')
@login_required
@admin_required
def game_user(game, user):
    game = Game.query.filter_by(id=game).first_or_404()
    user = User.query.filter_by(id=user).first_or_404()
    period_n = game.current_period

    period_id = f'{game.id}_{user.id}_{period_n}'
    # filter by partial string
    periods = Period.query.filter(Period.id.contains(period_id)).all()

    period_id = f'{game.id}_{user.id}_{period_n}'
    period_total = PeriodTotal.query.filter_by(id=period_id).first_or_404()

    return render_template('current_period.html', periods=periods, period_total=period_total, user=user)


@app.route('/confirm_finance/game/<game>/user/<user>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm_period_finance(game, user):
    game = Game.query.filter_by(id=game).first_or_404()
    period_id = f'{game.id}_{user}_{game.current_period}'
    period_total = PeriodTotal.query.filter_by(id=period_id).first_or_404()
    form = ReviewUserInputPeriodTotal(obj=period_total)
    if form.validate_on_submit():
        form.populate_obj(period_total)
        db.session.add(period_total)
        db.session.commit()
        flash(f'Изпратихте формата успешно')

    return render_template('current_period_finance.html', user=user,
                           period_total=period_total, form=form)


@app.route('/game/<game>/user/<user>/product/<product>', methods=['GET', 'POST'])
@login_required
@admin_required
def game_period_review(game, user, product):
    game = Game.query.filter_by(id=game).first_or_404()
    user = User.query.filter_by(id=user).first_or_404()
    period_n = game.current_period
    product = Product.query.filter_by(id=product).first_or_404()

    period_id = f'{game.id}_{user.id}_{period_n}_{product.id}'
    period = Period.query.filter_by(id=period_id).first()

    userinput = get_or_create(db.session, Userinput, id=f'{period.id}')
    form = ReviewUserInputForm(obj=userinput)
    if form.validate_on_submit():
        form.populate_obj(userinput)

        userinput.product_id = product.id
        userinput.period_number = game.current_period
        userinput.user_id = user.id

        db.session.add(userinput)
        db.session.commit()
        flash(f'Successfully updated form!')

    return render_template('current_period_product.html', period=period,
                           user=user, product=product, form=form)


@app.route('/confirm/game/<game>/user/<user>/product/<product>', methods=['GET', 'POST'])
@login_required
@admin_required
def confirm_period_results(game, user, product):
    game = Game.query.filter_by(id=game).first_or_404()
    user = User.query.filter_by(id=user).first_or_404()
    period_n = game.current_period
    product = Product.query.filter_by(id=product).first_or_404()

    period_id = f'{game.id}_{user.id}_{period_n}_{product.id}'
    period = Period.query.filter_by(id=period_id).first()

    form = ReviewPeriodForm(obj=period)
    if form.validate_on_submit():
        form.populate_obj(period)

        period.product_id = product.id
        period.period_number = game.current_period
        period.user_id = user.id

        db.session.add(period)
        db.session.commit()
        flash(f'Successfully updated form! {form.data}')

    return render_template('confirm_period_results.html', period=period,
                           user=user, product=product, form=form)


@app.route('/admin/scenarios/scenario_id/<scenario_id>/period/<period>', methods=['GET', 'POST'])
@login_required
@admin_required
def reveiw_scenario_period(scenario_id, period):
    scenario = ScenarioPerPeriod.query.filter_by(period=period, demand_scenario_id=scenario_id).first_or_404()
    form = ScenarioPerProductForm(obj=scenario)
    if form.validate_on_submit():
        form.populate_obj(scenario)
        db.session.add(scenario)
        db.session.commit()
        flash(f'Successfully updated scenario')
    return render_template('scenario_period.html', form=form, scenario=scenario)


@app.route('/admin/scenarios/scenario_id/<scenario_id>/period/<period>/product/<product>', methods=['GET', 'POST'])
@login_required
@admin_required
def reveiw_scenario_product(product, period, scenario_id):
    scenario = ScenarioPerProduct.query.filter_by(product_id=product, period=period,
                                                  demand_scenario_id=scenario_id).first_or_404()
    product = Product.query.filter_by(id=product).first_or_404()
    form = ScenarioPerPeriodForm(obj=scenario)
    if form.validate_on_submit():
        form.populate_obj(scenario)
        db.session.add(scenario)
        db.session.commit()
        flash(f'Successfully updated scenario')
    return render_template('scenario_product.html', form=form, scenario=scenario, product=product)


@app.route('/admin/scenarios')
@login_required
@admin_required
def scenarios_list():
    scenarios_per_product = ScenarioPerProduct.query.order_by(ScenarioPerProduct.period, ScenarioPerProduct.product_id).all()
    scenarios_per_period = ScenarioPerPeriod.query.order_by(ScenarioPerPeriod.period).all()
    scenario_ids = list(set([s.demand_scenario_id for s in scenarios_per_product]))
    return render_template('scenario_list.html', scenarios_product=scenarios_per_product,
                           scenarios_period=scenarios_per_period, scenario_ids=scenario_ids)


@app.route('/admin/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        user.display_name = form.display_name.data

        user.member1 = form.member1.data
        user.member2 = form.member2.data
        user.member3 = form.member3.data
        user.member4 = form.member4.data
        user.member5 = form.member5.data
        user.member6 = form.member6.data
        user.member7 = form.member7.data
        user.member8 = form.member8.data
        user.member9 = form.member9.data
        user.member10 = form.member10.data

        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()

        game = get_game()
        db.session.add(game)
        db.session.flush()

        user.game_id = game.id

        products = Product.query.all()
        for product in products:
            initial_period = Period(
                id=f'{game.id}_{user.id}_1_{product.id}', game_id=game.id,
                period_number=1, product_id=product.id,
                products_in_stock_beginning_of_period=DEFAULT_START_PRODUCTION)
            user.periods.append(initial_period)

        initial_period_total = PeriodTotal(
            id=f'{game.id}_{user.id}_1', game_id=game.id, period_number=1)
        initial_period_total.money_total_begining_of_period = INITIAL_CREDIT
        initial_period_total.credit_total = INITIAL_CREDIT
        user.period_total.append(initial_period_total)

        db.session.add(user)
        db.session.commit()

        flash(f'Registered new user: {user}')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


# funks
def _check_inputs(player):
    game = Game.query.filter_by(id=player.game_id).first()
    for player_input in player.userinput.filter_by(period_number=game.current_period).all():
        if not player_input.approved_by_admin:
            flash(f'Game: {game.id} Username: {player.username} '
                  f'UserID: {player.id} UserInput: {player_input} not approved.')


def _calculate_period_results(game) -> None:

    total_combined_score = 0

    for player in game.players:
        # fill in available data for current period per player
        current_player_period = PeriodTotal.query.filter_by(
            id=f'{game.id}_{player.id}_{game.current_period}').first()

        scenario_period = ScenarioPerPeriod.query.filter_by(
                demand_scenario_id=game.demand_scenario_id, period=game.current_period).first()

        total_administrative_costs = 0
        total_production_quantity = 0
        total_interest_costs = ((current_player_period.credit_total * scenario_period.interest_credit)
                                + (current_player_period.overdraft_total * scenario_period.interest_overdraft))
        current_player_period.total_interest_costs = total_interest_costs

        producing_at_least_one_product = any(
            [i.produce_quantity for i in player.userinput.filter_by(period_number=game.current_period).all()])

        for player_input in player.userinput.filter_by(period_number=game.current_period).all():

            rand = random.random()

            # scenario for current period current product
            scenario = ScenarioPerProduct.query.filter_by(
                demand_scenario_id=game.demand_scenario_id, period=game.current_period,
                product_id=player_input.product_id).first()

            previous_period = None if scenario.period == 1 else Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period-1}_{player_input.product_id}').first()

            marketing_research_marketing_costs = 1 if player_input.marketing_research_marketing_costs else 0
            marketing_research_price = 1 if player_input.marketing_research_price else 0
            marketing_research_quality = 1 if player_input.marketing_research_quality else 0
            marketing_research_sales = 1 if player_input.marketing_research_sales else 0

            marketing_index = calculate_marketing_index(previous_period, scenario, player_input)
            quality_budget = calculate_quality_budget(previous_period, scenario, player_input, rand)
            quality_index = calculate_quality_index(quality_budget, previous_period, scenario)

            # fill in available data for current period per product
            current_prod_period = Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period}_{player_input.product_id}').first()

            sell_price = player_input.sell_price
            current_prod_period.sell_price = sell_price

            recalc_marketing = marketing_index * scenario.sensitivity_marketing
            current_prod_period.recalc_marketing = recalc_marketing

            recalc_quality = quality_index * scenario.sensitivity_quality
            current_prod_period.recalc_quality = recalc_quality

            recalc_price = sell_price * scenario.sensitivity_price
            current_prod_period.recalc_price = recalc_price

            combined_score = recalc_marketing * recalc_quality * recalc_price
            current_prod_period.combined_score = combined_score
            total_combined_score += combined_score

            # fill in available data for current period
            current_prod_period = Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period}_{player_input.product_id}').first()

            current_prod_period.userinput_id = player_input.id
            current_prod_period.random_value = rand

            total_production_quantity += player_input.produce_quantity

            # Q&M indexes
            current_prod_period.index_marketing = marketing_index
            current_prod_period.index_quality = quality_index

            #  production costs
            labor_costs = player_input.produce_quantity * scenario.cost_labor * scenario.correction_cost_labor
            current_prod_period.labor_costs = labor_costs

            materials_costs = (player_input.produce_quantity * scenario.cost_materials_for_one_product
                               * scenario.correction_cost_materials_for_one_product)
            current_prod_period.material_costs = materials_costs

            total_production_cost = labor_costs + materials_costs
            current_prod_period.total_production_cost = total_production_cost

            #  non-production costs
            current_prod_period.marketing_costs = player_input.marketing_costs
            current_prod_period.research_and_development_costs = player_input.research_and_development_costs

            transport_costs = player_input.produce_quantity * scenario.cost_transport
            current_prod_period.transport_costs = transport_costs

            storage_costs = player_input.produce_quantity * scenario.cost_storage
            current_prod_period.storage_costs = storage_costs

            is_producing = True if player_input.produce_quantity else False
            current_prod_period.is_producing = is_producing
            was_produsing = previous_period.is_producing if previous_period else False

            product_manager_costs = (scenario.cost_product_manager
                                     if was_produsing else scenario.cost_new_product_manager) \
                if is_producing else 0
            current_prod_period.product_manager_costs = product_manager_costs

            marketing_research_costs = (
                    marketing_research_marketing_costs + marketing_research_price
                    + marketing_research_quality + marketing_research_sales) * scenario.price_research
            current_prod_period.marketing_research_costs = marketing_research_costs

            if producing_at_least_one_product:
                interest_costs = (player_input.produce_quantity /
                                  (current_player_period.total_production_quantity or 1)) * total_interest_costs
            else:
                interest_costs = total_interest_costs / 3

            current_prod_period.interest_costs = interest_costs

            # administrative costs
            current_prod_period.other_costs = scenario.cost_unpredicted
            total_administrative_costs += scenario.cost_unpredicted

            total_non_production_costs = (
                player_input.marketing_costs + player_input.research_and_development_costs +
                transport_costs + storage_costs + product_manager_costs + marketing_research_costs
                + scenario.cost_unpredicted + interest_costs
            )
            current_prod_period.total_non_production_costs = total_non_production_costs

            total_costs = (total_production_cost + total_non_production_costs)
            current_prod_period.total_costs = total_costs
            current_prod_period.total_costs_per_one = total_costs / player_input.produce_quantity \
                if player_input.produce_quantity else 0

            # budgets
            previous_period_consolidated_rnd_budget = previous_period.consolidated_rnd_budget \
                if previous_period else 0
            current_prod_period.consolidated_rnd_budget = previous_period_consolidated_rnd_budget + quality_budget

            previous_period_consolidated_marketing_budget = previous_period.consolidated_marketing_budget \
                if previous_period else 0
            current_prod_period.consolidated_marketing_budget = (previous_period_consolidated_marketing_budget
                                                                 + player_input.marketing_costs)

            # researches
            current_prod_period.research_price = marketing_research_price
            current_prod_period.research_marketing = marketing_research_marketing_costs
            current_prod_period.research_quality = marketing_research_quality
            current_prod_period.research_sales = marketing_research_sales

            db.session.add(current_prod_period)
            db.session.commit()
        # for player_input in player.userinput.filter_by(period_number=game.current_period).all():

        total_administrative_costs += scenario_period.cost_fixed_administrative
        current_player_period.total_administrative_costs = total_administrative_costs
        current_player_period.total_production_quantity = total_production_quantity
        db.session.add(current_player_period)
        db.session.commit()

    # second iteration after we have total_combined_score
    total_unsatisfied_demand = 0
    for player in game.players:
        current_player_period = PeriodTotal.query.filter_by(
            id=f'{game.id}_{player.id}_{game.current_period}').first()

        producing_at_least_one_product = any(
            [i.produce_quantity for i in player.userinput.filter_by(period_number=game.current_period).all()])

        for player_input in player.userinput.filter_by(period_number=game.current_period).all():

            scenario = ScenarioPerProduct.query.filter_by(
                demand_scenario_id=game.demand_scenario_id, period=game.current_period,
                product_id=player_input.product_id).first()

            current_prod_period = Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period}_{player_input.product_id}').first()

            supply = player_input.produce_quantity + current_prod_period.products_in_stock_beginning_of_period

            market_share = current_prod_period.combined_score / total_combined_score
            current_prod_period.market_share = market_share

            demand = math.floor(scenario.demand_quantity * market_share)
            current_prod_period.demand = demand

            direct_sells = min(supply, demand)
            current_prod_period.direct_sells = direct_sells

            unsatisfied_demand = demand - direct_sells
            current_prod_period.unsatisfied_demand = unsatisfied_demand
            total_unsatisfied_demand += unsatisfied_demand

            # calculate administrative costs by product after we have totals
            if producing_at_least_one_product:
                administrative_costs = (
                    player_input.produce_quantity / (current_player_period.total_production_quantity or 1)) \
                                       * current_player_period.total_administrative_costs
            else:
                administrative_costs = current_player_period.total_administrative_costs / 3

            current_prod_period.administrative_costs = administrative_costs

            # add administrative costs by product to total non prodiction costs
            current_prod_period.total_non_production_costs += administrative_costs

            db.session.add(current_prod_period)
            db.session.commit()

    # third iteration after we have 1total_unsatisfied_demand
    for player in game.players:
        total_period_proffit = 0
        player_total_period = PeriodTotal.query.filter_by(
            id=f'{game.id}_{player.id}_{game.current_period}').first()
        for player_input in player.userinput.filter_by(period_number=game.current_period).all():
            current_prod_period = Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period}_{player_input.product_id}').first()

            supply = player_input.produce_quantity + current_prod_period.products_in_stock_beginning_of_period
            unsatisfied_demand = current_prod_period.unsatisfied_demand
            direct_sells = current_prod_period.direct_sells
            market_share = current_prod_period.market_share

            secondary_sells = min(math.floor(market_share * total_unsatisfied_demand), (supply-direct_sells)) \
                if unsatisfied_demand == 0 else 0
            current_prod_period.secondary_sells = secondary_sells

            total_sells = direct_sells + secondary_sells
            current_prod_period.total_sells = total_sells

            income_from_sells = current_prod_period.sell_price * total_sells
            current_prod_period.income_from_sells = income_from_sells

            products_in_stock_end_of_period = supply - total_sells
            current_prod_period.products_in_stock_end_of_period = products_in_stock_end_of_period

            gross_proffit = income_from_sells - current_prod_period.total_production_cost
            current_prod_period.gross_proffit = gross_proffit

            net_proffit = gross_proffit - current_prod_period.total_non_production_costs
            current_prod_period.net_proffit = net_proffit

            previous_period = None if current_prod_period.period_number == 1 else Period.query.filter_by(
                id=f'{game.id}_{player.id}_{game.current_period - 1}_{player_input.product_id}').first()

            accumulated_proffit = previous_period.accumulated_proffit if previous_period else 0
            current_prod_period.accumulated_proffit = accumulated_proffit + net_proffit
            total_period_proffit += net_proffit

            current_prod_period.confirmed_by_admin = AUTO_CONFIRM_PERIOD

            db.session.add(current_prod_period)
            db.session.commit()
            flash(f'Successfully re/calculated results for game: {game} player: {player} '
                  f'product: {player_input.product_id}')
        player_total_period.money_total_end_of_period = (player_total_period.money_total_begining_of_period
                                                         + total_period_proffit)
        db.session.add(player_total_period)
        db.session.commit()
        flash(f'Successfully re/calculated financial results for game: {game} player: {player}')


def calculate_marketing_index(previous_period, scenario, player_input):
    previous_period_marketing_index = previous_period.index_marketing \
        if previous_period else scenario.marketing_index_min
    marketing_index = player_input.marketing_costs / (
            scenario.investment_for_one_marketing + (previous_period_marketing_index
                                                     * scenario.marketing_keep_effect))
    marketing_index = scenario.marketing_index_max \
        if marketing_index > scenario.marketing_index_max else marketing_index
    marketing_index = scenario.marketing_index_min \
        if marketing_index < scenario.marketing_index_min else marketing_index
    return marketing_index


def calculate_quality_budget(previous_period, scenario, player_input, rand):
    consolidated_rnd_budget = previous_period.consolidated_rnd_budget \
        if previous_period else 0
    return (player_input.research_and_development_costs + consolidated_rnd_budget) * \
           (rand * (1 - scenario.base_value_rand_quality) + scenario.base_value_rand_quality)


def calculate_quality_index(quality_budget, previous_period, scenario):
    previous_period_quality_index = previous_period.index_quality if previous_period else 0
    quality_index = previous_period_quality_index + (quality_budget / scenario.investment_for_one_quality)
    quality_index = scenario.quality_index_max if quality_index > scenario.quality_index_max else quality_index
    quality_index = scenario.quality_index_min if quality_index < scenario.quality_index_min else quality_index
    return quality_index


def get_or_create(session, model, **kwargs):
    """
    session, model, **kwargs
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def get_game(players_limit_per_game=PLAYERS_PER_GAME):
    games = [g for g in Game.query.filter_by(is_active=True).all()
             if len(g.players.all()) < players_limit_per_game]
    return games[0] if games else create_game(scenario_id=SCENARIO_ID)


def create_game(scenario_id):
    return Game(demand_scenario_id=scenario_id)

