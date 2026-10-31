import json

import allure
import requests

from helpers.constants import BASE_URL, REQUEST_TIMEOUT


class ScooterApi:
    """Базовый класс для работы с API сервиса «Яндекс Самокат»."""

    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        with allure.step(f"{method} {url}"):
            if kwargs:
                allure.attach(
                    json.dumps(
                        {key: value for key, value in kwargs.items()},
                        ensure_ascii=False,
                        default=str,
                    ),
                    name="request",
                    attachment_type=allure.attachment_type.JSON,
                )
            response = requests.request(method, url, timeout=REQUEST_TIMEOUT, **kwargs)
            allure.attach(
                f"status_code: {response.status_code}\n{response.text[:2000]}",
                name="response",
                attachment_type=allure.attachment_type.TEXT,
            )
        return response
