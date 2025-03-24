from flask import Flask, render_template, request

from tuition import Tuition, Family
from index import NEJAForm


app = Flask(__name__)
app.config["SECRET_KEY"] = "191234325129341234"


def format(amount):
    return f"${amount:,.2f}"


@app.route("/", methods=["GET", "POST"])
def main():
    form = NEJAForm()
    if not form.validate_on_submit():
        print("not validated")
        return render_template("form.html", form=form)

    tuition = Tuition("~/tuition/2025tuition.csv")
    students = {
        "ECC5F": int(form.ECC5F.data),
        "ECC3F": int(form.ECC3F.data),
        "ECC5H": int(form.ECC5H.data),
        "ECC3H": int(form.ECC3H.data),
        "ECCPP": int(form.ECCPP.data),
        "K": int(form.K.data),
        "G1": int(form.G1.data),
        "G25": int(form.G25.data),
        "G6": int(form.G6.data),
        "G78": int(form.G78.data),
        "G912": int(form.G912.data),
    }
    family = Family(form.agi.data, students)

    AGI = int(form.AGI.data)
    subsidy = bool(form.subsidy.data)
    cappable, uncappable = tuition.get_tuitions(family, subsidy)
    subtotal = cappable + uncappable
    total = tuition.get_total_tuition(family, subsidy=subsidy)

    max_tuition = family.max_tuition

    max_tuition = f"${max_tuition:,.2f}"
    subtotal = f"${subtotal:,.2f}"
    total = f"${total:,.2f}"
    cappable = f"${cappable:,.2f}"
    uncappable = f"${uncappable:,.2f}"

    return render_template(
        "form.html",
        form=form,
        AGI=AGI,
        max_tuition=max_tuition,
        subtotal=subtotal,
        total=total,
        cappable=cappable,
        uncappable=uncappable,
        students=students,
    )


if __name__ == "__main__":
    app.run(debug=True)
