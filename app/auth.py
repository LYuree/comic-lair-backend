from fastapi import status, FastAPI, HTTPException, Depends, Security, Request
import jwt #pip install pyjwt https://pypi.org/project/PyJWT/
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
# from routes import get_user
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import User
from typing import Annotated

from app.certificates.secrecy import JWT_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Authenticate the user
async def authenticate_user(username: str, password: str, db):
    # user = await get_user.filter(id=payload['sub']).first()
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise jwt.JsonHTTPException()
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: str, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role' : role}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, JWT_SECRET, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Token is invalid or expired")
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token is invalid or expired")
    
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/token")

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        # user_id: int = payload.get('id')
        user_id: str = payload.get('id') # the idiot Robby has integer user id's all over the place...
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user.')
        return {'username': username, 'id': user_id}
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Could not validate user.')

user_dependency = Annotated[dict, Depends(get_current_user)]