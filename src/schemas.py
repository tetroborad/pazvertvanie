from pydantic import BaseModel
from typing import Union, List

from src.models import Subscription


class RecipientBase(BaseModel):
    """
    Базовый класс для Recipient
    """
    name: str
    surname: str
    patronymic: Union[None, str]
    recipient_code: int
    outside: str
    house_number: str
    apartment_number: str


class RecipientCreate(RecipientBase):
    """
    Класс для создания Recipient, наследуется от базового RecipientBase, но не содержит
    дополнительных полей, пока что
    """
    pass


class Recipient(RecipientBase):
    """
    Класс для отображения Recipient, наследуется от базового RecipientBase
    поля значения для полей id и subscription_r будем получать из БД
    """
    id: int
    # Выключаешь и всё работает
    #subscription_r: List[Subscription]

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True
        #arbitrary_types_allowed = True


class SubscriptionBase(BaseModel):
    """
    Базовый класс для Subscription
    """
    subscription_period: int
    month_of_delivery_start: int
    year_of_delivery_start: int


class SubscriptionCreate(SubscriptionBase):
    """
    Класс для создания Subscription, наследуется от базового SubscriptionBase, но не содержит
    дополнительных полей, пока что
    """
    pass


class Subscription(SubscriptionBase):
    """
    Класс для отображения Subscription, наследуется от базового SubscriptionBase
    поля значения для полей id, recipient_id и edition_id будем получать из БД
    """
    id: int
    recipient_id: int
    edition_id: int

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True
        #arbitrary_types_allowed = True


class EditionBase(BaseModel):
    """
    Базовый класс для Edition
    """
    index_of_the_publication: int
    titles_of_the_publication: str
    type_of_publication: Union[None, str]


class EditionCreate(EditionBase):
    """
    Класс для создания Edition, наследуется от базового EditionBase, но не содержит
    дополнительных полей, пока что
    """
    pass


class Edition(EditionBase):
    """
    Класс для отображения Edition, наследуется от базового EditionBase
    поля значения для полей id и subscription_e будем получать из БД
    """
    id: int
    subscription_e: List[Subscription]

    class Config:
        """
        Задание настройки для возможности работать с объектами ORM
        """
        orm_mode = True
        #arbitrary_types_allowed = True
