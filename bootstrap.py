import os

files = {
    "AGENT.md": """# AI Coding Agent Guidelines

## Stack & Constraints
- Frontend: HTML5, Tailwind CSS (CDN), Vanilla JavaScript.
- Backend: Python 3.10+, FastAPI, Uvicorn, Pydantic.
- Style: Modern dark-mode SaaS UI (zinc-950 background, zinc-100 text).

## Rules
1. Keep frontend and backend strictly decoupled.
2. All Python functions must include type hints.
3. API endpoints must return valid JSON.
""",
    ".gitignore": """__pycache__/
*.py[cod]
venv/
.venv/
.env
.vscode/
.DS_Store
""",
    "README.md": """# Personal Portfolio & API

Full-stack personal website with FastAPI backend and Tailwind CSS frontend.

## Setup Instructions

### Backend
1. cd backend
2. python3 -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. uvicorn main:app --reload

FastAPI Interactive Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend
Open `frontend/index.html` directly in your browser.
""",
    "backend/requirements.txt": """fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.6.0
""",
    "backend/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Personal Website API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/api/projects")
def get_projects() -> list[dict]:
    return [
        {
            "id": 1,
            "title": "Personal Portfolio",
            "description": "Full-stack personal website with FastAPI backend and modern SaaS dark theme.",
            "tags": ["Python", "FastAPI", "Tailwind CSS", "JavaScript"],
            "demo_url": "#",
            "github_url": "#"
        }
    ]

@app.post("/api/contact")
def receive_contact(payload: ContactMessage) -> dict[str, str]:
    print(f"Received message from {payload.name} ({payload.email}): {payload.message}")
    return {"status": "success", "message": "Message received!"}
""",
    "frontend/index.html": """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Software Engineer Portfolio</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 500: '#3b82f6', 600: '#2563eb' }
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-zinc-950 text-zinc-100 font-sans antialiased min-h-screen">
    <nav class="border-b border-zinc-800 bg-zinc-900/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
            <span class="font-bold text-lg tracking-tight">Portfolio</span>
            <div class="space-x-6 text-sm text-zinc-400">
                <a href="#about" class="hover:text-zinc-100 transition">About</a>
                <a href="#projects" class="hover:text-zinc-100 transition">Projects</a>
                <a href="#skills" class="hover:text-zinc-100 transition">Skills</a>
                <a href="#contact" class="hover:text-zinc-100 transition">Contact</a>
            </div>
        </div>
    </nav>

    <main class="max-w-5xl mx-auto px-6 py-12 space-y-24">
        <section id="about" class="space-y-4">
            <span class="px-3 py-1 rounded-full text-xs font-medium bg-zinc-800 text-zinc-300 border border-zinc-700">Software Engineer</span>
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight">Building robust full-stack applications.</h1>
            <p class="text-zinc-400 max-w-2xl text-lg">Focusing on modern web engineering, clean architecture, and Python backends.</p>
        </section>

        <section id="projects" class="space-y-6">
            <h2 class="text-2xl font-bold tracking-tight">Projects</h2>
            <div id="projects-container" class="grid sm:grid-cols-2 gap-6"></div>
        </section>

        <section id="skills" class="space-y-6">
            <h2 class="text-2xl font-bold tracking-tight">Tech Stack</h2>
            <div class="flex flex-wrap gap-2">
                <span class="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm">Python</span>
                <span class="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm">FastAPI</span>
                <span class="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm">JavaScript</span>
                <span class="px-3 py-1.5 rounded-md bg-zinc-900 border border-zinc-800 text-sm">Tailwind CSS</span>
            </div>
        </section>

        <section id="contact" class="space-y-6 max-w-xl">
            <h2 class="text-2xl font-bold tracking-tight">Get in Touch</h2>
            <form id="contact-form" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium text-zinc-400 mb-1">Name</label>
                    <input type="text" id="contact-name" required class="w-full rounded-lg bg-zinc-900 border border-zinc-800 px-4 py-2 text-zinc-100">
                </div>
                <div>
                    <label class="block text-sm font-medium text-zinc-400 mb-1">Email</label>
                    <input type="email" id="contact-email" required class="w-full rounded-lg bg-zinc-900 border border-zinc-800 px-4 py-2 text-zinc-100">
                </div>
                <div>
                    <label class="block text-sm font-medium text-zinc-400 mb-1">Message</label>
                    <textarea id="contact-message" rows="4" required class="w-full rounded-lg bg-zinc-900 border border-zinc-800 px-4 py-2 text-zinc-100"></textarea>
                </div>
                <button type="submit" class="bg-zinc-100 text-zinc-950 px-5 py-2.5 rounded-lg font-medium hover:bg-zinc-200 transition">Send Message</button>
            </form>
        </section>
    </main>

    <script src="app.js"></script>
</body>
</html>
""",
    "frontend/app.js": """const API_BASE_URL = "[http://127.0.0.1:8000/api](http://127.0.0.1:8000/api)";

async function fetchProjects() {
    const container = document.getElementById("projects-container");
    try {
        const response = await fetch(`${API_BASE_URL}/projects`);
        const projects = await response.json();

        container.innerHTML = projects.map(project => `
            <div class="p-6 rounded-xl bg-zinc-900/50 border border-zinc-800 space-y-4">
                <h3 class="text-xl font-bold text-zinc-100">${project.title}</h3>
                <p class="text-zinc-400 text-sm">${project.description}</p>
                <div class="flex flex-wrap gap-2">
                    ${project.tags.map(tag => `<span class="text-xs px-2 py-0.5 rounded bg-zinc-800 text-zinc-300">${tag}</span>`).join('')}
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error("Failed to fetch projects:", error);
        container.innerHTML = `<p class="text-red-400 text-sm">Unable to load projects from server.</p>`;
    }
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
        } else {
            alert("Failed to send message.");
        }
    } catch (error) {
        console.error("Error submitting form:", error);
        alert("Server unreachable.");
    }
});

document.addEventListener("DOMContentLoaded", fetchProjects);
"""
}

for path, content in files.items():
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Personal website scaffold successfully created!")