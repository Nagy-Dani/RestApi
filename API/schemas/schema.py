from pydantic import BaseModel, EmailStr, field_validator
from typing import List

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

ShopName='Bolt'

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    @field_validator('id', mode='before')
    @classmethod
    def id_positive(cls, value):
        if value <= 0:
            raise ValueError("ID must be a positive integer.")
        return value

    @field_validator('name', mode='before')
    @classmethod
    def name_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        return value


class Item(BaseModel):
    item_id: int
    name: str
    brand: str
    price: float
    quantity: int

    @field_validator('price', 'item_id', 'quantity')
    @classmethod
    def positive_integer(cls, value):
        if value <= 0:
            raise ValueError("Value must be a positive integer.")
        return value

    @field_validator('name', 'brand')
    @classmethod
    def not_empty(cls, value):
        if not value.strip():
            raise ValueError("Field cannot be empty.")
        return value

class Basket(BaseModel):
    id: int
    user_id: int
    items: List[Item] = []

    @field_validator('id', 'user_id')
    @classmethod
    def id_positive(cls, value):
        if value <= 0:
            raise ValueError("ID must be a positive integer.")
        return value

    
