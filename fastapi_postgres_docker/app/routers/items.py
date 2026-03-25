from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, crud

router = APIRouter()


@router.post("/items", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db)
):
    return crud.create_item(db, item)


@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db)


@router.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_item(db, item_id)


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    return crud.delete_item(db, item_id)