from fastapi.testclient import TestClient
from dependency_injector import providers
from app.main import app
from app.core.container import Container
from app.core.dependencies import get_current_user

client = TestClient(app)

def dummy_current_user():
    return {"id": "dummy", "email": "dummy@example.com", "name": "Dummy User"}

app.dependency_overrides[get_current_user] = dummy_current_user
Container.auth_service.override(providers.Object(Container.auth_service.provider()))

# Menghapus data testing
def cleanup_test_user(email: str):
    get_response = client.get(f"/api/v1/users/email/{email}")
    if get_response.status_code == 200:
        user_data = get_response.json().get("data")
        if user_data and "id" in user_data:
            user_id = user_data["id"]
            client.delete(f"/api/v1/users/{user_id}")

# Test untuk register endpoint sukses
def test_auth_register_success():
    payload = {
        "email": "usertest@example.com",
        "name": "User Test",
        "password": "Password123!",
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "User Registered Successfully"

# Test untuk register endpoint gagal (tidak lengkap datanya)
def test_auth_register_missing_field():
    payload = {
        "name": "User Test",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 422

# Test untuk login endpoint sukses
def test_auth_login_success():
    login_payload = {
        "email": "usertest@example.com",
        "password": "Password123!"
    }
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 200
    json_data = login_response.json()
    assert json_data["message"] == "User Logged In Successfully"
    assert "access_token" in json_data["token"]
    cleanup_test_user("usertest@example.com")
    
# Test untuk login endpoint gagal (salah email atau passwordnya (credentialnya))
def test_auth_login_invalid_credentials():
    login_payload = {
        "email": "nonexistent@example.com",
        "password": "WrongPassword!"
    }
    login_response = client.post("/api/v1/auth/login", json=login_payload)
    assert login_response.status_code == 401

# Test untuk logout endpoint sukses
def test_auth_logout():
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully signed out"
