from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserSwiftDB(Base):
    __tablename__ = 'swift_db'
    id = Column(Integer, primary_key=True, index=True)

    swift_code = Column(String, unique=True, index=True, nullable=False)
    bank_name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    country_iso2 = Column(String, nullable=False)
    country_name = Column(String, nullable=False)
    is_headquarter = Column(Boolean, default=False)

    # TODO: add more fields, maybe auto check if XXX is unique