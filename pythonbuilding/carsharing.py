from fastapi import FastAPI, HTTPException, Depends, Request
from typing import Annotated
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from sqlmodel import SQLModel, Session, select
from pythonbuilding.db import get_session, engine
from pythonbuilding.schemas import Car, TripOutput, TripInput, Trip
from pythonbuilding.routers import car, web, user

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="Car Sharing", lifespan=lifespan)
app.include_router(web.router)
app.include_router(car.router)
app.include_router(user.router)

@app.exception_handler(car.BadTripException)
async def unicorn_exception_handler(request: Request, exc : car.BadTripException):
    return JSONResponse(
        status_code=422,
        content={"message": "Bad Trip"}
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
        raise HTTPException(status_code=404, detail=f"No car with id={car_id}.")

@app.get("/api/alltrips", response_model=list[TripOutput])
def get_all_trips(session: Annotated[Session, Depends(get_session)]):
    trips = session.exec(select(Trip)).all()
    return [TripOutput.model_validate(t) for t in trips]


