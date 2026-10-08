const API_BASE_URL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000/api"
    : "https://personal-website-api.onrender.com/api";
let activeTag = null;

async function fetchProjects(tag = null) {
    const container = document.getElementById("projects-container");
    try {
        const url = tag ? `${API_BASE_URL}/projects?tag=${encodeURIComponent(tag)}` : `${API_BASE_URL}/projects`;
        const response = await fetch(url);
        const projects = await response.json();

        if (projects.length === 0) {
            container.innerHTML = `<p class="text-zinc-500 text-sm col-span-2">No projects found tagged "${escapeHtml(tag)}".</p>`;
            return;
        }

        container.innerHTML = projects.map(project => `
            <div class="p-6 rounded-xl bg-zinc-900/50 border border-zinc-800 space-y-4">
                <h3 class="text-xl font-bold text-zinc-100">${escapeHtml(project.title)}</h3>
                <p class="text-zinc-400 text-sm">${escapeHtml(project.description)}</p>
                <div class="flex flex-wrap gap-2">
                    ${project.tags.map(t => `
                        <button onclick="filterByTag('${escapeHtml(t)}')" class="text-xs px-2 py-0.5 rounded bg-zinc-800 hover:bg-zinc-700 text-zinc-300 transition">
                            ${escapeHtml(t)}
                        </button>
                    `).join('')}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Failed to fetch projects:", error);
        container.innerHTML = `<p class="text-red-400 text-sm">Unable to load projects from server.</p>`;
    }
}

function filterByTag(tag) {
    activeTag = tag;
    renderFilterBar();
    fetchProjects(tag);
}

function resetFilter() {
    activeTag = null;
    renderFilterBar();
    fetchProjects();
}

function renderFilterBar() {
    const filterContainer = document.getElementById("filter-bar");
    if (!filterContainer) return;

    const tags = ["All", "Python", "FastAPI", "Tailwind CSS", "JavaScript", "AI"];
    filterContainer.innerHTML = tags.map(t => {
        const isActive = (t === "All" && !activeTag) || (t === activeTag);
        const clickHandler = t === "All" ? "resetFilter()" : `filterByTag('${t}')`;
        return `
            <button onclick="${clickHandler}" 
                class="px-3 py-1 rounded-md text-xs font-medium transition ${
                    isActive 
                    ? 'bg-zinc-100 text-zinc-950 font-semibold' 
                    : 'bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-zinc-100'
                }">
                ${t}
            </button>
        `;
    }).join('');
}

async function fetchMessages() {
    const listContainer = document.getElementById("messages-list");
    listContainer.innerHTML = `<p class="text-zinc-500 text-sm">Loading submissions...</p>`;

    try {
        const response = await fetch(`${API_BASE_URL}/messages`);
        const messages = await response.json();

        const badge = document.getElementById("message-badge");
        if (badge) {
            badge.textContent = messages.length;
            badge.classList.toggle("hidden", messages.length === 0);
        }

        if (!messages || messages.length === 0) {
            listContainer.innerHTML = `<p class="text-zinc-500 text-sm text-center py-8">No messages recorded yet.</p>`;
            return;
        }

        const sorted = [...messages].reverse();
        listContainer.innerHTML = sorted.map(msg => {
            const dateStr = msg.created_at ? new Date(msg.created_at).toLocaleString() : 'Unknown timestamp';
            return `
                <div class="p-4 rounded-xl bg-zinc-950/80 border border-zinc-800/80 space-y-2">
                    <div class="flex items-center justify-between">
                        <span class="font-semibold text-zinc-200 text-sm">${escapeHtml(msg.name)}</span>
                        <span class="text-[11px] text-zinc-500 font-mono">${dateStr}</span>
                    </div>
                    <div class="text-xs text-blue-400 font-mono">${escapeHtml(msg.email)}</div>
                    <p class="text-sm text-zinc-300 whitespace-pre-wrap pt-1">${escapeHtml(msg.message)}</p>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error("Failed to load messages:", error);
        listContainer.innerHTML = `<p class="text-red-400 text-sm">Error connecting to backend API.</p>`;
    }
}

function openMessagesModal() {
    document.getElementById("messages-modal").classList.remove("hidden");
    fetchMessages();
}

function closeMessagesModal() {
    document.getElementById("messages-modal").classList.add("hidden");
}

function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/[&<>"']/g, (m) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    })[m]);
}

document.getElementById("contact-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = {
        name: document.getElementById("contact-name").value,
        email: document.getElementById("contact-email").value,
        message: document.getElementById("contact-message").value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("Message sent successfully!");
            e.target.reset();
            fetchMessages(); // Refresh background counter & modal state
        } else {
            alert("Failed to send message.");
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Server unreachable.");
    }
});

document.addEventListener("DOMContentLoaded", () => {
    renderFilterBar();
    fetchProjects();
    fetchMessages();
});