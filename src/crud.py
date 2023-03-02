from sqlalchemy.orm import Session
from src import models, schemas
from src.models import Recipient, Subscription, Edition


def create_recipient(db: Session, recipient: schemas.RecipientCreate):
    """
    Добавления нового Пользователя
    """
    db_data = models.Recipient(name=recipient.name, surname=recipient.surname, patronymic=recipient.patronymic,
                               recipient_code=recipient.recipient_code, outside=recipient.outside,
                               house_number=recipient.house_number, apartment_number=recipient.apartment_number)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_subscription(db: Session, subscription: schemas.SubscriptionCreate, recipient_id: int, edition_id: int):
    """
    Добавление новой Подписки
    """
    db_data = models.Subscription(#**subscription.dict(),
                                  subscription_period=subscription.subscription_period,
                                  month_of_delivery_start=subscription.month_of_delivery_start,
                                  year_of_delivery_start=subscription.year_of_delivery_start,
                                  recipient_id=recipient_id, edition_id=edition_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_edition(db: Session, edition: schemas.EditionCreate):
    """
    Добавление нового Издания
    """
    db_data = models.Edition(titles_of_the_publication=edition.titles_of_the_publication,
                             index_of_the_publication=edition.index_of_the_publication,
                             type_of_publication=edition.type_of_publication)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_recipient(db: Session, recipient_id: int):
    """
    Получить Пользователя по его id
    """
    return db.query(models.Recipient).filter(models.Recipient.id == recipient_id).first()


def get_recipient_by_code(db: Session, recipient_code: int):
    """
    Получить Пользователя по его коду
    """
    return db.query(models.Recipient).filter(models.Recipient.recipient_code == recipient_code).first()


def get_edition(db: Session, edition_id: int):
    """
    Получить Издание по его id
    """
    return db.query(models.Edition).filter(models.Edition.id == edition_id).first()


def get_edition_by_index(db: Session, index_of_the_publication: int):
    """
    Получить Издание по его index
    """
    return db.query(models.Edition).filter(models.Edition.index_of_the_publication == index_of_the_publication).first()


def get_subscription(db: Session, subscription_id: int):#
    """
    Получить Подписку по его id
    """
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()


def get_subscription_by_recipient(db: Session, recipient_id: int):
    """
    Получить Подписку по Подпищику
    """
    return db.query(models.Subscription).filter(models.Subscription.recipient_id == recipient_id).first()


# def get_subscription_by_edition(db: Session, edition_id: int):
#     """
#     Получить Подписку по Изданию
#     """
#     return db.query(models.Subscription).filter(models.Subscription.edition_id == edition_id).first()


def get_recipients(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список Подпищиков
    """
    return db.query(models.Recipient).offset(skip).limit(limit).all()


def get_editions(db: Session, skip: int = 0, limit: int = 100):
    """
    Получить список Изданий
    """
    return db.query(models.Edition).offset(skip).limit(limit).all()


def get_subscriptions(db: Session, skip: int = 0, limit: int = 100):#
    """
    Получить список Подписок
    """
    return db.query(models.Subscription).offset(skip).limit(limit).all()

