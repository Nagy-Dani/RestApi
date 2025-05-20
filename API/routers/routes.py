from schemas.schema import User, Basket, Item
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi import APIRouter
from data.filereader import (
    get_all_users,
    get_user_by_id,
    get_basket_by_user_id,
    get_total_price_of_basket,
    load_json
)
from data.filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
    update_item_in_basket,
    delete_item_from_basket
)

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a 
  megfelelő Státus Code-ot, pl 404 - Not found, vagy 200 - OK

'''

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User) -> User:
    try:
        user_dict = user.dict()
        add_user(user_dict)
        return JSONResponse(content=user_dict, status_code=200)
    except Exception as e:
        print("Hiba a /users POST-ban:", e)
        raise HTTPException(status_code=404, detail=str(e))

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        new_basket = {
            "id": 100 + userid, 
            "user_id": userid,  
            "items": []  
        }
        add_basket(new_basket)
        return JSONResponse(content="New basket added to user", status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        updated_basket_dict = add_item_to_basket(userid, item)
        updated_basket = Basket(**updated_basket_dict)
        return JSONResponse(content=updated_basket.model_dump(), status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.put('/updateitem')
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        updated_basket = update_item_in_basket(userid, itemid, updateItem)
        return JSONResponse(content=updated_basket, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.delete('/deleteitem')
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        updated_basket = delete_item_from_basket(userid, itemid)
        return JSONResponse(content=updated_basket, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/user')
def user(userid: int) -> User:
    try:
        found_user = get_user_by_id(userid)
        return JSONResponse(content=found_user, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/users')
def users() -> list[User]:
    return JSONResponse(content=get_all_users(), status_code=200)

@routers.get('/shoppingbag')
def shoppingbag(userid: int) -> list[Item]:
    try:
        basket_items = get_basket_by_user_id(userid)
        return JSONResponse(content=basket_items, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    try:
        total_price = get_total_price_of_basket(userid)
        return JSONResponse(content={"total_price": total_price}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))




