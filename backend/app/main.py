from fastapi import FastAPI

from app.core.database import Base, engine
from app import models  # noqa: F401 - registers all models with Base

app = FastAPI(title="School Management API")


@app.on_event("startup")
def on_startup():
    # In development this auto-creates tables from our models if they
    # don't exist yet. In production you'd use Alembic migrations
    # instead of create_all, since this doesn't handle schema changes.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "ok"}
