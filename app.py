from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory
)

import os
import audit_engine
import report_generator

app = Flask(__name__)

latest_result = {}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/audit")
def audit():

    controls = audit_engine.load_controls()

    return render_template(
        "audit_form.html",
        controls=controls
    )


@app.route("/submit_audit", methods=["POST"])
def submit_audit():

    global latest_result

    org_info = {
        "organization_name": request.form.get(
            "organization_name"
        ),
        "industry": request.form.get(
            "industry"
        ),
        "employee_count": request.form.get(
            "employee_count"
        ),
        "auditor_name": request.form.get(
            "auditor_name"
        )
    }

    controls = audit_engine.load_controls()

    responses = {}

    for control in controls:

        responses[control["id"]] = request.form.get(
            control["id"],
            "No"
        )

    audit_result = audit_engine.evaluate_audit(
        controls,
        responses,
        org_info
    )

    latest_result = audit_result

    report_path = report_generator.generate_pdf_report(
        audit_result
    )

    latest_result["report_path"] = report_path

    latest_result["report_filename"] = os.path.basename(
        report_path
    )

    return redirect(
        url_for("dashboard")
    )


@app.route("/dashboard")
def dashboard():

    global latest_result

    if not latest_result:
        return redirect(
            url_for("audit")
        )

    return render_template(
        "dashboard.html",
        result=latest_result
    )


@app.route("/report")
def report_view():

    global latest_result

    if not latest_result:
        return redirect(
            url_for("audit")
        )

    return render_template(
        "report_view.html",
        result=latest_result
    )


@app.route("/reports/generated/<filename>")
def download_report(filename):

    return send_from_directory(
        "reports/generated",
        filename,
        as_attachment=True
    )


if __name__ == "__main__":

    os.makedirs(
        "reports/generated",
        exist_ok=True
    )

    app.run(
        debug=True
    )