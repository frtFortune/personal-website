import os
from typing import Annotated, Any

from database import Base, engine, get_db
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import MessageModel, ProjectModel
from pydantic import BaseModel
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

raw_origins = os.getenv("ALLOWED_ORIGINS", "*")

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "dev-secret-key")

app = FastAPI(title="Personal Website API")

DbSession = Annotated[Session, Depends(get_db)]

class ProjectCreate(BaseModel):
    title: str
    description: str
    tags: str
    link: str
    image_url: str | None = None


# Dependency to check X-API-Key header
def verify_admin_key(x_api_key: str = Header(...)):
    if x_api_key != ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin API key"
        )
    return x_api_key


# Clean up origins: strip leading/trailing whitespace and trailing slashes
if raw_origins.strip() == "*":
    allowed_origins = ["*"]
else:
    allowed_origins = [
        origin.strip().rstrip("/") 
        for origin in raw_origins.split(",") 
        if origin.strip()
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactMessage(BaseModel):
    name: str
    email: str
    message: str


def seed_projects(db: Session) -> None:
    if db.query(ProjectModel).count() == 0:
        initial_projects = [
            ProjectModel(
                title="Personal Portfolio Website",
                description="Full-stack decoupled web application built with a FastAPI backend and a modern SaaS dark-theme frontend.",
                tags=["Python", "FastAPI", "Tailwind CSS", "JavaScript"],
                demo_url="#",
                github_url="#",
            ),
            ProjectModel(
                title="Local AI Code Assistant Integrator",
                description="Spec-driven CLI automation tool for local LLM inference and code scaffolding using Ollama.",
                tags=["Python", "AI", "Ollama", "CLI"],
                demo_url="#",
                github_url="#",
            ),
            ProjectModel(
                title="SaaS Metrics Dashboard",
                description="Real-time analytics dashboard monitoring server response times, uptime, and user event streams.",
                tags=["JavaScript", "Tailwind CSS", "FastAPI"],
                demo_url="#",
                github_url="#",
            ),
        ]
        db.add_all(initial_projects)
        db.commit()


@app.on_event("startup")
def startup_event() -> None:
    db = next(get_db())
    try:
        seed_projects(db)
    finally:
        db.close()


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/api/projects")
def get_projects(db: DbSession, tag: str | None = None) -> list[dict[str, Any]]:
    projects = db.query(ProjectModel).all()
    project_list = [
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "tags": p.tags,
            "demo_url": p.demo_url,
            "github_url": p.github_url,
        }
        for p in projects
    ]

    if tag:
        normalized_tag = tag.lower()
        return [
            p
            for p in project_list
            if any(t.lower() == normalized_tag for t in p["tags"])
        ]
    return project_list


@app.post("/api/projects")
def create_project(payload: ProjectCreate, db: DbSession) -> dict[str, Any]:
    new_project = ProjectModel(
        title=payload.title,
        description=payload.description,
        tags=payload.tags,
        demo_url=payload.demo_url,
        github_url=payload.github_url,
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return {
        "status": "success",
        "project": {
            "id": new_project.id,
            "title": new_project.title,
            "description": new_project.description,
            "tags": new_project.tags,
            "demo_url": new_project.demo_url,
            "github_url": new_project.github_url,
        },
    }


@app.post("/api/contact")
def receive_contact(payload: ContactMessage, db: DbSession) -> dict[str, str]:
    new_message = MessageModel(
        name=payload.name,
        email=payload.email,
        message=payload.message,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return {"status": "success", "message": "Message saved to database!"}


@app.get("/api/messages")
def get_messages(db: DbSession) -> list[dict[str, Any]]:
    messages = db.query(MessageModel).order_by(MessageModel.created_at.desc()).all()
    return [
        {
            "id": msg.id,
            "name": msg.name,
            "email": msg.email,
            "message": msg.message,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }
        for msg in messages
    ]