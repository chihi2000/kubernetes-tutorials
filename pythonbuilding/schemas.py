from sqlmodel import SQLModel, Field, Relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Password utils
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


# Trip models
class TripInput(SQLModel):
    start: int
    end: int
    description: str

class TripOutput(TripInput):
    id: int

class Trip(TripInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    car_id: int = Field(foreign_key="car.id")
    car: "Car" = Relationship(back_populates="trips")


# Car models
class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"

    model_config = {
        "json_schema_extra": {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }
    }

class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []

class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    trips: list[Trip] = Relationship(back_populates="car")

class CarUpdate(CarInput):
    size: str | None = None
    fuel: str | None = None
    doors: int | None = None
    transmission: str | None = None


# User models
class UserInput(SQLModel):
    username: str
    password: str

class User(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    username: str
    password_hash: str

class UserOutput(SQLModel):
    id: int
    username: str
