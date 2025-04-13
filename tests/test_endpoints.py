import pytest
import httpx

BASE_URL = "http://localhost:8080"

@pytest.mark.asyncio
async def test_get_swift_code_with_branches():
    # TODO: iterate over entire db, not only one example
    swift_code = "ALBPPLP1BMW"
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