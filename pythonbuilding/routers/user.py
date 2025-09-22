from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException  # Remove 'security' from here
from sqlmodel import Session, select
from pythonbuilding.db import engine, get_session
from pythonbuilding.schemas import User, UserInput, hash_password, UserOutput
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # Import properly
from starlette import status


security = HTTPBasic()

router = APIRouter(prefix="/api/users")

@router.post("/signup", response_model=UserOutput)
def create_user(user_input: UserInput):
    with Session(engine) as session:
        # Check if username exists
        existing_user = session.exec(select(User).where(User.username == user_input.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")

        # create new user
        user = User(
            username=user_input.username,
            password_hash=hash_password(user_input.password)
        )

        session.add(user)
        session.commit()
        session.refresh(user)
    
    # return user (without password)
    return UserOutput(id=user.id, username=user.username)

#  enforce logging in dependency
def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],  # Now using the instance
    session: Annotated[Session, Depends(get_session)]
) -> UserOutput:
    query = select(User).where(User.username == credentials.username)
    user = session.exec(query).first()
    if user and user.verify_password(credentials.password):
        return UserOutput.model_validate(user)  
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
        )