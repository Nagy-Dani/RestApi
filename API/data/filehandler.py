import json
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = "data/data.json"

def load_json() -> Dict[str, Any]:
    """
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    """
    try:
        with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "Users": [],
            "Baskets": []
        }
        

def save_json(data: Dict[str, Any]) -> None:
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    
    if any(akk["id"] == user["id"] for akk in data["Users"]):
        raise ValueError(f"A felhasználó azonosítója ({user['id']}) foglalt.")
    
    data["Users"].append({
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    })
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    if (any(bas["id"] == basket["id"] for bas in data["Baskets"])):
        raise ValueError(f"A kosár azonosítója ({basket['id']}) foglalt.")
    
    if not any(akk["id"] == basket["user_id"] for akk in data["Users"]):
        raise ValueError(f"A felhasználó azonosítója ({basket['user_id']}) nem létezik.")
    
    
    data["Baskets"].append(basket)
    save_json(data)
    return basket



def add_item_to_basket(f: int, item: Dict[str, Any]) -> None:
    data = load_json()
    
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            basket["items"].append({
                "item_id": item["item_id"],
                "name": item["name"],
                "brand": item["brand"],
                "price": item["price"],
                "quantity": item["quantity"]
            })
            save_json(data)
            return basket
    
    raise ValueError(f"A felhasználónak ({user_id}) nincs kosara.")

def update_item_in_basket(user_id: int, item_id: int, new_data: Dict[str, Any]) -> None:
    data = load_json()
    
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            for item in basket["items"]:
                if item["item_id"] == item_id:
                    item.update(new_data)
                    save_json(data)
                    return basket
    
    raise ValueError(f"A felhasználó ({user_id}) kosarában nincs ilyen termék ({item_id}).")


def delete_item_from_basket(user_id: int, item_id: int) -> None:
    data = load_json()
    
    for basket in data["Baskets"]:
        if basket["user_id"] == user_id:
            original_length = len(basket["items"])
            basket["items"] = [item for item in basket["items"] if item["item_id"] != item_id]
            
            if len(basket["items"]) < original_length:
                save_json(data)
                return basket
    
    raise ValueError(f"A felhasználó ({user_id}) kosarában nincs ilyen termék ({item_id}).")

