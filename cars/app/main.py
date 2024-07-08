

from .cars import create_cars
from fastapi import FastAPI, Response, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel

cars = create_cars(100)  # Здесь хранятся список машин
app = FastAPI()


@app.get("/")
def index():
    return Response("<a href='/cars'>Cars</a>")

class Car(BaseModel):
    id: int
    name: str
    year: str
@app.get("/cars")
def get_cars(page: Optional[int] = Query(default=1, ge=1), limit: Optional[int] = Query(default=10, ge=1, le=100)):
    start_index = (page - 1) * limit
    end_index = start_index + limit
    return cars[start_index:end_index]

# Роут для получения информации о машине по её id
@app.get("/cars/{id}")
def get_car_by_id(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    raise HTTPException(status_code=404, detail="Not found")