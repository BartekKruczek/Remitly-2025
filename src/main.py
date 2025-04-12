from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from .db import engine, yield_db
from .model import Base
from .fetch_xlsx import parse_and_load_xlsx
from .crud import get_unique_swift_code

app = FastAPI()
Base.metadata.create_all(bind=engine)

class SwiftCodeResponse(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool

@app.on_event("startup")
def startup():
    print("Starting up app...")

    # next because it's a generator
    db = next(yield_db())
    parse_and_load_xlsx(db, "Interns_2025_SWIFT_CODES.xlsx")
    print("Database connected")

    # TODO : add check if db is empty, if not then load data

@app.get("/v1/swift-codes/{swift_code}")
def read_swift_code(swift_code: str, db: Session = Depends(yield_db)):
    record = get_unique_swift_code(db, swift_code)
    if not record:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    return SwiftCodeResponse(
        swiftCode=record.swift_code,
        bankName=record.bank_name,
        address=record.address,
        countryISO2=record.country_iso2,
        countryName=record.country_name,
        isHeadquarter=record.is_headquarter
    )

@app.delete("/v1/swift-codes/{swift_code}")
def delete_swift_code(swift_code: str, db: Session = Depends(yield_db)):
    record = get_unique_swift_code(db, swift_code)
    if not record:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    db.delete(record)
    db.commit()
    return {"message": f"Data associated with SWIFT code {swift_code} deleted successfully."}