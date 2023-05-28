import requests

base_url = "https://restful-booker.herokuapp.com"


def test_get_booking_ids():
    response = requests.get(base_url + "/booking")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body[0]["bookingid"] is not None
    assert isinstance(response_body, list)


def test_create_booking():
    new_booking = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(base_url + "/booking", json=new_booking)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["booking"]["firstname"] == "John"
    assert response_body["booking"]["lastname"] == "Doe"


def test_get_booking_by_id():
    booking_id = 11
    response = requests.get(base_url + f"/booking/{booking_id}")
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["firstname"] is not None
    assert response_body["lastname"] is not None

def test_create_booking_with_bad_request():
    new_booking = {
        "firstname": 12345,
        "lastname": "Doe",
        "totalprice": "123",
        "depositpaid": "Yes",
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(base_url + "/booking", json=new_booking)

    assert response.status_code == 500


def test_update_booking():
    new_booking = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2023-01-01",
            "checkout": "2023-01-02"
        },
        "additionalneeds": "Breakfast"
    }

    response = requests.post(base_url + "/booking", json=new_booking)
    booking_id = response.json()["bookingid"]

    updated_booking = {
        "firstname": "Jane",
        "lastname": "Doe",
        "totalprice": 456,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2023-01-03",
            "checkout": "2023-01-04"
        },
        "additionalneeds": "Lunch"
    }

    # get the token
    username = "admin"
    password = "password123"
    token = get_token(username, password)

    headers = {
        "Cookie": f"token={token}"
    }

    response = requests.put(base_url + f"/booking/{booking_id}", headers=headers, json=updated_booking)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["firstname"] == "Jane"
    assert response_body["lastname"] == "Doe"
    assert response_body["totalprice"] == 456


def get_token(username, password):
    auth_data = {
        "username": username,
        "password": password
    }
    response = requests.post(base_url + "/auth", json=auth_data)
    assert response.status_code == 200
    return response.json()["token"]