import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic.class_validators import List
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():   # pragma: no cover
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/recipient/", response_model=schemas.Recipient)
def create_recipient(recipient: schemas.RecipientCreate, db: Session = Depends(get_db)):
    """
    Создание Подпищика, если такой recipient codee уже есть в БД, то выдается ошибка
    """
    db_recipient = crud.get_recipient_by_code(db, recipient_code=recipient.recipient_code)
    if db_recipient:
        raise HTTPException(status_code=400, detail="Recipient already registered")
    return crud.create_recipient(db=db, recipient=recipient)


@app.post("/edition/", response_model=schemas.Edition)
def create_edition(edition: schemas.EditionCreate, db: Session = Depends(get_db)):
    """
    Создание Издания, если такой edition codee уже есть в БД, то выдается ошибка
    """
    db_edition = crud.get_edition_by_index(db, index_of_the_publication=edition.index_of_the_publication)
    if db_edition:
        raise HTTPException(status_code=400, detail="Edition already registered")
    return crud.create_edition(db=db, edition=edition)


@app.post("/subscription/", response_model=schemas.Subscription)
def create_subscription(subscription: schemas.SubscriptionCreate, recipient_id: int, edition_id: int, db: Session = Depends(get_db)):
    """
    Создание Подписки
    """
    db_recipient = crud.get_recipient(db, recipient_id=recipient_id)
    if not db_recipient:
        raise HTTPException(status_code=400, detail="Recipient not found")
    db_edition = crud.get_edition(db, edition_id=edition_id)
    if not db_edition:
        raise HTTPException(status_code=400, detail="Edition not found")
    return crud.create_subscription(db=db, subscription=subscription, recipient_id=recipient_id, edition_id=edition_id)


@app.get("/recipient/{recipient_id}", response_model=schemas.Recipient)
def read_recipient(recipient_id: int, db: Session = Depends(get_db)):
    """
    Получение Подпищика по id, если такой id уже есть в БД, то выдается ошибка
    """
    db_recipient = crud.get_recipient(db, recipient_id=recipient_id)
    if db_recipient is None:
        raise HTTPException(status_code=400, detail="Recipient not found")
    return db_recipient


@app.get("/edition/{edition_id}", response_model=schemas.Edition)
def read_edition(edition_id: int, db: Session = Depends(get_db)):
    """
    Получение Издания по id, если такой id уже есть в БД, то выдается ошибка
    """
    db_edition = crud.get_edition(db, edition_id=edition_id)
    if db_edition is None:
        raise HTTPException(status_code=400, detail="Recipient not found")
    return db_edition


@app.get("/recipient_subscription/{recipient_id}", response_model=schemas.Subscription)
def read_recipient_subscription(recipient_id: int, db: Session = Depends(get_db)):
    """
    Получение Подписки Подпищика по id
    """
    db_subscription = crud.get_subscription_by_recipient(db=db, recipient_id=recipient_id)
    if db_subscription is None:
        raise HTTPException(status_code=400, detail="Recipient subscription not found")
    return db_subscription


# @app.get("/edition_subscription/{recipient_id}", response_model=schemas.Subscription)
# def read_edition_subscription(edition_id: int, db: Session = Depends(get_db)):
#     """
#     Получение Подписки Издания по id
#     """
#     db_subscription = crud.get_subscription_by_edition(db=db, edition_id=edition_id)
#     if db_subscription is None:
#         raise HTTPException(status_code=400, detail="Edition subscription not found")
#     return db_subscription


@app.get("/subscription/{subscription_id}", response_model=schemas.Subscription)
def read_recipient_subscription(subscription_id: int, db: Session = Depends(get_db)):
    """
    Получение Подписки на Издания по id
    """
    db_subscription = crud.get_subscription(db, subscription_id=subscription_id)
    if db_subscription is None:
        raise HTTPException(status_code=400, detail="Subscription not found")
    return db_subscription


@app.get("/recipients/", response_model=list[schemas.Recipient])
def read_recipients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка пользователей
    """
    recipients = crud.get_recipients(db, skip=skip, limit=limit)
    return recipients


@app.get("/editions/", response_model=list[schemas.Edition])
def read_editions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка Издания
    """
    editions = crud.get_editions(db, skip=skip, limit=limit)
    return editions


@app.get("/subscriptions/", response_model=list[schemas.Subscription])
def read_editions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Получение списка Подписок
    """
    subscriptions = crud.get_subscriptions(db, skip=skip, limit=limit)
    return subscriptions


#if __name__ == "__main__":
#    uvicorn.run("main:app", port=6000, log_level="info", reload=True)