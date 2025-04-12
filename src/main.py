from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .db import engine, yield_db
from .model import Base, UserSwiftDB
from .fetch_xlsx import parse_and_load_xlsx
from .crud import get_unique_swift_code, create_swift_code
from .pydantic_structure import SwiftCodeResponse, SwiftCodeRecord, CountrySwiftCodesResponse, CreateNewData

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

# TODO: fix for branches
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

@app.get("/v1/swift-codes/country/{countryISO2code}")
def read_swift_codes_by_country(countryISO2code: str, db: Session = Depends(yield_db)):
    records = db.query(UserSwiftDB).filter(UserSwiftDB.country_iso2 == countryISO2code.upper()).all()
    if not records:
        raise HTTPException(status_code=404, detail="No SWIFT codes found for this country")
    
    country_name = records[0].country_name.upper()
    swift_codes = [
        SwiftCodeRecord(
            swiftCode=record.swift_code,
            bankName=record.bank_name,
            address=record.address,
            countryISO2=record.country_iso2,
            isHeadquarter=record.is_headquarter
        )
        for record in records
    ]
    return CountrySwiftCodesResponse(
        countryISO2=countryISO2code.upper(),
        countryName=country_name,
        swiftCodes=swift_codes
    )

@app.post("/v1/swift-codes", response_model=dict)
def create_swift_code_endpoint(payload: CreateNewData, db: Session = Depends(yield_db)):
    if get_unique_swift_code(db, payload.swift_code):
        raise HTTPException(status_code=400, detail="SWIFT code already exists")
    new_data = create_swift_code(db, payload.dict())
    return {"message": f"Record with swift code {new_data.swift_code} created successfully."}

@app.delete("/v1/swift-codes/{swift_code}")
def delete_swift_code(swift_code: str, db: Session = Depends(yield_db)):
    record = get_unique_swift_code(db, swift_code)
    if not record:
        raise HTTPException(status_code=404, detail="SWIFT code not found")
    db.delete(record)
    db.commit()
    return {"message": f"Data associated with SWIFT code {swift_code} deleted successfully."}