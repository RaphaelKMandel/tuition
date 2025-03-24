from flask import Flask, render_template, request

from tuition import Tuition, Family


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        agi = int(request.form.get("AGI"))
        subsidy = request.form.get("subsidy")
        students = {
            "ECC5F": int(request.form.get("ECC5F")),
            "ECC3F": int(request.form.get("ECC3F")),
            "ECC5H": int(request.form.get("ECC5H")),
            "ECC3H": int(request.form.get("ECC3H")),
            "ECCPP": int(request.form.get("ECCPP")),
            "K": int(request.form.get("K")),
            "G1": int(request.form.get("G1")),
            "G25": int(request.form.get("G25")),
            "G6": int(request.form.get("G6")),
            "G78": int(request.form.get("G78")),
            "G912": int(request.form.get("G912")),
        }

        tuition = Tuition("2025tuition.csv")
        family = Family(agi, students)

        print("subsidy", subsidy, bool(subsidy))
        total = tuition.get_total_tuition(family, subsidy=bool(subsidy))

        return render_template(
            "index.html",
            total=f"${total:,.2f}",
            agi=agi,
            subsidy=subsidy,
            **students,
        )

    return render_template("index.html", agi=100000, total=None)


if __name__ == "__main__":
    app.run(debug=True)
