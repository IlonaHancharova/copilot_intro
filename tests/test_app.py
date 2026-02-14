
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest_asyncio.fixture(scope="module")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_get_activities(async_client):
    response = await async_client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister(async_client):
    # Sign up a new student
    email = "teststudent@mergington.edu"
    activity = "Chess Club"
    response = await async_client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Try to sign up again (should fail)
    response = await async_client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister the student
    response = await async_client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Try to unregister again (should fail)
    response = await async_client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
