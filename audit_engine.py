import json


def load_controls():
    with open("controls.json", "r") as file:
        data = json.load(file)

    return data["controls"]


def evaluate_audit(controls, responses, org_info):

    total_controls = len(controls)
    compliant_controls = 0

    findings = []
    category_stats = {}

    for control in controls:

        category = control["category"]

        if category not in category_stats:
            category_stats[category] = {
                "total": 0,
                "compliant": 0
            }

        category_stats[category]["total"] += 1

        answer = responses.get(control["id"], "No")

        if answer == "Yes":

            compliant_controls += 1
            category_stats[category]["compliant"] += 1

        else:

            findings.append({
                "control_id": control["id"],
                "category": control["category"],
                "finding": control["question"],
                "impact": control["impact"],
                "recommendation": control["recommendation"]
            })

    non_compliant_controls = total_controls - compliant_controls

    compliance_percentage = round(
        (compliant_controls / total_controls) * 100,
        2
    )

    if compliance_percentage >= 95:
        compliance_status = "Fully Compliant"

    elif compliance_percentage >= 85:
        compliance_status = "Highly Compliant"

    elif compliance_percentage >= 70:
        compliance_status = "Moderately Compliant"

    elif compliance_percentage >= 50:
        compliance_status = "Partially Compliant"

    elif compliance_percentage >= 25:
        compliance_status = "Low Compliance"

    else:
        compliance_status = "Critical Compliance Gaps"

    category_summary = {}

    for category, stats in category_stats.items():

        percentage = round(
            (stats["compliant"] / stats["total"]) * 100,
            2
        )

        category_summary[category] = percentage

    return {
        "organization": org_info,
        "total_controls": total_controls,
        "compliant_controls": compliant_controls,
        "non_compliant_controls": non_compliant_controls,
        "compliance_percentage": compliance_percentage,
        "compliance_status": compliance_status,
        "category_summary": category_summary,
        "findings": findings
    }