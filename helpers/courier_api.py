import requests

from helpers.base_api import ScooterApi
from helpers.constants import COURIER_LOGIN_PATH, COURIER_PATH


class CourierApi(ScooterApi):
    """Ручки для работы с курьерами."""

    def create_courier(self, payload: dict) -> requests.Response:
        return self._request("POST", COURIER_PATH, data=payload)

    def login_courier(self, payload: dict) -> requests.Response:
        return self._request("POST", COURIER_LOGIN_PATH, data=payload)

    def delete_courier(self, courier_id: int) -> requests.Response:
        return self._request("DELETE", f"{COURIER_PATH}/{courier_id}")
