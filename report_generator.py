from fpdf import FPDF
from datetime import datetime
import os


def generate_pdf_report(result):

    os.makedirs("reports/generated", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"audit_report_{timestamp}.pdf"
    filepath = os.path.join("reports/generated", filename)

    pdf = FPDF()
    pdf.add_page()

    # Title

    pdf.set_font("Arial", "B", 18)
    pdf.cell(
        190,
        10,
        "Security Audit & Compliance Report",
        ln=True,
        align="C"
    )

    pdf.ln(10)

    # Organization Details

    org = result["organization"]

    pdf.set_font("Arial", "", 12)

    pdf.cell(
        190,
        8,
        f"Organization: {org['organization_name']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Industry: {org['industry']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Employees: {org['employee_count']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Auditor: {org['auditor_name']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Date: {datetime.now().strftime('%d-%m-%Y')}",
        ln=True
    )

    pdf.ln(10)

    # Executive Summary

    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Executive Summary", ln=True)

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        f"The organization achieved {result['compliance_percentage']}% compliance and is classified as {result['compliance_status']}."
    )

    pdf.ln(4)

    # Audit Statistics

    pdf.set_font("Arial", "B", 14)
    pdf.cell(190, 10, "Audit Statistics", ln=True)

    pdf.set_font("Arial", "", 11)

    pdf.cell(
        190,
        8,
        f"Total Controls Assessed: {result['total_controls']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Compliant Controls: {result['compliant_controls']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Non-Compliant Controls: {result['non_compliant_controls']}",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Compliance Percentage: {result['compliance_percentage']}%",
        ln=True
    )

    pdf.cell(
        190,
        8,
        f"Compliance Status: {result['compliance_status']}",
        ln=True
    )

    pdf.ln(5)

    # Category Summary

    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        190,
        10,
        "Category Compliance Summary",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    for category, percentage in result["category_summary"].items():

        pdf.cell(
            190,
            8,
            f"{category}: {percentage}%",
            ln=True
        )

    pdf.ln(5)

    # Audit Findings

    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        190,
        10,
        "Audit Findings",
        ln=True
    )

    categories = [
        "Access Control",
        "Network Security",
        "Data Protection",
        "Incident Response",
        "Compliance & Governance",
        "Asset Management"
    ]

    for category in categories:

        category_findings = []

        for finding in result["findings"]:

            if finding["category"] == category:
                category_findings.append(finding)

        if len(category_findings) == 0:
            continue

        pdf.ln(3)

        pdf.set_font("Arial", "B", 12)

        pdf.cell(
            190,
            8,
            f"{category} ({len(category_findings)} Findings)",
            ln=True
        )

        pdf.set_font("Arial", "", 10)

        for finding in category_findings:

            pdf.multi_cell(
                0,
                7,
                f"Control ID: {finding['control_id']}"
            )

            pdf.multi_cell(
                0,
                7,
                f"Finding: {finding['finding']}"
            )

            pdf.multi_cell(
                0,
                7,
                f"Impact: {finding['impact']}"
            )

            pdf.multi_cell(
                0,
                7,
                f"Recommendation: {finding['recommendation']}"
            )

            pdf.ln(2)

    # Conclusion

    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(
        190,
        10,
        "Conclusion",
        ln=True
    )

    pdf.set_font("Arial", "", 11)

    pdf.multi_cell(
        0,
        8,
        f"The organization's overall compliance status is {result['compliance_status']}."
    )

    pdf.output(filepath)

    return filepath