from functools import wraps

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, UserInputForm, ReviewUserInputForm, ScenarioForm
from app.models import User, Game, Period, Scenario, Userinput, Product

PLAYERS_PER_GAME = 10
SCENARIO_ID = 1


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

        initial_period = Period(id=f'{game.id}_{user.id}_1', game_id=game.id,
                                period_number=1)
        user.periods.append(initial_period)
        user.game_id = game.id
        db.session.add(user)
        db.session.commit()

        flash(f'Registered new user: {user}')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


def get_game(players_limit_per_game=PLAYERS_PER_GAME):
    games = [g for g in Game.query.filter_by(is_active=True).all()
             if len(g.players.all()) < players_limit_per_game]
    return games[0] if games else create_game(scenario_id=SCENARIO_ID)


def create_game(scenario_id):
    return Game(demand_scenario_id=scenario_id)


@app.route('/admin/reveiw_scenario/product<product>/period<period>/', methods=['GET', 'POST'])
@login_required
@admin_required
def reveiw_scenario(product, period):
    scenario = Scenario.query.filter_by(product_id=product, period=period).first_or_404()
    product = Product.query.filter_by(id=product).first_or_404()
    form = ScenarioForm(obj=scenario)
    if form.validate_on_submit():
        form.populate_obj(scenario)
        db.session.add(scenario)
        db.session.commit()
        flash(f'Successfully updated scenario')

    return render_template('scenario.html', form=form, scenario=scenario, product=product)


@app.route('/admin/scenarios')
@login_required
@admin_required
def scenarios_list():
    scenarios = Scenario.query.order_by(Scenario.period, Scenario.product_id).all()
    return render_template('scenario_list.html', scenarios=scenarios)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@app.route('/games')
@login_required
@admin_required
def games():
    games = Game.query.filter_by(is_active=True)
    periods = Period.query.all()
    return render_template('games.html', games=games, periods=periods)


@app.route('/current_period')
@login_required
def current_period():
    user = current_user
    game = Game.query.filter_by(id=user.game_id).first()
    if not game:
        flash(f'Your team is currently not participating in the game. '
              f'Please contact administrator.')
        return redirect(url_for('index'))
    return render_template('current_period.html', user=user,
                           current_period=game.current_period)


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
    period = Period.query.filter_by(id=period_id).first()
    userinput = get_or_create(db.session, Userinput, id=f'{period.id}_{product.id}')

    form = UserInputForm(obj=userinput)
    if form.validate_on_submit():
        form.populate_obj(userinput)
        userinput.product_id = product.id

        db.session.add(userinput)
        db.session.commit()
        flash(f'Successfully submitted form!')

    return render_template('current_period_product.html', user=user,
                           current_period=game.current_period, form=form, product=product)


@app.route('/game/<game>/user/<user>', methods=['GET', 'POST'])
@login_required
@admin_required
def game_period_review(game, user):
    game = Game.query.filter_by(id=game).first_or_404()
    user = User.query.filter_by(id=user).first_or_404()
    period_n = game.current_period

    period_id = f'{game.id}_{user.id}_{period_n}'

    period = Period.query.filter_by(id=period_id).first()
    form = UserInputForm(obj=period)

    if form.validate_on_submit():
        form.populate_obj(period)
        db.session.add(period)

        players_periods = [game.players[i].periods.filter_by(period_number=period_n).first()
                           for i in range(len(game.players.all()))]

        if all([i.approved for i in players_periods]):
            calculate_period_results(game, players_periods)

        db.session.commit()
        flash(f'Successfully updated form! {form.data}')

    return render_template('current_period.html', period=period, user=user, form=form)


def calculate_period_results(game, players_periods):
    pass


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
