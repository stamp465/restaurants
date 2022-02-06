from fastapi import FastAPI, Query
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

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
    result = collection.find({"name":name},{"_id" : 0})
    l_result = []
    for r in result:
        l_result.append(r)
    if(l_result != None):
        return {
            "result":l_result
        }
    return {
        "result" : "Not found"
    }
    
@app.get("reservation/by-table/{table}")
def get_reservation_by_table(table: int):
    result = collection.find_one({"table":table},{"_id" : 0})
    l_result = []
    for r in result:
        l_result.append(r)
    if(l_result != None):
        return {
            "result":l_result
        }
    return {
        "result" : "Not found"
    }
    
@app.post("/reservation")
def reserve(reservation : Reservation):
    m = jsonable_encoder(reservation)
    table_number = m["table_number"]
    time = m["time"]
    c = collection.find_one({"table_number": table_number,"time":time})
    if (c != None):
        return{
            "result" : "That time was already reserved, please book again."
        }
    collection.insert_one(m)
    return{
        "result" : "Complete!Thank you for choosing restaurant"
    }
    

@app.put("/reservation/update/")
def update_reservation(reservation: Reservation):
    m = jsonable_encoder(reservation)
    name = m["name"]
    table_number = m["table_number"]
    time = m["time"]
    c = collection.find_one({"table_number": table_number,"time":time})
    if (c != None):
        return{
            "result" : "That time was already reserved, please book again."
        }
    query = {"name" : name}
    newvalues = {"$set":{"table_number":table_number,"time":time}}
    collection.update_one(query,newvalues)
    return{
        "result" : "Complete!Thank you for choosing restaurant"
    }
    

@app.delete("/reservation/delete/{name}/{table_number}")
def cancel_reservation(name: str, table_number : int):
    query = {"name":name,"table_number":table_number}
    collection.delete_one(query)
    return {
        "result" : "Cancellation has been done"
    }

