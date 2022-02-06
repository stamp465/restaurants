from shelve import BsdDbShelf
from pymongo import MongoClient

from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Reservation(BaseModel):
    name : str
    time: float
    table_number: int
    
client = MongoClient('mongodb://localhost', 27018)

# TODO fill in database name
db = client["reservation"]

# TODO fill in collection name
collection = db["reserve"]

app = FastAPI()

@app.get("/")
def get_roots():
    return "Welcome to restaurants"

@app.get("/reservation")
def get_all_reservation():
    return [ r for r in collection.find({},{"_id":0}) ]

# TODO complete all endpoint.
@app.get("/reservation/by-name/{name}")
def get_reservation_by_name(name:str):
    return [ r for r in collection.find({"name":name},{"_id":0}) ]

@app.get("/reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    return [ r for r in collection.find({"table_number":table},{"_id":0}) ]

@app.post("/reservation")
def reserve(reservation : Reservation):
    result = collection.find({"table_number":reservation.table_number},{"_id":0})
    for i in result :
        if reservation.time == i["time"] :
            return {
                f'''Suppose that on table number {reservation.table_number} has a reservation at {reservation.time}:00. You can't make a reservation on that time and that table.'''
            }
    a = jsonable_encoder(reservation)
    collection.insert_one(a)
    return {
        "result" : "reserve done"
    }

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    myquery = { 
        "name": reservation.name,
        "table_number" : reservation.table_number
    }
    newvalues = { "$set": { "time": reservation.time } }
    
    result = collection.find({"table_number":reservation.table_number},{"_id":0})
    for i in result :
        if reservation.time == i["time"] :
            return {
                f'''Suppose that on table number {reservation.table_number} has a reservation at {reservation.time}:00. You can't make a reservation on that time and that table.'''
            }
    print(myquery,newvalues)
    collection.update_one(myquery, newvalues)
    return {
        "result" : "update_one done"
    }

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    data = {
        "name" : name,
        "table_number" : table_number
    }
    collection.delete_one(data)
    return {
        "result" : "delete done"
    }

