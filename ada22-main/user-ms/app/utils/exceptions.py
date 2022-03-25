from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND


unauthorized = HTTPException(
    status_code=HTTP_401_UNAUTHORIZED,
    detail="Authentication failed",
    headers={"WWW-Authenticate": "Bearer"})


not_found = HTTPException(
    status_code=HTTP_404_NOT_FOUND,
    detail="Not found")
