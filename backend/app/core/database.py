from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# The engine manages the actual pool of connections to MySQL.
# pool_pre_ping checks a connection is alive before handing it out,
# which avoids "MySQL server has gone away" errors after idle time.
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Each request gets its own Session (a "workspace" for queries/changes).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All ORM models inherit from this Base so SQLAlchemy knows about them.
Base = declarative_base()


def get_db():
    """
    FastAPI dependency: yields a DB session for a single request,
    then always closes it afterwards — even if the request raised.
    Use like: def endpoint(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
