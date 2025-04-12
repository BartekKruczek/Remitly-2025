from pydantic import BaseModel, Field
from typing import List

class SwiftCodeRecord(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    isHeadquarter: bool

class SwiftCodeResponse(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    branches: List[SwiftCodeRecord] = Field(default_factory=list)

class CountrySwiftCodesResponse(BaseModel):
    countryISO2: str
    countryName: str
    swiftCodes: List[SwiftCodeRecord]

class CreateNewData(BaseModel):
    swift_code: str
    bank_name: str
    address: str
    country_iso2: str
    country_name: str
    is_headquarter: bool