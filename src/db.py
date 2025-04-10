import os

# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL")

# create engine
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define db
class DB:
    def __init__(self):
        self.session = SessionLocal()

    def yield_db(self):
        try:
            yield self.session
        finally:
            self.session.close()


db = DB()