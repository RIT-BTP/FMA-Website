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
from fields import MultiCheckboxField
from wtforms.fields.html5 import DateField


class StockEntryForm(Form):
    ticker = StringField(
        "Ticker", [validators.Length(min=1, max=10), validators.DataRequired()]
    )
    quantity = IntegerField("Quantity", [validators.DataRequired()])
    cost = DecimalField("Cost", [validators.DataRequired()])
    index = StringField("Financial Index")
    sector = StringField("Financial Sector")


class StockUpdateForm(Form):
    id = IntegerField("Stock ID", [validators.DataRequired()])
    ticker = StringField("Ticker")
    quantity = IntegerField("Quantity")
    cost = DecimalField("Cost")
    index = StringField("Financial Index")
    sector = StringField("Financial Sector")


class StockDeleteForm(Form):
    id = IntegerField("Stock ID", [validators.DataRequired()])


class AddLeadershipForm(Form):
    icon = FileField("Icon")
    name = StringField(
        "Name", [validators.Length(min=4, max=25), validators.DataRequired()]
    )
    description = TextAreaField(
        "Short Description",
        [validators.Length(min=10, max=500), validators.DataRequired()],
    )
    position = StringField("Position", [validators.DataRequired()])
    major = StringField("Major", [validators.DataRequired()])
    year = IntegerField("Year")


class ManageLeadershipForm(Form):
    active = MultiCheckboxField()
