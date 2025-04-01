import pathlib
from flask import Flask, render_template, request


from tuition import Tuition, Progressive
from index import NEJAForm


HOME = pathlib.Path.home()

app = Flask(__name__)
app.config["SECRET_KEY"] = "191234325129341234"


@app.route("/", methods=["GET", "POST"])
def main():
    form = NEJAForm()
    if not form.validate_on_submit():
        print("not validated")
        return render_template("form.html", form=form)

    tuition = Tuition(f"{HOME}/tuition/2025tuition.csv")
    prog = Progressive([300_000, 400_000], [0.15, 0.175, 0.2])

    AGI = int(form.AGI.data)
    cap_data = prog.evaluate(AGI)

    students = {
        "ECC 5 Full Days": int(form.ECC5F.data),
        "ECC 3 Full Days": int(form.ECC3F.data),
        "ECC 5 Half Days": int(form.ECC5H.data),
        "ECC 3 Half Days": int(form.ECC3H.data),
        "ECC Extended Hours": int(form.ECCPP.data),
        "Kindergarden": int(form.K.data),
        "Grade 1": int(form.G1.data),
        "Grades 2-5": int(form.G25.data),
        "Grade 6": int(form.G6.data),
        "Grades 7-8": int(form.G78.data),
        "Grades 9-12": int(form.G912.data),
    }

    subsidized = bool(form.subsidy.data)
    debug = bool(form.debug.data)
    tuition_data = tuition.get_tuitions(
        students, cap_data["max tuition"], subsidized=subsidized
    )

    return render_template(
        "form.html",
        form=form,
        output_data=get_output(tuition_data["totals"]["total"]),
        debug=debug,
        debug_data=get_debug(cap_data, tuition_data),
    )


def get_debug(cap_data, tuition_data):
    output = []
    AGI = cap_data["AGI"]
    output.append(f"At an AGI of {AGI}:")

    for band in cap_data["bands"]:
        output.append(
            f" Income between {band['band'][0]}-{band['band'][1]} is considered at {band['rate']}. You earned {band['diff']} resulting in {band['value']}"
        )

    output.append(
        f"Summing the values in each band results in your maximum qualified tuition: {cap_data['max tuition']}"
    )

    output.append("Your tuition expenses are as follows:")
    for grade, data in tuition_data["grades"].items():
        count = data["count"]
        if count > 0:
            output.append(
                f" {count} student(s) in {grade} @ {data['each']}/student for a sub-total of {data['tuition']} of which {data['qualified']} is qualified for the tuition cap."
            )

    output.append(
        f"Your unqualified tuition expenses total {tuition_data['totals']['unqualified']}. These expenses are not subject to a tuition cap."
    )
    qualified = tuition_data["totals"]["qualified"]
    max_tuition = cap_data["max tuition"]
    total = tuition_data["totals"]["total"]

    if qualified > max_tuition:
        output.append(
            f"Your qualified tuition expenses total {qualified}, which will be capped to your max tuition: {max_tuition}"
        )
    else:
        output.append(
            f"Your qualified tuition expenses total: {qualified}. Because of your AGI, these tuition expenses will not be capped."
        )

    output.append(
        f"Summing your qualified and unqualified tuitions results in your total tuition: {total}"
    )

    return output


def get_output(total):
    output = []
    output.append(f"Your Total Tuition is {total}")
    return output


if __name__ == "__main__":
    app.run(debug=True)
