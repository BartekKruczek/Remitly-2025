from fastapi import FastAPI
from .db import engine, yield_db
from .model import Base
from .fetch_xlsx import parse_and_load_xlsx

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    print("Starting up app...")

    # next because it's a generator
    db = next(yield_db())
    parse_and_load_xlsx(db, "Interns_2025_SWIFT_CODES.xlsx")
    print("Database connected")

    # TODO : add check if db is empty, if not then load data

@app.get("/")
def home():
    return {"status": "ok", "message": "Hello from Docker + FastAPI!"}