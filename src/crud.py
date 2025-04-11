from sqlalchemy.orm import Session
from .model import UserSwiftDB

def get_unique_swift_code(db: Session, swift_code: str) -> UserSwiftDB:
    return db.query(UserSwiftDB).filter(UserSwiftDB.swift_code == swift_code).first()

def create_swift_code(db: Session, data: dict) -> UserSwiftDB:
    """
    Here we create a new swift code. We use a dictionary to pass in the data
    """
    new_swift = UserSwiftDB(**data)
    db.add(new_swift)
    db.commit()
    db.refresh(new_swift)
    return new_swift