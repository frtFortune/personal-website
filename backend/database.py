from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite database file stored inside the backend folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./portfolio.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite with FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()