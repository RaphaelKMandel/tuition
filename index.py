from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

NOS = [0, 1, 2, 3, 4, 5, 6]


class NEJAForm(FlaskForm):
    agi = IntegerField(
        "AGI", validators=[DataRequired(), NumberRange(min=0, max=10_000_000)]
    )
    subsidy = BooleanField("subsidy")
    ECC5F = SelectField(label="ECC5F", choices=NOS)
    ECC3F = SelectField(label="ECC3F", choices=NOS)
    ECC5H = SelectField(label="ECC5H", choices=NOS)
    ECC3H = SelectField(label="ECC3H", choices=NOS)
    ECCPP = SelectField(label="ECCPP", choices=NOS)
    K = SelectField(label="K", choices=NOS)
    G1 = SelectField(label="G1", choices=NOS)
    G25 = SelectField(label="G25", choices=NOS)
    G6 = SelectField(label="G6", choices=NOS)
    G78 = SelectField(label="G78", choices=NOS)
    G912 = SelectField(label="G912", choices=NOS)

    submit = SubmitField("Submit Please")
