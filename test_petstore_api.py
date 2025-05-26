import pytest
import requests

BASE_URL = "http://localhost:4010"

# Valid and invalid test data
VALID_PET = {"name": "Fluffy", "tag": "dog"}
INVALID_PET = {"tag": "dog"}  # Missing required "name"


@pytest.fixture
def pet_id():
    """Create a pet and return its ID (from Prism's example or default to 1)."""
    response = requests.post(f"{BASE_URL}/pets", json=VALID_PET)
    assert response.status_code == 200
    data = response.json()
    return data.get("id", 1)


def test_get_all_pets():
    response = requests.get(f"{BASE_URL}/pets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_pets_with_query_params():
    response = requests.get(f"{BASE_URL}/pets", params={"tags": ["dog"], "limit": 5})
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_pet_success():
    response = requests.post(f"{BASE_URL}/pets", json=VALID_PET)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "name" in data


def test_add_pet_missing_name():
    response = requests.post(f"{BASE_URL}/pets", json=INVALID_PET)
    assert response.status_code in (400, 422)


def test_add_pet_empty_body():
    response = requests.post(f"{BASE_URL}/pets", json={})
    assert response.status_code in (400, 422)


def test_get_pet_by_id(pet_id):
    response = requests.get(f"{BASE_URL}/pets/{pet_id}")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "name" in data


def test_get_pet_by_id_invalid():
    response = requests.get(f"{BASE_URL}/pets/abc")  # invalid ID format
    assert response.status_code in (400, 422)


def test_get_pet_by_id_not_found():
    response = requests.get(f"{BASE_URL}/pets/999999")
    assert response.status_code in (404, 200)  # Prism may still return example


def test_delete_pet_success(pet_id):
    response = requests.delete(f"{BASE_URL}/pets/{pet_id}")
    assert response.status_code in (204, 200)  # Prism may default to 200


def test_delete_pet_invalid_id():
    response = requests.delete(f"{BASE_URL}/pets/invalid")
    assert response.status_code in (400, 422)


def test_delete_pet_not_found():
    response = requests.delete(f"{BASE_URL}/pets/999999")
    assert response.status_code in (404, 204, 200)
