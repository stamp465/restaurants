from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel

class Reservation(BaseModel):
    name : str
    time: int
    table_number: int
    
client = MongoClient('mongodb://localhost', 27017)

# TODO fill in database name
db = client["reservation"]

# TODO fill in collection name
collection = db["reserve"]

app = FastAPI()


# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    result = collection.find({"name":name},{"_id": 0, "name": 1,"time":1,"table_number":1})
    my_result = []
    for r in result:
        my_result.append(r)
    print(my_result)
    return my_result

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find({"table_number":table},{"_id": 0, "name": 1,"time":1,"table_number":1})
    my_result = []
    for r in result:
        my_result.append(r)
    print(my_result)
    return my_result

@app.post("/reservation")
def reserve(reservation : Reservation):
    collection.insert_one(Reservation)

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    pass

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    pass