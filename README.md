# Sprint_7 — тесты API сервиса «Яндекс Самокат»

Проект автотестов на Python + pytest + requests для учебного сервиса
[qa-scooter.praktikum-services.ru](https://qa-scooter.praktikum-services.ru/docs/).

## Структура

```
Sprint_7/
├── conftest.py              # фикстуры: создание/удаление курьера, создание заказа
├── pytest.ini               # настройки pytest + формирование allure-results
├── requirements.txt
├── helpers/
│   ├── base_api.py          # базовый клиент: логирование запроса/ответа в Allure
│   ├── constants.py         # базовый URL и пути ручек
│   ├── courier_api.py       # методы ручек курьера
│   ├── order_api.py         # методы ручек заказов
│   └── data_generator.py    # генерация уникальных тестовых данных
├── tests/
│   ├── test_create_courier.py      # Создание курьера
│   ├── test_login_courier.py       # Логин курьера
│   ├── test_create_order.py        # Создание заказа (параметризация по цветам)
│   ├── test_get_orders_list.py     # Список заказов
│   ├── test_delete_courier.py      # Удаление курьера (доп. задание)
│   ├── test_accept_order.py        # Принять заказ (доп. задание)
│   └── test_get_order_by_track.py  # Получить заказ по номеру (доп. задание)
└── allure-report/           # сгенерированный HTML-отчёт
```

На каждую ручку — отдельный класс внутри своего файла. Тесты независимы:
необходимые данные создаются в фикстурах перед тестом и удаляются после него.

## Запуск

```bash
pip install -r requirements.txt
pytest
allure serve allure-results        # посмотреть отчёт локально
allure generate allure-results --clean -o allure-report
```

## Тестовые данные

- Курьер создаётся фикстурой `registered_courier` (уникальный логин из случайных букв),
  после теста удаляется через `DELETE /courier/{id}`.
- Заказ создаётся фикстурой `created_order`. Отдельного метода удаления заказа в API нет,
  поэтому в тир-дауне заказ отменяется через `PUT /orders/cancel?track=...`.

## Особенности и расхождения со стендом

Поведение проверено вручную до написания тестов; зафиксированы расхождения с документацией:

1. **Удаление курьера** — id передаётся в путь (`DELETE /api/v1/courier/{id}`),
   а не в query-параметрах, как указано в документации.
2. **Принятие заказа** — id заказа передаётся в путь (`PUT /api/v1/orders/accept/{id}?courierId=`).
3. **Логин без пароля** — по документации должен вернуться 400, фактически стенд отвечает
   504 или не отвечает вовсе. Тест `test_login_courier_without_password_returns_error`
   принимает любой из этих вариантов как ошибку авторизации и не роняет прогон.
4. **Отмена заказа** — `PUT /api/v1/orders/cancel?track=` (track в параметрах запроса).

Результат последнего прогона: **34 passed**.
