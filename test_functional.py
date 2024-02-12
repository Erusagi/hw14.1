
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_create_contact(client):
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "123456789",
        "birthday": "1990-01-01",
        "additional_info": "Additional information"
    }

    response = client.post("/contacts/", json=contact_data)

    assert response.status_code == 200
    created_contact = response.json()
    assert created_contact["first_name"] == contact_data["first_name"]

def test_update_user_avatar(client):
    avatar_file = ("avatar.jpg", b"binary_data_of_image")

    response = client.put("/users/update-avatar/", files={"avatar": avatar_file})

    assert response.status_code == 200
    assert response.json() == {"message": "Avatar updated successfully"}
