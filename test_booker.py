from client import RestfulBookerClient

client = RestfulBookerClient()
client.authorize("admin", "password123")


def test_get_booking_ids():
    response = client.perform_get_request("/booking")
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

    response = client.perform_post_request("/booking", new_booking)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["booking"]["firstname"] == "John"
    assert response_body["booking"]["lastname"] == "Doe"


def test_get_booking_by_id():
    booking_id = 11
    response = client.perform_get_request(f"/booking/{booking_id}")
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

    response = client.perform_post_request("/booking", new_booking)

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

    response = client.perform_post_request("/booking", new_booking)
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

    response = client.perform_put_request(f"/booking/{booking_id}", updated_booking)
    response_body = response.json()

    assert response.status_code == 200
    assert response_body["firstname"] == "Jane"
    assert response_body["lastname"] == "Doe"
    assert response_body["totalprice"] == 456
