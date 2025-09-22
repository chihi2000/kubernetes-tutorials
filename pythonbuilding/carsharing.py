import statistics
from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Annotated

from fastapi.responses import JSONResponse
from pythonbuilding.db import get_session
from pythonbuilding.schemas import Car, CarOutput, TripOutput, TripInput, Trip
from sqlmodel import SQLModel, Field, Session, select
from contextlib import asynccontextmanager
from pythonbuilding.db import engine
from pythonbuilding.routers import car, web, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Car Sharing", lifespan=lifespan)
app.include_router(car.router)
app.include_router(web.router)
app.include_router(user.router)

@app.exception_handler(car.BadTripException)
async def unicorn_exception_handler(request: Request, exc : car.BadTripException):
    return JSONResponse(
        status_code=statistics.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Bad Trip"}, 
    )

@app.post("/api/cars/{car_id}/trips")
def add_trip(session: Annotated[Session, Depends(get_session)],
             car_id: int, trip_input: TripInput) -> Trip:

    car = session.get(Car, car_id)
    if car:
        new_trip = Trip.model_validate(trip_input, update={'car_id': car_id})
        car.trips.append(new_trip)  
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.get("/api/alltrips", response_model=list[TripOutput])
async def get_all_cars(session: Session = Depends(get_session)):
    trips = session.exec(select(Trip)).all()
    return [TripOutput.model_validate(t) for t in trips]


# @app.middleware("http")
# async def ad_cars_cookies(request: Request, call_next):
#     response = await call_next(request)
#     response.set_cookie(key = "cars_cookie", value="you_visited_carsharing_app")
#     return response