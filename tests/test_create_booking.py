import allure
import pytest
from pydantic import ValidationError
from core.models.booking import BookingResponse


@allure.feature('Test Create')
def test_create_booking(api_client, generate_random_booking_date):
    data_generate = generate_random_booking_date
    response_json = api_client.create_booking(generate_random_booking_date)
    assert isinstance(response_json, dict)
    assert response_json["booking"]["firstname"] == data_generate.get("firstname")
    assert response_json["booking"]["lastname"] == data_generate.get("lastname")
    assert response_json["booking"]["totalprice"] == data_generate.get("totalprice")
    assert response_json["booking"]["depositpaid"] == data_generate.get("depositpaid")
    assert response_json["booking"]["bookingdates"] == data_generate.get("bookingdates")
    assert response_json["booking"]["additionalneeds"] == data_generate.get("additionalneeds")


@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data')
def test_create_booking_with_custom_data(api_client):
    booking_data = {
        "firstname": "Ivan",
        "lastname": "Ivannovich",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-02-01",
            "checkout": "2025-02-10"
        },
        "additionalneeds": "Dinner"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")
    assert response["booking"]["firstname"] == booking_data.get("firstname")
    assert response["booking"]["lastname"] == booking_data.get("lastname")
    assert response["booking"]["totalprice"] == booking_data.get("totalprice")
    assert response["booking"]["depositpaid"] == booking_data.get("depositpaid")
    assert response["booking"]["bookingdates"]["checkin"] == booking_data.get("bookingdates").get("checkin")
    assert response["booking"]["bookingdates"]["checkout"] == booking_data.get("bookingdates").get("checkout")
    assert response["booking"]["additionalneeds"] == booking_data.get("additionalneeds")

#В booking_data генерируются даты checkin и checkout и проверка результата
@allure.feature('Test creating booking')
@allure.story('Positive: creating booking with custom data and bookingdates')
def test_create_booking_with_custom_data_and_bookingdates(api_client,booking_dates):
    booking_data = {
        "firstname": "Petr",
        "lastname": "Ivannovich",
        "totalprice": 149,
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates.get("checkin"),
            "checkout": booking_dates.get("checkout")
        },
        "additionalneeds": "Dinner"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed: {e}")

    assert response["booking"]["firstname"] == booking_data.get("firstname")
    assert response["booking"]["lastname"] == booking_data.get("lastname")
    assert response["booking"]["totalprice"] == booking_data.get("totalprice")
    assert response["booking"]["depositpaid"] == booking_data.get("depositpaid")
    assert response["booking"]["bookingdates"]["checkin"] == booking_data.get("bookingdates").get("checkin")
    assert response["booking"]["bookingdates"]["checkout"] == booking_data.get("bookingdates").get("checkout")
    assert response["booking"]["additionalneeds"] == booking_data.get("additionalneeds")


#Негативный сценарий, создать бранирования и не указывать пользовательские данные, а только даты
@allure.feature('Test creating booking')
@allure.story('Negative: creating a booking without user data')
def test_create_without_user_data(api_client,booking_dates,mocker):
    booking_data = {
        "bookingdates": {
            "checkin": booking_dates.get("checkin"),
            "checkout": booking_dates.get("checkout")
        }
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200 but got 500"):
        api_client.create_booking(booking_data)


#Негативный сценарий, создание бронирования с данными в неверном формате
@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with incorrect format data')
def test_create_with_incorrect_format(api_client,booking_dates,mocker):
    booking_data = {
        "firstname": 134,
        "lastname": "Ivannovich",
        "totalprice": "149",
        "depositpaid": True,
        "bookingdates": {
            "checkin": booking_dates.get("checkin"),
            "checkout": booking_dates.get("checkout")
        },
        "additionalneeds": "Dinner"
    }

    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200 but got 500"):
        api_client.create_booking(booking_data)

#Негативный сценарий, создание бронирования без данных
@allure.feature('Test creating booking')
@allure.story('Negative: creating booking with not data')
def test_create_with_not_data(api_client,mocker):
    booking_data = {}

    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, 'post', return_value=mock_response)
    with pytest.raises(AssertionError, match="Expected status code 200 but got 500"):
        api_client.create_booking(booking_data)