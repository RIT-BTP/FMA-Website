from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import base64
import datetime

app = Flask(__name__)

# FOR DEV ONLY
app.config["APP_SETTINGS"] = "config.DevelopmentConfig"

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from models import Stocks
from forms import StockEntryForm, StockUpdateForm, StockDeleteForm

# from functions import user_check


@app.route("/")
def root():
    return redirect(url_for("home"))


@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/new stocks", methods=["GET", "POST"])
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
        return redirect(url_for("home"))
    return render_template("new_stocks.html", form=form)

@app.route("/update stocks", methods=["GET", "POST"] )
def update_stocks():
    form = StockUpdateForm(request.form)
    if request.method=='POST' and form.validate():
        stock = Stocks.get(id=form.id.data)[0]
        if form.ticker.data:
            stock.name=form.ticker.data
        if form.quantity.data:
            stock.quantity=form.quantity.data
        if form.cost.data != 0:
            stock.cost=form.cost.data
        if form.index.data:
            stock.index=form.index.data
        if form.sector.data:
            stock.sector=form.sector.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_stocks.html",form=form)

@app.route("/delete stocks", methods=['GET', "POST"])
def delete_stocks():
    form = StockDeleteForm(request.form)
    if request.method == 'POST' and form.validate():
        stock = Stocks.get(id=form.id.data)[0]
        db.session.delete(stock)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("delete_stocks.html",form=form)