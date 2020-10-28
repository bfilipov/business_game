from functools import wraps

from flask import current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, UserInputForm, ReviewUserInputForm
from app.models import User, Game, Period, Demand, Userinput, Product


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


def get_game(players_limit_per_game=4):
    games = [g for g in Game.query.filter_by(is_active=True).all()
             if len(g.players.all()) < players_limit_per_game]
    return games[0] if games else create_game()


def create_game():
    return Game()


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


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

    max_price = 10

    percentages = {
        1: 40,
        2: 30,
        3: 20,
        4: 10
    }

    current_demand = Demand.query.filter_by(demand_scenario_id=game.demand_scenario_id,
                                            period=game.current_period).first()

    demand_a = current_demand.demand_A
    demand_b = current_demand.demand_B
    demand_c = current_demand.demand_C

    cost_a = 1
    cost_b = 1
    cost_c = 1

    users_score = {}

    for product in ['a', 'b', 'c']:
        marketing = {}
        price = {}
        quality = {}
        for player in players_periods:

            # sort scores from lowest to highest.
            # update each user score with 1,2,3,4 points

            price[player] = max_price - getattr(player, f'price_product_{product}')
            players_sorted_by_price = [i[0] for i in sorted(price.items(), key=lambda item: item[1])]
            for i in range(1, len(players_sorted_by_price) + 1):
                users_score[players_sorted_by_price[i - 1]] = i

            quality[player] = getattr(player, f'product_{product}_actual_quality')
            players_sorted_by_quality = [i[0] for i in sorted(price.items(), key=lambda item: item[1])]
            for i in range(1, len(players_sorted_by_price) + 1):
                users_score[players_sorted_by_quality[i - 1]] = i

            marketing[player] = getattr(player, f'product_{product}_marketing')
            players_sorted_by_marketing = [i[0] for i in sorted(marketing.items(), key=lambda item: item[1])]
            for i in range(1, len(players_sorted_by_marketing) + 1):
                users_score[players_sorted_by_marketing[i - 1]] += i

        # TODO:!!!REMOVE THE BEWLOW PDB BREAKPOINT
        import ipdb; ipdb.set_trace()
        # TODO:!!!REMOVE THE ABOVE PDB BREAKPOINT
    game.current_period += 1
    db.session.add(game)


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
