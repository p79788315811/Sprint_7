import random
import string


def generate_random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_courier_payload() -> dict:
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


def generate_order_payload(color: list | None = None) -> dict:
    payload = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2026-10-30",
        "comment": "Saske, come back to Konoha",
    }
    if color is not None:
        payload["color"] = color
    return payload
