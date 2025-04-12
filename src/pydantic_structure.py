from pydantic import BaseModel
from typing import List

class SwiftCodeResponse(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool

class SwiftCodeRecord(BaseModel):
    swiftCode: str
    bankName: str
    address: str
    countryISO2: str
    isHeadquarter: bool

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