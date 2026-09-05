/**
 * 🚀 Portfolio Data Loader Script
 * 
 * This script dynamically loads user profile data, social links, projects, certifications,
 * education, research papers, and hobbies from JSON files located in the `/Portfolio-Templates/assets/user_data/` directory. 📁
 * 
 * It uses async functions to fetch and parse JSON files, then populates corresponding sections
 * on the portfolio webpage by creating and appending HTML elements. 🖥️✨
 * 
 * Features:
 * - 👤 Loads user info (name, role, bio, skills)
 * - 🔗 Loads social media and professional links with icons
 * - 📂 Displays project cards with images, descriptions, and links
 * - 🎓 Shows certifications with issuer details and certificate links
 * - 🏫 Renders education history as cards
 * - 📄 Lists research papers with links
 * - 🎨 Displays hobbies with icons
 * - ⚠️ Handles error cases by hiding sections gracefully if data is missing or fetch fails
 * 
 * Dependencies:
 * - 🦊 Font Awesome (for icons)
 * - 📐 HTML structure with specific element IDs expected for each section
 * 
 * Usage:
 * - 📜 Include this script on your portfolio page
 * - 📂 Ensure JSON data files are correctly placed in the specified folder
 * - ▶️ Call the load functions as needed to populate the page dynamically
 * 
 * Main Functions:
 * 
 * - async loadUserInfo() 👤
 *   Fetches and displays user personal details like name, role, and bio in the home section.
 * 
 * - async loadSocialLinks() 🔗
 *   Retrieves social media and professional profile links, rendering icons and clickable anchors.
 * 
 * - async loadProjects() 📂
 *   Loads project data including titles, descriptions, images, and repository/demo links as cards.
 * 
 * - async loadCertifications() 🎓
 *   Fetches certifications data and displays issuer, certificate name, and link to certificate PDF or webpage.
 * 
 * - async loadEducation() 🏫
 *   Retrieves educational history and shows degrees, institutions, and duration in a card layout.
 * 
 * - async loadResearchPapers() 📄
 *   Lists research papers or publications with clickable links to download or view.
 * 
 * - async loadHobbies() 🎨
 *   Displays hobbies and interests with matching icons and descriptions.
 * 
 * Author: Madhurima Rawat 👩‍💻
 * Date: 2025-06-03 📅
 */


// 🔗 Select all navigation links
document.querySelectorAll('nav a.nav-link').forEach(link => {
    // 🧏 Add click event listener to each nav link
    link.addEventListener('click', function (e) {
        const href = this.getAttribute('href'); // 🔍 Get the href attribute

        // 🚫 Skip external links or "Home" link (which has target="_blank" or full path)
        if (href.startsWith('http') || href === '{{ site.baseurl }}/' || this.hasAttribute('target')) return;

        e.preventDefault(); // ✋ Prevent default anchor behavior (jump)

        const targetId = href.substring(1); // 🔤 Remove '#' to get target ID
        const target = document.getElementById(targetId); // 🎯 Find the section with that ID
        const offset = 30; // 📏 Offset from the top in pixels

        if (target) {
            const elementPosition = target.getBoundingClientRect().top; // 📐 Element’s position relative to viewport
            const offsetPosition = elementPosition + window.pageYOffset - offset; // 🔢 Final scroll position

            // 🔽 Smoothly scroll to the calculated position
            window.scrollTo({
                top: offsetPosition,
                behavior: 'smooth' // 🌊 Smooth scroll
            });
        }
    });
});


// Paths to JSON files relative to this script location
const basePath = "/Portfolio-Templates/assets/user_data/";

const iconMap = {
    "email-id": "fas fa-envelope",   // 📧 Email icon (Font Awesome Solid)
    "linkedin": "fab fa-linkedin",   // 🔗 LinkedIn icon (Font Awesome Brands)
    "github": "fab fa-github",       // 🐙 GitHub icon (Font Awesome Brands)
    "instagram": "fab fa-instagram", // 📸 Instagram icon (Font Awesome Brands)
    "twitter": "fab fa-twitter",     // 🐦 Twitter icon (Font Awesome Brands)
    "medium": "fab fa-medium",       // ✍️ Medium icon (Font Awesome Brands)
    "devto": "fab fa-dev"            // 💻 Dev.to icon (Font Awesome Brands)
};

async function fetchJSON(filename) {
    // 📂 Fetch a JSON file from the base path + filename
    const response = await fetch(basePath + filename);

    // ❌ Throw error if response is not OK (e.g., 404)
    if (!response.ok) throw new Error(`Failed to fetch ${filename}`);

    // ✅ Parse and return JSON data
    return await response.json();
}

// 🛠️ Helper function to hide a section by its HTML element ID 🆔
function hideSection(id) {
    // 🔍 Find the element with the given ID on the page
    const section = document.getElementById(id);

    // 🙈 If the element exists, hide it by setting CSS display to "none"
    // This removes it from view and layout flow
    if (section) section.style.display = "none";
}


function createSocialLink(name, url) {
    // 🔗 Create anchor element for social link
    const a = document.createElement("a");

    // ✉️ Use mailto: for email, else normal URL
    a.href = name === "email-id" ? `mailto:${url}` : url;

    // 🌐 Open in new tab safely
    a.target = "_blank";
    a.rel = "noopener noreferrer";

    // 🎨 Add CSS class for styling social links
    a.className = "social-link";

    // 🖼️ Create <i> element for Font Awesome icon
    const icon = document.createElement("i");

    // 🎭 Set icon class based on mapping, fallback to envelope icon
    icon.className = iconMap[name] || "fas fa-envelope";

    // 🎯 Add margin to the right for spacing
    icon.style.marginRight = "8px";

    // ➕ Append icon to the anchor element
    a.appendChild(icon);

    // 📝 Append the uppercase, hyphen replaced text (e.g. "EMAIL ID")
    a.appendChild(document.createTextNode(name.replace("-", " ").toUpperCase()));

    // 🔙 Return the fully constructed social link element
    return a;
}


// 📆 Set current year and user name in footer
function setFooter(user) {
    const footerName = document.getElementById("footer-name");
    const footerYear = document.getElementById("footer-year");

    // 🧾 Set current year dynamically
    const year = new Date().getFullYear();
    if (footerYear) footerYear.textContent = year;

    // 👤 Replace '@name' with actual user name or fallback
    if (footerName) footerName.textContent = user.name || "Your Name";
}


// 🧑‍💼 Load and display user info: name, role, bio, skills
async function loadUserInfo() {
    // Helper to hide a section by its ID
    function hideSection(id) {
        const section = document.getElementById(id);
        if (section) {
            section.style.display = "none";
            section.classList.add("hidden"); // Optional: for CSS visibility fallback
        }
    }


    try {
        const user = await fetchJSON("user.json");

        // Check if user has any info to show
        if (user.name || user.role || user.bio || (user.skills && user.skills.length)) {
            // 👤 Set user name, role, bio text content or empty string
            document.getElementById("name").textContent = user.name || "";
            document.getElementById("role").textContent = user.role || "";
            document.getElementById("bio").textContent = user.bio || "";

            const skillsList = document.getElementById("skills-list");
            skillsList.innerHTML = "";

            // 🛠️ Populate skills list if available
            if (user.skills && user.skills.length > 0) {
                user.skills.forEach(skill => {
                    const li = document.createElement("li");
                    li.textContent = skill;
                    skillsList.appendChild(li);
                });
            } else {
                hideSection("skills"); // ❌ Hide Skills if none
            }

            // ✅ Set footer with the user object
            setFooter(user);


        } else {
            // ❌ Hide home and skills section if no user info
            hideSection("home");
            hideSection("skills");
        }

    } catch (error) {
        // 🚫 On error, hide user related sections
        hideSection("home");
        hideSection("skills");
    }
}

// 🌐 Load and display social media/professional links
async function loadSocialLinks() {


    try {
        const social = await fetchJSON("social_links.json");

        const keys = Object.keys(social);
        if (keys.length === 0) throw new Error("Empty social_links.json");

        const socialContainer = document.getElementById("social-links");
        socialContainer.innerHTML = "";

        // 🔗 Create and append each social link element
        keys.forEach(key => {
            socialContainer.appendChild(createSocialLink(key, social[key]));
        });

    } catch (error) {
        // ❌ Hide social section on failure
        hideSection("social");
    }
}

function createProjectCard(project) {
    const card = document.createElement("div");
    card.className = "project-card section-card";

    // ✅ Add project image at the top
    if (project.image) {
        const img = document.createElement("img");
        img.src = project.image;
        img.alt = `${project.name} image`;
        img.className = "project-image section-image";
        card.appendChild(img);
    }

    const title = document.createElement("h3");
    title.className = "project-name section-subheading";
    title.textContent = project.name;

    const description = document.createElement("p");
    description.className = "project-description section-description";
    description.textContent = project.description;

    const tools = document.createElement("p");
    tools.className = "project-tools section-meta";
    tools.textContent = `Tools: ${project.tools}`;

    const links = document.createElement("div");
    links.className = "project-links section-links";

    if (project.link?.live_demo) {
        const demoLink = document.createElement("a");
        demoLink.href = project.link.live_demo;
        demoLink.textContent = "Live Demo";
        demoLink.target = "_blank";
        links.appendChild(demoLink);
    }

    if (project.link?.github) {
        const githubLink = document.createElement("a");
        githubLink.href = project.link.github;
        githubLink.textContent = "GitHub";
        githubLink.target = "_blank";
        links.appendChild(githubLink);
    }

    card.appendChild(title);
    card.appendChild(description);
    card.appendChild(tools);
    card.appendChild(links);

    return card;
}



// 📁 Load and display projects as cards
async function loadProjects() {

    try {
        // Await fetching and parsing JSON
        const response = await fetch(basePath + "projects.json");
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const projects = await response.json();

        // Check if projects is an array and not empty
        if (!Array.isArray(projects) || projects.length === 0) {
            throw new Error("No projects found");
        }

        const projectsList = document.getElementById("projects-list");
        if (!projectsList) throw new Error("Projects list container not found");

        // Clear existing content
        projectsList.innerHTML = "";

        // Append project cards
        projects.forEach(project => {
            projectsList.appendChild(createProjectCard(project));
        });

        // Make sure section is visible
        const section = document.getElementById("projects");
        if (section) section.style.display = "block";

    } catch (error) {
        console.error("Error loading projects:", error);
        // Hide projects section on error or no projects
        hideSection("projects");
    }
}


// 🎓 Load and display certifications
async function loadCertifications() {

    try {
        const certifications = await fetchJSON("certifications.json");

        if (!Array.isArray(certifications) || certifications.length === 0)
            throw new Error("No certifications found");

        const certList = document.getElementById("certifications-list");
        certList.innerHTML = "";

        // 📝 For each certification, create a card with title, issuer, year, and link
        certifications.forEach(cert => {
            const certItem = document.createElement("div");
            certItem.className = "certification-card section-card";

            const title = document.createElement("h3");
            title.className = "cert-title section-subheading";
            title.textContent = cert.title;

            const issuer = document.createElement("p");
            issuer.className = "cert-issuer section-meta";
            issuer.textContent = `Issued by: ${cert.issuer}`;

            const year = document.createElement("p");
            year.className = "cert-year section-description";
            year.textContent = cert.year;

            certItem.appendChild(title);
            certItem.appendChild(year);
            certItem.appendChild(issuer);

            // 🔗 Add certificate link if available
            if (cert.link) {
                const linkP = document.createElement("p");
                linkP.className = "cert-link section-links";

                const linkA = document.createElement("a");
                linkA.href = cert.link;
                linkA.target = "_blank";
                linkA.rel = "noopener noreferrer";
                linkA.textContent = "View Certificate";

                linkP.appendChild(linkA);
                certItem.appendChild(linkP);
            }

            certList.appendChild(certItem);
        });

    } catch (error) {
        // ❌ Hide certifications section if error or none
        hideSection("certifications");
    }
}

// 🎓 Load and display education
async function loadEducation() {
    const sectionId = "education";

    try {
        const education = await fetchJSON("education.json");

        const educationTable = document.getElementById("education-table");
        educationTable.innerHTML = "";

        if (!Array.isArray(education) || education.length === 0) {
            hideSection(sectionId);
            return;
        }

        education.forEach(edu => {
            const eduItem = document.createElement("div");
            eduItem.className = "education-item section-card";

            const degree = document.createElement("h3");
            degree.className = "education-degree section-subheading";
            degree.textContent = edu.degree;

            const institution = document.createElement("p");
            institution.className = "education-institution section-description";
            institution.textContent = edu.institution;

            const year = document.createElement("p");
            year.className = "education-year section-meta";
            year.textContent = edu.year;

            const details = document.createElement("p");
            details.className = "education-details section-description";
            details.textContent = edu.details;

            eduItem.appendChild(degree);
            eduItem.appendChild(institution);
            eduItem.appendChild(year);
            eduItem.appendChild(details);

            educationTable.appendChild(eduItem);
        });

    } catch (error) {
        hideSection(sectionId);  // Hide entire section if JSON is missing or invalid
    }
}

// 📄 Load and display research papers
async function loadResearchPapers() {
    const sectionId = "research";
    try {
        const papers = await fetchJSON("research_papers.json");

        const researchList = document.getElementById("research-papers");
        researchList.innerHTML = "";

        if (!Array.isArray(papers) || papers.length === 0) {
            hideSection(sectionId);
            return;
        }

        papers.forEach(paper => {
            const paperItem = document.createElement("div");
            paperItem.className = "research-paper-item section-card section-description";

            const title = document.createElement("h3");
            title.className = "research-title section-subheading";
            title.textContent = paper.title;

            const publication = document.createElement("p");
            publication.className = "research-publication section-description";
            publication.textContent = `Published in: ${paper.publication}`;

            const year = document.createElement("p");
            year.className = "research-year section-meta";
            year.textContent = paper.year;

            paperItem.appendChild(title);
            paperItem.appendChild(publication);
            paperItem.appendChild(year);

            if (paper.link) {
                const linkP = document.createElement("p");
                linkP.className = "research-link section-links";

                const linkA = document.createElement("a");
                linkA.href = paper.link;
                linkA.target = "_blank";
                linkA.rel = "noopener noreferrer";
                linkA.textContent = "Read Paper";

                linkP.appendChild(linkA);
                paperItem.appendChild(linkP);
            }

            researchList.appendChild(paperItem);
        });

    } catch (error) {
        hideSection(sectionId);
    }
}


// 🎯 Load and display hobbies & interests
async function loadHobbies() {
    const sectionId = "hobbies";
    try {
        const hobbies = await fetchJSON("hobbies.json");

        const hobbiesList = document.getElementById("hobbies-list");
        hobbiesList.innerHTML = "";

        if (!Array.isArray(hobbies) || hobbies.length === 0) {
            hideSection(sectionId);
            return;
        }

        const iconMap = {
            "Photography": "fas fa-camera-retro",
            "Traveling": "fas fa-globe-americas",
            "Creative Writing": "fas fa-pen-nib",
            "Open Source Contribution": "fab fa-github",
            "Sketching & Doodling": "fas fa-pencil-alt",
            "Reading Non-Fiction": "fas fa-book-open"
        };

        hobbies.forEach(hobby => {
            const hobbyItem = document.createElement("div");
            hobbyItem.className = "hobby-card section-card section-description";

            const title = document.createElement("h3");
            title.className = "hobby-title section-subheading";

            const iconClass = iconMap[hobby.title] || "fas fa-star";
            const icon = document.createElement("i");
            icon.className = `${iconClass} hobby-icon`;
            title.appendChild(icon);

            const textSpan = document.createElement("span");
            textSpan.textContent = ` ${hobby.title}`;
            title.appendChild(textSpan);

            const description = document.createElement("p");
            description.className = "hobby-description section-meta";
            description.textContent = hobby.publication;

            hobbyItem.appendChild(title);
            hobbyItem.appendChild(description);

            if (hobby.link) {
                const linkP = document.createElement("p");
                linkP.className = "hobby-link section-links";

                const linkA = document.createElement("a");
                linkA.href = hobby.link;
                linkA.target = "_blank";
                linkA.rel = "noopener noreferrer";
                linkA.textContent = "Read More";

                linkP.appendChild(linkA);
                hobbyItem.appendChild(linkP);
            }

            hobbiesList.appendChild(hobbyItem);
        });

    } catch (error) {
        hideSection(sectionId);
    }
}


// 🚀 Main function to load the entire portfolio by calling each loader
async function loadPortfolio() {
    await loadUserInfo();
    await loadSocialLinks();
    await loadProjects();
    await loadCertifications();
    await loadEducation();
    await loadResearchPapers();
    await loadHobbies();
}

document.addEventListener("DOMContentLoaded", loadPortfolio);


// Toggle dark mode by adding/removing a class on the body
function toggleDarkMode() {
    const darkModeToggle = document.querySelector('a[href="#mode"]');
    const icon = darkModeToggle.querySelector("i");

    // Get the text node after the icon
    let textNode = darkModeToggle.childNodes[1];
    if (!textNode || textNode.nodeType !== Node.TEXT_NODE) {
        for (const node of darkModeToggle.childNodes) {
            if (node.nodeType === Node.TEXT_NODE && node.textContent.trim().length > 0) {
                textNode = node;
                break;
            }
        }
    }

    const isDark = document.body.classList.toggle("dark-mode");

    // Update icon and label
    if (isDark) {
        icon.classList.replace("fa-moon", "fa-sun");
        if (textNode) textNode.textContent = " Light Mode";
        localStorage.setItem("Portfolio-Templates-darkMode", "enabled");
    } else {
        icon.classList.replace("fa-sun", "fa-moon");
        if (textNode) textNode.textContent = " Dark Mode";
        localStorage.setItem("Portfolio-Templates-darkMode", "disabled");
    }
}

// Initialize dark mode based on localStorage or system preference
function initDarkMode() {
    const darkModeToggle = document.querySelector('a[href="#mode"]');
    const icon = darkModeToggle.querySelector("i");

    // Use localStorage if available, else use system preference
    const savedMode = localStorage.getItem("Portfolio-Templates-darkMode");
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;

    let isDark = false;
    if (savedMode === "enabled") {
        isDark = true;
    } else if (savedMode === "disabled") {
        isDark = false;
    } else {
        isDark = prefersDark;
    }

    if (isDark) {
        document.body.classList.add("dark-mode");
        icon.classList.replace("fa-moon", "fa-sun");
        darkModeToggle.childNodes[1].textContent = " Light Mode";
    } else {
        document.body.classList.remove("dark-mode");
        icon.classList.replace("fa-sun", "fa-moon");
        darkModeToggle.childNodes[1].textContent = " Dark Mode";
    }
}


// Attach event listener on DOM ready
document.addEventListener("DOMContentLoaded", () => {
    initDarkMode();

    const darkModeToggle = document.querySelector('a[href="#mode"]');
    darkModeToggle.addEventListener("click", e => {
        e.preventDefault();
        toggleDarkMode();
    });
});

