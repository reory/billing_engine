# Dependencies module:
# A place to put shared FastAPI dependency functions so they’re not
# duplicated across routers.

from app.database import SessionLocal

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
