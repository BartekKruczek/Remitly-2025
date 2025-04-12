import os

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@db:5432/mydb")

# create engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define db
def yield_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()