let currentStep = 1;

const totalSteps = 7;

const stepTitles = {
    1: "Access Control",
    2: "Network Security",
    3: "Data Protection",
    4: "Incident Response",
    5: "Compliance & Governance",
    6: "Asset Management",
    7: "Review & Submit"
};

document.addEventListener("DOMContentLoaded", function () {

    showStep(1);

    const nextBtn = document.getElementById("nextBtn");
    const prevBtn = document.getElementById("prevBtn");

    if (nextBtn) {
        nextBtn.addEventListener("click", nextStep);
    }

    if (prevBtn) {
        prevBtn.addEventListener("click", previousStep);
    }

    document
        .querySelectorAll('input[type="radio"]')
        .forEach(radio => {
            radio.addEventListener("change", updateProgress);
        });

    updateProgress();
});

function showStep(stepNumber) {

    document
        .querySelectorAll(".audit-step")
        .forEach(step => {
            step.style.display = "none";
        });

    const currentSection =
        document.querySelector(
            `[data-step="${stepNumber}"]`
        );

    if (currentSection) {
        currentSection.style.display = "block";
    }

    updateHeader(stepNumber);
    updateButtons(stepNumber);

    if (stepNumber === 7) {
        generateReview();
    }

    updateProgress();
}

function nextStep() {

    if (!validateCurrentStep()) {
        return;
    }

    if (currentStep < totalSteps) {

        currentStep++;

        showStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
}

function previousStep() {

    if (currentStep > 1) {

        currentStep--;

        showStep(currentStep);

        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    }
}

function validateCurrentStep() {

    if (currentStep === 7) {
        return true;
    }

    const currentSection =
        document.querySelector(
            `[data-step="${currentStep}"]`
        );

    if (!currentSection) {
        return true;
    }

    const radioGroups = {};

    currentSection
        .querySelectorAll(
            'input[type="radio"]'
        )
        .forEach(radio => {

            radioGroups[radio.name] = true;
        });

    for (const groupName in radioGroups) {

        const selected =
            currentSection.querySelector(
                `input[name="${groupName}"]:checked`
            );

        if (!selected) {

            alert(
                "Please answer all controls in this category before proceeding."
            );

            return false;
        }
    }

    return true;
}

function updateHeader(stepNumber) {

    const title =
        document.getElementById("stepTitle");

    if (!title) return;

    if (stepNumber === 7) {

        title.innerText =
            "Review & Submit";

    } else {

        title.innerText =
            `Step ${stepNumber} of 6 - ${stepTitles[stepNumber]}`;
    }
}

function updateButtons(stepNumber) {

    const prevBtn =
        document.getElementById("prevBtn");

    const nextBtn =
        document.getElementById("nextBtn");

    const submitBtn =
        document.getElementById("submitBtn");

    if (!prevBtn || !nextBtn || !submitBtn) {
        return;
    }

     prevBtn.style.visibility =
    stepNumber === 1
        ? "hidden"
        : "visible";

    if (stepNumber === 7) {

        nextBtn.style.display = "none";
        submitBtn.style.display = "inline-block";

    } else {

        nextBtn.style.display = "inline-block";
        submitBtn.style.display = "none";
    }
}

function updateProgress() {

    const progressBar =
        document.getElementById("progressBar");

    const progressText =
        document.getElementById("progressText");

    if (!progressBar || !progressText) {
        return;
    }

    const totalControls =
        document.querySelectorAll(
            'input[type="radio"][value="Yes"]'
        ).length;

    const answeredControls =
        document.querySelectorAll(
            'input[type="radio"]:checked'
        ).length;

    let percentage = 0;

    if (totalControls > 0) {

        percentage = Math.round(
            (answeredControls / totalControls) * 100
        );
    }

    progressBar.style.width =
        percentage + "%";

    progressText.innerText =
        `${answeredControls} of ${totalControls} controls answered (${percentage}%)`;
}

function generateReview() {

    const reviewContainer =
        document.getElementById("reviewAnswers");

    if (!reviewContainer) {
        return;
    }

    const organizationName =
        document.querySelector(
            'input[name="organization_name"]'
        )?.value || "";

    const industry =
        document.querySelector(
            'input[name="industry"]'
        )?.value || "";

    const employeeCount =
        document.querySelector(
            'input[name="employee_count"]'
        )?.value || "";

    const auditorName =
        document.querySelector(
            'input[name="auditor_name"]'
        )?.value || "";

    const categories = {
        "Access Control": { yes: 0, no: 0 },
        "Network Security": { yes: 0, no: 0 },
        "Data Protection": { yes: 0, no: 0 },
        "Incident Response": { yes: 0, no: 0 },
        "Compliance & Governance": { yes: 0, no: 0 },
        "Asset Management": { yes: 0, no: 0 }
    };

    let totalYes = 0;
    let totalNo = 0;

    document
        .querySelectorAll(
            'input[type="radio"]:checked'
        )
        .forEach(input => {

            const id = input.name;

            let category = "";

            if (id.startsWith("AC")) category = "Access Control";
            else if (id.startsWith("NS")) category = "Network Security";
            else if (id.startsWith("DP")) category = "Data Protection";
            else if (id.startsWith("IR")) category = "Incident Response";
            else if (id.startsWith("CG")) category = "Compliance & Governance";
            else if (id.startsWith("AM")) category = "Asset Management";

            if (input.value === "Yes") {
                categories[category].yes++;
                totalYes++;
            } else {
                categories[category].no++;
                totalNo++;
            }
        });

    let html = `
        <div class="review-card">

            <h3>Organization Information</h3>

            <p><strong>Organization:</strong> ${organizationName}</p>
            <p><strong>Industry:</strong> ${industry}</p>
            <p><strong>Employees:</strong> ${employeeCount}</p>
            <p><strong>Auditor:</strong> ${auditorName}</p>

        </div>

        <div class="review-card">

            <h3>Audit Response Summary</h3>

            <table style="width:100%; border-collapse:collapse;">

                <thead>
                    <tr>
                        <th style="padding:10px; text-align:left;">Category</th>
                        <th style="padding:10px;">Yes</th>
                        <th style="padding:10px;">No</th>
                    </tr>
                </thead>

                <tbody>
    `;

    Object.keys(categories).forEach(category => {

        html += `
            <tr>
                <td style="padding:10px;">${category}</td>
                <td style="text-align:center;">${categories[category].yes}</td>
                <td style="text-align:center;">${categories[category].no}</td>
            </tr>
        `;
    });

    html += `
                </tbody>

            </table>

            <hr style="margin:20px 0;">

            <p><strong>Total Controls:</strong> 30</p>
            <p><strong>Yes Responses:</strong> ${totalYes}</p>
            <p><strong>No Responses:</strong> ${totalNo}</p>

        </div>
    `;

    reviewContainer.innerHTML = html;
}
