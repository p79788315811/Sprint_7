import allure
import pytest

from helpers.data_generator import generate_order_payload


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Заказ создаётся с цветом: {color_name}")
    @allure.description("Цвет можно указать один, оба сразу или не указать совсем — заказ создаётся")
    @pytest.mark.parametrize(
        "color, color_name",
        [
            pytest.param(["BLACK"], "BLACK", id="black"),
            pytest.param(["GREY"], "GREY", id="grey"),
            pytest.param(["BLACK", "GREY"], "BLACK и GREY", id="black-grey"),
            pytest.param([], "пустой список", id="empty-list"),
            pytest.param(None, "не передан", id="not-passed"),
        ],
    )
    def test_create_order_with_different_colors_returns_201(self, order_api, color, color_name):
        payload = generate_order_payload(color=color)

        response = order_api.create_order(payload)

        assert response.status_code == 201
        assert "track" in response.json(), f"В теле ответа нет track: {response.text}"

        order_api.cancel_order(response.json()["track"])

    @allure.title("Тело ответа при создании заказа содержит track")
    @allure.description("track — номер заказа, целое число, по нему заказ можно получить")
    def test_create_order_response_contains_track(self, order_api):
        response = order_api.create_order(generate_order_payload(color=["BLACK"]))

        assert response.status_code == 201
        track = response.json()["track"]
        assert isinstance(track, int)

        order_api.cancel_order(track)
