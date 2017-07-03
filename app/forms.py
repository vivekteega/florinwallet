from flask_wtf import Form
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired


class walletForm(Form):
    address = StringField('address', validators=[DataRequired()])
    amount = FloatField('amount', validators=[DataRequired()])
    comm = StringField('comm', validators=[DataRequired()])
