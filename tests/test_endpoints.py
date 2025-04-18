import pytest
import httpx

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List

from src.model import UserSwiftDB

BASE_URL = "http://localhost:8080"
DATABASE_URL = "postgresql://postgres:password@db:5432/mydb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

with SessionLocal() as db:
    swift_code_list: List[str] = [row[0] for row in db.query(UserSwiftDB.swift_code).all()]
    iso2_list: List[str] = [row[0] for row in db.query(UserSwiftDB.country_iso2).distinct().all()]


@pytest.mark.asyncio
@pytest.mark.parametrize("swift_code", swift_code_list)
async def test_get_swift_code_with_branches(swift_code):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v1/swift-codes/{swift_code}")
        assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
        data = response.json()
        assert data.get("swiftCode") == swift_code
        assert isinstance(data.get("branches"), list)
        assert isinstance(data.get("bankName"), str)
        assert isinstance(data.get("address"), str)
        assert isinstance(data.get("countryISO2"), str)
        assert isinstance(data.get("countryName"), str)
        assert isinstance(data.get("isHeadquarter"), bool)

@pytest.mark.asyncio
@pytest.mark.parametrize("iso2_code", iso2_list)
async def test_get_iso2_code(iso2_code):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v1/swift-codes/country/{iso2_code}")
        assert response.status_code == 200, f"Got {response.status_code}: {response.text}"
        
        data = response.json()

        assert data["countryISO2"] == iso2_code.upper()
        assert isinstance(data["countryName"], str)
        assert isinstance(data["swiftCodes"], list)


@pytest.mark.asyncio
async def test_create_swift_code():
    new_data = {
        "swift_code": "FAKECODE123",
        "bank_name": "Fake Bank",
        "address": "123 Fake St",
        "country_iso2": "FB",
        "country_name": "FakeCountry",
        "is_headquarter": True
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/v1/swift-codes", json=new_data)
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "FAKECODE123" in data["message"]

        get_response = await client.get(f"{BASE_URL}/v1/swift-codes/{new_data['swift_code']}")
        assert get_response.status_code == 200
        get_data = get_response.json()
        assert get_data["swiftCode"] == "FAKECODE123"
        assert get_data["bankName"] == "Fake Bank"
        assert get_data["address"] == "123 Fake St"
        assert get_data["countryISO2"] == "FB"
        assert get_data["countryName"] == "FakeCountry"
        assert get_data["isHeadquarter"] == True


@pytest.mark.asyncio
async def test_create_swift_code_already_exists():
    existing_swift_code = "AAISALTRXXX" # is in database
    new_data = {
        "swift_code": existing_swift_code,
        "bank_name": "Some Bank",
        "address": "No matter",
        "country_iso2": "SB",
        "country_name": "SomeCountry",
        "is_headquarter": False
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/v1/swift-codes", json=new_data)
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "SWIFT code already exists"

@pytest.mark.asyncio
async def test_delete_swift_code():
    new_code = "DELETEME1"
    new_data = {
        "swift_code": new_code,
        "bank_name": "To Be Deleted",
        "address": "Temp 123",
        "country_iso2": "XX",
        "country_name": "XTEST",
        "is_headquarter": False
    }
    async with httpx.AsyncClient() as client:
        create_resp = await client.post(f"{BASE_URL}/v1/swift-codes", json=new_data)
        assert create_resp.status_code == 200
        
        delete_resp = await client.delete(f"{BASE_URL}/v1/swift-codes/{new_code}")
        assert delete_resp.status_code == 200
        delete_data = delete_resp.json()
        assert f"Data associated with SWIFT code {new_code} deleted successfully." in delete_data["message"]

        get_resp = await client.get(f"{BASE_URL}/v1/swift-codes/{new_code}")
        assert get_resp.status_code == 404
        get_data = get_resp.json()
        assert get_data["detail"] == "SWIFT code not found"

@pytest.mark.asyncio
async def test_delete_swift_code_not_found():
    non_existing_code = "NONEXISTENTCODE" # does not exist in database
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/v1/swift-codes/{non_existing_code}")
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "SWIFT code not found"