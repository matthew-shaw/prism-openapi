import uuid

import pytest
import requests

BASE_URL = "http://localhost:4010"


# Fixtures
@pytest.fixture
def valid_token():
    return "Bearer valid.jwt.token.here"  # Replace with real token if applicable


@pytest.fixture
def headers(valid_token):
    return {"Authorization": valid_token, "Content-Type": "application/json"}


# ---------------------------
# USERS ENDPOINT
# ---------------------------


def test_list_users_success(headers):
    params = {"sort": "created_at", "order": "desc"}
    response = requests.get(f"{BASE_URL}/users", headers=headers, params=params)
    assert response.status_code in (200, 204)


def test_list_users_with_email_filter(headers):
    params = {
        "sort": "email_address",
        "order": "asc",
        "email_address": "mash@example.com",
    }
    response = requests.get(f"{BASE_URL}/users", headers=headers, params=params)
    assert response.status_code in (200, 204)


def test_list_users_unauthorized():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 401


def test_list_users_invalid_sort(headers):
    params = {"sort": "not_valid", "order": "asc"}
    response = requests.get(f"{BASE_URL}/users", headers=headers, params=params)
    assert response.status_code in (400, 422)


def test_list_users_invalid_order(headers):
    params = {"sort": "email_address", "order": "descending"}
    response = requests.get(f"{BASE_URL}/users", headers=headers, params=params)
    assert response.status_code in (400, 422)


def test_create_user_success():
    payload = {
        "email_address": "newuser@example.com",
        "password": "CorrectHorseBatteryStaple",
    }
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201


def test_create_user_missing_fields():
    payload = {"email_address": "missingpass@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code in (400, 422)


def test_get_user_success(headers):
    user_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code in (200, 404)


def test_get_user_unauthorized():
    user_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 401


def test_update_user_success(headers):
    user_id = str(uuid.uuid4())
    payload = {"email_address": "updated@example.com", "password": "NewPass123"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=headers, json=payload)
    assert response.status_code in (200, 404)


def test_delete_user_success(headers):
    user_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code in (204, 404)


# ---------------------------
# THINGS ENDPOINT
# ---------------------------


def test_list_things_basic(headers):
    params = {"sort": "created_at", "order": "desc"}
    response = requests.get(f"{BASE_URL}/things", headers=headers, params=params)
    assert response.status_code in (200, 204)


def test_list_things_with_all_filters(headers):
    params = {
        "name": "Apple",
        "colour": "red",
        "quantity": 100,
        "sort": "quantity",
        "order": "asc",
    }
    response = requests.get(f"{BASE_URL}/things", headers=headers, params=params)
    assert response.status_code in (200, 204)


def test_list_things_unauthorized():
    response = requests.get(f"{BASE_URL}/things")
    assert response.status_code == 401


def test_list_things_invalid_sort(headers):
    response = requests.get(
        f"{BASE_URL}/things",
        headers=headers,
        params={"sort": "invalid", "order": "asc"},
    )
    assert response.status_code in (400, 422)


def test_list_things_invalid_order(headers):
    response = requests.get(f"{BASE_URL}/things", headers=headers, params={"sort": "name", "order": "wrong"})
    assert response.status_code in (400, 422)


def test_create_thing_success(headers):
    payload = {"name": "Banana", "colour": "yellow", "quantity": 50}
    response = requests.post(f"{BASE_URL}/things", json=payload, headers=headers)
    assert response.status_code == 201


def test_create_thing_missing_fields(headers):
    payload = {"name": "NoColour"}
    response = requests.post(f"{BASE_URL}/things", json=payload, headers=headers)
    assert response.status_code in (400, 422)


def test_get_thing_success(headers):
    thing_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/things/{thing_id}", headers=headers)
    assert response.status_code in (200, 404)


def test_get_thing_unauthorized():
    thing_id = str(uuid.uuid4())
    response = requests.get(f"{BASE_URL}/things/{thing_id}")
    assert response.status_code == 401


def test_update_thing_success(headers):
    thing_id = str(uuid.uuid4())
    payload = {"name": "UpdatedThing", "colour": "blue", "quantity": 77}
    response = requests.put(f"{BASE_URL}/things/{thing_id}", headers=headers, json=payload)
    assert response.status_code in (200, 404)


def test_delete_thing_success(headers):
    thing_id = str(uuid.uuid4())
    response = requests.delete(f"{BASE_URL}/things/{thing_id}", headers=headers)
    assert response.status_code in (204, 404)


# ---------------------------
# BOUNDARY TESTS FOR quantity
# ---------------------------


@pytest.mark.parametrize("quantity", [1, 1000])
def test_quantity_boundary_valid(headers, quantity):
    payload = {"name": "BoundaryThing", "colour": "green", "quantity": quantity}
    response = requests.post(f"{BASE_URL}/things", json=payload, headers=headers)
    assert response.status_code == 201


@pytest.mark.parametrize("quantity", [0, -1, 1001])
def test_quantity_boundary_invalid(headers, quantity):
    payload = {"name": "BoundaryThing", "colour": "blue", "quantity": quantity}
    response = requests.post(f"{BASE_URL}/things", json=payload, headers=headers)
    assert response.status_code in (400, 422)


# ---------------------------
# AUTH TOKEN ENDPOINT
# ---------------------------


def test_get_token_success():
    response = requests.get(f"{BASE_URL}/auth/token", auth=("user", "pass"))
    assert response.status_code == 200


def test_get_token_unauthorized():
    response = requests.get(f"{BASE_URL}/auth/token")
    assert response.status_code == 401
