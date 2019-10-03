from wtforms import (
    Form,
    BooleanField,
    StringField,
    PasswordField,
    validators,
    FileField,
    TextAreaField,
    IntegerField,
    DecimalField,
)
from wtforms.fields.html5 import DateField


class StockEntryForm(Form):
    ticker = StringField(
        "Ticker", [validators.Length(min=1, max=10), validators.DataRequired()]
    )
    quantity = IntegerField("Quantity", [validators.DataRequired()])
    cost = DecimalField("Cost", [validators.DataRequired()])
    index = StringField("Financial Index", [validators.length(min=2, max=20)])
    sector = StringField("Financial Sector", [validators.length(min=1, max=20)])

class StockUpdateForm(Form):

    id= IntegerField("Stock ID", [validators.DataRequired()]
    ticker = StringField(
    "Ticker"
    )
    quantity = IntegerField("Quantity")
    cost = DecimalField("Cost")
    index = StringField("Financial Index")
    sector = StringField("Financial Sector")