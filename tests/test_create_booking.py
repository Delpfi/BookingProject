import allure
import pytest
import requests

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