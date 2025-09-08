import json

from sqlmodel import SQLModel, Field, Relationship

class TripInput(SQLModel):
    start : int
    end : int
    description : str

class TripOutput(TripInput):
    id: int



class Trip(TripInput, table=True):
   id: int | None = Field(primary_key=True, default= None)
   car_id: int = Field(foreign_key="car.id")
   car: "Car" = Relationship(back_populates="trips")
    
class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    model_config = {
        "json_schema_extra": {
            "example" : {
                "size" : "m",
                "doors" : 5,
                "transmission" : "manual",
                "fuel" : "hybrid"
                
            }

            
        }
                }

class CarOutput(CarInput):
    id : int
    trips : list[TripOutput] = []
    
class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default= None)
    trips: list[Trip] = Relationship(back_populates="car")


class CarUpdate(CarInput):

    size: str | None = None
    fuel: str | None = None
    doors: int | None = None
    transmission: str | None = None 