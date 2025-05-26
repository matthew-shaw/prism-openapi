from typing import Dict

import pytest
import requests
from requests.models import Response

BASE_URL: str = "http://localhost:4010"

# Valid and invalid test data
VALID_PET: Dict[str, str] = {"name": "Fluffy", "tag": "dog"}
INVALID_PET: Dict[str, str] = {"tag": "dog"}  # Missing required "name"


@pytest.fixture
def pet_id() -> int:
    """
    Fixture to create a new pet using POST /pets and return its ID.

    Returns:
        int: ID of the created pet (default to 1 if missing in response).
    """
    response: Response = requests.post(f"{BASE_URL}/pets", json=VALID_PET)
    assert response.status_code == 200
    data: Dict[str, object] = response.json()
    return int(data.get("id", 1))


def test_get_all_pets() -> None:
    """
    Test retrieving all pets using GET /pets.

    Asserts:
        - Response status code is 200.
        - Response body is a list.
    """
    response: Response = requests.get(f"{BASE_URL}/pets")
    assert response.status_code == 200
    data: object = response.json()
    assert isinstance(data, list)


def test_get_pets_with_query_params() -> None:
    """
    Test GET /pets with query parameters `tags` and `limit`.

    Asserts:
        - Response status code is 200.
        - Response body is a list.
    """
    response: Response = requests.get(f"{BASE_URL}/pets", params={"tags": ["dog"], "limit": 5})
    assert response.status_code == 200
    data: object = response.json()
    assert isinstance(data, list)


def test_add_pet_success() -> None:
    """
    Test successfully adding a new pet using POST /pets.

    Asserts:
        - Response status code is 200.
        - Response contains "id" and "name".
    """
    response: Response = requests.post(f"{BASE_URL}/pets", json=VALID_PET)
    assert response.status_code == 200
    data: Dict[str, object] = response.json()
    assert "id" in data
    assert "name" in data


def test_add_pet_missing_name() -> None:
    """
    Test POST /pets with missing required field 'name'.

    Asserts:
        - Response status code is 400 or 422.
    """
    response: Response = requests.post(f"{BASE_URL}/pets", json=INVALID_PET)
    assert response.status_code in (400, 422)


def test_add_pet_empty_body() -> None:
    """
    Test POST /pets with an empty JSON body.

    Asserts:
        - Response status code is 400 or 422.
    """
    response: Response = requests.post(f"{BASE_URL}/pets", json={})
    assert response.status_code in (400, 422)


def test_get_pet_by_id(pet_id: int) -> None:
    """
    Test retrieving a pet by ID using GET /pets/{id}.

    Args:
        pet_id (int): ID of the pet to retrieve (provided by fixture).

    Asserts:
        - Response status code is 200.
        - Response contains "id" and "name".
    """
    response: Response = requests.get(f"{BASE_URL}/pets/{pet_id}")
    assert response.status_code == 200
    data: Dict[str, object] = response.json()
    assert "id" in data and "name" in data


def test_get_pet_by_id_invalid() -> None:
    """
    Test GET /pets/{id} with an invalid (non-integer) ID.

    Asserts:
        - Response status code is 400 or 422.
    """
    response: Response = requests.get(f"{BASE_URL}/pets/abc")
    assert response.status_code in (400, 422)


def test_get_pet_by_id_not_found() -> None:
    """
    Test GET /pets/{id} with a non-existent ID.

    Asserts:
        - Response status code is 404 or 200 depending on stub behavior.
    """
    response: Response = requests.get(f"{BASE_URL}/pets/999999")
    assert response.status_code in (404, 200)  # Prism may still return example


def test_delete_pet_success(pet_id: int) -> None:
    """
    Test successfully deleting a pet using DELETE /pets/{id}.

    Args:
        pet_id (int): ID of the pet to delete (provided by fixture).

    Asserts:
        - Response status code is 204 or 200 depending on stub behavior.
    """
    response: Response = requests.delete(f"{BASE_URL}/pets/{pet_id}")
    assert response.status_code in (204, 200)


def test_delete_pet_invalid_id() -> None:
    """
    Test DELETE /pets/{id} with an invalid (non-integer) ID.

    Asserts:
        - Response status code is 400 or 422.
    """
    response: Response = requests.delete(f"{BASE_URL}/pets/invalid")
    assert response.status_code in (400, 422)


def test_delete_pet_not_found() -> None:
    """
    Test DELETE /pets/{id} with a non-existent ID.

    Asserts:
        - Response status code is 404, 204, or 200 depending on stub behavior.
    """
    response: Response = requests.delete(f"{BASE_URL}/pets/999999")
    assert response.status_code in (404, 204, 200)
