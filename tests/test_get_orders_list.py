import allure
import pytest


@allure.epic("Яндекс Самокат API")
@allure.feature("Список заказов")
class TestGetOrdersList:

    @allure.title("В тело ответа возвращается список заказов")
    @allure.description("Ручка возвращает 200, список заказов и информацию о странице")
    def test_get_orders_returns_orders_list(self, order_api):
        response = order_api.get_orders()

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)
        assert len(body["orders"]) > 0

    @allure.title("Список заказов учитывает параметр limit")
    @allure.description("В pageInfo возвращается запрошенный размер страницы")
    @pytest.mark.parametrize("limit", [1, 10])
    def test_get_orders_respects_limit(self, order_api, limit):
        response = order_api.get_orders(params={"limit": limit, "page": 0})

        assert response.status_code == 200
        body = response.json()
        assert len(body["orders"]) <= limit
        assert body["pageInfo"]["limit"] == limit
