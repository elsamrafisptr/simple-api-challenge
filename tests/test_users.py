from fastapi.testclient import TestClient
from dependency_injector import providers
from app.main import app
from app.core.container import Container
from app.core.dependencies import get_current_user

client = TestClient(app)

Container.auth_service.override(providers.Object(Container.auth_service.provider()))
Container.user_service.override(providers.Object(Container.user_service.provider()))

# Fungsi untuk register user testing/dummy 
def register_test_user(email: str, name: str, password: str):
    payload = {
        "email": email,
        "name": name,
        "password": password,
        "confirm_password": password
    }
    return client.post("/api/v1/auth/register", json=payload)

# Menghapus data testing
def cleanup_test_user(email: str):
    get_response = client.get(f"/api/v1/users/email/{email}")
    if get_response.status_code == 200:
        user_data = get_response.json().get("data")
        if user_data and "id" in user_data:
            user_id = user_data["id"]
            client.delete(f"/api/v1/users/{user_id}")

# Test untuk get all users endpoint sukses
def test_get_all_users_success():
    response = client.get("/api/v1/users/?page=1&limit=5&sort=created_at&order=asc")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "Users retrieved successfully"
    assert isinstance(json_data["data"], list)
    assert "pagination" in json_data

# Test untuk get user by email endpoint sukses
def test_get_user_by_email_success():
    email = "user_test_email@example.com"
    reg_resp = register_test_user(email, "User Test Email", "Password123!")
    assert reg_resp.status_code == 201
    response = client.get(f"/api/v1/users/email/{email}")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "User retrieved successfully"
    assert json_data["data"]["email"] == email
    cleanup_test_user(email)

# Test untuk get user by email endpoint gagal 
def test_get_user_by_email_not_found():
    response = client.get("/api/v1/users/email/nonexistent@example.com")
    assert response.status_code == 404

# Test untuk get user by id endpoint sukses
def test_get_user_by_id_success():
    email = "user_test_id@example.com"
    reg_resp = register_test_user(email, "User Test ID", "Password123!")
    assert reg_resp.status_code == 201
    get_resp = client.get(f"/api/v1/users/email/{email}")
    assert get_resp.status_code == 200
    user_id = get_resp.json()["data"]["id"]
    response = client.get(f"/api/v1/users/id/{user_id}")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "User retrieved successfully"
    assert json_data["data"]["id"] == user_id
    cleanup_test_user(email)

# Test untuk get user by gagal endpoint gagal
def test_get_user_by_id_not_found():
    response = client.get("/api/v1/users/id/nonexistent")
    assert response.status_code == 404

# Test untuk get user current user endpoint sukses
def test_get_current_user_info_success():
    email = "dummy_current@example.com"
    reg_resp = register_test_user(email, "Dummy Current", "Password123!")
    assert reg_resp.status_code == 201

    get_resp = client.get(f"/api/v1/users/email/{email}")
    assert get_resp.status_code == 200
    user_data = get_resp.json()["data"]

    def override_current_user():
        return user_data
    app.dependency_overrides[get_current_user] = override_current_user

    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "User retrieved successfully"
    assert json_data["data"]["id"] == user_data["id"]
    cleanup_test_user(email)
    app.dependency_overrides[get_current_user] = lambda: {"id": "dummy", "email": "dummy@example.com", "name": "Dummy User"}

# Test untuk update data user endpoint sukses
def test_update_user_success():
    email = "user_update@example.com"
    reg_resp = register_test_user(email, "User Update", "Password123!")
    assert reg_resp.status_code == 201
    get_resp = client.get(f"/api/v1/users/email/{email}")
    assert get_resp.status_code == 200
    user_id = get_resp.json()["data"]["id"]
    payload = {"name": "Updated Name"}
    response = client.put(f"/api/v1/users/{user_id}", json=payload)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["message"] == "User retrieved successfully"
    assert json_data["data"]["name"] == "Updated Name"
    cleanup_test_user(email)

# Test untuk update data user endpoint gagal
def test_update_user_not_found():
    payload = {"name": "Updated Name"}
    response = client.put("/api/v1/users/nonexistent", json=payload)
    assert response.status_code == 404

# Test untuk delete user endpoint sukses
def test_delete_user_success():
    email = "user_delete@example.com"
    reg_resp = register_test_user(email, "User Delete", "Password123!")
    assert reg_resp.status_code == 201
    get_resp = client.get(f"/api/v1/users/email/{email}")
    assert get_resp.status_code == 200
    user_id = get_resp.json()["data"]["id"]
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "User Deleted Successfully"

# Test untuk delete user endpoint gagal
def test_delete_user_not_found():
    response = client.delete("/api/v1/users/nonexistent")
    assert response.status_code == 404
