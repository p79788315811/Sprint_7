import allure
import pytest

from helpers.data_generator import generate_courier_payload


@allure.epic("Яндекс Самокат API")
@allure.feature("Удаление курьера")
class TestDeleteCourier:

    @allure.title("Курьера можно удалить")
    @allure.description("Успешный запрос возвращает код 200 и тело {'ok': true}")
    def test_delete_courier_returns_200_and_ok(self, registered_courier, courier_api):
        response = courier_api.delete_courier(registered_courier["id"])

        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title("Повторное удаление курьера возвращает ошибку")
    @allure.description("После успешного удаления курьера повторный запрос возвращает 404")
    def test_delete_already_deleted_courier_returns_404(self, registered_courier, courier_api):
        courier_api.delete_courier(registered_courier["id"])

        response = courier_api.delete_courier(registered_courier["id"])

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."

    @allure.title("Запрос без id возвращает ошибку")
    @allure.description("Если id курьера не передан, возвращается код 404")
    def test_delete_courier_without_id_returns_error(self, courier_api):
        response = courier_api._request("DELETE", "/courier/")

        assert response.status_code == 404
        assert response.json()["code"] == 404

    @allure.title("Запрос с несуществующим id возвращает ошибку")
    @allure.description("Для несуществующего id курьера возвращается 404")
    @pytest.mark.parametrize("nonexistent_id", [0, 999999999])
    def test_delete_courier_with_nonexistent_id_returns_404(self, courier_api, nonexistent_id):
        response = courier_api.delete_courier(nonexistent_id)

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id нет."
