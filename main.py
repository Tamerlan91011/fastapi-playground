from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI()

database = [
    {'id': 1, 'city': 'Sochi',      'name': 'Vacation Plaza', },
    {'id': 2, 'city': 'Moscow',     'name': 'Moscow City', },
    {'id': 3, 'city': 'Ufa',        'name': 'UncleChudra', },
    {'id': 4, 'city': 'Volgograd',  'name': 'VolgogradCity', },
    {'id': 5, 'city': 'Volgograd',  'name': 'Start', },
]

@app.get("/hotels")
def get_hotel(
        id: int | None = Query(default=None, description="ID города"),
        city: str | None = Query(default=None, description="Название города")
):
    hotel = [hotel for hotel in database if id == hotel['id'] or city == hotel['city']]
    return hotel

@app.delete("/hotels/{hotels_id}")
def delete_hotel(hotels_id: int):
    global database
    database = [hotel for hotel in database if hotels_id != hotel['id']]
    return {'Status': 'OK'}

@app.put("/hotels/{hotels_id}")
def fully_update_hotel(
        hotel_id: int,
        city: str = Query(description='Название города'),
        name: str = Query(description='Название отеля')
):
    global database
    
    if hotel_id in [hotel["id"] for hotel in database]:
        database[-1].update({"id": hotel_id, "city": city, "name": name})
        return {"Status": "OK"}
        
    return {"Status": "NOT NOK"}

@app.patch("/hotels/{hotels_id}")
def partly_update_hotel(
        hotel_id: int,
        city: str | None = Query(description='Название города'),
        name: str | None = Query(description='Название отеля')
):
    global database
    
    if hotel_id in [hotel["id"] for hotel in database]:
        edited_hotel = database[hotel_id]
        edited_hotel['city'] = edited_hotel['city'] if city is None else city
        edited_hotel['name'] = edited_hotel['name'] if city is None else name
                
        database[-1].update(edited_hotel)
        
        return {"Status": "OK"}
        
    return {"Status": "NOT NOK"}

@app.post('/hotels')
def create_hotel(
        city: str = Body(embed=True, description="Название города"),
        name: str = Body(embed=True, description="Название отеля")
):
    global database
    last_hotel = database[-1]
    
    last_id = int(last_hotel['id'])
    
    new_hotel = {
        'id': int(last_id + 1),
        'city': city,
        "name": name
    }
    
    database.append(new_hotel)
    
    return {"Status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
