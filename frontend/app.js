
const fileInput = document.getElementById("resumeFile");
const matchButton = document.getElementById("matchButton");
const status = document.getElementById("status");

const profileSection = document.getElementById("profileSection");
const jobsSection = document.getElementById("jobsSection");

const skillsContainer = document.getElementById("skills");
const researchInterest = document.getElementById("researchInterest");

const jobsContainer = document.getElementById("jobsContainer");
const jobCount = document.getElementById("jobCount");


matchButton.addEventListener("click", async function () {

    const file = fileInput.files[0];

    if (!file) {
        status.textContent = "Please select a PDF resume.";
        return;
    }

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        status.textContent = "Only PDF resumes are supported.";
        return;
    }

    status.textContent = "Uploading resume and finding jobs...";
    matchButton.disabled = true;

    profileSection.classList.add("hidden");
    jobsSection.classList.add("hidden");

    const formData = new FormData();
    formData.append("file", file);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/upload-resume",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {
            throw new Error("Backend returned an error: " + response.status);
        }

        const data = await response.json();

        console.log("API response:", data);

        if (!data.profile) {
            throw new Error("Resume profile was not returned.");
        }

        displayProfile(data.profile);

        if (data.matched_jobs) {
            displayJobs(data.matched_jobs);
        } else {
            throw new Error("No matched jobs were returned.");
        }

        status.textContent =
            `Done. Found ${data.matched_jobs.length} matching jobs.`;

    } catch (error) {

        console.error("Error:", error);

        status.textContent =
            "Error: " + error.message;

    } finally {

        matchButton.disabled = false;
    }
});


function displayProfile(profile) {

    profileSection.classList.remove("hidden");

    skillsContainer.innerHTML = "";

    if (profile.skills && profile.skills.length > 0) {

        profile.skills.forEach(function (skill) {

            const skillElement = document.createElement("span");

            skillElement.className = "skill";
            skillElement.textContent = skill;

            skillsContainer.appendChild(skillElement);
        });

    } else {

        skillsContainer.textContent = "No skills detected.";
    }


    researchInterest.textContent =
        profile.research_interest || "Not available.";
}


function displayJobs(jobs) {

    jobsSection.classList.remove("hidden");

    jobsContainer.innerHTML = "";

    jobCount.textContent = `${jobs.length} jobs`;


    jobs.forEach(function (item, index) {

        const job = item;
        const match = item.match;

        const card = document.createElement("div");

        card.className = "job-card";


        let location = job.location;

        if (Array.isArray(location)) {
            location = location.join(", ");
        }


        let score = "Unable to evaluate";

        if (match && match.score !== null && match.score !== undefined) {
            score = `${match.score}%`;
        }


        let matchedSkills = "None";

        if (
            match &&
            match.matched_skills &&
            match.matched_skills.length > 0
        ) {
            matchedSkills = match.matched_skills.join(", ");
        }


        let missingSkills = "None";

        if (
            match &&
            match.missing_skills &&
            match.missing_skills.length > 0
        ) {
            missingSkills = match.missing_skills.join(", ");
        }


        const reason =
            match && match.reason
                ? match.reason
                : "No reason available.";


        card.innerHTML = `
            <h3>
                ${index + 1}. ${escapeHTML(job.title)}
            </h3>

            <div class="company">
                ${escapeHTML(job.company)}
            </div>

            <div class="location">
                ${escapeHTML(location)}
            </div>

            <div class="match-score">
                Match: ${escapeHTML(score)}
            </div>

            <div class="matched">
                <strong>Matched skills:</strong>
                ${escapeHTML(matchedSkills)}
            </div>

            <div class="missing">
                <strong>Missing skills:</strong>
                ${escapeHTML(missingSkills)}
            </div>

            <p class="reason">
                ${escapeHTML(reason)}
            </p>

            <a
                class="apply-button"
                href="${job.application_link}"
                target="_blank"
                rel="noopener noreferrer"
            >
                Apply
            </a>
        `;


        jobsContainer.appendChild(card);

    });
}


function escapeHTML(value) {

    if (value === null || value === undefined) {
        return "";
    }

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
