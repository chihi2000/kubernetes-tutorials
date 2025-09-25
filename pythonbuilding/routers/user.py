from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException  
from sqlmodel import Session, select
from pythonbuilding.db import engine, get_session
from pythonbuilding.schemas import User, UserInput, hash_password, UserOutput
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status

URL_PREFIX = "/auth"
router = APIRouter(prefix = "/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{URL_PREFIX}/token")

def create_user(user_input: UserInput, session: Session) -> UserOutput:
    existing_user = session.query(User).filter(User.username == user_input.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(
        username=user_input.username,
        password_hash=hash_password(user_input.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOutput(id=user.id, username=user.username)




@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                session: Annotated[Session, Depends(get_session)]):
    query = select(User).where(User.username== form_data.username)
    user  = session.exec(query).first()
    if user and user.verify_password(form_data.password):
        return {"access_token": user.username, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail = "Inccorect username or password")

#  enforce logging in dependency
def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    session: Annotated[Session, Depends(get_session)]
) -> UserOutput:
    query = select(User).where(User.username == token)
    user = session.exec(query).first()
    if user :
        return UserOutput.model_validate(user)  
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
            headers= {"WWW-Authenticate": "Bearer"}
        )