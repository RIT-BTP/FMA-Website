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
from forms import StockEntryForm

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
