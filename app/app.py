from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
import flask_login
from flask_login import current_user, login_user, login_required, LoginManager, logout_user
import os
import base64
import datetime

app = Flask(__name__)
login_manager = flask_login.LoginManager()

login_manager.init_app(app)
login = LoginManager(app)

# FOR DEV ONLY
os.environ["APP_SETTINGS"] = "config.DevelopmentConfig"


app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Stocks, Leadership, CurStockData, User, History
from forms import (
    StockEntryForm,
    StockUpdateForm,
    StockDeleteForm,
    AddLeadershipForm,
    ManageLeadershipForm,
    LoginForm
)
from functions import StockThread, socketio, thread, refresh_stock_data, cur_state, random_color
current = cur_state()

@app.context_processor
def inject_current():
    global current
    return dict(current=current)

@app.route("/")
def root():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    stocks = Stocks.get()
    labels = list(set([stock.sector for stock in stocks]))
    data = []
    colors = []
    
    global current
    total = current[0]
    for label in labels:
        stocks = Stocks.get(sector=label)
        label_total = 0
        for stock in stocks:
            s_data = CurStockData.get(name=stock.name)
            label_total += stock.quantity*s_data[0].cost
        data.append(str(round(label_total/total,2)))
    equity_data = {
        'labels':labels,
        'data':data
    }
    data = [0,0,0,0,0]
    stocks = Stocks.get()
    for stock in stocks:
        s_data = CurStockData.get(name=stock.name)
        if stock.sector in ['Technology', 'Defense', 'Health Care', 'Financials', 'Consumer Goods', 'Automotive']:
            data[0] += stock.quantity*s_data[0].cost
        elif stock.sector in ['Precious Metals']:
            data[-1] += stock.quantity*s_data[0].cost
        elif stock.sector in ['REITS']:
            data[1] += stock.quantity*s_data[0].cost
        elif stock.sector in ['Fixed Income']:
            data[2] += stock.quantity*s_data[0].cost
    data[-2] += 21055.23
    data = [str(i) for i in data]
    asset_data = {

        'labels' : ['Equity', 'REIT', 'Fixed Income', 'Cash', 'Gold'],
        'data' : data
    }
    history = History.get()
    history = list(sorted(history, key=lambda x: x.date))
    date = [str(h.date) for h in history]
    total = []
    sp500 = []
    for i,h in enumerate(history):
        if i!=0:
            total.append(total[i-1]+((h.total/history[i-1].total)-1)*100)
            sp500.append(sp500[i-1]+((h.sp500/history[i-1].sp500)-1)*100)
        else:
            total.append(0)
            sp500.append(0)
    total = list(map(str,total))
    sp500 = list(map(str,sp500))
    line_data = {
        'dates' : date,
        'totals' : total,
        'sp500' : sp500
    }
    return render_template("home.html", equity_data=equity_data, asset_data=asset_data, line_data=line_data)


@app.route("/new stocks", methods=["GET", "POST"])
@login_required
def new_stocks():
    form = StockEntryForm(request.form)
    if request.method == "POST" and form.validate():
        Stocks.insert(
            name=form.ticker.data,
            quantity=form.quantity.data,
            cost=form.cost.data,
            index=form.index.data,
            sector=form.sector.data,
        )
        return redirect(url_for("new_stocks"))
    return render_template("new_stocks.html", form=form)


@app.route("/update stocks", methods=["GET", "POST"])
@login_required
def update_stocks():
    form = StockUpdateForm(request.form)
    if request.method == "POST" and form.validate():
        stock = Stocks.get(id=form.id.data)[0]
        if form.ticker.data:
            stock.name = form.ticker.data
        if form.quantity.data:
            stock.quantity = form.quantity.data
        if form.cost.data != 0:
            stock.cost = form.cost.data
        if form.index.data:
            stock.index = form.index.data
        if form.sector.data:
            stock.sector = form.sector.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_stocks.html", form=form)


@app.route("/delete stocks", methods=["GET", "POST"])
@login_required
def delete_stocks():
    form = StockDeleteForm(request.form)
    if request.method == "POST" and form.validate():
        stock = Stocks.get(id=form.id.data)[0]
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("delete_stocks.html", form=form)


@app.route("/portfolio")
def portfolio():
    stocks = CurStockData.get()
    top_per = list(sorted(stocks, key=lambda x: x.chg, reverse=True))[:3]
    low_per = list(sorted(stocks, key=lambda x: x.chg))[:3]
    history = History.get()
    history = list(sorted(history, key=lambda x: x.date, reverse=True))
    return render_template("portfolio.html", top_per=top_per, low_per=low_per, history=history)


@app.route("/rawdata")
def rawdata():
    stocks = Stocks.get()
    # uncomment to refresh data
    # refresh_stock_data(set(stocks))
    total = sum([stock.cost * stock.quantity for stock in stocks])
    for stock in stocks:
        data = CurStockData.get(name=stock.name)
        setattr(
            stock, "per_cost", round(((stock.cost * stock.quantity / total) * 100), 2)
        )
        setattr(stock, "cur_cost", data[0].cost)
        setattr(
            stock, "weight", round(((stock.cur_cost * stock.quantity) / total) * 100, 2)
        )
        setattr(
            stock,
            "per_gain",
            round(((stock.cur_cost - stock.cost) / stock.cost) * 100, 2),
        )
        setattr(stock, "price_chg", data[0].chg)
        if data[0].dividend:
            setattr(stock, "dividend", data[0].dividend)
            setattr(
                stock,
                "cur_yeild",
                round(((stock.dividend * 4) / stock.cur_cost) * 100, 2),
            )
            setattr(stock, "ann_inc", stock.dividend * stock.quantity * 4)
            setattr(
                stock,
                "yd_cost",
                round((stock.ann_inc / (stock.cost * stock.quantity)) * 100, 2),
            )
        else:
            setattr(stock, "dividend", "N/A")
            setattr(stock, "cur_yeild", "N/A")
            setattr(stock, "ann_inc", "N/A")
            setattr(stock, "yd_cost", "N/A")
    return render_template("rawdata.html", stocks=stocks, total=total)


@app.route("/about")
def about():
    leaders = Leadership.get(active=True)
    return render_template("about.html", leaders=leaders)


@app.route("/manage-leaders", methods=["GET", "POST"])
@login_required
def manage_leaders():
    leaders = Leadership.get()
    mychoices = [(leader.id, leader.name) for leader in leaders]
    prechecked = [leader.id for leader in leaders if leader.active]
    form = ManageLeadershipForm(request.form)
    form.active.choices = mychoices
    form.active.coerce = str
    if request.method == "GET":
        form.active.process_data(prechecked)

    if request.method == "POST":
        active = [int(i) for i in form.active.data]
        for leader in leaders:
            if leader.id in active:
                leader.active = True
            else:
                leader.active = False
        db.session.commit()
        return redirect(url_for("about"))

    return render_template("manage-leadership.html", form=form)


@app.route("/add-leaders", methods=["GET", "POST"])
@login_required
def add_leaders():
    form = AddLeadershipForm(request.form)

    if request.method == "POST" and form.validate():
        Leadership.insert(
            name=form.name.data,
            icon=base64.b64encode(request.files[form.icon.name].read()),
            position=form.position.data,
            description=form.description.data,
            major=form.major.data,
            year=form.year.data,
        )
        return redirect(url_for("about"))
    return render_template("add-leadership.html", form=form)


@socketio.on("connect", namespace="/stock-api")
def test_connect():
    global thread
    print("Client connected")

    if not thread.isAlive():
        print("Starting Thread")
        thread = StockThread()
        thread.start()


@socketio.on("disconnect", namespace="/stock-api")
def test_disconnect():
    print("Client disconnected")

@app.route('/background_refresh')
def background_process_test():
    stocks = Stocks.get()
    refresh_stock_data(set(stocks))
    global current
    current = cur_state()
    return "nothing"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.get(username=form.username.data)
        if not user or not user[0].check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user[0], remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))
