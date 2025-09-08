
from pythonbuilding.db import get_session
from pythonbuilding.schemas import Car, CarInput, CarOutput, CarUpdate
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select
 
router = APIRouter(prefix="/api/cars")
 
@router.get("/allcars", response_model=list[CarOutput])
async def get_all_cars(session: Session = Depends(get_session)):
    cars = session.exec(select(Car)).all()
    return [CarOutput.model_validate(c) for c in cars]


@router.get("/")
def get_cars(
    size: str | None = None,
    doors: int | None = None,
    session: Session = Depends(get_session)
) -> list:
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)
    return session.exec(query).all()


@router.get("/{id}", response_model=CarOutput)
def car_by_id(id: int, session: Session = Depends(get_session)):
    car = session.get(Car, id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return CarOutput.model_validate(car)


@router.post("/", response_model=CarOutput)
def add_car(car_input: CarInput, session: Session = Depends(get_session)):
    new_car = Car.model_validate(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car


@router.patch("/{id}", response_model=CarOutput)
def update_car(id: int, car_update: CarUpdate, session: Session = Depends(get_session)) -> CarOutput:
    db_car = session.get(Car, id)
    if not db_car:
        raise HTTPException(status_code=404, detail="Car does not exist")

    update_data = car_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        setattr(db_car, key, value)

    session.commit()
    session.refresh(db_car)

    return CarOutput.model_validate(db_car)


@router.delete("/{id}")
def delete_car (id : int, session : Session = Depends(get_session)):
    db_car = session.get(Car, id)
    if not db_car:
        raise HTTPException(status_code=404, detail = "Car already not existing")
    session.delete(db_car)
    session.commit()
    return {"detail": "Car deleted successfully"}