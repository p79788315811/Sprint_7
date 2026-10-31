import allure
import pytest

from helpers.courier_api import CourierApi
from helpers.data_generator import generate_courier_payload, generate_order_payload
from helpers.order_api import OrderApi


@pytest.fixture
def courier_api() -> CourierApi:
    return CourierApi()


@pytest.fixture
def order_api() -> OrderApi:
    return OrderApi()


@allure.step("Создать курьера через API")
def _create_courier(courier_api: CourierApi) -> dict:
    payload = generate_courier_payload()
    response = courier_api.create_courier(payload)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.status_code} {response.text}"

    login_response = courier_api.login_courier(
        {"login": payload["login"], "password": payload["password"]}
    )
    courier_id = login_response.json().get("id")

    return {**payload, "id": courier_id}


@pytest.fixture
def registered_courier(courier_api: CourierApi) -> dict:
    courier = _create_courier(courier_api)
    yield courier

    # Курьер может быть уже удалён внутри теста — повторное удаление вернёт 404, это допустимо
    courier_api.delete_courier(courier["id"])


@pytest.fixture
def created_order(order_api: OrderApi) -> dict:
    payload = generate_order_payload(color=["BLACK"])
    response = order_api.create_order(payload)
    assert response.status_code == 201, f"Не удалось создать заказ: {response.status_code} {response.text}"
    track = response.json()["track"]

    yield {**payload, "track": track}

    # Отдельного метода удаления заказа в API нет: освобождаем данные отменой заказа
    order_api.cancel_order(track)
