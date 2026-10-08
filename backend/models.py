import uuid
from datetime import datetime, timezone

from database import Base
from sqlalchemy import JSON, Column, DateTime, Integer, String


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tags = Column(JSON, nullable=False, default=list)
    demo_url = Column(String, default="#")
    github_url = Column(String, default="#")