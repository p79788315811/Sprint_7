import requests

from helpers.base_api import ScooterApi
from helpers.constants import (
    ORDERS_ACCEPT_PATH,
    ORDERS_CANCEL_PATH,
    ORDERS_PATH,
    ORDERS_TRACK_PATH,
)


class OrderApi(ScooterApi):
    """Ручки для работы с заказами."""

    def create_order(self, payload: dict) -> requests.Response:
        return self._request("POST", ORDERS_PATH, json=payload)

    def get_orders(self, params: dict | None = None) -> requests.Response:
        return self._request("GET", ORDERS_PATH, params=params)

    def get_order_by_track(self, track: int | None = None) -> requests.Response:
        params = {"t": track} if track is not None else None
        return self._request("GET", ORDERS_TRACK_PATH, params=params)

    def accept_order(self, order_id: int | None = None, courier_id: int | None = None) -> requests.Response:
        params = {"courierId": courier_id} if courier_id is not None else None
        path = f"{ORDERS_ACCEPT_PATH}/{order_id}" if order_id is not None else ORDERS_ACCEPT_PATH
        return self._request("PUT", path, params=params)

    def cancel_order(self, track: int | None = None) -> requests.Response:
        params = {"track": track} if track is not None else None
        return self._request("PUT", ORDERS_CANCEL_PATH, params=params)
