from sqlalchemy import Column, String, Integer
from db import Base

class Drink(Base):
    __tablename__ = "coffee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    image = Column(String)
    price = Column(String)
    description = Column(String)
