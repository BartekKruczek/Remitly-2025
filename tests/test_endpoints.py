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
        assert response.status_code == 200, f"Niepoprawny status {response.status_code}"
        
        data = response.json()

        assert data["countryISO2"] == iso2_code.upper()
        # TODO: add more assertions