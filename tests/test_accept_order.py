import allure
import pytest


@allure.epic("Яндекс Самокат API")
@allure.feature("Принять заказ")
class TestAcceptOrder:

    @allure.title("Курьер может принять заказ")
    @allure.description("Успешный запрос возвращает код 200 и тело {'ok': true}")
    def test_accept_order_returns_200_and_ok(self, order_api, registered_courier, created_order):
        order_id = order_api.get_order_by_track(created_order["track"]).json()["order"]["id"]

        response = order_api.accept_order(order_id=order_id, courier_id=registered_courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Запрос без id курьера возвращает ошибку")
    @allure.description("Если не передать id курьера, возвращается код 400")
    def test_accept_order_without_courier_id_returns_400(self, order_api, registered_courier, created_order):
        order_id = order_api.get_order_by_track(created_order["track"]).json()["order"]["id"]

        response = order_api.accept_order(order_id=order_id)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Запрос с неверным id курьера возвращает ошибку")
    @allure.description("Для несуществующего курьера возвращается код 404")
    def test_accept_order_with_invalid_courier_id_returns_404(self, order_api, created_order):
        order_id = order_api.get_order_by_track(created_order["track"]).json()["order"]["id"]

        response = order_api.accept_order(order_id=order_id, courier_id=0)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Запрос без id заказа возвращает ошибку")
    @allure.description("Если не передать id заказа, возвращается код 404")
    def test_accept_order_without_order_id_returns_error(self, order_api, registered_courier):
        response = order_api.accept_order(courier_id=registered_courier["id"])

        assert response.status_code == 404
        assert response.json()["code"] == 404

    @allure.title("Запрос с неверным id заказа возвращает ошибку")
    @allure.description("Для несуществующего заказа возвращается код 404")
    def test_accept_order_with_invalid_order_id_returns_404(self, order_api, registered_courier):
        response = order_api.accept_order(order_id=0, courier_id=registered_courier["id"])

        assert response.status_code == 404
        assert response.json()["message"] == "Заказа с таким id не существует"
