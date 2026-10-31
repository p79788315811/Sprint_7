import allure
import pytest


@allure.epic("Яндекс Самокат API")
@allure.feature("Получить заказ по его номеру")
class TestGetOrderByTrack:

    @allure.title("Успешный запрос возвращает объект с заказом")
    @allure.description("По трек-номеру возвращается код 200 и объект заказа внутри поля order")
    def test_get_order_by_track_returns_order(self, order_api, created_order):
        response = order_api.get_order_by_track(created_order["track"])

        assert response.status_code == 200
        order = response.json()["order"]
        assert order["track"] == created_order["track"]
        assert order["firstName"] == created_order["firstName"]
        assert order["address"] == created_order["address"]

    @allure.title("Запрос без номера заказа возвращает ошибку")
    @allure.description("Если номер заказа не передан, возвращается код 400")
    def test_get_order_without_track_returns_400(self, order_api):
        response = order_api.get_order_by_track()

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Запрос с несуществующим номером заказа возвращает ошибку")
    @allure.description("Для несуществующего трек-номера возвращается код 404")
    @pytest.mark.parametrize("nonexistent_track", [0, 999999999])
    def test_get_order_with_nonexistent_track_returns_404(self, order_api, nonexistent_track):
        response = order_api.get_order_by_track(nonexistent_track)

        assert response.status_code == 404
        assert response.json()["message"] == "Заказ не найден"
