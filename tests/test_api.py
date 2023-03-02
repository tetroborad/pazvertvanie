from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Тестовая БД

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)  # Удаляем таблицы из БД
Base.metadata.create_all(bind=engine)  # Создаем таблицы в БД


def override_get_db():
    """
    Данная функция при тестах будет подменять функцию get_db() в main.py.
    Таким образом приложение будет подключаться к тестовой базе данных.
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db  # Делаем подмену

client = TestClient(app)  # создаем тестовый клиент к нашему приложению


def test_create_recipient():
    """
    Тест на создание нового Подпищика
    """
    response = client.post(
        "/recipient/",
        json={"name": "Alex", "surname": "Corleone", "patronymic": "Vito",
                "recipient_code": "865", "outside": "Karl-Marks", "house_number": "5",
                "apartment_number": "40 б"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["recipient_code"] == 865


def test_create_exist_recipient():
    """
    Проверка случая, когда мы пытаемся добавить существующего Подпищика
    в БД, т.е. когда данные уже присутствует в БД.
    """
    response = client.post(
        "/recipient/",
        json={"name": "Alex", "surname": "Corleone", "patronymic": "Vito",
                "recipient_code": 865, "outside": "Karl-Marks", "house_number": "5",
                "apartment_number": "40 б"}
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient already registered"


def test_read_recipients():
    """
    Тест на получение списка пользователей из БД
    """
    response = client.get("/recipients/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["recipient_code"] == 865


def test_read_recipient():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/recipient/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["recipient_code"] == 865


def test_recipient_not_found():
    """
    Проверка случая, если пользователь с таким id отсутствует в БД
    """
    response = client.get("/recipient/7")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient not found"


def test_create_edition():
    response = client.post(
        "/edition/",
        json={
            "titles_of_the_publication": "Pravda",
            "index_of_the_publication": 49848597,
            "type_of_publication": "Newspaper"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    #assert data["detail"] == "Recipient not found"
    assert data["titles_of_the_publication"] == "Pravda"
    assert data["index_of_the_publication"] == 49848597
    assert data["type_of_publication"] == "Newspaper"


def test_bad_create_edition():
    response = client.post(
        "/edition/",
        json={
            "titles_of_the_publication": "Pravda",
            "index_of_the_publication": 49848597,
            "type_of_publication": "Newspaper"
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Edition already registered"
    #assert data["titles_of_the_publication"] == "Pravda"
    #assert data["index_of_the_publication"] == 49848597
    #assert data["type_of_publication"] == "Newspaper"


def test_read_editions():
    """
    Тест на получение пользователя из БД по его id
    """
    response = client.get("/editions/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["index_of_the_publication"] == 49848597


def test_create_subscription():
    response = client.post(
        "/subscription/?recipient_id=1&edition_id=1",
        json={
            "subscription_period": 5,
            "month_of_delivery_start": 2,
            "year_of_delivery_start": 1
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["subscription_period"] == 5
    assert data["month_of_delivery_start"] == 2
    assert data["year_of_delivery_start"] == 1


def test_create_bad_recipient_subscription():
    response = client.post(
        "/subscription/?recipient_id=853&edition_id=1",
        json={
            "subscription_period": 4963,
            "month_of_delivery_start": 2,
            "year_of_delivery_start": 1
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient not found"


def test_create_bad_edition_subscription():
    response = client.post(
        "/subscription/?recipient_id=1&edition_id=95658",
        json={
            "subscription_period": 4963,
            "month_of_delivery_start": 2,
            "year_of_delivery_start": 1
        }
    )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Edition not found"


def test_get_recipient():
    response = client.get("/recipient/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Alex"
    assert data["surname"] == "Corleone"
    assert data["patronymic"] == "Vito"
    assert data["recipient_code"] == 865
    assert data["outside"] == "Karl-Marks"
    assert data["house_number"] == "5"
    assert data["apartment_number"] == "40 б"


def test_get_not_exist_recipient():
    response = client.get("/recipient/785")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient not found"


def test_get_edition():
    response = client.get("/edition/1")
    assert response.status_code == 200, response.text
    data = response.json()
    #assert data["detail"] == "Recipient not found"
    assert data["index_of_the_publication"] == 49848597


def test_get_not_exist_edition():
    response = client.get("/edition/2")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient not found"


def test_get_subscription_by_recipient():
    response = client.get("/recipient_subscription/1")
    assert response.status_code == 200, response.text
    data = response.json()
    #assert data[0]["edition_id"] == 5
    assert data["year_of_delivery_start"] == 1


def test_bad_get_subscription_by_recipient():
    response = client.get("/recipient_subscription/4")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Recipient subscription not found"
    #assert data[0]["edition_id"] == 5
    #assert data["year_of_delivery_start"] == 1


# def test_get_subscription_by_edition():
#     response = client.get("/edition_subscription/4")
#     assert response.status_code == 422, response.text
#     data = response.json()
#     #assert data["detail"] != "Edition subscription not found"
#     #assert data["subscription_period"] == 49848597
#     #assert data["month_of_delivery_start"] == 9
#     #assert data["year_of_delivery_start"] == 2022


# def test_get_subscription_by_edition():
#     response = client.get("/edition_subscription/1")
#     assert response.status_code == 422, response.text
#     data = response.json()
#     assert data[{'loc': ['query', 'edition_id'], 'msg': 'field required', 'type': 'value_error.missing'}] == 'Edition subscription not found'
#     #assert data["edition.id"] == 1
#     #assert data["month_of_delivery_start"] == 9
#     #assert data["year_of_delivery_start"] == 2022


def test_get_subscription():
    response = client.get("/subscription/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["year_of_delivery_start"] == 1


def test_get_not_exist_subscription():
    response = client.get("/subscription/4963")
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Subscription not found"


def test_get_subscriptions():
    """
    Тест на получение списка Подпищиков
    """
    response = client.get("/subscriptions/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["subscription_period"] == 5
    #"subscription_period": 4963,
    assert data[0]["month_of_delivery_start"] == 2
