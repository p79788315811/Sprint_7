import allure
import pytest

from helpers.data_generator import generate_courier_payload


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Курьера можно создать")
    @allure.description("Успешный запрос возвращает код 201 и тело {'ok': true}")
    def test_create_courier_returns_201_and_ok(self, courier_api):
        payload = generate_courier_payload()

        response = courier_api.create_courier(payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        courier_id = courier_api.login_courier(
            {"login": payload["login"], "password": payload["password"]}
        ).json()["id"]
        courier_api.delete_courier(courier_id)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    @allure.description("Повторная регистрация с тем же логином возвращает ошибку 409")
    def test_create_duplicate_courier_returns_409(self, registered_courier, courier_api):
        response = courier_api.create_courier(
            {
                "login": registered_courier["login"],
                "password": registered_courier["password"],
                "firstName": registered_courier["firstName"],
            }
        )

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Нельзя создать курьера без обязательного поля: {missing_field}")
    @allure.description("Если одного из обязательных полей нет, запрос возвращает ошибку 400")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field_returns_400(self, courier_api, missing_field):
        payload = generate_courier_payload()
        payload.pop(missing_field)

        response = courier_api.create_courier(payload)

        assert response.status_code == 400
        assert response.json()["code"] == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Нельзя создать курьера с уже существующим логином")
    @allure.description("Логин занят, даже если остальные поля отличаются — ошибка 409")
    def test_create_courier_with_existing_login_returns_409(self, registered_courier, courier_api):
        payload = generate_courier_payload()
        payload["login"] = registered_courier["login"]

        response = courier_api.create_courier(payload)

        assert response.status_code == 409
        assert response.json()["code"] == 409
