from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class NEJAForm(FlaskForm):
    AGI = IntegerField(
        "AGI",
        default=100000,
        render_kw={"step": 1000},
        validators=[DataRequired(), NumberRange(min=0, max=10_000_000)],
    )
    subsidy = BooleanField("subsidy", default=True)
    debug = BooleanField("debug")
    ECC5F = IntegerField(
        label="ECC5F", default=0, validators=[NumberRange(min=0, max=10)]
    )
    ECC3F = IntegerField(
        label="ECC3F", default=0, validators=[NumberRange(min=0, max=10)]
    )
    ECC5H = IntegerField(
        label="ECC5H", default=0, validators=[NumberRange(min=0, max=10)]
    )
    ECC3H = IntegerField(
        label="ECC3H", default=0, validators=[NumberRange(min=0, max=10)]
    )
    ECCPP = IntegerField(
        label="ECCPP", default=0, validators=[NumberRange(min=0, max=10)]
    )
    K = IntegerField(label="K", default=0, validators=[NumberRange(min=0, max=10)])
    G1 = IntegerField(label="G1", default=0, validators=[NumberRange(min=0, max=10)])
    G25 = IntegerField(label="G25", default=0, validators=[NumberRange(min=0, max=10)])
    G6 = IntegerField(label="G6", default=0, validators=[NumberRange(min=0, max=10)])
    G78 = IntegerField(label="G78", default=0, validators=[NumberRange(min=0, max=10)])
    G912 = IntegerField(
        label="G912", default=0, validators=[NumberRange(min=0, max=10)]
    )

    submit = SubmitField("Submit")
