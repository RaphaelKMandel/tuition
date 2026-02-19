import pathlib
from nicegui import ui
from tuition import Tuition, WaterFall

# Resolve tuition CSV: prefer home/tuition/, fallback to script directory
HOME = pathlib.Path.home()
SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
TUITION_CSV = HOME / "tuition" / "2026tuition.csv"
if not TUITION_CSV.exists():
    TUITION_CSV = SCRIPT_DIR / "2026tuition.csv"

GRADE_LABELS = [
    ("ECC 5 Full Days", "ECC5F"),
    ("ECC 3 Full Days", "ECC3F"),
    ("ECC 5 Half Days", "ECC5H"),
    ("ECC 3 Half Days", "ECC3H"),
    ("ECC Extended Hours", "ECCPP"),
    ("Kindergarden", "K"),
    ("Grade 1", "G1"),
    ("Grades 2-5", "G25"),
    ("Grade 6", "G6"),
    ("Grades 7-8", "G78"),
    ("Grades 9-12", "G912"),
]


def get_debug(cap_data, tuition_data):
    lines = []
    AGI = cap_data["AGI"]
    lines.append(f"At an AGI of {AGI}:")
    for band in cap_data["bands"]:
        if len(band["band"]) == 1:
            lines.append(
                f"    Income above {band['band'][0]} is considered at {band['rate']}. "
                f"You earned {band['diff']} resulting in {band['value']}"
            )
        else:
            lines.append(
                f"    Income between {band['band'][0]}-{band['band'][1]} is considered at {band['rate']}. "
                f"You earned {band['diff']} resulting in {band['value']}"
            )
    lines.append(
        f"Summing the values in each band results in your maximum qualified tuition: {cap_data['max tuition']}"
    )
    lines.append("Your tuition expenses are as follows:")
    for grade, data in tuition_data["grades"].items():
        count = data["count"]
        if count > 0:
            lines.append(
                f"    {count} student(s) in {grade} @ {data['each']}/student for a sub-total of {data['tuition']} "
                f"of which {data['qualified']} is qualified for the tuition cap."
            )
    lines.append(
        f"Your unqualified tuition expenses total {tuition_data['totals']['unqualified']}. "
        "These expenses are not subject to a tuition cap."
    )
    qualified = tuition_data["totals"]["qualified"]
    max_tuition = cap_data["max tuition"]
    total = tuition_data["totals"]["total"]
    if qualified > max_tuition:
        lines.append(
            f"Your qualified tuition expenses total {qualified}, which will be capped to your max tuition: {max_tuition}"
        )
    else:
        lines.append(
            f"Your qualified tuition expenses total: {qualified}. "
            "Because of your AGI, these tuition expenses will not be capped."
        )
    lines.append(
        f"Summing your qualified and unqualified tuitions results in your total tuition: {total}"
    )
    return lines


@ui.page("/")
def main():
    ui.label("2026 NEJA Tuition Calculator").classes("text-2xl font-bold")
    ui.separator()

    with ui.row().classes("items-center gap-y-0 gap-x-2 p-0").style("grid-template-columns: minmax(0, max-content) 4rem"):
        ui.label("Family AGI (Previous Year):").classes("font-bold text-xl")
        agi = ui.number(value=100_000, format="%.0f")
        subsidy = ui.checkbox("Use subsidy rates?", value=True)


    counts = {}
    # Compact 2-col grid: label left, number right; fixed col width so numbers line up; no padding
    with ui.grid(columns=2).classes("items-center gap-y-0 gap-x-2 p-0").style("grid-template-columns: minmax(0, max-content) 4rem"):
        ui.label("Grade").classes("font-bold text-xl p-0")
        ui.label("# Students").classes("font-bold text-xl p-0 w-32")
        ui.separator()
        ui.separator()
        for label, key in GRADE_LABELS:
            ui.label(label).classes("p-0")
            num = ui.number(value=0, format="%.0f").classes("w-32")
            num.props("min=0 max=10 dense outlined")
            num.classes("p-0")
            counts[key] = num
    
    def calculate():
        try:
            agi_val = int(float(agi.value or 0))
        except (TypeError, ValueError):
            agi_val = 0
        agi_val = max(0, min(10_000_000, agi_val))

        students = {
            label: max(0, min(10, int((counts[key].value or 0))))
            for label, key in GRADE_LABELS
        }

        tuition = Tuition(str(TUITION_CSV))
        rates = WaterFall([300_000, 400_000], [0.15, 0.175, 0.2])
        cap_data = rates.evaluate(agi_val)
        subsidized = subsidy.value
        tuition_data = tuition.get_tuitions(
            students, cap_data["max tuition"], subsidized=subsidized
        )
        total = tuition_data["totals"]["total"]

        output_container.clear()
        with output_container:
            ui.label("Your Results")
            ui.label(f"Your Total Tuition is {total}")
            if debug.value:
                for line in get_debug(cap_data, tuition_data):
                    ui.label(line).style("white-space: pre-wrap")

    with ui.row():
        ui.button("Calculate", on_click=calculate)
        debug = ui.checkbox("Show details?", value=False)

    output_container = ui.column()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="2026 NEJA Tuition Calculator", host="0.0.0.0", dark=False)
