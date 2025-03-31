import pathlib
from flask import Flask, render_template, request


from tuition import Tuition, Family
from index import NEJAForm


HOME = pathlib.Path.home()

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

    tuition = Tuition(f"{HOME}/Tuition/2025tuition.csv")

    AGI = int(form.AGI.data)
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
    family = Family(AGI, students)

    subsidy = bool(form.subsidy.data)
    debug = bool(form.debug.data)
    cappable, uncappable = tuition.get_tuitions(family, subsidy)

    total = tuition.get_total_tuition(family, subsidy=subsidy)

    return render_template(
        "form.html",
        form=form,
        output_data=get_output(total),
        debug=debug,
        debug_data=get_debug(
            AGI, family.rate, family.max_tuition, cappable, uncappable, total, students
        ),
    )


def get_debug(AGI, percent, max_tuition, cappable, uncappable, total, students):
    output = []
    output.append(
        f"At an AGI of {format(AGI)}, your maximum qualified NEJA tuition is capped at {round(percent*100,2)}% of AGI, or {format(max_tuition)}"
    )

    # output.append("Your tuition expenses are as follows:")
    # for key, value in students.items():
    #     if value > 0:
    #         output.append(f"{value} {key} @ {123} each totaling {value * 123}")

    output.append(
        f"Your unqualified NEJA Tuition Expenses Total {format(uncappable)}. These expenses are not subject to a tuition cap."
    )
    if cappable > max_tuition:
        output.append(
            f"Your qualified NEJA tuition expenses total {format(cappable)}, which will be capped to your max tuition: {format(max_tuition)}"
        )
    else:
        output.append(
            f"Your qualified NEJA tuition expenses total: {format(cappable)}. Because of your AGI, these tuition expenses will not be capped."
        )

    output.append(
        f"Summing your qualified and unqualified tuitions results in Your total NEJA tuition: {format(total)}"
    )

    return output


def get_output(total):
    output = []
    output.append(f"Your Total NEJA Tuition is {format(total)}")
    return output


if __name__ == "__main__":
    app.run(debug=True)
